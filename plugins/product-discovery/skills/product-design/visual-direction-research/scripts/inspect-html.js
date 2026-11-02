(() => {
  const ids = new Map();
  document.querySelectorAll('[id]').forEach(el => ids.set(el.id, (ids.get(el.id) || 0) + 1));
  const visible = el => Boolean(el.getClientRects().length);
  const images = [...document.querySelectorAll('img')].map((el, index) => ({
    index, alt: el.getAttribute('alt'), complete: el.complete,
    loaded: el.complete && el.naturalWidth > 0,
    visible: visible(el), inViewport: visible(el) && el.getBoundingClientRect().bottom > 0
      && el.getBoundingClientRect().top < innerHeight, lazy: el.loading === 'lazy'
  }));
  const tables = [...document.querySelectorAll('table')].map((table, index) => {
    const rows = [...table.rows];
    const widths = rows.map(row => [...row.cells].reduce((n, cell) => n + cell.colSpan, 0));
    const header = rows.find(row => [...row.cells].some(cell => cell.tagName === 'TH'));
    const expected = header ? [...header.cells].reduce((n, cell) => n + cell.colSpan, 0) : null;
    const hasRowSpan = rows.some(row => [...row.cells].some(cell => cell.rowSpan !== 1));
    return {
      index, visible: visible(table), expectedColumns: expected, rowWidths: widths,
      irregularRows: !hasRowSpan && expected !== null
        ? widths.map((width, row) => ({row, width})).filter(x => x.width !== expected) : [],
      needsManualReview: hasRowSpan || expected === null
    };
  });
  const brokenAnchors = [...document.querySelectorAll('a[href^="#"]')]
    .map(a => ({text: a.textContent.trim(), href: a.getAttribute('href')}))
    .filter(a => a.href.length > 1)
    .filter(a => {
      try { return !document.getElementById(decodeURIComponent(a.href.slice(1))); }
      catch { return true; }
    });
  return {
    title: document.title,
    viewport: {width: innerWidth, height: innerHeight},
    horizontalOverflow: document.documentElement.scrollWidth > innerWidth + 1,
    duplicateIds: [...ids].filter(([, count]) => count > 1).map(([id, count]) => ({id, count})),
    brokenAnchors,
    images: {
      total: images.length,
      broken: images.filter(i => i.complete && !i.loaded),
      pendingVisible: images.filter(i => i.inViewport && !i.complete),
      missingAlt: images.filter(i => i.alt === null),
      pendingOutsideViewport: images.filter(i => !i.inViewport && !i.complete)
    },
    tables,
    emptyControls: [...document.querySelectorAll('button, select, textarea')]
      .filter(el => visible(el) && !el.textContent.trim() && !el.getAttribute('aria-label')
        && !el.getAttribute('aria-labelledby') && !(el.labels && el.labels.length))
      .map(el => ({tag: el.tagName, id: el.id})),
    note: 'Read-only structural diagnostics. Visually inspect layout and evidence; pending lazy images and complex tables need context.'
  };
})()
