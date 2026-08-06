/* Verification harness for the susceptibility layer in agent-model.html.

   Run from the repository root:
     node visual-review/verify_agent_model.js visual-review/agent-model.html

   THE LOAD-BEARING TEST IS THE PER-GROUP DOSE INVARIANCE ONE. The whole
   design claim of this layer is that it describes WHO is standing in the
   noise and never touches the noise itself. If switching the layer on moves
   any dose for a group whose itinerary did not change, that claim is false
   and the page must not ship. That test has already caught two real defects:
   the rung being baked into the group sub-seed (which silently broke the
   ladder's own stated purpose), and a scenario draw being skipped on the
   dog-walk override (which desynchronised every subsequent draw). */
const { chromium } = require("playwright");
const nodePath = require("path");
const arg = process.argv[2] || "visual-review/agent-model.html";

const URL = "file:///" + nodePath.resolve(arg).replace(/\\/g, "/");

async function runCfg(page, cfg) {
  return await page.evaluate(async (c) => {
    state.rung = c.rung; state.seed = c.seed; state.day = c.day;
    state.hour = c.hour; state.pop = c.pop;
    reset();
    let guard = 0;
    while (!state.done && guard++ < 400000) tickOnce();
    const personSec = state.groups.reduce((s, g) => s + g.secs * g.size, 0);
    const people = state.groups.reduce((s, g) => s + g.size, 0);
    const dogs = state.groups.reduce((s, g) => s + g.dogs, 0);
    const doses = state.groups.filter(g => g.secs > 0).map(g => +doseLeq(g).toFixed(6));
    // Per-group dose keyed by id, so two runs can be compared group by group
    // rather than only in aggregate.
    const byGroup = {};
    state.groups.forEach(g => { byGroup[g.id] = { d: +doseLeq(g).toFixed(6), sc: g.scenario }; });
    const sumClassSec = SENSITIVITIES.filter(x => x.kind === "person")
      .reduce((a, x) => a + (state.sensSec[x.id] || 0), 0);
    return {
      done: state.done, guard, groups: state.groups.length, people, dogs,
      personSec: +personSec.toFixed(3),
      doseHash: doses.join(","), byGroup,
      meanDose: +doses.reduce((a, b) => a + b, 0).toFixed(6),
      sensSec: state.sensSec, anySensSec: +state.anySensSec.toFixed(3),
      sumClassSec: +sumClassSec.toFixed(3),
      carried: +state.carriedSec.toFixed(3), chosen: +state.chosenSec.toFixed(3),
      led: +state.ledSec.toFixed(3),
      dogrunVisits: byId.dogrun.visits,
      dogrunDogSec: +byId.dogrun.dogSec.toFixed(3),
      dogWalks: state.groups.filter(g => g.scenario === "dog_walk").length,
      dogWalkNoDog: state.groups.filter(g => g.scenario === "dog_walk" && g.dogs === 0).length,
      zeroLen: state.groups.filter(g => g.state === "departed" && g.secs === 0).length,
      contended: state.counts["place.contended"] || 0,
      sensNoLayer: Object.keys(state.sens || {}).length
    };
  }, cfg);
}

