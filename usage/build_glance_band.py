"""Insert an at-a-glance infographic band at the top of the usage dashboard.

Idempotent: delimited by markers and rewritten in place, so re-running this
replaces the band rather than stacking another copy. Every number in it is
read from usage-data.json at page load by the page's own render(), not baked
in here - this script only installs the markup and the styling.
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(ROOT, "usage-dashboard.html")

OPEN, CLOSE = "<!--IGBAND-->", "<!--/IGBAND-->"

# A marker has to be a comment in the language it sits in. An HTML comment
# inside <style> is not a comment, it is a syntax error that most browsers
# silently swallow along with the rules that follow it - which would drop the
# band's styling and leave a correctly-populated but unstyled block.
#
# The open marker must also not be a SUBSTRING of the close marker, or the
# idempotence check counts the closer as a second opener and the block gets
# spliced at the wrong boundary on every re-run.
CSS_OPEN, CSS_CLOSE = "/*IGBAND-BEGIN*/", "/*IGBAND-END*/"
JS_OPEN, JS_CLOSE = "//IGBAND-BEGIN", "//IGBAND-END"

CSS = """
/* -- at-a-glance band ----------------------------------------------------
   The dashboard opens with sixteen sections of method. A reader who wants
   the result has to earn it, and most will not. This band carries the four
   numbers, the model split and the money split, and nothing else. */
.ig { margin: 22px 0 26px; }
.ig .igh {
  display: flex; align-items: baseline; gap: 12px; flex-wrap: wrap;
  margin: 0 0 14px;
}
.ig .igh h2 { margin: 0; font-size: 1.05rem; letter-spacing: 0.04em;
  text-transform: uppercase; color: var(--cp-text-muted); }
.ig .igh .igs { font-size: 0.84rem; color: var(--cp-text-soft); }

.ig .igbig {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(168px, 1fr));
  gap: 14px; margin-bottom: 18px;
}
.ig .igbig > div {
  background: var(--cp-surface); border: 1px solid var(--cp-border);
  border-radius: 14px; padding: 18px 18px 16px;
  box-shadow: 0 0 2px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.14);
}
.ig .igbig b { display: block; font-size: 2.05rem; line-height: 1.08;
  letter-spacing: -0.025em; color: var(--cp-accent); }
/* These two tiles used to carry a spelled-out date, which is fourteen
   characters where every other headline is three or four, and had to be set at
   roughly half size to fit. They now carry "Aug 1st" and "T+11", so they take
   the band's full headline size like everything beside them. nowrap stays:
   "Aug 1st" would otherwise break between the month and the day, which reads
   as two lines of nothing. The band's tiles get NARROWER above 1024px, because
   the grid answers width by adding columns - so this is set by the narrowest
   tile the band ever produces, not by the viewport. */
.ig .igbig b.dt { white-space: nowrap; }
.ig .igbig span { display: block; font-size: 0.76rem; margin-top: 6px;
  text-transform: uppercase; letter-spacing: 0.05em;
  color: var(--cp-text-muted); }
.ig .igbig em { display: block; font-style: normal; font-size: 0.82rem;
  color: var(--cp-text-soft); margin-top: 7px; }

.ig .igrow {
  background: var(--cp-surface); border: 1px solid var(--cp-border);
  border-radius: 14px; padding: 18px 20px; margin-bottom: 14px;
  box-shadow: 0 0 2px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.14);
}
.ig .igrow > h3 { margin: 0 0 12px; font-size: 0.78rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.06em;
  color: var(--cp-text-muted); }

/* Deliberately NOT .bar - this page uses .bar for the ledger charts and the
   masthead uses .mh-bar. A third meaning of the same class is how a stylesheet
   starts fighting itself. */
.ig .igm { display: grid; grid-template-columns: minmax(104px, 150px) 1fr auto;
  gap: 12px; align-items: center; padding: 4px 0; font-size: 0.87rem; }
