# Opportunity scoring rubric

PRES = **Pain + Reach + Evidence + Strategic fit**. Four integer axes, each 1-5, summed without weights. Use this rubric consistently within a comparison. This is the convention extracted from the original OST workflow, not a claim that these numbers are a universal or statistically validated scale.

Use 2 or 4 when evidence falls between the stated anchors and explain why. Anchors are judgments for comparison, not measured facts. Do not invent percentages, affected populations, source counts or causal effects to satisfy an anchor. An unsupported axis is `unknown` and prevents a total. Sources support an observation; the score assigned to it remains a reviewable judgment.

## P: Pain

How seriously does the problem affect the user in this situation?

| Score | Anchor |
|---|---|
| 1 | Minor inconvenience; the user completes the task without a meaningful workaround or consequence. |
| 3 | Blocks or disrupts a step; the user seeks help, repeats work or uses a meaningful workaround. |
| 5 | Causes a consequential failure such as abandonment, refund, churn or substantial loss of time/money. |

Score the person's experience, not team frustration, roadmap visibility or emotional wording alone. A critical isolated event may be high Pain and low Reach. Do not turn one extreme anecdote into the whole segment's experience.

## R: Reach

How many people in the relevant population experience the problem, and how often?

| Score | Anchor |
|---|---|
| 1 | An uncommon problem or infrequent event affecting a small part of the relevant population. |
| 3 | A recurring problem for a meaningful segment, or a frequent problem for a smaller segment. |
| 5 | A frequent problem affecting most of the relevant population or its core task. |

Name the denominator, period and recurrence separately. Use the same comparison population/window across candidates; show actual counts or rates when available. Broad anchors avoid pretending that a percentage alone captures both population and recurrence. If the team needs quantitative cutoffs, propose context-specific anchors for human review before scoring, without changing them to favor one candidate.

Interview mention counts describe the analyzed sample, not automatically market reach. Several deliberately recruited users reporting a problem do not establish what percentage of all users experiences it. Preserve the sample limit; if no defensible reach assessment is possible, leave it unknown. Unknown is not 1.

## E: Evidence

How strongly do the sources support the existence and framing of this problem for this population?

| Score | Anchor |
|---|---|
| 1 | Team/agent hypothesis with no supporting user or behavioral evidence. |
| 3 | A repeating relevant signal across independent experiences, or a suitable quantitative measure supporting the problem's framing. |
| 5 | Strong, applicable triangulation across independent evidence and complementary methods; important rival explanations and contradictions have been assessed. |

Consider directness, independence, method fit, recency, segment match and counterevidence. Source count alone is not sufficient. Three quotes from one interview are one experience; reports reusing one dataset are not independent sources. Analytics may show where behavior changes without establishing why. A repeated customer statement does not prove its stated cause.

**Evidence = 1: stop scoring this candidate**, assign `research-first`, omit its total and propose a targeted evidence-gathering step. Do not silently delete it or prevent a deliberate human choice. Where known evidence is inaccessible or its relevance is unclear, record that gap rather than claiming there is no evidence.

## S: Strategic fit

How plausibly would addressing this need contribute to the agreed outcome?

| Score | Anchor |
|---|---|
| 1 | Tangential to the current outcome; little supported connection. |
| 3 | Contributes indirectly through an identifiable intermediate behavior or condition. |
| 5 | Closely connected to the outcome through a clear, evidence-supported mechanism. |

State the mechanism and supporting evidence or explicit strategic direction from the human. A business aspiration is a valid source for the chosen direction, not proof of the magnitude of an effect. Even 5 does not prove causality or that a specific solution will succeed. No agreed outcome means S is unknown and no overall ranking is defensible yet.

## Reading the scorecard

- Compare complete candidates against the same outcome and segment. Do not rank broad needs against narrowly scoped incidents without addressing the difference.
- Keep an equal-weight sum, not a product. Never display a total that includes missing values, Evidence = 1 or unsupported default scores.
- A one-point difference is a discussion signal. Review uncertain axes and ask the human to decide; do not add decimal precision or percentages of confidence.
- Opportunity priority is separate from solution confidence, delivery effort, experiment sequencing and implementation approval. Those need other judgments.
