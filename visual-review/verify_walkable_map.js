/* Verification harness for visual-review/walkable-map.html.
 *
 * Run:  node visual-review/verify_walkable_map.js
 * Needs Playwright with the msedge channel:
 *   $env:NODE_PATH="<repo>\node_modules"
 *
 * What it asserts, and why each one is here rather than being eyeballed:
 *   - zero console errors and zero page errors in BOTH themes, because a
 *     page that reports an error it does not have trains a reader to ignore
 *     errors;
 *   - the canvas is not blank in every mode, because a painter's-algorithm
 *     renderer that silently draws nothing looks exactly like a page that is
 *     still loading;
 *   - the counts the page prints in prose equal the counts the renderer
 *     actually holds, because a number maintained in two places will
 *     eventually disagree with itself;
 *   - no NaN reaches the projection, because one NaN vertex poisons a whole
 *     face and leaves a hole rather than an error.
 */
const { chromium } = require("playwright");
const path = require("path");

const FILE = "file:///" +
  path.join(__dirname, "walkable-map.html").replace(/\\/g, "/");

function blank(buf) {
  /* A PNG of a single flat colour compresses to almost nothing. This is a
     coarse test and it is the one that catches "renderer threw on frame 1". */
  return buf.length < 3000;
}

(async () => {
  const browser = await chromium.launch({ channel: "msedge" });
  let bad = 0;

  for (const theme of ["light", "dark"]) {
    const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    const errs = [];
    page.on("console", (m) => { if (m.type() === "error") errs.push(m.text()); });
    page.on("pageerror", (e) => errs.push("pageerror: " + e.message));
    page.on("response", (r) => {
      if (r.status() >= 400) errs.push("HTTP " + r.status() + " " + r.url());
    });

    await page.goto(FILE, { waitUntil: "load" });
    await page.evaluate((t) =>
      document.documentElement.setAttribute("data-theme", t), theme);
    await page.waitForTimeout(700);

    const api = await page.evaluate(() => {
      const a = window.__WMAPI__;
      return a ? { ok: true, counts: a.counts(), route: a.routeLen(),
                   agents: a.agents() } : { ok: false };
    });
    if (!api.ok) { console.log("FAIL " + theme + ": no __WMAPI__"); bad++; continue; }

    /* Prose vs renderer. The page prints these counts in the sources card;
       the renderer holds them in its payload. They must be the same. */
    const txt = await page.evaluate(() => document.body.innerText);
    const fmt = (n) => n.toLocaleString("en-US");
    for (const [label, n] of [["near", api.counts.near], ["far", api.counts.far],
                              ["nodes", api.counts.nodes]]) {
      if (txt.indexOf(fmt(n)) < 0) {
        console.log("FAIL " + theme + ": prose does not mention " + label +
                    " = " + fmt(n));
        bad++;
      }
    }

    for (const mode of ["model", "plan", "walk"]) {
      await page.evaluate((m) => window.__WMAPI__.setMode(m), mode);
      await page.waitForTimeout(450);
      const shot = await page.locator("#vp").screenshot();
      const faces = await page.evaluate(() => window.__WMAPI__.faces());
      if (blank(shot)) {
        console.log("FAIL " + theme + "/" + mode + ": canvas is blank");
        bad++;
      }
      if (mode !== "plan" && faces < 200) {
        console.log("FAIL " + theme + "/" + mode + ": only " + faces + " faces");
        bad++;
      }
      console.log("  " + theme + "/" + mode + " ok, " + faces + " faces, " +
                  shot.length + " png bytes");
    }

    /* Every layer off must still not throw, and must not leave the canvas
       reporting geometry it is no longer drawing. */
    await page.evaluate(() => window.__WMAPI__.setMode("model"));
    for (const k of ["build", "paths", "agents", "marks"]) {
      await page.click('[data-toggle="' + k + '"]');
    }
    await page.waitForTimeout(350);
    const stripped = await page.evaluate(() => window.__WMAPI__.faces());
    if (stripped !== 0) {
      console.log("FAIL " + theme + ": " + stripped +
                  " faces with every layer switched off");
      bad++;
    }
    for (const k of ["build", "paths", "agents", "marks"]) {
      await page.click('[data-toggle="' + k + '"]');
    }

    /* The level wash is the one layer that samples the interpolation on a
       grid, so it is where a NaN would first show. */
    await page.evaluate(() => window.__WMAPI__.setMode("plan"));
    await page.click('[data-toggle="sound"]');
    await page.waitForTimeout(350);
    const dbs = await page.evaluate(() => {
      const a = window.__WMAPI__, out = [];
      for (let x = -400; x <= 400; x += 100)
        for (let y = -400; y <= 400; y += 100) out.push(a.dbAt(x, y));
      return out;
    });
    if (dbs.some((v) => !isFinite(v))) {
      console.log("FAIL " + theme + ": non-finite value from dbAt");
      bad++;
    }

    /* The tour drives the eye-level camera along the routed walk. If the
       route is degenerate the walk never advances and the page looks
       frozen rather than broken. */
    await page.click("#tour");
    await page.waitForTimeout(1400);
    const chain = await page.evaluate(() =>
      document.getElementById("h3").textContent);
    if (!/chainage \d+ m of \d+/.test(chain)) {
      console.log("FAIL " + theme + ": tour did not advance (" + chain + ")");
      bad++;
    }
    await page.click("#tour");

    const junk = txt.match(/NaN|\[object |Infinity|undefined m|__[A-Z]+__|@@/);
    if (junk) {
      console.log("FAIL " + theme + ": junk in body text: " + junk[0]);
      bad++;
    }
    if (errs.length) {
      console.log("FAIL " + theme + ": " + errs.length + " error(s)");
      errs.slice(0, 6).forEach((e) => console.log("    " + e));
      bad += errs.length;
    } else {
      console.log(theme + ": 0 console errors, route " +
                  api.route.toFixed(1) + " m, " + api.agents + " figures");
    }
    await page.close();
  }

  await browser.close();
  console.log(bad ? "\nFAILED with " + bad + " problem(s)" : "\nok");
  process.exit(bad ? 1 : 0);
})();
