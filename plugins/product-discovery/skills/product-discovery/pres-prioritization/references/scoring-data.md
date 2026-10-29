# Reproducible scoring data

The bundled helper checks axis values and calculates sums. It does not assess source quality, verify references, approve the scorecard, choose an opportunity or modify files.

Use it when producing a saved comparison or handing scores back to another workflow:

```sh
python3 <skill-directory>/scripts/score_pres.py <run>/pres-input.json
```

Read stdout as the calculated view; save it as `pres-assessment.json` beside the Markdown scorecard. Use the actual skill directory discovered by the host. No packages beyond Python's standard library are required.

Input has `outcome` (agreed direction or null), `population`, `window`, `revision`, `review_status`, `selected_opportunity_ids` and `opportunities`. Each opportunity has a stable `id`, `statement`, and `scores` with exactly `pain`, `reach`, `evidence`, `strategic_fit`. Each axis is an object:

```json
{"value": null, "rationale": "Name the missing evidence, or explain the proposed numeric score.", "source_refs": []}
```

A numeric value must be an integer 1-5 with at least one real source reference; null means unknown and may have an empty source list. For Evidence = 1 cite the actual human hypothesis or source audit establishing the evidence gap. For research-first candidates keep other axes null rather than manufacturing scores. Do not copy this shape example as project evidence.

Output retains every candidate and its source/decision metadata, replaces calculated `total`/`assessment_status`, and adds `comparison`: complete candidates' `eligible_ids` in descending total order, separate `incomplete_ids` and `research_first_ids`, and all `near_ties` within one point. Equal totals retain input order for display only; this is not a tie-break rule or selection. A missing outcome prevents any total; Evidence = 1 takes research-first precedence. The helper never changes `review_status` or `selected_opportunity_ids`.

Check the cited materials yourself and present the human-readable rationales. A structurally valid source reference or total is not proof of evidence quality, human approval or causal impact. Preserve the distinction between assessment completeness (`scored`, `incomplete`, `research-first`) and human review (`proposed`, `approved`, `revised`, or explicit delegation).
