# Progressive tree contract

The tree is the visible working memory of the cycle. Update it during the conversation and show it after material work, not only at completion. Preserve the same artifact path and browser tab where possible.

## Persistent product Canvas and checkpoints

Follow `references/human-checkpoints.md`. Above the graph, always show the product name, a short description, intended users, the current goal or an explicit unknown, and the active human checkpoint. Display this block even for a zero-node tree. Read it from the cycle's state and `context/product.md`, not a hidden personal context source. Show proposals as proposals; the product context does not create a new tree layer. Mirror it to the intended native Canvas only when that surface is writable through supported capabilities.

Refreshing the Canvas/tree never accepts a stage. A proposed stage stays `awaiting_review` until the human approves its exact revision. Keep the input and review checkpoints distinct and preserve the current waiting point on resume.

## What appears when

| Work completed | Visible update |
|---|---|
| Initial problem/direction only | Show the working question in the page context; do not invent a finished goal |
| Goal proposed or adopted | Add the goal with proposed/provisional/accepted status |
| Signals analyzed | Add unique evidenced signal cards in the Signals band between Goal and Opportunities, even before opportunities exist |
| Opportunity candidates written | Add candidates with evidence links; none is selected merely because shown |
| Focus selected | Emphasize the selected opportunity and path, retaining alternatives |
| Ideas developed/selected | Add actual ideas and distinguish proposals from selections |
| Tests designed | Connect ideas directly to tests, with hypothesis, method/action and expected measurement inside the test |
| Real observations supplied | Add observed results with their provenance and review status |
| Decision reached | Add the actual decision and next action; preserve remaining uncertainty |

A rerender is not a new decision. Do not ask permission just to refresh a reversible view. Show the change before moving into a new stage so the human can follow the developing structure. Preserve previously authorized choices; do not treat an example of formatting as a selected branch.

## State and graph

The router writes the project's state, not the renderer. For new cycles use `assets/state-template.json`: store localized actual node/edge records in `nodes` and `edges`. Existing cycles may retain a separate graph at `state.tree.projection_path`; the renderer reads it without migrating or rewriting the state.

Each node has:

- Stable `id` and `type`: `goal`, `opportunity`, `idea`, `experiment`, `signal`, `result`, or `decision`.
- `title` (or existing `label`), `summary`, `status`, optional localized `status_label`.
- `preview_blocks`: a short list of localized `{label, body}` objects. Use a few sentences for context, not the complete source document.
- `artifact_path` or `source_path`: a cycle-relative source document path, or a safe HTTP(S) source URL.
- Optional `selected` and `recommended` booleans; for existing cycles selection IDs in state take precedence when present.
- An experiment may instead have `card: {title, hypothesis, experiment, observable}`. Its preview uses these three concise fields. Keep full explanations in its source plan.

Edges have `source`, `target` node IDs and a relation `type`; evidence/reference relations must remain distinguishable from the main structural links. For new graphs use goal -> signal context links (`context`) when the relationship is established, signal -> opportunity evidence links (`evidence`), opportunity -> idea and idea -> experiment structural links (`supports`). A shared signal keeps one stable ID and separate outgoing evidence edges to all supported opportunities. Keep analyzed signals without an assigned opportunity too. Missing signals or missing evidence must be stated as gaps; never invent a signal or a link to complete the picture. Existing graph directions, IDs and relationships remain intact in state on resume. In HTML and Mermaid, outgoing signal connectors are drawn only when the target is an opportunity; legacy signal links to other node types remain stored but are not drawn, including during inspection. Goal -> signal context links remain visible. When signals exist, hide outgoing goal links to later layers. For legacy signal -> goal evidence, add a view-only goal -> signal context connector derived from that existing relationship, deduplicating explicit context links. Preserve the original evidence edge in state and the projection; do not infer a goal association merely from sharing a cycle. Without a Signals layer, retain existing goal connections in a partial tree. Renderer validation rejects dangling edges and duplicate IDs. Do not include assumption nodes: the hypothesis belongs inside the test. Keep history/internal assumption IDs in existing state if needed.

Populate all labels, summaries, previews and statuses in the user's language. Optional `tree_ui` in state or graph overrides renderer interface labels for languages beyond the bundled English/Polish defaults. Provide full translations when using another language.

## Titles and previews that make sense on their own

Write natural, descriptive language in every layer, including experiment names. A reader should be able to picture the person, the specific information or product change, and the action without opening another node or knowing research terminology. For a test, also make clear what we will observe. A slightly longer title or several short preview sentences are preferable to compressed jargon; do not enforce a fixed naming formula.

Avoid bare abstractions such as "interpret evidence", "improve assessment", or "test the mechanism" when they hide what the person sees or does. Replace them with the actual project situation. Explain what "the material", "the explanation", or "the card" contains inside the same preview, including who prepares it when relevant. Name the real task the test examines; do not rename understanding information as verifying skills or rename intent as payment.

Before displaying the tree, read each changed title and preview without its neighbors or full-source document. Could the reader explain who receives what, what they do next, and what we will learn? Does it sound natural when spoken in the user's language? If not, clarify the canonical stage or specialist artifact first, then update state and the view without changing its meaning. Keep evidence, IDs, selection status, comparison, and measurement scope intact. Do not invent missing details or make the source link carry the basic explanation.

