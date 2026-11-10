#!/usr/bin/env python3
"""Create, refresh, extract and render a single offline readiness report. Stdlib only."""
import argparse
import base64
import copy
from datetime import datetime, timezone
import hashlib
import html
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import uuid

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = json.loads((ROOT / 'assets/checklist.json').read_text(encoding='utf-8'))
DATA_RE = re.compile(r'<script id="readiness-data" type="application/json">(.*?)</script>', re.S)
STATUSES = {'pass': 'Spełnione', 'fail': 'Wymaga poprawy', 'unverified': 'Do sprawdzenia', 'stale': 'Sprawdź ponownie'}
OWNERS = {'agent': 'Agent', 'human': 'Użytkownik'}
STAGES = {'preparation': 'Przygotowanie do wdrożenia', 'deployment': 'Sprawdzenie wdrożenia',
          'observation': 'Obserwacja działania'}
ENVIRONMENT_KINDS = {'local': 'Lokalne', 'development': 'Dev', 'preview': 'Preview',
                     'staging': 'Staging', 'production': 'Produkcja'}
ENVIRONMENT_FIELDS = ('id', 'kind', 'name', 'address', 'version', 'source_version', 'config_revision', 'available')


def environment(model, item):
    return next((env for env in model['environments'] if env['id'] == item['environment_id']), None)


def waiting_reason(model, item):
    if item['applicability'] == 'no':
        return ''
    state = model['context']['release_state']
    if item['stage'] == 'deployment' and state == 'not_deployed':
        return 'Do sprawdzenia po wdrożeniu'
    if item['stage'] == 'observation' and state != 'live':
        return 'Do obserwacji po udostępnieniu'
    env = environment(model, item)
    if item['stage'] == 'preparation' and env and not env['available']:
        return 'Czeka na środowisko testowe'
    return ''


def evidence_current(model, item, record):
    env = environment(model, item)
    return bool(env and env['available'] and env['kind'] in item['environment_kinds'] and
                all(nonempty(env[key]) for key in ('address', 'version', 'source_version', 'config_revision')) and
                nonempty(model['context']['source_version']) and
                env['source_version'] == model['context']['source_version'] and
                record.get('environment') == {key: env[key] for key in ENVIRONMENT_FIELDS} and
                record.get('source_version') == model['context']['source_version'] and
                record.get('stage') == item['stage'] and record['audit_id'] == model['audit']['id'] and
                not waiting_reason(model, item))


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def timestamp(value):
    require(nonempty(value), 'Missing timestamp')
    date = datetime.fromisoformat(value.replace('Z', '+00:00'))
    require(date.tzinfo is not None, 'Timestamps need a timezone')


def repo_info(repo, output):
    """Record identity and dirtiness; never execute project scripts or store a diff."""
    def git(*args):
        result = subprocess.run(['git', '-C', str(repo), *args], capture_output=True, text=True, timeout=20)
        return result.stdout.strip() if result.returncode == 0 else None
    commit = git('rev-parse', 'HEAD')
    relative = output.relative_to(repo).as_posix()
    status = git('status', '--porcelain', '--untracked-files=all', '--', '.', ':(exclude)' + relative)
    listing = subprocess.run(['git', '-C', str(repo), 'ls-files', '-z', '--cached', '--others', '--exclude-standard'],
                             capture_output=True, timeout=20)
    fingerprint = None
    if listing.returncode == 0:
        digest = hashlib.sha256()
        for raw in sorted(set(listing.stdout.split(b'\0')) - {b''}):
            path = repo / os.fsdecode(raw)
            if path.resolve() == output.resolve():
                continue
            digest.update(raw + b'\0')
            if path.is_symlink():
                digest.update(b'link:' + os.fsencode(os.readlink(path)))
            elif path.is_file():
                with path.open('rb') as stream:
                    for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                        digest.update(chunk)
            else:
                digest.update(b'missing-or-submodule')
            digest.update(b'\0')
        fingerprint = digest.hexdigest()
    return {'name': repo.name, 'commit': commit, 'dirty': bool(status) if status is not None else None,
            'fingerprint': fingerprint}


