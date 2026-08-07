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
/* A date is eleven characters where every other headline is three or four, so
   it wraps in a tile sized for a number. Smaller here rather than a wider
   tile: widening the minimum would re-flow the whole band to fit two cells
   that are the least important thing in it. */
.ig .igbig b.dt { font-size: 1.42rem; letter-spacing: -0.01em; }
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
  // Dates are shown as plain calendar days in the zone the work happened in.
  // A reader asking "is this current" is asking about the published work, so
  // last-updated is the last COMMIT where one exists, not the last request -
  // a session can burn requests without publishing a line.
  const D = d.dates || {};
  const day = iso => {
    if (!iso) return "\\u2014";
    const p = String(iso).slice(0, 10).split("-").map(Number);
    return new Date(p[0], p[1] - 1, p[2]).toLocaleDateString("en-US",
      { year: "numeric", month: "short", day: "numeric" });
  };
  const updated = D.last_commit || D.last_request;

  $("igbig").innerHTML = [
    [day(D.started), "research started",
     D.active_days ? D.active_days + " active days over " + D.calendar_days + " calendar days"
                   : "first request issued", "dt"],
    [day(updated), "last updated",
     D.last_commit ? "most recent commit" : "most recent model request", "dt"],
    [usd(t.usd), "total metered cost",
     n0(Math.round(t.aiu)) + " AI credits, at published rates"],
    [n0(t.requests), "model requests",
     n0(t.turns) + " human turns drove them"],
    [t.models + " of " + d.catalogue.offered, "models used",
     d.catalogue.selectable + " were selectable"],
    [active ? n1(active.active_s / 3600) + " h" : "\\u2014", "active time",
     active ? "over " + n1(T.wall_span_s / 3600) + " h of calendar"
            : "not computed"],
    [n0(Math.round(allTokens / 1e6)) + "M", "tokens billed",
     pct(tk.cache_read, allTokens) + " of them re-read from cache"],
    [n0(d.outputs.markdown_words), "words published",
     n0(d.outputs.commit_count) + " commits"]
  ].map(([b, s, e, k]) =>
    `<div><b class="${k || ""}">${esc(b)}</b><span>${esc(s)}</span><em>${esc(e)}</em></div>`
  ).join("");

  // Models, biggest first, measured by spend rather than by request count -
  // requests are not equal in size and ranking by them flatters the cheap one.
  const ms = d.models.slice().sort((a, b) => b.usd - a.usd);
  const top = ms.length ? ms[0].usd : 1;
  $("igmodels").innerHTML = ms.map(m => `
    <div class="igm">
      <span class="l" title="${esc(m.model)}">${esc(m.model)}</span>
      <span class="t"><span class="f" style="width:${(100 * m.usd / top).toFixed(2)}%"></span></span>
      <span class="v">${usd(m.usd)} &middot; ${n0(m.requests)} req</span>
    </div>`).join("");

  // The delegation identity. Asserted from the data rather than typed, and it
  // says nothing at all if the identity does not hold.
  const subReq = (d.agents || []).reduce((s, a) => s + a.requests, 0);
  const subModels = [...new Set((d.agents || []).flatMap(a => a.models || []))];
  const delegated = ms.filter(m => subModels.includes(m.model));
  const exact = subModels.length === 1 && delegated.length === 1 &&
                delegated[0].requests === subReq && subReq > 0;
  $("igmodelfind").innerHTML = exact
    ? `<b>The model split is exactly the delegation boundary.</b> All
       ${n0(subReq)} <code>${esc(subModels[0])}</code> requests are sub-agent
       requests &mdash; it never ran on the main thread, and the main model
       never ran inside a sub-agent. The second model is not a second opinion;
       it is ${d.totals.subagents} delegated searches.`
    : `${n0(subReq)} of ${n0(t.requests)} requests ran inside
       ${d.totals.subagents} sub-agents.`;

  // Money by channel, pooled across models. Cache read is the cheapest token
  // there is and still the largest line, which is the whole point.
  const byType = {};
  (d.channels || []).forEach(c => {
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

  const cf = d.counterfactual || {};
  $("igmoneyfind").innerHTML = cf.uncached_usd
    ? `<b>Most of the bill is re-reading.</b> An agent's context is resent on
       every request, so the same words are paid for again and again. Caching
       held that to ${usd(cf.actual_usd)}; without it the identical work would
       have listed at <b>${usd(cf.uncached_usd)}</b>, or
       ${cf.ratio.toFixed(1)}&times; more. What the model actually wrote is
       ${pct(tk.output, allTokens)} of the tokens.`
    : `What the model actually wrote is ${pct(tk.output, allTokens)} of the
       tokens billed.`;
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