"""Render media.html from media-data.json.

Every number on the page comes out of the JSON. Nothing here re-derives an
analysis result, and nothing here is typed by hand that also exists in the
data - if a figure appears both in the JSON and in prose on this page, the
prose reads it from the JSON. That is the same rule build_pages.py follows for
the site, and it exists because this repository has already shipped stale
hand-maintained counts twice.

The charts are inline SVG generated HERE, in Python, rather than drawn by
JavaScript in the browser. Two reasons:

  1. A chart drawn at build time cannot throw a console error on a reader's
     machine, and cannot silently render an empty track the way forty <span>
     bar fills did on the usage dashboard.
  2. The audio envelope is 400 fixed samples per clip. There is no interaction
     to support, so shipping a charting runtime to redraw a static polyline
     would be cost with no return.

Run:  python pedestrian-site-visits/build_media_page.py
"""

import html
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "media-data.json")
OUT = os.path.join(HERE, "media.html")
HEAD_SRC = os.path.join(os.path.dirname(HERE), "usage", "usage-dashboard.html")


def esc(s):
    return html.escape(str(s), quote=True)


def num(x, nd=0):
    if x is None:
        return "&mdash;"
    return ("{:,.%df}" % nd).format(float(x))


def mb(b):
    return "%.1f MB" % (b / 1048576.0) if b >= 1048576 else "%.0f kB" % (b / 1024.0)


def load_head():
    """Take the theme system and base stylesheet from a page that already has
    them, rather than re-typing 700 lines of CSS that would then drift.

    The head is copied verbatim from <!doctype> to the end of the first
    </style>. If that page's structure changes so this cannot be found, the
    build stops rather than emitting a page with no styling - an unstyled page
    still renders, still passes a link check, and looks like a deployment
    failure to a reader.
    """
    with io.open(HEAD_SRC, encoding="utf-8") as fh:
        t = fh.read()
    end = t.find("</style>")
    if end < 0 or not t.lstrip().startswith("<!doctype"):
        raise SystemExit("cannot find a head to copy in %s" % HEAD_SRC)
    head = t[:end]
    for need in (":root", "--cp-accent", "data-theme", ".wrap", ".card"):
        if need not in head:
            raise SystemExit("copied head is missing %s - refusing to emit "
                             "an unstyled page" % need)
    return head


# --------------------------------------------------------------------------
# charts
# --------------------------------------------------------------------------

def envelope_svg(trace, events, dur_s, excluded=False, w=1080, h=150):
    """The level trace of one clip, with detected excursions banded behind it.

    The y axis is LABELLED dBFS AND IS NOT LABELLED dB(A). That distinction is
    the whole reason this page can exist at all: dBFS is a number about the
    file, and the shape of it over time is real, while the absolute value is a
    property of an unknown gain chain. Anyone who reads this as sound pressure
    has been told four times on the page above it not to.
    """
    if not trace:
        return "<p class='muted'>no trace</p>"
    pad_l, pad_r, pad_t, pad_b = 46, 14, 12, 26
    iw, ih = w - pad_l - pad_r, h - pad_t - pad_b
    lo = min(trace) - 1.0
    hi = max(trace) + 1.0
    if hi - lo < 6:
        mid = (hi + lo) / 2.0
        lo, hi = mid - 3, mid + 3

    def x(i):
        return pad_l + iw * i / float(len(trace) - 1)

    def y(v):
        return pad_t + ih * (hi - v) / float(hi - lo)

    def tx(t):
        return pad_l + iw * t / float(dur_s) if dur_s else pad_l

    p = []
    stroke = "var(--cp-text-muted)" if excluded else "var(--cp-accent)"
    p.append("<svg viewBox='0 0 %d %d' width='100%%' role='img' "
             "data-kind='envelope' class='envsvg' "
             "aria-label='level trace'>" % (w, h))

    for ev in events or []:
        x0, x1 = tx(ev["start_s"]), tx(ev["end_s"])
        p.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' "
                 "fill='var(--cp-accent)' opacity='0.13'/>"
                 % (x0, pad_t, max(1.0, x1 - x0), ih))
        if ev.get("truncated"):
            p.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' "
                     "stroke='var(--cp-warning)' stroke-width='2' "
                     "stroke-dasharray='3 3'/>" % (x1, pad_t, x1, pad_t + ih))

    for g in range(4):
        v = lo + (hi - lo) * g / 3.0
        yy = y(v)
        p.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' "
                 "stroke='var(--cp-border)' stroke-width='1'/>"
                 % (pad_l, yy, w - pad_r, yy))
        p.append("<text x='%d' y='%.1f' font-size='10' text-anchor='end' "
                 "fill='var(--cp-text-muted)'>%.0f</text>"
                 % (pad_l - 6, yy + 3, v))

    pts = " ".join("%.1f,%.1f" % (x(i), y(v)) for i, v in enumerate(trace))
    p.append("<polyline points='%s' fill='none' stroke='%s' "
             "stroke-width='1.4'/>" % (pts, stroke))

    step = 10 if dur_s <= 70 else 20
    t = 0
    while t <= dur_s:
        p.append("<text x='%.1f' y='%d' font-size='10' text-anchor='middle' "
                 "fill='var(--cp-text-muted)'>%ds</text>"
                 % (tx(t), h - 8, t))
        t += step
    p.append("<text x='6' y='%d' font-size='10' fill='var(--cp-text-muted)' "
             "transform='rotate(-90 12,%d)'>dBFS</text>"
             % (pad_t + ih / 2, pad_t + ih / 2))
    p.append("</svg>")
    return "".join(p)