def new_model(repo, output):
    project = repo_info(repo, output)
    version = project['fingerprint'] or project['commit'] or ''
    items = copy.deepcopy(TEMPLATE['items'])
    for item in items:
        item.update(applicability='yes' if item['condition'] == 'Zawsze' else 'unknown',
                    applicability_reason='', status='unverified', finding='Nie sprawdzono jeszcze tego wymagania.',
                    owner='agent', evidence=[], risk_acceptance=None,
                    environment_id='local' if 'local' in item['environment_kinds'] else None)
    return {'schema_version': 2, 'template_version': TEMPLATE['version'], 'revision': 0,
            'audit': {'id': str(uuid.uuid4()), 'started_at': now(), 'phase': 'in_progress'},
            'project': project,
            'context': {'hosting': 'Nie ustalono', 'audience': 'Nie ustalono', 'data': 'Nie ustalono',
                        'outage_impact': 'Nie ustalono', 'scope_confirmed': False,
                        'target_stage': 'preparation', 'release_state': 'not_deployed', 'source_version': version},
            'environments': [{'id': 'local', 'kind': 'local', 'name': 'Lokalne repozytorium',
                              'address': 'repo:' + str(repo), 'version': version, 'source_version': version,
                              'config_revision': '', 'available': True}],
            'items': items, 'next_item_id': 'environment', 'history': []}


def extract(path):
    raw = path.read_text(encoding='utf-8')
    blocks = DATA_RE.findall(raw)
    require(len(blocks) == 1, 'Expected exactly one embedded readiness-data block')
    model = json.loads(blocks[0])
    validate(model)
    model['_base_digest'] = hashlib.sha256(raw.encode()).hexdigest()
    return model


