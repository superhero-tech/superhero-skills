# Keep the user oriented and moving

Read at startup, on resume and after each specialist result. Supersprint owns the route through the cycle: a specialist finishing its analysis is a handback to the router, not the end of guidance.

## A concrete next move at every stopping point

Briefly locate the user: the current stage, what we have just learned or accepted, and the next decision. Recommend one concrete action and explain the decision-relevant reason. Offer two or three useful choices in total, with the recommendation first, when a real choice exists. Each choice says what happens next, what is needed and what it helps decide. Use ordinary product language rather than making users choose skill names. The router loads the relevant specialist after the choice.

End with one focused question about that decision, within the current human checkpoint. A missing product or outcome may need a single question rather than a fabricated menu. Do not end with only a report link, "let me know", "what next?", or a generic invitation to add anything. If the user has already chosen the action or explicitly delegated that choice, perform the authorized work instead of offering the same menu again. At a necessary wait, explain the exact user action needed to resume. At a draft review, also name the concrete action you recommend immediately after approval, with its expected output or the human task required. Recover/read the actual draft before recommending its approval; a saved waiting status alone is not a reason to recommend accepting an unread plan. Recommend the next work without defaulting to approval. For example, approving a test plan can lead to preparing its task scenario and observation sheet; "then we will determine the next steps" is not enough. Do not invent details absent from the plan or execute the test merely because a plan was reviewed.

Recommend a route without selecting a focus, approving findings or changing stages for the human. Reuse their current reply and existing reviews. Follow `references/human-checkpoints.md`; clear options can make that checkpoint easy to answer without adding a second navigation approval.

## After analysis: decide whether to deepen signals or proceed

Ask whether another method could materially change the next decision. The methods below are complements, not a fixed checklist or mandatory research sequence. Reuse current analyses; do not rerun them because their folders exist.

| What we have | Useful recommendation when that gap remains | Other sensible routes |
|---|---|---|
| Quantitative findings show where behavior changes but not why | Analyze available transcripts with `affinity-mapping`; without transcripts, use `interview-plan` to prepare real conversations about that behavior | Use `desk-research` for one relevant mechanism or external comparison, or accept the current synthesis and prepare Opportunities if the human considers their knowledge sufficient |
| Qualitative themes explain experiences but their extent or distribution is unclear | Use `data-analysis` on available behavioral data to examine the relevant segment or pattern | A targeted external evidence check, or proceed with unknown prevalence explicitly retained |
| Desk research describes market patterns or supplier claims without evidence from this product's users | Check the relevant behavior in available product data or prepare user research, whichever addresses the actual uncertainty | Another narrowly scoped source check only if it can change the choice, or proceed with applicability limits stated |
| Several methods already answer the working question well enough | Recommend synthesizing the signals and moving to candidate Opportunities plus PRES | Resolve a named contradiction or missing segment if it could change the choice; do not prescribe another method merely for completeness |

After quantitative analysis, normally make the three routes explicit: qualitative work, targeted desk research, or proceeding to Opportunities with the knowledge already available. Recommend the one with the highest expected value for the actual gap. If there is no useful new research question or the human already has the missing context, recommend proceeding instead. Do not recommend unavailable transcripts as though they exist; distinguish analyzing existing material from preparing research that someone must conduct.

The human judges whether their knowledge is sufficient to move on. Explain what remains uncertain and the consequence of proceeding, then honor that choice. Their experience can be recorded as attributed human judgment; it does not turn into measured customer evidence. Missing research categories, unknown Reach or incomplete PRES scores do not create an endless research loop. Carry unknowns into the opportunity comparison; do not invent scores or causal claims to make it complete.

For example, after an onboarding analysis: "We can see that people stop at the file import, but the export does not tell us why. I recommend analyzing the support conversations already available. We can also check how comparable products explain import errors, or accept these findings and prepare candidate needs with PRES if you feel we know enough. Which route do you choose?" Adapt the question to the actual review state and the user's language.

## Keep direction through specialist work and detours

Before a handoff, tie the bounded task to the agreed goal and current decision: the question to answer, selected scope/inputs, what artifact returns, and where the cycle resumes. Do not turn a question about one behavior into a general market report or implementation task.

After a handback, summarize what it answers and what it does not. Import the findings with their sources/status, update the synthesis and tree, then present the next recommended route and relevant alternatives. An analysis being complete does not automatically mean that Signals is accepted or that a cause is established.

Treat a new feature suggestion as a possible idea or a clue to a need, not an automatic selection or permission to abandon the current analysis. Answer a short relevant detour and return to the pending decision. If the user explicitly changes the goal or task, follow that instruction and record the changed route and affected earlier conclusions; do not force the old route.

## Moves between stages

| Current point | Suggested next decision |
|---|---|
| Product/outcome missing | Ask for that specific missing context; help frame a working goal after the answer |
| Goal draft ready | Review this goal, then choose the first decision-relevant signal source |
| Signal analysis ready | Decide between a complementary method, a targeted gap check or proceeding with stated uncertainty |
| Signal synthesis accepted | Prepare candidate user needs and a PRES comparison, reusing supplied input rather than asking the user to design the process |
| Opportunities compared with PRES | Recommend a focus with its evidence/limits; offer that focus, another candidate or a specific correction/research gap. Do not silently choose the highest total |
| Opportunity focus accepted | Invite existing ideas/constraints or explicit permission to draft approaches; then compare concrete mechanisms |
| Ideas reviewed | Recommend the assumption and practical test to prepare with `experiment-design`; retain alternatives and human selections |
| Experiment plan ready | Review or revise the plan, then identify the concrete preparation or real execution step and who must do it. Do not claim a planned test has produced results |
| Waiting for actual observations | Explain what needs to be observed/recorded; offer help preparing materials or a results note, or interpret supplied actual results |
| Results reviewed | Recommend develop, revise, discard or research further with reasons and a concrete next action; keep the decision with the human |
| Decision accepted | Close the cycle with an owner/action and, when appropriate, a scoped next cycle or implementation handoff |

PRES is the existing required opportunity comparison: read `references/opportunity-prioritization.md` and use `pres-prioritization`. Navigation must not replace it with an intuitive ranking, score ideas with PRES, or reopen an unchanged previously accepted focus merely because old state lacks a scorecard.

## Persist the route and resume it

Keep `next_action` as the immediate executable step or precise pending human choice. The optional `navigation` record in the state template stores:

- `decision_question`, `recommended_id` and `options`: the offered choices. Each option has a stable `id`, a self-contained `label`, its `reason` and `needs`; include the specialist `skill` and `target_stage` when useful.
- `selected_id` and `selection_source_refs`: the actual human choice, not the agent recommendation.
- `return_to`: the stage and pending decision to resume after the chosen research or detour.

`current_stage` and `human_gates` remain authoritative for stage/review status. A recommendation or research-method choice does not approve a draft. When replacing obsolete options, retain material choices and reasons in history; do not let stale recommendations overwrite accepted choices. On resume, recover the current question, actual selection and return point; do not restart the cycle or completed analyses. Older states can acquire navigation when a real choice is offered, without a forced migration or invented past choices.
