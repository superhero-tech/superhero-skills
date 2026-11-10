# State and commands

The HTML is the single durable artifact. `checklist.py` embeds JSON in `script#readiness-data`, escapes untrusted content, calculates ratings and keeps previous report snapshots. Do not hand-edit generated HTML or its history. Python 3.9+ and the standard library suffice. The renderer validates records; the agent still owns the factual assessment of evidence and applicability.

Resolve `SKILL_DIR` and `PROJECT_DIR` to absolute paths. Default output is `docs/production-readiness.html` inside the project. A custom `--output` must also remain inside that project. Inspect repository instructions and existing reports first.

```sh
# New report, never overwrites an existing file.
python3 "$SKILL_DIR/scripts/checklist.py" init --repo "$PROJECT_DIR"

# Existing report: begin a fresh audit, retaining history. Previous passes
# become stale, conditional applicability is reset, scope needs reconfirmation.
python3 "$SKILL_DIR/scripts/checklist.py" refresh --repo "$PROJECT_DIR"

# Make a private temporary working copy, edit its JSON using file tools,
# then render. Only the HTML is retained in the target repository.
CHECKLIST_WORK=$(mktemp -t production-readiness.XXXXXX)
python3 "$SKILL_DIR/scripts/checklist.py" extract --repo "$PROJECT_DIR" > "$CHECKLIST_WORK"
python3 "$SKILL_DIR/scripts/checklist.py" render --repo "$PROJECT_DIR" --input "$CHECKLIST_WORK"
rm "$CHECKLIST_WORK"

python3 "$SKILL_DIR/scripts/checklist.py" validate --repo "$PROJECT_DIR"
```

Insert the JSON edit between `extract` and `render`; rendering an untouched extract does not perform an audit. Use the same `--output` on every command when customizing the path. If there is no Python, report the missing prerequisite instead of claiming a generated HTML result. Do not install dependencies silently.

## Editing contract

- `schema_version`, `template_version`, `revision` and `_base_digest`: preserve values from extraction. `_base_digest` prevents overwriting a report changed since extraction and is not stored in the HTML.
- `audit`: preserve `id` and `started_at` for one assessment. Set `phase` to `complete` after completing the agreed audit, even if checks fail. Use `refresh` for another assessment, especially after code fixes.
- `project`: generated name, commit, dirty flag and content fingerprint of Git-listed files (excluding the report). Do not invent a commit for a non-Git repository. The renderer compares metadata before saving and rejects a changed working tree. Without Git the fingerprint is null, so content changes need direct assessment. Ignored files, submodule contents and external configuration also need direct assessment. Refresh after application/configuration edits, even when not tracked by Git.
- `context`: `hosting`, `audience`, `data`, `outage_impact` are nonempty plain-language strings. `scope_confirmed` becomes true only when these are established for the assessed release. No credentials, real personal data or sensitive incident details.
- `items`: baseline fields come from `assets/checklist.json`; do not delete baseline or existing custom IDs. Keep required criteria required. To add an application-specific item, use a new stable lowercase-hyphen ID, `origin: custom`, an existing category and a rationale explaining why it matters.
- Each item has `title`, `why`, `condition`, `verification`, `steps` (nonempty list), `rationale`, `category`, `required` (boolean), `priority` (`high` or `normal`), `origin` (`baseline` or `custom`). Rewrite explanations for the actual application without weakening checks. `high` orders next actions; it does not weight the score.
- `applicability`: `yes`, `no`, `unknown`. `no` needs `applicability_reason`; unconditional baseline items cannot be excluded. Unknown is not an exclusion and prevents a completed readiness verdict.
- `status`: `pass`, `fail`, `unverified`, `stale`. A pass needs applicable=yes and current evidence. `finding` explains the actual observation in everyday language. `owner` is `agent` or `human`, identifying who can take the next step. `steps` should become concrete, numbered instructions appropriate to that owner.
- `evidence`: list of records with `kind` (`agent` or `human`), `source`, `result`, `checked_at` (ISO timestamp with timezone), and `audit_id`. Human evidence also needs `person`. For a pass, every attached record must belong to the current audit. Keep old evidence in historical snapshots; do not relabel it as new. A newly reconfirmed human record should describe the original event and what was actually reconfirmed now.
- `risk_acceptance`: null or `{person, reason, recorded_at}`. This annotation never changes a score or blocker. Keep it visible until the underlying issue is resolved; history preserves prior decisions.
- `next_item_id`: unresolved item to emphasize or null for automatic prioritization. Prefer a required blocker the person/agent can act on now. If all checks pass but context is unresolved, finish the assessment first.
- `history`: managed by the renderer, not by the agent. Every save appends the previous complete state without recursively nesting history. Existing history supplied in edited JSON is replaced with history from the actual report.

Example evidence (replace all details with real observations):

```json
{
  "kind": "agent",
  "source": "tests/access.test.ts:18; npm run test:access (exit 0)",
  "result": "Próba odczytu danych innego konta została odrzucona. Oba scenariusze testowe zakończyły się poprawnie.",
  "checked_at": "2026-11-09T12:00:00+01:00",
  "audit_id": "the-current-audit-id"
}
```

## Rating and verdict

The denominator is all required items whose applicability is not `no`, including unknown applicability. The numerator is applicable required items passed with evidence belonging to the current audit. The percentage is floored, so an incomplete result never rounds to 100%. Zero denominator gives no score, not 100%. Category ratings use the same rule. Recommendations never count.

Each remaining denominator item is an open blocker, including an accepted risk. Verdict precedence: incomplete scope/audit/applicability -> `Ocena nieukończona`; open mandatory requirements -> `Wydanie zablokowane`; no denominator -> `Brak podstaw do oceny`; otherwise -> `Spełnia wymagania checklisty`. Show blocker count even during an incomplete audit. A ready verdict allows recommendations to remain open and never deploys anything.

HTML filters only affect viewing. They cannot change statuses, evidence or the stored score. The page makes no network requests, writes no local storage and cannot save itself. Only the agent and renderer update the durable artifact.
