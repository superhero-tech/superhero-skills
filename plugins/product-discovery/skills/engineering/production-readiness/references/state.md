# State and commands

The HTML is the single durable artifact. `checklist.py` embeds JSON in `script#readiness-data`, escapes untrusted content, calculates stage ratings and keeps previous completed audit snapshots. The renderer validates records; the agent owns the factual assessment. It never runs application commands or checks an external environment automatically.

Resolve `SKILL_DIR` and `PROJECT_DIR` to absolute paths. Python 3.9+ and its standard library suffice. Default output is `docs/production-readiness.html`; a custom `--output` must also stay inside the project.

## New reports only

This version initializes schema 2 with baseline template 2. There is no migration and no rewriting of legacy reports. If the default path contains an older report, leave its bytes and history untouched. Initialize a separate report, for example `--output docs/production-readiness-v2.html`, and use that output on every subsequent command. The CLI rejects unsupported schemas before writing. Old offline HTML remains independently readable.

```sh
# Never overwrites an existing file.
python3 "$SKILL_DIR/scripts/checklist.py" init --repo "$PROJECT_DIR"

# Start a new assessment in schema 2: new audit ID, previous passes stale.
# To continue an unchanged version after deployment, extract/render instead; see below.
python3 "$SKILL_DIR/scripts/checklist.py" refresh --repo "$PROJECT_DIR"

CHECKLIST_WORK=$(mktemp -t production-readiness.XXXXXX)
python3 "$SKILL_DIR/scripts/checklist.py" extract --repo "$PROJECT_DIR" > "$CHECKLIST_WORK"
# Edit the extracted JSON using file tools, then render actual findings.
python3 "$SKILL_DIR/scripts/checklist.py" render --repo "$PROJECT_DIR" --input "$CHECKLIST_WORK"
rm "$CHECKLIST_WORK"

python3 "$SKILL_DIR/scripts/checklist.py" validate --repo "$PROJECT_DIR"
```

An untouched extraction is not an audit. Do not hand-edit generated HTML or history. Do not install dependencies silently.

## Stages and environments

These are independent axes. Every item has one stage, allowed environment kinds and a selected concrete environment ID. Separate items represent independently verifiable parts of a broader requirement; do not duplicate all items in all environments.

| Stage | Meaning | Examples |
| --- | --- | --- |
| `preparation` | Evidence needed to prepare this version for deployment | Source checks, build/start, main journey on safe data, restore/migration rehearsal, release and rollback plans |
| `deployment` | Evidence from the actual target deployment, possibly before opening it to users | HTTPS, actual configuration, production smoke, access, logs, delivered alert, actual backup coverage |
| `observation` | Evidence from real use after admission of users | Error/success signals, actual resource consumption and costs, app-specific operational checks |

`context.target_stage` selects the current assessment. It controls the main summary, category progress, current checklist and next action. Other stages remain in collapsed disclosures, with earlier unresolved prerequisites expanded. This does not delete or exclude requirements or alter scores. The UI has one prominent result; users are guided through a dev run and a later production run, with real-use observation as follow-up.

`context.release_state` is `not_deployed`, `deployed` (the assessed version exists at its target address, before admission) or `live` (serving real users, including internal users). Establish this for the assessed version, not an unrelated older production release. Registration of a new target environment or movement to a later stage can remain in the same audit if sources and earlier assessed configurations have not changed. Changing the target stage alone does not invalidate evidence. Reopen `audit.phase: in_progress` under the same ID while performing the next part, then complete it when that agreed work ends. Preserve original timestamps and identities of unchanged preparation evidence; never relabel it as freshly executed.

Before deployment, deployment checks are waiting. Before real use, observation checks are waiting. A preparation check can wait for a selected, unavailable test environment. Waiting is a derived presentation, not a stored `pass`, `fail` or exclusion. Lack of access to an existing production deployment stays `unverified` and actionable. A known failure stays visible even if execution is currently waiting.

`environments` is a nonempty list. Each instance has:

- `id`: unique stable identifier, such as `local`, `preview-pr-42`, `production-eu`.
- `kind`: `local`, `development`, `preview`, `staging` or `production`.
- `name`, `address`: meaningful name and exact inspected URL or local resource path. Do not include tokens or credentials in URLs.
- `version`: observed build/deployment ID or local source fingerprint.
- `source_version`: identity of the assessed sources proven to correspond to that build/deployment.
- `config_revision`: actual non-secret configuration revision, inspected configuration fingerprint or immutable configuration reference. Do not use a made-up value like "current". Never store secret values or hashes of individual secrets. The agent must inspect relevant ignored/local settings and external configuration as well as tracked code.
- `available`: boolean indicating access for the authorized inspection. Lack of access never makes a requirement not applicable.

New reports register only the local repository, with the known source identity and an empty config revision awaiting inspection. Add other environments only when they exist or are meaningfully planned; missing optional preview/staging is not a blocker. Restore or migration trials still need an isolated safe resource; a temporary local instance can suffice when representative. A production-only baseline item cannot be assigned to staging.

## Editing contract

