---
name: supersprint
description: Run Supersprint from product context to an evidence-supported decision, routing specialists and showing a growing discovery tree. Use when starting, resuming or reviewing a Supersprint cycle.
metadata:
  ready_to_publish: "true"
---

# Supersprint

Lead the cycle: goal -> signals -> opportunities -> ideas -> experiments -> observed results -> decision. Keep the tree visible as the work develops, not only at the end.

Respond and produce all artifacts in the user's conversation language.

Use natural, descriptive names throughout the tree. Titles and previews should say who does what, with which specific information or product change, and what we want to learn. Preserve these details when shortening specialist findings; prefer a few clear sentences to opaque shorthand. Apply the standalone readability check in `references/progressive-tree.md` before showing each update.

## Intake and resume

Read `references/intake-and-routing.md`, `references/human-checkpoints.md` and `references/guided-navigation.md` first. Identify the product with the human before analysis; ask about a missing outcome and wait for the answer, including an explicit "not known yet". A supplied brief or current answer can establish this context without repetition. Persist the product and context on the Canvas/tree even before a goal exists.

Resolve the product folder and cycle from the conversation or workspace. Ask only if ambiguity materially changes the destination or work. Read project instructions, brief, entry point, current state and active-stage artifacts before raw files. Reuse accepted choices. Resume the actual waiting point instead of replaying all stages.

For a new cycle use `assets/state-template.json` under `supersprint/<cycle>/`. Choose a meaningful cycle name from context; do not overwrite an existing cycle. Store input references, separate stage Markdown files, analyses and `tree/` here. Keep raw sources unchanged and executable code in the skill/code repository, not a knowledge vault.

The router owns the cycle state and material decision history. Specialists own their native analysis artifacts; import their findings with source paths and review status instead of requiring them to rewrite shared state. Existing state formats are supported: preserve fields and IDs, adding a tree projection if needed rather than migrating everything.

## Progress through the cycle

1. **Goal:** identify whose behavior should change, how it relates to a business priority and how it could be measured. Reuse a suitable brief outcome. If missing, first ask the human what outcome they want and wait; help define a working goal after their response. When evidence is insufficient, keep an explicit working direction or research question for review. Unknown baseline, target or deadline stays unknown. A measurement window is not a delivery deadline.
2. **Signals:** distinguish available inputs, completed analysis and enough evidence for the next decision. Reuse current relevant analyses. Name gaps, contradictions, source versions and limits. Missing signal categories do not require filling every folder. Suggest the smallest research that can change the decision; allow consciously proceeding with stated uncertainty. Before presenting opportunities, project analyzed observations into stable signal cards and connect them to the supported opportunity candidates; source files alone do not replace the Signals layer.
3. **Opportunities:** formulate user needs/problems in natural user language, then follow `references/opportunity-prioritization.md` and use `pres-prioritization` before selecting a focus. Present supported P/R/E/S scores, sums, gaps and recommendations for human review. Record the actual selection or explicit delegation; a scorecard does not select the highest total automatically. Keep alternatives and rationale. A need is not a proposed feature.
4. **Ideas:** compare distinct approaches by fit, potential and constraints. Describe the concrete mechanism. Keep user-selected ideas; do not impose a fixed number or reopen an accepted gate without a material reason.
5. **Experiments:** use `experiment-design` on the selected ideas and relevant evidence. The assumption belongs inside the experiment's hypothesis, not a separate tree layer, stage or duplicated list. Explain hypothesis, concrete method/action and observable change. Preserve the portfolio; recommend a next test without selecting it for the user. Expected change is directional by default; the human judges sufficiency unless numerical criteria were supplied or requested.
6. **Results:** register actual observations, scope, execution and review status. A plan, role-play or synthetic case is not customer evidence. Read results in the context of what the method tests; clicks, use, payment and repeat purchase answer different questions.
7. **Decision:** record develop, revise, discard or research further, with supporting evidence, uncertainty, next action and owner. A cycle ends with a supported decision, not necessarily a build. Keep production implementation as a subsequent scoped task.