def validate(model):
    require(isinstance(model, dict) and model.get('schema_version') == 2,
            'Only new schema-2 reports are supported. Existing reports are not migrated or modified; use init with a different --output.')
    require(model.get('template_version') == TEMPLATE['version'], 'Unsupported template version; create a new report')
    require(type(model.get('revision')) is int and model['revision'] >= 0, 'Invalid revision')
    audit = model['audit']
    require(nonempty(audit['id']) and audit['phase'] in {'in_progress', 'complete'}, 'Invalid audit')
    timestamp(audit['started_at'])
    context = model['context']
    require(context['target_stage'] in STAGES, 'Unknown target stage')
    require(context['release_state'] in {'not_deployed', 'deployed', 'live'}, 'Invalid release state')
    require(isinstance(context['source_version'], str), 'Invalid source version')
    require(type(context['scope_confirmed']) is bool, 'scope_confirmed must be boolean')
    for field in ('hosting', 'audience', 'data', 'outage_impact'):
        require(nonempty(context[field]), 'Missing context: ' + field)
        if context['scope_confirmed']:
            require(context[field] != 'Nie ustalono', 'Unresolved context: ' + field)
    require(nonempty(model['project']['name']), 'Missing project name')
    require(model['project']['dirty'] is None or type(model['project']['dirty']) is bool, 'Invalid dirty flag')
    require(model['project']['commit'] is None or nonempty(model['project']['commit']), 'Invalid commit')
    known_source = model['project']['fingerprint'] or model['project']['commit']
    require(not known_source or context['source_version'] == known_source,
            'Source version must match the recorded repository state; refresh after source changes')
    require(isinstance(model['history'], list), 'Invalid history')
    require(isinstance(model['environments'], list) and model['environments'], 'Missing environments')
    environment_ids = set()
    for env in model['environments']:
        require(nonempty(env['id']) and env['id'] not in environment_ids, 'Invalid or duplicate environment ID')
        environment_ids.add(env['id'])
        require(env['kind'] in ENVIRONMENT_KINDS and nonempty(env['name']), 'Invalid environment')
        require(type(env['available']) is bool, 'Invalid environment availability')
        for field in ('address', 'version', 'source_version', 'config_revision'):
            require(isinstance(env[field], str), 'Invalid environment ' + field)
    require(isinstance(model['items'], list) and model['items'], 'Checklist cannot be empty')
    ids = set()
    categories = {c['id'] for c in TEMPLATE['categories']}
    baseline = {i['id']: i for i in TEMPLATE['items']}
    for item in model['items']:
        require(nonempty(item['id']) and re.fullmatch(r'[a-z0-9][a-z0-9-]*', item['id']), 'Invalid item ID')
        require(item['id'] not in ids, 'Duplicate item: ' + item['id'])
        ids.add(item['id'])
        require(item['category'] in categories, 'Unknown category')
        require(type(item['required']) is bool, 'required must be boolean')
        require(item['priority'] in {'high', 'normal'}, 'Invalid priority')
        require(item['stage'] in STAGES, 'Invalid item stage')
        require(isinstance(item['environment_kinds'], list) and item['environment_kinds'] and
                set(item['environment_kinds']).issubset(ENVIRONMENT_KINDS), 'Invalid environment kinds')
        require(item['environment_id'] is None or item['environment_id'] in environment_ids, 'Unknown item environment')
        env = environment(model, item)
        require(not env or env['kind'] in item['environment_kinds'], 'Wrong environment kind for ' + item['id'])
        for field in ('title', 'why', 'condition', 'verification', 'finding', 'rationale'):
            require(nonempty(item[field]), 'Missing ' + field + ' on ' + item['id'])
        require(isinstance(item['steps'], list) and item['steps'] and all(nonempty(s) for s in item['steps']), 'Missing steps')
        if item['id'] in baseline:
            base = baseline[item['id']]
            require(item['origin'] == 'baseline' and item['category'] == base['category'], 'Baseline identity changed')
            require(not base['required'] or item['required'], 'Cannot weaken a baseline requirement')
            require(item['stage'] == base['stage'] and item['environment_kinds'] == base['environment_kinds'],
                    'Cannot change baseline stage or environment kinds')
            if base['condition'] == 'Zawsze':
                require(item['applicability'] == 'yes', 'An unconditional baseline cannot be excluded')
        else:
            require(item['origin'] == 'custom', 'New criteria need custom origin and rationale')
        require(item['applicability'] in {'yes', 'no', 'unknown'}, 'Invalid applicability')
        if item['applicability'] == 'no':
            require(nonempty(item['applicability_reason']), 'Exclusion requires a reason')
        require(item['status'] in STATUSES and item['owner'] in OWNERS, 'Invalid status or owner')
        require(isinstance(item['evidence'], list), 'Evidence must be a list')
        for ev in item['evidence']:
            require(ev['kind'] in {'agent', 'human'}, 'Invalid evidence source')
            for field in ('source', 'result', 'audit_id'):
                require(nonempty(ev[field]), 'Incomplete evidence: ' + field)
            timestamp(ev['checked_at'])
            require(ev['stage'] == item['stage'], 'Evidence stage does not match the check')
            require(nonempty(ev['source_version']) and isinstance(ev['environment'], dict), 'Missing evidence identity')
            for field in ENVIRONMENT_FIELDS:
                require(field in ev['environment'], 'Incomplete evidence environment')
            if ev['kind'] == 'human':
                require(nonempty(ev.get('person')), 'Human confirmation needs a person')
        if item['status'] == 'pass':
            require(item['applicability'] == 'yes', 'Only applicable criteria can pass')
            require(item['evidence'] and all(evidence_current(model, item, ev) for ev in item['evidence']),
                    'Passing requires current evidence for the assessed source, stage, environment and configuration: ' + item['id'])
        risk = item['risk_acceptance']
        if risk is not None:
            require(nonempty(risk['person']) and nonempty(risk['reason']), 'Risk acceptance needs who and why')
            timestamp(risk['recorded_at'])
    require(set(baseline).issubset(ids), 'Baseline criteria cannot be removed')
    require(model['next_item_id'] is None or model['next_item_id'] in ids, 'Unknown next item')


def is_pass(item, model):
    return item['applicability'] == 'yes' and item['status'] == 'pass' and bool(item['evidence']) and all(
        evidence_current(model, item, record) for record in item['evidence'])


def metrics(model, items=None, stage=None):
    stage = stage or model['context']['target_stage']
    items = model['items'] if items is None else items
    required = [i for i in items if i['stage'] == stage and i['required'] and i['applicability'] != 'no']
    passed = sum(is_pass(i, model) for i in required)
    total = len(required)
    waiting = sum(bool(waiting_reason(model, i)) and i['status'] != 'fail' and not is_pass(i, model)
                  for i in required)
    return {'passed': passed, 'total': total, 'score': passed * 100 // total if total else None,
            'blockers': total - passed, 'waiting': waiting, 'actionable': total - passed - waiting}


