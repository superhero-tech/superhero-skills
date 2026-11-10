---
name: production-readiness
description: Guide users through preparing a web app or API for production, verifying its deployment and observing real use. Create an offline HTML checklist with separate stage ratings, environment-specific evidence and blockers, and implement agreed local fixes.
---

# Production readiness

Help the user prepare an application for release, step by step. The durable result is one Polish, offline `docs/production-readiness.html` with embedded state, evidence and history. Default to the user's language in conversation; use Polish in the report unless requested otherwise. Do not describe its output as a security certification.

Requires local repository access and Python 3.9 or later. The HTML works offline, including its embedded Geist Sans font; JavaScript only enables filters.

## Guide two practical runs

The normal journey is: run on dev to find and fix problems before deploying; after deployment, run again with the production URL to verify the remaining requirements. Explain it in those words. Real-use observation is a later follow-up, not a third dashboard competing for attention.

## Separate environments from release stages

- Environments are concrete local/dev, preview, staging or production instances. Preview/staging is optional; do not require an extra hosted environment for every small application. An isolated restore or migration trial still needs a suitable safe place.
- Assess three stages separately: `preparation` before deployment, `deployment` verification of the target deployment (which can happen before admitting users), and `observation` of real use after release. A production instance can exist without serving users yet. Never average these stage ratings or call local success production verification.
- Evaluate the baseline for every stage, but prioritize checks that can be performed now. Future checks remain open in their own stage, labeled as waiting for deployment or real use; they do not reduce preparation progress. Missing access to an existing production instance is an unverified requirement, not an excuse to defer or exclude it.
- Split a broad requirement when it needs independent evidence: local main journey and production smoke, prepared logging and deployed logging/alerts, restore rehearsal and coverage of the actual production store. Do not duplicate the entire checklist across environments. Add app-specific production or observation checks where configuration or real use changes the evidence needed.
- Bind evidence to the assessed source version, stage and exact environment, deployment and configuration revision. A changed address, version or configuration requires reassessment; keep prior results in history. Do not invent configuration IDs or relabel old evidence.

## Guide a person, not an operator

- Assume the user may not know Git, hosting, rollback or databases. Explain the consequence in everyday language before the technical term. Put technical evidence behind details.
- Inspect what you can yourself. Ask only for missing decisions or facts you cannot obtain. Ask a small, concrete question, recommend an answer and explain the tradeoff. Never ask the user to run an unexplained terminal command.
- At each checkpoint say what is already done, what prevents release and the one next step. Distinguish work the agent can do from a decision or action for the person. Give numbered, provider-specific instructions when external action is needed; verify current provider documentation before giving navigation steps.
- Organize the HTML into six categories. Keep each check collapsed by default, showing only status and title. Do not list every possible environment under each title. Show the actual selected place of inspection after expanding the check, and keep allowed environment kinds and precise identity in technical details. Expand it to reveal why it matters, what was found, how to check it and what to do next; technical evidence can remain in a nested disclosure.
- Keep the top focused: a plain-language explanation of what is being checked now, one current result, one next-action line and category links for the current checklist. On dev show preparation checks; put deployment checks in a collapsed "Po wdrożeniu" section and real-use checks in a later disclosure. After deployment show deployment checks, retain prior preparation results in a separate disclosure, and make unresolved prerequisites visible. Keep scope, evidence and rating explanations behind details. Never show three competing scores or environment/stage filter controls in the main workflow.

## Establish context and resume

Read project instructions, inspect the working tree and look for the existing report before changing files. Preserve unrelated work; do not commit, push, install tools or deploy merely because a source workflow does so.

Resolve `SKILL_DIR` to this installed skill directory and `PROJECT_DIR` to the target repository. Read [the state contract and commands](references/state.md). This version applies to new schema-2 reports only. Do not migrate, rewrite or update legacy reports. If a legacy report occupies the default path, retain it and initialize a new report at a distinct explicit `--output`. For schema-2 reports, read the current state before choosing how to resume. When continuing the same assessed source version after deployment, verify source/configuration identities and continue that audit with the production environment and `target_stage: deployment`; preserve valid preparation evidence with its original timestamps. Do not reset all preparation work merely because the user moved to the next stage. Use `refresh` for a new assessment, changed sources/configuration or evidence that needs reassessment; recheck stale requirements. The renderer never runs project commands. Keep temporary JSON outside the repo; the HTML is the only durable checklist file.