## Default layout and navigation

Use these accepted defaults when generating or refreshing the HTML tree, unless the user explicitly requests a different view:

- **Top to bottom:** use full-width horizontal bands in this order: Goal, Signals, Opportunities, Ideas, Tests/experiments. Add Observed results and Decision below only when they exist. Use the same order in HTML, Mermaid and any requested native Canvas or external board. Do not render empty future stages or hide an existing Signals layer.
- **One Signals band:** place every signal once in source order, independently of the opportunity branches. Do not create “Signals by opportunity” groups, repeat evidence cards, or move signals into a supporting appendix. All signal -> opportunity edges are visible on the initial view and remain visible after inspection closes. Show many-to-many signal -> opportunity relationships as actual connectors. Signals have no outgoing visual links to other layers.
- **Branch layout:** center each opportunity/idea over its descendant branch horizontally, allocating widths so cards cannot overlap. A shared idea/test is drawn once; its first incoming forward structural edge defines its layout parent, while every permitted tree relationship is drawn. Signal evidence does not determine ownership or grouping. Center the goal and the independent Signals row above the branches.
- **Stage colors:** use pale yellow for Goal, blue for Signals, green for Opportunities, purple for Ideas and orange for Tests/experiments, with slightly tinted bands and darker pastel cards. Keep SF typography and readable dark text. Selection uses a strong dark frame; recommendation uses a dashed frame; color identifies the stage, not approval.
- **Spacing at 100%:** cards are 280 px wide, horizontal sibling gaps are at least 36 px, and stage bands are 80 px apart. Measure actual card heights and reserve space for the tallest card in each band. Use orthogonal elbow connectors, not curves or diagonals. Connect forward adjacent stages from card bottom to card top, with horizontal runs in the gap between stage bands. Fan-out from one source shares one horizontal track; different sources use separate tracks so unrelated evidence does not merge into one bus. Route same-stage, backward and stage-skipping references outside the card rows so they do not run through intervening cards.
- **Zoom:** include minus/plus buttons, a 1-150% slider, reset to 100%, and fit-entire-tree. Start at 100%. Zoom the canvas and its connectors together; keep the detail panel at normal readable size. Preserve the viewed area when changing scale, and recompute canvas bounds and connector coordinates. Localize controls through English/Polish defaults or `tree_ui`.
- **Inspect connections:** clicking any card, including a signal, highlights its directly incoming and outgoing lines in blue (`#2563EB`) and brings them above other lines. Inspection never hides other evidence links. Keep this inspection while zooming; closing the panel or pressing Escape clears only the temporary highlight. Permanent selections and recommendations keep their frames and styling.

Apply layout and connection updates after cards or fonts change size. Keep the HTML offline and self-contained, with keyboard-operable native controls. Cosmetic view updates do not change node IDs, graph edges, review status, selections, or evidence. Do not create a new discovery decision merely because a card is inspected, zoomed, or repositioned.

When localizing through `tree_ui`, also supply `zoom_controls`, `zoom_out`, `zoom_in`, `zoom_scale`, `zoom_reset`, and `zoom_fit` for languages without bundled labels.

## Export and show

After saving a material change, increment `state.tree.revision`, set its current paths and use:

```sh
python3 <skill-directory>/scripts/render_tree.py <cycle>/state.json --output <cycle>/tree/tree.html --snapshot
```

The script validates and generates HTML plus sibling `tree.mmd`. With `--snapshot`, it writes `snapshots/rNNNN/` containing state, normalized graph, Mermaid and hash manifest. Existing different snapshots are never replaced; an identical retry is safe. Raw source files are not duplicated in every snapshot. If a view export fails, retain the state, name the stale view and retry without replaying decisions.

Open/refresh the HTML through the host's built-in visible browser, reusing the existing tab when supported. Report what changed (for example, new opportunities or a selected idea), current stage and next step. A saved file/editor open is not proof of successful preview. Respect browser policy; if blocked, give the local link plus an inline Mermaid or concise tree update. Do not use an alternate route to evade the restriction.

The tree starts with Goal, then the independent Signals band and its visible evidence links to Opportunities, then Ideas and Tests/experiments. Keep a strong frame on the selected path and a distinct recommended-test style. Clicking a node only inspects it. For requested PDF exports, follow `references/pdf-export.md`. The bundled `--pdf` export places the original full-card vector tree first, followed by compact stage tables with ID-based mappings, statuses and source links. It preserves the tree layout and simplifies only the accompanying documentation.

## Boundaries

Do not prefill later stages or simulate user/customer results. A source quote supports a rationale, not proof that a proposed solution works. Preserve provisional goals, pending synthesis reviews, unstarted experiments and missing results visibly. Board synchronization remains optional and capability-dependent.

For other interface languages, also localize the product-context and checkpoint labels from the bundled renderer UI through `tree_ui`.

When prioritizing opportunities with PRES, follow `references/opportunity-prioritization.md`. Keep scores and completeness in opportunity metadata, a compact summary and the linked scorecard, not a separate layer. A ranking or scorecard approval does not change selection frames without the actual human focus choice.
