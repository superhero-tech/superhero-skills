#!/usr/bin/env python3
"""Render an agent-authored process model as one offline HTML board (stdlib only)."""
import argparse
import copy
import html
import json
import re
from pathlib import Path

PALETTE = {
    "DOMAIN EVENT": "#FF9F43", "COMMAND": "#6CB5F9", "POLICY": "#C6A0E8",
    "ACTOR": "#FFE066", "READ MODEL": "#A8D98D", "EXTERNAL SYSTEM": "#F4A6C1",
    "HOT SPOT": "#F87171", "AGGREGATE": "#FFF2B3",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def string(obj, key):
    require(isinstance(obj.get(key), str) and bool(obj[key].strip()), f"Text required: {key}")


def inside(repo, path):
    target = (repo / path).resolve()
    require(target.is_relative_to(repo), f"Path outside the project: {path}")
    return target


def evidence(item, repo, files):
    require(isinstance(item.get("sources"), list) and item["sources"], "Card or command note requires sources")
    for source in item["sources"]:
        require(isinstance(source, dict), "A source must be an object")
        string(source, "path")
        require(not Path(source["path"]).is_absolute(), "A source requires a relative path")
        target = inside(repo, source["path"])
        if target not in files:
            files[target] = target.read_text(encoding="utf-8").splitlines()
        lines = files[target]
        start, end = source.get("line"), source.get("end", source.get("line"))
        require(type(start) is int and type(end) is int and 1 <= start <= end <= len(lines),
                f"Source range does not exist: {source['path']}:{start}–{end}")
        require(end - start < 40, "A source excerpt exceeds 40 lines")
        source["excerpt"] = "\n".join(f"{i + 1:>4}  {lines[i]}" for i in range(start - 1, end))
        source["end"] = end


def prepare(model, repo):
    """Validate before writing; embed bounded, current source excerpts."""
    repo = Path(repo).resolve()
    data = copy.deepcopy(model)
    require(isinstance(data, dict), "The model must be an object")
    for key in ("title", "summary"):
        string(data, key)
    require(isinstance(data.get("lanes"), list) and data["lanes"], "At least one process is required")
    ids, lane_ids, files = set(), set(), {}
    for lane in data["lanes"]:
        require(isinstance(lane, dict), "A process must be an object")
        for key in ("id", "title", "description"):
            string(lane, key)
        require(lane["id"] not in lane_ids, f"Duplicate process ID: {lane['id']}")
        lane_ids.add(lane["id"])
        require(isinstance(lane.get("nodes"), list) and lane["nodes"], "A process requires at least one card")
        require(isinstance(lane.get("edges"), list), "An edges list is required")
        cells, local = set(), {}
        for node in lane["nodes"]:
            require(isinstance(node, dict), "A card must be an object")
            for key in ("id", "type", "title", "detail"):
                string(node, key)
            require(node["id"] not in ids, f"Duplicate card ID: {node['id']}")
            require(node["type"] in PALETTE, f"Unknown card type: {node['type']}")
            ids.add(node["id"])
            local[node["id"]] = node
            for key in ("col", "row"):
                require(type(node.get(key)) is int and 0 <= node[key] <= 100,
                        f"{key} must be an integer from 0 to 100")
            cell = (node["col"], node["row"])
            require(cell not in cells, f"Overlapping cards: {cell}")
            cells.add(cell)
            evidence(node, repo, files)
            for key in ("rules", "outcomes"):
                notes = node.get(key, [])
                require(isinstance(notes, list), f"{key} must be a list")
                require(not notes or node["type"] == "COMMAND", f"{key} is only allowed on commands")
                for note in notes:
                    require(isinstance(note, dict), "A command note must be an object")
                    string(note, "text")
                    evidence(note, repo, files)
        for edge in lane["edges"]:
            require(isinstance(edge, dict), "An edge must be an object")
            for key in ("from", "to", "kind", "label"):
                string(edge, key)
            require(edge["from"] in local and edge["to"] in local,
                    f"Unknown edge endpoint: {edge['from']} → {edge['to']}")
            require(edge["from"] != edge["to"], "An edge cannot connect a card to itself")
            require(edge["kind"] in ("flow", "information", "annotation"), "Unknown edge kind")
            a, b = local[edge["from"]], local[edge["to"]]
            has_hotspot = "HOT SPOT" in (a["type"], b["type"])
            if edge["kind"] == "annotation":
                require(has_hotspot, "An annotation must connect to a hot spot")
            else:
                require(not has_hotspot, "A hot spot requires an annotation edge")
            if edge["kind"] == "flow":
                require("READ MODEL" not in (a["type"], b["type"]), "A read model requires an information edge")
                require(a["col"] < b["col"], "A flow edge must point to a later column")
    return {"title": data["title"], "summary": data["summary"], "lanes": data["lanes"], "palette": PALETTE}


def render(model, repo):
    data = prepare(model, repo)
    # JSON in a raw-text script must never contain an HTML closing tag.
    payload = json.dumps(data, ensure_ascii=False).replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e")
    template = (Path(__file__).parent.parent / "assets" / "board.html").read_text(encoding="utf-8")
    replacements = {"__TITLE__": html.escape(data["title"]), "__MODEL__": payload}
    return re.sub(r"__TITLE__|__MODEL__", lambda match: replacements[match[0]], template)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, default=Path("docs/event-storming.html"))
    args = parser.parse_args()
    try:
        repo = args.repo.resolve(strict=True)
        output = inside(repo, args.output)
        require(output.suffix.lower() == ".html", "The output must have an .html extension")
        model_path = inside(repo, args.model)
        require(output != model_path, "The output cannot overwrite the model")
        result = render(json.loads(model_path.read_text(encoding="utf-8")), repo)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(result, encoding="utf-8")
        print(output)
    except (ValueError, OSError) as error:
        parser.exit(2, f"Error: {error}\n")


if __name__ == "__main__":
    main()
