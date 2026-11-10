# Audit guidance

Start from a real user journey and its failure consequences. Read implementation, tests, project scripts, deployment configuration and operational documentation. Distinguish current implementation from proposed behavior. A local inspection cannot establish production settings or a real restore outcome.

## Establish when and where a check is possible

Guide the user through a dev run before deployment, then a production run after deployment. Record the assessed source version, target stage and release state before interpreting results. Identify concrete environments, not just labels such as "dev" or "prod": exact resource/address, observed deployment/build and non-secret configuration revision. Confirm which source version actually backs a deployed artifact. Do not mark a version deployed merely because an older production release exists.

Prepare locally or on dev/preview/staging as appropriate; no permanent staging environment is mandatory. Rehearsals must still be isolated and representative. A restore trial can run in a disposable local database, but evidence must establish what production data/configuration it represents. A production backup check separately confirms the actual store is covered.

Before admitting users, inspect the target deployment: TLS/cookies, actual service configuration, access boundaries, a completed smoke test, logs, delivered alerts and backup coverage. Follow the existing authorization boundary for live operations. A prepared smoke plan and installed monitoring library are preparation evidence only; neither proves the deployed integration works. A test payment is not proof that live credentials/webhook configuration are correct; inspect those separately without charging anyone.

After real use begins, agree meaningful observation criteria and a sufficient window/sample for this app. Inspect journey success/failures, relevant availability, resource use and actual costs. Consider reporting delays. Low/no traffic is not proof of adequate capacity. Do not invent a universal observation duration, success threshold or traffic target. Add domain-specific checks when needed; the two baseline observation items do not constitute complete coverage for every app.

Present the current checklist first, with one score and a concrete next step. Put future checks in collapsed later-stage sections, rather than mixing waiting production rows into the dev checklist. Keep future checks in their own stage as waiting. Missing permission or access to an existing deployment is an unresolved verification task. Do not turn it into "not applicable" or an observed failure. Expose the actual next action: register the environment, obtain a non-sensitive confirmation, perform an authorized safe check, or wait for an agreed real-use sample.

## Apply the baseline

`assets/checklist.json` contains the maintained baseline. Conditions are questions for the agent to resolve, not expressions evaluated by the renderer. Unknown applicability stays in its stage's required denominator and blocks a successful verdict for that stage. Later unknown applicability does not block completion of preparation. For each exclusion, record why the condition is false in this application. Do not use exclusion to hide lack of access, failed checks or accepted risk.

Use the same six categories for additional checks. Assign `required: true` when failure could prevent an acceptable release in the agreed context; explain the rationale. Add `required: false` improvements separately. Do not invent universal performance, coverage or availability thresholds. Agree measurable expectations from actual audience, costs and consequences. Escalate specialist questions when the agent cannot establish the answer, without claiming a compliance audit.

## Areas to investigate

- Access: anonymous and signed-in entry points, server-side authorization on each sensitive operation, cross-account object access, admin routes, session expiry and login abuse. A hidden button is not authorization.
- Data: trace inputs through storage, logs, exports and external services. Check validation, injection protections appropriate to the stack, access to secrets and key rotation after exposure. Examine necessary data collection, retention/deletion, and real restore evidence for persistent valuable data. Do not embed real personal data in the report.
- Behavior: test an important journey, rejection/error paths and the production build configuration. Inspect dependency findings for actual impact. For payments/webhooks, check signatures, repeat delivery, retries and partial failures. For concurrent writes, examine transaction boundaries and conflicting updates. For file upload or URL fetching, inspect relevant size/type/access and network boundaries.
- Delivery: understand how the known version is built and configured, how changes to stored data are migrated, how a previous working version is restored, and how the release is checked. A source rollback is not a database rollback. Keep secrets out of bundles and preview/staging data separate from production.
- Reliability: external calls need bounded wait/retry behavior appropriate to the journey. Inspect timeouts, total retry budgets and effects of repeated side effects. Investigate expected load/resource limits based on realistic usage rather than an arbitrary benchmark.
- Operations: a real recipient for alerts, visible failures without sensitive logs, a health signal that represents useful service, an owner and understandable recovery steps. A contact name alone does not establish monitoring or response.

## Evidence and human steps

Read only relevant evidence, and cite precise sources with the actual result. An agent evidence source can be `src/auth.ts:42` or an inspected command with its result; it must not imply execution when only code was read. Every record includes the stage, assessed source version and exact environment/configuration snapshot from the state contract. A human confirmation should name the person and describe the actual action, date, environment and outcome. "We have backups" is insufficient evidence for restore.

When a required check cannot be performed, give the person a short procedure tailored to their provider. Example: explain that the aim is to restore a copy into a separate test environment; identify where to start using current documentation, tell them what successful recovery looks like and what non-sensitive result to report. Do not suggest overwriting production to test a backup. Ask for text confirmation or a redacted result, never credentials.

Test/build commands can contain database resets, deployment hooks or network calls. Read the script chain, configuration and target environment before running them. If a check would touch live systems, save it as an external next step and separately agree the action. Lack of permission is a reason for `unverified`, not `pass` or `not applicable`.

## Rating and trust

All applicable mandatory requirements have equal weight within their stage. Each percentage measures progress, not risk reduction: one severe gap may remain at 95%. Show the raw fraction and unresolved/waiting counts next to it. Category ratings concern the selected assessment stage. Never combine the three stage scores. Adding newly discovered requirements or restoring stale checks can decrease the score; explain that change using the retained history. Never hide a new issue to maintain a rising score.

Do not offer a successful stage verdict while the audit is in progress, scope is unconfirmed, relevant applicability is unknown or mandatory requirements of this or a prerequisite stage lack current passing evidence. Completed preparation can coexist with deployment checks still waiting. Recommended improvements can remain open. A reported result is a snapshot, not a continuously monitored promise.
