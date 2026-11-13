---
name: ab-test-design
description: Design an A/B test and decide whether available traffic can detect a useful effect. Use when planning a randomized product comparison, checking sample size or test duration, or creating an interactive A/B test card.
metadata:
  ready_to_publish: "true"
---

# A/B Test Design

Help the user decide whether an A/B test is worth running, then produce a compact test card with an interactive calculator. A well-supported decision not to run is a valid outcome.

Respond and produce all artifacts in the user's conversation language.
Keep the conversation light: ask one focused question at a time, explain unfamiliar terms in plain language, and reuse information already supplied. Do not present the whole intake as a questionnaire or require a discovery framework.

## Four conversational gates

### 1. Change and hypothesis

Ask what specifically changes, what behavior or outcome should improve, and why the change should cause it. Help turn vague goals into a concrete comparison; do not invent the user's mechanism.

An initially vague idea, such as a more prominent call to action, is a valid starting point. Help formulate a tentative mechanism without promoting a guess to evidence. Do not reject a visual change merely because it sounds small; assess the decision, effort, traffic and plausible useful effect. If several attributes change, explain that the test evaluates their combined effect.

Draft: "If we [change], then [population] will [observable outcome], because [mechanism]." Name A (current experience) and B (changed experience). This is a first hypothesis; add the measurable target in gate 3.

Check whether an experiment would change a real decision. If the change must ship regardless, is a repair of a known defect, or only needs a usability check, explain when an A/B test adds little value. Ask about the alternative method only if it helps this decision.

### 2. Population and exposure

Ask who is eligible, where they enter the experiment, and how many **new unique eligible randomization units** enter per day or week. Default to stable random assignment of users, A/B 50/50, with the same user always seeing the same variant. Explain that 1,000 eligible users/week means about 500 per variant/week, not 1,000 per variant. Visits, events and repeat sessions are not extra independent people.

If only a segment or part of the traffic participates, use its effective traffic once, without multiplying the eligibility/rollout fraction twice. Check that eligibility is determined before the treatment can affect it. Count everyone assigned in the metric denominator, including non-converters. Avoid filtering the comparison to people who completed a treatment-affected step.

Check concurrent randomized comparison is possible. Company-level assignment, network effects, paired data, interference or more than two variants require another calculation; do not apply the bundled independent-user calculator.

### 3. One primary metric and a useful effect

Ask how success is measured. Define the numerator, denominator, desired direction, and outcome window **per assigned unit**. Prefer a rate such as accounts created / eligible users over raw totals when opportunities differ.

Collect the current baseline and its source/period for the same population and outcome window. Ask what change is worth acting on and what effect the user realistically expects. These may differ: record both, and normally size the test to detect the smallest effect worth acting on. A hopeful forecast is not a sufficient reason to choose an easy-to-detect target.

When the user asks what target or duration to choose, offer a calculated, explicitly proposed option from known traffic and baseline. Do not make them guess statistical inputs. An ambitious target stays a business threshold, not an established forecast; show sensitivity where downstream sizing depends on it.

Clarify relative percent versus percentage points with actual values: 20% to 21% is +5% relative, +1 pp; 20% to 25% is +5 pp. Never silently interpret "+5%".

Separate **recruitment duration** from **outcome maturity** and the deadline for a decision. "Within 14 days" may mean any of these; resolve that ambiguity. For 14 days of recruitment and a 7-day outcome window, allow up to 21 days before the last cohort is mature. Also ask the maximum useful duration when a longer test could miss the decision.

Plan recruitment for **at least 14 consecutive days, then whole-week intervals: 14, 21, 28, 35 days, etc.** Round the sample-driven duration up to the next allowed interval, even when enough people arrive sooner. Start and end at the same weekday and local clock time so every weekday occurs equally often. Add the full outcome/guardrail follow-up after recruitment; that waiting period need not be a whole number of weeks. Check national holidays in the audience's markets, promotions, campaigns and other unusual events before fixing dates. Two weeks helps cover weekly variation but does not eliminate holiday effects or longer seasonality; move the dates or plan a longer representative window when needed. Set the horizon before launch. Any extension must be justified by recruitment or calendar coverage, not by waiting for significance; retain early safety stops.

Unknown baseline/traffic/target stays unknown. Offer a clearly labeled sensitivity scenario or a short baseline measurement, not fabricated precision or a launch-ready plan. Do not assume baseline 50% is universally conservative for a relative lift.

### 4. Guardrails

Ask what could worsen while the primary metric improves. Usually one or two meaningful metrics are enough. Define the action, population/denominator, current rate when known, observation window and harmful direction. Check denominator consistency: 10% activation among registrants is different from 10% among all visitors. Do not silently change the user's denominator or require a second metric merely to complete a framework.

