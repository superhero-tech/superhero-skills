# Evidence format

Use relative paths from the evidence directory. Do not put credentials, cookies, browser storage, HTML dumps, or complete page text in artifacts. The extractor records only short labels useful for identifying samples; omit them on sensitive pages if not needed.

`design-evidence/manifest.json`:

```json
{
  "schemaVersion": "2.0",
  "snapshots": [
    {"id": "page-1-desktop-default", "path": "page-1-desktop-default.json"}
  ],
  "screenshots": [
    {"id": "page-1-desktop", "path": "page-1-desktop.png",
     "snapshotId": "page-1-desktop-default", "capture": "viewport"}
  ],
  "checks": [
    {"status": "passed", "kind": "comparison", "detail": "Primary button matches desktop screenshot"},
    {"status": "skipped", "kind": "hover", "detail": "Current integration does not expose pointer positioning"}
  ],
  "limitations": ["Only the supplied page was inspected"]
}
```

A raw snapshot from `extract-styles.js` includes:

- `schemaVersion`, `source` URL/title/date/viewport/fonts status, and `state` label plus matched pseudo-classes;
- `coverage` counts, sampling policy, limits, and explicit gaps;
- `elements`: stable selectors where possible, bounding boxes, short identifiers, semantic tag/role, and exact computed `styles`;
- `components`: candidate classifications referencing element IDs; candidates require visual review;
- `tokens`: frequency summaries with evidence references `{elementId, property}`;
- `cssVariables`: resolved root custom properties, when accessible;
- `assets`: rendered image URLs and inline-SVG candidates with their selectors; logo candidates are not confirmed logos;
- `declaredMediaQueries`: accessible CSS declarations, not verified breakpoint behavior.

Preserve modern colors (`oklch()`, `color()`, etc.), RGB/RGBA alpha, gradients, font stacks, and all four corner values. Do not normalize away information just to obtain six-digit HEX. If converting a value for convenience, retain the original and label the conversion.

The manifest can omit screenshots when unavailable, but `checks` and `limitations` must explain missing visual or viewport coverage. A failed or skipped probe is not a snapshot. Use unique IDs/filenames and include actual URL/viewport in each saved snapshot, including for redirects.

In `DESIGN.md`, cite a measurement with both file and selector, for example:

`Measured: 16px / 600; evidence: [desktop snapshot](design-evidence/page-1-desktop-default.json), #primary-cta, fontSize/fontWeight.`

The supplied validator checks manifest paths, snapshot structure, source references, component IDs, and whether token summaries equal their cited element properties. It cannot validate screenshot interpretation or whether an inference is justified; the agent must compare those explicitly.
