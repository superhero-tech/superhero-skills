"""Behavioral tests for scores, evidence, history and safe rendering."""
import copy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

import checklist as c


class ChecklistTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.repo = Path(self.directory.name)
        self.output = self.repo / 'docs/production-readiness.html'
        self.model = c.new_model(self.repo, self.output)

    def pass_item(self, item):
        item.update(applicability='yes', status='pass', evidence=[{
            'kind': 'agent', 'source': 'test fixture:1', 'result': 'Observed successful check',
            'audit_id': self.model['audit']['id'], 'checked_at': c.now()}])

    def all_passed(self):
        self.model['audit']['phase'] = 'complete'
        self.model['context'].update(hosting='Test host', audience='Internal users', data='No private data',
                                     outage_impact='Temporary unavailability', scope_confirmed=True)
        for item in self.model['items']:
            self.pass_item(item)

    def test_initial_score_is_zero_and_incomplete(self):
        self.assertEqual(c.metrics(self.model)['score'], 0)
        self.assertEqual(c.metrics(self.model)['total'], 26)
        self.assertEqual(c.verdict(self.model), 'Ocena nieukończona')

    def test_all_required_pass_recommendations_do_not_count(self):
        self.all_passed()
        for item in self.model['items']:
            if not item['required']:
                item.update(status='unverified', evidence=[])
        c.validate(self.model)
        self.assertEqual(c.metrics(self.model)['score'], 100)
        self.assertEqual(c.verdict(self.model), 'Spełnia wymagania checklisty')

    def test_high_score_does_not_override_blocker_or_risk(self):
        self.all_passed()
        item = self.model['items'][0]
        item.update(status='fail', evidence=[], risk_acceptance={
            'person': 'Owner', 'reason': 'Accepting the impact', 'recorded_at': c.now()})
        self.assertEqual(c.metrics(self.model)['score'], 96)
        self.assertEqual(c.metrics(self.model)['blockers'], 1)
        self.assertEqual(c.verdict(self.model), 'Wydanie zablokowane')

    def test_exclusion_changes_denominator_with_reason(self):
        item = self.model['items'][0]
        item.update(applicability='no', applicability_reason='Public read-only site')
        c.validate(self.model)
        self.assertEqual(c.metrics(self.model)['total'], 25)
        item['applicability_reason'] = ''
        with self.assertRaises(ValueError):
            c.validate(self.model)

    def test_unknown_applicability_not_excluded(self):
        self.all_passed()
        self.model['items'][0].update(applicability='unknown', status='unverified', evidence=[])
        self.assertEqual(c.metrics(self.model)['total'], 26)
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
        self.assertEqual(len(saved['history']), 1)
        self.assertEqual(saved['history'][0]['items'][0]['finding'], self.model['items'][0]['finding'])
        self.assertNotIn('history', saved['history'][0])
        with self.assertRaises(ValueError):
            c.save(stale, self.output)
        self.assertEqual(len(list(self.output.parent.iterdir())), 1)

    def test_supplied_history_cannot_replace_stored_history(self):
        c.save(self.model, self.output)
        candidate = c.extract(self.output)
        candidate['history'] = [{'malicious': 'fabricated history'}]
        c.save(candidate, self.output)
        self.assertEqual(len(c.extract(self.output)['history']), 1)
        self.assertIn('items', c.extract(self.output)['history'][0])

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
        self.assertNotIn('Przejrzyj ocenę i zdecyduj', rendered)

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


if __name__ == '__main__':
    unittest.main()
