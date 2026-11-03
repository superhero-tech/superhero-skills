# DESIGN.md format

Write in the user's language. Keep sections proportional to observed evidence. Use this structure as a starting point; optional sections may be absent. No minimum color/component counts.

1. **Source and coverage:** actual URL(s), extraction date, evidence directory, browser, viewport dimensions, measured states, and material limitations. Do not call sample widths exact breakpoints.
2. **Visual character:** a short screenshot-backed description of density, hierarchy, image treatment, alignment, and whitespace. Avoid formulaic personality claims. Label interpretation as Observed or Inferred.
3. **Style values:** tables for colors with observed roles, complete type styles, spacing, radii, borders, shadows, and motion where present. Keep exact computed values and references. Do not infer a spacing base unit from a few values or rank palette frequency as brand importance. Describe fontFamily as a CSS stack unless actual rendering is verified.
4. **Components:** representative buttons/links, cards, navigation, and fields that were found. Include selector, shape/layout/type values, observed default state, and separately measured states. Missing hover/focus/disabled variants are Unverified, not conventional defaults supplied by the agent.
5. **Responsive behavior and themes:** compare actual snapshots and screenshot changes. Cite both widths. Separate accessible declared media queries from checked behavior. Include a dark palette only if captured and verified.
6. **Brand assets:** confirmed logo source or inline-SVG selector and observed image treatment. Candidate logos remain candidates until visually confirmed. Do not fabricate missing URLs or export inaccessible assets.
7. **Implementation guidance:** a few concrete rules derived from evidence. Preserve the observed hierarchy and component styling. Ready-to-use prompts are optional and must not add undocumented tokens, component states, or behavior.
8. **Gaps:** unavailable pages/variants, truncated sampling, unsupported capabilities, uncertain fonts, or obstructed content. Summarize next measurements that would resolve important gaps, without doing unrelated research.

Use the labels **Measured**, **Observed**, **Inferred**, and **Unverified** in the document's language. They can be table columns or paragraph labels rather than repeated prefixes on every sentence. Every exact source claim must be traceable to a snapshot property or clearly identified CSS declaration. Visual claims cite screenshots. An inference cites its supporting observations and remains an inference.

Evidence references should remain clickable when the artifact is moved with its evidence directory. Do not invent success/error colors, missing H3 styles, disabled states, or responsive thresholds to fill a template.
