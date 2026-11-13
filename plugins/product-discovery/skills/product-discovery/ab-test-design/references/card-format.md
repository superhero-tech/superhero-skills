# Card data and rendering

Use the generic [example JSON](../assets/example.json) as the shape, replacing all example content with the user's plan. Do not use the example's numerical assumptions as defaults for a real test. `illustrative: true` displays a prominent demo banner; real plans normally use `false`.

All prose fields are plain text, rendered with `textContent`. Numeric fields:

| Field | Meaning |
|---|---|
| `baseline` | Rate as a fraction, e.g. 0.20; `null` if unknown |
| `effect` | Positive magnitude, e.g. 5; `null` if unknown |
| `effect_type` | `relative` for relative percent, or `pp` for percentage points |
| `direction` | `up` or `down`; desired direction of primary metric |
| `weekly_users` | Effective new independent eligible units/week across A+B; `null` if unknown |
| `recruitment_days` | Recruitment duration: at least 14 days and a multiple of 7 (14, 21, 28, etc.), excluding final follow-up; `null` if unknown |
| `primary_window_days` | Full per-person primary outcome window; `null` if unknown |
| `guardrail_window_days` | Longest guardrail follow-up from assignment; `null` if unknown |
| `max_readout_days` | Maximum useful total time from launch to final readout; `null` if unknown |
| `calculator_supported` | `false` for continuous metrics, clusters, unequal splits and other unsupported designs |

`guardrails` contains objects with `name`, `definition` and `limit` (include the current rate and observation window in the definition and the agreed response to deterioration in the limit). `blockers` is a list of unresolved design/measurement issues. Missing required inputs, an unsupported design, explicit blockers and demo status prevent a green ready badge, even if the numerical scenario is adequately powered.

Keep guardrails as plain text: `name`, `definition` and `limit`. Describe what is measured, its current rate when known, the observation window, and the agreed response to a significant deterioration. Use `guardrail_window_days` to include follow-up in the final readout. The default card has one primary-metric calculator; it does not calculate guardrail margins or sample-size scenarios. See `references/guardrails.md` for the monitoring rule and its interpretation.

The free-text `recommendation` and `decision_rule` describe the saved plan, not whatever scenario a reader explores. Put expected versus minimum useful effects in the hypothesis or recommendation if they differ. `effect` is the chosen sizing effect, normally the minimum useful change. The code's significance test compares B against A at zero difference; it does not prove the entire chosen sizing effect.

Required textual keys: `title`, `hypothesis`, `control`, `treatment`, `population`, `metric`, `metric_definition`, `baseline_source`, `recommendation`, `decision_rule`. Unknowns can be described explicitly, but must not be replaced with fictional values. Empty guardrails automatically add a missing-guardrail warning.

Render with Python 3 standard library only:

```sh
python3 <skill-dir>/scripts/render_card.py experiments/<name>/card.json --output experiments/<name>/ab-test-card.html
```

Use `--demo` instead of the input path to render the bundled hypothetical example. Use `--summary` to print the same planning calculation through Node.js when it is available; the HTML itself needs only a browser. If Node is unavailable, read the calculation from the browser. The renderer does not require Node unless `--summary` is requested.

The output embeds all CSS, JavaScript and JSON; it works offline as a local file. Language codes `pl` and `en` are built in. For another language, add a translated entry to the `I18N` interface dictionary in `assets/card.js` in a temporary template copy, allow that language code in the copied renderer's validation, and translate `card.html`'s fallback title. Do not change the shared skill with project-specific translations. Preserve all calculations and field IDs.

Scenario values can be exported as a separate JSON file. Export preserves the original card, blockers and demo status; it replaces only numerical scenario fields. Before reusing the exported file as a plan, review and update the hypothesis, recommendation and decision rule. The card explicitly identifies this as a scenario rather than a revised approved plan.
