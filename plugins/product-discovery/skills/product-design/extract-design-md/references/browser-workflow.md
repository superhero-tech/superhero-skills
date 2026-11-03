# Browser workflow and adapters

Read this when choosing tools or collecting browser evidence. Use the environment's documented API, not a fixed list of MCP tool names. Do not silently replace a user's chosen browser.

## Capability check

Navigate to the supplied page and find a visible heading, link, or control. Probe a read-only function such as:

```javascript
() => {
  const el = document.querySelector('h1') || document.querySelector('button, a');
  if (!el) return {supported: false, reason: 'No representative element'};
  const s = getComputedStyle(el);
  return {supported: true, color: s.color, fontFamily: s.fontFamily,
    fontSize: s.fontSize, fontWeight: s.fontWeight, lineHeight: s.lineHeight};
}
```

Separately establish whether screenshots can be saved and the viewport can be controlled. A successful CSS probe does not imply hover, arbitrary JavaScript, filesystem access, or device emulation is available. If evaluation is read-only, keep it read-only. The extractor never creates elements, writes attributes, fetches resources, or changes storage.

## Desktop Codex

Use the current computer/browser tool instructions to select the in-app browser. Supported versions expose read-only evaluation, DOM snapshots, screenshots, viewport capabilities, and page assets. Read their current capability documentation before calling them. Evaluate the expression from `scripts/extract-styles.js`, then persist its JSON using normal file tools. Confirm important interaction states in the returned evidence. Do not enable full CDP access to compensate for an unsupported operation; use supported tools, mark the gap, or use an authorized fallback.

## Claude Code desktop and browser integrations

Use the existing Browser tools; discover their current contracts. Desktop Browser can inspect DOM, capture screenshots, and interact with external sites. Verify exact computed-style extraction rather than assuming that DOM inspection supplies it. In CLI environments an existing Claude in Chrome or other browser integration may provide the needed capabilities. Do not require it to be installed if the available tools already work.

## Standalone Playwright fallback

Use this when the native tools are unavailable, cannot produce needed evidence, or the user chooses a script workflow. Use an existing supported runtime and browser installation first. `scripts/capture-playwright.mjs` is a narrow fallback, not an app modifier:

```bash
node scripts/capture-playwright.mjs https://example.com /absolute/project/design-evidence
```

It requires the `playwright` package and its Chromium binary. If the environment provides a bundled package outside ordinary module resolution, set `EXTRACT_DESIGN_PLAYWRIGHT_MODULE` to its documented absolute module entry path. If dependencies are missing, report what is missing and follow the environment's dependency/installation rules; do not install globally or change the app's dependencies automatically. It captures a single URL at 1440×900 and 390×844, with raw data and viewport screenshots. It also attempts a real hover and focus for a primary control and a field, and records skipped probes. Programmatic focus is not proof of keyboard focus-visible; that is recorded independently. Use supported site controls for dark mode separately; the fallback does not invent a theme toggle. For multiple supplied pages use distinct evidence directories or merge uniquely named records into one manifest.

## Readiness and state handling

- Wait for the main content and `document.fonts.ready` through supported mechanisms. Do not wait forever for `networkidle` on pages with continuous traffic. The fallback bounds its font wait and records the status.
- Treat transient overlays as context: dismiss through supported UI when appropriate and explain persistent obstruction.
- A pseudo-class match such as `:hover` or `:focus-visible` confirms a state; simply finding a transition in CSS does not.
- Recollect measurements at each width. Report observed changes and sampling widths; record an exact breakpoint only when accessible CSS declares it, and distinguish declarations from verified behavior.
- Restore the viewport and actual initial site theme. In a fallback's isolated browser, close the context/browser even after failure. Do not change stored preferences in an existing user session just for extraction.
- Top-document extraction may miss iframe contents, shadow DOM, pseudo-elements, lazy content, local CSS variables, or protected stylesheets. Record these gaps. Do not claim hidden/unvisited content was inspected.

## Sources for capability descriptions

- Codex desktop: https://learn.chatgpt.com/docs/browser
- Claude Code desktop: https://code.claude.com/docs/en/desktop#browse-external-sites
- Claude in Chrome: https://code.claude.com/docs/en/chrome
- Playwright: https://playwright.dev/docs/evaluating and https://playwright.dev/docs/emulation

These describe capabilities, not guarantees about the user's installed version. The live probe remains authoritative.
