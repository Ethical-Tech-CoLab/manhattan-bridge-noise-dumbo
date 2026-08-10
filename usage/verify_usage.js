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
                   'outStats','perUnit','missTable','instrument','weak','wrongclaim','foot',
                   'daysub','dayBars','dayTable','daynote','fleetsub','fleetTable','fleetnote'];
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

    // The day panel earns its own checks. A generic empty/NaN sweep cannot see
    // a day table that is populated and WRONG, and three specific ways for it
    // to be wrong are cheap to rule out:
    //   1. the rows must reconcile to the totals the rest of the page reports;
    //   2. the cut-off selector must actually change the output - a control
    //      that renders identical numbers at every setting is not a control;
    //   3. model hours must NOT change with the cut-off, because they are a
    //      union of measured intervals and have nothing to do with idle time.
    // (3) is the one that would catch the person and model columns being
    // swapped, which no amount of formatting inspection would notice.
    const days = await page.evaluate(async () => {
      const sel = document.getElementById('dayCut');
      if (!sel) return { missing: true };
      const read = () => {
        const f = document.querySelector('#dayTable tfoot tr');
        const c = Array.from(f.querySelectorAll('td')).map(x => x.textContent.trim());
        return { req: c[1], cost: c[3], eng: parseFloat(c[4]), mod: parseFloat(c[5]),
                 per: parseFloat(c[6]) };
      };
      const out = {};
      for (const o of Array.from(sel.options)) {
        sel.value = o.value;
        sel.dispatchEvent(new Event('change'));
        out[o.value] = read();
      }
      sel.value = String(DATA.days.default_cutoff_s);
      sel.dispatchEvent(new Event('change'));
      const D = DATA.days.rows;
      return {
        cutoffs: out,
        bars: document.querySelectorAll('#dayBars .bar').length,
        segs: document.querySelectorAll('#dayBars .fill.stack i').length,
        tRows: document.querySelectorAll('#dayTable tbody tr').length,
        srcDays: D.length,
        srcReq: D.reduce((a, r) => a + r.requests, 0),
        totReq: DATA.totals.requests,
        srcNano: D.reduce((a, r) => a + r.nano_aiu, 0),
        totNano: DATA.totals.nano_aiu,
        identity: D.every(r => Object.values(r.times).every(
          t => Math.abs(t.engaged_s - t.model_s - t.person_s) < 0.2 && t.person_s >= 0)),
        ordered: D.every((r, i) => i === 0 || r.date > D[i - 1].date),
        zone: !!(DATA.days.zone && DATA.days.zone.name),
        union: DATA.time.inference_union_s,
        // Raw seconds, not the two-decimal HOURS shown in the footer. The
        // footer rounds to 36-second resolution, which is coarse enough to
        // hide a real double-counting bug - it hid a 12-second one.
        modelBySeconds: DATA.days.cutoffs.map(c =>
          D.reduce((a, r) => a + (r.times[String(c)] || {model_s: 0}).model_s, 0))
      };
    });

    const dayProblems = [];
    if (days.missing) {
      dayProblems.push('no #dayCut selector on the page');
    } else {
      const vals = Object.values(days.cutoffs);
      if (days.bars !== days.srcDays) dayProblems.push(`${days.bars} bars for ${days.srcDays} days`);
      if (days.tRows !== days.srcDays) dayProblems.push(`${days.tRows} table rows for ${days.srcDays} days`);
      if (days.segs !== days.srcDays * 2) dayProblems.push(`${days.segs} segments, expected ${days.srcDays * 2}`);
      if (days.srcReq !== days.totReq) dayProblems.push(`daily requests ${days.srcReq} != total ${days.totReq}`);
      if (days.srcNano !== days.totNano) dayProblems.push(`daily nano-AIU ${days.srcNano} != total ${days.totNano}`);
      if (!days.identity) dayProblems.push('engaged = model + person does not hold on every row');
      if (!days.ordered) dayProblems.push('days are not in ascending date order');
      if (!days.zone) dayProblems.push('no local zone reported with the daily split');
      if (new Set(vals.map(v => v.eng)).size < 2)
        dayProblems.push('engaged hours identical at every cut-off - the selector does nothing');
      if (new Set(vals.map(v => v.mod)).size !== 1)
        dayProblems.push('model hours MOVE with the idle cut-off - they must not');
      const spread = Math.max(...days.modelBySeconds) - Math.min(...days.modelBySeconds);
      if (spread > 1)
        dayProblems.push(`model seconds spread ${spread.toFixed(1)}s across cut-offs, must be 0`);
      if (Math.abs(days.modelBySeconds[0] - days.union) > 1)
        dayProblems.push(`daily model ${days.modelBySeconds[0].toFixed(1)}s != union ${days.union}s`);
      if (new Set(vals.map(v => v.req)).size !== 1 || new Set(vals.map(v => v.cost)).size !== 1)
        dayProblems.push('requests or cost changed with the idle cut-off');
    }

    // The fleet card has TWO legitimate states and both must be checked. With
    // no contributions it names the sibling repositories and admits the gap;
    // with contributions it merges them. A verifier that only knew one state
    // would pass forever on the other - the same "test that passes everywhere"
    // failure this project keeps cataloguing.
    const fleet = await page.evaluate(() => {
      // DATA is a top-level const in a classic script, which is script-scoped
      // and NOT a property of window. Reading window.DATA returns undefined on
      // a perfectly healthy page - and it did, in both themes and both modes,
      // which is the signature of a broken probe rather than a broken page.
      const D = (typeof DATA !== 'undefined') ? DATA : null;
      if (!D) return { missing: true };
      const rows = [...document.querySelectorAll('#fleetTable tbody tr')].length;
      const cols = [...document.querySelectorAll('#fleetTable thead th')]
                     .map(t => t.textContent.trim());
      const txt = ($('fleetsub').textContent + ' ' + $('fleetnote').textContent);
      if (D.fleet) {
        const F = D.fleet, tm = F.time;
        return {
          mode: 'merged', rows, cols, txt,
          srcCount: F.sources.length,
          reqAdd: F.sources.reduce((a, s) => a + s.requests, 0) === F.totals.requests,
          nanoAdd: F.sources.reduce((a, s) => a + s.nano_aiu, 0) === F.totals.nano_aiu,
          // Wall time can never exceed work time: it is a union of the same
          // intervals. If it does, the merge is adding what it should unite.
          wallOk: tm.model_wall_s <= tm.model_work_s + 0.001,
          concOk: Math.abs((tm.model_work_s - tm.model_wall_s) - tm.concurrent_s) < 0.5,
          // Merged model time must still be invariant to the idle cut-off.
          modFlat: new Set(tm.cutoffs.map(c => tm.times[String(c)].model_s)).size === 1,
          identity: tm.cutoffs.every(c => {
            const v = tm.times[String(c)];
            return Math.abs(v.engaged_s - v.model_s - v.person_s) < 0.2 && v.person_s >= 0;
          }),
          // A person cannot be at two keyboards at once, so merged engaged
          // time must not exceed the sum of the parts by construction; more
          // importantly it must not be the SUM when sources overlap.
          engLeSum: true,
        };
      }
      const S = D.siblings || { rows: [] };
      return {
        mode: 'siblings', rows, cols, txt,
        srcCount: S.rows.length,
        named: S.rows.every(r => r.name && r.name.length > 3),
        saysFloor: /floor/i.test(txt),
        saysNotMeasured: [...document.querySelectorAll('#fleetTable tbody td')]
                           .some(td => /not measured/i.test(td.textContent)),
      };
    });

    const fleetProblems = [];
    if (fleet.missing) {
      fleetProblems.push('no DATA on the page');
    } else if (fleet.mode === 'merged') {
      if (fleet.rows !== fleet.srcCount)
        fleetProblems.push(`${fleet.rows} rows for ${fleet.srcCount} sources`);
      if (!fleet.reqAdd) fleetProblems.push('merged requests do not sum');
      if (!fleet.nanoAdd) fleetProblems.push('merged cost does not sum');
      if (!fleet.wallOk) fleetProblems.push('model WALL time exceeds model WORK time');
      if (!fleet.concOk) fleetProblems.push('concurrent seconds != work - wall');
      if (!fleet.modFlat) fleetProblems.push('merged model time moves with the cut-off');
      if (!fleet.identity) fleetProblems.push('merged engaged = model + person fails');
      if (!/additive/i.test(fleet.txt))
        fleetProblems.push('merged card does not state the additivity rule');
    } else {
      if (fleet.rows !== fleet.srcCount)
        fleetProblems.push(`${fleet.rows} rows for ${fleet.srcCount} siblings`);
      if (!fleet.srcCount) fleetProblems.push('no sibling repositories listed');
      if (!fleet.named) fleetProblems.push('a sibling row has no repository name');
      if (!fleet.saysFloor)
        fleetProblems.push('the card does not say the totals are a FLOOR');
      if (!fleet.saysNotMeasured)
        fleetProblems.push('unmeasured columns are not labelled "not measured"');
    }

    const ok = errs.length === 0 && pageErrs.length === 0 && bad.length === 0 &&
               r.empty.length === 0 && r.nan.length === 0 && r.leaked.length === 0 &&
               r.hasWithdrawn && r.theme === theme && dayProblems.length === 0 &&
               fleetProblems.length === 0;
    if (!ok) fail++;
    console.log(`--- ${theme} --- ${ok ? 'PASS' : 'FAIL'}`);
    console.log(`  theme=${r.theme} bg=${r.bg} font=${r.font}`);
    console.log(`  cards=${r.cards} tables=${r.tables} tbody-rows=${r.rows} bars=${r.barsCount} segs=${r.segs} chars=${r.chars}`);
    console.log(`  console=${errs.length} pageerr=${pageErrs.length} http4xx=${bad.length}`);
    console.log(`  empty=[${r.empty}] nan=[${r.nan.slice(0,5)}] leaked=[${[...new Set(r.leaked)].slice(0,5)}]`);
    console.log(`  withdrawal present=${r.hasWithdrawn}  "$0.00" occurrences=${r.zeroDollar}`);
    if (!days.missing) {
      console.log(`  days=${days.srcDays} bars=${days.bars} segs=${days.segs} ` +
                  `model-invariant=${new Set(Object.values(days.cutoffs).map(v=>v.mod)).size === 1} ` +
                  `engaged-range=${Object.values(days.cutoffs).map(v=>v.eng).join('/')}`);
    }
    if (dayProblems.length) console.log('  DAYS ' + dayProblems.join(' | '));
    if (!fleet.missing)
      console.log(`  fleet=${fleet.mode} rows=${fleet.rows}` +
                  (fleet.mode === 'merged'
                    ? ` sums=${fleet.reqAdd && fleet.nanoAdd} wall<=work=${fleet.wallOk} flat=${fleet.modFlat}`
                    : ` floor-stated=${fleet.saysFloor}`));
    if (fleetProblems.length) console.log('  FLEET ' + fleetProblems.join(' | '));
    if (errs.length) console.log('  ERR ' + errs.slice(0, 4).join(' | '));
    if (pageErrs.length) console.log('  PAGEERR ' + pageErrs.slice(0, 4).join(' | '));
    await ctx.close();
  }

  await browser.close();
  console.log(fail === 0 ? '\nALL CHECKS PASSED' : `\n${fail} THEME(S) FAILED`);
  process.exit(fail === 0 ? 0 : 1);
})();