Default to a simple monitoring rule: after the planned test and full follow-up, check whether the guardrail has a statistically significant deterioration relative to the concurrent control. If so, hold the rollout and investigate. If not, the monitoring condition does not block a successful primary result. Describe this as "no deterioration detected", not proof of zero harm. Missing or invalid data cannot count as a pass.

Read [references/guardrails.md](references/guardrails.md) when selecting or interpreting this rule. Agree the rule before launch. Do not require non-inferiority margins, separate power estimates or a guardrail calculator in the normal flow. Introduce stronger safety claims and their requirements only if the user explicitly needs them. Do not turn a request for simplicity into a promise of certainty.

An outcome window such as 7 days says when a person's activation can be assessed, not how much data has been collected. Keep the 14-day minimum and whole-week recruitment intervals, then add the longest follow-up. Explain once, in plain language, that a small deterioration can go undetected. Do not make the same qualification dominate every section.

## Feasibility and decision

Read [references/statistics.md](references/statistics.md) before calculating. The bundled calculator supports **one binary outcome per independent unit, two variants, equal allocation**, fixed horizon, two-sided alpha 0.05 and target power 80%. These defaults are visible, not a guarantee of a significant result. Run `scripts/check_calculator.py` when changing the calculation or renderer.

Run the bundled primary-metric code; do not estimate sample size mentally. For revenue, time, counts, clustered assignment, rare events or other designs, explain the missing variance/design information and use a suitable method separately. Still produce a card marked as needing that calculation, with the unsupported calculator disabled.

Report the baseline-to-target change, expected sample per arm, required sample per arm, approximate power, recruitment time and final readout time including the longest relevant follow-up. Recruitment must respect the 14-day minimum and whole-week intervals above; check whether longer business or seasonal cycles require more time.

Use three outcomes:

- **Reasonable to run:** enough power for a useful, plausible effect within a useful time, and a measurable randomized comparison with defined guardrails. This is a design recommendation, not permission to launch.
- **Revise the plan:** show the required duration, or the minimum detectable effect at the available duration. Offer longer recruitment, genuinely more eligible traffic, or a materially different change with a credible chance of a larger effect. Do not raise the target merely to make the arithmetic pass.
- **Do not run this A/B test now:** detection would take too long, the useful effect is too small for available traffic, the design cannot support a causal comparison, or results would not change the decision. Suggest the smallest useful alternative (baseline measurement, usability study, prototype, staged monitored release). Explain what that alternative can establish.

Do not suggest lowering the evidence standard, repeated peeking, post-hoc segment hunting or silently switching to a one-sided test as fixes for insufficient traffic.

## Deliverable

Create `experiments/<short-name>/card.json` and a standalone `ab-test-card.html` in the user's project (preserve earlier versions). Use [references/card-format.md](references/card-format.md) for the data contract and renderer. Keep client data outside this skill.

The card includes the hypothesis, variants, population, primary metric, target, a short description of what else to watch, timing and a clear recommendation. Use one primary-metric calculator with sliders and precise inputs. Keep each guardrail to what is measured, over what period, and what we do if it worsens. Do not add guardrail calculators, margin tables or a second results dashboard. Scenario changes must not silently rewrite the saved hypothesis or plan. Include a reset to the saved plan.

Write for a product person without a statistics background: short concrete sentences, familiar words, and a clear next action. Put calculation details under the method disclosure, not into the hypothesis or recommendation. State uncertainty once where it changes interpretation; avoid repeated caveats.

Clearly separate planning power from observed significance. The results panel starts empty; never turn expected conversions into observed data. Show p-value, effect and interval only after actual counts are entered, flag sparse data and allocation mismatch, and withhold a final interpretation until the planned horizon and full follow-up are complete and data quality is checked. No statistical result alone authorizes shipping.

Predeclare a simple decision rule: consider rollout if the primary result meets the agreed goal and no significant guardrail deterioration is detected; hold if deterioration is detected; call the result unresolved if primary evidence or required data are insufficient. The design's green/yellow/red tag describes whether the plan is worth running, not an observed win or permission to launch.

Use a restrained experiment-tool layout: experiment description on the left, recommendation above the calculator on the right. Put a green, yellow or red status tag inside each recommendation box, with a textual verdict as well as color. Place the relative-percent / percentage-point selector beside the effect input. Include A/B variant cards, primary metric, guardrail rows and sample progress. No external fonts, dependencies or network calls. Polish and English UI are bundled; for other languages translate the template's interface dictionary as well as the card content before rendering.

Open the output in an available browser and verify desktop/mobile layout, scenario updates and reset, missing-data state, and a known results example. If no browser is available, run the statistical checks and say visual verification remains undone. Return a link to the HTML and a short explanation of whether the proposed test is worth running. Designing the test does not launch it or configure an external experimentation tool.