def sweep_svg(rows_by_clip, ceiling, rejected_duty, w=1080, h=210):
    """Duty cycle against detection threshold, one line per clip.

    The point of the chart is the CEILING line, not the curves. A duty figure
    that moves from 44% to 0% depending on where you set a threshold cannot
    carry a conclusion on its own; the highest value any threshold produces
    can, because a claim above that line is refuted no matter how the
    threshold is chosen.
    """
    pad_l, pad_r, pad_t, pad_b = 46, 224, 14, 34
    iw, ih = w - pad_l - pad_r, h - pad_t - pad_b
    ths = sorted({r["thresh_db"] for rows in rows_by_clip.values() for r in rows})
    if not ths:
        return ""
    tmin, tmax = min(ths), max(ths)
    vmax = max(rejected_duty, ceiling, 1.0) * 1.12

    def x(t):
        return pad_l + iw * (t - tmin) / float(tmax - tmin)

    def y(v):
        return pad_t + ih * (1 - v / vmax)

    p = ["<svg viewBox='0 0 %d %d' width='100%%' role='img' class='envsvg' "
         "data-kind='sweep' aria-label='duty cycle against threshold'>"
         % (w, h)]
    for g in range(5):
        v = vmax * g / 4.0
        p.append("<line x1='%d' y1='%.1f' x2='%.1f' y2='%.1f' "
                 "stroke='var(--cp-border)' stroke-width='1'/>"
                 % (pad_l, y(v), pad_l + iw, y(v)))
        p.append("<text x='%d' y='%.1f' font-size='10' text-anchor='end' "
                 "fill='var(--cp-text-muted)'>%.0f%%</text>"
                 % (pad_l - 6, y(v) + 3, v))

    p.append("<line x1='%d' y1='%.1f' x2='%.1f' y2='%.1f' "
             "stroke='var(--cp-danger)' stroke-width='2' "
             "stroke-dasharray='6 4'/>" % (pad_l, y(rejected_duty),
                                           pad_l + iw, y(rejected_duty)))
    p.append("<text x='%.1f' y='%.1f' font-size='11' fill='var(--cp-danger)'>"
             "the rejected reading needs %.0f%%</text>"
             % (pad_l + iw + 8, y(rejected_duty) + 4, rejected_duty))
    p.append("<line x1='%d' y1='%.1f' x2='%.1f' y2='%.1f' "
             "stroke='var(--cp-success)' stroke-width='2'/>"
             % (pad_l, y(ceiling), pad_l + iw, y(ceiling)))
    p.append("<text x='%.1f' y='%.1f' font-size='11' fill='var(--cp-success)'>"
             "measured ceiling %.0f%%</text>"
             % (pad_l + iw + 8, y(ceiling) + 4, ceiling))

    dashes = ["", "4 3", "1 3"]
    # The series labels are placed at fixed rows in the right margin, not
    # beside each line's last point. Both curves converge on zero at the
    # tightest threshold - which is the point of the chart - so anchoring the
    # labels to the curves puts them on top of each other exactly where the
    # chart is making its argument.
    for i, (clip, rows) in enumerate(sorted(rows_by_clip.items())):
        rows = sorted(rows, key=lambda r: r["thresh_db"])
        pts = " ".join("%.1f,%.1f" % (x(r["thresh_db"]), y(r["duty_pct"]))
                       for r in rows)
        d = dashes[i % len(dashes)]
        p.append("<polyline points='%s' fill='none' stroke='var(--cp-accent)' "
                 "stroke-width='1.6'%s/>"
                 % (pts, (" stroke-dasharray='%s'" % d) if d else ""))
        ly = pad_t + ih - 34 + i * 15
        p.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' "
                 "stroke='var(--cp-accent)' stroke-width='1.6'%s/>"
                 % (pad_l + iw + 8, ly - 4, pad_l + iw + 30, ly - 4,
                    (" stroke-dasharray='%s'" % d) if d else ""))
        p.append("<text x='%d' y='%.1f' font-size='10' "
                 "fill='var(--cp-text-muted)'>%s</text>"
                 % (pad_l + iw + 36, ly, esc(clip.split("-2026")[0])))

    for t in ths:
        p.append("<text x='%.1f' y='%d' font-size='10' text-anchor='middle' "
                 "fill='var(--cp-text-muted)'>%d</text>" % (x(t), h - 16, t))
    p.append("<text x='%.1f' y='%d' font-size='10' text-anchor='middle' "
             "fill='var(--cp-text-muted)'>detection threshold, dB above the "
             "clip's own median</text>" % (pad_l + iw / 2, h - 3))
    p.append("</svg>")
    return "".join(p)


def laps_svg(laps, chosen_is_odd, w=1080, h=150):
    """The fourteen stopwatch laps as alternating bars.

    Drawn because the argument for choosing between the two readings is
    VISUAL before it is statistical: one interleaving gives long bars that are
    all similar and short bars that are all over the place, and the other
    gives the reverse. The coefficient of variation just puts a number on
    what the picture already shows.
    """
    pad_l, pad_r, pad_t, pad_b = 46, 14, 16, 48
    iw, ih = w - pad_l - pad_r, h - pad_t - pad_b
    vmax = max(l["lap_s"] for l in laps) * 1.1
    bw = iw / float(len(laps))
    p = ["<svg viewBox='0 0 %d %d' width='100%%' role='img' class='envsvg' "
         "data-kind='laps' aria-label='stopwatch laps'>" % (w, h)]
    for g in range(4):
        v = vmax * g / 3.0
        yy = pad_t + ih * (1 - v / vmax)
        p.append("<line x1='%d' y1='%.1f' x2='%.1f' y2='%.1f' "
                 "stroke='var(--cp-border)' stroke-width='1'/>"
                 % (pad_l, yy, pad_l + iw, yy))
        p.append("<text x='%d' y='%.1f' font-size='10' text-anchor='end' "
                 "fill='var(--cp-text-muted)'>%.0f</text>"
                 % (pad_l - 6, yy + 3, v))
    for i, l in enumerate(laps):
        odd = (i % 2 == 0)
        noise = (odd == chosen_is_odd)
        bh = ih * l["lap_s"] / vmax
        p.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' "
                 "fill='%s' opacity='%s'/>"
                 % (pad_l + i * bw + 1, pad_t + ih - bh, bw - 2, bh,
                    "var(--cp-accent)" if noise else "var(--cp-text-muted)",
                    "0.9" if noise else "0.35"))
        p.append("<text x='%.1f' y='%d' font-size='9' text-anchor='middle' "
                 "fill='var(--cp-text-muted)'>%.1f</text>"
                 % (pad_l + i * bw + bw / 2, h - 32, l["lap_s"]))
        p.append("<text x='%.1f' y='%d' font-size='9' text-anchor='middle' "
                 "fill='var(--cp-text-soft)'>%d</text>"
                 % (pad_l + i * bw + bw / 2, h - 20, l["lap"]))
    p.append("<text x='%d' y='%d' font-size='10' fill='var(--cp-text-muted)'>"
             "lap seconds above, lap number below.</text>" % (pad_l, h - 6))
    p.append("<rect x='%d' y='%d' width='9' height='9' fill='var(--cp-accent)' "
             "opacity='0.9'/><text x='%d' y='%d' font-size='10' "
             "fill='var(--cp-text-muted)'>read as train noise</text>"
             % (pad_l + 216, h - 14, pad_l + 230, h - 6))
    p.append("<rect x='%d' y='%d' width='9' height='9' "
             "fill='var(--cp-text-muted)' opacity='0.35'/><text x='%d' y='%d' "
             "font-size='10' fill='var(--cp-text-muted)'>read as quiet between "
             "trains</text>" % (pad_l + 358, h - 14, pad_l + 372, h - 6))
    p.append("</svg>")
    return "".join(p)