def verdict(model, stage=None):
    stage = stage or model['context']['target_stage']
    result = metrics(model, stage=stage)
    if stage == 'deployment' and model['context']['release_state'] == 'not_deployed':
        return 'Do sprawdzenia po wdrożeniu'
    if stage == 'observation' and model['context']['release_state'] != 'live':
        return 'Do obserwacji po udostępnieniu'
    if model['audit']['phase'] != 'complete' or not model['context']['scope_confirmed'] or any(
            i['applicability'] == 'unknown' for i in model['items'] if i['stage'] == stage):
        return 'Ocena nieukończona'
    for earlier in list(STAGES)[:list(STAGES).index(stage)]:
        if metrics(model, stage=earlier)['blockers']:
            return 'Najpierw ukończ: ' + STAGES[earlier].lower()
    if result['blockers']:
        return 'Przygotowanie zablokowane' if stage == 'preparation' else 'Wymaga sprawdzenia lub poprawy'
    if not result['total']:
        return 'Brak podstaw do oceny'
    return {'preparation': 'Gotowe do wdrożenia', 'deployment': 'Wdrożenie sprawdzone',
            'observation': 'Spełnia ustalone kryteria obserwacji'}[stage]


def e(value):
    return html.escape(str(value), quote=True)


def label(item, model):
    if item['applicability'] == 'no':
        return 'Nie dotyczy'
    if item['status'] == 'fail':
        return STATUSES['fail']
    if item['status'] == 'stale':
        return STATUSES['stale']
    if item['applicability'] == 'unknown':
        return waiting_reason(model, item) or 'Ustal, czy dotyczy'
    return waiting_reason(model, item) or STATUSES[item['status']]


def next_item(model):
    stages = list(STAGES)
    target_index = stages.index(model['context']['target_stage'])
    pending = [i for i in model['items'] if i['applicability'] != 'no' and not is_pass(i, model) and
               stages.index(i['stage']) <= target_index and
               (not waiting_reason(model, i) or i['stage'] == 'preparation' or i['status'] == 'fail')]
    # A future manual selection must not displace an actionable prerequisite.
    first_stage = min((stages.index(i['stage']) for i in pending if i['required']), default=target_index)
    pending = [i for i in pending if stages.index(i['stage']) <= first_stage]
    chosen = next((i for i in pending if i['id'] == model['next_item_id']), None)
    return chosen or next(iter(sorted(pending, key=lambda i: (not i['required'], i['priority'] != 'high'))), None)


