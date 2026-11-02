---
name: visual-direction-research
description: Research existing websites across the open web to find a visual direction, build an evidence-based comparative HTML moodboard, and deepen one direction after the user selects a reference or a combination of elements. Use for visual discovery and art-direction research, rather than implementation of an already chosen style.
---

# Visual Direction Research

Turn the user's brief into a designer's decision process: live research → comparative HTML moodboard → user selection → a deeper HTML direction study. The outcome is an actionable visual direction supported by real interfaces, not a list of attractive homepages.

These instructions and supporting resources are in English. Produce research artifacts and discussion in the user's conversation language unless they request another language.

## Start at the appropriate stage

Use existing work and explicit choices. A user who has already selected a direction can go directly to the deeper study; do not force another moodboard or repeat a selection question they have answered.

1. **Frame the research.** Infer the product, audience, primary task, important screen types, desired expression, information density, brand constraints, and likes/dislikes from the brief. Distinguish stated constraints from your assumptions. Ask only for a missing decision that materially prevents useful research; otherwise begin and state assumptions.
2. **Research broadly.** Search the open web, relevant live products and brand sites, curated galleries, and design case studies. The example galleries in [references/research-sources.md](references/research-sources.md) are optional starting points, not an exclusive source list. Search beyond them, including products outside the user's industry when their visual mechanisms transfer well.
3. **Curate and inspect.** Keep a compact working longlist, then select a few distinct, relevant references. A useful default is 3–6 finalists, adjusted to the brief. Prefer a smaller evidenced selection over padding with weak examples. Explain what each contributes and its trade-offs. Review actual rendered interfaces before making visual claims.
4. **Build the comparative HTML moodboard.** Follow the evidence and analysis rubric in [references/designer-analysis.md](references/designer-analysis.md) and the artifact requirements in [references/html-deliverables.md](references/html-deliverables.md). Present the full deliverable with real screenshots, categories, component details, tokens with provenance, and implications for the user's product.
5. **Get the user's selection.** After delivering the reviewable moodboard, ask which reference, direction, or specific elements they prefer. They may combine typography from one, color from another, and composition from a third. Wait for their answer before synthesizing the final direction. If it is already explicit in the request, proceed without asking again. Preserve the original board and the user's subsequent corrections.
6. **Deepen one coherent direction.** Gather additional screens from the selected site or sites. Study several distinct page types and relevant states, not just multiple crops of a homepage. Translate selected ingredients into one coherent system; resolve incompatible choices rather than presenting an unexplained collage. Deliver a separate, detailed HTML analysis.
7. **Offer PDF as an optional next step.** After the final HTML is complete, suggest PDF export briefly when useful. Do not create it automatically unless requested. If requested, use the available PDF workflow, retain the HTML, and inspect the rendered PDF for page breaks, images, tables, and clipping.

## Research and capture rules

- Prefer the available built-in/in-app browser for visual inspection and follow its current documentation. Respect an explicit browser preference. Use search tools for discovery and source lookup where appropriate.
- A gallery entry is a discovery source. Follow it to the original site when possible. Separate live interfaces, archived screenshots, concepts, templates, agency case studies, and promotional mockups.
- Choose references for the user's actual task. For a dense catalog, inspect listings, filters, repeated cards, and detail screens. A spectacular landing hero is not sufficient evidence for a working product.
- Inspect multiple meaningful screens of each finalist when accessible; typically 2–3 for comparison and 4–6 distinct views for a deep study. These are planning defaults, not permission to invent pages. Record actual coverage and any shortfall.
- Label different scroll positions as frames of the same page. A crop, a mobile version, and a full-page capture are not automatically three different page types.
- Capture useful loaded states with no obstructing banners. Inspect saved image files, not only the live viewport: overlays can still be fading during capture. Preserve originals; use labeled crops to expose details.
- For every screen, keep an ID, direct URL, capture date, viewport dimensions when known, page type, state, screenshot path, and relevant limitations. Claims and crops must lead back to that screen.
- Use supported read-only computed-style inspection for exact values when available and useful. Retain a small record of the element, property, value, viewport/state, and source screen. Do not infer an official token name or complete design system from one CSS value.
- Avoid repeated retries on persistent blocks. Use other references or available archived material with clear labeling. If the selected direction cannot be inspected sufficiently, explain the gap and request only the source or access necessary to continue.
- Observe hover, focus, responsive behavior, and motion only when relevant and supported. A static screenshot does not establish animation, accessibility, conversion, or all interaction states.
- Browsing and creating local research artifacts do not authorize publishing, installing integrations, submitting forms, or modifying the studied sites.

## Designer-level analysis

Read [references/designer-analysis.md](references/designer-analysis.md) when synthesizing either HTML deliverable.

Make each important finding follow this chain:

**Visible example → design mechanism → effect on the information hierarchy → adaptation for this product → trade-off or decision.**

Analyze the source of expression: interface styling, typography, imagery/content, brand marks, composition, or motion. A colorful portfolio can have neutral UI. Identify which mechanisms survive when the user's product lacks the same imagery, content budget, or sparse catalog.

Keep four statuses distinct at the point of use:

- **Measured:** exact rendered values with element/property/state evidence.
- **Observed:** directly visible patterns in inspected screens.
- **Estimated:** approximate visual values, labeled as such.
- **Proposed / unverified:** adaptations, semantic token names, extrapolated states, or gaps.

Never present proposed decisions as user-approved. For a mixed direction, map each chosen ingredient to its source and explain how it fits the synthesized system. Explicit user corrections take precedence over earlier recommendations.

## Deliverable boundaries and verification

Create standalone HTML research documents in the user's workspace or requested output directory, not inside this skill. Keep screenshots and a small evidence record with the project. Prefer a portable HTML with embedded images; do not rely on hotlinked gallery thumbnails or ephemeral remote URLs.

This skill does not automatically build a production site, create a component library, export DESIGN.md, or send work to Figma/Notion. Those are separate requests. The report's own editorial styling is not the researched product style; label all original design studies as proposals.

Read [references/html-deliverables.md](references/html-deliverables.md) before authoring or revising an artifact. Verify the rendered document at desktop and a narrow width, including lower sections, dense tables, images, anchor links, and any selection or lightbox controls. The read-only browser expression in [scripts/inspect-html.js](scripts/inspect-html.js) helps check structural failures; it does not replace visual review.

Report the actual coverage and link the complete HTML. At the comparison stage, end with a clear request for the user's choice. At the deep-study stage, summarize the key design decisions and optionally offer PDF.
