(() => {
  'use strict';
  // Read-only expression: suitable for a browser evaluation API, no imports.
  const MAX_ELEMENTS = 400;
  const MAX_VARIABLES = 100;
  const MAX_ASSETS = 60;
  const styleCache = new Map();
  const styleOf = el => {
    if (!styleCache.has(el)) styleCache.set(el, getComputedStyle(el));
    return styleCache.get(el);
  };
  const all = Array.from(document.querySelectorAll('body *'));
  const visible = el => {
    if (['SCRIPT', 'STYLE', 'TEMPLATE', 'NOSCRIPT'].includes(el.tagName)) return false;
    const rect = el.getBoundingClientRect();
    if (rect.width <= 0 || rect.height <= 0 || !el.getClientRects().length) return false;
    const s = styleOf(el);
    if (s.visibility === 'hidden' || s.visibility === 'collapse') return false;
    for (let p = el; p; p = p.parentElement) {
      const ps = styleOf(p);
      if (ps.display === 'none' || ps.contentVisibility === 'hidden' || Number(ps.opacity) === 0) return false;
    }
    return true;
  };
  const visibleElements = all.filter(visible);
  const cssEscape = value => typeof CSS !== 'undefined' && CSS.escape
    ? CSS.escape(value) : String(value).replace(/[^a-zA-Z0-9_-]/g, c => '\\' + c);
  const selectorFor = el => {
    const parts = [];
    let node = el;
    while (node && node.nodeType === 1) {
      if (node.id) {
        const idSelector = '#' + cssEscape(node.id);
        if (document.querySelectorAll(idSelector).length === 1) {
          parts.unshift(idSelector);
          break;
        }
      }
      const tag = node.tagName.toLowerCase();
      const siblings = node.parentElement
        ? Array.from(node.parentElement.children).filter(sib => sib.tagName === node.tagName) : [node];
      parts.unshift(siblings.length > 1 ? `${tag}:nth-of-type(${siblings.indexOf(node) + 1})` : tag);
      node = node.parentElement;
    }
    return parts.join(' > ');
  };
  const componentKinds = el => {
    const kinds = [];
    const tag = el.tagName.toLowerCase();
    const role = el.getAttribute('role');
    const s = styleOf(el);
    if (tag === 'button' || role === 'button' || (tag === 'a' && (s.backgroundColor !== 'rgba(0, 0, 0, 0)' || /button|btn|cta/i.test(el.className || '')))) kinds.push('button');
    else if (tag === 'a') kinds.push('link');
    if (['input', 'textarea', 'select'].includes(tag) || ['textbox', 'combobox'].includes(role)) kinds.push('field');
    if (tag === 'nav' || role === 'navigation') kinds.push('navigation');
    const rect = el.getBoundingClientRect();
    const border = ['Top', 'Right', 'Bottom', 'Left'].some(side => Number(s['border' + side + 'Width'].replace(/px$/, '')) > 0 && s['border' + side + 'Style'] !== 'none');
    if (!['body', 'html', 'img', 'svg', 'button', 'input', 'textarea', 'select', 'a'].includes(tag)
      && rect.width * rect.height >= 10000 && (border || s.boxShadow !== 'none')) kinds.push('card-candidate');
    return kinds;
  };
  const priority = visibleElements.filter(el => componentKinds(el).length
    || /^H[1-6]$/.test(el.tagName) || ['IMG', 'svg', 'P', 'MAIN', 'HEADER', 'FOOTER'].includes(el.tagName));
  // Reserve half the sample for structured controls/text/assets, then sample the page.
  const chosen = new Set(priority.slice(0, Math.floor(MAX_ELEMENTS / 2)));
  const slots = MAX_ELEMENTS - chosen.size;
  const remainder = visibleElements.filter(el => !chosen.has(el));
  const stride = Math.max(1, Math.ceil(remainder.length / slots));
  for (let i = 0; i < remainder.length && chosen.size < MAX_ELEMENTS; i += stride) chosen.add(remainder[i]);
  const sampled = visibleElements.filter(el => chosen.has(el));
  const properties = [
    'color', 'backgroundColor', 'backgroundImage', 'opacity',
    'fontFamily', 'fontSize', 'fontWeight', 'fontStyle', 'lineHeight', 'letterSpacing', 'textTransform', 'textAlign',
    'paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft',
    'marginTop', 'marginRight', 'marginBottom', 'marginLeft', 'rowGap', 'columnGap',
    'borderTopLeftRadius', 'borderTopRightRadius', 'borderBottomRightRadius', 'borderBottomLeftRadius',
    'boxShadow', 'backdropFilter', 'outlineColor', 'outlineStyle', 'outlineWidth', 'outlineOffset',
    'display', 'position', 'width', 'height', 'maxWidth', 'minWidth', 'gridTemplateColumns', 'gridTemplateRows',
    'flexDirection', 'flexWrap', 'alignItems', 'justifyContent', 'objectFit', 'aspectRatio',
    'transitionProperty', 'transitionDuration', 'transitionTimingFunction',
    'animationName', 'animationDuration', 'animationTimingFunction'
  ];
  for (const side of ['Top', 'Right', 'Bottom', 'Left']) {
    for (const prop of ['Color', 'Width', 'Style']) properties.push('border' + side + prop);
  }
  const tokenMaps = {colors: {}, spacing: {}, radius: {}, shadows: {}, typography: {}};
  const addToken = (kind, value, id, property) => {
    if (!value) return;
    const bucket = tokenMaps[kind];
    if (!bucket[value]) bucket[value] = {value, count: 0, evidence: []};
    bucket[value].count++;
    if (bucket[value].evidence.length < 3) bucket[value].evidence.push({elementId: id, property});
  };
  const elements = sampled.map((el, i) => {
    const s = styleOf(el);
    const id = 'e' + (i + 1);
    const rect = el.getBoundingClientRect();
    const styles = Object.fromEntries(properties.map(prop => [prop, s[prop] || '']));
    for (const prop of ['color', 'backgroundColor', 'borderTopColor', 'borderRightColor', 'borderBottomColor', 'borderLeftColor']) {
      addToken('colors', styles[prop], id, prop);
    }
    for (const prop of properties.filter(p => /^(padding|margin)|Gap$/.test(p))) {
      if (!['0px', 'normal', ''].includes(styles[prop])) addToken('spacing', styles[prop], id, prop);
    }
    for (const prop of properties.filter(p => /Radius$/.test(p))) addToken('radius', styles[prop], id, prop);
    if (s.boxShadow !== 'none') addToken('shadows', s.boxShadow, id, 'boxShadow');
    const ownText = Array.from(el.childNodes).some(n => n.nodeType === 3 && n.textContent.trim());
    if (ownText || ['input', 'textarea', 'select', 'button'].includes(el.tagName.toLowerCase())) {
      const typeStyle = Object.fromEntries(['fontFamily', 'fontSize', 'fontWeight', 'fontStyle', 'lineHeight', 'letterSpacing', 'textTransform'].map(p => [p, styles[p]]));
      const key = JSON.stringify(typeStyle);
      const bucket = tokenMaps.typography;
      if (!bucket[key]) bucket[key] = {value: typeStyle, count: 0, evidence: []};
      bucket[key].count++;
      if (bucket[key].evidence.length < 3) bucket[key].evidence.push({elementId: id, properties: Object.keys(typeStyle)});
    }
    return {
      id, selector: selectorFor(el), tag: el.tagName.toLowerCase(), role: el.getAttribute('role'),
      label: (el.getAttribute('aria-label') || el.getAttribute('alt') || (ownText ? el.textContent : '') || '').trim().slice(0, 80),
      componentKinds: componentKinds(el),
      states: {hover: el.matches(':hover'), focus: el.matches(':focus'), focusVisible: el.matches(':focus-visible'), disabled: el.matches(':disabled')},
      rect: {x: rect.x, y: rect.y, width: rect.width, height: rect.height}, styles
    };
  });
  const limitations = [
    'Top document only: iframe contents, shadow-root descendants, and pseudo-element styles are not extracted.',
    'Only currently rendered elements are sampled; lazy/unvisited content and unmeasured states are not covered.',
    'Font families are computed CSS stacks, not verified rendered font files.',
    'Token frequencies count sampled CSS property occurrences, not brand importance or a proven design scale.',
    'Only root-level custom properties are collected; local component variables may be absent.'
  ];
  if (sampled.length < visibleElements.length) limitations.push(`Sampled ${sampled.length} of ${visibleElements.length} rendered elements.`);
  const cssVariables = {};
  let variableCount = 0;
  try {
    const root = getComputedStyle(document.documentElement);
    for (let i = 0; i < root.length; i++) {
      const name = root.item(i);
      if (name.startsWith('--')) {
        variableCount++;
        if (Object.keys(cssVariables).length < MAX_VARIABLES) cssVariables[name] = root.getPropertyValue(name).trim();
      }
    }
  } catch (e) { limitations.push('Root CSS variables unavailable: ' + String(e.message || e)); }
  if (variableCount > MAX_VARIABLES) limitations.push(`Root CSS variables truncated to ${MAX_VARIABLES} of ${variableCount}.`);
  const media = new Set();
  let inaccessibleSheets = 0;
  const walkRules = rules => {
    for (const rule of Array.from(rules)) {
      if (rule.media && rule.media.mediaText) media.add(rule.media.mediaText);
      if (rule.cssRules) walkRules(rule.cssRules);
    }
  };
  try {
    for (const sheet of Array.from(document.styleSheets)) {
      try { walkRules(sheet.cssRules); } catch (_) { inaccessibleSheets++; }
    }
  } catch (_) { limitations.push('Stylesheet declarations unavailable in this evaluation scope.'); }
  if (inaccessibleSheets) limitations.push(`${inaccessibleSheets} stylesheet(s) could not be inspected for media declarations.`);
  const assetElements = visibleElements.filter(el => ['img', 'svg'].includes(el.tagName.toLowerCase()));
  const assets = assetElements.slice(0, MAX_ASSETS).map(el => {
    const selector = selectorFor(el);
    const tag = el.tagName.toLowerCase();
    const name = el.getAttribute('alt') || el.getAttribute('aria-label') || '';
    const src = tag === 'img' ? (el.currentSrc || el.src || '') : null;
    const hint = [name, el.id, el.getAttribute('class'), src].join(' ');
    return {selector, kind: tag === 'img' ? 'image' : 'inline-svg', sourceUrl: src,
      label: name.slice(0, 80), logoCandidate: /logo|brandmark|wordmark/i.test(hint),
      viewBox: tag === 'svg' ? el.getAttribute('viewBox') : null,
      renderedWidth: el.getBoundingClientRect().width, renderedHeight: el.getBoundingClientRect().height,
      objectFit: styleOf(el).objectFit || '', confirmedLogo: false};
  });
  if (assetElements.length > MAX_ASSETS) limitations.push(`Assets truncated to ${MAX_ASSETS} of ${assetElements.length}.`);
  const tokens = Object.fromEntries(Object.entries(tokenMaps).map(([kind, bucket]) =>
    [kind, Object.values(bucket).sort((a, b) => b.count - a.count)]));
  const bodyStyles = styleOf(document.body);
  const fontStatus = (() => { try { return document.fonts.status; } catch (_) { return 'unavailable'; } })();
  return {
    schemaVersion: '2.0',
    source: {url: document.location.href, title: document.title, extractedAt: new Date().toISOString(),
      viewport: {width: window.innerWidth, height: window.innerHeight, devicePixelRatio: window.devicePixelRatio},
      fontsStatus: fontStatus, documentReadyState: document.readyState},
    state: {label: 'observed-current', activeElementSelector: document.activeElement && document.activeElement !== document.body ? selectorFor(document.activeElement) : null},
    coverage: {scope: 'top-document', totalElements: all.length, renderedElements: visibleElements.length,
      sampledElements: elements.length, maxElements: MAX_ELEMENTS, sampling: 'semantic-priority plus evenly distributed remainder',
      inaccessibleStylesheets: inaccessibleSheets, limitations},
    pageSurface: {selector: 'body', color: bodyStyles.color, backgroundColor: bodyStyles.backgroundColor, backgroundImage: bodyStyles.backgroundImage, fontFamily: bodyStyles.fontFamily},
    elements,
    components: elements.filter(el => el.componentKinds.length).map(el => ({elementId: el.id, kinds: el.componentKinds})),
    tokens, cssVariables, assets, declaredMediaQueries: Array.from(media)
  };
})()