def item_html(item, model):
    waiting = waiting_reason(model, item)
    unresolved = item['applicability'] != 'no' and not is_pass(item, model)
    relevant = list(STAGES).index(item['stage']) <= list(STAGES).index(model['context']['target_stage'])
    kind = ('excluded' if item['applicability'] == 'no' else 'passed' if is_pass(item, model) else
            'waiting' if waiting and item['status'] != 'fail' else
            'recommendation' if not item['required'] else 'blocker' if unresolved and relevant else 'pending')
    status = ('excluded' if item['applicability'] == 'no' else 'waiting' if waiting and item['status'] not in {'fail', 'stale'} else
              'unknown' if item['applicability'] == 'unknown' else item['status'])
    evidence = ''
    for ev in item['evidence']:
        env = ev['environment']
        identity = f"{env['name']} | {env['address']} | wdrożenie: {env['version']} | konfiguracja: {env['config_revision']} | źródła: {ev['source_version']}"
        evidence += ('<li><strong>' + e('Potwierdzenie: ' + ev['person'] if ev['kind'] == 'human' else 'Sprawdzenie agenta') +
                     '</strong><p>' + e(ev['result']) + '</p><code>' + e(ev['source']) + '</code><p class="muted">' +
                     e(STAGES[ev['stage']]) + ' | ' + e(identity) + '</p><p class="muted">' +
                     e(ev['checked_at']) + (' - wymaga ponownej oceny' if not evidence_current(model, item, ev) else '') + '</p></li>')
    risk = item['risk_acceptance']
    acceptance = ('<aside class="risk"><strong>Zaakceptowano ryzyko - wymaganie nadal oceniane osobno</strong><p>' +
                  e(risk['person']) + ': ' + e(risk['reason']) + '</p><small>' + e(risk['recorded_at']) + '</small></aside>') if risk else ''
    steps = ''.join('<li>' + e(s) + '</li>' for s in item['steps'])
    exclusion = ('<p><strong>Dlaczego nie dotyczy:</strong> ' + e(item['applicability_reason']) + '</p>') if item['applicability'] == 'no' else ''
    env = environment(model, item)
    location = env['name'] if env else 'Agent ustali miejsce sprawdzenia tego punktu.'
    kinds = ', '.join(ENVIRONMENT_KINDS[k] for k in item['environment_kinds'])
    return f'''<details class="check" id="{e(item['id'])}" data-kind="{kind}" data-stage="{e(item['stage'])}" data-environment="{e(env['kind'] if env else 'unassigned')}" data-environments="{e(' '.join(item['environment_kinds']))}" data-category="{e(item['category'])}">
<summary class="check-summary"><span class="badge {kind} status-{status}">{e(label(item, model))}</span><span class="check-title">{e(item['title'])}</span></summary>
<div class="check-body">
<p class="muted">{'Wymagane na tym etapie' if item['required'] else 'Zalecane usprawnienie'} | Następny krok: {e(OWNERS[item['owner']])}</p>
<p><strong>Miejsce sprawdzenia:</strong> {e(location)}</p>
<p>{e(item['finding'])}</p>{exclusion}{acceptance}
<p><strong>Dlaczego to ważne:</strong> {e(item['why'])}</p><h4>Co zrobić krok po kroku</h4><ol>{steps}</ol>
<p><strong>Jak potwierdzimy:</strong> {e(item['verification'])}</p><p class="muted">Kiedy dotyczy: {e(item['condition'])}</p>
<p class="muted">Uzasadnienie wymagania: {e(item['rationale'])}</p>
<details><summary>Dowody i szczegóły techniczne ({len(item['evidence'])})</summary><ul class="evidence">{evidence or '<li>Brak potwierdzenia. Ten punkt wymaga sprawdzenia.</li>'}</ul><p class="muted">ID: {e(item['id'])} | {e(STAGES[item['stage']])}</p><p class="muted">Możliwe środowiska: {e(kinds)}</p></details></div></details>'''


def checklist_sections(model, items, prefix='cat-'):
    sections = []
    for cat in TEMPLATE['categories']:
        selected = [i for i in items if i['category'] == cat['id']]
        if selected:
            sections.append(f'<section class="category-section" id="{e(prefix + cat["id"])}"><h2>{e(cat["title"])}</h2><p class="muted">{e(cat["description"])}</p><div class="check-list">' + ''.join(item_html(i, model) for i in selected) + '</div></section>')
    return ''.join(sections)


def other_stages_html(model):
    stages = list(STAGES)
    target = stages.index(model['context']['target_stage'])
    previous, later = [], []
    for index, stage in enumerate(stages):
        if index == target:
            continue
        items = [i for i in model['items'] if i['stage'] == stage]
        stats = metrics(model, stage=stage)
        if index < target:
            title = ('Do ponownego sprawdzenia: ' if stats['blockers'] else 'Wcześniej sprawdzone: ') + STAGES[stage].lower()
            description = (f'{stats["passed"]}/{stats["total"]} wymagań potwierdzonych. '
                           'Wyniki dotyczą zapisanej wersji i konfiguracji. Po zmianach wymagają ponownego sprawdzenia.')
        else:
            title = 'Po wdrożeniu' if stage == 'deployment' else 'Po rozpoczęciu korzystania z aplikacji'
            description = ('Gdy aplikacja będzie wdrożona, uruchom skill ponownie i podaj jej adres produkcyjny. Sprawdzimy działające wdrożenie: m.in. logowanie, połączenie, konfigurację i alarmy.'
                           if stage == 'deployment' else 'Te punkty wymagają rzeczywistego użycia aplikacji. Sprawdzimy je później na odpowiedniej próbce ruchu, błędów i kosztów.')
        opened = ' open' if index < target and stats['blockers'] else ''
        count = f'{stats["passed"]}/{stats["total"]} wymagań' if index < target else f'Punkty: {len(items)}'
        group = f'<details class="stage-group" data-stage="{stage}"{opened}><summary>{e(title)} <span>{e(count)}</span></summary><p>{e(description)}</p>' + checklist_sections(model, items, 'other-' + stage + '-') + '</details>'
        (previous if index < target else later).append(group)
    return ''.join(previous), ''.join(later)


