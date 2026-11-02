# Reviewable HTML deliverables

Use before creating or updating the moodboard or deeper study.

## Artifact structure

Honor the requested location and existing project conventions. Otherwise use a dedicated task output folder, for example:

- moodboard.html
- direction-study.html
- evidence/manifest.json
- evidence/screenshots/...
- evidence/styles/... when exact values were inspected

Names are examples, not fixed requirements. Preserve the comparison when producing the final study. Do not save user deliverables in the installed skill directory.

Produce a complete standalone HTML document. Prefer embedding images to make the file portable; retain original screenshot files and their source records for traceability. Do not require a running server, remote APIs, hotlinked thumbnails, or a visualization-specific host runtime for ordinary viewing.

A visual-direction report should be composed for comparison: large enough evidence, deliberate typography, clear section hierarchy, and concise annotations. Let examples dominate the moodboard. Let the evidence-to-decision chain organize the deep study. Do not use the report's editorial styling as evidence of the researched site's direction.

Each screenshot/crop needs an accessible label, stable ID, and a way to reach the original full screen and source URL. Keep URLs and capture dates available without hover. Distinguish original screenshots from authored sketches or component studies.

## Evidence record

A lightweight manifest may use this shape; adapt to the available tools:

    {
      "screens": [
        {
          "id": "source-a-list-desktop",
          "site": "Source A",
          "url": "https://example.com/list",
          "captured_at": "actual capture time",
          "page_type": "listing",
          "frame": "viewport, top",
          "viewport_css_px": {"width": 1440, "height": 900},
          "state": "default",
          "screenshot": "screenshots/source-a-list-desktop.jpg",
          "limitations": []
        }
      ]
    }

Record unknown viewport dimensions as unknown rather than substituting the screenshot's pixel size; device pixel ratio may differ. Store crop bounds and the parent screen ID. Attach measured styles to the relevant screen/element/state. Identify archive dates separately from capture dates.

## Interaction and accessibility

Use interactions that help review: expand a screenshot, navigate to evidence, filter reference families, or compare choices. Primary findings must remain readable without interacting. Do not add nonfunctional controls.

Use semantic headings, native buttons/selects, meaningful alt text, visible keyboard focus, and labeled dialogs. Close lightboxes with the normal dialog controls and Escape. Maintain readable contrast and touch targets. Support narrow widths by stacking analysis panels; use a contained horizontal scroller only where a genuine table needs it.

A brief builder is optional. Label its defaults as proposals; changing it must not silently create approved decisions or write external records. For a static report, a clear decision table is sufficient.

## Verification before delivery

Inspect the actual saved artifact in a supported browser. Check:

- Every evidence image is present, loaded, and correctly labeled; crops show the cited detail.
- Figures preserve legible proportions. No stretched long-page thumbnails masquerading as readable evidence.
- Source and internal links point to the intended screen; no duplicate IDs.
- Tables have actual cells for every value, matching their headers. Browser recovery can silently move malformed table text outside the table.
- Body text, tables, captions, and lower sections do not overlap, clip, or overflow at desktop and a narrow width.
- Lightbox open/close, filters, selectors and brief updates work when included.
- Original screenshots contain neither loading skeletons nor obstructing/transient overlays used as design evidence.
- Relevant claims agree with what the images and any measured values actually show.

Read scripts/inspect-html.js and run its single read-only expression through the browser's documented evaluation API where supported. It returns structural diagnostics for the currently rendered artifact. Inspect every reported issue; it is not a pass/fail accessibility audit and does not prove content accuracy or visual quality.

After a fix, rebuild the standalone HTML if generated from templates and recheck the affected section. Verify the deliverable itself rather than only its source template. Keep changes focused when the user reports an issue.

## PDF handoff

Offer PDF after delivering the final direction study, not before the user has chosen a direction. If requested, preserve source HTML, provide print-specific layout, resolve interactive-only content into visible static content, and inspect all PDF pages after rendering. Verify whole-screen figures, detail crops, tables, text glyphs, and section transitions. Use the available PDF skill when present.
