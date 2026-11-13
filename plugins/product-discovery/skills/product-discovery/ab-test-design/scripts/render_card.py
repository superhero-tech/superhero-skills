#!/usr/bin/env python3
"""Render a standalone HTML card using only the Python standard library."""
import argparse
import json
import math
import re
from pathlib import Path
import subprocess

ASSETS = Path(__file__).resolve().parents[1] / "assets"
TEXT = "title hypothesis control treatment population metric metric_definition baseline_source recommendation decision_rule".split()
NUMBERS = "baseline effect weekly_users recruitment_days primary_window_days guardrail_window_days max_readout_days".split()


def validate(data):
    if not isinstance(data, dict):
        raise ValueError("Card must be a JSON object")
    for key in TEXT:
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ValueError(f"Non-empty text required: {key}")
    if data.get("language") not in ("pl", "en"):
        raise ValueError("Translate the interface dictionary before adding another language")
    for key in ("illustrative", "calculator_supported"):
        if not isinstance(data.get(key), bool):
            raise ValueError(f"Boolean required: {key}")
    for key in NUMBERS:
        if key not in data:
            raise ValueError(f"Required field (null if unknown): {key}")
        value = data[key]
        if value is not None and (isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value)):
            raise ValueError(f"Finite number or null required: {key}")
        if value is not None:
            if key == "baseline" and not 0 < value < 1:
                raise ValueError("Baseline must be strictly between 0 and 1; use null and explain boundary cases")
            if key in ("effect", "weekly_users", "recruitment_days", "max_readout_days") and value <= 0:
                raise ValueError(f"Positive number required: {key}")
            if key.endswith("_days") and (value < 0 or int(value) != value):
                raise ValueError(f"Non-negative whole days required: {key}")
            if key == "recruitment_days" and (value < 14 or value % 7):
                raise ValueError("Recruitment requires at least 14 days in whole weeks: 14, 21, 28, ...")
    if data.get("effect_type") not in ("relative", "pp") or data.get("direction") not in ("up", "down"):
        raise ValueError("Invalid effect_type or direction")
    if not isinstance(data.get("guardrails"), list) or not isinstance(data.get("blockers"), list):
        raise ValueError("guardrails and blockers must be arrays")
    for guardrail in data["guardrails"]:
        if not isinstance(guardrail, dict) or any(not isinstance(guardrail.get(k), str) or not guardrail[k].strip() for k in ("name", "definition", "limit")):
            raise ValueError("Each guardrail needs name, definition and limit")
    if not all(isinstance(x, str) and x.strip() for x in data["blockers"]):
        raise ValueError("Blockers must be non-empty strings")


def render(data):
    validate(data)
    encoded = json.dumps(data, ensure_ascii=False, allow_nan=False)
    # Keep user-supplied text from closing the script element.
    encoded = encoded.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    replacements = {
        "__LANG__": data["language"],
        "__CARD_CSS__": (ASSETS / "card.css").read_text(),
        "__CARD_DATA__": encoded,
        "__STATS_JS__": (ASSETS / "statistics.js").read_text(),
        "__CARD_JS__": (ASSETS / "card.js").read_text(),
    }
    # One pass prevents tokens in user content from becoming template directives.
    return re.sub("|".join(map(re.escape, replacements)), lambda m: replacements[m.group()], (ASSETS / "card.html").read_text())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", type=Path)
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--summary", action="store_true", help="Use Node.js to print the planning calculation")
    args = parser.parse_args()
    if bool(args.input) == args.demo:
        parser.error("Provide an input JSON file or --demo")
    try:
        data = json.loads((ASSETS / "example.json" if args.demo else args.input).read_text())
        html = render(data)
        if args.output.exists():
            raise ValueError(f"Output already exists; choose a new version: {args.output}")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(html)
        print(args.output.resolve())
        if args.summary:
            code = "const s=require(process.argv[1]);let d='';process.stdin.on('data',v=>d+=v);process.stdin.on('end',()=>{const p=JSON.parse(d);console.log(JSON.stringify(p.calculator_supported?s.plan(p):{error:'unsupported'},null,2));});"
            subprocess.run(["node", "-e", code, str(ASSETS / "statistics.js")], input=json.dumps(data), text=True, check=True)
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"{exc}\n")


if __name__ == "__main__":
    main()