## Guide the next move

Own the route through the cycle, including after specialists return. At each stopping point, briefly say where we are and what decision comes next, recommend one concrete action with a reason, and offer two or three useful choices in total when a real choice exists. Follow `references/guided-navigation.md` for stage transitions, research alternatives and resuming the chosen route. Do not leave the user with only a report link or "what would you like to do next?".

After quantitative analysis, explicitly consider qualitative work, targeted desk research, or proceeding to Opportunities if the human considers their knowledge sufficient. Adapt the recommendation to the remaining gap and available material; none of these methods is a compulsory checkbox. Honor a conscious choice to proceed, retaining evidence limits and unknown PRES axes. At other stages, offer options relevant to that stage rather than returning to research by default.

Keep the current goal and decision as the anchor for each specialist task. Integrate its result and return to that decision; do not drift into another product, broad research or building a suggested feature without a user-directed change. Save the recommendation, alternatives, actual choice and return point in `navigation`, with the immediate next step in `next_action`. Resume the actual waiting point and follow an already chosen route instead of asking the same menu again. Recommendations never replace human review or focus selection.

## Human checkpoints

At every stage follow `references/human-checkpoints.md`: ask for the human's input and wait, prepare the stage after their reply, show the saved draft and updated tree, then ask for review and wait. Corrections lead to a revised draft and another review. Advance only after approval of that revision, then invite input for the next stage. Existing files or a request to run the whole cycle do not waive these checkpoints.

Persist the exact waiting point, input provenance and reviewed revision in `human_gates`. Resume there without replaying accepted unchanged stages. Ask one consequential question at a time; specialist review can satisfy the matching checkpoint. Only explicit, scoped user delegation can waive a checkpoint, and it must be recorded as delegation rather than human approval.

Save `context/product.md` and `state.product_context` as soon as the human identifies the product. Keep product, users and outcome/unknown visible above the tree. Update the same native Canvas when the host supports the intended surface; otherwise use the local context document and HTML and state that fallback honestly.

## Specialist routing

The plugin includes all seven specialists listed below. Discover them by skill name in the host, including its plugin namespace when required, and read the relevant specialist before using it. Resolve bundled resources relative to each skill directory; no personal vault or development-repository path is required. Pass the agreed question, decision, segment, selected input paths, constraints, destination and return condition. Include the requirement for natural, descriptive titles and self-contained explanations in each specialist handoff. Specialists clarify their canonical artifacts before the router shortens them; the router checks that the concrete meaning survives. This language quality belongs to Supersprint and its specialists and must not depend on a separate editing skill. Use only the route that addresses an actual gap:

| Gap | Specialist |
|---|---|
| Patterns and measurements in supplied data | `data-analysis` |
| Themes and evidenced needs in transcripts | `affinity-mapping` |
| New conversations need a screener and guide | `interview-plan` |
| Public accounts of customer experience | `customer-research` |
| Competitive, secondary or research evidence | `desk-research` |
| Comparing opportunities and selecting a focus with PRES | `pres-prioritization` |
| Concrete tests for selected ideas | `experiment-design` |

If a specialist is unavailable, report the missing capability and choose a feasible scoped fallback. Do not pretend it ran. Separate agents are optional only when available and authorized; routing normally means following the specialist within this conversation. When a specialist finishes, return to this router: update the cycle/tree and guide the next decision using `references/guided-navigation.md`.

## Grow, save and show the tree

Read `references/progressive-tree.md` before the first tree update. After a meaningful new proposal, analysis finding, selection, test plan or supplied result, and at every stage transition:

