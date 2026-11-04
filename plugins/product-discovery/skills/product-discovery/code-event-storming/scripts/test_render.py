"""Behavioral checks for renderer validation and safe, portable output. Stdlib only."""
import copy
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

from render import PALETTE, prepare, render


class RendererTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.repo = Path(self.directory.name).resolve()
        (self.repo / "rule.ts").write_text('if (available > 0) confirm();\n// </script><img src=x onerror=alert(1)>\n')
        def node(id, kind, col, row):
            return dict(id=id, type=kind, title=id, detail='Reguła < > & "', col=col, row=row,
                        sources=[dict(path="rule.ts", line=1, end=2)])
        self.model = dict(title='Zażółć < & __TITLE__ __MODEL__', summary="Migawka", lanes=[dict(
            id="flow", title="Proces", description="Zdarzenie i informacja",
            nodes=[node("command", "COMMAND", 0, 0), node("event", "DOMAIN EVENT", 1, 0),
                   node("availability", "READ MODEL", 2, 1)],
            edges=[{"from":"command", "to":"event", "kind":"flow", "label":"jest miejsce"},
                   {"from":"event", "to":"availability", "kind":"information", "label":"aktualizuje dostępność"}])])

    def test_model_keeps_sources_and_exact_palette_without_mutating_input(self):
        original = copy.deepcopy(self.model)
        data = prepare(self.model, self.repo)
        self.assertEqual(self.model, original)
        self.assertEqual(len(data["lanes"][0]["edges"]), 2)
        self.assertEqual(data["palette"], PALETTE)
        self.assertIn("1  if (available > 0)", data["lanes"][0]["nodes"][0]["sources"][0]["excerpt"])

    def test_embedded_text_cannot_close_script_and_roundtrips_unchanged(self):
        output = render(self.model, self.repo)
        payload = re.search(r'<script id="model" type="application/json">(.*?)</script>', output, re.S)[1]
        data = json.loads(payload)
        self.assertEqual(data["title"], self.model["title"])
        self.assertNotIn("<", payload)
        self.assertIn('</script><img src=x onerror=alert(1)>', data["lanes"][0]["nodes"][0]["sources"][0]["excerpt"])
        self.assertIn('Zażółć &lt; &amp; __TITLE__ __MODEL__', output)

    def test_rejects_invalid_graphs_and_layout(self):
        mutations = [
            lambda lane: lane["nodes"][1].update(id="command"),
            lambda lane: lane["nodes"][0].update(type="DATABASE"),
            lambda lane: lane["edges"][0].update(to="missing"),
            lambda lane: lane["nodes"][1].update(col=0),
            lambda lane: lane["nodes"][0].update(row=-1),
            lambda lane: lane["nodes"][0].update(col=True),
            lambda lane: lane["edges"][0].update(kind="unknown"),
            lambda lane: lane["edges"][0].pop("kind"),
            lambda lane: lane["edges"][1].update(kind="flow"),
        ]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                data = copy.deepcopy(self.model); mutation(data["lanes"][0])
                with self.assertRaises(ValueError): prepare(data, self.repo)

    def test_hotspot_is_only_an_annotation_and_information_can_return(self):
        lane=self.model["lanes"][0]
        lane["nodes"][2]["col"]=0  # A different row receives feedback from the event.
        hotspot=copy.deepcopy(lane["nodes"][0])
        hotspot.update(id="question",type="HOT SPOT",row=2)
        lane["nodes"].append(hotspot)
        lane["edges"].append({"from":"command","to":"question","kind":"annotation","label":"pytanie o termin"})
        data=prepare(self.model,self.repo)
        self.assertEqual(data["lanes"][0]["edges"][-1]["kind"],"annotation")
        for kind in ("flow","information"):
            changed=copy.deepcopy(self.model);changed["lanes"][0]["edges"][-1]["kind"]=kind
            with self.subTest(kind=kind),self.assertRaises(ValueError):prepare(changed,self.repo)
        lane["edges"][-1].update(to="event")
        with self.assertRaises(ValueError):prepare(self.model,self.repo)

    def test_command_notes_have_their_own_source_evidence(self):
        command=self.model["lanes"][0]["nodes"][0]
        command["rules"]=[{"text":"Jeden aktywny zapis", "sources":[{"path":"rule.ts","line":1}]}]
        command["outcomes"]=[{"text":"Brak miejsc: odmów < &", "sources":[{"path":"rule.ts","line":2}]}]
        output=render(self.model,self.repo)
        payload=re.search(r'<script id="model" type="application/json">(.*?)</script>',output,re.S)[1]
        rendered=json.loads(payload)["lanes"][0]["nodes"][0]
        self.assertIn("1  if",rendered["rules"][0]["sources"][0]["excerpt"])
        self.assertEqual(rendered["outcomes"][0]["text"],"Brak miejsc: odmów < &")
        command["rules"][0]["sources"]=[]
        with self.assertRaises(ValueError):prepare(self.model,self.repo)

    def test_command_notes_do_not_turn_read_models_into_results(self):
        read_model=self.model["lanes"][0]["nodes"][2]
        read_model["outcomes"]=[{"text":"Brak zmian", "sources":[{"path":"rule.ts","line":1}]}]
        with self.assertRaises(ValueError):prepare(self.model,self.repo)

    def test_rejects_missing_out_of_bounds_and_escaping_sources(self):
        for source in [{"path":"rule.ts","line":9}, {"path":"../outside.ts","line":1},
                       {"path":str(self.repo/"rule.ts"),"line":1}]:
            data = copy.deepcopy(self.model); data["lanes"][0]["nodes"][0]["sources"]=[source]
            with self.subTest(source=source), self.assertRaises(ValueError): prepare(data, self.repo)
        with tempfile.TemporaryDirectory() as other:
            target = Path(other)/"outside.ts"; target.write_text("outside")
            (self.repo/"link.ts").symlink_to(target)
            data = copy.deepcopy(self.model)
            data["lanes"][0]["nodes"][0]["sources"]=[{"path":"link.ts","line":1}]
            with self.assertRaises(ValueError): prepare(data, self.repo)

    def test_cli_writes_custom_html_and_leaves_existing_output_on_validation_error(self):
        model = self.repo/"model.json"; model.write_text(json.dumps(self.model))
        script = str(Path(__file__).with_name("render.py"))
        command=[sys.executable,script,str(model),"--repo",str(self.repo),"--output","custom/board.html"]
        result=subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        output=self.repo/"custom/board.html"; before=output.read_bytes()
        self.model["lanes"][0]["edges"][0]["to"]="missing"; model.write_text(json.dumps(self.model))
        result=subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode,2)
        self.assertEqual(output.read_bytes(),before)
        result=subprocess.run(command[:-1]+["../escape.html"], capture_output=True, text=True)
        self.assertEqual(result.returncode,2)


if __name__ == "__main__":
    unittest.main()
