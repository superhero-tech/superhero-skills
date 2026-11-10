"""Behavioral tests for scores, evidence, history and safe rendering."""
import copy
import json
from html.parser import HTMLParser
from pathlib import Path
import subprocess
import tempfile
import unittest

import checklist as c


class ReportView(HTMLParser):
    """Inspect semantic grouping independently of renderer helper functions."""
    def __init__(self, source):
        super().__init__()
        self.stack = []
        self.checks = {}
        self.groups = {}
        self.summaries = {}
        self.feed(source)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        classes = attrs.get('class', '').split()
        if tag == 'details' and 'stage-group' in classes:
            self.groups[attrs['data-stage']] = 'open' in attrs
        if tag == 'details' and 'check' in classes:
            self.checks[attrs['id']] = {
                'current': any('current-checklist' in a.get('class', '').split() for _, a in self.stack),
                'stage': attrs['data-stage']}
            self.summaries[attrs['id']] = []
        if tag not in {'meta', 'input', 'br', 'hr', 'img', 'link'}:
            self.stack.append((tag, attrs))

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break

    def handle_data(self, text):
        details = next((attrs for tag, attrs in reversed(self.stack) if tag == 'details'), None)
        if details and 'check' in details.get('class', '').split() and any(tag == 'summary' for tag, _ in self.stack):
            self.summaries[details['id']].append(text)


class ChecklistTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.repo = Path(self.directory.name)
        self.output = self.repo / 'docs/production-readiness.html'
        self.model = c.new_model(self.repo, self.output)
        self.model['context']['source_version'] = 'fixture-source'
        self.model['environments'][0].update(version='fixture-source', source_version='fixture-source', config_revision='local-config-1')
        self.model['environments'].append(dict(id='prod', kind='production', name='Production',
            address='https://example.test', version='deployment-1', source_version='fixture-source',
            config_revision='prod-config-1', available=True))
        self.required_total = sum(i['required'] and i['stage'] == 'preparation' for i in self.model['items'])

    def pass_item(self, item):
        if item['environment_id'] is None:
            item['environment_id'] = 'prod'
        item.update(applicability='yes', status='pass', evidence=[{
            'kind': 'agent', 'source': 'test fixture:1', 'result': 'Observed successful check',
            'audit_id': self.model['audit']['id'], 'checked_at': c.now(),
            'stage': item['stage'], 'source_version': self.model['context']['source_version'],
            'environment': copy.deepcopy(c.environment(self.model, item))}])

    def all_passed(self):
        self.model['audit']['phase'] = 'complete'
        self.model['context']['release_state'] = 'live'
        self.model['context'].update(hosting='Test host', audience='Internal users', data='No private data',
                                     outage_impact='Temporary unavailability', scope_confirmed=True)
        for item in self.model['items']:
            self.pass_item(item)

    def test_initial_score_is_zero_and_incomplete(self):
        self.assertEqual(c.metrics(self.model)['score'], 0)
        self.assertEqual(c.metrics(self.model)['total'], self.required_total)
        self.assertEqual(c.verdict(self.model), 'Ocena nieukończona')

    def test_all_required_pass_recommendations_do_not_count(self):
        self.all_passed()
        for item in self.model['items']:
            if not item['required']:
                item.update(status='unverified', evidence=[])
        c.validate(self.model)
        self.assertEqual(c.metrics(self.model)['score'], 100)
        self.assertEqual(c.verdict(self.model), 'Gotowe do wdrożenia')

    def test_high_score_does_not_override_blocker_or_risk(self):
        self.all_passed()
        item = self.model['items'][0]
        item.update(status='fail', evidence=[], risk_acceptance={
            'person': 'Owner', 'reason': 'Accepting the impact', 'recorded_at': c.now()})
        self.assertEqual(c.metrics(self.model)['score'], (self.required_total - 1) * 100 // self.required_total)
        self.assertEqual(c.metrics(self.model)['blockers'], 1)
        self.assertEqual(c.verdict(self.model), 'Przygotowanie zablokowane')

    def test_exclusion_changes_denominator_with_reason(self):
        item = self.model['items'][0]
        item.update(applicability='no', applicability_reason='Public read-only site')
        c.validate(self.model)
        self.assertEqual(c.metrics(self.model)['total'], self.required_total - 1)
        item['applicability_reason'] = ''
        with self.assertRaises(ValueError):
            c.validate(self.model)

    def test_unknown_applicability_not_excluded(self):
        self.all_passed()
        self.model['items'][0].update(applicability='unknown', status='unverified', evidence=[])
        self.assertEqual(c.metrics(self.model)['total'], self.required_total)
        self.assertEqual(c.metrics(self.model)['blockers'], 1)
        self.assertEqual(c.verdict(self.model), 'Ocena nieukończona')

    def test_no_applicable_items_is_not_100_percent(self):
        self.assertIsNone(c.metrics(self.model, [])['score'])

    def test_pass_requires_current_evidence(self):
        item = self.model['items'][0]
        self.pass_item(item)
        item['evidence'][0]['audit_id'] = 'old-run'
        with self.assertRaises(ValueError):
            c.validate(self.model)
        self.assertEqual(c.metrics(self.model)['passed'], 0)
        item['evidence'] = []
        with self.assertRaises(ValueError):
            c.validate(self.model)

    def test_human_evidence_needs_named_person(self):
        item = self.model['items'][0]
        self.pass_item(item)
        item['evidence'][0]['kind'] = 'human'
        with self.assertRaises(ValueError):
            c.validate(self.model)
        item['evidence'][0]['person'] = 'Product owner'
        c.validate(self.model)

    def test_unconditional_baseline_cannot_be_excluded(self):
        item = next(i for i in self.model['items'] if i['condition'] == 'Zawsze')
        item.update(applicability='no', applicability_reason='Accept risk')
        with self.assertRaises(ValueError):
            c.validate(self.model)

    def test_baseline_cannot_be_removed_downgraded_or_duplicated(self):
        for mutate in (lambda m: m['items'].pop(),
                       lambda m: m['items'][0].update(required=False),
                       lambda m: m['items'].append(copy.deepcopy(m['items'][0]))):
            model = copy.deepcopy(self.model)
            mutate(model)
            with self.assertRaises(ValueError):
                c.validate(model)

    def test_refresh_stales_passes_and_rechecks_exclusions(self):
        self.all_passed()
        self.model['items'][0].update(applicability='no', status='unverified', evidence=[], applicability_reason='Not used')
        refreshed = c.refresh(self.model, self.repo, self.output)
        self.assertEqual(c.metrics(refreshed)['score'], 0)
        self.assertEqual(refreshed['items'][0]['applicability'], 'unknown')
        self.assertEqual(refreshed['items'][1]['status'], 'stale')
        self.assertFalse(refreshed['context']['scope_confirmed'])
        self.assertNotEqual(refreshed['audit']['id'], self.model['audit']['id'])
        c.validate(refreshed)

    def test_single_html_roundtrip_history_and_concurrency(self):
        c.save(self.model, self.output)
        current = c.extract(self.output)
        stale = copy.deepcopy(current)
        current['items'][0]['finding'] = 'Now inspected'
        c.save(current, self.output)
        saved = c.extract(self.output)
        self.assertEqual(saved['revision'], 2)
        self.assertEqual(saved['history'], [])
        self.assertEqual(saved['items'][0]['finding'], 'Now inspected')
        with self.assertRaises(ValueError):
            c.save(stale, self.output)
        self.assertEqual(len(list(self.output.parent.iterdir())), 1)

    def test_supplied_history_cannot_replace_stored_history(self):
        self.model['audit']['phase'] = 'complete'
        c.save(self.model, self.output)
        candidate = c.refresh(c.extract(self.output), self.repo, self.output)
        candidate['history'] = [{'malicious': 'fabricated history'}]
        c.save(candidate, self.output)
        self.assertEqual(len(c.extract(self.output)['history']), 1)
        self.assertIn('items', c.extract(self.output)['history'][0])

    def test_working_saves_do_not_become_audit_results(self):
        c.save(self.model, self.output)
        working = c.extract(self.output)
        working['items'][0]['finding'] = 'First working observation'
        c.save(working, self.output)
        complete = c.extract(self.output)
        complete['audit']['phase'] = 'complete'
        c.save(complete, self.output)
        first = c.extract(self.output)
        self.assertEqual(first['history'], [])
        next_run = c.refresh(first, self.repo, self.output)
        c.save(next_run, self.output)
        working = c.extract(self.output)
        working['items'][0]['finding'] = 'Unfinished reassessment'
        c.save(working, self.output)
        saved = c.extract(self.output)
        self.assertEqual(len(saved['history']), 1)
        self.assertEqual(saved['history'][0]['audit'], first['audit'])
        self.assertEqual(saved['history'][0]['items'], first['items'])
        self.assertNotIn('history', saved['history'][0])

    def test_repeated_completion_keeps_latest_result_without_duplicate_current(self):
        self.model['audit']['phase'] = 'complete'
        c.save(self.model, self.output)
        corrected = c.extract(self.output)
        corrected['items'][0]['finding'] = 'Latest completed observation'
        c.save(corrected, self.output)
        latest = c.extract(self.output)
        self.assertEqual(latest['history'], [])
        reopened = copy.deepcopy(latest)
        reopened['audit']['phase'] = 'in_progress'
        c.save(reopened, self.output)
        self.assertEqual(len(c.extract(self.output)['history']), 1)
        completed = c.extract(self.output)
        completed['audit']['phase'] = 'complete'
        c.save(completed, self.output)
        self.assertEqual(c.extract(self.output)['history'], [])
        next_run = c.refresh(c.extract(self.output), self.repo, self.output)
        c.save(next_run, self.output)
        archived = c.extract(self.output)['history']
        self.assertEqual(len(archived), 1)
        self.assertEqual(archived[0]['items'][0]['finding'], 'Latest completed observation')

    def test_completed_stages_of_same_audit_are_retained_independently(self):
        self.model['audit']['phase'] = 'complete'
        c.save(self.model, self.output)
        deployment = c.extract(self.output)
        audit_id = deployment['audit']['id']
        deployment['context'].update(target_stage='deployment', release_state='deployed')
        deployment['audit']['phase'] = 'in_progress'
        c.save(deployment, self.output)
        deployment = c.extract(self.output)
        deployment['audit']['phase'] = 'complete'
        c.save(deployment, self.output)
        saved = c.extract(self.output)
        self.assertEqual(len(saved['history']), 1)
        self.assertEqual(saved['history'][0]['audit']['id'], audit_id)
        self.assertEqual(saved['history'][0]['context']['target_stage'], 'preparation')
        next_run = c.refresh(saved, self.repo, self.output)
        c.save(next_run, self.output)
        archived = c.extract(self.output)['history']
        self.assertEqual([h['context']['target_stage'] for h in archived], ['preparation', 'deployment'])
        self.assertTrue(all(h['audit']['phase'] == 'complete' for h in archived))

    def test_old_mixed_history_is_cleaned_without_changing_current_assessment(self):
        self.model['audit']['phase'] = 'complete'
        c.save(self.model, self.output)
        old = c.extract(self.output)
        snapshot = copy.deepcopy(old)
        snapshot.pop('history')
        snapshot.pop('_base_digest')
        draft = copy.deepcopy(snapshot)
        draft.update(revision=10, saved_at='2026-01-01T00:00:00+00:00')
        draft['audit'].update(id='old-draft', phase='in_progress')
        complete = copy.deepcopy(snapshot)
        complete.update(revision=11, saved_at='2026-01-02T00:00:00+00:00')
        complete['audit']['id'] = 'previous-audit'
        latest = copy.deepcopy(complete)
        latest.update(revision=12, saved_at='2026-01-03T00:00:00+00:00')
        latest['environments'][0]['config_revision'] = 'retained-historical-config'
        old['history'] = [draft, complete, latest, copy.deepcopy(snapshot)]
        # Simulate a report written by the former schema-2 renderer.
        self.output.write_text(c.document(old))
        history_view = self.output.read_text().split('<section class="history">')[1].split('</section>')[0]
        self.assertNotIn(draft['saved_at'], history_view)
        self.assertNotIn(complete['saved_at'], history_view)
        self.assertIn(latest['saved_at'], history_view)
        before = c.extract(self.output)
        c.save(before, self.output)
        after = c.extract(self.output)
        self.assertEqual(after['history'], [latest])
        for field in ('audit', 'project', 'context', 'items', 'environments'):
            self.assertEqual(after[field], before[field])
        self.assertEqual(c.metrics(after), c.metrics(before))

    def test_custom_criteria_cannot_disappear_on_update(self):
        custom = copy.deepcopy(self.model['items'][0])
        custom.update(id='custom-domain-rule', origin='custom', rationale='Domain-specific invariant')
        self.model['items'].append(custom)
        c.save(self.model, self.output)
        candidate = c.extract(self.output)
        candidate['items'].pop()
        with self.assertRaises(ValueError):
            c.save(candidate, self.output)

    def test_embedded_data_cannot_escape_script_or_replace_template(self):
        text = '</script><script>alert("x")</script><img src=x onerror=alert(1)> @@DATA@@ &'
        self.model['items'][0]['finding'] = text
        c.save(self.model, self.output)
        raw = self.output.read_text()
        self.assertNotIn('<script>alert', raw)
        self.assertNotIn('<img src=x', raw)
        self.assertIn('&lt;img', raw)
        self.assertEqual(c.extract(self.output)['items'][0]['finding'], text)
        self.assertEqual(len(c.DATA_RE.findall(raw)), 1)

    def test_incomplete_scope_does_not_suggest_releasing(self):
        self.all_passed()
        self.model['context']['scope_confirmed'] = False
        rendered = c.document(self.model)
        self.assertIn('Dokończ ustalenie zakresu', rendered)
        self.assertNotIn('Uzgodnij wdrożenie', rendered)

    def test_fingerprint_changes_inside_an_already_dirty_tree(self):
        subprocess.run(['git', 'init', '-q', str(self.repo)], check=True)
        source = self.repo / 'app.txt'
        source.write_text('first version')
        before = c.repo_info(self.repo, self.output)
        source.write_text('second version')
        after = c.repo_info(self.repo, self.output)
        self.assertTrue(before['dirty'] and after['dirty'])
        self.assertNotEqual(before['fingerprint'], after['fingerprint'])
        self.output.parent.mkdir()
        self.output.write_text('report is excluded')
        self.assertEqual(after, c.repo_info(self.repo, self.output))

    def test_cli_rejects_output_outside_project(self):
        result = subprocess.run(['python3', str(c.ROOT / 'scripts/checklist.py'), 'init', '--repo', str(self.repo),
                                 '--output', '../escape.html'], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('inside the target project', result.stderr)

    def test_invalid_update_leaves_report_untouched(self):
        c.save(self.model, self.output)
        previous = self.output.read_bytes()
        candidate = c.extract(self.output)
        candidate['items'][0].update(status='pass', applicability='yes', evidence=[])
        with self.assertRaises(ValueError):
            c.save(candidate, self.output)
        self.assertEqual(previous, self.output.read_bytes())

    def test_preparation_can_complete_without_deployment_or_staging(self):
        self.all_passed()
        self.model['context']['release_state'] = 'not_deployed'
        for item in self.model['items']:
            if item['stage'] != 'preparation':
                item.update(status='unverified', evidence=[], applicability='yes' if item['condition'] == 'Zawsze' else 'unknown')
        c.validate(self.model)
        self.assertEqual(c.metrics(self.model)['score'], 100)
        self.assertEqual(c.verdict(self.model), 'Gotowe do wdrożenia')
        self.assertEqual(c.metrics(self.model, stage='deployment')['score'], 0)
        self.assertEqual(c.verdict(self.model, 'deployment'), 'Do sprawdzenia po wdrożeniu')
        self.assertEqual(c.verdict(self.model, 'observation'), 'Do obserwacji po udostępnieniu')
        self.assertFalse(any(e['kind'] == 'staging' for e in self.model['environments']))

    def test_stage_denominators_are_independent(self):
        self.all_passed()
        before = c.metrics(self.model)
        deployment = next(i for i in self.model['items'] if i['stage'] == 'deployment')
        deployment.update(status='fail', evidence=[])
        self.assertEqual(c.metrics(self.model), before)
        self.assertGreater(c.metrics(self.model, stage='deployment')['blockers'], 0)
        self.assertEqual(c.verdict(self.model, 'deployment'), 'Wymaga sprawdzenia lub poprawy')

    def test_local_pass_does_not_pass_production_smoke(self):
        local = next(i for i in self.model['items'] if i['id'] == 'main-journey')
        smoke = next(i for i in self.model['items'] if i['id'] == 'main-journey-production')
        self.pass_item(local)
        self.assertTrue(c.is_pass(local, self.model))
        self.assertFalse(c.is_pass(smoke, self.model))
        self.model['context']['release_state'] = 'deployed'
        smoke.update(status='pass', applicability='yes', evidence=copy.deepcopy(local['evidence']), environment_id='local')
        with self.assertRaises(ValueError):
            c.validate(self.model)

    def test_staging_does_not_stand_in_for_production(self):
        self.all_passed()
        self.model['environments'][1]['kind'] = 'staging'
        with self.assertRaises(ValueError):
            c.validate(self.model)

    def test_environment_source_config_and_deployment_changes_invalidate_passes(self):
        self.all_passed()
        for field, replacement in [('address', 'https://other.test'), ('version', 'deployment-2'),
                                   ('config_revision', 'config-2'), ('source_version', 'other-source'),
                                   ('available', False)]:
            with self.subTest(field=field):
                candidate = copy.deepcopy(self.model)
                candidate['environments'][1][field] = replacement
                self.assertLess(c.metrics(candidate, stage='deployment')['score'], 100)
                with self.assertRaises(ValueError):
                    c.validate(candidate)
        candidate = copy.deepcopy(self.model)
        candidate['context']['source_version'] = 'new-source'
        with self.assertRaises(ValueError):
            c.validate(candidate)

    def test_missing_environment_identity_cannot_pass(self):
        self.all_passed()
        for field in ('address', 'version', 'config_revision', 'source_version'):
            candidate = copy.deepcopy(self.model)
            candidate['environments'][1][field] = ''
            with self.assertRaises(ValueError):
                c.validate(candidate)

    def test_evidence_cannot_omit_or_change_environment(self):
        self.all_passed()
        evidence = self.model['items'][0]['evidence'][0]
        evidence['environment']['address'] = 'repo:/somewhere-else'
        with self.assertRaises(ValueError):
            c.validate(self.model)

    def test_baseline_cannot_move_to_another_stage(self):
        self.model['items'][0]['stage'] = 'observation'
        with self.assertRaises(ValueError):
            c.validate(self.model)

    def test_later_stage_requires_earlier_checks(self):
        self.all_passed()
        self.model['items'][0].update(status='fail', evidence=[])
        self.assertEqual(c.metrics(self.model, stage='deployment')['score'], 100)
        self.assertIn('Najpierw ukończ', c.verdict(self.model, 'deployment'))
        self.assertIn('Najpierw ukończ', c.verdict(self.model, 'observation'))

    def test_observation_cannot_pass_before_real_use(self):
        self.all_passed()
        self.model['context']['release_state'] = 'deployed'
        self.assertEqual(c.verdict(self.model, 'observation'), 'Do obserwacji po udostępnieniu')
        with self.assertRaises(ValueError):
            c.validate(self.model)

    def test_missing_access_to_existing_production_is_unverified_not_waiting(self):
        self.model['context'].update(release_state='deployed', target_stage='deployment')
        item = next(i for i in self.model['items'] if i['id'] == 'transport')
        item['environment_id'] = 'prod'
        self.model['environments'][1]['available'] = False
        self.assertEqual(c.waiting_reason(self.model, item), '')
        self.assertEqual(c.label(item, self.model), 'Do sprawdzenia')
        self.assertIn('data-kind="blocker"', c.item_html(item, self.model))

    def test_future_selection_does_not_displace_actionable_preparation(self):
        self.model['next_item_id'] = 'main-journey-production'
        self.assertEqual(c.next_item(self.model)['stage'], 'preparation')

    def test_waiting_is_not_a_failure_and_is_kept_in_own_denominator(self):
        item = next(i for i in self.model['items'] if i['id'] == 'transport')
        self.assertIn('data-kind="waiting"', c.item_html(item, self.model))
        self.assertEqual(item['status'], 'unverified')
        stats = c.metrics(self.model, stage='deployment')
        self.assertEqual(stats['waiting'], stats['total'])
        self.assertEqual(stats['passed'], 0)

    def test_legacy_report_is_not_read_migrated_or_overwritten(self):
        legacy = copy.deepcopy(self.model)
        legacy['schema_version'] = 1
        legacy['template_version'] = 1
        self.output.parent.mkdir()
        raw = '<script id="readiness-data" type="application/json">' + json.dumps(legacy) + '</script>'
        self.output.write_text(raw)
        for action in ('extract', 'refresh', 'validate', 'init'):
            result = subprocess.run(['python3', str(c.ROOT / 'scripts/checklist.py'), action, '--repo', str(self.repo)],
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(self.output.read_text(), raw)
        with self.assertRaises(ValueError):
            c.save(self.model, self.output)
        self.assertEqual(self.output.read_text(), raw)
        new_output = self.repo / 'docs/new-readiness.html'
        c.save(c.new_model(self.repo, new_output), new_output)
        self.assertEqual(c.extract(new_output)['schema_version'], 2)
        self.assertEqual(self.output.read_text(), raw)

    def test_dev_view_focuses_on_preparation_without_hiding_future_state(self):
        view = ReportView(c.document(self.model))
        self.assertEqual(set(view.checks), {i['id'] for i in self.model['items']})
        current = [record for record in view.checks.values() if record['current']]
        self.assertTrue(current)
        self.assertTrue(all(record['stage'] == 'preparation' for record in current))
        self.assertFalse(view.groups['deployment'])
        self.assertFalse(view.groups['observation'])
        self.assertFalse(view.checks['main-journey-production']['current'])

    def test_production_view_moves_preparation_to_previous_results(self):
        self.all_passed()
        self.model['context']['target_stage'] = 'deployment'
        view = ReportView(c.document(self.model))
        self.assertTrue(view.checks['main-journey-production']['current'])
        self.assertFalse(view.checks['main-journey']['current'])
        self.assertFalse(view.groups['preparation'])
        self.assertFalse(view.groups['observation'])
        self.assertEqual(sum(record['current'] for record in view.checks.values()),
                         sum(i['stage'] == 'deployment' for i in self.model['items']))

    def test_unresolved_prerequisites_are_expanded_and_actionable(self):
        self.all_passed()
        self.model['context']['target_stage'] = 'deployment'
        item = self.model['items'][0]
        item.update(status='stale', evidence=[])
        view = ReportView(c.document(self.model))
        self.assertTrue(view.groups['preparation'])
        self.assertEqual(c.next_item(self.model)['id'], item['id'])
        self.assertEqual(c.metrics(self.model, stage='preparation')['blockers'], 1)

    def test_collapsed_check_contains_status_and_title_without_environment_menu(self):
        item = self.model['items'][0]
        view = ReportView(c.document(self.model))
        summary = ' '.join(' '.join(view.summaries[item['id']]).split())
        self.assertEqual(summary, c.label(item, self.model) + ' ' + item['title'])

    def test_continuing_same_release_keeps_dev_evidence_with_original_identity(self):
        self.all_passed()
        self.model['context']['release_state'] = 'not_deployed'
        for item in self.model['items']:
            if item['stage'] != 'preparation':
                item.update(status='unverified', evidence=[])
        c.save(self.model, self.output)
        continued = c.extract(self.output)
        before = copy.deepcopy(continued['items'][0]['evidence'])
        audit_id = continued['audit']['id']
        continued['context'].update(target_stage='deployment', release_state='deployed')
        continued['audit']['phase'] = 'in_progress'
        c.save(continued, self.output)
        saved = c.extract(self.output)
        self.assertEqual(saved['items'][0]['evidence'], before)
        self.assertEqual(saved['audit']['id'], audit_id)
        self.assertEqual(c.metrics(saved, stage='preparation')['score'], 100)
        self.assertEqual(c.metrics(saved, stage='deployment')['score'], 0)

    def test_source_identity_cannot_override_repository_fingerprint(self):
        self.model['project']['fingerprint'] = 'actual-repository-fingerprint'
        with self.assertRaises(ValueError):
            c.validate(self.model)

    def test_font_is_embedded_without_external_requests(self):
        raw = c.document(self.model)
        self.assertIn('font-src data:', raw)
        self.assertIn('data:font/woff2;base64,', raw)
        self.assertIn('Geist', raw)
        self.assertIn('SIL OPEN FONT LICENSE', raw)
        self.assertNotIn('@@FONT@@', raw)

    def test_history_keeps_environment_identities(self):
        self.all_passed()
        c.save(self.model, self.output)
        current = c.refresh(c.extract(self.output), self.repo, self.output)
        current['environments'][1]['config_revision'] = 'config-2'
        c.save(current, self.output)
        saved = c.extract(self.output)
        self.assertEqual(saved['history'][0]['environments'][1]['config_revision'], 'prod-config-1')
        self.assertEqual(saved['environments'][1]['config_revision'], 'config-2')


if __name__ == '__main__':
    unittest.main()