- Preserve `schema_version`, `template_version`, `revision` and `_base_digest` from extraction. `_base_digest` prevents overwriting a concurrently changed report and is not stored in the HTML.
- `audit`: preserve `id` and `started_at` within one assessment; set `phase: complete` after the agreed assessment, even if checks remain open or later stages are waiting. Use `refresh` for a new audit, especially after code/configuration changes. Never relabel an old record with the new audit ID.
- `project`: generated name, commit, dirty flag and content fingerprint of Git-listed files, excluding this report. Do not invent a commit for a non-Git repository. The CLI rejects rendering if the working tree no longer matches. Ignored files, submodules and external settings require direct inspection.
- `context`: nonempty plain-language `hosting`, `audience`, `data`, `outage_impact`; `scope_confirmed` becomes true only when those are established. Also set `target_stage`, `release_state` and `source_version`. For Git the source identity must equal the generated content fingerprint (commit fallback). Without Git, establish a concrete source version/fingerprint yourself before passing anything; the renderer cannot detect filesystem drift there.
- `items`: preserve all baseline and existing custom IDs. Baseline stage and allowed environment kinds are fixed. Mandatory criteria cannot be weakened. Add app-specific requirements with a new stable lowercase-hyphen ID, `origin: custom`, a category from the baseline and a rationale.
- Each item has `title`, `why`, `condition`, `verification`, nonempty `steps`, `rationale`, `category`, `required` (boolean), `priority` (`high` or `normal`), `origin`, `stage`, `environment_kinds` (nonempty list of allowed kinds), and `environment_id` (selected instance ID or null). Explain checks for this app without weakening them. Priority affects next-action ordering, not score weight.
- `applicability`: `yes`, `no`, `unknown`. `no` needs `applicability_reason`; unconditional baseline requirements cannot be excluded. Unknown remains in its stage denominator and prevents a completed verdict for that stage.
- `status`: `pass`, `fail`, `unverified`, `stale`. `finding` is the concrete observation in everyday language. `owner` is `agent` or `human`, indicating who can take the next step; tailor `steps` accordingly. Missing evidence/access is unverified, not an observed defect.
- `evidence`: records with `kind` (`agent` or `human`), `source`, `result`, timezone-aware `checked_at`, `audit_id`, `stage`, `source_version` and an `environment` snapshot containing all fields listed above. Human evidence also needs `person`. Copy identity fields only after actually verifying them; a matching JSON identity does not prove the underlying test happened.
- A pass requires applicable=yes, current-audit evidence for the item's stage, an available allowed environment with all identity fields established, and exact matching source/environment/configuration snapshots. The environment's `source_version` must match the assessed source version. A future waiting check cannot pass. Every attached record must be current; retain older evidence in historical snapshots instead.
- Changed sources, environment address, build or configuration invalidate affected passes. Use `refresh`, which stales all passes conservatively, and recheck. Local source metadata updates on refresh; remote deployment identities are not guessed or rewritten to match new sources. Re-establish the mapping or leave them unverified/stale.
- `risk_acceptance`: null or `{person, reason, recorded_at}`. It changes neither score nor blockers and does not authorize production actions.
- `next_item_id`: unresolved actionable item or null. The renderer ignores checks waiting for a future deployment or real use and prioritizes unresolved mandatory prerequisite stages. An unavailable preparation environment prompts restoring access; a known failure remains actionable even when other checks are waiting.
- `history`: renderer-managed prior completed snapshots only, without recursively nesting history. Keep the latest completed snapshot per `(audit.id, context.target_stage)`; keep different stages of one audit independently. Working saves never become historical outcomes. A new completed result for the current audit/stage replaces its prior checkpoint, so the current result is not duplicated in history. While that same stage is reopened as work in progress, retain its last completed checkpoint until completion. Supplied replacement history is ignored. A normal renderer save also removes working snapshots and duplicate checkpoints left by earlier schema-2 renderers, preserving the retained snapshots' original dates, evidence and environment identities.

Example evidence (replace every value with real observations):

```json
{
  "kind": "agent",
  "source": "Inspected browser smoke test at https://app.example.test",
  "result": "Test account completed the main journey and read the saved result.",
  "checked_at": "2026-11-10T12:00:00+01:00",
  "audit_id": "the-current-audit-id",
  "stage": "deployment",
  "source_version": "the-assessed-source-fingerprint",
  "environment": {
    "id": "production-eu",
    "kind": "production",
    "name": "Production EU",
    "address": "https://app.example.test",
    "version": "the-observed-deployment-id",
    "source_version": "the-assessed-source-fingerprint",
    "config_revision": "the-observed-config-revision",
    "available": true
  }
}
```

## Ratings and verdicts

Each stage has its own denominator: required items in that stage whose applicability is not `no`, including unknown applicability and waiting items. Its numerator is current passing requirements. Equal weights, percentage floored, zero denominator means no score. Recommendations never count. `blockers` is the stage's total unresolved requirements, `waiting` is its unresolved waiting subset and `actionable` the remainder. Waiting checks never enter an earlier stage's denominator.

Verdicts distinguish a future stage, incomplete assessment/scope/applicability, incomplete prerequisite stages, open mandatory requirements and no basis to assess. Passing results are `Gotowe do wdrożenia`, `Wdrożenie sprawdzone` and `Spełnia ustalone kryteria obserwacji`. A later stage cannot receive its successful verdict while an earlier mandatory stage is unresolved. No score or verdict deploys anything or promises future stability. Observation criteria and sufficient sample/window are app-specific, not a universal 24-hour wait.

HTML status and text filters affect only the current checklist, not later or previous groups, and never change scores. Each collapsed row shows status and title. Expanded content identifies the actual selected place of inspection; allowed environment kinds and precise identities stay in technical details. The next-action link opens any enclosing previous-stage disclosure when needed. The page makes no network requests, writes no local storage and cannot save itself. Geist Sans and its OFL license are embedded in the generated HTML.
