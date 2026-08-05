const { chromium } = require('playwright');
const path = process.cwd().replace(/\\/g, '/') + '/pedestrian-site-visits/media.html';

(async () => {
  const b = await chromium.launch({ channel: 'msedge' });
  let bad = 0;
  for (const theme of ['light', 'dark']) {
    const p = await b.newPage({ viewportSize: { width: 1280, height: 1200 } });
    const errs = [];
    p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    p.on('pageerror', e => errs.push('PAGEERROR ' + e.message));
    const bad404 = [];
    p.on('response', r => { if (r.status() >= 400) bad404.push(r.status() + ' ' + r.url()); });
    await p.goto('file:///' + path + '?scoutTheme=' + theme);
    await p.waitForTimeout(1400);

    // Images are loading="lazy", so an off-screen one legitimately reports
    // naturalWidth 0. Checking without scrolling would pass a page whose
    // images are all broken AND fail a page whose images are all fine, which
    // is the worst of both. Scroll each one into view and wait for a decode.
    for (const el of await p.$$('img')) {
      await el.scrollIntoViewIfNeeded();
    }
    await p.waitForFunction(
      () => [...document.images].every(i => i.complete), null, { timeout: 15000 }
    ).catch(() => {});
    await p.evaluate(() => window.scrollTo(0, 0));
    await p.waitForTimeout(400);

    // every image actually decoded
    const imgs = await p.$$eval('img', els => els.map(e => ({
      src: e.getAttribute('src'), w: e.naturalWidth, h: e.naturalHeight })));
    const broken = imgs.filter(i => !i.w || !i.h);

    // Every svg chart has real geometry. The check is per chart type, not one
    // blunt rule: an envelope is a polyline, the laps chart is fourteen rects,
    // and the geo chart is circles and rects. A single rule strict enough to
    // catch an empty envelope would fail two charts that are perfectly fine,
    // and a rule loose enough to pass all four would catch nothing.
    const svgs = await p.$$eval('svg.envsvg', els => els.map(e => {
      const r = e.getBoundingClientRect();
      const n = s => e.querySelectorAll(s).length;
      return { kind: e.dataset.kind, w: Math.round(r.width), h: Math.round(r.height),
               poly: n('polyline'), rect: n('rect'), circ: n('circle'),
               line: n('line'), text: n('text') };
    }));
    const MIN = { envelope: s => s.poly >= 1 && s.line >= 4 && s.text >= 5,
                  sweep:    s => s.poly >= 2 && s.line >= 6 && s.text >= 8,
                  laps:     s => s.rect >= 14 && s.text >= 15,
                  geo:      s => s.circ >= 4 && s.rect >= 3 && s.text >= 8 };
    const emptySvg = svgs.filter(s =>
      s.w < 200 || s.h < 40 || !MIN[s.kind] || !MIN[s.kind](s));

    // audio elements point at files that exist
    const auds = await p.$$eval('audio', els => els.map(e => e.getAttribute('src')));

    // junk text, scoped to value-bearing elements only
    const junk = await p.$$eval('td, th, .gv, .gn, .pill, figcaption',
      els => els.map(e => e.textContent.trim())
        .filter(t => /NaN|undefined|\[object|Infinity|&mdash;s|%\.\d/.test(t)));

    // local links resolve
    const hrefs = await p.$$eval('a[href]', els => els.map(e => e.getAttribute('href')));

    const cards = await p.$$eval('section.card', e => e.length);
    const tables = await p.$$eval('table', e => e.length);

    const ok = !errs.length && !bad404.length && !broken.length &&
               !emptySvg.length && !junk.length && cards === 15;
    if (!ok) bad++;
    console.log(`${ok ? 'ok  ' : 'FAIL'} ${theme}  cards=${cards} tables=${tables} ` +
      `imgs=${imgs.length}/${broken.length}bad svg=${svgs.length}/${emptySvg.length}empty ` +
      `audio=${auds.length} err=${errs.length} 4xx=${bad404.length} junk=${junk.length}`);
    if (errs.length) console.log('   errs :', errs.slice(0, 4));
    if (bad404.length) console.log('   4xx  :', bad404.slice(0, 6));
    if (broken.length) console.log('   img  :', broken.slice(0, 6));
    if (emptySvg.length) console.log('   svg  :', emptySvg);
    if (junk.length) console.log('   junk :', junk.slice(0, 6));
    if (theme === 'light') console.log('   links:', hrefs.join(' '));
    await p.screenshot({ path: `_media-${theme}.png`, fullPage: false });
    await p.close();
  }
  await b.close();
  process.exit(bad ? 1 : 0);
})();