def completed_audit_history(snapshots, current):
    """Keep the latest completed checkpoint per audit and stage."""
    current_key = (current['audit']['id'], current['context']['target_stage'])
    latest = {}
    for snapshot in snapshots:
        if snapshot['audit']['phase'] != 'complete':
            continue
        key = (snapshot['audit']['id'], snapshot['context']['target_stage'])
        if current['audit']['phase'] == 'complete' and key == current_key:
            continue  # The latest completed result is already the current report.
        latest.pop(key, None)
        latest[key] = snapshot
    return list(latest.values())


def document(model):
    validate(model)
    result = metrics(model)
    stage = model['context']['target_stage']
    score = str(result['score']) + '%' if result['score'] is not None else 'Brak oceny'
    selected = next_item(model)
    if selected:
        access_step = ('Zapewnij dostęp do środowiska testowego, aby sprawdzić: '
                       if selected['stage'] == 'preparation' and waiting_reason(model, selected) else '')
        next_html = f'<span class="next-label">Następny krok | {e(OWNERS[selected["owner"]])}</span><a class="jump" href="#{e(selected["id"])}">{e(access_step + selected["title"])}</a>'
    elif model['audit']['phase'] != 'complete' or not model['context']['scope_confirmed']:
        next_html = '<span class="next-label">Następny krok | Agent i użytkownik</span><span>Dokończ ustalenie zakresu oceny</span>'
    else:
        stage = model['context']['target_stage']
        action = {'preparation': 'Wdróż aplikację, a potem uruchom ten skill ponownie i podaj adres produkcyjny.',
                  'deployment': 'Ustal udostępnienie użytkownikom i kryteria obserwacji.',
                  'observation': 'Utrzymuj monitoring i ponów ocenę po zmianie wersji lub konfiguracji.'}[stage]
        if waiting_reason(model, {'stage': stage, 'applicability': 'yes', 'environment_id': None}):
            action = ('Wróć do kontroli wdrożenia, gdy ta wersja będzie dostępna pod docelowym adresem.'
                      if stage == 'deployment' else 'Rozpocznij obserwację po udostępnieniu tej wersji użytkownikom.')
        next_html = '<span class="next-label">Następny krok | Użytkownik</span><span>' + e(action) + '</span>'
    categories = []
    current_items = [i for i in model['items'] if i['stage'] == stage]
    short_categories = {'access': 'Dostęp', 'data': 'Dane', 'behavior': 'Działanie',
                        'release': 'Wdrożenie', 'monitoring': 'Monitoring', 'recovery': 'Awarie'}
    for cat in TEMPLATE['categories']:
        items = [i for i in current_items if i['category'] == cat['id']]
        if not items:
            continue
        stats = metrics(model, items)
        percent = str(stats['score']) + '%' if stats['score'] is not None else 'Zalecenia'
        category_description = f'{cat["title"]}: {stats["passed"]}/{stats["total"]} wymagań, otwarte: {stats["blockers"]}'
        categories.append(f'<a class="category jump" href="#cat-{cat["id"]}" title="{e(category_description)}" aria-label="{e(category_description)}"><strong>{e(short_categories[cat["id"]])}</strong><span>{percent}</span></a>')
    sections = checklist_sections(model, current_items)
    previous, later = other_stages_html(model)
    workflow_titles = {'preparation': 'Przed wdrożeniem: sprawdzamy wersję developerską',
                       'deployment': 'Po wdrożeniu: sprawdzamy działającą aplikację',
                       'observation': 'Po wdrożeniu: sprawdzamy rzeczywiste działanie'}
    workflow_descriptions = {
        'preparation': 'Tutaj sprawdzamy i naprawiamy to, co można przygotować na devie przed wdrożeniem. Wynik dotyczy tylko tej części. Po wdrożeniu uruchom skill ponownie z adresem produkcyjnym, żeby sprawdzić pozostałe rzeczy.',
        'deployment': 'Teraz sprawdzamy wdrożoną wersję pod adresem produkcyjnym. Wcześniejsze kontrole z deva są zapisane poniżej. Ten wynik dotyczy kontroli wdrożenia.',
        'observation': 'Teraz sprawdzamy, jak aplikacja działa przy rzeczywistym użyciu. Kontrola samego wdrożenia jest zapisana poniżej. Ocena wymaga odpowiedniej próbki ruchu i kosztów.'}
    issues = sum(i['required'] and i['applicability'] != 'no' and i['status'] == 'fail' for i in current_items)
    unresolved = result['blockers'] - issues
    history = []
    for old in reversed(completed_audit_history(model['history'], model)):
        stats = metrics(old)
        oldscore = str(stats['score']) + '%' if stats['score'] is not None else 'Brak oceny'
        statuses = ''.join('<li>' + e(i['title']) + ' - ' + e(label(i, old)) + '</li>' for i in old['items'])
        history.append(f'<details><summary>Audyt · {e(STAGES[old["context"]["target_stage"]])} · {e(old["saved_at"])} · {oldscore} · Otwarte wymagania: {stats["blockers"]}</summary><p>{e(verdict(old))}</p><ul>{statuses}</ul></details>')
    context = ''.join('<div><dt>' + label_ + '</dt><dd>' + e(model['context'][key]) + '</dd></div>' for key, label_ in
                      [('hosting', 'Gdzie uruchamiamy'), ('audience', 'Dla kogo'), ('data', 'Rodzaj danych'), ('outage_impact', 'Skutki awarii')])
    context += '<div><dt>Aktualny etap oceny</dt><dd>' + e(STAGES[model['context']['target_stage']]) + '</dd></div>'
    context += '<div><dt>Stan udostępnienia</dt><dd>' + e({'not_deployed': 'Przed wdrożeniem', 'deployed': 'Wdrożone, przed udostępnieniem', 'live': 'Udostępnione użytkownikom'}[model['context']['release_state']]) + '</dd></div>'
    for env in model['environments']:
        identity = f"{env['address'] or 'adres nieustalony'} | wersja: {env['version'] or 'nieustalona'} | konfiguracja: {env['config_revision'] or 'nieustalona'} | źródła: {env['source_version'] or 'nieustalone'}"
        context += '<div><dt>' + e(env['name'] + ' (' + ENVIRONMENT_KINDS[env['kind']] + ')') + '</dt><dd><code>' + e(identity) + '</code></dd></div>'
    project = model['project']
    dirty = 'lokalne zmiany' if project['dirty'] else ('czysty stan Git' if project['dirty'] is False else 'stan Git nieznany')
    payload = json.dumps(model, ensure_ascii=False, separators=(',', ':'), allow_nan=False).replace('&', '\\u0026').replace('<', '\\u003c').replace('>', '\\u003e')
    replacements = {'TITLE': e(project['name']), 'SCORE': score, 'PASSED': str(result['passed']), 'TOTAL': str(result['total']),
                    'BLOCKERS': str(result['blockers']), 'VERDICT': e(verdict(model)), 'NEXT': next_html, 'CATEGORIES': ''.join(categories),
                    'SECTIONS': sections, 'CONTEXT': context, 'HISTORY': ''.join(history) or '<p>Brak wcześniejszych zakończonych audytów.</p>',
                    'VERSION': e((project['commit'] or 'Brak commita') + ' · ' + dirty), 'SAVED': e(model.get('saved_at', model['audit']['started_at'])),
                    'PREVIOUS': previous, 'LATER': later, 'STAGETITLE': e(STAGES[stage]),
                    'WORKFLOWTITLE': e(workflow_titles[stage]),
                    'CHECKLISTTITLE': e({'preparation': 'Sprawdzenia przed wdrożeniem', 'deployment': 'Sprawdzenia wdrożonej aplikacji', 'observation': 'Sprawdzenia rzeczywistego działania'}[stage]), 'WORKFLOWDESCRIPTION': e(workflow_descriptions[stage]),
                    'ISSUES': str(issues), 'UNRESOLVED': str(unresolved),
                    'WAITING': str(result['waiting']),
                    'FONT': base64.b64encode((ROOT / 'assets/Geist.woff2').read_bytes()).decode('ascii'),
                    'FONTLICENSE': e((ROOT / 'assets/Geist-OFL.txt').read_text(encoding='utf-8')),
                    'PHASE': 'Sprawdzanie zakończone' if model['audit']['phase'] == 'complete' else 'Trwa sprawdzanie', 'DATA': payload}
    source = (ROOT / 'assets/report.html').read_text(encoding='utf-8')
    # Single substitution pass: user strings that look like placeholders remain literal.
    return re.sub(r'@@([A-Z]+)@@', lambda m: replacements[m.group(1)], source)