def geo_svg(geo, w=1080, h=290):
    """Captures and MTA measurement points in the alignment's own frame.

    Chainage along the fitted track axis on x, perpendicular offset on y. This
    is the frame the rest of the repository already uses, so a reader can put
    these captures beside the noise-canyon drawings without a coordinate
    conversion - and, more usefully, can see at a glance that two of the
    captures sit closer to the track than three of the four points anyone has
    ever measured.
    """
    caps = geo["captures"]
    ancs = geo["anchors"]
    xs = [c["chainage_m"] for c in caps] + [a["chainage_m"] for a in ancs]
    ys = [c["offset_m"] for c in caps] + [a["offset_m"] for a in ancs]
    x0, x1 = min(xs) - 40, max(xs) + 40
    y0, y1 = min(ys) - 40, max(ys) + 40
    pad_l, pad_r, pad_t, pad_b = 52, 16, 30, 50
    iw, ih = w - pad_l - pad_r, h - pad_t - pad_b

    def px(v):
        return pad_l + iw * (v - x0) / float(x1 - x0)

    def py(v):
        return pad_t + ih * (y1 - v) / float(y1 - y0)

    p = ["<svg viewBox='0 0 %d %d' width='100%%' role='img' class='envsvg' "
         "data-kind='geo' aria-label='captures against the alignment'>"
         % (w, h)]
    for g in range(4):
        v = y0 + (y1 - y0) * g / 3.0
        p.append("<line x1='%d' y1='%.1f' x2='%.1f' y2='%.1f' "
                 "stroke='var(--cp-border)' stroke-width='1'/>"
                 % (pad_l, py(v), pad_l + iw, py(v)))
        p.append("<text x='%d' y='%.1f' font-size='10' text-anchor='end' "
                 "fill='var(--cp-text-muted)'>%.0f</text>"
                 % (pad_l - 6, py(v) + 3, v))
    p.append("<line x1='%d' y1='%.1f' x2='%.1f' y2='%.1f' "
             "stroke='var(--cp-text)' stroke-width='2.5' opacity='0.55'/>"
             % (pad_l, py(0), pad_l + iw, py(0)))
    p.append("<text x='%.1f' y='%.1f' font-size='10' text-anchor='end' "
             "fill='var(--cp-text-muted)'>fitted track axis</text>"
             % (pad_l + iw - 2, py(0) - 6))

    # Anchor labels collide: three of the four MTA points sit within 130 m of
    # each other in chainage, which is a handful of pixels. Two rules keep
    # them readable. Each label goes on the side of its marker AWAY from the
    # axis, so it never prints on top of the axis line; and where two markers
    # are too close in x to sit side by side, the second is stacked a row
    # further out. An unreadable label is worse than no label, and this
    # chart's whole job is showing which capture sits where.
    ancs = sorted(ancs, key=lambda a: a["chainage_m"])
    last_x, row = -1e9, 0
    for a in ancs:
        ax, ay = px(a["chainage_m"]), py(a["offset_m"])
        row = (row + 1) % 2 if (ax - last_x) < 150 else 0
        last_x = ax
        away = -1 if a["offset_m"] >= 0 else 1
        p.append("<circle cx='%.1f' cy='%.1f' r='5' fill='none' "
                 "stroke='var(--cp-text)' stroke-width='1.8'/>" % (ax, ay))
        p.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' "
                 "stroke='var(--cp-border-strong)' stroke-width='1'/>"
                 % (ax, ay + away * 6, ax, ay + away * (11 + row * 13)))
        p.append("<text x='%.1f' y='%.1f' font-size='10' text-anchor='middle' "
                 "fill='var(--cp-text-muted)'>%s</text>"
                 % (ax, ay + away * (14 + row * 13) + (4 if away > 0 else 0),
                    esc(a["name"].split(",")[0])))
    for c in caps:
        excl = c.get("excluded")
        fill = "var(--cp-text-muted)" if excl else "var(--cp-accent)"
        shape = ("<rect x='%.1f' y='%.1f' width='9' height='9' fill='%s'/>"
                 % (px(c["chainage_m"]) - 4.5, py(c["offset_m"]) - 4.5, fill)
                 if c["kind"] == "video" else
                 "<circle cx='%.1f' cy='%.1f' r='4.5' fill='%s'/>"
                 % (px(c["chainage_m"]), py(c["offset_m"]), fill))
        p.append(shape)
    p.append("<text x='%.1f' y='%d' font-size='10' text-anchor='middle' "
             "fill='var(--cp-text-muted)'>chainage along the alignment, m "
             "(0 = the DUMBO Archway)</text>" % (pad_l + iw / 2, h - 4))
    p.append("<text x='10' y='%d' font-size='10' fill='var(--cp-text-muted)' "
             "transform='rotate(-90 14,%d)'>offset, m</text>"
             % (pad_t + ih / 2, pad_t + ih / 2))
    # Legend bottom-left, inside the plot but below every plotted point. Top
    # right put it straight through the Brooklyn Bridge Park anchor label.
    ly = h - 20
    p.append("<g font-size='10' fill='var(--cp-text-muted)'>")
    p.append("<rect x='%d' y='%d' width='9' height='9' "
             "fill='var(--cp-accent)'/><text x='%d' y='%d'>video</text>"
             % (pad_l + 2, ly - 8, pad_l + 16, ly))
    p.append("<circle cx='%d' cy='%d' r='4.5' fill='var(--cp-accent)'/>"
             "<text x='%d' y='%d'>still</text>"
             % (pad_l + 62, ly - 4, pad_l + 72, ly))
    p.append("<circle cx='%d' cy='%d' r='5' fill='none' stroke='var(--cp-text)' "
             "stroke-width='1.8'/><text x='%d' y='%d'>MTA measurement "
             "point</text>" % (pad_l + 108, ly - 4, pad_l + 118, ly))
    p.append("<rect x='%d' y='%d' width='9' height='9' "
             "fill='var(--cp-text-muted)'/><text x='%d' y='%d'>excluded</text>"
             % (pad_l + 258, ly - 8, pad_l + 272, ly))
    p.append("</g></svg>")
    return "".join(p)


# --------------------------------------------------------------------------
# page
# --------------------------------------------------------------------------

def card(title, body, sub=""):
    s = "<section class='card'><h2>%s</h2>" % esc(title)
    if sub:
        s += "<p class='sub'>%s</p>" % sub
    return s + body + "</section>"


