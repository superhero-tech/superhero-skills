# PDF export

Use this reference when the user requests a PDF of the Supersprint tree or a shareable explanation of how its cards connect.

```sh
python3 <skill-directory>/scripts/render_tree.py <cycle>/state.json --output <cycle>/tree/tree.html --pdf
```

This refreshes HTML and Mermaid and creates sibling `tree.pdf`. The HTML includes a localized Download PDF link only when the PDF was generated in this run. Rerender with `--pdf` after changes so the download stays current. State, source files, reviews and selections are not modified. Existing snapshot rules still apply when `--snapshot` is also supplied.

## Default: original tree followed by compact tables

Start the document with the original tree on its own graph-sized vector page; follow it with the stage tables. Preserve the diagram and shorten only its accompanying documentation. Do not add a separate cover or a repeated node-by-node essay. Do not replace signal cards with ID-only chips, simplify the tree into a different map, or force the diagram onto A4/A3.

1. **Original vector tree:** retain Goal -> Signals -> Opportunities -> Ideas -> Tests/experiments, then actual Results/Decision when present. Keep full cards with IDs, titles, summaries and statuses, the original branch layout, stage colors, elbow connectors and selection/recommendation frames. Use a graph-sized page and allow zooming instead of replacing signal cards with IDs. The diagram does not group or duplicate signals by opportunity. Clicking a card opens its register entry; the goal links to its source.
2. **A4 landscape registers:** keep each stage in a table with ID, full title and compact relationship chains (`preceding IDs > this ID > following IDs`). Repeat column headers on continued pages. Shared signals list every supported opportunity. A trailing `-` on a signal marks a missing direct opportunity link. Show a common stage status once; retain individual statuses where they differ and preserve selections/recommendations. IDs open the full source artifacts.
3. **Keep the report short:** full titles and exact ID mappings replace repeated descriptions of every edge. Do not copy preview blocks or full test protocols by default. All cards, alternatives and visible relationships remain represented; detailed explanations are available through the source links. Let actual content determine pagination rather than enforcing a fixed page count.

The tree retains its original card text size; the registers remain readable on standard A4 landscape pages. Never shrink or silently omit cards to fit a fixed page. Reject graph pages beyond the portable PDF size limit. An empty cycle shows its unknown context explicitly.

## Optional: full description catalogue

Use this only when the user explicitly requests every preview explanation and a complete description catalogue:

```sh
python3 <skill-directory>/scripts/render_tree.py <cycle>/state.json --output <cycle>/tree/tree.html --pdf --pdf-layout full
```

Full mode includes product context, a graph-sized vector page and A4 node descriptions, preview blocks, statuses, sources and per-edge explanations. It can be substantially longer; it is not the default. Both modes use the same normalized graph and visible relationships. Goal context does not prove causal impact. Neither mode restores legacy Signal -> Experiment or Goal -> Opportunity bypasses.

## Runtime and checks

`scripts/export_pdf.py` requires ReportLab in the Python environment used for the command. HTML/Mermaid export does not require it. Prefer the host's bundled environment; otherwise install ReportLab in a suitable environment. Use a TTF font covering the cycle's language; supply `--pdf-font /path/to/font.ttf` if automatic detection fails. Other languages can supply the exporter's `pdf_*` and `pdf_compact_*` labels through `tree_ui`.

Before delivery, extract text to check IDs, characters and mapping coverage. Render pages and inspect the map, continued tables and later pages for clipping, overlaps, tiny text or unnecessary empty pages. Check internal navigation and source links. Do not claim visual verification from text extraction alone. Check that the cycle state and statuses did not change.