def save(model, output):
    validate(model)
    model = copy.deepcopy(model)
    previous = extract(output) if output.exists() else None
    if previous:
        require(model.pop('_base_digest', None) == previous.pop('_base_digest'), 'Report changed; extract again before updating')
        require(model['revision'] == previous['revision'], 'Stale revision')
        current = {i['id']: i for i in model['items']}
        for old in previous['items']:
            require(old['id'] in current, 'Existing criteria cannot be deleted; explain applicability instead')
            require(not old['required'] or current[old['id']]['required'], 'Existing mandatory criteria cannot be downgraded')
        past = copy.deepcopy(previous)
        past.pop('history')
        model['history'] = completed_audit_history(previous['history'] + [past], model)
    else:
        require(model['revision'] == 0 and not model['history'], 'New report must start at revision zero')
        model.pop('_base_digest', None)
    model['revision'] += 1
    model['saved_at'] = now()
    rendered = document(model)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=output.parent, delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(rendered)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, output)
    finally:
        if temporary and temporary.exists():
            temporary.unlink()
    return model


def refresh(model, repo, output):
    model = copy.deepcopy(model)
    model['audit'] = {'id': str(uuid.uuid4()), 'started_at': now(), 'phase': 'in_progress'}
    model['project'] = repo_info(repo, output)
    model['context']['scope_confirmed'] = False
    version = model['project']['fingerprint'] or model['project']['commit']
    if version:
        model['context']['source_version'] = version
        for env in model['environments']:
            if env['kind'] == 'local':
                env['source_version'] = version
                env['version'] = version
    for item in model['items']:
        if item['status'] == 'pass':
            item['status'] = 'stale'
        if item['condition'] != 'Zawsze':
            item['applicability'] = 'unknown'
            item['applicability_reason'] = ''
    return model


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['init', 'extract', 'refresh', 'render', 'validate'])
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=Path('docs/production-readiness.html'))
    parser.add_argument('--input', type=Path, help='Temporary edited JSON, required for render')
    args = parser.parse_args()
    repo = args.repo.resolve(strict=True)
    output = (repo / args.output).resolve()
    require(output.is_relative_to(repo), 'Report must remain inside the target project')
    require(output.suffix.lower() == '.html', 'Output must be HTML')
    if args.command == 'init':
        require(not output.exists(), 'Report exists; use refresh or extract')
        model = save(new_model(repo, output), output)
    elif args.command == 'extract':
        print(json.dumps(extract(output), ensure_ascii=False, indent=2))
        return
    elif args.command == 'refresh':
        model = save(refresh(extract(output), repo, output), output)
    elif args.command == 'render':
        require(args.input is not None, 'render requires --input')
        model = json.loads(args.input.read_text(encoding='utf-8'))
        require(model['project'] == repo_info(repo, output), 'Repository state changed; refresh and recheck evidence')
        model = save(model, output)
    else:
        model = extract(output)
    print(json.dumps({'output': str(output), 'revision': model['revision'], 'verdict': verdict(model), **metrics(model),
                      'stages': {stage: {'verdict': verdict(model, stage), **metrics(model, stage=stage)} for stage in STAGES}}, ensure_ascii=False))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError, subprocess.TimeoutExpired) as error:
        raise SystemExit('Checklist error: ' + str(error))