(async () => {
  const problems = [];
  const browser = await chromium.launch({ channel: "msedge" });

  for (const theme of ["light", "dark"]) {
    const page = await browser.newPage();
    const errs = [];
    page.on("console", m => { if (m.type() === "error") errs.push(m.text()); });
    page.on("pageerror", e => errs.push("PAGEERROR " + e.message));
    await page.goto(URL);
    await page.evaluate(t => document.documentElement.setAttribute("data-theme", t), theme);
    await page.waitForTimeout(400);

    const base = { seed: 20260731, day: "Weekday", hour: 14, pop: 400 };

    // 1. The layer runs and produces non-zero accruals.
    const sens = await runCfg(page, { ...base, rung: "sensitive" });
    if (!sens.done) problems.push(theme + " :: run did not complete");
    if (sens.anySensSec <= 0) problems.push(theme + " :: no any-class seconds accrued");
    if (sens.dogs <= 0) problems.push(theme + " :: no dogs spawned");
    if (sens.dogrunVisits <= 0) problems.push(theme + " :: dog run never visited");
    if (sens.dogrunDogSec <= 0) problems.push(theme + " :: no dog-seconds at the dog run");
    if (sens.zeroLen > 0) problems.push(theme + " :: " + sens.zeroLen + " zero-length visits");

    // 2. THE LOAD-BEARING TEST. Switching the layer on must not move the dose of
    //    anyone whose itinerary it did not change. Groups that now walk a dog
    //    genuinely go somewhere else, so those are expected to differ and are
    //    counted separately rather than excused silently.
    const cont = await runCfg(page, { ...base, rung: "contend" });
    let moved = 0, sameScen = 0, changedScen = 0;
    for (const id in sens.byGroup) {
      const a = cont.byGroup[id], b = sens.byGroup[id];
      if (!a) { problems.push(theme + " :: group " + id + " missing from contend run"); continue; }
      if (a.sc === b.sc) { sameScen++; if (a.d !== b.d) moved++; }
      else changedScen++;
    }
    if (moved > 0)
      problems.push(theme + " :: " + moved + " of " + sameScen +
        " unchanged-itinerary groups had their dose MOVED by the susceptibility layer");
    if (changedScen <= 0)
      problems.push(theme + " :: no itineraries changed, so the dog-walk path is not exercised");
    if (cont.anySensSec !== 0 || Object.keys(cont.sensSec).length !== 0)
      problems.push(theme + " :: class accruals leaked into the contend rung");
    if (cont.dogs !== 0) problems.push(theme + " :: dogs leaked into the contend rung");

    // 3. Contention must still fire at the rung ABOVE contend.
    if (sens.contended <= 0)
      problems.push(theme + " :: contention did not fire at the sensitive rung (rank check broken)");

    // 4. Overlap must be real: class rows must exceed the any-class total.
    if (!(sens.sumClassSec > sens.anySensSec))
      problems.push(theme + " :: class sum " + sens.sumClassSec + " not greater than any-class " +
        sens.anySensSec + " -- overlap is not being modelled");

    // 5. Consistency: a dog walk requires a dog.
    if (sens.dogWalkNoDog > 0)
      problems.push(theme + " :: " + sens.dogWalkNoDog + " dog_walk groups have no dog");
    if (sens.dogWalks <= 0) problems.push(theme + " :: no dog walks planned");

    // 6. Agency must partition the people.
    const agencyTot = sens.carried + sens.chosen;
    if (Math.abs(agencyTot - sens.personSec) > 0.5)
      problems.push(theme + " :: agency split " + agencyTot + " != person-seconds " + sens.personSec);
    if (sens.carried <= 0) problems.push(theme + " :: nobody in the carried class");

    // 7. Determinism at a seed.
    const again = await runCfg(page, { ...base, rung: "sensitive" });
    if (JSON.stringify(again) !== JSON.stringify(sens))
      problems.push(theme + " :: run is not deterministic at a fixed seed");

    // 8. A different seed must change the composition.
    const other = await runCfg(page, { ...base, rung: "sensitive", seed: 99 });
    if (other.anySensSec === sens.anySensSec)
      problems.push(theme + " :: seed 99 gave an identical any-class total");

    // 9. Panels render, in this theme, with no junk.
    await page.evaluate(() => { state.rung = "sensitive"; reset();
      let g = 0; while (!state.done && g++ < 400000) tickOnce(); redrawAll(); });
    for (const id of ["sensTable", "agencyTable", "sensPlaceTable", "sensDefTable"]) {
      const t = await page.$eval(id === "sensDefTable" ? "#sensDefTable" : "#" + id,
        el => el.innerText.trim());
      if (!t) problems.push(theme + " :: " + id + " is empty");
      if (/NaN|undefined|Infinity|\[object/.test(t))
        problems.push(theme + " :: " + id + " contains junk -> " +
          t.split("\n").find(l => /NaN|undefined|Infinity|\[object/.test(l)));
      const rows = await page.$$eval("#" + id + " tbody tr", r => r.length).catch(() => 0);
      if (id !== "agencyTable" && rows < 3) problems.push(theme + " :: " + id + " has only " + rows + " rows");
    }
    // The refusal must be present and must not have been quietly turned into a number.
    const body = await page.$eval("body", el => el.innerText);
    if (!/not in the same units/.test(body))
      problems.push(theme + " :: the dB HL refusal is missing from the page");
    if (/weighted dose|sensitivity multiplier|penalty of \d+ dB/i.test(body))
      problems.push(theme + " :: the page appears to publish a weighted dose");

    if (errs.length) problems.push(theme + " :: console/page errors -> " + errs.slice(0, 3).join(" | "));

    console.log(theme.padEnd(6),
      "groups", sens.groups, "people", sens.people, "dogs", sens.dogs,
      "| any-class h", (sens.anySensSec / 3600).toFixed(2),
      "sum-class h", (sens.sumClassSec / 3600).toFixed(2),
      "| carried h", (sens.carried / 3600).toFixed(2),
      "| dogrun visits", sens.dogrunVisits,
      "| contended", sens.contended,
      "| unchanged-itinerary doses identical:", moved === 0,
      "(" + sameScen + " same, " + changedScen + " rerouted)");
    await page.close();
  }

  await browser.close();
  if (problems.length) { console.log("\nPROBLEMS (" + problems.length + ")");
    problems.forEach(p => console.log("  - " + p)); process.exit(1); }
  console.log("\nOK - susceptibility layer clean in both themes");
})();
