// Verification harness for visual-review/noise-canyon.html.
//
//   node visual-review/verify_carousel.js            check only
//   node visual-review/verify_carousel.js --shots    also write _c-<id>.png
//
// Run from the repository root. Checks, in both themes:
//   - slide count matches dot count
//   - every slide carries art, and it is real art: a generated slide must have
//     drawn shapes, an image slide must have DECODED (naturalWidth > 0), which
//     catches a broken src that would otherwise render as an empty box
//   - no NaN / Infinity / undefined / [object in any SVG label
//   - the stage has a sensible height, so a collapsed or clipped drawing fails
//   - keyboard navigation works
//   - zero console errors and zero page errors
//
// Slides are selected by CLICKING THEIR DOT and then reading whichever slide
// reports aria-hidden="false". Screenshotting `.slide` by index does not work:
// the track is transform-translated, so an element screenshot silently
// captures whatever happens to be at that viewport position.
const { chromium } = require("playwright");

(async () => {
  const dir = process.cwd().replace(/\\/g, "/");
  const b = await chromium.launch({ channel: "msedge" });
  let bad = 0;

  for (const theme of ["light", "dark"]) {
    const pg = await b.newPage({
      viewportSize: { width: 1520, height: 1200 },
      deviceScaleFactor: 1.3,
    });
    const errs = [];
    pg.on("console", (m) => { if (m.type() === "error") errs.push(m.text()); });
    pg.on("pageerror", (e) => errs.push("PAGEERROR " + e.message));
    pg.on("response", (r) => {
      if (r.status() >= 400) errs.push("HTTP " + r.status() + " " + r.url());
    });

    await pg.goto("file:///" + dir +
      "/visual-review/noise-canyon.html?scoutTheme=" + theme);
    await pg.waitForTimeout(700);

    const n = await pg.locator(".slide").count();
    const dots = await pg.locator(".dot").count();
    if (n !== dots) { console.log("MISMATCH slides", n, "dots", dots); bad++; }

    for (let i = 0; i < n; i++) {
      await pg.locator(".dot").nth(i).click();
      await pg.waitForTimeout(650);
      const info = await pg.evaluate(async () => {
        const t = document.getElementById("track");
        const vis = [...t.querySelectorAll(".slide")].find(
          (s) => s.getAttribute("aria-hidden") === "false");
        const stage = vis.querySelector(".stage");
        const svg = stage.querySelector("svg.art");
        const img = stage.querySelector("img");
        if (img && !img.complete) {
          await new Promise((res) => { img.onload = img.onerror = res; });
        }
        const texts = svg
          ? [...svg.querySelectorAll("text")].map((x) => x.textContent) : [];
        return {
          id: vis.dataset.id,
          count: document.getElementById("cur").textContent,
          kind: svg ? "svg" : (img ? "img" : "none"),
          paths: svg ? svg.querySelectorAll("path,rect,circle").length : 0,
          nat: img ? img.naturalWidth : 0,
          badnum: texts.filter((x) => /NaN|Infinity|undefined|\[object/.test(x)),
          h: stage.getBoundingClientRect().height,
        };
      });
      const artOk = info.kind === "svg" ? info.paths >= 20
        : info.kind === "img" ? info.nat > 0 : false;
      const flag = !artOk || info.badnum.length > 0 || info.h < 200 || info.h > 1000;
      if (flag) bad++;
      console.log(
        (flag ? "FAIL " : "ok   ") + theme.padEnd(6),
        info.id.padEnd(16), info.count.padEnd(9),
        (info.kind === "img" ? "img=" + info.nat + "px"
          : "shapes=" + info.paths).padEnd(14),
        "h=" + Math.round(info.h),
        info.badnum.length ? "BAD:" + info.badnum.join("|") : "");
      if (theme === "light" && process.argv[2] === "--shots") {
        await pg.locator(".car").screenshot({ path: "_c-" + info.id + ".png" });
      }
    }

    await pg.locator(".dot").first().click();
    await pg.waitForTimeout(400);
    await pg.keyboard.press("ArrowRight");
    await pg.waitForTimeout(500);
    const after = await pg.evaluate(
      () => document.getElementById("cur").textContent);
    if (!after.startsWith("2")) {
      console.log("FAIL keyboard ArrowRight ->", after); bad++;
    }
    await pg.keyboard.press("End");
    await pg.waitForTimeout(500);
    const end = await pg.evaluate(
      () => document.getElementById("cur").textContent);
    if (!end.startsWith(String(n))) {
      console.log("FAIL keyboard End ->", end); bad++;
    }

    console.log(theme, "console errors:", errs.length ? errs.join(" | ") : "none");
    if (errs.length) bad++;
    await pg.close();
  }

  await b.close();
  console.log(bad ? "\nFAILURES: " + bad : "\nALL CLEAR");
  process.exit(bad ? 1 : 0);
})();
