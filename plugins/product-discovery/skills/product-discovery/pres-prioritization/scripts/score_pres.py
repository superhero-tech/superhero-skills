#!/usr/bin/env python3
"""Sprawdź uzasadnienia ocen PRES i oblicz sumy bez wybierania szansy."""
import argparse
import copy
import json
from pathlib import Path

AXES = ('pain', 'reach', 'evidence', 'strategic_fit')


def assess(data):
    if not isinstance(data, dict) or not isinstance(data.get('opportunities'), list):
        raise ValueError('Expected an opportunities list')
    output = copy.deepcopy(data)
    ids = set()
    eligible = []
    incomplete = []
    research_first = []
    for item in output['opportunities']:
        identity = item.get('id')
        if not isinstance(identity, str) or not identity.strip() or identity in ids:
            raise ValueError('Opportunity IDs must be unique nonempty strings')
        ids.add(identity)
        if not isinstance(item.get('statement'), str) or not item['statement'].strip():
            raise ValueError('Each opportunity needs a statement')
        scores = item.get('scores')
        if not isinstance(scores, dict) or set(scores) != set(AXES):
            raise ValueError('Provide exactly the four PRES axes')
        for axis in AXES:
            record = scores[axis]
            if not isinstance(record, dict):
                raise ValueError('Each axis needs a record')
            value = record.get('value')
            if value is not None and (type(value) is not int or not 1 <= value <= 5):
                raise ValueError('Scores must be integer 1-5 or null for unknown')
            if not isinstance(record.get('rationale'), str) or not record['rationale'].strip():
                raise ValueError('Every axis needs a rationale or a named evidence gap')
            refs = record.get('source_refs')
            if not isinstance(refs, list) or any(not isinstance(ref, str) or not ref.strip() for ref in refs):
                raise ValueError('source_refs must be a list of nonempty strings')
            if value is not None and not refs:
                raise ValueError('Every numerical score needs source references')
        item['total'] = None
        if scores['evidence']['value'] == 1:
            item['assessment_status'] = 'research-first'
            research_first.append(identity)
        elif any(scores[axis]['value'] is None for axis in AXES) or not str(data.get('outcome') or '').strip():
            item['assessment_status'] = 'incomplete'
            incomplete.append(identity)
        else:
            item['total'] = sum(scores[axis]['value'] for axis in AXES)
            item['assessment_status'] = 'scored'
            eligible.append(item)
    eligible.sort(key=lambda item: -item['total'])
    output['comparison'] = dict(
        eligible_ids=[item['id'] for item in eligible],
        incomplete_ids=incomplete,
        research_first_ids=research_first,
        near_ties=[[a['id'], b['id']] for i, a in enumerate(eligible) for b in eligible[i+1:] if abs(a['total'] - b['total']) <= 1],
    )
    # Dane wejściowe zachowują wybory i przegląd; obliczenie nie nadaje im statusu.
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    args = parser.parse_args()
    try:
        result = assess(json.loads(args.input.read_text(encoding='utf-8')))
    except (OSError, ValueError, TypeError, KeyError) as error:
        parser.exit(1, f'Error: {error}\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