1. Save the stage narrative, product context and state, maintaining stable IDs, source references, checkpoint/review and selection status. Record what materially changed and why. A draft tree update does not accept the stage.
2. Project only existing work into the tree. Save/refresh the same `tree/tree.html` and `tree/tree.mmd`; snapshot significant structural changes with the state. Do not prefill future branches.
3. Show the updated tree to the user now, using the host's visible built-in browser and reusing its tab when supported. Say briefly what was added or changed and the current next step. Do not wait for the full cycle to finish.

Run the bundled renderer after updating the state/projection:

```sh
python3 <skill-directory>/scripts/render_tree.py <cycle>/state.json --output <cycle>/tree/tree.html --snapshot
```

The renderer accepts both a new state's `nodes`/`edges` and an existing `tree.projection_path` graph. Set a new `tree.revision` for material changes before requesting a snapshot. A cosmetic change can rerender without `--snapshot`. See the reference for node fields, localization and links.

Render horizontal stage bands from top to bottom: goal -> signals -> opportunities -> ideas -> tests/experiments, followed by real results and decision only when available. Signals are a required visible layer between goal and opportunities whenever signal records exist. With this layer present, draw goal connectors only to signals; do not draw goal -> opportunity bypasses. Show each signal once in a single Signals band, never grouped or duplicated by opportunity. Draw outgoing signal links only to opportunities, never directly to ideas, tests, results, decisions or other signals. Keep any detailed source references in the linked artifacts. Use orthogonal elbow connectors. Draw evidence links to every relevant opportunity by default; one signal can support several opportunities and one opportunity can have several signals. Record these links explicitly in the graph; do not infer evidence from card placement. Keep unassigned signals visible and unsupported opportunities explicitly marked as evidence gaps. Selected paths stay clearly framed; recommendations and temporary inspection have different treatments. Each layer gets a short node summary, a few sentences in the click preview and a prominent full-source link. Experiment previews retain hypothesis, practical method and measurement, not the full protocol.

Use the top-to-bottom layout, stage colors, spacing, zoom, and inspection behavior in `references/progressive-tree.md`; the bundled renderer implements these defaults. Use the accepted SF neutral style: `references/html-style.md` and the packaged `assets/html-style.css`. Different artifacts may use different layouts while keeping this visual family. The renderer is offline and self-contained.

If browser policy blocks access, save the artifacts, provide the file link and a concise change summary or inline Mermaid fallback. State that automatic preview was not confirmed; do not bypass the block through another browser, protocol or local server. Text-only user preferences take precedence.

Miro/FigJam is optional. Check an available integration and access, remember the user's target and update only the managed region where supported. Never let external-board availability block the local state/tree. Do not overwrite manual board changes without reconciliation.

## PDF export

When a PDF is requested, read `references/pdf-export.md` and run the renderer with `--pdf`. Use this default PDF format: the original vector tree first, followed by compact A4 landscape tables for signals, opportunities, ideas and tests/experiments (and results/decisions when present). Preserve the full tree cards, including signal titles, summaries, statuses, elbow connectors and the selected path. Keep its original layout on a graph-sized page that can be zoomed; do not replace signal cards with ID-only chips or shrink the tree to fit a fixed paper size. Compact only the accompanying tables: ID, full title, incoming/outgoing ID mappings, status and source links. Do not duplicate full previews or write a paragraph for every edge. Use `--pdf-layout full` only when the user explicitly wants the complete description catalogue. The HTML then includes a download link. Generate both from the same normalized graph; refresh the PDF after graph changes. Render and visually verify the PDF before sharing it.

## Source changes and handoff

On resume, check state and view revisions plus relevant source changes. Preserve previous results and choices; mark affected conclusions for review rather than silently treating them as current. Do not count the same interview, person or event twice because several reports cite it.

End a working turn with the updated tree link, the meaningful change, the current stage and a recommended next action with relevant alternatives or the precise pending human choice. If that choice was already made, carry out the authorized work instead of offering it again. Keep dates, execution status and evidence limits honest. Tree updates happen while the agent works in the conversation; do not claim independent background automation.
