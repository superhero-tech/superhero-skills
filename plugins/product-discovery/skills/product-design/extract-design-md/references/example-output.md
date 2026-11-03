# Example: sparse but honest output

This example describes the controlled test page used during development. It is not a palette or layout to reuse for other sites. Only write claims whose evidence exists in the current extraction.

```markdown
# Design: Test Store

Source: http://127.0.0.1:8765/fixture.html
Coverage: one page, desktop 1440×900 and mobile 390×844. Evidence: design-evidence/manifest.json.

## Style values

| Use | Value | Status | Evidence |
| --- | --- | --- | --- |
| Primary button background | rgb(37, 99, 235) | Measured | desktop-default.json, #primary-cta, backgroundColor |
| Primary button label | 16px, 600, line-height 24px; Arial, sans-serif | Measured CSS stack | desktop-default.json, #primary-cta |
| Button corners | 8px on all corners | Measured | desktop-default.json, #primary-cta |

## Visual character

Observed: the page groups products in bordered cards; desktop screenshot shows three columns. Mobile screenshot shows one column.

## Components and states

Primary button: use the measured blue background, white label, and 8px corners.
Hover: measured only if hover-button.json exists and reports :hover for #primary-cta.
Disabled: unverified; no disabled control was inspected.

## Responsive behavior

Measured: .product-grid has three columns at 1440px and one at 390px.
Declared CSS: (max-width: 600px), if the snapshot's declaredMediaQueries contains it.
The exact width at which the layout changes was not experimentally located.

## Guidance and gaps

Maintain the measured button and card styles. Do not introduce an additional brand accent without a product decision.
No success/error states were observed. The font stack was measured; the actual font file was not independently verified.
```
