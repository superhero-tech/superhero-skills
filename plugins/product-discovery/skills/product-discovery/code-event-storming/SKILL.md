---
name: code-event-storming
description: Reconstruct an EventStorming board from business behavior evidenced in an existing codebase. Use to map current processes, commands, domain events, read models, and open questions in a self-contained HTML board.
compatibility: Requires access to the analyzed project and Python 3.9 or later. The HTML board opens in a browser with JavaScript enabled and works offline.
---

# EventStorming from code

Reconstruct a snapshot of the current implementation for people to review together. Analyze the entire project unless the user specifies a process. Write `docs/event-storming.json` and `docs/event-storming.html` by default. For a custom HTML path inside the project, save the JSON next to it with the same basename. Keep any proposed changes separate from the observed behavior.

## Discover the process

- Read the project instructions and inspect the current working tree, including uncommitted code. Leave application code and data untouched.
- Find entry points, business decisions, permissions, transaction boundaries, database constraints, side effects, and reads. Compare these with tests, scenarios, and documentation. Use implementation as evidence of current behavior and record disagreements between sources as questions.
- Cite actual `file:line` evidence for every card, rule, and command outcome. Use only the source lines needed to explain the behavior. The renderer embeds excerpts in the board, so exclude secrets and personal data.

## Model the behavior

- Order events from left to right. Follow the business story across entry points: an event makes information available, an actor uses it to decide, and a command produces the next event. Use process lanes to organize the view and label proposed aggregate or context boundaries as hypotheses.
- **DOMAIN EVENT** is a business fact in the past tense. A modeled event can be implicit in the implementation. Record an unsuccessful operation as an event only if the outcome itself matters to the business.
- **COMMAND** is an intent to change state. Use the imperative. Put business conditions in `rules` and refusals or safe retries in `outcomes`, each with its own evidence. Explain HTTP, SQL, validation order, and transactions in the details.
- **READ MODEL** is information used to make a decision, such as stock availability or an order history. Show which **ACTOR** uses the information and what command they can issue. Label the actor by role. Name the information itself, such as “Stock availability”.
- **POLICY** is an evidenced business reaction linking an event to a command or action. It can be manual or automatic, and synchronous or asynchronous. For example, “Order confirmed” can trigger “Notify the buyer”, leading to “Record confirmation in the outbox”. Explain the implementation and any shared transaction in the details. Put validation and permission checks that precede a command in its rules.
- **HOT SPOT** is an open question, a missing rule, or conflicting evidence. Place it beside the relevant card and connect it with an `annotation` edge. Distinguish observed gaps from suggestions.
- Mark each connection as `flow` for cause or reaction, `information` for information becoming available or informing a decision, or `annotation` for a hot spot. Use **AGGREGATE** and **EXTERNAL SYSTEM** only where the code supports those roles.
- Write titles, details, and questions in the language of the conversation. Keep the English type labels and preserve source excerpts verbatim.

## Render and review

Read the [model specification](references/model.md) and prepare the JSON yourself from the evidence. The renderer validates and draws the model. It does not infer rules from source files.

Resolve `SKILL_DIR` to the absolute directory containing this installed `SKILL.md` and `PROJECT_DIR` to the analyzed project root. With those variables set, run:

```sh
python3 "$SKILL_DIR/scripts/render.py" docs/event-storming.json --repo "$PROJECT_DIR" --output docs/event-storming.html
```

If Python is unavailable, save the model and report that the HTML could not be rendered. When a browser is available, inspect readability, branching, zoom, pan, the process picker, the **Fit entire board** button, and keyboard access to the source panel. Report when preview is unavailable. To revise the board, edit the model and render again.

Return links to the saved files and the main questions for domain experts. Present the board as a snapshot for review.
