// Structural harness for procurement/procurement-dashboard.html.
//
// Committed rather than written and deleted each time, for the same reason
// the usage-calc verifier is: every phase that wrote its own throwaway checker
// wrote one that caught the PREVIOUS phase's mistake, and a defect shipped
// for three phases as a result.
//
//   node procurement/verify_procurement.js
//
// Asserts on counts rather than on content, so it fails when a card silently
// stops rendering - which is the failure mode this page has already had once,
// when a marker in the page's own prose caused the data injection to splice
// out the script and the page rendered empty with no console error.

const { chromium } = require('playwright');
const path = require('path');

const PAGE = 'file:///' + path.join(__dirname, 'procurement-dashboard.html')
  .replace(/\\/g, '/');

const EXPECT = {
  // Floors, not equalities. A hardcoded equality fails whenever a card is
  // legitimately added -- which is exactly when the page most needs checking
  // -- and it trains you to edit the test rather than read the page. The
  // named CARD_IDS list below is what actually pins the page's structure.
  minCards: 15,     // every card in the body
  minTables: 12,
  minRows: 55,      // tbody rows across all tables once data is injected
  minBars: 25,      // bar-chart rows
  minStats: 10,     // headline stat cells
  maxBarHeight: 60, // a bar taller than this means the masthead .bar rules leaked
};

// Every card must be present by id. A card that is deleted or renamed shows up
// here rather than as a quietly shorter page.
const CARD_IDS = [
  'head', 'refuse', 'delivered', 'ladder', 'bottomup', 'awards', 'design',
  'direction', 'crosscheck', 'notdelivered', 'seven', 'transparency',
  'measured', 'weak', 'method',
];

(async () => {
  const browser = await chromium.launch({ channel: 'msedge' });
  let failures = 0;
  const fail = (m) => { failures++; console.log('  FAIL ' + m); };

  for (const theme of ['light', 'dark']) {
    console.log(theme);
    const page = await browser.newPage();
    const errs = [];
    page.on('console', (m) => { if (m.type() === 'error') errs.push(m.text()); });
    page.on('pageerror', (e) => errs.push('PAGEERROR ' + e.message));
    page.on('response', (r) => {
      if (r.status() >= 400) errs.push('HTTP ' + r.status() + ' ' + r.url());
    });

    await page.goto(PAGE + '?scoutTheme=' + theme, { waitUntil: 'networkidle' });
    await page.waitForTimeout(800);

    const r = await page.evaluate((ids) => {
      const t = document.body.innerText;
      const bars = [...document.querySelectorAll('.bar')]
        .map((e) => e.getBoundingClientRect().height);
      return {
        cards: document.querySelectorAll('section.card').length,
        tables: document.querySelectorAll('table').length,
        rows: document.querySelectorAll('tbody tr').length,
        bars: bars.length,
        maxBar: bars.length ? Math.max(...bars) : 0,
        stats: document.querySelectorAll('.stat').length,
        missing: ids.filter((id) => !document.getElementById(id)),
        // Injection failure and template failure both surface as text.
        junk: /NaN|undefined|Infinity|\[object|&mdash;|&lt;/.test(t),
        // The masthead must be present and must be exactly one row.
        mhBars: document.querySelectorAll('.mh-bar').length,
        mhRows: (() => {
          const n = document.querySelector('.mh-nav');
          if (!n) return -1;
          const tops = new Set([...n.children]
            .map((e) => Math.round(e.getBoundingClientRect().top)));
          return tops.size;
        })(),
        // Every dollar figure must carry a thousands separator; a raw float
        // is the signature of a value that bypassed the formatter.
        rawFloat: /\$\d+\.\d{3,}/.test(t),
      };
    }, CARD_IDS);

    if (errs.length) fail('console/page/http errors: ' + JSON.stringify(errs.slice(0, 6)));
    if (r.cards < EXPECT.minCards) fail('cards ' + r.cards + ' < ' + EXPECT.minCards);
    if (r.tables < EXPECT.minTables) fail('tables ' + r.tables + ' < ' + EXPECT.minTables);
    if (r.rows < EXPECT.minRows) fail('tbody rows ' + r.rows + ' < ' + EXPECT.minRows);
    if (r.bars < EXPECT.minBars) fail('bars ' + r.bars + ' < ' + EXPECT.minBars);
    if (r.stats < EXPECT.minStats) fail('stats ' + r.stats + ' < ' + EXPECT.minStats);
    if (r.missing.length) fail('missing cards: ' + r.missing.join(', '));
    if (r.junk) fail('unrendered placeholder or leaked entity in body text');
    if (r.rawFloat) fail('unformatted float in a dollar figure');
    if (r.maxBar > EXPECT.maxBarHeight) {
      fail('bar height ' + r.maxBar.toFixed(1) + 'px > ' + EXPECT.maxBarHeight
           + ' - the masthead .bar rules have leaked onto the charts');
    }
    if (r.mhBars !== 1) fail('mh-bar count ' + r.mhBars + ' != 1');
    if (r.mhRows !== 1) fail('masthead nav wraps to ' + r.mhRows + ' rows');

    console.log('  ' + JSON.stringify(r));
    await page.close();
  }

  await browser.close();
  console.log(failures ? '\nFAILURES: ' + failures : '\nOK');
  process.exit(failures ? 1 : 0);
})();
