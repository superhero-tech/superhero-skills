# Analysis rubric and evidence model

Use for comparative moodboards and deeper direction studies. Scale depth to the deliverable, but do not replace evidence with style adjectives.

## Analyze the system, not only individual screens

| Dimension | Inspect | Translate into a decision |
| --- | --- | --- |
| Expression | Where the interface is loud or quiet; interface-led vs content-led character | Where should the user's brand spend attention? |
| Typography | Families/stacks when measured; heading/body roles, weight, contrast, line length and wrapping | Which text carries personality, which must remain utilitarian? |
| Color | Base surfaces, text, accent, action and selected states, image-derived colors | What does each color mean, and which roles need separate signals? |
| Composition | Grid, alignment, margins, content width, sectioning and reading order | Which layouts suit discovery, comparison, reading and action? |
| Density and rhythm | Repeated items, fact grouping, whitespace and number of visible choices | What stays stable when many real items repeat? |
| Component anatomy | Required/optional parts, title, image/logo, facts, tags, controls, CTA | What is the primary object and its essential information? |
| Geometry and depth | Corner hierarchy, border weight, dividers, shadow and layering | Which shapes distinguish containers from controls? |
| Imagery and identity | Photography, illustration, logos, iconography, textures and asset quality | How much of the direction depends on editorial production? |
| Interaction | Observed focus/selection/hover, progressive disclosure, sticky elements, motion | Which behaviors are essential, and which remain unverified? |
| Content and narrative | Labels, employer/product story, facts vs persuasion, missing data | How does the visual hierarchy support the user's decision? |

A token table should include the value, role, evidence ID, and status. Preserve variation instead of forcing a falsely uniform system. For example:

| Role / proposed token | Value | Status | Evidence and interpretation |
| --- | --- | --- | --- |
| Selected-tab fill | Exact CSS value, if inspected | Measured | Screen + element + property + state |
| Section background | Approximate visual color | Estimated | Labeled crop; not a verified official token |
| Proposed heading scale | Starting size/weight for our product | Proposed | Reason and reference mechanism |
| Mobile breakpoint | Unknown unless actually established | Unverified | Two viewport captures do not establish an exact threshold |

A CSS font stack is not proof of which font file rendered. Do not infer precise spacing, letter spacing, radii, contrast compliance, or layout breakpoints from screenshots alone. Where useful, give labeled visual estimates rather than omitting the dimension entirely.

## Comparative moodboard

Organize finalists into descriptive visual families derived from observations, such as editorial typography, graphic interface, content-led gallery, or brand-accented utility. Categories may overlap. Avoid invented numerical style scores or ratings presented as measurements.

For each finalist include:

- Name, direct source links, sampled screens and coverage.
- A short thesis about its visual mechanism.
- Screenshots, useful crops, palette and typographic roles.
- Key component anatomy and a concise token table with provenance.
- Information hierarchy and the relation between expression and density.
- Transferable ingredients, content dependencies, limitations, and costs.
- A concrete choice the reference helps the user make.

Add a cross-reference comparison: typography, color semantics, grid, density, component treatment, and reliance on imagery. Make direction names stable so the user can select them without ambiguous image-order numbers. Label numbered screenshots explicitly.

The selection prompt should accept both a whole direction and a combination, e.g. “Use the typography from A, the card structure from B, and less color than C.” Do not ask the user to pick dozens of tokens individually.

## Deeper direction study

Base the study on several distinct screens of the selected reference(s). Prefer a meaningful path through the product: entry → listing → entity profile → detail, or the equivalent for the domain. Include lower-page content and a narrow-screen sample when relevant and accessible.

Deliver:

1. An atlas identifying distinct page types, frames, viewports and states.
2. A concise direction thesis backed by repeated patterns.
3. Detailed features with the following chain:
   - Observation and cited screenshot/detail.
   - Design mechanism and its impact on hierarchy.
   - Implication for the user's product.
   - Trade-off, dependency, or unresolved choice.
4. Shared foundations and component families, including tokens with evidence status.
5. What varies by screen/task, including inconsistencies in the source.
6. A decision table: keep/adapt/drop, rationale, and what needs testing.
7. A proposed visual brief specifying expression, typography, accent roles, surfaces, geometry, layouts, hierarchy and asset requirements.
8. Limits of the sample and open decisions.

Use real evidence for every major feature, preferably examples from more than one view where the feature is claimed to be systemic. Do not force two screenshots when a feature is unique to one observed page. Preserve the distinction between a one-off feature and a recurring rule.

## Combining selected ingredients

Build a provenance map: ingredient → source → user's choice → adapted rule. Resolve conflicts between font density, generous cards, multiple accent colors, different icon weights, or incompatible corner systems.

Aim for a single grammar that works across the user's screens, not a collage of brand signatures. Do not copy source logos or reuse third-party screenshots as interface artwork. A token or decision chosen by the user overrides a proposed default; unselected recommendations remain proposals.

Use relevant content stress cases when explaining feasibility: long titles, missing values, many tags, dense repeated entries, and mobile reading order. These are proposed tests, not claims that the original product has passed them.

Do not infer conversion uplift, verified accessibility, or motion from appearance. State a plausible intended effect as an interpretation and identify what would need testing.
