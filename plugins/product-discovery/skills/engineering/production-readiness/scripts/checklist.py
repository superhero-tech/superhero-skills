#!/usr/bin/env python3
"""Create, refresh, extract and render a single offline readiness report. Stdlib only."""
import argparse
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
    items = copy.deepcopy(TEMPLATE['items'])
    for item in items:
        item.update(applicability='yes' if item['condition'] == 'Zawsze' else 'unknown',
                    applicability_reason='', status='unverified', finding='Nie sprawdzono jeszcze tego wymagania.',
                    owner='agent', evidence=[], risk_acceptance=None)
    return {'schema_version': 1, 'template_version': TEMPLATE['version'], 'revision': 0,
            'audit': {'id': str(uuid.uuid4()), 'started_at': now(), 'phase': 'in_progress'},
            'project': repo_info(repo, output),
            'context': {'hosting': 'Nie ustalono', 'audience': 'Nie ustalono', 'data': 'Nie ustalono',
                        'outage_impact': 'Nie ustalono', 'scope_confirmed': False},
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
    require(isinstance(model, dict) and model.get('schema_version') == 1, 'Unsupported schema version')
    require(model.get('template_version') == TEMPLATE['version'], 'Unsupported template version; migrate explicitly')
    require(type(model.get('revision')) is int and model['revision'] >= 0, 'Invalid revision')
    audit = model['audit']
    require(nonempty(audit['id']) and audit['phase'] in {'in_progress', 'complete'}, 'Invalid audit')
    timestamp(audit['started_at'])
    context = model['context']
    require(type(context['scope_confirmed']) is bool, 'scope_confirmed must be boolean')
    for field in ('hosting', 'audience', 'data', 'outage_impact'):
        require(nonempty(context[field]), 'Missing context: ' + field)
        if context['scope_confirmed']:
            require(context[field] != 'Nie ustalono', 'Unresolved context: ' + field)
    require(nonempty(model['project']['name']), 'Missing project name')
    require(model['project']['dirty'] is None or type(model['project']['dirty']) is bool, 'Invalid dirty flag')
    require(model['project']['commit'] is None or nonempty(model['project']['commit']), 'Invalid commit')
    require(isinstance(model['history'], list), 'Invalid history')
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
        for field in ('title', 'why', 'condition', 'verification', 'finding', 'rationale'):
            require(nonempty(item[field]), 'Missing ' + field + ' on ' + item['id'])
        require(isinstance(item['steps'], list) and item['steps'] and all(nonempty(s) for s in item['steps']), 'Missing steps')
        if item['id'] in baseline:
            base = baseline[item['id']]
            require(item['origin'] == 'baseline' and item['category'] == base['category'], 'Baseline identity changed')
            require(not base['required'] or item['required'], 'Cannot weaken a baseline requirement')
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
            if ev['kind'] == 'human':
                require(nonempty(ev.get('person')), 'Human confirmation needs a person')
        if item['status'] == 'pass':
            require(item['applicability'] == 'yes', 'Only applicable criteria can pass')
            require(item['evidence'] and all(ev['audit_id'] == audit['id'] for ev in item['evidence']),
                    'Passing requires current evidence: ' + item['id'])
        risk = item['risk_acceptance']
        if risk is not None:
            require(nonempty(risk['person']) and nonempty(risk['reason']), 'Risk acceptance needs who and why')
            timestamp(risk['recorded_at'])
    require(set(baseline).issubset(ids), 'Baseline criteria cannot be removed')
    require(model['next_item_id'] is None or model['next_item_id'] in ids, 'Unknown next item')


def is_pass(item, audit_id):
    return item['applicability'] == 'yes' and item['status'] == 'pass' and bool(item['evidence']) and all(
        e['audit_id'] == audit_id for e in item['evidence'])


def metrics(model, items=None):
    items = model['items'] if items is None else items
    required = [i for i in items if i['required'] and i['applicability'] != 'no']
    passed = sum(is_pass(i, model['audit']['id']) for i in required)
    total = len(required)
    return {'passed': passed, 'total': total, 'score': passed * 100 // total if total else None,
            'blockers': total - passed}


def verdict(model):
    result = metrics(model)
    if model['audit']['phase'] != 'complete' or not model['context']['scope_confirmed'] or any(
            i['applicability'] == 'unknown' for i in model['items']):
        return 'Ocena nieukończona'
    if result['blockers']:
        return 'Wydanie zablokowane'
    if not result['total']:
        return 'Brak podstaw do oceny'
    return 'Spełnia wymagania checklisty'


def e(value):
    return html.escape(str(value), quote=True)


def label(item):
    if item['applicability'] == 'no':
        return 'Nie dotyczy'
    if item['applicability'] == 'unknown':
        return 'Ustal, czy dotyczy'
    return STATUSES[item['status']]


def next_item(model):
    pending = [i for i in model['items'] if i['applicability'] != 'no' and not is_pass(i, model['audit']['id'])]
    chosen = next((i for i in pending if i['id'] == model['next_item_id']), None)
    return chosen or next(iter(sorted(pending, key=lambda i: (not i['required'], i['priority'] != 'high'))), None)


def item_html(item, model):
    blocking = item['required'] and item['applicability'] != 'no' and not is_pass(item, model['audit']['id'])
    kind = 'blocker' if blocking else ('recommendation' if not item['required'] else ('excluded' if item['applicability'] == 'no' else 'passed'))
    evidence = ''.join('<li><strong>' + e('Potwierdzenie: ' + ev['person'] if ev['kind'] == 'human' else 'Sprawdzenie agenta') +
                       '</strong><p>' + e(ev['result']) + '</p><code>' + e(ev['source']) + '</code><p class="muted">' +
                       e(ev['checked_at']) + (' - poprzednia ocena' if ev['audit_id'] != model['audit']['id'] else '') + '</p></li>' for ev in item['evidence'])
    risk = item['risk_acceptance']
    acceptance = ('<aside class="risk"><strong>Zaakceptowano ryzyko - wymaganie nadal oceniane osobno</strong><p>' +
                  e(risk['person']) + ': ' + e(risk['reason']) + '</p><small>' + e(risk['recorded_at']) + '</small></aside>') if risk else ''
    steps = ''.join('<li>' + e(s) + '</li>' for s in item['steps'])
    exclusion = ('<p><strong>Dlaczego nie dotyczy:</strong> ' + e(item['applicability_reason']) + '</p>') if item['applicability'] == 'no' else ''
    return f'''<details class="check" id="{e(item['id'])}" data-kind="{kind}" data-category="{e(item['category'])}">
<summary class="check-summary"><span class="badge {kind}">{e(label(item))}</span><span class="check-title">{e(item['title'])}</span></summary>
<div class="check-body">
<p class="muted">{'Wymagane do wydania' if item['required'] else 'Zalecane usprawnienie'} · Następny krok: {e(OWNERS[item['owner']])}</p>
<p>{e(item['finding'])}</p>{exclusion}{acceptance}
<p><strong>Dlaczego to ważne:</strong> {e(item['why'])}</p><h4>Co zrobić krok po kroku</h4><ol>{steps}</ol>
<p><strong>Jak potwierdzimy:</strong> {e(item['verification'])}</p><p class="muted">Kiedy dotyczy: {e(item['condition'])}</p>
<p class="muted">Uzasadnienie wymagania: {e(item['rationale'])}</p>
<details><summary>Dowody i szczegóły techniczne ({len(item['evidence'])})</summary><ul class="evidence">{evidence or '<li>Brak potwierdzenia. Ten punkt wymaga sprawdzenia.</li>'}</ul><p class="muted">ID: {e(item['id'])}</p></details></div></details>'''


def document(model):
    validate(model)
    result = metrics(model)
    score = str(result['score']) + '%' if result['score'] is not None else 'Brak oceny'
    selected = next_item(model)
    if selected:
        next_html = f'<p class="eyebrow">Następny krok · {e(OWNERS[selected["owner"]])}</p><h2>{e(selected["title"])}</h2><p>{e(selected["why"])}</p><p>{e(selected["steps"][0])}</p><a class="button jump" href="#{e(selected["id"])}">Zobacz instrukcję</a>'
    elif verdict(model) != 'Spełnia wymagania checklisty':
        next_html = '<p class="eyebrow">Następny krok · Agent i użytkownik</p><h2>Dokończ ustalenie zakresu oceny</h2><p>Potwierdź środowisko, odbiorców, dane i skutki awarii. Dopiero zakończona ocena może być podstawą decyzji o wydaniu.</p>'
    else:
        next_html = '<p class="eyebrow">Następny krok · Użytkownik</p><h2>Przejrzyj ocenę i zdecyduj o wydaniu</h2><p>Agent nie wdraża aplikacji. Ta checklista jest zapisem oceny wskazanej wersji i środowiska.</p>'
    categories, sections = [], []
    for cat in TEMPLATE['categories']:
        items = [i for i in model['items'] if i['category'] == cat['id']]
        stats = metrics(model, items)
        percent = str(stats['score']) + '%' if stats['score'] is not None else 'Nie dotyczy'
        categories.append(f'<a class="category jump" href="#cat-{cat["id"]}"><strong>{e(cat["title"])}</strong><span>{percent}</span><small>{stats["passed"]}/{stats["total"]} wymagań · Blokery: {stats["blockers"]}</small></a>')
        sections.append(f'<section class="category-section" id="cat-{cat["id"]}"><h2>{e(cat["title"])}</h2><p class="muted">{e(cat["description"])}</p><div class="check-list">' + ''.join(item_html(i, model) for i in items) + '</div></section>')
    history = []
    for old in reversed(model['history']):
        stats = metrics(old)
        oldscore = str(stats['score']) + '%' if stats['score'] is not None else 'Brak oceny'
        statuses = ''.join('<li>' + e(i['title']) + ' - ' + e(label(i)) + '</li>' for i in old['items'])
        history.append(f'<details><summary>Wersja raportu {old["revision"]} · {e(old["saved_at"])} · {oldscore} · Blokery: {stats["blockers"]}</summary><p>{e(verdict(old))}</p><ul>{statuses}</ul></details>')
    context = ''.join('<div><dt>' + label_ + '</dt><dd>' + e(model['context'][key]) + '</dd></div>' for key, label_ in
                      [('hosting', 'Gdzie uruchamiamy'), ('audience', 'Dla kogo'), ('data', 'Rodzaj danych'), ('outage_impact', 'Skutki awarii')])
    project = model['project']
    dirty = 'lokalne zmiany' if project['dirty'] else ('czysty stan Git' if project['dirty'] is False else 'stan Git nieznany')
    payload = json.dumps(model, ensure_ascii=False, separators=(',', ':'), allow_nan=False).replace('&', '\\u0026').replace('<', '\\u003c').replace('>', '\\u003e')
    replacements = {'TITLE': e(project['name']), 'SCORE': score, 'PASSED': str(result['passed']), 'TOTAL': str(result['total']),
                    'BLOCKERS': str(result['blockers']), 'VERDICT': e(verdict(model)), 'NEXT': next_html, 'CATEGORIES': ''.join(categories),
                    'SECTIONS': ''.join(sections), 'CONTEXT': context, 'HISTORY': ''.join(history) or '<p>To pierwsza zapisana ocena.</p>',
                    'VERSION': e((project['commit'] or 'Brak commita') + ' · ' + dirty), 'SAVED': e(model.get('saved_at', model['audit']['started_at'])),
                    'PHASE': 'Audyt zakończony' if model['audit']['phase'] == 'complete' else 'Audyt trwa', 'DATA': payload}
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
        model['history'] = previous['history'] + [past]
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
    print(json.dumps({'output': str(output), 'revision': model['revision'], 'verdict': verdict(model), **metrics(model)}, ensure_ascii=False))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError, subprocess.TimeoutExpired) as error:
        raise SystemExit('Checklist error: ' + str(error))
