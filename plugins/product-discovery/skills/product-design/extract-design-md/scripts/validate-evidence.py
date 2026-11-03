#!/usr/bin/env python3
"""Check saved measurements and their references; does not judge visual fidelity."""
import json
from pathlib import Path
import sys


def validate(directory):
    base = Path(directory).resolve()
    errors = []

    def check(condition, message):
        if not condition:
            errors.append(message)

    def artifact(relative):
        if not isinstance(relative, str) or not relative:
            raise ValueError('Missing artifact path')
        target = (base / relative).resolve()
        if not target.is_relative_to(base):
            raise ValueError('Artifact path leaves evidence directory')
        if not target.is_file():
            raise ValueError(f'Artifact does not exist: {relative}')
        return target

    try:
        manifest = json.loads((base / 'manifest.json').read_text())
        if not isinstance(manifest, dict):
            raise ValueError('Manifest must be an object')
    except (OSError, ValueError) as exc:
        return [f'Manifest: {exc}']
    check(manifest.get('schemaVersion') == '2.0', 'Manifest version must be 2.0')
    check(isinstance(manifest.get('checks'), list), 'Manifest must list checks (including skipped probes)')
    check(isinstance(manifest.get('limitations'), list), 'Manifest must list limitations')
    snapshots = manifest.get('snapshots', [])
    if not isinstance(snapshots, list) or not snapshots:
        return errors + ['Manifest must contain at least one successful snapshot']
    ids = set()
    paths = set()
    for entry in snapshots:
        try:
            if not isinstance(entry, dict):
                raise ValueError('Snapshot entry must be an object')
            sid = entry.get('id')
            check(isinstance(sid, str) and bool(sid) and sid not in ids, f'Duplicate/missing snapshot id: {sid}')
            ids.add(sid)
            check(entry.get('path') not in paths, f'Duplicate snapshot path: {entry.get("path")}')
            paths.add(entry.get('path'))
            raw = json.loads(artifact(entry.get('path')).read_text())
            check(raw.get('schemaVersion') == '2.0', f'{sid}: snapshot version must be 2.0')
            source = raw.get('source', {})
            check(isinstance(source.get('url'), str) and source['url'].startswith(('http://', 'https://')), f'{sid}: missing HTTP source URL')
            check(bool(source.get('extractedAt')), f'{sid}: missing extraction date')
            viewport = source.get('viewport', {})
            check(all(isinstance(viewport.get(p), (int, float)) and viewport[p] > 0 for p in ('width', 'height')), f'{sid}: invalid viewport')
            check(bool(raw.get('state', {}).get('label')), f'{sid}: missing observed state label')
            elements = raw.get('elements', [])
            check(isinstance(elements, list) and bool(elements), f'{sid}: no measured elements')
            by_id = {}
            for el in elements:
                eid = el.get('id')
                check(bool(eid) and eid not in by_id, f'{sid}: duplicate/missing element id: {eid}')
                check(bool(el.get('selector')), f'{sid}/{eid}: missing source selector')
                check(isinstance(el.get('styles'), dict), f'{sid}/{eid}: missing computed styles')
                by_id[eid] = el
            coverage = raw.get('coverage', {})
            check(coverage.get('sampledElements') == len(elements), f'{sid}: wrong sampled element count')
            check(isinstance(coverage.get('limitations'), list), f'{sid}: missing coverage limitations')
            for comp in raw.get('components', []):
                check(comp.get('elementId') in by_id, f'{sid}: component references unknown element')
            for kind, tokens in raw.get('tokens', {}).items():
                for token in tokens:
                    evidence = token.get('evidence', [])
                    check(bool(evidence), f'{sid}/{kind}: token has no evidence')
                    for ref in evidence:
                        el = by_id.get(ref.get('elementId'))
                        if not el:
                            errors.append(f'{sid}/{kind}: unknown token source element')
                            continue
                        styles = el.get('styles', {})
                        if kind == 'typography':
                            value = token.get('value', {})
                            props = ref.get('properties', [])
                            check(bool(props) and isinstance(value, dict) and set(props) == set(value), f'{sid}/{kind}: incomplete type reference')
                            check(all(prop in styles and styles[prop] == value.get(prop) for prop in props), f'{sid}/{kind}: typography differs from source')
                        else:
                            prop = ref.get('property')
                            check(prop in styles and styles[prop] == token.get('value'), f'{sid}/{kind}: token differs from source property {prop}')
        except (OSError, ValueError, TypeError, AttributeError) as exc:
            errors.append(f'Snapshot: {exc}')
    screenshots = manifest.get('screenshots', [])
    if not isinstance(screenshots, list):
        return errors + ['Screenshots must be a list']
    shot_ids = set()
    for shot in screenshots:
        try:
            check(shot.get('snapshotId') in ids, 'Screenshot references unknown snapshot')
            check(shot.get('capture') in ('viewport', 'full-page', 'element'), 'Screenshot must state capture extent')
            check(bool(shot.get('id')) and shot['id'] not in shot_ids, 'Duplicate/missing screenshot id')
            shot_ids.add(shot.get('id'))
            artifact(shot.get('path'))
        except (OSError, ValueError, TypeError, AttributeError) as exc:
            errors.append(f'Screenshot: {exc}')
    if not screenshots:
        skipped = any(isinstance(c, dict) and c.get('kind') == 'screenshot' and c.get('status') in ('skipped', 'failed') for c in manifest.get('checks', []))
        check(skipped, 'No screenshot: record a skipped/failed screenshot check')
    return errors


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: validate-evidence.py <design-evidence-directory>', file=sys.stderr)
        sys.exit(2)
    issues = validate(sys.argv[1])
    if issues:
        print('\n'.join(f'ERROR: {issue}' for issue in issues), file=sys.stderr)
        sys.exit(1)
    print('Evidence references and token values are consistent. Visual review still required.')