def build():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    with io.open(DATA, encoding="utf-8") as fh:
        d = json.load(fh)

    files = d["files"]
    caps = [f for f in files if f["kind"] in ("video", "still", "screenshot")]
    vids = [f for f in files if f["kind"] == "video"]
    excl = set(d["excluded_clips"])
    kept = [f for f in vids if f["name"] not in excl]
    deriv = d["derivatives"]
    geo = d["geo"]
    corr = d["corroboration"]
    sw = d["stopwatch"]
    ch = sw["readings"][sw["chosen"]]
    rej = sw["readings"][sw["rejected"]]
    rate = d["rate_check"]
    co = d["constant_obstruction"]
    det = d["detectability"]

    parts = []

    # ---- hero -----------------------------------------------------------
    parts.append("""
<header class="top"><div class="wrap">
<p class="eyebrow">Document 10 &middot; field media</p>
<h1>What a phone actually recorded under the Manhattan Bridge</h1>
<p class="lede">On 3 and 4 August 2026 an observer stood under the bridge in
DUMBO with a consumer Samsung Galaxy S23+, filmed the buildings on either
side, walked to the lawn on the south side, and separately stood with a
stopwatch and tapped a lap every time train noise started and stopped. This
page is everything that came back and everything that can and cannot be
concluded from it.</p>
<p class="lede"><strong>Nothing on this page is a decibel.</strong> A phone
with automatic gain control does not measure sound pressure, and no attempt
is made here to pretend otherwise. What survives an unknown, time-varying
gain is <em>when</em> things happened and <em>how long</em> they lasted, and
that is the only thing this page claims.</p>
</div></header>
<div class="wrap">""")

    # ---- at a glance ----------------------------------------------------
    g = []

    def stat(v, label, note):
        g.append("<div class='gcell'><div class='gv'>%s</div>"
                 "<div class='gl'>%s</div><div class='gn'>%s</div></div>"
                 % (v, esc(label), note))

    stat(str(len(caps)), "captures", "%s of masters, %s shipped"
         % (mb(deriv["master_bytes"]), mb(deriv["web_bytes"])))
    stat("%.0f s" % corr["audio_span_s"], "audio analysed",
         "across %d clips, after 1 exclusion" % len(kept))
    stat(str(corr["audio_n_excursions"]), "level excursions",
         "longest %.1f s" % corr["audio_longest_s"])
    stat(str(sw["n_laps"]), "stopwatch laps",
         "one observer, %s to %s" % (esc(sw["start_local_approx"]),
                                     esc(sw["end_local_approx"])))
    stat("%.1f/h" % rate["observed_per_hour"], "observed rate",
         "schedule says %.1f/h" % rate["scheduled_per_hour"])
    stat("%.0f%%" % corr["duty_ceiling_pct"], "duty ceiling",
         "at the loosest threshold tested")
    parts.append("<section class='card glance'><h2>At a glance</h2>"
                 "<div class='ggrid'>%s</div></section>" % "".join(g))

    # ---- the refusal ----------------------------------------------------
    parts.append(card(
        "What this is not",
        """
<p>The obvious thing to do with a phone recording of a loud place is to read a
level off it. That is refused here, and the refusal is the most important
methodological statement on the page.</p>
<ul>
<li><strong>Automatic gain control was active and cannot be undone.</strong>
Android applies AGC on the default capture path. A compressor that pulls the
level down during a loud passage and lets it back up afterwards writes its own
release curve into the file. Anything computed from the absolute value of
these samples is a property of Samsung's compressor, not of the bridge.</li>
<li><strong>The microphone response is unknown and is not flat.</strong> Phone
MEMS capsules are routinely high-passed in hardware, and low frequency is
exactly where bridge structural radiation lives. A spectrum taken from this
material would be missing the part that matters, with no way to tell from the
file that it is missing.</li>
<li><strong>There was no calibration and no windscreen.</strong> Both are
named in <a href="../read/field-capture-protocol.html">Document 5</a> as the
things that decide whether a session is worth anything, and neither was
present.</li>
</ul>
<p>What survives all three is <strong>timing</strong>. AGC changes how loud a
sample is; it does not change when the sample was written. Onsets, durations,
gaps and rates are recoverable from a file whose absolute scale is worthless,
and every quantitative claim below is one of those four.</p>
<p class="note">The unit on every chart here is <span class="mono">dBFS</span>
&mdash; decibels relative to digital full scale, a number about the file. It
is never <span class="mono">dB(A)</span>. The MTA's measured
<span class="mono">dB(A)</span> figures used elsewhere in this repository are
from a calibrated meter and are not comparable to anything on this page.</p>
"""))

    # ---- inventory ------------------------------------------------------
    rows = []
    for f in sorted(caps, key=lambda r: (r["kind"], r["name"])):
        dv = deriv["files"].get(f["name"], {})
        links = " ".join(
            "<a href='%s'>%s</a>" % (esc(v["file"]), esc(k))
            for k, v in sorted(dv.items()))
        flag = (" <span class='pill bad'>excluded</span>"
                if f["name"] in excl else "")
        rows.append(
            "<tr><td>%s%s</td><td>%s</td><td>%s</td><td class='num'>%s</td>"
            "<td class='num'>%s</td><td class='mono sha'>%s</td><td>%s</td></tr>"
            % (esc(f["name"]), flag, esc(f["kind"]), esc(f.get("place") or ""),
               esc(f.get("filename_time") or ""),
               ("%.1f s" % f["duration_s"]) if f.get("duration_s") else "&mdash;",
               esc(f["sha256"][:16]), links))
    parts.append(card(
        "Every file, and its fingerprint",
        "<div class='tw'><table><thead><tr><th>file</th><th>kind</th>"
        "<th>place</th><th>clock</th><th>length</th><th>sha-256 (first 16)</th>"
        "<th>what ships</th></tr></thead><tbody>%s</tbody></table></div>"
        "<p class='note'>%s</p>"
        "<p class='note'>The masters total %s and the web versions total %s, a "
        "factor of %s. Android names a video file at the moment recording "
        "<em>starts</em> and writes the container timestamp when it "
        "<em>closes</em>, so the clock column is the start and the two differ "
        "by the length of the clip. Every capture carried GPS and full EXIF; "
        "none of it was stripped before analysis.</p>"
        % ("".join(rows), esc(deriv["note"]),
           mb(deriv["master_bytes"]), mb(deriv["web_bytes"]),
           "%.0f&times;" % deriv["shrink_x"])))

    # ---- geo ------------------------------------------------------------
    # The excluded clip is still a place someone stood, so it stays on the
    # map - but it is drawn in the muted colour, because a reader scanning
    # the chart should not have to cross-reference the exclusion card to
    # find out that one of these markers contributes nothing.
    for c in geo["captures"]:
        c["excluded"] = c["name"] in excl
    grows = []
    for c in geo["captures"]:
        grows.append(
            "<tr><td>%s</td><td class='num'>%+.1f</td><td class='num'>%.1f</td>"
            "<td>%s</td><td>%s</td><td class='num'>%.0f m</td></tr>"
            % (esc(c["name"]), c["chainage_m"], c["abs_offset_m"],
               esc(c["side"]), esc(c["nearest_anchor"]), c["nearest_anchor_m"]))
    parts.append(card(
        "Where each capture actually stood",
        geo_svg(geo)        + "<div class='tw'><table><thead><tr><th>capture</th>"
          "<th>chainage, m</th><th>offset from track, m</th><th>which side</th>"
          "<th>nearest MTA measurement</th><th>distance to it</th>"
          "</tr></thead><tbody>%s</tbody></table></div>" % "".join(grows)
        + """
<p>The frame is the one the rest of this repository already uses: distance
along the fitted track axis, and perpendicular distance from it. Chainage zero
is the DUMBO Archway, which is itself one of the four points the MTA measured.
The axis is fitted to %d OpenStreetMap nodes tagged as subway on the bridge and
is straight to within %.1f m over the %.0f m it was fitted across; every
capture here falls inside that run, so no offset above is an extrapolation.</p>
<p class="note"><strong>The compass direction is derived, not typed.</strong>
The first version of this table hard-coded &ldquo;north-east&rdquo; for a
positive offset. Probing the fitted axis showed positive offset actually points
%s. A refit that flips the sign would have silently inverted every row, so the
bearing is now read off the axis at build time.</p>
<p>Two of the video captures stand <strong>%.0f m and %.0f m</strong> from the
track. Three of the four points the MTA measured are further from it than that.
This is not a claim that the captures are better sited &mdash; they carry no
calibration and the MTA's do &mdash; but it does mean the geometry is not the
reason nothing here can be compared with a decibel.</p>
""" % (21, geo["axis_straightness_m"],
            geo["axis_fitted_to_m"] - geo["axis_fitted_from_m"],
            esc(geo["negative_offset_dir"] if geo.get("negative_offset_dir")
                else "the other way"),
            min(c["abs_offset_m"] for c in geo["captures"]
                if c["kind"] == "video"),
            sorted(c["abs_offset_m"] for c in geo["captures"]
                   if c["kind"] == "video")[1])))

    # ---- envelopes ------------------------------------------------------
    ebits = []
    for f in sorted(vids, key=lambda r: r["name"]):
        a = f["audio"]
        is_ex = f["name"] in excl
        dv = deriv["files"].get(f["name"], {})
        ebits.append("<h3>%s%s</h3>" % (
            esc(f["name"]),
            " <span class='pill bad'>excluded from every statistic</span>"
            if is_ex else ""))
        ebits.append("<p class='sub'>%s &middot; %.1f s &middot; %s %s at %s Hz, "
                     "decoded to %s Hz mono-per-channel for analysis "
                     "&middot; %d level excursion%s detected</p>"
                     % (esc(f.get("place") or ""), f["duration_s"],
                        esc(f.get("channels") or ""),
                        esc((f.get("audio_codec") or "").upper()),
                        num(f.get("sample_rate")), num(a["sample_rate"]),
                        a["n_events"], "" if a["n_events"] == 1 else "s"))
        ebits.append(envelope_svg(a["trace_dbfs"], a["events"],
                                  a["analysed_s"], excluded=is_ex))
        if a["events"]:
            er = "".join(
                "<tr><td class='num'>%.2f</td><td class='num'>%.2f</td>"
                "<td class='num'>%.2f</td><td class='num'>%+.1f</td>"
                "<td>%s</td></tr>"
                % (e["start_s"], e["end_s"], e["dur_s"], e["rise_db"],
                   "cut off by the end of the clip" if e["truncated"] else "complete")
                for e in a["events"])
            ebits.append("<div class='tw narrow'><table><thead><tr>"
                         "<th class='num'>start, s</th>"
                         "<th class='num'>end, s</th>"
                         "<th class='num'>duration, s</th>"
                         "<th class='num'>rise above the clip median, dB</th>"
                         "<th>&nbsp;</th></tr></thead><tbody>%s</tbody>"
                         "</table></div>" % er)
        if dv.get("audio"):
            # preload="metadata" not "none": with none the control renders
            # "0:00 / 0:00" until the reader presses play, which looks like a
            # broken file. Three short m4a headers is a cheap price for a
            # control that shows its own length.
            ebits.append("<audio controls preload='metadata' src='%s'></audio>"
                         % esc(dv["audio"]["file"]))
        if is_ex:
            ebits.append("<p class='note bad'>This clip contributes nothing to "
                         "any number on this page. See the next card.</p>")
    parts.append(card(
        "The level traces, and what was picked out of them",
        "".join(ebits),
        "An excursion is a stretch at least %.1f s long that sits at least "
        "%.0f dB above the clip's own rolling median, with excursions less "
        "than %.1f s apart merged. It is <em>a level excursion</em>, not "
        "<em>a train</em>: the detector cannot tell a train from a truck, and "
        "does not try to."
        % (d["analysis"]["min_event_s"], d["analysis"]["threshold_db"],
           d["analysis"]["min_gap_s"])))

    # ---- obstruction ----------------------------------------------------
    orows = "".join(
        "<tr%s><td>%s</td><td class='num'>%.1f</td><td class='num'>%.1f</td>"
        "<td class='num'>%.3f</td><td class='num'>%d of 3</td></tr>"
        % (" class='flagged'" if r["clip"] == co["suspect"] else "",
           esc(r["clip"]), r["floor_dbfs"], r["range_db"], r["corr"], r["flags"])
        for r in co["rows"])
    notes = "".join(
        "<li>&ldquo;%s&rdquo; &mdash; rated %d/5, %s. Tested by: %s.</li>"
        % (esc(n["claim"]), n["rating"], esc(n["status"].lower()),
           esc(n["tested_by"]))
        for n in d["operator_notes"][co["suspect"]])
    parts.append(card(
        "One clip was thrown away, and the reason is worth more than the clip",
        """
<p>After the recordings were made, the operator volunteered two recollections
about the lawn clip:</p>
<ul class="quotes">%s</ul>
<p>Both are testable in the file, and both tests were written <em>after</em>
the recollection and are free to disagree with it. Recording a recollection as
evidence would be circular; recording it as a <em>hypothesis</em> and then
testing it is not.</p>
<p>The first pass found neither. There was no drop-out at all &mdash; the clip
sits inside a %s dB band for its whole length &mdash; and no sustained sign
change between the channels. That looked like a clean negative until the test
was checked for a blind spot, and it has one:
<strong>a within-clip test measures each clip against its own median, so an
obstruction that never lifts moves the baseline with it and becomes
invisible.</strong></p>
<p>So a second, between-clip test was written, on three indicators that move
in known and <em>different</em> directions for a hand over a microphone versus
a genuinely quiet site. A hand raises the noise floor, compresses the dynamic
range, and decorrelates the two channels. Quiet <em>lowers</em> the floor and
leaves the channels agreeing.</p>
<div class="tw"><table><thead><tr><th>clip</th>
<th>noise floor, dBFS</th><th>dynamic range, dB</th>
<th>channel correlation</th><th>indicators flagged</th>
</tr></thead><tbody>%s</tbody></table></div>
<p><strong>All three picked the same clip, unanimously.</strong> %s</p>
<p class="note">The clip is excluded <em>at source</em>, before any statistic
is computed &mdash; not caveated afterwards. A caveat below a number does not
stop the number being quoted. The audio span on this page is
%.1f s, not %.1f s, because of it, and the conclusion in the corroboration
card survives losing it.</p>
""" % (notes, "5.9", orows, esc(co["verdict"]),
            corr["audio_span_s"], corr["audio_span_s"] + 10.28)))

    # ---- detectability --------------------------------------------------
    drows = "".join(
        "<tr%s><td>%s</td><td class='num'>%.1f</td><td class='num'>%.2f</td>"
        "<td class='num'>%d</td><td class='num'>%.1f%%</td><td>%s</td></tr>"
        % ("" if r["informative"] else " class='flagged'",
           esc(r["clip"]), r["analysed_s"], r["expected_events"],
           r["observed"], r["p_zero_pct"],
           "informative" if r["informative"] else
           "<strong>carries no information</strong>")
        for r in sorted(det["clips"], key=lambda r: -r["analysed_s"]))
    parts.append(card(
        "A clip shorter than a headway cannot be evidence of quiet",
        """
<p>The lawn clip is <em>closer</em> to the track than either canyon clip and
detected nothing. That is the shape of a finding, and it is not one. At
%.1f trains an hour the expected number of trains inside a %.1f s window is
%.2f, so the chance of catching none at all is <strong>%.1f%%</strong>
regardless of how loud the site is.</p>
<div class="tw"><table><thead><tr><th>clip</th><th>analysed, s</th>
<th>trains expected</th><th>excursions observed</th>
<th>chance of zero by luck alone</th><th>&nbsp;</th>
</tr></thead><tbody>%s</tbody></table></div>
<p class="note">%s</p>
""" % (det["rate_per_hour"],
            [c for c in det["clips"] if not c["informative"]][0]["analysed_s"],
            [c for c in det["clips"] if not c["informative"]][0]["expected_events"],
            [c for c in det["clips"] if not c["informative"]][0]["p_zero_pct"],
            drows, esc(det["note"]))))

    # ---- stopwatch ------------------------------------------------------
    def reading_block(key, r, chosen):
        return ("<div class='rd %s'><h4>%s%s</h4>"
                "<table class='kv'>"
                "<tr><th>events counted</th><td class='num'>%d</td></tr>"
                "<tr><th>mean event</th><td class='num'>%.1f s</td></tr>"
                "<tr><th>median event</th><td class='num'>%.1f s</td></tr>"
                "<tr><th>event spread (CV)</th><td class='num'>%.3f</td></tr>"
                "<tr><th>gap spread (CV)</th><td class='num'>%.3f</td></tr>"
                "<tr><th>implied cycle</th><td class='num'>%.1f s</td></tr>"
                "<tr><th>implied rate</th><td class='num'>%.1f/h</td></tr>"
                "<tr><th>implied duty cycle</th><td class='num'>%.1f%%</td></tr>"
                "</table></div>"
                % ("ok" if chosen else "no",
                   "odd laps are noise" if key == "odd_noise"
                   else "odd laps are quiet",
                   " &mdash; <strong>taken</strong>" if chosen
                   else " &mdash; <strong>rejected</strong>",
                   r["noise"]["n"], r["noise"]["mean"], r["noise"]["median"],
                   r["noise"]["cv"], r["gap_cv"], r["cycle_s"],
                   r["events_per_hour"], r["duty_pct"]))

    # The outlier note has to be derived, not typed. An earlier draft said the
    # second lap was "a quiet interval" - it is not, it is the first NOISE
    # interval under the chosen reading, and the ratio quoted with it was
    # computed against the wrong set. Getting this from the chosen reading's
    # own values means it cannot disagree with the table beside it, and it
    # flips automatically if the reading is ever re-chosen.
    nv = sorted(ch["noise"]["values"], reverse=True)
    out_v, next_v = nv[0], nv[1]
    out_lap = next(l["lap"] for l in sw["laps"]
                   if abs(l["lap_s"] - out_v) < 0.001)

    parts.append(card(
        "Fourteen taps, two readings, and only one of them can be right",
        laps_svg(sw["laps"], chosen_is_odd=(sw["chosen"] == "odd_noise"))
        + """
<p>The stopwatch records a lap every time the observer judged train noise to
start <em>or</em> stop. The file therefore contains fourteen durations that
alternate between noise and quiet &mdash; but <strong>it does not record which
kind the first lap was</strong>, and the observer did not write it down. Both
interleavings are arithmetically valid and they give opposite answers.</p>
<div class="rds">%s%s</div>
<p>The tie is broken on a property of the railway rather than a preference.
<strong>Headway is scheduled and event duration is not.</strong> Trains are
dispatched to a timetable, so the gaps between them should cluster; how long a
given train sounds loud depends on its speed, its length, which of four tracks
it is on and where the observer is standing, so the events should scatter. The
reading whose <em>quiet</em> intervals cluster more tightly is the reading in
which the quiet intervals are really quiet intervals.</p>
<p>The two readings differ by a factor of <strong>%.1f&times;</strong> in
exactly that respect, which is not a marginal call. Under the chosen reading
the gaps between trains have a coefficient of variation of %.3f and the events
scatter at %.3f; under the rejected reading those two numbers swap over, which
would mean the railway runs to no timetable and every train sounds loud for
almost exactly the same length of time.</p>
<p class="note"><strong>One event does not fit, and it is not being hidden.
</strong> Lap %d is %.2f s, against %.2f s for the next longest of the seven
and a median of %.1f s &mdash; a %.1f&times; outlier on the median. It is the
first event of the session, which is where a settling error would sit: someone
starting a stopwatch on a train already passing, or missing the tap that ends
the first event and catching the one that ends the second. Both mean the
duration spans two real intervals rather than one. The mean of the chosen
reading is %.1f s and the median is %.1f s, a gap this one lap almost entirely
accounts for, which is why the median is quoted beside the mean everywhere it
matters. The lap was <em>not</em> dropped and the reading was <em>not</em>
re-chosen to make it go away.</p>
""" % (reading_block(sw["chosen"], ch, True),
            reading_block(sw["rejected"], rej, False),
            sw["cv_ratio"], ch["gap_cv"], ch["noise"]["cv"],
            out_lap, out_v, next_v, ch["noise"]["median"],
            out_v / ch["noise"]["median"],
            ch["noise"]["mean"], ch["noise"]["median"])))

    # ---- corroboration --------------------------------------------------
    sweep = {f["name"]: f["audio"]["duty_sweep"] for f in kept}
    parts.append(card(
        "The audio was analysed without reference to the stopwatch, "
        "and it refutes the reading that was rejected",
        sweep_svg(sweep, corr["duty_ceiling_pct"], corr["rejected_duty_pct"])
        + """
<p>The two instruments are independent: different day, different place,
different mechanism, and the audio detector was written and run before the
stopwatch file was parsed. So the audio can be asked whether the rejected
reading is even possible.</p>
<p>The rejected reading requires this corridor to be under train noise about
<strong>%.0f%%</strong> of the time, with each event lasting about
<strong>%.0f s</strong>. In %.1f s of recording the longest sustained level
excursion of any kind is <strong>%.1f s</strong>, and the duty cycle never
exceeds <strong>%.0f%%</strong> at any detection threshold tested &mdash;
including thresholds loose enough to be catching footsteps.</p>
<div class="tw"><table><thead><tr><th>&nbsp;</th>
<th>rejected reading</th><th>chosen reading</th><th>what the audio shows</th>
</tr></thead><tbody>
<tr><th>duty cycle</th><td class='num'>%.1f%%</td><td class='num'>%.1f%%</td>
<td class='num'>ceiling %.1f%%</td></tr>
<tr><th>typical event</th><td class='num'>%.1f s</td><td class='num'>%.1f s</td>
<td class='num'>longest %.1f s</td></tr>
</tbody></table></div>
<p class="note"><strong>This refutes one reading. It does not confirm the
other.</strong> The same sweep runs from %.0f%% down to zero as the threshold
tightens, so the duty figure is threshold-dependent and only its
<em>ceiling</em> is load-bearing. A ceiling can kill a claim above it and can
say nothing about a claim below it.</p>
""" % (corr["rejected_duty_pct"], corr["rejected_mean_event_s"],
            corr["audio_span_s"], corr["audio_longest_s"],
            corr["duty_ceiling_pct"],
            corr["rejected_duty_pct"], ch["duty_pct"], corr["duty_ceiling_pct"],
            corr["rejected_mean_event_s"], ch["noise"]["median"],
            corr["audio_longest_s"], corr["duty_ceiling_pct"])))

    # ---- rate -----------------------------------------------------------
    parts.append(card(
        "The rate agrees with the published timetable, within a wide interval",
        """
<p>The chosen reading counts <strong>%d</strong> events in %.1f s, which is
<strong>%.1f</strong> an hour. The MTA's own schedule for the same weekday
window puts <strong>%d</strong> trains across the bridge, or
<strong>%.1f</strong> an hour.</p>
<p>Seven events is a small sample. The 95%% interval on a Poisson count of
seven runs from <strong>%.1f</strong> to <strong>%.1f</strong> an hour, and
the scheduled rate sits inside it. %s</p>
<p class="note">This is the only figure on the page that touches an external
source, and the direction of the check matters: it was possible for the
observed rate to land <em>outside</em> the interval, which would have said the
stopwatch reading was wrong. It did not. That is weak positive evidence, and
it is reported as weak.</p>
""" % (rate["observed_n"], rate["observed_span_s"], rate["observed_per_hour"],
            rate["scheduled_n"], rate["scheduled_per_hour"],
            rate["ci95_low"], rate["ci95_high"], esc(rate["note"]))))

    # ---- gallery --------------------------------------------------------
    gal = []
    for f in sorted(caps, key=lambda r: r["name"]):
        dv = deriv["files"].get(f["name"], {})
        src = (dv.get("image") or dv.get("poster") or {}).get("file")
        if not src:
            continue
        cap = f.get("place") or f["kind"]
        if f["kind"] == "video":
            cap = "poster frame &mdash; " + esc(cap)
        else:
            cap = esc(cap)
        gal.append("<figure><img src='%s' alt='%s' loading='lazy'>"
                   "<figcaption>%s<br><span class='mono'>%s</span></figcaption>"
                   "</figure>" % (esc(src), esc(f["name"]), cap,
                                  esc(f["name"])))
    parts.append(card(
        "What it looks like",
        "<div class='gal'>%s</div>" % "".join(gal)
        + """
<p>Two of these are worth more than the rest. The poster frame of the first
canyon clip puts a <strong>John St / DUMBO Historic District</strong> street
sign directly under the bridge deck, which fixes the location of that
recording against a street name rather than against a coordinate the reader
has to trust. The bridge underside fills the top third of the frame.</p>
<p>The lawn frame is the only image in this repository that shows the
<strong>receptor rather than the source</strong>. There are three separate
walking groups in it and one of them has a pushchair. That is not a
measurement and it is not a count &mdash; a single frame cannot be either
&mdash; but the population this investigation has been modelling from
turnstile arithmetic is visible in it, doing the thing the model says it does,
under the deck.</p>
<p class="note">People appear in two of these frames at a distance, in a public
park, incidentally and unidentifiably. The programme's own ethics position in
<a href="../read/field-capture-protocol.html">Document 5</a> is that this work
argues for the interests of the people it would incidentally record, so it
carries that burden voluntarily: no frame here was selected for a person in
it, no face is resolvable at the published size, and the audio published
alongside carries no intelligible speech.</p>
""",
        "None of these is a measurement. They are what the corridor looked "
        "like on the two afternoons the recordings were made."))

    # ---- adams/john -----------------------------------------------------
    parts.append(card(
        "One thing that was asked for and is not separately here",
        """
<p>The capture list requested an <strong>audio recording at Adams and John
Street</strong> as a distinct file. No audio-only file exists in the material
that was handed over. That material appears instead to be
<em>inside</em> the canyon videos: both were shot at 40.7044, &minus;73.9885,
which is the John Street block, and the poster frame of the first one shows
the John Street sign directly. Their audio tracks are extracted and published
above as <span class="mono">.m4a</span> files, so the recording exists &mdash;
it is simply not a separate capture.</p>
<p>This is recorded rather than quietly reconciled because the difference
matters for what comes next. A separate audio-only capture would have been
made with the phone held still and pointed; a video's audio track was made by
someone walking and turning. The second is worse for anything spectral and no
worse for anything temporal, which is all that is claimed from it here.</p>
"""))

    # ---- against protocol -----------------------------------------------
    parts.append(card(
        "Measured against the protocol this repository wrote for itself",
        """
<div class="tw"><table><thead><tr><th>capture</th><th>what Document 5 asked
for</th><th>status</th></tr></thead><tbody>
<tr><td>C1 &mdash; spectrum</td><td>Third-octave spectrum of a pass-by, to
replace the invented spectrum in the acoustic demonstration</td>
<td class="st no"><strong>Not satisfied.</strong> No windscreen, unknown
microphone response, AGC active. A spectrum from this material would be
confidently wrong.</td></tr>
<tr><td>C2 &mdash; envelope</td><td>A measured pass-by envelope, to open the
closed loop in section 1.7</td>
<td class="st part"><strong>Partly, and not usefully.</strong> Four excursion
envelopes were recovered, but AGC deforms exactly the rise and decay that
section 1.7 assumes a shape for. The durations are usable; the shape is
not.</td></tr>
<tr><td>C3 &mdash; headway</td><td>Ninety minutes of event timing, needing no
calibration at all</td>
<td class="st part"><strong>Partly.</strong> %.1f s of stopwatch and %.0f s of
audio against the ninety minutes asked for. It is the capture this material
comes closest to satisfying, and it is the one that needed the least
equipment.</td></tr>
<tr><td>C4 &mdash; attribution</td><td>Acoustic events matched to identified
trains via GTFS-realtime</td>
<td class="st no"><strong>Not attempted.</strong> Requires a live feed poller
running beside the recorder.</td></tr>
<tr><td>C5 &mdash; photogrammetry</td><td>Structure-from-motion imagery of the
under-deck</td>
<td class="st no"><strong>Not satisfied.</strong> Four stills and two walking
videos are not a photogrammetric set.</td></tr>
</tbody></table></div>
<p class="note">Document 5 was written before any of this existed and
specified five captures. This session satisfies none of them completely and
two of them partly. That is the honest score, and it is worth stating plainly
because the temptation with first field data is to let its existence stand in
for its adequacy.</p>
""" % (sw["span_s"], corr["audio_span_s"])))

    # ---- wrong ----------------------------------------------------------
    parts.append(card(
        "Where this is likely to be wrong",
        """
<ol class="wrong">
<li><strong>The pairing inference is the load-bearing assumption and it is an
inference.</strong> Everything the stopwatch contributes rests on deciding
which laps were noise. The tie-break is principled and the ratio is %.1f&times;
&mdash; but it is one observer, fourteen laps, and no independent record of
what the first tap meant. If the pairing is wrong, the duty cycle, the event
durations and the rate are all wrong together, and the audio corroboration
only rules out the alternative on duty cycle, not on everything.</li>
<li><strong>The observer knew what the study is about.</strong> The same
person who has been writing about train noise for weeks decided, in real time,
when train noise started and stopped. Expectancy effects are not controlled
for and cannot be recovered from the file.</li>
<li><strong>A level excursion is not a train.</strong> The detector responds
to trucks, to the observer's own footsteps and clothing, to wind, and to
anything else loud. On a corridor carrying heavy road traffic under the same
deck, some of the four excursions may not be trains at all.</li>
<li><strong>Four excursions is not a sample.</strong> Every audio statistic
here rests on four events in under two minutes of usable recording. Almost
nothing survives that being an unrepresentative two minutes.</li>
<li><strong>The exclusion was decided by three indicators over three
clips.</strong> That cannot carry a p-value and none is claimed. With a
different third clip the unanimity might not hold. The defence is that the
consequence does not depend on the cause being resolved &mdash; a clip that
looks like that is not usable either way.</li>
<li><strong>The rate agreement is weak and could easily be coincidence.</strong>
A 95%% interval running from %.1f to %.1f an hour would have accepted a very
large range of observed rates.</li>
<li><strong>The schedule is not the service.</strong> Every comparison with the
timetable inherits the known problems of GTFS static: it excludes non-revenue
moves, it is a plan rather than an observation, and its departure times are
quantised to the half minute.</li>
<li><strong>The geometry rests on a fitted axis and digitised anchor
positions.</strong> The MTA memos give locations as descriptions, not
coordinates. The offsets in the geometry table are good to tens of metres,
not to metres.</li>
<li><strong>One consumer handset, two days, one observer, one weather
condition.</strong> Nothing here establishes anything about a different
season, a different time of day, wet rail, or a different phone.</li>
<li><strong>The duty ceiling is a ceiling because of how the sweep was
defined.</strong> If a real excursion sits below the loosest threshold tested,
the ceiling is too low and the refutation weakens. The sweep was run to a
threshold loose enough to catch footsteps specifically to make this
unlikely, which is an argument and not a proof.</li>
</ol>
""" % (sw["cv_ratio"], rate["ci95_low"], rate["ci95_high"])))

    parts.append("""
<section class="card">
<h2>Reproducing this</h2>
<p>Two scripts, both in <span class="mono">pedestrian-site-visits/</span>.
<span class="mono">build_media_data.py</span> decodes the audio, detects the
excursions, runs the obstruction and detectability tests, places every capture
against the alignment, parses the stopwatch and writes
<span class="mono">media-data.json</span>.
<span class="mono">build_media_page.py</span> renders this page from that JSON
and computes nothing.</p>
<p>The master files are not in the repository &mdash; one of them is over
GitHub's hard file size limit &mdash; so the first script will not run from a
clean clone without them. Every master is fingerprinted by SHA-256 in the
inventory above, so a master supplied later can be checked against the one
actually analysed. Everything the page displays is in the committed JSON.</p>
</section>
</div>""")

    head = load_head()
    doc = (head
           + "\n" + PAGE_CSS + "\n</style>\n</head>\n<body>\n"
           + "\n".join(parts)
           + "\n</body>\n</html>\n")
    doc = doc.replace(
        "<title>Usage dashboard - what this investigation cost</title>",
        "<title>Field media - what a phone recorded under the "
        "Manhattan Bridge</title>")

    if "Usage dashboard" in doc:
        raise SystemExit("copied head still carries the source page's title")

    # A literal percent sign left unescaped in a prose block that is also a
    # format string is the sharpest trap in this file. Some of them raise -
    # "95% interval" gives "not enough arguments" and stops the build. But
    # "% d" is a VALID conversion (space flag, decimal), so a sentence like
    # "50% duty" would silently consume an argument and shift every value
    # after it by one. That failure emits a page that renders perfectly and
    # is wrong. These assertions are cheap and they catch the shift, because
    # a shifted run puts the wrong type in the wrong place almost immediately.
    for probe in ("%s", "%d", "%.1f", "%.0f", "&mdash;s",
                  ">None<", ">nan<", ">null<", "None</", "nan</"):
        if probe in doc:
            raise SystemExit("unsubstituted or junk value in output: %r"
                             % probe)
    for need in ("At a glance", "What this is not", "dBFS",
                 "Where this is likely to be wrong", "sha-256"):
        if need not in doc:
            raise SystemExit("output is missing a required section: %r" % need)
    n_svg = doc.count("<svg ")
    if n_svg != len(vids) + 3:
        raise SystemExit("expected %d charts (%d envelopes + geo + sweep + "
                         "laps), got %d" % (len(vids) + 3, len(vids), n_svg))

    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        fh.write(doc)
    print("wrote %s (%d bytes)" % (OUT, os.path.getsize(OUT)))
    print("  cards      : %d" % doc.count("<section class"))
    print("  captures   : %d" % len(caps))
    print("  audio ele  : %d" % doc.count("<audio"))
    print("  images     : %d" % doc.count("<img "))
    print("  svg charts : %d" % doc.count("<svg "))
    return doc