.ig .igm .l { color: var(--cp-text); font-weight: 600;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.ig .igm .t { background: var(--cp-surface-soft); border-radius: 5px;
  height: 19px; overflow: hidden; border: 1px solid var(--cp-border); }
/* display:block is load-bearing, not decoration. A fill written as a <span>
   inside a track that is not a flex container stays inline, and an inline
   element ignores width and height - so it renders 0x0 while the track around
   it still paints. The chart then looks like an axis with no data rather than
   like a broken page, which is why forty of them shipped that way on this
   dashboard before anyone noticed. Blockifying here makes the rule correct for
   either a <span> or a <div>. */
.ig .igm .f { display: block; height: 100%; background: var(--cp-accent); }
.ig .igm .v { font-family: Consolas, "Courier New", Courier, monospace;
  font-size: 0.8rem; color: var(--cp-text-muted); min-width: 128px;
  text-align: right; }

.ig .igsplit { display: flex; height: 34px; border-radius: 9px;
  overflow: hidden; border: 1px solid var(--cp-border); }
.ig .igsplit div { display: flex; align-items: center; justify-content: center;
  font-size: 0.74rem; font-weight: 600; color: var(--cp-accent-fg);
  overflow: hidden; white-space: nowrap; }
.ig .iglg { display: flex; flex-wrap: wrap; gap: 15px; margin-top: 11px;
  font-size: 0.79rem; color: var(--cp-text-muted); }
.ig .iglg i { display: inline-block; width: 11px; height: 11px;
  border-radius: 3px; margin-right: 6px; vertical-align: -1px; }

.ig .igfind { margin: 12px 0 0; font-size: 0.88rem; line-height: 1.55;
  border-left: 3px solid var(--cp-accent); padding: 2px 0 2px 13px;
  color: var(--cp-text-muted); }
.ig .igfind b { color: var(--cp-text); }
"""

BODY = """
<div class="ig" id="igband">
  <div class="igh">
    <h2>At a glance</h2>
    <span class="igs">Every figure below is read from the client's own
      per-request log. The method, the caveats and the things this page got
      wrong are underneath.</span>
  </div>
  <div class="igbig" id="igbig"></div>

  <div class="igrow">
    <h3>Which models did the work</h3>
    <div id="igmodels"></div>
    <p class="igfind" id="igmodelfind"></p>
  </div>

  <div class="igrow">
    <h3>Where the money went</h3>
    <div class="igsplit" id="igmoney"></div>
    <div class="iglg" id="igmoneylg"></div>
    <p class="igfind" id="igmoneyfind"></p>
  </div>
</div>
"""

JS = """
// -- at-a-glance band ------------------------------------------------------
// Rendered from the same DATA object as the rest of the page, so the headline
// numbers cannot drift away from the detail underneath them.
function renderBand() {
  const d = DATA, t = d.totals, T = d.time, tk = t.tokens;
  const allTokens = tk.input + tk.cache_read + tk.cache_write + tk.output;
  const active = (T.active || []).find(a => a.cutoff_s === 300) ||
                 (T.active || [])[0] || null;
  // Dates are shown as plain calendar days in the zone the work happened in,
  // in the one format the whole page uses: 10-August-2026. "Aug 10, 2026" is
  // locale-bound and "10/8" is ambiguous between two continents.
  // A reader asking "is this current" is asking about the published work, so
  // last-updated is the last COMMIT where one exists, not the last request -
  // a session can burn requests without publishing a line.
  const D = d.dates || {};
  const MONTHS = ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November",
                  "December"];
  const day = iso => {
    if (!iso) return "\\u2014";
    const p = String(iso).slice(0, 10).split("-").map(Number);
    return p[2] + "-" + MONTHS[p[1] - 1] + "-" + p[0];
  };
  const updated = D.last_commit || D.last_request;

  // A DATE IS NOT A HEADLINE. Every other tile in this band leads with a
  // quantity and explains it underneath; these two led with a fourteen-
  // character string, which had to be set at half the size of its neighbours
  // to fit and so read as the least important thing in the row.
  //
  // They are now a matched pair: the day the work started, and how far from
  // it the last publication sits. A reader should not have to subtract two
  // dates in their head to learn the answer the band exists to give.
  //
  // THE FULL DATE IS NOT DROPPED, IT MOVES DOWN. "Aug 1st" on its own is
  // unreadable on a page opened in 2028, so the canonical 1-August-2026 sits
  // in the sub-line of both tiles - which also keeps the whole page in one
  // date format.
  const ORD = n => {
    const t = n % 100;
    if (t >= 11 && t <= 13) return n + "th";
    return n + (["th", "st", "nd", "rd"][n % 10] || "th");
  };
  const shortDay = iso => {
    if (!iso) return "\\u2014";
    const p = String(iso).slice(0, 10).split("-").map(Number);
    return MONTHS[p[1] - 1].slice(0, 3) + " " + ORD(p[2]);
  };
  // T+N COUNTS DAYS SPANNED, NOT DAYS ELAPSED, and the difference is not
  // pedantry: 1 to 11 August is ten days elapsed and eleven days spanned, so
  // the same pair of dates supports two different headline numbers. The
  // spanned count is used because it is the one already published beside it -
  // the tile to its left reads "10 of 11 days were active", which is what
  // tells a reader which convention T+ follows without a sentence spent on it.
  const spanDays = (a, b) => {
    if (!a || !b) return null;
    const x = String(a).slice(0, 10).split("-").map(Number);
    const y = String(b).slice(0, 10).split("-").map(Number);
    return Math.round((Date.UTC(y[0], y[1] - 1, y[2]) -
                       Date.UTC(x[0], x[1] - 1, x[2])) / 86400000) + 1;
  };
  const span = D.calendar_days || spanDays(D.started, updated);

  // WHOLE DOLLARS IN THE BAND ONLY. Cents are meaningless at a glance - the
  // reader is being told the order of magnitude of a bill, not reconciling it -
  // and ".12" on a four-figure number is two characters of noise in the widest
  // headline in the row. Every place the number is used as EVIDENCE still
  // carries cents: the tables, the per-model rows, the unit rates. This is
  // rounded for display and nothing is recomputed from it.
  const usd0 = x => (x > 0 && x < 0.5) ? "<$1" : "$" + n0(x);

  // WHEN THE LABEL SAYS FIVE REPOSITORIES, THE NUMBER BESIDE IT MUST COVER
  // FIVE REPOSITORIES. Merged usage makes the headline figures project-wide;
  // without it they are this repository's and the tile says the total is a
  // floor. Getting this pairing wrong would understate the project by more
  // than half while looking authoritative.
  const F = d.fleet;
  const bigUsd = F ? F.totals.usd : t.usd;  const bigReq = F ? F.totals.requests : t.requests;
  const bigTurns = F ? F.totals.turns : t.turns;
  const bigTok = F ? F.totals.tokens : allTokens;
  const bigHrs = F ? F.time.times[String(F.time.default_cutoff_s)].engaged_s / 3600
                   : (active ? active.active_s / 3600 : null);
  // Models used is a SET across repositories, not a sum: the sibling work
  // reached for one the primary session never used, and adding the counts
  // would have claimed nine of thirty-nine.
  const bigModels = F
    ? new Set([].concat(...F.sources.map(s => s.models || []))).size
    : t.models;
  // Commits across every repository named in the project, which is what the
  // scope list already computes - it reaches GitHub for the ones that are not
  // checked out here. Falls back to this repository's own count when there is
  // no scope list to ask.
  const allScope = (typeof SC !== "undefined" && SC)
    ? SC.entries.find(e => e.kind === "all") : null;
  const bigCommits = allScope && allScope.commits != null
    ? allScope.commits : d.outputs.commit_count;

  $("igbig").innerHTML = [
    [shortDay(D.started), "research started",
     day(D.started) + (D.active_days
        ? " \\u00b7 " + D.active_days + " of " + D.calendar_days + " days were active"
        : " \\u00b7 first request issued"), "dt"],
    [span ? "T+" + n0(span) : "\\u2014", "last updated",
     day(updated) + " \\u00b7 " +
     (D.last_commit ? "most recent commit" : "most recent model request"), "dt"],
    [usd0(bigUsd), "total metered cost",
     (F
        ? "across " + n0(F.totals.projects) + " repositories, " +
          usd0(t.usd) + " of it here"
        : (d.siblings && d.siblings.rows.length
             ? "a floor: " + n0(d.siblings.rows.length) + " sibling repos unmeasured"
             : n0(Math.round(t.aiu)) + " AI credits, at published rates"))],
    [n0(bigReq), "model requests",
     n0(bigTurns) + " human turns drove them"],
    [bigModels + " of " + d.catalogue.offered, "models used",
     d.catalogue.selectable + " were selectable"],
    [bigHrs === null ? "\\u2014" : n1(bigHrs) + " h", "engaged time",
     F ? n1(F.time.model_wall_s / 3600) + " h of it a model generating"
       : (active ? "over " + n1(T.wall_span_s / 3600) + " h of calendar"
                 : "not computed")],
    [n0(Math.round(bigTok / 1e6)) + "M", "tokens billed",
     F ? n0(Math.round(allTokens / 1e6)) + "M of them in this repository"
       : pct(tk.cache_read, allTokens) + " of them re-read from cache"],
    // COMMITS ARE POOLED AND WORDS ARE NOT, and the tile has to say so. It
    // used to print this repository's commit count beside a row of pooled
    // headlines, so the band read 55 commits while the cards below it read
    // 147 for the same selection. Commits are known for every repository
    // because they come from GitHub rather than from a checkout; words are
    // counted from a working tree, and only one of the five is checked out
    // here, so the count is named rather than quietly generalised.
    [n0(d.outputs.markdown_words), "words published",
     bigCommits == null ? "commits not counted"
       : n0(bigCommits) + " commits" +
         (F ? " \\u00b7 words counted in 1 of " + n0(F.totals.projects) +
              " repositories" : "")]
  ].map(([b, s, e, k]) =>
    `<div><b class="${k || ""}">${esc(b)}</b><span>${esc(s)}</span><em>${esc(e)}</em></div>`
  ).join("");

  // Models, biggest first, measured by spend rather than by request count -
  // requests are not equal in size and ranking by them flatters the cheap one.
  //
  // POOLED, BECAUSE THE TILES ABOVE ARE POOLED. This row used to read the
  // primary repository's split while the tile directly above it counted models
  // across all five, so the row summed to $675 under a headline of $1,559 and
  // showed four models beside a tile saying five. Both panels now answer the
  // same question about the same repositories.
  const ms = (F && F.models ? F.models : d.models)
    .slice().sort((a, b) => b.usd - a.usd);
  const msReq = F ? F.totals.requests : t.requests;
  const top = ms.length ? ms[0].usd : 1;
  $("igmodels").innerHTML = ms.map(m => `
    <div class="igm">
      <span class="l" title="${esc(m.model)}">${esc(m.model)}</span>
      <span class="t"><span class="f" style="width:${(100 * m.usd / top).toFixed(2)}%"></span></span>
      <span class="v">${usd(m.usd)} &middot; ${n0(m.requests)} req</span>
    </div>`).join("");

  // The delegation identity. Asserted from the data rather than typed, and it
  // says nothing at all if the identity does not hold.
  //
  // Sub-agent counts are the one thing here that does NOT pool cleanly: a
  // contribution records which of its requests ran inside a sub-agent but not
  // which model or which agent, so the identity below can only be tested on
  // the repository whose agents are named. It is therefore tested on the
  // primary and stated as such; the pooled count is reported beside it.
  const subReq = (d.agents || []).reduce((s, a) => s + a.requests, 0);
  // The page defines MAIN; the band must not depend on that having happened.
  const bandMain = (typeof SC !== "undefined" && SC)
    ? SC.main : (d.project.repository || d.project.name);
  const fleetSub = F && F.totals.subagent_requests != null
    ? F.totals.subagent_requests : subReq;
  const subModels = [...new Set((d.agents || []).flatMap(a => a.models || []))];
  const pModels = d.models.slice().sort((a, b) => b.usd - a.usd);
  const delegated = pModels.filter(m => subModels.includes(m.model));
  const exact = subModels.length === 1 && delegated.length === 1 &&
                delegated[0].requests === subReq && subReq > 0;
  $("igmodelfind").innerHTML = exact
    ? `<b>The model split is exactly the delegation boundary.</b> In
       <code>${esc(bandMain)}</code> all ${n0(subReq)}
       <code>${esc(subModels[0])}</code> requests are sub-agent requests
       &mdash; it never ran on the main thread, and the main model never ran
       inside a sub-agent. The second model is not a second opinion; it is
       ${d.totals.subagents} delegated searches.`
    : `${n0(fleetSub)} of ${n0(msReq)} requests ran inside sub-agents.`;

  // Money by channel, pooled across models AND across repositories. Cache read
  // is the cheapest token there is and still the largest line, which is the
  // whole point. A contribution states no per-request price, so its split
  // comes from the aggregate its exporter wrote; the merge checks that the
  // four channels add up to the fleet's own bill before any of this renders.
  const byType = {};
  ((F && F.channels) ? F.channels : (d.channels || [])).forEach(c => {
    byType[c.type] = (byType[c.type] || 0) + c.usd;
  });
  const LABEL = {
    cache_read: "reading what it already sent",
    cache_write: "putting context into cache",
    output: "writing",
    input: "fresh input"
  };
  const COLOR = {
    cache_read: "var(--cp-accent)",
    cache_write: "var(--cp-accent-muted, #6e7781)",
    output: "var(--cp-success)",
    input: "var(--cp-warning)"
  };
  const rows = Object.entries(byType).sort((a, b) => b[1] - a[1]);
  const sum = rows.reduce((s, r) => s + r[1], 0) || 1;
  $("igmoney").innerHTML = rows.map(([k, v]) => {
    const w = 100 * v / sum;
    return `<div style="width:${w.toFixed(2)}%;background:${COLOR[k] || "var(--cp-accent)"}"
            title="${esc(LABEL[k] || k)}: ${usd(v)}">${w > 9 ? w.toFixed(0) + "%" : ""}</div>`;
  }).join("");
  $("igmoneylg").innerHTML = rows.map(([k, v]) =>
    `<span><i style="background:${COLOR[k] || "var(--cp-accent)"}"></i>${esc(LABEL[k] || k)} &mdash; ${usd(v)}</span>`
  ).join("");

  // Pooled counterfactual and pooled output share, so this sentence describes
  // the same bar it sits under. The output share is read from the same channel
  // rows the bar is drawn from rather than from the primary token totals,
  // which is what kept it consistent when the bar went project-wide.
  const cf = (F && F.counterfactual) ? F.counterfactual : (d.counterfactual || {});
  const chTok = {};
  ((F && F.channels) ? F.channels : (d.channels || [])).forEach(c => {
    chTok[c.type] = (chTok[c.type] || 0) + c.tokens;
  });
  const chAll = Object.values(chTok).reduce((s, v) => s + v, 0) || allTokens;
  const wrote = pct(chTok.output || tk.output, chAll);
  $("igmoneyfind").innerHTML = cf.uncached_usd
    ? `<b>Most of the bill is re-reading.</b> An agent's context is resent on
       every request, so the same words are paid for again and again. Caching
       held that to ${usd(cf.actual_usd)}; without it the identical work would
       have listed at <b>${usd(cf.uncached_usd)}</b>, or
       ${cf.ratio.toFixed(1)}&times; more. What the model actually wrote is
       ${wrote} of the tokens.`
    : `What the model actually wrote is ${wrote} of the tokens billed.`;
}
"""


def replace_block(text, o, c, payload):
    """Replace a marked block if present, else return None."""
    if o not in text:
        return None
    a = text.index(o)
    b = text.index(c) + len(c)
    return text[:a] + o + payload + c + text[b:]


def main():
    with io.open(PAGE, encoding="utf-8") as fh:
        t = fh.read()
    before = t

    # Guard every assumption this script makes about the page. Each one fails
    # silently: a missing anchor splices into the wrong place, and a renamed
    # helper produces a band that is present in the DOM, correctly styled, and
    # permanently empty - with no console error.
    for need in ("</style>", '<div class="wrap">', "function render() {",
                 '$("whyusd").textContent', "const usd =", "const esc =",
                 "const n0 =", "const n1 =", "const pct ="):
        if need not in t:
            raise SystemExit("usage-dashboard.html has no %r - the page "
                             "changed shape, refusing to guess" % need)

    if OPEN in t:
        for name, o, c, payload in (("css", CSS_OPEN, CSS_CLOSE, CSS),
                                    ("html", OPEN, CLOSE, BODY),
                                    ("js", JS_OPEN, JS_CLOSE, JS)):
            r = replace_block(t, o, c, payload)
            if r is None:
                raise SystemExit("page carries the HTML marker but not the %s "
                                 "marker - it is half-installed" % name)
            t = r
        action = "updated"
    else:
        t = t.replace("</style>", CSS_OPEN + CSS + CSS_CLOSE + "\n</style>", 1)
        anchor = '<div class="wrap">'
        i = t.index(anchor)
        t = t[:i + len(anchor)] + "\n" + OPEN + BODY + CLOSE + t[i + len(anchor):]
        t = t.replace("function render() {",
                      JS_OPEN + JS + JS_CLOSE + "\nfunction render() {", 1)
        t = t.replace('$("whyusd").textContent',
                      'renderBand();\n  $("whyusd").textContent', 1)
        action = "installed"

    # Post-conditions, each guarding a specific silent failure.
    if t.count("renderBand()") < 2:
        raise SystemExit("renderBand is defined but never called - the band "
                         "would render empty")
    for name, o, c in (("html", OPEN, CLOSE), ("css", CSS_OPEN, CSS_CLOSE),
                       ("js", JS_OPEN, JS_CLOSE)):
        if t.count(o) != 1 or t.count(c) != 1:
            raise SystemExit("%s markers appear %dx/%dx, expected 1/1"
                             % (name, t.count(o), t.count(c)))
    if t.index(CSS_OPEN) > t.index("</style>"):
        raise SystemExit("CSS block landed outside <style>")
    if t == before:
        # Not an error any more. As a scratch one-shot installer, an unchanged
        # page meant the injection had silently missed, so this exited non-zero.
        # As a build step it is the normal result of rebuilding when the source
        # numbers have not moved, and every guard above has already passed by
        # the time we get here.
        print("band already current: %s" % os.path.basename(PAGE))
        return

    with io.open(PAGE, "w", encoding="utf-8", newline="") as fh:
        fh.write(t)
    print("band %s: %s (%d -> %d bytes)"
          % (action, os.path.basename(PAGE), len(before), len(t)))


if __name__ == "__main__":
    main()