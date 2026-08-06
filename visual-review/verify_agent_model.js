/* Verification harness for the susceptibility and arrival layers in
   agent-model.html.

   Run from the repository root:
     node visual-review/verify_agent_model.js visual-review/agent-model.html

   TWO LOAD-BEARING TESTS, each guarding a design claim the page makes in
   prose:

   1. PER-GROUP DOSE INVARIANCE. The susceptibility layer describes WHO is
      standing in the noise and never touches the noise itself. If switching
      the layer on moves any dose for a group whose itinerary did not change,
      that claim is false and the page must not ship. It has already caught
      two real defects: the rung being baked into the group sub-seed (which
      silently broke the ladder's own stated purpose), and a scenario draw
      being skipped on the dog-walk override (which desynchronised every
      subsequent draw).

   2. ARRIVAL IDENTITY INVARIANCE. The comparison card claims a diff across
      arrival processes is a diff of timing and of nothing else. That is only
      true if the population is identical across processes, so it is asserted
      here rather than trusted. */
const { chromium } = require("playwright");
const nodePath = require("path");
const arg = process.argv[2] || "visual-review/agent-model.html";

const URL = "file:///" + nodePath.resolve(arg).replace(/\\/g, "/");

async function runCfg(page, cfg) {
  return await page.evaluate(async (c) => {
    state.rung = c.rung; state.seed = c.seed; state.day = c.day;
    state.hour = c.hour; state.pop = c.pop;
    if (c.arrival) state.arrival = c.arrival;
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
    state.groups.forEach(g => { byGroup[g.id] = { d: +doseLeq(g).toFixed(6), sc: g.scenario,
                                                  replans: g.replans }; });
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
      // Identity of the population, independent of when anyone walked in.
      // If an arrival process changes any of these it is not a timing change.
      identity: state.pending.map(g =>
        [g.id, g.persona, g.size, g.scenario, g.ingress, g.egress,
         g.dogs, (g.plan || []).join(">")].join("|")).join(";"),
      spawnAt: state.spawnAt.map(t => +t.toFixed(3)),
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

    const base = { seed: 20260731, day: "Weekday", hour: 14, pop: 400,
                   arrival: "poisson" };

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
    // 2. THE LOAD-BEARING TEST. Switching the layer on must not move the dose of
    //    anyone whose itinerary it did not change -- EXCEPT through contention,
    //    which legitimately couples strangers to each other. Rerouting a dog
    //    walker frees a bench, and the person who gets that bench stays longer
    //    and accrues a different dose without anything about them changing.
    //    That is the race condition this model exists to demonstrate, so it is
    //    DISTINGUISHED rather than excused: a dose may move only if the group's
    //    re-plan count also moved. A dose that moves with the same plan, the
    //    same spawn time AND the same re-plan count means a random stream has
    //    desynchronised, and that is a defect.
    const cont = await runCfg(page, { ...base, rung: "contend" });
    let moved = 0, coupled = 0, sameScen = 0, changedScen = 0;
    const badMoves = [];
    for (const id in sens.byGroup) {
      const a = cont.byGroup[id], b = sens.byGroup[id];
      if (!a) { problems.push(theme + " :: group " + id + " missing from contend run"); continue; }
      if (a.sc !== b.sc) { changedScen++; continue; }
      sameScen++;
      if (a.d === b.d) continue;
      if (a.replans !== b.replans) { coupled++; continue; }
      moved++; badMoves.push(id);
    }
    if (moved > 0)
      problems.push(theme + " :: " + moved + " of " + sameScen +
        " unchanged-itinerary groups had their dose MOVED with no change in contention -> " +
        badMoves.slice(0, 3).join(", "));
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

    // 9. ARRIVAL PROCESSES MAY CHANGE TIMING AND NOTHING ELSE. The comparison
    //    card on the page claims a diff across processes is a diff of when
    //    people walked in. That claim is only true if the population is
    //    byte-identical across processes, so it is asserted rather than
    //    assumed: same ids, personas, party sizes, itineraries, gateways and
    //    dogs, with only the spawn schedule free to move.
    const arr = {};
    for (const a of ["ramp", "poisson", "burst"])
      arr[a] = await runCfg(page, { ...base, rung: "sensitive", arrival: a });
    for (const a of ["ramp", "burst"]) {
      if (arr[a].identity !== arr.poisson.identity)
        problems.push(theme + " :: arrival process '" + a +
          "' changed WHO is in the run, not just when they arrive");
      if (arr[a].people !== arr.poisson.people || arr[a].dogs !== arr.poisson.dogs)
        problems.push(theme + " :: arrival process '" + a + "' changed the headcount");
      if (JSON.stringify(arr[a].spawnAt) === JSON.stringify(arr.poisson.spawnAt))
        problems.push(theme + " :: arrival process '" + a +
          "' produced an identical spawn schedule to Poisson, so it is not doing anything");
      if (arr[a].zeroLen > 0)
        problems.push(theme + " :: arrival process '" + a + "' produced zero-length visits");
      if (!arr[a].done)
        problems.push(theme + " :: arrival process '" + a + "' did not drain inside the run");
    }
    // The ramp is deterministic by definition: evenly spaced, no random draw.
    const gaps = arr.ramp.spawnAt.slice(1).map((t, i) => +(t - arr.ramp.spawnAt[i]).toFixed(3));
    if (new Set(gaps).size !== 1)
      problems.push(theme + " :: the ramp is not evenly spaced (" + new Set(gaps).size + " distinct gaps)");
    // And bursting must actually bunch people, or the comparison is vacuous.
    const peak = s => { const b = {}; s.forEach(t => { const k = Math.floor(t / 60); b[k] = (b[k] || 0) + 1; });
                        return Math.max(...Object.values(b)); };
    const pR = peak(arr.ramp.spawnAt), pP = peak(arr.poisson.spawnAt), pB = peak(arr.burst.spawnAt);
    if (!(pB > pP && pP >= pR))
      problems.push(theme + " :: bunching is not ordered ramp<=poisson<burst (" +
        pR + ", " + pP + ", " + pB + ")");
    // Restore the page default before the render checks below.
    await page.evaluate(() => { state.arrival = "poisson"; });

    // 10. Panels render, in this theme, with no junk.
    await page.evaluate(() => { state.rung = "sensitive"; reset();
      let g = 0; while (!state.done && g++ < 400000) tickOnce(); redrawAll(); });
    for (const id of ["sensTable", "agencyTable", "sensPlaceTable", "sensDefTable", "arrivalTable"]) {
      const t = await page.$eval(id === "sensDefTable" ? "#sensDefTable" : "#" + id,
        el => el.innerText.trim());
      if (!t) problems.push(theme + " :: " + id + " is empty");
      if (/NaN|undefined|Infinity|\[object/.test(t))
        problems.push(theme + " :: " + id + " contains junk -> " +
          t.split("\n").find(l => /NaN|undefined|Infinity|\[object/.test(l)));
      const rows = await page.$$eval("#" + id + " tbody tr", r => r.length).catch(() => 0);
      if (id !== "agencyTable" && rows < 3) problems.push(theme + " :: " + id + " has only " + rows + " rows");
    }
    // The comparison button must run and populate the results columns.
    await page.click("#runArrivals");
    await page.waitForFunction(() => !document.getElementById("runArrivals").disabled,
                               null, { timeout: 120000 });
    const arrTxt = await page.$eval("#arrivalTable", el => el.innerText);
    const arrNote = await page.$eval("#arrivalNote", el => el.innerText);
    if (/NaN|undefined|Infinity|\[object/.test(arrTxt + arrNote))
      problems.push(theme + " :: arrival comparison contains junk");
    if (!/dose/i.test(arrNote) || !/\d/.test(arrNote))
      problems.push(theme + " :: arrival comparison note did not report a result -> " + arrNote);
    const cols = await page.$$eval("#arrivalTable thead th", h => h.length);
    if (cols < 7) problems.push(theme + " :: arrival comparison did not add result columns (" + cols + ")");
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
      "(" + sameScen + " same, " + coupled + " coupled via contention, " + changedScen + " rerouted)",
      "| peak/min ramp/pois/burst", pR + "/" + pP + "/" + pB);
    await page.close();
  }

  await browser.close();
  if (problems.length) { console.log("\nPROBLEMS (" + problems.length + ")");
    problems.forEach(p => console.log("  - " + p)); process.exit(1); }
  console.log("\nOK - susceptibility and arrival layers clean in both themes");
})();
