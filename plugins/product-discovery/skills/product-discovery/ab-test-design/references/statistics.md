# Calculation contract

## Planning versus results

Power is the probability of rejecting the null if a specified true effect exists under the assumed model. It is not the probability the hypothesis is true or a promise of significance. Prospective sizing is different from an observed p-value. Do not report post-hoc observed power.

Defaults: independent binary outcomes, equal A/B allocation, two-sided alpha = 0.05, power = 0.80, one primary metric, a predeclared final analysis. A business threshold and statistical detectability answer different questions. Sizing to detect a 5% relative improvement against zero does not prove an improvement of at least 5%; such a claim needs an interval/test against that margin.

## Implemented approximation

Let p0 be baseline, p1 the target, d = |p1 - p0|, n the sample **per arm**, q = (p0+p1)/2, z = 1.959963984540054.

```
v0 = 2*q*(1-q)
v1 = p0*(1-p0) + p1*(1-p1)
power(n) = Phi((d*sqrt(n) - z*sqrt(v0))/sqrt(v1))
         + Phi((-d*sqrt(n) - z*sqrt(v0))/sqrt(v1))
```

This uses pooled null variance and unpooled alternative variance. Solve numerically for the smallest integer n with power >= 0.80. Solve for the minimum detectable absolute change in the specified direction at the available n. Do not return an MDE if even the boundary rate cannot attain the target power.

```
n_available_per_arm = floor(weekly_unique_eligible_units * recruitment_days / 14)
sample_driven_days = ceil(2*n_required * 7 / weekly_unique_eligible_units)
recruitment_days_required = max(14, 7 * ceil(sample_driven_days / 7))
readout_days = recruitment_days + max(primary_window_days, guardrail_window_days)
```

Recruitment accepts only 14, 21, 28, 35 days and subsequent full-week intervals, with matching start/end weekday and local clock time. The calculator rejects shorter or incomplete-week scenarios. This is the skill's planning rule, not a mathematical consequence of power analysis. Traffic is a constant-arrival planning assumption; actual arrivals and allocation vary. Check national holidays in relevant markets, promotions and campaigns before choosing dates. Fourteen days covers two of each weekday but does not guarantee protection from special events or longer seasonality. Adjust dates or lengthen the planned horizon in full weeks when needed. Choose the horizon before launch; do not extend because a p-value is close to significance. Timing excludes preparation. Users recruited on the last day still need their full outcome window; follow-up is added after recruitment and need not be in whole weeks. Missing outcomes are not immediate failures before maturity.

Rates must lie strictly between 0 and 1; targets must also stay strictly inside this range. A baseline at 0 or 100%, or fewer than 10 expected successes/failures in either arm at the planned sample, triggers an approximation warning and blocks a ready recommendation. Required sample remains an approximate scenario; rare-event/exact or simulation-based design may be needed.

## Observed binary results

Accept integer assignments nA, nB and integer successes xA, xB, with 0 <= x <= n. The denominator includes all assigned eligible units with a complete outcome window. Do not derive it from post-treatment events.

```
pA = xA/nA; pB = xB/nB
pooled = (xA+xB)/(nA+nB)
SE0 = sqrt(pooled*(1-pooled)*(1/nA+1/nB))
z_observed = (pB-pA)/SE0
p_value = 2 * Phi(-|z_observed|)
SE1 = sqrt(pA*(1-pA)/nA + pB*(1-pB)/nB)
95% CI = (pB-pA) +/- 1.959963984540054*SE1
```

The CI is an approximate unpooled Wald interval for the absolute difference, displayed in percentage points. It may disagree slightly at the threshold with the pooled z-test. Do not calculate a definitive result for fewer than 10 observed successes/failures in any cell; use an exact or otherwise appropriate method separately. The display suppresses p and CI in that state, including all-zero/all-one data.

Check A/B 50/50 assignment with Pearson chi-square (df = 1), equivalently zSRM = (nA-nB)/sqrt(nA+nB), two-sided p. pSRM < 0.001 is an explicit diagnostic warning threshold, not proof of its cause. Block interpretation until investigated. Do not confuse metric denominators after filtering with original assigned counts.

Final interpretation requires full planned duration, mature outcomes, and valid instrumentation/assignment. If p < 0.05, report the effect's direction, magnitude, uncertainty and guardrails; do not auto-ship. If p >= 0.05, say evidence is insufficient, not that variants are equal. An interval excluding an economically useful effect can support a different decision than a wide interval. Stop early for harm under the agreed safety rule; repeated unadjusted significance checks cannot justify an early win. Sequential designs need their own method.

## Sources

- [statsmodels: power for two independent proportions](https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.power_proportions_2indep.html): pooled null/unpooled alternative variance.
- [statsmodels: two-proportion z-test](https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.proportions_ztest.html): observed binary comparison.
- [Microsoft: during-experiment patterns](https://www.microsoft.com/en-us/research/group/experimentation-platform-exp/articles/patterns-of-trustworthy-experimentation-during-experiment-stage/): guardrails, data quality and repeated testing.
- [Microsoft: diagnosing sample ratio mismatch](https://www.microsoft.com/en-us/research/publication/diagnosing-sample-ratio-mismatch-in-online-controlled-experiments-a-taxonomy-and-rules-of-thumb-for-practitioners/): allocation as a validity check.
