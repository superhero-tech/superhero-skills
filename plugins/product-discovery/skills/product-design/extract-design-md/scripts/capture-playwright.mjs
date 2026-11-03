#!/usr/bin/env node
// Optional fallback. Native browser tools are preferred; no app code is modified.
import {readFile, writeFile, mkdir, access} from 'node:fs/promises';
import path from 'node:path';

const [url, outputDirectory] = process.argv.slice(2);
if (!url || !outputDirectory) {
  console.error('Usage: capture-playwright.mjs <http(s)-url> <evidence-directory>');
  process.exit(2);
}
const target = new URL(url);
if (!['http:', 'https:'].includes(target.protocol) || target.username || target.password) {
  throw new Error('Use an HTTP(S) URL without embedded credentials.');
}
let chromium;
try { ({chromium} = await import(process.env.EXTRACT_DESIGN_PLAYWRIGHT_MODULE || 'playwright')); }
catch { throw new Error('Playwright is unavailable. Use the native browser or an existing runtime with playwright installed; no dependencies were changed.'); }
const output = path.resolve(outputDirectory);
await mkdir(output, {recursive: true});
const manifestPath = path.join(output, 'manifest.json');
try {
  await access(manifestPath);
  throw new Error('An evidence manifest already exists here; choose a new directory or deliberately merge reviewed artifacts.');
} catch (error) { if (error.code !== 'ENOENT') throw error; }
const expression = await readFile(new URL('./extract-styles.js', import.meta.url), 'utf8');
const manifest = {schemaVersion: '2.0', snapshots: [], screenshots: [], checks: [],
  limitations: ['One supplied URL, two sample widths; a starter style inventory, not a complete product system.', 'Theme variants are not captured automatically.']};
let browser;
try {
  browser = await chromium.launch({headless: true});
  const context = await browser.newContext({viewport: {width: 1440, height: 900}});
  const page = await context.newPage();
  await page.goto(target.href, {waitUntil: 'domcontentloaded', timeout: 30000});
  await page.locator('body').waitFor({state: 'visible', timeout: 10000});
  const fontReady = await page.evaluate(async () => {
    if (!document.fonts) return false;
    return Promise.race([document.fonts.ready.then(() => true), new Promise(resolve => setTimeout(() => resolve(false), 5000))]);
  });
  manifest.checks.push({kind: 'fonts-ready', status: fontReady ? 'passed' : 'skipped', detail: fontReady ? 'Font loading settled; actual rendered families remain unverified' : 'Font wait unavailable or exceeded 5 seconds'});
  async function capture(id, label) {
    const raw = await page.evaluate(expression);
    raw.state.label = label;
    raw.source.browser = 'standalone-playwright-chromium';
    await writeFile(path.join(output, id + '.json'), JSON.stringify(raw, null, 2) + '\n');
    manifest.snapshots.push({id, path: id + '.json'});
    await page.screenshot({path: path.join(output, id + '.png')});
    manifest.screenshots.push({id: id + '-screenshot', path: id + '.png', snapshotId: id, capture: 'viewport'});
    return raw;
  }
  const desktop = await capture('desktop-default', 'desktop-current');
  const candidates = [
    ['button', desktop.elements.find(el => el.componentKinds.includes('button') && !el.states.disabled)],
    ['field', desktop.elements.find(el => el.componentKinds.includes('field') && !el.states.disabled)]
  ];
  for (const [kind, candidate] of candidates) {
    for (const state of kind === 'button' ? ['hover', 'focus'] : ['focus']) {
      if (!candidate) {
        manifest.checks.push({kind: `${state}-${kind}`, status: 'skipped', detail: 'No rendered enabled candidate found'});
        continue;
      }
      try {
        const locator = page.locator(candidate.selector);
        if (state === 'hover') await locator.hover({timeout: 5000});
        else await locator.focus({timeout: 5000});
        const matched = await locator.evaluate((el, pseudo) => el.matches(':' + pseudo), state);
        if (!matched) throw new Error('Requested pseudo-class was not active');
        await capture(`desktop-${state}-${kind}`, `${state}: ${candidate.selector}`);
        manifest.checks.push({kind: `${state}-${kind}`, status: 'passed', detail: `Confirmed :${state} on ${candidate.selector}; focus-visible separately recorded in raw data`});
      } catch (error) {
        manifest.checks.push({kind: `${state}-${kind}`, status: 'skipped', detail: String(error.message)});
      }
    }
  }
  // Capture mobile in a clean isolated page so hover/focus do not contaminate it.
  const mobilePage = await context.newPage();
  await mobilePage.setViewportSize({width: 390, height: 844});
  await mobilePage.goto(target.href, {waitUntil: 'domcontentloaded', timeout: 30000});
  await mobilePage.locator('body').waitFor({state: 'visible', timeout: 10000});
  await mobilePage.evaluate(async () => { if (document.fonts) await Promise.race([document.fonts.ready, new Promise(resolve => setTimeout(resolve, 5000))]); });
  const mobile = await mobilePage.evaluate(expression);
  mobile.state.label = 'mobile-current';
  mobile.source.browser = 'standalone-playwright-chromium';
  await writeFile(path.join(output, 'mobile-default.json'), JSON.stringify(mobile, null, 2) + '\n');
  manifest.snapshots.push({id: 'mobile-default', path: 'mobile-default.json'});
  await mobilePage.screenshot({path: path.join(output, 'mobile-default.png')});
  manifest.screenshots.push({id: 'mobile-default-screenshot', path: 'mobile-default.png', snapshotId: 'mobile-default', capture: 'viewport'});
  console.log(`Saved ${manifest.snapshots.length} snapshots in ${output}. Review screenshots before writing DESIGN.md.`);
} catch (error) {
  manifest.checks.push({kind: 'capture', status: 'failed', detail: String(error.message)});
  if (!manifest.snapshots.length) process.exitCode = 1;
  console.error(`Capture incomplete: ${error.message}`);
} finally {
  if (browser) await browser.close();
  await writeFile(manifestPath, JSON.stringify(manifest, null, 2) + '\n');
}
