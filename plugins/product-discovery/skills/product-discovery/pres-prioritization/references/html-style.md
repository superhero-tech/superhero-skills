# Default HTML visual style

Use this style for every HTML artifact from this skill, both standalone and within a discovery process, unless the user explicitly requests another style. This is a presentation contract; preserve evidence, language, decisions and method-specific interactions.

- SF Pro regular (400) and medium (500), with native Apple/system sans-serif fallback. Letter spacing: -0.15px. Do not download or bundle an unavailable font.
- Text sizes: 12px for metadata/navigation, 13px for body/UI, 14px for card titles/emphasis, 24px for page/detail titles. Create hierarchy with weight, spacing and color rather than additional sizes.
- Text hierarchy: #292929 primary, #5D5D5D secondary, #9E9E9E metadata. White/light neutral surfaces and subtle gray borders; solid CTA text may be white. Keep critical instructions and controls in the darker tiers.
- Navigation icons: 14px. Card icons: 20px. Use local inline SVG when icons are useful; no icon CDN or required remote font.
- Radii: 8px navigation/controls, 16px cards, fully rounded pill CTAs and status badges.
- Distinguish an explicitly selected opportunity with a strong frame or clear status label. A recommendation needs a separate treatment (for example a dashed frame and status text); never imply human selection through recommendation styling. Sorting or inspecting a candidate must preserve actual scores, review status and selections.
- Adapt composition to the artifact: evidence map, chart/report, comparison and tree may use different layouts. Keep concise previews and link to full source context where appropriate.
- Charts may retain meaningful categorical or sequential color encodings with labels; use the shared neutral UI around them. Do not change data, quotes or review status while applying style.

## Packaged stylesheet

Use `assets/html-style.css` as the base and inline it into the final HTML. It provides typography, color and component tokens. This skill has no bundled HTML renderer; build a comparison view from the saved scorecard and inline the stylesheet. Override the base only for an explicit user style request. Keep artifacts self-contained, responsive and usable by keyboard, with print styles and no runtime network dependency.

Each standalone skill carries its own matching copy, so selective distribution works without a neighboring skill, project folder or plugin-wide runtime. When updating the shared design, keep those copies synchronized. No client data belongs in these resources.

Check the actual generated output for the typography/color/radius tokens, preserved content and interactions, and no external runtime. Perform visual review in the host's built-in browser when available, respecting the skill's preview and policy rules; never claim a preview was verified when it was blocked.