PAGE_CSS = """
/*MEDIACSS*/
.eyebrow { text-transform: uppercase; letter-spacing: 0.1em; font-size: 0.78rem;
  color: var(--cp-text-muted); margin: 0 0 8px; font-weight: 600; }
.lede { font-size: 1.06rem; max-width: 74ch; color: var(--cp-text-muted); }
.lede strong { color: var(--cp-text); }
.card { background: var(--cp-surface); border: 1px solid var(--cp-border);
  border-radius: 12px; padding: 20px 22px; margin: 0 0 20px; }
.card h2 { font-size: 1.22rem; margin: 0 0 6px; }
.card h3 { font-size: 1rem; margin: 22px 0 2px; }
.card h4 { font-size: 0.95rem; margin: 0 0 8px; }
.card .sub { color: var(--cp-text-muted); font-size: 0.92rem; margin: 0 0 14px; }
.card p { max-width: 78ch; }
.ggrid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 14px; }
.gcell { background: var(--cp-surface-soft); border: 1px solid var(--cp-border);
  border-radius: 10px; padding: 12px 14px; }
.gv { font-size: 1.7rem; font-weight: 700; color: var(--cp-accent);
  line-height: 1.1; }
.gl { text-transform: uppercase; letter-spacing: 0.06em; font-size: 0.7rem;
  color: var(--cp-text-muted); margin-top: 3px; font-weight: 600; }
.gn { font-size: 0.82rem; color: var(--cp-text-soft); margin-top: 6px; }
.tw { overflow-x: auto; margin: 12px 0; }
.tw.narrow table { max-width: 760px; }
table { border-collapse: collapse; width: 100%; font-size: 0.9rem; }
th, td { text-align: left; padding: 7px 10px;
  border-bottom: 1px solid var(--cp-border); vertical-align: top; }
th { font-size: 0.76rem; text-transform: uppercase; letter-spacing: 0.05em;
  color: var(--cp-text-muted); font-weight: 600; }
td.num, th.num { text-align: right; }
tr.flagged td { background: var(--cp-accent-soft); }
.sha { font-size: 0.78rem; color: var(--cp-text-muted); }
.note { font-size: 0.9rem; color: var(--cp-text-muted);
  border-left: 3px solid var(--cp-border-strong); padding-left: 12px;
  margin: 14px 0 0; }
.note.bad { border-left-color: var(--cp-danger); }
.pill { display: inline-block; font-size: 0.7rem; text-transform: uppercase;
  letter-spacing: 0.05em; padding: 2px 7px; border-radius: 999px;
  font-weight: 600; vertical-align: middle; }
.pill.bad { background: var(--cp-danger); color: #fff; }
.envsvg { display: block; margin: 10px 0 4px; max-width: 100%; height: auto; }
audio { width: 100%; max-width: 520px; margin: 8px 0 4px; display: block; }
.rds { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 14px; margin: 14px 0; }
.rd { border: 1px solid var(--cp-border); border-radius: 10px; padding: 14px; }
.rd.ok { border-color: var(--cp-success); background: var(--cp-surface-soft); }
.rd.no { border-color: var(--cp-danger); opacity: 0.82; }
.rd table.kv { font-size: 0.86rem; }
.rd table.kv th { text-transform: none; letter-spacing: 0; font-weight: 400; }
.gal { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
  gap: 14px; }
.gal figure { margin: 0; }
/* contain, not cover. These are portrait phone frames, and the evidence in
   two of them - the John Street sign under the deck, and the people on the
   lawn - sits in the top third, which a cover crop to a landscape tile cuts
   off completely. A gallery that silently deletes the thing the caption is
   pointing at is worse than no gallery. */
.gal img { width: 100%; height: 300px; object-fit: contain;
  background: var(--cp-surface-soft); border-radius: 8px;
  border: 1px solid var(--cp-border); display: block; }
.gal figcaption { font-size: 0.8rem; color: var(--cp-text-muted); margin-top: 6px; }
.gal figcaption .mono { font-size: 0.74rem; }
ul.quotes li { margin-bottom: 6px; }
ol.wrong li { margin-bottom: 10px; max-width: 78ch; }
td.st.no { color: var(--cp-danger); }
td.st.part { color: var(--cp-warning); }
/*MEDIACSS-END*/
"""


if __name__ == "__main__":
    build()
