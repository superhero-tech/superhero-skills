---
name: extract-design-md
description: Inspect the rendered style of supplied website URLs and create an evidence-backed DESIGN.md for building matching prototypes. Use for extracting a site's visual language, design tokens, typography, or component styling; not for implementing or redesigning the site.
---

# Extract Design MD

Create a practical `DESIGN.md` from measured browser styles and visual observations. Document the pages and states actually inspected; a page sample is not a complete product design system. Preserve exact values, distinguish inference, and report gaps instead of promising pixel-perfect reproduction.

## Inputs and tools

Use the URL(s) and output directory supplied by the user. Default output is the current project's root. Ask only for missing information that prevents useful work. Inspect existing output before replacing it; preserve unrelated project files.

Prefer the agent's available built-in browser. In desktop Codex use the in-app browser; in Claude Code desktop use Browser. In other environments use an available browser integration. Tool names and capabilities vary: read the current browser instructions, then follow [references/browser-workflow.md](references/browser-workflow.md).

Probe read-only computed-style access, screenshot support, and viewport control. Use only supported capabilities; never assume a DOM snapshot contains CSS or an integration exposes full Playwright. If needed, use the standalone Playwright fallback described in the reference. Do not require Chrome DevTools MCP, install a new integration, or enable full debugging access merely to inspect ordinary styles. Respect the user's browser choice and environment restrictions.

## Workflow

1. **Inspect the rendered page.** Wait for meaningful content and fonts using supported readiness checks. Resolve loading overlays or cookie notices when appropriate. On an authentication wall, ask the user to sign in through the supported flow. Do not describe the login page as the requested product. Stop retrying a persistent navigation failure; explain it and retain successful measurements from other requested pages.
2. **Collect evidence.** Read `scripts/extract-styles.js`: its single self-contained expression can be passed to the browser's read-only evaluation API. It returns a JSON-serializable snapshot with exact CSS values, element selectors, component candidates, assets, counts, and limitations. Set `state.label` to the state actually observed. Start with a desktop viewport; default test widths are 1440 and 390 CSS px if supported. These are sampling widths, not inferred breakpoints. When an API cannot run the expression, adapt only the browser adapter or collect a smaller supported sample and disclose that limitation.
3. **Capture screenshots and variants.** Save screenshots for the measured desktop and mobile states. Inspect the top and lower page regions when that adds meaningful coverage. Sample a representative primary button or link and a form field when present. Observe hover/focus through supported interaction tools, confirm the state, then remeasure the target. Record unavailable states as unverified. Inspect dark mode only through a genuine site control or supported color-scheme emulation, and verify that it changes the page. Do not inject `.dark` or mutate the page to fabricate a variant. Restore temporary viewport, theme, scroll, and interaction changes in a `finally`/cleanup step, including after errors. Do not submit forms or alter account settings to obtain visual states.
4. **Save raw artifacts.** Store each successful snapshot and screenshot under `design-evidence/`, using distinct page/viewport/state names. Maintain `design-evidence/manifest.json` using [references/evidence-format.md](references/evidence-format.md). Record skipped or failed measurements and their reasons; never label a screenshot-only result as an exact measurement. Prefer viewport screenshots where the API supports only those; record whether a capture covers the viewport or full page. Download logo files only if requested or materially useful and supported; source URLs and inline-SVG selectors suffice by default.
5. **Synthesize the document.** Follow [references/design-md-format.md](references/design-md-format.md) and its [example](references/example-output.md). Classify claims as **Measured**, **Observed**, **Inferred**, or **Unverified** and link to their evidence. Functional names must follow observed usage, not color-frequency rankings. Font stacks do not prove which font file rendered. Mobile layouts at two widths do not reveal an exact breakpoint. Keep unknowns explicit. Describe only supported components, variants, logos, motion, and functional colors; omit absent optional sections. A working CSS transition is measured configuration, not proof of every interaction state.
6. **Validate and report.** Check [evals/structural-check.md](evals/structural-check.md) and [evals/language-check.md](evals/language-check.md), and run `python3 scripts/validate-evidence.py <design-evidence-directory>` where available. Compare representative document values against raw snapshots and screenshots; repair discrepancies and unsupported claims. Report the saved document, coverage, and material gaps. Validation checks evidence consistency, not visual fidelity by itself.

## Output boundaries

- The main deliverable is `DESIGN.md`, plus raw snapshots, screenshots, and an evidence manifest. Generate token CSS only when requested; do not overwrite or import app styles as part of extraction.
- Use the user's language for the document. Prefer concise descriptions, exact CSS values, and tables. CSS names are allowed; metaphors and descriptive color names are optional.
- Do not invent minimum numbers of colors, fonts, components, or sections. Transparent, modern CSS color functions, gradients, and asymmetric shapes must retain their actual values.
- Partial evidence is useful when clearly scoped. Unobserved success/error states, disabled styles, assets, or responsive thresholds remain unverified.
