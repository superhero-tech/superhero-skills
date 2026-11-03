---
name: poster-people-ui
description: >-
  Build or extend screens in a poster-like visual direction with crisp black contours,
  paper surfaces, pink accents, and expressive hand-drawn people. Use when this direction
  or a Gumroad-meets-illustrated-people style is requested for a job board, marketplace,
  directory, or adjacent product screen.
---

# Poster People UI

Build one coherent family of screens: **poster-like interface construction, human character illustration, clear comparison of real information**. The chosen ingredients are Gumroad's graphic UI language and Work With Indies' expressive people. Preserve the user's product, identity, content, and requested implementation scope.

Respond and produce user-facing artifacts in the conversation language. Follow the host project's code and documentation conventions.

## Read the evidence, then choose the composition

Read [the visual system](references/visual-system.md) and [screenshot index](references/screenshots.md). Open the actual images for the task: a working UI reference (S02, S03, or S04), plus S05 for the character language. For responsive work, also open the closest narrow reference (S08–S12). Do not use filenames as a substitute for visual inspection.

Read [screen recipes and review gates](references/screen-recipes.md) for the requested screen type. Read [the illustration brief](references/illustration-brief.md) when creating, commissioning, or adapting original people illustrations.

The bundled screenshots are offline research evidence, not interface artwork. Do not paste them into the product or copy the source brands' logos. Their promotional text, commerce features, and third-party forms are not product requirements.

## Establish continuity

Inspect existing navigation, components, theme roles, assets, and real content before editing. Reuse the framework and shared primitives. Map the direction onto the project's native tokens instead of adding unrelated per-screen values. A request for one screen does not authorize an application-wide conversion.

In a new project, use the reference defaults without asking the user to choose every token. [assets/tokens.css](assets/tokens.css) supplies opt-in light-theme variables; it is a starting palette, not a complete component library. In a governed design system, translate these roles into its vocabulary and apply changes within the authorized scope. Copy needed implementation assets into the project and keep their paths project-relative.

## The shared grammar

1. **Construction carries the poster character.** Use opaque white working surfaces over warm paper, thin dark outlines, small consistent radii, and purposeful internal divisions. Let geometry organize content. Avoid thick offset shadows or a separate frame around every fact.
2. **Keep expression outside repeated facts.** A broad entry composition can be bold; results, detail reading, forms, saved items, and account views need calmer density. Do not repeat a full-height marketing hero on every route.
3. **Use one color hierarchy.** Pink is the default primary-action accent; a lighter pink can mark a key fact such as salary. Dark selected filters are distinct from both. Yellow mainly belongs in illustrations. Do not import the turquoise CTA from the illustration source as a second primary-action system. An explicit product palette or user correction takes precedence.
4. **Use one neutral sans family.** Give personality to scale and composition, with a stronger weight for the primary object title. Do not automatically combine ABC Favorit with Poppins, or replace the direction with a decorative serif. Exact font choice remains open; retain a compatible existing family when possible.
5. **Illustrations are authored people, not background noise.** Use organic black contours, elastic silhouettes, meaningful activity, flat restrained fills, and generous clear space. The people and the UI share a palette; the UI keeps straight geometry. Place people at entry points, category orientation, or selected empty/confirmation states, rather than inside every result card.
6. **Compare information before images.** A visual-goods marketplace may need a gallery; a text-heavy job board normally needs wide rows. Role, company, salary/terms, location, and work mode keep stable positions. Logos stay small and have a meaningful fallback. Never require a decorative cover image for each role.
7. **Preserve full titles and truthful missing states.** Let long titles wrap rather than shrinking individual font sizes. Show explicit missing-data text. Keep contract and salary period attached to the amount. Group tags by relevance; do not let a tag cloud outrank the primary title.
8. **Translate the source to the product.** A salary can borrow a price label's visual emphasis, but source discounts, star ratings, urgency, subscriptions, and purchase behavior do not authorize inventing equivalents in recruitment or another domain. Preserve existing legitimate behavior and permission boundaries.

These are a chosen visual direction with practical implementation defaults, not official tokens from either source. Exact palette, type scale, geometry, mobile adaptations, and asset composition were proposed in the study; do not claim the user individually approved them. Make coherent choices within that direction and state consequential deviations briefly.

## Build the requested screen

Choose the composition from the task, not from the reference homepage:

| Task | Useful composition | Illustration role |
| --- | --- | --- |
| Invite and orient | Strong title, useful entry controls, early content | One human scene with a clear text zone |
| Compare results | Stable repeated rows; desktop filters where useful | Small orientation vignette or empty state |
| Evaluate a detail | Reading column plus facts/action panel | Optional subordinate accent |
| Understand an organization | Identity, facts, narrative, reused result cards | Platform art does not replace employer identity |
| Apply, edit, or configure | Compact task shell; grouped fields and feedback | Small purposeful state illustration, if useful |

On narrow screens, adapt the composition rather than scaling the desktop canvas. Text-heavy results use one column; filters become compact, facts remain near the title, and action placement respects keyboard and safe-area behavior. A small mobile vignette can retain character; the reference's hidden mobile hero is an observation, not a mandatory rule. A fixed action bar is optional and must be tested in the actual flow.

Deliver functioning controls for an implementation. If the requested artifact is only a visual study, label proposed states and noninteractive specimens clearly. Do not change domain behavior just to make a screenshot resemble the reference.

## Review the rendered result

Inspect the intended desktop layout and a narrow viewport, including lower content and a repeated dense component. Check the visual contract against the relevant bundled images: paper/white hierarchy, fine contour, small-radius geometry, action versus fact color, title prominence, and illustration placement.

Use real content where available. Include a long title with Polish diacritics when relevant, missing logo/salary, long locations, many tags, and enough varied repeated items to reveal density problems. For this direction, those cases should change wrapping and height, not force smaller type or horizontal page overflow.

Verify the controls and states the requested flow needs: focus, selected, disabled, loading, empty, validation error, recovery, and success. Review the semantic meaning separately from the visual accent. The source screenshots do not prove accessibility, conversion, animation, or complete mobile behavior.

Deliver the screen or implementation, briefly naming the choices that keep it in this family, what was actually checked, and any material gap. Do not claim application deployment or functionality from a static visual alone.
