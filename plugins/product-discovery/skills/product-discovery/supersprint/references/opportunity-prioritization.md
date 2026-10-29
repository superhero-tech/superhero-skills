# Select opportunities with PRES

Read when preparing or resuming the Opportunities stage. Use the bundled standalone `pres-prioritization` skill after formulating candidate user needs and before asking which to pursue. This is part of the existing Opportunities stage, not a new stage or tree layer. Do not use PRES to score ideas, solutions or experiments.

## Handoff and checkpoints

1. Reuse the Opportunities input checkpoint from `references/human-checkpoints.md`. Pass the actual user reply/source to `pres-prioritization` so it does not repeat an already answered input question. Include the product, current agreed goal and its status, target population, observation window, candidate IDs/statements, source paths, contradictions, constraints and cycle-relative output destination `opportunities/`.
2. Read the specialist's own instructions and rubric. It proposes P/R/E/S scores with rationale and citations, sums supported complete candidates, and keeps unknown and Evidence-1 candidates separate. If the goal is not agreed or scope is unclear, resolve the question with the human rather than inventing Strategic fit. Target values and deadlines can remain unknown if the direction is agreed. Do not fill a missing Reach with a low value or use interview counts as market prevalence.
3. Save `opportunities/pres-prioritization.md`, its scoring inputs and calculated `pres-assessment.json`. Link the scorecard from the stage narrative and display the ranking, material rationales and uncertainties. Keep `human_gates.stages.opportunities` at `awaiting_review`; the generated ranking does not select an opportunity.
4. Ask for human review of the scorecard and then the focus selection, one consequential question at a time. One response may do both explicitly. If the user only approves scores, request the selection before entering Ideas. PRES's review satisfies the matching router checkpoint; do not request approval twice for the same revision. Capture corrections, re-score and show the updated comparison for review. A choice below the highest total remains a valid human choice; preserve its reason and risk.
5. Only after the selected focus and review are resolved, update `selected_opportunity_id`, the stage acceptance record and decision history. Explicit scoped delegation is recorded as delegation. Keep alternatives, near-ties, incomplete and research-first candidates visible. Continue to the Ideas input checkpoint, not directly into solution generation.

## Saved state and tree

The router owns state. Store `opportunity_prioritization` with:

- `method: "PRES"`, `revision`, `goal_id`, `population`, `window`, `source_refs`.
- Cycle-relative `artifact_path` and `assessment_path`.
- `review_status`, `reviewed_revision`, `review_source_refs` for the actual human review, distinct from computational completeness.
- Candidate records returned by the specialist, retaining IDs, axes, per-axis rationales/source references, total or null, and `assessment_status`.

Project the matching assessment into each opportunity's optional `pres` metadata. Keep natural-language titles intact; add a brief localized comparison result to its summary or preview only when useful. For missing totals show an explicit gap or research-first status, never zero. Use the source scorecard for the full four-axis explanation. Do not duplicate a full scoring table inside every click preview. Keep existing evidence links and the human-selected path unchanged while the ranking is proposed. There is no PRES node or additional layer.

On resume, reuse current reviewed scores if the goal, population, evidence and candidates are unchanged. An accepted existing focus is not reopened just because this skill was added to the plugin. If a material input changed, flag the affected assessment for review and retain prior decisions; do not silently replace the winner. Old states without `opportunity_prioritization` remain valid. Initialize this record when actually doing a new comparison, not by manufacturing historical scores.

If `pres-prioritization` is unavailable, name the missing capability and preserve the current state and checkpoint. A scoped descriptive comparison may be offered as a fallback, but do not call it a completed PRES assessment.
