# Human checkpoints and product context

Read at startup and before entering or resuming a stage. The default is an interactive cycle with two distinct checkpoints at every stage. Starting the full process is not permission to answer either checkpoint for the user.

## Startup: identify the product and ask about the outcome

1. Read the conversation and relevant saved context. If the product and what it does are missing or ambiguous, ask which product/service we are working on, for whom, and what it helps them do. Ask this as one focused context question, then wait. Do not infer a product from a folder name, unrelated files or a previous project's example.
2. Save the user's product name in `state.product`, the short description and audience in `state.product_context`, and the source of those statements. If the supplied brief already establishes this context, reuse it and ask only about material gaps. Do not make the user repeat established information.
3. If there is no agreed outcome, ask what change they want to achieve for this product, then wait. Do not substitute a model-generated goal and proceed to analysis. "I do not know yet" is a valid answer: record it, help draft a working goal in the goal stage, and request review. Missing baseline, target or deadline does not prevent drafting that working goal. A current message that already answers this question satisfies this input checkpoint.
4. Set `intake.product_confirmed` only from the user's statement or an identified supplied source, and store `intake.outcome_response` plus `source_refs`. Neither field means the goal draft has been approved.

## Keep the product on the Canvas

As soon as the product is identified, save `context/product.md` inside the cycle with the product name, what it does, intended users, business context if supplied, the user's outcome or an explicit unknown, sources and review status. Link it from the cycle entry point and state. Update it after accepted context or goal changes, preserving the difference between human statements and agent proposals.

Keep a prominent Product and outcome block above the HTML tree, including when no goal or branches exist yet. Derive the displayed outcome from the actual goal node(s); if absent, say it is not defined. Never invent a goal node just to fill the Canvas. The renderer includes this context in its saved projection and Mermaid comments.

When the host exposes a writable native Canvas and it is the intended working surface, create or update the same product-context section there using its supported capability. Save its identity in `product_context.canvas` and preserve unrelated user content. A Miro/FigJam target is used only when selected by the user. If no writable Canvas is available, show the context in the HTML tree and provide `context/product.md`; explain this fallback without claiming a native Canvas was updated. Do not make this depend on a personal vault or a specific vendor's tool name.

## The loop at every stage

**Input -> agent draft -> human review -> next stage.** The stages are `goal`, `signals`, `opportunities`, `ideas`, `experiments`, `results`, `decision`.

1. **Ask for input and stop.** Briefly state the stage's purpose and what is already known. Ask what the human wants to add or change: materials, observations, constraints or a hypothesis relevant to this stage. Make clear that "nothing else; prepare a proposal" is a valid response. Save `awaiting_input` and wait. Existing files do not answer this question automatically. If the current user message explicitly supplies the requested stage input, record it without asking the same question again.
2. **Prepare the stage after the reply.** Record the actual response/source and set `drafting`. Incorporate it, run the relevant specialist within this stage, and fill gaps using available evidence. Mark unknowns and agent-proposed interpretations. Do not invent customer observations, results or human choices. A missing input may require further research or a provisional proposal rather than fabricated completeness.
3. **Show the draft and stop for review.** Save the stage artifact, its revision and proposed nodes. Refresh the tree/Canvas, highlight the meaningful change and ask the human to approve or correct the current stage. Set `awaiting_review`; keep `current_stage` unchanged. Rendering, opening a source, silence, elapsed time or answering the earlier input question is not approval.
4. **Apply the review.** On corrections, record the feedback, return to `drafting`, revise the artifact, increment its revision and request review again. On explicit approval of the displayed revision, save the user's response/source, set `accepted`, then enter the next stage as `awaiting_input`. Ask that next stage's input question and wait before doing its work. One message may approve the current draft and provide next-stage input only when it explicitly does both.

| Stage | Useful input to invite | What the human reviews |
|---|---|---|
| Goal | Product priority, desired behavior/outcome, constraints | Working goal, measurement meaning and unknowns |
| Signals | Files, observations, questions, gaps in coverage | Findings, limits and whether evidence is sufficient to continue |
| Opportunities | Needs noticed by the human or missing from the synthesis | Candidate needs, the PRES scorecard and the selected focus |
| Ideas | Existing approaches, constraints and ideas | Concrete mechanisms and which ideas to explore |
| Experiments | Main uncertainty, participant access, practical constraints | Hypotheses, methods, observable changes and next test |
| Results | Actual observations and execution details | Interpretation and limitations; missing results stay missing |
| Decision | Human interpretation, business constraints and preferences | Develop, revise, discard or research further, and the next action |

Specialist checkpoints can satisfy the corresponding stage review when they cover the same artifact and revision; do not duplicate the same approval. Ask one consequential question at a time. Previously accepted unchanged work does not need to pass its checkpoints again.

## Persist and resume the actual checkpoint

Use `human_gates.stages[stage]` from `assets/state-template.json`:

- `status`: `not_started`, `awaiting_input`, `drafting`, `awaiting_review`, `accepted`.
- `input`: `response` and `source_refs` for the human input or explicit permission to draft with no extra input.
- `draft`: positive integer `revision` and cycle-relative `artifact_path`.
- `review`: `decision` (`approved` or `revise`), `response`, `source_refs`, and `reviewed_revision` matching the displayed draft when approved.

The renderer checks these records before writing a view: a later stage cannot precede acceptance of earlier ones, and an accepted review cannot refer to another draft revision. This validates stored consistency, not the authenticity of a human response; never manufacture that provenance. Keep `pending_reviews`, stage status and the narrative consistent.

On resume, `awaiting_input` repeats or clarifies the pending input question; `drafting` continues only that stage; `awaiting_review` shows the saved draft and asks for review; `accepted` enters the next stage. On older states, preserve actual accepted decisions and their evidence, initialize missing checkpoint records conservatively, and ask only at the first unresolved checkpoint. Do not mark historical acceptance without a supporting user decision.

Only an explicit user instruction to skip named checkpoints changes this default. Record its scope, actual response/source and a stable ID in `human_gates.delegations`; a delegated stage review uses `decision: delegated` plus `delegation_id`, not a fabricated human approval. A general request to start or continue, a short reply, or access to files does not waive checkpoints. If the user restores human review, stop at the next applicable checkpoint.
