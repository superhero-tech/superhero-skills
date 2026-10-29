---
name: pres-prioritization
description: Prioritize product opportunities using Pain, Reach, Evidence and Strategic fit. Use when comparing user needs or problems, scoring opportunities with PRES, or reviewing an opportunity ranking; not for ranking solutions or experiments.
metadata:
  ready_to_publish: "true"
---

# PRES Prioritization

Compare customer needs, pains and desires against a shared product outcome. Make the evidence and disagreements inspectable; the score supports the human's choice rather than making it.

Respond and produce all artifacts in the user's conversation language.

This skill is self-contained. It can work from a message, brief, research files or an existing discovery cycle. It requires neither an OST, Supersprint, personal knowledge vault nor another skill. PRES here means the opportunity-scoring convention defined in `references/pres-rubric.md`; do not attribute it to Teresa Torres as her framework.

## 1. Establish the comparison and invite input

Read the conversation and relevant supplied context. Establish the product, target population, agreed outcome, candidate opportunities, available sources and destination. Ask one focused question at a time about material gaps. A missing numerical target is acceptable; an absent direction or outcome prevents scoring Strategic fit and an overall ranking.

Read `references/pres-rubric.md` before scoring. Explain the four dimensions and additive calculation briefly. Invite the human to add missing opportunities, evidence, constraints or concerns before preparing the comparison, then wait. A current message supplying that input satisfies this checkpoint; do not ask again. Explicit permission to draft with no extra input also suffices.

An opportunity describes a user need/problem, not a feature or implementation. If candidates are solutions, propose the underlying needs and ask for confirmation before scoring. Keep the original candidate IDs and record any accepted rewording. Compare at a similar level of detail and against the same outcome/population; split materially different segments rather than averaging away their differences.

## 2. Prepare evidence-backed scores

For each candidate:

1. State the need, who experiences it and in which situation. Retain its sources and relevant counterevidence.
2. Assess **Evidence first**. If Evidence = 1, label the candidate `research-first`, leave its total empty and identify the smallest research that could change that status. Continue assessing other candidates; one weak candidate does not block the entire comparison.
3. For eligible candidates, propose integer **Pain**, **Reach**, **Evidence** and **Strategic fit** scores from 1 to 5 using the rubric. Give each score a short rationale and an exact source reference. Separate observed facts, human judgments and agent inferences.
4. Leave an unsupported axis `unknown`, with its missing evidence named. An unknown reach is not a small reach; an unknown effect is not a weak strategic fit. Do not manufacture a 1 or 2 merely to complete the table. A total is unavailable until all four axes are supported.
5. Calculate **PRES = P + R + E + S**, an unweighted sum from 4 to 20. Do not multiply, normalize, add effort or silently introduce weights. For this workflow, candidates with Evidence = 1 remain outside the scored ranking even though four numerical axes could mathematically sum to a value.
6. Sort complete, eligible candidates by total. Keep incomplete and research-first candidates visible in separate sections, without treating them as the lowest-ranked opportunities. A total cannot establish prevalence, causal impact or a solution's effectiveness.

Evidence citations must resolve to the supplied material: file/section or URL/passage, and the supporting quote or data point where needed. Deduplicate people, organizations, events and underlying datasets across reports. More quotations from the same event do not create independent corroboration. Opposing evidence remains next to the affected score.

## 3. Compare and request human review

Use `references/output-format.md`. Present one table with candidate ID, natural-language need, P/R/E/S, total and review status. Follow with concise per-axis rationales and source references, disagreements and missing evidence. Recommend a focus with reasons, retaining alternatives and limits.

Treat differences of one point or less as near-ties for discussion, not decisive superiority. Explain which uncertain assessment could change the order. Do not break ties automatically by Reach, ID or the model's preference. Ask the human to correct the scores and choose which opportunities to pursue, then wait. Revisions require another review; seeing the table or saying there is nothing to add at intake is not approval.

A recommendation, approval of the scorecard and selection of an opportunity are distinct. Record the user's exact decision and relevant message/source. If the human selects a lower-scored or research-first candidate, preserve that choice and its rationale or unresolved risk. Do not silently rescore it to make the decision appear numerically inevitable. Only explicit scoped delegation allows the agent to make that choice, recorded as delegated rather than human-approved.

## 4. Save and hand back

Save `pres-prioritization.md` in the user's chosen location, normally an `opportunities/` folder in the current project. Use a run-specific directory if that would overwrite earlier results. Keep the outcome, segment, source references, scores, unknowns, review status and human decision together. Keep filenames in English and content in the user's language.

For reproducible totals and machine-readable handoff, read `references/scoring-data.md` and run `scripts/score_pres.py`; save its output beside the scorecard. It validates structure and arithmetic, not evidence quality or human approval.

If called by another workflow, return candidate IDs, four-axis assessments, eligible totals, limitations and the actual review/selection status. The caller owns its state and tree. Do not select nodes, replace prior decisions or alter a shared cycle merely because a table was produced. Existing accepted rankings may be reused if their outcome, evidence and scope remain current; flag affected scores when inputs change.

Markdown is the default deliverable. If an HTML comparison is requested, read `references/html-style.md` and inline `assets/html-style.css`; preserve the same content and review status with no remote assets or runtime. Prefer the host's built-in browser when permitted. If access is blocked, save the HTML and report the unverified preview without attempting to bypass the restriction.

Before delivery, check the arithmetic, source references, consistent population/window, separation of unknowns from low scores, exclusion of Evidence-1 candidates from totals, and the difference between proposed scores and human choices. Return the saved scorecard link, main comparison and pending human decision. Never claim that scoring validates a solution or executes an experiment.