Infer stack, user journeys, authentication, persistence, integrations, delivery mechanism, available environments and whether the assessed version is deployed or serving real users. Establish the current assessment stage, source identity and safe non-secret environment/configuration identifiers. Confirm only missing decisions or inaccessible context: hosting, audience, sensitive data and consequences of an outage. Record unknowns explicitly. Read [audit guidance](references/audit.md) and `assets/checklist.json`. Do not claim coverage is complete while relevant scope or applicability remains unknown.

## Audit and evidence

1. Evaluate every baseline item. Keep stable IDs. Explain exclusions; never silently remove or weaken a baseline requirement. Add app-specific checks with a rationale and a verification method. Keep recommendations separate from mandatory requirements.
2. Inspect scripts and their configuration before executing tests, builds or scans. Names like `test` do not make a command safe. Run understood local checks within the user's scope. Separately agree operations that mutate external data, cost money or touch production. Do not expose secrets or upload the repo to external scanners.
3. Record observations, not assumptions. Evidence includes a timestamp, this audit's ID, stage, assessed source version, an exact snapshot of the inspected environment identity/configuration, source, result and either the inspected `file:line` / executed command or a named human's concrete confirmation. Verify that a deployment actually corresponds to the assessed sources before binding it. Describe exit status and relevant result without storing sensitive output. A lockfile does not prove dependencies are safe; backup configuration does not prove recovery works; a successful build does not prove the main user journey works.
4. Use `pass` only with current evidence of the entire requirement. Use `fail` for an observed defect and `unverified` for missing evidence/access. On a new assessment re-run automated checks and assess human evidence again; do not relabel an old confirmation as freshly obtained. Leave unrechecked results `stale`.
5. Record accepted risk separately with who, when and why. It never changes a failing/unknown requirement to `pass`, excludes it from the denominator or authorizes deployment. A human may still decide to release, but that decision is not a passing checklist.

Render the first audit before proposing fixes. Mark `phase: complete` when the agreed audit work has ended, even if the application is not ready. Keep `scope_confirmed: false` if context remains missing. The renderer calculates the rating and verdict; never supply a hand-picked score.

## Agree and complete a repair package

Present a short plain-language package: affected items, intended behavior, local edits, checks and decisions needed. Obtain approval for the package unless the current conversation already explicitly authorizes that concrete scope. Then execute it without asking about each edit. Preserve unrelated changes.

Stop for a new decision when a repair would expand scope, choose a paid service, change authentication policy or affect external/production state. Do not deploy. Do not treat retries, migrations or idempotency changes as mechanically safe fixes.

After repairs, begin a fresh audit using `refresh`, repeat relevant checks and revalidate other requirements before marking them current. Save actual results. If blocked by access or a human task, finish authorized independent work, leave the remaining blocker with an owner and actionable steps, and save the report. Never spin until everything is green.

## Review and hand off

Keep only completed audit results in history. Working saves remain the current report; do not archive them as audit outcomes. The renderer keeps the latest completed result per audit ID and stage, without duplicating the current result. Use the renderer to clean existing schema-2 history; do not hand-edit snapshots or start a new audit just to tidy history.

Use the renderer to save atomically and retain previous completed audit results. Inspect the HTML in an available browser: summary, current-only checklist, collapsed later checks, prior unresolved requirements, next-action navigation, filters, expanded evidence, mobile width and print layout. If browser preview is unavailable, report that limitation. Do not confuse technical validation with the user's visual acceptance.

Return the HTML link, the current percentage with numerator/denominator, what needs fixing or checking now and the next step. Briefly explain what remains for after deployment; keep other stage results secondary. A completed preparation stage means ready to deploy, not that deployment or operation has been verified. Explain that 100% means the applicable mandatory requirements of that stage are evidenced for the recorded version/environment; it is not a probability of safe operation. Recommendations do not inflate or reduce scores. A completed audit can still report "not ready".

For provenance and reuse boundaries, see [sources](references/sources.md). No other skill or plugin is required to run this workflow.
