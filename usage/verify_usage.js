const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ channel: 'msedge' });
  const base = 'file:///' + process.cwd().replace(/\\/g, '/') + '/usage/usage-dashboard.html';
  let fail = 0;

  for (const theme of ['light', 'dark']) {
    const ctx = await browser.newContext();
    const page = await ctx.newPage();
    const errs = [], pageErrs = [], bad = [];
    page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    page.on('pageerror', e => pageErrs.push(e.message));
    page.on('response', r => { if (r.status() >= 400) bad.push(r.status() + ' ' + r.url()); });

    await page.goto(base + '?scoutTheme=' + theme, { waitUntil: 'networkidle' });
    await page.waitForTimeout(400);

    const r = await page.evaluate(() => {
      const txt = document.body.innerText;
      const ids = ['hero','chanTable','dual','initBars','effortBars','cfStats','timeTable',
                   'activeBars','turnBars','turnTable','modelTable','agentTable','energyTable',
                   'outStats','perUnit','missTable','instrument','weak','wrongclaim','foot'];
      const empty = ids.filter(i => {
        const el = document.getElementById(i);
        return !el || el.innerHTML.trim().length < 20;
      });
      return {
        theme: document.documentElement.getAttribute('data-theme'),
        chars: txt.length,
        cards: document.querySelectorAll('.card').length,
        tables: document.querySelectorAll('table').length,
        rows: document.querySelectorAll('tbody tr').length,
        barsCount: document.querySelectorAll('.bar').length,
        segs: document.querySelectorAll('.seg div').length,
        empty,
        nan: (txt.match(/NaN|undefined|Infinity|\[object|null%|\$NaN/g) || []),
        leaked: (txt.match(/<span|&lt;|&mdash;|&rsquo;|&amp;/g) || []),
        zeroDollar: (txt.match(/\$0\.00\b/g) || []).length,
        hasWithdrawn: txt.includes('That is withdrawn'),
        bg: getComputedStyle(document.body).backgroundColor,
        font: getComputedStyle(document.body).fontFamily.slice(0, 20)
      };
    });

    const ok = errs.length === 0 && pageErrs.length === 0 && bad.length === 0 &&
               r.empty.length === 0 && r.nan.length === 0 && r.leaked.length === 0 &&
               r.hasWithdrawn && r.theme === theme;
    if (!ok) fail++;
    console.log(`--- ${theme} --- ${ok ? 'PASS' : 'FAIL'}`);
    console.log(`  theme=${r.theme} bg=${r.bg} font=${r.font}`);
    console.log(`  cards=${r.cards} tables=${r.tables} tbody-rows=${r.rows} bars=${r.barsCount} segs=${r.segs} chars=${r.chars}`);
    console.log(`  console=${errs.length} pageerr=${pageErrs.length} http4xx=${bad.length}`);
    console.log(`  empty=[${r.empty}] nan=[${r.nan.slice(0,5)}] leaked=[${[...new Set(r.leaked)].slice(0,5)}]`);
    console.log(`  withdrawal present=${r.hasWithdrawn}  "$0.00" occurrences=${r.zeroDollar}`);
    if (errs.length) console.log('  ERR ' + errs.slice(0, 4).join(' | '));
    if (pageErrs.length) console.log('  PAGEERR ' + pageErrs.slice(0, 4).join(' | '));
    await ctx.close();
  }

  await browser.close();
  console.log(fail === 0 ? '\nALL CHECKS PASSED' : `\n${fail} THEME(S) FAILED`);
  process.exit(fail === 0 ? 0 : 1);
})();
