#!/usr/bin/env python3
"""Numerical and renderer contract checks using Python 3 and Node.js."""
import copy
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("render_card", ROOT / "scripts/render_card.py")
renderer = importlib.util.module_from_spec(spec)
sys.dont_write_bytecode = True
spec.loader.exec_module(renderer)
EXAMPLE = json.loads((ROOT / "assets/example.json").read_text())


def js(expression):
    code = "const s=require(process.argv[1]); const d=JSON.parse(process.argv[2]); console.log(JSON.stringify(" + expression + "));"
    return json.loads(subprocess.check_output(["node", "-e", code, str(ROOT / "assets/statistics.js"), json.dumps(EXAMPLE)], text=True))


def exact_rejection_probability(n, a, b):
    # Sum binomial probabilities over the rejection region independently
    # of the normal-approximation power formula.
    def binomial(p):
        return [math.exp(math.lgamma(n+1)-math.lgamma(x+1)-math.lgamma(n-x+1)+x*math.log(p)+(n-x)*math.log1p(-p)) for x in range(n+1)]
    pa, pb = binomial(a), binomial(b)
    probability = 0.0
    for x, px in enumerate(pa):
        for y, py in enumerate(pb):
            pooled = (x+y)/(2*n)
            variance = 2*pooled*(1-pooled)/n
            if variance > 0 and abs((y-x)/n)/math.sqrt(variance) > 1.959963984540054:
                probability += px*py
    return probability


class CalculatorChecks(unittest.TestCase):
    def test_power_against_binomial_enumeration(self):
        for n, a, b in [(100, .2, .4), (200, .2, .25), (500, .2, .21)]:
            with self.subTest(n=n, a=a, b=b):
                approximate = js(f"s.power({a},{b},{n})")
                self.assertAlmostEqual(approximate, exact_rejection_probability(n,a,b), delta=.015)

    def test_required_is_smallest_sufficient_sample(self):
        result = js("[s.required(.2,.21),s.power(.2,.21,25582),s.power(.2,.21,25583)]")
        self.assertEqual(result[0], 25583)
        self.assertLess(result[1], .8)
        self.assertGreaterEqual(result[2], .8)

    def test_relative_points_and_followup(self):
        relative, points = js("[s.plan(d),s.plan({...d,effect_type:'pp'})]")
        self.assertAlmostEqual(relative["target"], .21)
        self.assertAlmostEqual(points["target"], .25)
        self.assertEqual(relative["n"], 1000)
        self.assertEqual(relative["readout"], 21)
        self.assertEqual(relative["days"], 364)
        self.assertEqual(relative["required_readout"], 371)
        self.assertGreater(relative["need"], points["need"])

    def test_mde_and_downward_effect(self):
        result = js("(()=>{const delta=s.mde(.2,1000,'up');return [delta,s.power(.2,.2+delta,1000),s.power(.2,.2+delta*.999,1000),s.plan({...d,direction:'down'})];})()")
        self.assertAlmostEqual(result[1], .8, places=6)
        self.assertLess(result[2], .8)
        self.assertAlmostEqual(result[3]["target"], .19)

    def test_minimum_two_weeks_even_with_large_traffic(self):
        result = js("s.plan({...d,baseline:.05,effect:3,effect_type:'pp',weekly_users:50000,primary_window_days:1,guardrail_window_days:0})")
        self.assertEqual(result["days"], 14)
        self.assertEqual(result["required_readout"], 15)

    def test_full_week_rounding_and_followup(self):
        for sample_days, expected in [(14,14),(15,21),(21,21),(22,28)]:
            with self.subTest(sample_days=sample_days):
                result = js(f"(()=>{{const traffic=s.required(.2,.21)*14/({sample_days}-.25);const r=s.plan({{...d,weekly_users:traffic}});return [r,s.plan({{...d,weekly_users:traffic,recruitment_days:r.days}})];}})()")
                self.assertEqual(result[0]["days"], expected)
                self.assertEqual(result[0]["required_readout"], expected+7)
                self.assertGreaterEqual(result[1]["power"], .8)

    def test_rejects_short_or_partial_week_duration(self):
        for duration in [1,7,13,15,20,22]:
            with self.subTest(duration=duration):
                self.assertEqual(js(f"s.plan({{...d,recruitment_days:{duration}}})")["error"], "duration")
                with self.assertRaises(ValueError):
                    renderer.render({**EXAMPLE,"recruitment_days":duration})

    def test_observed_against_known_normal_tail(self):
        result = js("s.observed(1000,200,1000,250)")
        pooled = .225
        z = .05 / math.sqrt(pooled*(1-pooled)*.002)
        self.assertAlmostEqual(result["p"], math.erfc(z/math.sqrt(2)), places=7)
        self.assertAlmostEqual(result["diff"], .05)
        self.assertLess(result["low"], .05)
        self.assertGreater(result["low"], 0)
        self.assertAlmostEqual(result["srm"], 1, places=6)

    def test_missing_sparse_invalid_and_allocation(self):
        result = js("[s.plan({...d,baseline:null}),s.plan({...d,effect:500}),s.plan({...d,weekly_users:1}),s.observed(100,0,100,0),s.observed(100,101,100,30),s.observed(100,.5,100,30),s.observed(1000,200,500,100),s.required(.2,.2)]")
        self.assertEqual(result[0]["error"], "inputs")
        self.assertEqual(result[1]["error"], "target")
        self.assertTrue(result[2]["sparse"])
        self.assertEqual(result[3]["error"], "sparse")
        self.assertEqual(result[4]["error"], "counts")
        self.assertEqual(result[5]["error"], "counts")
        self.assertLess(result[6]["srm"], .001)
        self.assertIsNone(result[7])

    def test_render_preserves_text_without_script_injection(self):
        data = copy.deepcopy(EXAMPLE)
        data["hypothesis"] = '</script><script>alert(1)</script> __CARD_JS__'
        rendered = renderer.render(data)
        self.assertNotIn(data["hypothesis"], rendered)
        self.assertIn('\\u003c/script\\u003e', rendered)
        # JSON preserves user content without expanding its template-like tokens.
        json_text = rendered.split('<script type="application/json" id="card-data">')[1].split('</script>')[0]
        self.assertEqual(json.loads(json_text)["hypothesis"], data["hypothesis"])

    def test_renderer_accepts_unknowns_and_rejects_bad_contracts(self):
        data = copy.deepcopy(EXAMPLE)
        data["baseline"] = None
        self.assertIn('"baseline": null', renderer.render(data))
        for key, bad in [("weekly_users", -1), ("primary_window_days", -.5), ("effect", float('nan')), ("guardrails", [{}])]:
            with self.subTest(key=key):
                changed = {**data, key:bad}
                with self.assertRaises(ValueError):
                    renderer.render(changed)


if __name__ == "__main__":
    unittest.main(verbosity=2)
