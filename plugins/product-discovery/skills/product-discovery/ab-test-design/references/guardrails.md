# Simple guardrail monitoring

Use one or two metrics to check whether improving the primary outcome causes an unwanted deterioration. Keep the usual conversation and card light.

1. Define the event, denominator, current value if known, observation window from assignment and harmful direction.
2. Agree before launch that a statistically significant deterioration against concurrent A blocks the rollout and prompts investigation.
3. Review after the fixed recruitment horizon and the full follow-up for every participant. Seven days for activation is a per-person outcome window, not a sufficient sample size or permission to end recruitment early.
4. If no significant deterioration is detected, this monitoring rule does not block an otherwise successful primary result. This is an agreed detection rule, not proof of exact equality or absence of harm. Say that once in plain language. Do not label it non-inferiority.
5. Missing, immature, corrupted or extremely sparse data cannot establish that monitoring has passed. If reliable assessment is impossible, explain the concrete issue and keep that result unresolved.

For a binary guardrail, the existing two-proportion calculation can be used after actual counts are supplied: a harmful-direction difference with a two-sided p < 0.05 is detected deterioration under the default rule. Use the guardrail's actual denominator. Check allocation/SRM on the original randomized counts, not on treatment-dependent registration counts. Keep the alpha and direction fixed before the test. Do not use repeated unadjusted peeking to claim success. Early safety intervention is allowed under the agreed rule.

Check the denominator. Registration at 5% and activation at 10% can be consistent if activation is measured among registrants. Preserve that denominator when it expresses the user's concern about acquired-user quality. Because the treatment changes who registers, this rate describes the resulting mix; it is not an effect on the same underlying people. Activation per all randomized people can be a useful extra view, but do not require it or silently substitute it for the requested metric.

A compact card can say: "We track first projects created within 7 days. Today this is about 10% of people who register. If B has a statistically significant drop against A, we hold the rollout and investigate." Keep one short note explaining that no detected decline does not guarantee zero impact.

Do not require a tolerated deterioration margin or separate guardrail power calculator by default. If the user explicitly needs evidence that harm is smaller than a specified amount, explain that this is a different, stronger question. Agree an acceptable margin and use an appropriate separately verified non-inferiority method; do not silently turn the basic card into that workflow.

Source: [Spotify explains detection and non-inferiority as two different ways to use guardrails](https://confidence.spotify.com/blog/better-decisions-with-guardrails).
