---
name: production-readiness
description: Guide technical and nontechnical users through preparing a local web app or API for production. Audit evidence, maintain one offline HTML checklist with a preparation rating and separate blockers, and implement agreed local fixes.
---

# Production readiness

Help the user prepare an application for release, step by step. The durable result is one Polish, offline `docs/production-readiness.html` with embedded state, evidence and history. Default to the user's language in conversation; use Polish in the report unless requested otherwise. This initial skill requires validation on real product work; do not describe its output as a security certification.

Requires local repository access and Python 3.9 or later. The HTML works offline; JavaScript only enables filters.

## Guide a person, not an operator

- Assume the user may not know Git, hosting, rollback or databases. Explain the consequence in everyday language before the technical term. Put technical evidence behind details.
- Inspect what you can yourself. Ask only for missing decisions or facts you cannot obtain. Ask a small, concrete question, recommend an answer and explain the tradeoff. Never ask the user to run an unexplained terminal command.
- At each checkpoint say what is already done, what prevents release and the one next step. Distinguish work the agent can do from a decision or action for the person. Give numbered, provider-specific instructions when external action is needed; verify current provider documentation before giving navigation steps.
- Organize the HTML into six categories, not a wall of security jargon. Each item explains why it matters, what was found, how to check it and what to do next.

## Establish context and resume

Read project instructions, inspect the working tree and look for the existing report before changing files. Preserve unrelated work; do not commit, push, install tools or deploy merely because a source workflow does so.

Resolve `SKILL_DIR` to this installed skill directory and `PROJECT_DIR` to the target repository. Read [the state contract and commands](references/state.md). Use `init` for a new report or `refresh` to begin a new audit in an existing one. The renderer never runs project commands. Keep temporary JSON outside the repo; the HTML is the only durable checklist file.

Infer stack, user journeys, authentication, persistence, integrations and delivery mechanism. Confirm only missing context: intended hosting/environment, audience, sensitive data and consequences of an outage. Record unknowns explicitly. Read [audit guidance](references/audit.md) and `assets/checklist.json`. Do not claim coverage is complete while scope or applicability remains unknown.

## Audit and evidence

1. Evaluate every baseline item. Keep stable IDs. Explain exclusions; never silently remove or weaken a baseline requirement. Add app-specific checks with a rationale and a verification method. Keep recommendations separate from mandatory requirements.
2. Inspect scripts and their configuration before executing tests, builds or scans. Names like `test` do not make a command safe. Run understood local checks within the user's scope. Separately agree operations that mutate external data, cost money or touch production. Do not expose secrets or upload the repo to external scanners.
3. Record observations, not assumptions. Evidence includes a timestamp, this audit's ID, source, result and either the inspected `file:line` / executed command or a named human's concrete confirmation. Describe exit status and relevant result without storing sensitive output. A lockfile does not prove dependencies are safe; backup configuration does not prove recovery works; a successful build does not prove the main user journey works.
4. Use `pass` only with current evidence of the entire requirement. Use `fail` for an observed defect and `unverified` for missing evidence/access. On resumption re-run automated checks and assess human evidence again; do not relabel an old confirmation as freshly obtained. Leave unrechecked results `stale`.
5. Record accepted risk separately with who, when and why. It never changes a failing/unknown requirement to `pass`, excludes it from the denominator or authorizes deployment. A human may still decide to release, but that decision is not a passing checklist.

Render the first audit before proposing fixes. Mark `phase: complete` when the agreed audit work has ended, even if the application is not ready. Keep `scope_confirmed: false` if context remains missing. The renderer calculates the rating and verdict; never supply a hand-picked score.

## Agree and complete a repair package

Present a short plain-language package: affected items, intended behavior, local edits, checks and decisions needed. Obtain approval for the package unless the current conversation already explicitly authorizes that concrete scope. Then execute it without asking about each edit. Preserve unrelated changes.

Stop for a new decision when a repair would expand scope, choose a paid service, change authentication policy or affect external/production state. Do not deploy. Do not treat retries, migrations or idempotency changes as mechanically safe fixes.

After repairs, begin a fresh audit using `refresh`, repeat relevant checks and revalidate other requirements before marking them current. Save actual results. If blocked by access or a human task, finish authorized independent work, leave the remaining blocker with an owner and actionable steps, and save the report. Never spin until everything is green.

## Review and hand off

Use the renderer to save atomically and retain previous revisions. Inspect the HTML in an available browser: summary, next action, category navigation, filters, expanded evidence, mobile width and print layout. If browser preview is unavailable, report that limitation. Do not confuse technical validation with the user's visual acceptance.

Return the HTML link, preparation percentage with numerator/denominator, release blockers and the next step. Explain that 100% means the applicable mandatory checklist requirements are evidenced for the recorded version/environment; it is not a probability of safe operation. Recommendations do not inflate or reduce that score. A completed audit can still report "not ready".

For provenance and reuse boundaries, see [sources](references/sources.md). No other skill or plugin is required to run this workflow.
