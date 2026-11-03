# Visual system

## Intent and evidence status

The selected combination is a poster-like marketplace interface with expressive drawn people. Gumroad supplies the interface construction; Work With Indies supplies the human illustration language. The study was completed on 2026-11-02.

Keep three categories separate:

- **Measured:** the CSS values below, for named source elements and captured states only.
- **Observed:** screenshot-visible anatomy, composition, and illustration characteristics.
- **Default / proposed:** our adapted system for building screens. These are usable starting decisions, not verified source tokens or individually approved user choices.

The screenshot index and provenance JSON retain URLs, actual viewport dimensions, timestamps, frame descriptions, and limitations. A font-family stack does not prove which font file rendered. Two viewport samples do not establish an exact breakpoint.

## Source measurements

| Source | Element / state | Measurement |
| --- | --- | --- |
| S03 Gumroad product | Main purchase link, default, 1280 × 720 | Background #ff90e8; black text; border 1px solid black; radius 4px; padding 12px 16px; text 16px/22px |
| S04 Gumroad storefront | First article, 1011 × 1177 | White; border 1px solid black; radius 4px; no shadow |
| S04 Gumroad storefront | First article h4, same viewport | ABC Favorit stack; 16px/22px; weight 400 |
| S02 Gumroad catalog | Body, 1280 × 720 | Background #f4f4f0; base text 16px/22px |
| S06 Work With Indies detail | h1, 1280 × 720 | Poppins stack; 36px/44px; weight 800 |
| S06 Work With Indies detail | First description paragraph | Poppins stack; 16px/24px; weight 300 |
| S11 Gumroad mobile detail | Product information region, purchase bar visible | position: fixed; bottom: 0px; inspected at 390 × 844 |

An earlier 1280 × 720 storefront frame measured its first title at 20px/28px, weight 400. S04's narrower frame measures 16px/22px. Preserve this variation as evidence, rather than claiming one official source scale.

## Implementation defaults

Use these when no existing compatible system or explicit user choice takes precedence. Define them once and reuse through semantic roles. The optional token file mirrors these defaults; it does not apply page or component styles automatically.

| Role | Starting value | Reason / adaptation |
| --- | --- | --- |
| Paper canvas | #f4f4f0 | Measured catalog ground, kept as a useful neutral |
| Working surface | #ffffff | Opaque cards, fields, reading and action panels |
| Ink / contour | #181818 | Adapted dark neutral; source contour was black |
| Secondary text | #5e5a5c | Proposed readable subordinate role; verify in context |
| Primary action | #ff90e8 with dark text | Source purchase accent, adapted to the product's primary action |
| Key-fact fill | #ffe0f7 | Proposed quieter pink, e.g. salary; do not make it compete with the CTA |
| Selected filter | Ink fill, white text | Proposed state distinct from pink fact and action roles |
| Illustration accent | Pink plus approximately #ffe45b | Yellow estimated from the people reference; keep out of competing primary actions |
| Border | 1px dark | Repeated source structure; increase only for a deliberate hierarchy |
| Card / control radius | 4px | Measured source starting point |
| Large panel radius | Up to 8px | Proposed adaptation, not a second unrelated corner language |
| Default shadow | None | Hierarchy through surface, line, and space |
| Focus | Visible 3px ink outline with offset | Proposed state; adapt to background and host-system focus patterns |

Do not give every category a new saturated card background. If categories need color, keep classification subordinate and distinct from selected state, action, error, or outcome. A business status must retain its label; color alone does not explain it.

The light direction is specified here. For an existing dark mode, create a coherent semantic mapping when in scope; do not silently remove the mode, apply light literal values to dark text roles, or claim a dark system was studied.

## Typography and rhythm defaults

One neutral sans family with complete locale coverage is enough. Use a compatible existing product family. In an unbranded prototype, system-ui is a dependency-free starting choice; it is not the source font. No font files or licenses are bundled.

| Role | Starting size / line height | Weight |
| --- | --- | --- |
| Entry display | 56–64 / 60–68 desktop; 36–40 / 40–44 narrow | Choose for the family and available line length |
| Page / detail title | 32–40 / 38–46 desktop; 28–32 / 34–38 narrow | 600 or appropriate family equivalent |
| Result title | 20 / 26 desktop; 19–20 / 25–26 narrow | 600 |
| Body | 16 / 24 | 400 |
| Facts / labels | 14 / 20 | 400–600 according to role |
| Small tags | 12–13 / 18–20 | 400–500; avoid making essential facts this small |

Useful starting rhythm: 20–24px card padding, 12–16px between result cards, 8–12px between related facts. Use the host system's nearest coherent steps when it already defines spacing. Do not independently tighten one long title to align card heights.

## Component grammar

### Result / role card

Three semantic zones: small object identity, dominant title with nearby facts, and key terms/action. On a job board:

1. Company name and small logo or initials.
2. Full role title.
3. Location, work mode, seniority and contract where provided.
4. Salary range with period and contract-specific interpretation; a quieter pink label can help.
5. A visible, labeled route to the detail; keep save as a separate control if that behavior exists.

A wide desktop row can put salary/action in an end column. On narrow screens, stack terms under title/facts, keeping a stable reading order. Use one outer contour and at most a useful divider between semantic zones as a starting point. A literal ribbon notch is optional; a plain filled label can express the same hierarchy more reliably with long content.

Explicitly show missing information. Do not fill unavailable salary with an invented estimate, a zero, or a promotional-looking blank ribbon. Long titles wrap fully; long company/location text can gain another line. Tags are optional and subordinate: limit or prioritize them according to product needs rather than inheriting the study's many-tag stress case as a requirement.

### Controls and forms

Use the same small-radius geometry, dark edge, measured heights, label alignment, and padding across adjacent fields and buttons. Native project components remain authoritative. Selected filters, active navigation and a primary CTA need separate, legible signals.

Group fields by task, use persistent labels, keep helper and error text near its field, and expose one clear next action. Preserve entered data through recoverable errors where the product supports it. A borrowed Typeform introduction in S13 is an exception in the source, not a second form design system to imitate.

### Detail and action panels

Keep long reading content dominant; group key facts and the action in a supporting panel. The panel can repeat the card's contour and salary emphasis without repeating a giant illustration.

A mobile bottom action is an optional adaptation from S11. Inspect its visibility rules, keyboard, safe area, content overlap, expired/unavailable states and role/session logic in the actual product. A static screenshot is insufficient validation.

### Expression and imagery

The organic person and the straight card are complementary. Do not make controls hand-wobbled to match the drawing. Source character colors are not all UI colors. Use original illustration, a clear text zone, and consistent palette handling; see the dedicated brief.

## Recognizable drift

Correct drift when the screen becomes a generic soft dashboard: oversized pill cards, gradients on every surface, glass/translucent panels, repeated stock portraits, painted nature margins, or a decorative serif replacing the neutral sans. Also correct the opposite extreme: thick hard shadows, black boxes around every label, and loud illustration on every result.

The desired identity should survive removal of large artwork: paper, precise contours, information rhythm, pink action and fact hierarchy. When artwork is present, it adds human energy without carrying the only recognizable part of the design.
