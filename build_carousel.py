"""Build visual-review/noise-canyon.html from visual-review/carousel.json.

Slides are declared in the JSON manifest. Adding one is a single object;
removing one is deleting that object or setting "enabled": false. This file
supplies the drawing routines named by the manifest and nothing else decides
what appears on the page.

Artwork is generated as inline SVG from open data so that it inherits the
page's theme variables and so that every line on it is re-derivable. No
proprietary basemap is traced.

    python build_carousel.py            build the page
    python build_carousel.py --check    validate the manifest and exit

Geodata is fetched by data-collection/fetch_geodata.py.
"""
import json
import math
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
GEO = os.path.join(ROOT, "data-collection", "geo")
MANIFEST = os.path.join(ROOT, "visual-review", "carousel.json")
OUTPAGE = os.path.join(ROOT, "visual-review", "noise-canyon.html")

# Same local grid as visual-review/agent-model.html so positions are comparable
# between artifacts rather than each one having its own quiet convention.
LAT0, LON0 = 40.7020, -73.9900
MX = 111320 * math.cos(math.radians(LAT0))
MY = 110540

FT = 0.3048

# The DUMBO Archway, one of the four measured points, used as chainage zero.
ARCHWAY = (40.7036, -73.9887)

# MTA's own instrumented sessions. Levels 5/5, positions 2/5 and ours.
ANCHORS = [
    ("dogrun", "Brooklyn Bridge Park, Main Street section", 40.7042, -73.9930, 87.50, 98.90),
    ("archway", "DUMBO Archway", 40.7036, -73.9887, 81.33, 91.80),
    ("library", "Adams Street Library", 40.7027, -73.9878, 84.65, 98.10),
    ("frontpine", "Front and Pine Street", 40.7028, -73.9880, None, 94.40),
]

STATIONS = [
    ("york", "York St (F)", 40.701397, -73.98675),
    ("high", "High St (A,C)", 40.699337, -73.99053),
]

# Waypoints the walk must pass through, in order. Chosen to describe the
# ordinary approach: out of the station, north-west to the river, then
# south-west along the water past the bridge.
WALK = [
    ("York Street F station", 40.70135, -73.98665),
    ("Water Street at the Archway", 40.70355, -73.98885),
    ("Main Street at the water", 40.70395, -73.99385),
    ("Empire Fulton Ferry lawn", 40.70325, -73.99560),
    ("Pier 1 promenade", 40.70055, -73.99730),
]

WALKABLE = {
    "footway", "pedestrian", "path", "steps", "living_street", "residential",
    "service", "unclassified", "tertiary", "secondary", "cycleway",
    "tertiary_link", "secondary_link", "track",
}


def g(lat, lon):
    return ((lon - LON0) * MX, (lat - LAT0) * MY)


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def f(v, n=1):
    return ("%." + str(n) + "f") % v


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

_cache = {}


def geodata():
    if "b" not in _cache:
        for name in ("buildings.json", "osm.json"):
            p = os.path.join(GEO, name)
            if not os.path.exists(p):
                raise SystemExit(
                    "missing %s\nrun: python data-collection/fetch_geodata.py" % p)
        with open(os.path.join(GEO, "buildings.json"), encoding="utf-8") as fh:
            _cache["b"] = json.load(fh)
        with open(os.path.join(GEO, "osm.json"), encoding="utf-8") as fh:
            _cache["o"] = json.load(fh)
    return _cache["b"], _cache["o"]


def building_rings(near_only=True):
    """Flatten every footprint to a list of (ring_in_metres, height_m, bin).

    near_only defaults True and every caller in this file wants it. The
    footprint set covers two extents: the walkable study area, and a context
    band across the East River that exists purely so the far shore can be
    drawn behind the near field on the walkable map. None of the drawings
    here are about the far shore, and the canyon massing in particular is a
    claim about buildings a pedestrian stands between. Letting Manhattan
    into that set would not raise an error - it would quietly restate a
    finding about 76 surveyed Brooklyn buildings over a different population.
    """
    b, _ = geodata()
    out = []
    for rec in b["buildings"]:
        if near_only and not rec.get("near", 1):
            continue
        gm = rec["geom"]
        polys = []
        if gm["type"] == "Polygon":
            polys = [gm["coordinates"]]
        elif gm["type"] == "MultiPolygon":
            polys = gm["coordinates"]
        for poly in polys:
            if not poly:
                continue
            ring = [g(pt[1], pt[0]) for pt in poly[0]]
            if len(ring) < 4:
                continue
            out.append((ring, rec["h"] * FT, rec["bin"], rec["ge"] * FT))
    return out


def bridge_axis():
    """Track centreline of the Manhattan Bridge, from OSM, as a unit vector.

    Taken from the subway ways OSM tags as carried on the bridge rather than
    from the roadway, because it is the track that is being modelled. The
    result is checked against the alignment digitised by eye in
    agent-model.html and the difference is reported by the build.
    """
    _, o = geodata()
    pts = []
    for w in o["ways"]:
        t = w["tags"]
        if t.get("railway") == "subway" and t.get("bridge") == "yes":
            pts += [g(p[1], p[0]) for p in w["geom"]]
    if len(pts) < 4:
        raise SystemExit("no bridge-carried subway geometry in osm.json")

    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    sxx = sum((p[0] - cx) ** 2 for p in pts)
    syy = sum((p[1] - cy) ** 2 for p in pts)
    sxy = sum((p[0] - cx) * (p[1] - cy) for p in pts)
    theta = 0.5 * math.atan2(2 * sxy, sxx - syy)
    ux, uy = math.cos(theta), math.sin(theta)
    if uy < 0:
        ux, uy = -ux, -uy

    # The Manhattan Bridge runs river-crossing north-north-west on this grid.
    # Anything far from that is not this bridge, and the way it gets in is
    # documented in fetch_geodata._outside: Overpass returns a way whole when
    # it merely clips the bounding box, so a neighbouring crossing tagged
    # identically can join the fit and drag the axis with it. The fit is the
    # datum every chainage in this file is measured against, so it is asserted
    # rather than trusted.
    brg = math.degrees(math.atan2(ux, uy)) % 360
    if not (325.0 <= brg <= 350.0):
        raise SystemExit(
            "bridge axis fitted to %.2f deg, outside the 325-350 deg the\n"
            "Manhattan Bridge occupies. Something other than this bridge is\n"
            "in the fit - check for ways whose geometry leaves the requested\n"
            "extent (see data-collection/fetch_geodata.py _outside)." % brg)

    # The fitted points are the river span, so their centroid is out in the
    # water. Slide the origin along the axis to the DUMBO Archway instead, so
    # that chainage zero is a place on land that the measurements refer to.
    a = g(*ARCHWAY)
    d = (a[0] - cx) * ux + (a[1] - cy) * uy
    c = (cx + ux * d, cy + uy * d)
    return c, (ux, uy), pts


def chain(p, c, u):
    """Along-track and across-track coordinates of p, in metres."""
    wx, wy = p[0] - c[0], p[1] - c[1]
    s = wx * u[0] + wy * u[1]
    t = -wx * u[1] + wy * u[0]
    return s, t


# ---------------------------------------------------------------------------
# Pedestrian routing over the OSM network
# ---------------------------------------------------------------------------

def build_graph():
    _, o = geodata()
    nodes = {}
    adj = {}

    def key(lon, lat):
        return (round(lon, 6), round(lat, 6))

    for w in o["ways"]:
        t = w["tags"]
        hw = t.get("highway")
        if hw not in WALKABLE:
            continue
        # Do not route over the bridge itself; this is a walk underneath it.
        if t.get("bridge") == "yes" and "Manhattan Bridge" in (t.get("name") or ""):
            continue
        seq = [key(p[0], p[1]) for p in w["geom"]]
        for k, p in zip(seq, w["geom"]):
            nodes.setdefault(k, g(p[1], p[0]))
        for a, b in zip(seq, seq[1:]):
            if a == b:
                continue
            pa, pb = nodes[a], nodes[b]
            d = math.hypot(pb[0] - pa[0], pb[1] - pa[1])
            adj.setdefault(a, []).append((b, d))
            adj.setdefault(b, []).append((a, d))
    return nodes, adj


def nearest(nodes, lat, lon):
    p = g(lat, lon)
    best, bk = 1e18, None
    for k, q in nodes.items():
        d = (q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2
        if d < best:
            best, bk = d, k
    return bk, math.sqrt(best)


def dijkstra(nodes, adj, src, dst):
    import heapq
    dist = {src: 0.0}
    prev = {}
    pq = [(0.0, src)]
    seen = set()
    while pq:
        d, u = heapq.heappop(pq)
        if u in seen:
            continue
        seen.add(u)
        if u == dst:
            break
        for v, w in adj.get(u, ()):
            nd = d + w
            if nd < dist.get(v, 1e18):
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    if dst not in dist:
        return None, None
    path, cur = [dst], dst
    while cur != src:
        cur = prev[cur]
        path.append(cur)
    path.reverse()
    return [nodes[k] for k in path], dist[dst]


def route():
    if "route" in _cache:
        return _cache["route"]
    nodes, adj = build_graph()
    legs, total, marks = [], 0.0, []
    snapped = []
    for name, lat, lon in WALK:
        k, off = nearest(nodes, lat, lon)
        snapped.append((name, k, off))
    for (n0, k0, o0), (n1, k1, o1) in zip(snapped, snapped[1:]):
        pts, d = dijkstra(nodes, adj, k0, k1)
        if pts is None:
            raise SystemExit("no walkable route from %s to %s" % (n0, n1))
        marks.append((n0, total))
        legs.append(pts)
        total += d
    marks.append((snapped[-1][0], total))
    poly = []
    for i, leg in enumerate(legs):
        poly += leg if i == 0 else leg[1:]
    _cache["route"] = (poly, total, marks, [s[2] for s in snapped])
    return _cache["route"]


def route_chainage(pt, poly):
    """Distance along the route of the nearest point on it to pt."""
    best, bestd = 0.0, 1e18
    run = 0.0
    for a, b in zip(poly, poly[1:]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        L2 = dx * dx + dy * dy
        if L2 <= 0:
            continue
        t = max(0.0, min(1.0, ((pt[0] - a[0]) * dx + (pt[1] - a[1]) * dy) / L2))
        qx, qy = a[0] + t * dx, a[1] + t * dy
        d = math.hypot(pt[0] - qx, pt[1] - qy)
        if d < bestd:
            bestd, best = d, run + t * math.sqrt(L2)
        run += math.sqrt(L2)
    return best, bestd


# ---------------------------------------------------------------------------
# SVG helpers
# ---------------------------------------------------------------------------

class Svg:
    def __init__(self, w, h, extra=""):
        self.w, self.h = w, h
        self.parts = []
        self.extra = extra

    def add(self, s):
        self.parts.append(s)

    def out(self, title, desc):
        return (
            '<svg class="art" viewBox="0 0 %d %d" role="img" '
            'preserveAspectRatio="xMidYMid meet" aria-label="%s"%s>'
            "<title>%s</title><desc>%s</desc>%s</svg>"
            % (self.w, self.h, esc(title), (" " + self.extra) if self.extra else "",
               esc(title), esc(desc), "".join(self.parts)))


def path_d(pts, close=False):
    if not pts:
        return ""
    d = "M" + " L".join("%s %s" % (f(p[0], 1), f(p[1], 1)) for p in pts)
    return d + ("Z" if close else "")


def label(x, y, text, cls="lbl", anchor="start", dy=0):
    return ('<text class="%s" x="%s" y="%s" text-anchor="%s"%s>%s</text>'
            % (cls, f(x), f(y + dy), anchor, "", esc(text)))


# ---------------------------------------------------------------------------
# Generator: the canyon in isometric massing
# ---------------------------------------------------------------------------

def canyon_massing():
    W = 1600
    rings = building_rings()
    c, u, bpts = bridge_axis()

    def to_st(p):
        return chain(p, c, u)

    # Window on DUMBO and Vinegar Hill immediately either side of the
    # alignment. Wide enough to show both walls of the corridor, tight enough
    # that the Downtown Brooklyn towers do not dominate a drawing about DUMBO.
    S0, S1 = -300.0, 430.0
    T0, T1 = -240.0, 175.0

    sel = []
    for ring, h, binid, ge in rings:
        st = [to_st(p) for p in ring]
        ss = [p[0] for p in st]
        ts = [p[1] for p in st]
        if max(ss) < S0 or min(ss) > S1 or max(ts) < T0 or min(ts) > T1:
            continue
        if h <= 0:
            continue
        ct = sum(ts) / len(ts)
        sel.append((st, h, binid, ct))

    # Oblique projection of (along, across, up) in metres. Increasing t moves
    # up and to the left, so t is depth and the painter's key is t descending.
    AX, AY, KZ = 0.55, 0.42, 1.00

    def proj(s, t, z):
        return (s - t * AX, -t * AY - z * KZ)

    DECK_LO, DECK_HI, HW = 20.0, 32.0, 11.0

    # Run the structure only as far as the buildings it runs between, so the
    # drawing does not trail off into empty frame.
    bs = [s for st, _, _, _ in sel for s, _ in st]
    D0 = max(S0, min(bs) - 40.0)
    D1 = min(S1, max(bs) + 40.0)

    pts = []
    for st, h, _, _ in sel:
        for s, t in st:
            pts.append(proj(s, t, 0))
            pts.append(proj(s, t, h))
    for s in (D0, D1):
        for t in (-HW, HW):
            pts.append(proj(s, t, DECK_HI))
    minx = min(p[0] for p in pts); maxx = max(p[0] for p in pts)
    miny = min(p[1] for p in pts); maxy = max(p[1] for p in pts)
    padx, padt, padb = 56, 118, 96
    # Scale from the width and let the height follow, so the drawing fills the
    # frame instead of sitting in the top half of a fixed box.
    sc = (W - 2 * padx) / (maxx - minx)
    H = int(padt + padb + (maxy - miny) * sc)
    ox = padx - minx * sc
    oy = padt - miny * sc

    def P(s, t, z):
        x, y = proj(s, t, z)
        return (ox + x * sc, oy + y * sc)

    sv = Svg(W, H)
    sv.add('<rect class="bgplate" x="0" y="0" width="%d" height="%d"/>' % (W, H))
    sv.add('<path class="ground" d="%s"/>' % path_d(
        [P(S0, T0, 0), P(S1, T0, 0), P(S1, T1, 0), P(S0, T1, 0)], True))

    hs = sorted(h for _, h, _, _ in sel)
    hmax = hs[int(len(hs) * 0.97)] if hs else 1.0

    def block(st, h, band):
        out = ['<path class="bl b%d" d="%s"/>'
               % (band, path_d([P(s, t, h) for s, t in st], True))]
        for (s0, t0), (s1, t1) in zip(st, st[1:]):
            quad = [P(s0, t0, 0), P(s1, t1, 0), P(s1, t1, h), P(s0, t0, h)]
            a = 0.0
            for i in range(4):
                x0, y0 = quad[i]
                x1, y1 = quad[(i + 1) % 4]
                a += x0 * y1 - x1 * y0
            if a <= 0:
                continue
            out.append('<path class="fc f%d" d="%s"/>' % (band, path_d(quad, True)))
        return "".join(out)

    def draw(group):
        group.sort(key=lambda r: -r[3])
        return "".join(
            block(st, h, min(4, int(4.0 * min(h, hmax) / hmax)))
            for st, h, _, _ in group)

    far = [r for r in sel if r[3] > 0]
    near = [r for r in sel if r[3] <= 0]

    sv.add('<g>%s</g>' % draw(far))

    # The structure, drawn between the two walls it sits between. It is the
    # only object in this picture whose position is not surveyed, so it is
    # drawn in the accent colour and dashed rather than solid.
    deck = []
    top = [P(D0, -HW, DECK_HI), P(D1, -HW, DECK_HI),
           P(D1, HW, DECK_HI), P(D0, HW, DECK_HI)]
    side = [P(D0, -HW, DECK_LO), P(D1, -HW, DECK_LO),
            P(D1, -HW, DECK_HI), P(D0, -HW, DECK_HI)]
    endf = [P(D1, -HW, DECK_LO), P(D1, HW, DECK_LO),
            P(D1, HW, DECK_HI), P(D1, -HW, DECK_HI)]
    for s in range(int(D0) + 30, int(D1), 76):
        for t in (-HW * 0.72, HW * 0.72):
            deck.append('<path class="pier" d="%s"/>'
                        % path_d([P(s, t, 0), P(s, t, DECK_LO)]))
    deck.append('<path class="deck" d="%s"/>' % path_d(top, True))
    deck.append('<path class="deckside" d="%s"/>' % path_d(side, True))
    deck.append('<path class="deckside" d="%s"/>' % path_d(endf, True))
    sv.add('<g>%s</g>' % "".join(deck))

    sv.add('<g>%s</g>' % draw(near))

    # Chainage zero is the DUMBO Archway, which is also where the MTA measured.
    ap = P(0.0, -HW - 6, DECK_HI)
    sv.add('<path class="lead" d="M%s %s V%s"/>' % (f(ap[0]), f(ap[1]), f(padt + 22)))
    sv.add('<circle class="anchord" cx="%s" cy="%s" r="4"/>' % (f(ap[0]), f(ap[1])))
    sv.add(label(ap[0] + 8, padt + 18, "DUMBO Archway", "lbl acc"))
    sv.add(label(ap[0] + 8, padt + 38,
                 "81.33 dB(A) Leq \u00b7 91.80 dB(A) average maximum", "lbl s"))

    bx, by = 66, H - 54
    L = 100.0 * sc
    sv.add('<path class="scale" d="M%s %s h%s"/>' % (f(bx), f(by), f(L)))
    sv.add('<path class="scale" d="M%s %s v10 M%s %s v10"/>'
           % (f(bx), f(by - 5), f(bx + L), f(by - 5)))
    sv.add(label(bx + L + 12, by + 5, "100 m along the alignment", "lbl"))

    tall = max(sel, key=lambda r: r[1])
    mean_h = sum(r[1] for r in sel) / len(sel)
    flank = [r for r in sel if HW < abs(r[3]) < 90]
    fmean = (sum(r[1] for r in flank) / len(flank)) if flank else 0.0

    sv.add(label(56, 42, "THE CANYON THE TRAINS RUN DOWN", "lbl h"))
    sv.add(label(56, 66, "DUMBO and Vinegar Hill, looking north-west along the "
                         "alignment", "lbl s"))
    sv.add(label(W - 56, 42, "%d buildings, every height surveyed"
                 % len(sel), "lbl", "end"))
    sv.add(label(W - 56, 66, "mean %s m \u00b7 tallest %s m \u00b7 mean within "
                             "90 m of the track %s m"
                 % (f(mean_h, 0), f(tall[1], 0), f(fmean, 0)), "lbl s", "end"))
    sv.add(label(W - 56, H - 54, "ELEVATED STRUCTURE \u2014 position inferred, 2/5",
                 "lbl acc", "end"))
    sv.add(label(W - 56, H - 32, "no public source gives its height over DUMBO",
                 "lbl s", "end"))

    return sv.out("Isometric massing of the DUMBO corridor",
                  "Surveyed building footprints extruded to measured roof "
                  "heights, with the inferred Manhattan Bridge alignment "
                  "running between them."), {
        "n": len(sel), "tallest": tall[1], "mean": mean_h, "flank_mean": fmean}


# ---------------------------------------------------------------------------
# Generator: section across the canyon
# ---------------------------------------------------------------------------

def canyon_section():
    W = 1600
    rings = building_rings()
    c, u, _ = bridge_axis()

    # Cut at the DUMBO Archway, which is chainage zero and one of the four
    # measured points.
    cut_s, _ = chain(g(*ARCHWAY), c, u)
    T0, T1 = -170.0, 150.0

    # A true section: intersect each footprint with the plane s = cut_s and
    # keep the intervals that lie inside it. Taking the whole footprint's
    # extent instead, as a first version of this did, turns every building
    # that runs parallel to the cut into a wall and hides the street.
    blocks = []
    ncut = 0
    for ring, h, binid, ge in rings:
        st = [chain(p, c, u) for p in ring]
        ss = [p[0] for p in st]
        if h <= 0 or min(ss) > cut_s or max(ss) < cut_s:
            continue
        xs = []
        for (s0, t0), (s1, t1) in zip(st, st[1:]):
            if (s0 - cut_s) * (s1 - cut_s) < 0:
                fr = (cut_s - s0) / (s1 - s0)
                xs.append(t0 + fr * (t1 - t0))
        if len(xs) < 2:
            continue
        ncut += 1
        xs.sort()
        for i in range(0, len(xs) - 1, 2):
            a, b = xs[i], xs[i + 1]
            if b - a < 0.4:
                continue
            blocks.append((a, b, h))
    blocks.sort(key=lambda r: r[0])

    pad_l, pad_r, pad_t, pad_b = 96, 96, 104, 150
    hmax = max([b[2] for b in blocks] + [40.0])
    ztop = math.ceil(max(hmax * 1.12, 46.0) / 10.0) * 10
    sx = (W - pad_l - pad_r) / (T1 - T0)
    sy = min(sx * 1.0, 6.2)
    H = int(pad_t + pad_b + ztop * sy)

    def X(t):
        return pad_l + (t - T0) * sx

    def Y(z):
        return H - pad_b - z * sy

    sv = Svg(W, H)
    sv.add('<rect class="bgplate" x="0" y="0" width="%d" height="%d"/>' % (W, H))

    for z in range(0, int(ztop) + 1, 20):
        sv.add('<path class="grid" d="M%s %s H%s"/>' % (f(X(T0)), f(Y(z)), f(X(T1))))
        sv.add(label(pad_l - 12, Y(z) + 5, "%d m" % z, "lbl s", "end"))

    for a, b, h in blocks:
        sv.add('<rect class="sect" x="%s" y="%s" width="%s" height="%s"/>'
               % (f(X(a)), f(Y(h)), f(max(1.2, (b - a) * sx)), f(h * sy)))

    sv.add('<path class="grade" d="M%s %s H%s"/>' % (f(X(T0)), f(Y(0)), f(X(T1))))

    # The deck: assumed, and drawn as a band because a line would be a claim.
    DECK_LO, DECK_HI, HW = 20.0, 32.0, 11.0
    sv.add('<rect class="assumed" x="%s" y="%s" width="%s" height="%s"/>'
           % (f(X(-HW)), f(Y(DECK_HI)), f(2 * HW * sx), f((DECK_HI - DECK_LO) * sy)))

    left = [b for b in blocks if b[1] <= -HW]
    right = [b for b in blocks if b[0] >= HW]
    width = hw_ratio = mh = 0.0
    if left and right:
        lf = max(left, key=lambda r: r[1])
        rf = min(right, key=lambda r: r[0])
        width = rf[0] - lf[1]
        mh = (lf[2] + rf[2]) / 2.0
        hw_ratio = mh / width if width else 0.0

        # First-order reflection paths off the two nearest facades. Geometry
        # only: no absorption coefficient for either surface is published.
        for fa in (lf[1], rf[0]):
            sv.add('<path class="ray" d="%s"/>' % path_d(
                [(X(0), Y(DECK_LO)), (X(fa), Y(mh * 0.55)), (X(0), Y(1.6))]))

        yd = Y(0) + 44
        sv.add('<path class="dim" d="M%s %s H%s"/>' % (f(X(lf[1])), f(yd), f(X(rf[0]))))
        sv.add('<path class="dim" d="M%s %s v-9 M%s %s v-9"/>'
               % (f(X(lf[1])), f(yd), f(X(rf[0])), f(yd)))
        sv.add(label((X(lf[1]) + X(rf[0])) / 2, yd + 22,
                     "%s m between the nearest facades" % f(width, 0),
                     "lbl", "middle"))
        sv.add(label(X(lf[1]) - 10, Y(lf[2]) - 8, "%s m" % f(lf[2], 0), "lbl w", "end"))
        sv.add(label(X(rf[0]) + 10, Y(rf[2]) - 8, "%s m" % f(rf[2], 0), "lbl w"))

    sv.add(label(X(0), Y(DECK_HI) - 30,
                 "ELEVATED STRUCTURE", "lbl acc", "middle"))
    sv.add(label(X(0), Y(DECK_HI) - 12,
                 "ASSUMED 20\u201332 m \u00b7 1/5", "lbl s", "middle"))

    sv.add(label(pad_l, 44, "A SECTION CUT ACROSS THE CORRIDOR", "lbl h"))
    sv.add(label(pad_l, 70, "at the DUMBO Archway, looking north-west along "
                            "the track", "lbl s"))
    sv.add(label(W - pad_r, 44, "%d buildings cut by this plane" % ncut,
                 "lbl", "end"))
    sv.add(label(W - pad_r, 70, "mean flanking height / street width = %s"
                 % f(hw_ratio, 2), "lbl s", "end"))
    sv.add(label(pad_l, H - 40,
                 "The MTA measured 81.33 dB(A) Leq and 91.80 dB(A) average "
                 "maximum at this cut. Every height here is surveyed except "
                 "the hatched one.", "lbl"))

    return sv.out("Section across the DUMBO corridor at the Archway",
                  "Surveyed building heights either side of a hatched band "
                  "marking the assumed position of the elevated structure."), {
        "width": width, "hw": hw_ratio, "ncut": ncut, "blocks": len(blocks)}


# ---------------------------------------------------------------------------
# Generator: the walk
# ---------------------------------------------------------------------------

def _plan_frame(W, H, gutter, pad=48):
    """Fit the plan into the drawing area left of the label gutter."""
    poly, total, marks, offs = route()
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    for _, _, la, lo, _, _ in ANCHORS:
        p = g(la, lo)
        xs.append(p[0]); ys.append(p[1])
    for _, _, la, lo in STATIONS:
        p = g(la, lo)
        xs.append(p[0]); ys.append(p[1])
    x0, x1 = min(xs) - 130, max(xs) + 130
    y0, y1 = min(ys) - 160, max(ys) + 130
    mw = W - gutter
    sc = min((mw - 2 * pad) / (x1 - x0), (H - 2 * pad) / (y1 - y0))
    ox = pad + (mw - 2 * pad - (x1 - x0) * sc) / 2
    oy = pad + (H - 2 * pad - (y1 - y0) * sc) / 2

    def P(p):
        return (ox + (p[0] - x0) * sc, H - (oy + (p[1] - y0) * sc))
    return P, sc, (x0, y0, x1, y1)


def walk_map():
    W, H, GUT = 1600, 980, 372
    _, o = geodata()
    poly, total, marks, offs = route()
    P, sc, box = _plan_frame(W, H, GUT)
    x0, y0, x1, y1 = box

    def inbox(pts):
        return any(x0 - 150 < p[0] < x1 + 150 and y0 - 150 < p[1] < y1 + 150
                   for p in pts)

    sv = Svg(W, H)
    sv.add('<rect class="bgplate" x="0" y="0" width="%d" height="%d"/>' % (W, H))
    sv.add('<clipPath id="mapclip"><rect x="0" y="0" width="%d" height="%d"/>'
           "</clipPath>" % (W - GUT, H))
    sv.add('<g clip-path="url(#mapclip)">')

    water, parks, streets, foots = [], [], [], []
    for w in o["ways"]:
        t = w["tags"]
        pts = [g(p[1], p[0]) for p in w["geom"]]
        if not inbox(pts):
            continue
        d = path_d([P(p) for p in pts], close=True)
        if t.get("natural") == "water":
            water.append('<path class="water" d="%s"/>' % d)
        elif t.get("leisure") == "park":
            parks.append('<path class="park" d="%s"/>' % d)
        elif t.get("natural") == "coastline" or t.get("man_made") == "pier":
            water.append('<path class="shore" d="%s"/>'
                         % path_d([P(p) for p in pts]))
        elif t.get("highway") in ("motorway", "trunk", "primary", "secondary",
                                  "tertiary", "residential", "unclassified",
                                  "motorway_link", "trunk_link", "primary_link",
                                  "secondary_link"):
            streets.append('<path class="st" d="%s"/>' % path_d([P(p) for p in pts]))
        elif t.get("highway") in ("footway", "pedestrian", "path", "steps"):
            foots.append('<path class="fw" d="%s"/>' % path_d([P(p) for p in pts]))

    sv.add('<g class="lwater">%s</g>' % "".join(water))
    sv.add('<g class="lpark">%s</g>' % "".join(parks))
    sv.add('<g class="lfoot">%s</g>' % "".join(foots))
    sv.add('<g class="lst">%s</g>' % "".join(streets))

    # The bridge, drawn as a corridor with a width because that is what it is
    # on the ground.
    c, u, bpts = bridge_axis()
    HW = 12.0
    axis = [(c[0] + u[0] * s, c[1] + u[1] * s) for s in (-620, 900)]
    nx, ny = -u[1], u[0]
    corr = [(axis[0][0] + nx * HW, axis[0][1] + ny * HW),
            (axis[1][0] + nx * HW, axis[1][1] + ny * HW),
            (axis[1][0] - nx * HW, axis[1][1] - ny * HW),
            (axis[0][0] - nx * HW, axis[0][1] - ny * HW)]
    sv.add('<path class="bridge" d="%s"/>' % path_d([P(p) for p in corr], True))
    sv.add('<path class="bridgec" d="%s"/>' % path_d([P(p) for p in axis]))
    mid = P((c[0] + u[0] * 210, c[1] + u[1] * 210))
    # Screen y is flipped, and text must not end up mirrored, so fold the
    # bearing into the readable half-plane.
    ang = math.degrees(math.atan2(-u[1], u[0]))
    if ang > 90:
        ang -= 180
    elif ang < -90:
        ang += 180
    sv.add('<text class="lbl acc bt" x="%s" y="%s" text-anchor="middle" '
           'transform="rotate(%s %s %s)">MANHATTAN BRIDGE</text>'
           % (f(mid[0]), f(mid[1]), f(ang), f(mid[0]), f(mid[1])))

    sv.add('<path class="walkhalo" d="%s"/>' % path_d([P(p) for p in poly]))
    sv.add('<path class="walk" d="%s"/>' % path_d([P(p) for p in poly]))

    run, nxt = 0.0, 100.0
    for a, b in zip(poly, poly[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        while L > 0 and run + L >= nxt:
            t = (nxt - run) / L
            px, py = P((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
            sv.add('<circle class="tick" cx="%s" cy="%s" r="4.5"/>' % (f(px), f(py)))
            nxt += 100.0
        run += L

    ends = [(marks[0][0], poly[0], marks[0][1]),
            (marks[-1][0], poly[-1], marks[-1][1])]
    endpts = []
    for nm, q, dm in ends:
        p = P(q)
        endpts.append(p)
        sv.add('<circle class="wp" cx="%s" cy="%s" r="9"/>' % (f(p[0]), f(p[1])))
        anch = "start" if p[0] < (W - GUT) * 0.55 else "end"
        dx = 17 if anch == "start" else -17
        ty = min(max(p[1], 44), H - 34)
        sv.add(label(p[0] + dx, ty - 12, nm, "lbl w", anch))
        sv.add(label(p[0] + dx, ty + 7, "%s m along the walk" % f(dm, 0),
                     "lbl s", anch))

    for sid, nm, la, lo in STATIONS:
        p = P(g(la, lo))
        sv.add('<rect class="stn" x="%s" y="%s" width="18" height="18" rx="4"/>'
               % (f(p[0] - 9), f(p[1] - 9)))
        # The walk starts at a station, so one of these labels would be written
        # on top of the endpoint label. Let the endpoint label carry the name.
        if min(math.hypot(p[0] - e[0], p[1] - e[1]) for e in endpts) > 60:
            sv.add(label(p[0] + 15, p[1] + 6, nm, "lbl"))

    for aid, nm, la, lo, leq, lmax in ANCHORS:
        p = P(g(la, lo))
        sv.add('<circle class="anchor" cx="%s" cy="%s" r="15"/>' % (f(p[0]), f(p[1])))
        sv.add('<circle class="anchord" cx="%s" cy="%s" r="5"/>' % (f(p[0]), f(p[1])))
    sv.add("</g>")

    # Label gutter, outside the map so nothing is written over the drawing.
    gx = W - GUT + 26
    sv.add('<path class="gut" d="M%s 0 V%d"/>' % (f(W - GUT + 1), H))
    sv.add(label(gx, 60, "MEASURED HERE", "lbl h"))
    sv.add(label(gx, 84, "every session the MTA has published", "lbl s"))
    lab = sorted(((P(g(la, lo)), nm, leq, lmax)
                  for _, nm, la, lo, leq, lmax in ANCHORS),
                 key=lambda r: r[0][1])
    ly = 132.0
    for p, nm, leq, lmax in lab:
        ty = max(ly, min(p[1], H - 150))
        ly = ty + 74
        sv.add('<path class="lead" d="M%s %s L%s %s"/>'
               % (f(p[0]), f(p[1]), f(gx - 12), f(ty)))
        sv.add('<circle class="anchord" cx="%s" cy="%s" r="4"/>' % (f(gx - 6), f(ty)))
        sv.add(label(gx + 6, ty + 5, nm, "lbl w"))
        sv.add(label(gx + 6, ty + 26,
                     ("%s dB(A) Leq \u00b7 %s max" % (f(leq, 2), f(lmax, 2)))
                     if leq is not None else
                     ("no Leq published \u00b7 %s max" % f(lmax, 2)), "lbl s"))
    sv.add(label(gx + 4, H - 96, "STATION", "lbl s"))
    sv.add(label(gx + 4, H - 72, "WALKING ROUTE, dots every 100 m", "lbl s"))
    sv.add(label(gx + 4, H - 48, "BRIDGE CORRIDOR, alignment inferred", "lbl s"))
    sv.add(label(gx, H - 22, "\u00a9 OpenStreetMap contributors, ODbL", "lbl s"))
    sv.add('<rect class="stn" x="%s" y="%s" width="12" height="12" rx="3"/>'
           % (f(gx - 18), f(H - 107)))
    sv.add('<path class="walk" d="M%s %s h14"/>' % (f(gx - 20), f(H - 77)))
    sv.add('<path class="bridgec" d="M%s %s h14"/>' % (f(gx - 20), f(H - 53)))

    sv.add(label(48, 44, "A TYPICAL WALK INTO DUMBO", "lbl h"))
    sv.add(label(48, 68, "York Street F station to Pier 1, %s m, routed over "
                         "the OpenStreetMap footway network" % f(total, 0),
                 "lbl s"))
    return sv.out("Plan of the walk from York Street to Pier 1",
                  "A routed pedestrian path through DUMBO with the four MTA "
                  "measurement locations marked."), {
        "total": total, "snap": max(offs)}


# ---------------------------------------------------------------------------
# Generator: what is known along the walk
# ---------------------------------------------------------------------------

def walk_known():
    W, H = 1600, 760
    poly, total, marks, offs = route()

    pad_l, pad_r = 96, 96
    sx = (W - pad_l - pad_r) / total

    def X(d):
        return pad_l + d * sx

    sv = Svg(W, H)
    sv.add('<rect class="bgplate" x="0" y="0" width="%d" height="%d"/>' % (W, H))

    top, bot = 190, 470
    sv.add('<rect class="unknown" x="%s" y="%s" width="%s" height="%s"/>'
           % (f(X(0)), top, f(total * sx), bot - top))

    # dB scale for the measured bands
    LO, HI = 60.0, 100.0

    def Y(db):
        return bot - (db - LO) / (HI - LO) * (bot - top)

    for db in range(60, 101, 10):
        sv.add('<path class="grid" d="M%s %s H%s"/>' % (f(X(0)), f(Y(db)), f(X(total))))
        sv.add(label(pad_l - 12, Y(db) + 4, "%d dB(A)" % db, "lbl s", "end"))

    # CEQR marks already used elsewhere in this repository.
    for db, nm in ((65, "CEQR 65"), (80, "CEQR 80")):
        sv.add('<path class="ceqr" d="M%s %s H%s"/>' % (f(X(0)), f(Y(db)), f(X(total))))
        sv.add(label(X(total) + 8, Y(db) + 4, nm, "lbl s"))

    POSJ = 55.0  # position uncertainty, metres, from the 2/5 rating
    hits = []
    lastcx = -1e9
    for aid, nm, la, lo, leq, lmax in ANCHORS:
        d, off = route_chainage(g(la, lo), poly)
        hits.append((d, off, nm, leq, lmax))
    hits.sort()

    for i, (d, off, nm, leq, lmax) in enumerate(hits):
        a, b = X(max(0, d - POSJ)), X(min(total, d + POSJ))
        cx = (a + b) / 2
        # Two of the four sessions are 23 m apart, so their bands and their
        # labels overlap. Alternate rows rather than let the text collide.
        near = i > 0 and cx - lastcx < 210
        row = 0 if not near else 1
        lastcx = cx
        sv.add('<rect class="known" x="%s" y="%s" width="%s" height="%s"/>'
               % (f(a), f(Y(lmax)), f(max(6, b - a)), f(bot - Y(lmax))))
        sv.add('<path class="lmax" d="M%s %s H%s"/>' % (f(a), f(Y(lmax)), f(b)))
        if leq is not None:
            sv.add('<path class="leq" d="M%s %s H%s"/>' % (f(a), f(Y(leq)), f(b)))
        if near:
            sv.add(label(b + 9, Y(lmax) + 5, f(lmax, 1), "lbl w", "start"))
        else:
            sv.add(label(cx, Y(lmax) - 14, f(lmax, 1), "lbl w", "middle"))
        ly = bot + 26 + row * 62
        sv.add('<path class="lead" d="M%s %s V%s"/>' % (f(cx), f(bot + 4), f(ly - 13)))
        sv.add(label(cx, ly, nm, "lbl s", "middle"))
        sv.add(label(cx, ly + 18, "%s m from the station" % f(d, 0),
                     "lbl s", "middle"))
        if off > 30:
            sv.add(label(cx, ly + 36, "%s m off the route" % f(off, 0),
                         "lbl s", "middle"))

    covered = 0.0
    spans = []
    for d, _, _, _, _ in hits:
        spans.append((max(0, d - POSJ), min(total, d + POSJ)))
    spans.sort()
    merged = []
    for s, e in spans:
        if merged and s <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], e))
        else:
            merged.append((s, e))
    covered = sum(e - s for s, e in merged)

    sv.add('<path class="axis" d="M%s %s H%s"/>' % (f(X(0)), f(bot), f(X(total))))
    for d in range(0, int(total) + 1, 200):
        sv.add('<path class="axis" d="M%s %s v9"/>' % (f(X(d)), f(bot)))
    sv.add(label(X(0), bot + 156, "York Street F station", "lbl"))
    sv.add(label(X(total), bot + 156, "Pier 1", "lbl", "end"))

    sv.add(label(pad_l, 52, "WHAT HAS BEEN MEASURED ALONG THIS WALK", "lbl h"))
    sv.add(label(pad_l, 78,
                 "bars are the MTA's own sessions, drawn as wide as the "
                 "uncertainty in where they were", "lbl s"))
    sv.add(label(X(total), 52,
                 "%s m of %s m" % (f(covered, 0), f(total, 0)), "lbl h", "end"))
    sv.add(label(X(total), 78, "%s per cent of the walk"
                 % f(100.0 * covered / total, 1), "lbl s", "end"))
    sv.add(label(pad_l, H - 40,
                 "The shaded field is not quiet. It is unmeasured, which is a "
                 "different thing and the whole point.", "lbl acc"))
    return sv.out("Measured coverage along the walk",
                  "A strip along the walking route showing four measured "
                  "bands against an otherwise unmeasured field."), {
        "covered": covered, "total": total,
        "pct": 100.0 * covered / total}


GENERATORS = {
    "canyon_massing": canyon_massing,
    "canyon_section": canyon_section,
    "walk_map": walk_map,
    "walk_known": walk_known,
}


# ---------------------------------------------------------------------------
# The page
# ---------------------------------------------------------------------------

THEME_JS = """<script>
  (() => {
    const param = new URLSearchParams(window.location.search).get("scoutTheme");
    const theme =
      param || (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    document.documentElement.setAttribute("data-theme", theme);
  })();
</script>"""

FAVICON = (
    '<link rel="icon" href="data:image/svg+xml,'
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'"
    "%3E%3Crect width='32' height='32' rx='7' fill='%23b11f4b'/"
    "%3E%3Cpath d='M3 22h26' stroke='%23fff' stroke-width='2.4' "
    "stroke-linecap='round'/%3E%3Cpath d='M9 8v14M23 8v14' stroke='%23fff' "
    "stroke-width='2' stroke-linecap='round'/%3E%3Cpath "
    "d='M3 14L9 8Q16 17 23 8L29 14' stroke='%23fff' stroke-width='2' "
    "fill='none' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E\">")

CSS = """
:root {
  color-scheme: light;
  --cp-bg: #f7f4ef;
  --cp-bg-elevated: #fcfbf8;
  --cp-surface: #ffffff;
  --cp-surface-soft: #f5f5f5;
  --cp-border: #dedede;
  --cp-border-strong: #919191;
  --cp-text: #242424;
  --cp-text-muted: #5c5c5c;
  --cp-text-soft: #6f6f6f;
  --cp-accent: #b11f4b;
  --cp-accent-hover: #9a1a41;
  --cp-accent-soft: rgba(177, 31, 75, 0.08);
  --cp-accent-fg: #ffffff;
  --cp-success: #16a34a;
  --cp-danger: #dc2626;
  --cp-warning: #f59e0b;
  --cp-link: #0078d4;
  --cp-shadow: 0 18px 48px rgba(0, 0, 0, 0.12);
  --cp-overlay: rgba(255, 255, 255, 0.8);
  --cp-panel: rgba(255, 255, 255, 0.86);
  --cp-panel-strong: rgba(255, 255, 255, 0.96);
  --cp-sheen: rgba(255, 255, 255, 0.55);
  --cp-highlight: rgba(177, 31, 75, 0.12);
  --plate: #f1ece4;
  --massing-0: #d9d2c6;
  --massing-1: #c9c0b1;
  --massing-2: #b6ab98;
  --massing-3: #9d9080;
  --massing-4: #7f7466;
  --water: #dbe6ec;
  --parkfill: #e2eadc;
}
html[data-theme="dark"] {
  color-scheme: dark;
  --cp-bg: #3d3b3a;
  --cp-bg-elevated: #343231;
  --cp-surface: #292929;
  --cp-surface-soft: #2e2e2e;
  --cp-border: #474747;
  --cp-border-strong: #5f5f5f;
  --cp-text: #dedede;
  --cp-text-muted: #919191;
  --cp-text-soft: #b0b0b0;
  --cp-accent: #fd8ea1;
  --cp-accent-hover: #fb7b91;
  --cp-accent-soft: rgba(253, 142, 161, 0.14);
  --cp-accent-fg: #1a1a1a;
  --cp-success: #4ade80;
  --cp-danger: #f87171;
  --cp-warning: #fbbf24;
  --cp-link: #4da6ff;
  --cp-shadow: 0 18px 48px rgba(0, 0, 0, 0.32);
  --cp-overlay: rgba(41, 41, 41, 0.88);
  --cp-panel: rgba(41, 41, 41, 0.72);
  --cp-panel-strong: rgba(41, 41, 41, 0.96);
  --cp-sheen: rgba(255, 255, 255, 0.04);
  --cp-highlight: rgba(253, 142, 161, 0.12);
  --plate: #232221;
  --massing-0: #3a3734;
  --massing-1: #464240;
  --massing-2: #55504c;
  --massing-3: #6a635d;
  --massing-4: #837a72;
  --water: #26313a;
  --parkfill: #263028;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--cp-bg);
  color: var(--cp-text);
  font-family: "Segoe UI", Aptos, Calibri, -apple-system, BlinkMacSystemFont, sans-serif;
  font-size: 16px;
  line-height: 1.62;
  -webkit-font-smoothing: antialiased;
}
a { color: var(--cp-link); text-decoration: none; }
a:hover { text-decoration: underline; }
code { font-family: Consolas, "Courier New", Courier, monospace; font-size: 0.9em; }

.bar {
  position: sticky; top: 0; z-index: 60;
  background: var(--cp-panel-strong);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--cp-border);
}
.bar .in {
  max-width: 1320px; margin: 0 auto; padding: 10px 22px;
  display: flex; align-items: center; gap: 14px; flex-wrap: wrap;
}
.bar .home { font-weight: 700; color: var(--cp-text); font-size: 0.95rem; }
.bar .home:hover { color: var(--cp-accent); text-decoration: none; }
.bar nav { display: flex; gap: 4px; flex-wrap: wrap; margin-left: auto; }
.bar nav a {
  color: var(--cp-text-muted); font-size: 0.82rem; padding: 4px 9px;
  border-radius: 999px; white-space: nowrap;
}
.bar nav a:hover { background: var(--cp-accent-soft); color: var(--cp-accent); text-decoration: none; }

.wrap { max-width: 1320px; margin: 0 auto; padding: 26px 22px 80px; }
h1 { font-size: 2.05rem; line-height: 1.16; margin: 0 0 8px; letter-spacing: -0.01em; }
.sub { color: var(--cp-text-muted); font-size: 1.04rem; margin: 0 0 22px; max-width: 70ch; }

/* ---- carousel ---- */
.car {
  background: var(--cp-surface);
  border: 1px solid var(--cp-border);
  border-radius: 16px;
  box-shadow: 0 0 2px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.14);
  overflow: hidden;
}
.track { display: flex; transition: transform 420ms cubic-bezier(.4,0,.2,1); }
@media (prefers-reduced-motion: reduce) { .track { transition: none; } }
.slide { flex: 0 0 100%; min-width: 0; }
.slide[hidden] { display: none; }

.stage {
  background: var(--plate);
  border-bottom: 1px solid var(--cp-border);
  padding: 0;
  position: relative;
}
.stage .art, .stage img { display: block; width: 100%; height: auto; }
/* A portrait photograph would otherwise push the stage past the fold and hide
   the slide's own caption, so images are fitted rather than stretched. */
.stage img {
  background: var(--plate); width: auto; max-width: 100%;
  max-height: min(70vh, 720px); margin: 0 auto;
}

.meta { padding: 24px 30px 28px; display: grid; grid-template-columns: 1.55fr 1fr; gap: 30px; }
.eyebrow {
  font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.09em;
  color: var(--cp-accent); font-weight: 700; margin: 0 0 6px;
}
.meta h2 { font-size: 1.42rem; margin: 0 0 12px; letter-spacing: -0.005em; line-height: 1.25; }
.stand { font-size: 1.03rem; margin: 0 0 14px; }
.notes { margin: 0; padding-left: 20px; color: var(--cp-text-muted); }
.notes li { margin-bottom: 7px; }
.side { font-size: 0.86rem; }
.side .h {
  font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.07em;
  color: var(--cp-text-soft); font-weight: 700; margin: 0 0 6px;
}
.srcs { list-style: none; margin: 0 0 18px; padding: 0; }
.srcs li { margin-bottom: 8px; color: var(--cp-text-muted); line-height: 1.45; }
.rate {
  display: inline-block; font-family: Consolas, "Courier New", monospace;
  font-size: 0.72rem; padding: 1px 6px; border-radius: 4px;
  border: 1px solid var(--cp-border-strong); color: var(--cp-text-soft);
  margin-right: 6px; white-space: nowrap;
}
.caveat {
  background: var(--cp-accent-soft);
  border-left: 3px solid var(--cp-accent);
  border-radius: 0 0.625rem 0.625rem 0;
  padding: 11px 14px; color: var(--cp-text); line-height: 1.5;
}
.caveat b { color: var(--cp-accent); }

.ctrls {
  display: flex; align-items: center; gap: 12px; flex-wrap: wrap;
  padding: 12px 30px 16px; border-top: 1px solid var(--cp-border);
  background: var(--cp-surface-soft);
}
.btn {
  font: inherit; font-size: 0.85rem; cursor: pointer;
  background: var(--cp-surface); color: var(--cp-text);
  border: 1px solid var(--cp-border-strong); border-radius: 0.625rem;
  padding: 6px 13px;
}
.btn:hover { border-color: var(--cp-accent); color: var(--cp-accent); }
.btn:focus-visible { outline: 2px solid var(--cp-accent); outline-offset: 2px; }
.dots { display: flex; gap: 7px; margin-left: auto; flex-wrap: wrap; }
.dot {
  width: 11px; height: 11px; border-radius: 999px; padding: 0; cursor: pointer;
  border: 1px solid var(--cp-border-strong); background: var(--cp-surface);
}
.dot[aria-current="true"] { background: var(--cp-accent); border-color: var(--cp-accent); }
.dot:focus-visible { outline: 2px solid var(--cp-accent); outline-offset: 2px; }
.count { font-size: 0.82rem; color: var(--cp-text-muted); font-variant-numeric: tabular-nums; }

.foot { margin-top: 26px; color: var(--cp-text-muted); font-size: 0.88rem; max-width: 82ch; }
.foot h3 { font-size: 0.95rem; color: var(--cp-text); margin: 20px 0 6px; }
.foot code {
  background: var(--cp-surface-soft); border: 1px solid var(--cp-border);
  border-radius: 4px; padding: 0.1em 0.36em;
}

/* ---- drawing ---- */
.art { font-family: "Segoe UI", Aptos, Calibri, sans-serif; }
.bgplate { fill: var(--plate); }
.ground { fill: var(--cp-surface-soft); opacity: 0.55; }
.bl { stroke: var(--cp-border-strong); stroke-width: 0.6; }
.fc { stroke: var(--cp-border-strong); stroke-width: 0.5; }
.b0, .f0 { fill: var(--massing-0); }
.b1, .f1 { fill: var(--massing-1); }
.b2, .f2 { fill: var(--massing-2); }
.b3, .f3 { fill: var(--massing-3); }
.b4, .f4 { fill: var(--massing-4); }
.fc { filter: brightness(0.88); }
.deck { fill: var(--cp-accent); opacity: 0.34; stroke: var(--cp-accent);
        stroke-width: 1.6; stroke-dasharray: 10 6; }
.deckside { fill: var(--cp-accent); opacity: 0.20; stroke: var(--cp-accent);
            stroke-width: 1.6; stroke-dasharray: 10 6; }
.deckedge { stroke: var(--cp-accent); stroke-width: 2.4; fill: none; }
.pier { stroke: var(--cp-accent); stroke-width: 2.2; opacity: 0.55; fill: none;
        stroke-dasharray: 6 5; }
.scale { stroke: var(--cp-text-muted); stroke-width: 1.6; fill: none; }
.grid { stroke: var(--cp-border); stroke-width: 1; fill: none; }
.grade { stroke: var(--cp-border-strong); stroke-width: 2; fill: none; }
.sect { fill: var(--massing-2); stroke: var(--cp-border-strong); stroke-width: 0.8; }
.assumed { fill: url(#hatch); stroke: var(--cp-accent); stroke-width: 2;
           stroke-dasharray: 9 6; }
.ray { stroke: var(--cp-accent); stroke-width: 1.4; fill: none; opacity: 0.75;
       stroke-dasharray: 4 4; }
.dim { stroke: var(--cp-text-muted); stroke-width: 1.2; fill: none; }
.water { fill: var(--water); stroke: none; }
.shore { stroke: var(--cp-border-strong); stroke-width: 1.2; fill: none; }
.park { fill: var(--parkfill); stroke: none; }
.st { stroke: var(--cp-border-strong); stroke-width: 1.5; fill: none; opacity: 0.8; }
.fw { stroke: var(--cp-border); stroke-width: 1; fill: none; }
.rail { stroke: var(--cp-accent); stroke-width: 2; fill: none; }
.bridge { fill: var(--cp-accent); opacity: 0.16; stroke: var(--cp-accent);
          stroke-width: 1.2; stroke-dasharray: 8 5; }
.bridgec { stroke: var(--cp-accent); stroke-width: 1.6; fill: none; opacity: 0.7; }
.walkhalo { stroke: var(--plate); stroke-width: 11; fill: none;
            stroke-linejoin: round; stroke-linecap: round; }
.walk { stroke: var(--cp-link); stroke-width: 5; fill: none;
        stroke-linejoin: round; stroke-linecap: round; }
.tick { fill: var(--cp-link); opacity: 0.85; }
.wp { fill: var(--cp-surface); stroke: var(--cp-link); stroke-width: 3.4; }
.stn { fill: var(--cp-surface); stroke: var(--cp-text); stroke-width: 2.4; }
.anchor { fill: none; stroke: var(--cp-accent); stroke-width: 3; }
.anchord { fill: var(--cp-accent); }
.lead { stroke: var(--cp-accent); stroke-width: 1; fill: none; opacity: 0.5;
        stroke-dasharray: 3 3; }
.gut { stroke: var(--cp-border); stroke-width: 1.4; fill: none; }
.unknown { fill: url(#unk); stroke: var(--cp-border-strong); stroke-width: 1;
           stroke-dasharray: 6 5; }
.known { fill: var(--cp-accent); opacity: 0.20; }
.lmax { stroke: var(--cp-accent); stroke-width: 4; fill: none; }
.leq { stroke: var(--cp-accent); stroke-width: 2; fill: none; stroke-dasharray: 6 4; }
.ceqr { stroke: var(--cp-warning); stroke-width: 1.4; fill: none; stroke-dasharray: 9 6; }
.axis { stroke: var(--cp-text-muted); stroke-width: 1.6; fill: none; }
text.lbl { fill: var(--cp-text-muted); font-size: 15px; }
text.lbl.s { fill: var(--cp-text-soft); font-size: 13px; }
text.lbl.w { fill: var(--cp-text); font-weight: 700; }
text.lbl.h { fill: var(--cp-text); font-weight: 700; font-size: 17px;
             letter-spacing: 0.06em; }
text.lbl.acc { fill: var(--cp-accent); font-weight: 700; }
text.bt { font-size: 14px; letter-spacing: 0.18em; }

@media (max-width: 1000px) {
  .meta { grid-template-columns: 1fr; gap: 20px; padding: 20px 18px 24px; }
  .ctrls { padding: 12px 18px 16px; }
  .wrap { padding: 20px 14px 60px; }
  h1 { font-size: 1.6rem; }
}
"""

DEFS = (
    '<svg width="0" height="0" style="position:absolute" aria-hidden="true">'
    '<defs>'
    '<pattern id="hatch" width="9" height="9" patternTransform="rotate(45)" '
    'patternUnits="userSpaceOnUse">'
    '<rect width="9" height="9" fill="var(--cp-accent-soft)"/>'
    '<line x1="0" y1="0" x2="0" y2="9" stroke="var(--cp-accent)" '
    'stroke-width="2.4" opacity="0.55"/></pattern>'
    '<pattern id="unk" width="14" height="14" patternTransform="rotate(45)" '
    'patternUnits="userSpaceOnUse">'
    '<rect width="14" height="14" fill="var(--cp-surface-soft)"/>'
    '<line x1="0" y1="0" x2="0" y2="14" stroke="var(--cp-border-strong)" '
    'stroke-width="1.2" opacity="0.7"/></pattern>'
    '</defs></svg>')

JS = """<script>
(() => {
  const track = document.getElementById("track");
  const slides = [...track.querySelectorAll(".slide")];
  const dots = [...document.querySelectorAll(".dot")];
  const cur = document.getElementById("cur");
  let i = 0;

  function go(n) {
    i = (n + slides.length) % slides.length;
    track.style.transform = "translateX(" + (-i * 100) + "%)";
    slides.forEach((s, k) => {
      s.setAttribute("aria-hidden", k === i ? "false" : "true");
      s.querySelectorAll("a").forEach(a => {
        if (k === i) a.removeAttribute("tabindex"); else a.setAttribute("tabindex", "-1");
      });
    });
    dots.forEach((d, k) => d.setAttribute("aria-current", k === i ? "true" : "false"));
    cur.textContent = (i + 1) + " of " + slides.length;
    if (location.hash.slice(1) !== slides[i].dataset.id) {
      history.replaceState(null, "", "#" + slides[i].dataset.id);
    }
  }

  document.getElementById("prev").addEventListener("click", () => go(i - 1));
  document.getElementById("next").addEventListener("click", () => go(i + 1));
  dots.forEach((d, k) => d.addEventListener("click", () => go(k)));

  document.addEventListener("keydown", e => {
    if (e.target.matches("input, textarea, select")) return;
    if (e.key === "ArrowLeft") { go(i - 1); e.preventDefault(); }
    if (e.key === "ArrowRight") { go(i + 1); e.preventDefault(); }
    if (e.key === "Home") { go(0); e.preventDefault(); }
    if (e.key === "End") { go(slides.length - 1); e.preventDefault(); }
  });

  let x0 = null;
  track.addEventListener("touchstart", e => { x0 = e.touches[0].clientX; }, { passive: true });
  track.addEventListener("touchend", e => {
    if (x0 === null) return;
    const dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 55) go(i + (dx < 0 ? 1 : -1));
    x0 = null;
  }, { passive: true });

  const want = slides.findIndex(s => s.dataset.id === location.hash.slice(1));
  go(want >= 0 ? want : 0);
})();
</script>"""


def validate(man):
    """Fail loudly on a manifest that would ship a slide with no provenance."""
    errs = []
    slides = man.get("slides", [])
    if not slides:
        errs.append("manifest has no slides")
    seen = set()
    for n, s in enumerate(slides):
        w = "slide %d (%s)" % (n, s.get("id", "no id"))
        for k in ("id", "eyebrow", "title", "art", "alt", "standfirst",
                  "sources", "caveat"):
            if not s.get(k):
                errs.append("%s: missing %s" % (w, k))
        sid = s.get("id")
        if sid in seen:
            errs.append("%s: duplicate id" % w)
        seen.add(sid)
        art = s.get("art") or {}
        kind = art.get("kind")
        if kind == "generated":
            if art.get("generator") not in GENERATORS:
                errs.append("%s: unknown generator %r; known: %s"
                            % (w, art.get("generator"),
                               ", ".join(sorted(GENERATORS))))
        elif kind == "image":
            src = art.get("src") or ""
            if not src:
                errs.append("%s: image art needs src" % w)
            elif not os.path.exists(os.path.join(ROOT, src.replace("/", os.sep))):
                errs.append("%s: image not found: %s" % (w, src))
        else:
            errs.append("%s: art.kind must be 'generated' or 'image'" % w)
        for src in s.get("sources") or []:
            if not isinstance(src, list) or len(src) != 3:
                errs.append("%s: each source must be [label, href, rating]" % w)
    return errs


def render_slide(s, n, total):
    art = s["art"]
    stats = {}
    if art["kind"] == "generated":
        svg, stats = GENERATORS[art["generator"]]()
    else:
        rel = os.path.relpath(os.path.join(ROOT, art["src"].replace("/", os.sep)),
                              os.path.join(ROOT, "visual-review")).replace("\\", "/")
        svg = '<img src="%s" alt="%s" loading="lazy">' % (esc(rel), esc(s["alt"]))

    o = []
    o.append('<section class="slide" data-id="%s" aria-roledescription="slide" '
             'aria-label="%d of %d: %s">' % (esc(s["id"]), n, total, esc(s["title"])))
    o.append('<div class="stage">%s</div>' % svg)
    o.append('<div class="meta"><div>')
    o.append('<p class="eyebrow">%s</p>' % esc(s["eyebrow"]))
    o.append("<h2>%s</h2>" % esc(s["title"]))
    o.append('<p class="stand">%s</p>' % esc(s["standfirst"]))
    if s.get("notes"):
        o.append('<ul class="notes">%s</ul>'
                 % "".join("<li>%s</li>" % esc(x) for x in s["notes"]))
    o.append("</div><div class=\"side\">")
    o.append('<p class="h">Drawn from</p><ul class="srcs">')
    for lbl, href, rating in s["sources"]:
        link = ('<a href="%s">%s</a>' % (esc(href), esc(lbl))
                if href.startswith("http") else
                '<a href="../%s">%s</a>' % (esc(href), esc(lbl)))
        o.append('<li><span class="rate">%s</span>%s</li>' % (esc(rating), link))
    o.append("</ul>")
    o.append('<p class="h">Where this is weak</p>')
    o.append('<div class="caveat">%s</div>' % esc(s["caveat"]))
    o.append("</div></div></section>")
    return "".join(o), stats


NAV = [
    ("../index.html", "Overview"),
    ("model-3d.html", "3D model"),
    ("acoustic-demo.html", "Audio"),
    ("frequency-dashboard.html", "Frequency"),
    ("agent-model.html", "Agents"),
    ("section-problem.html", "Section"),
]


def build(man):
    slides = [s for s in man["slides"] if s.get("enabled", True)]
    total = len(slides)
    body, allstats = [], {}
    for n, s in enumerate(slides, 1):
        html, st = render_slide(s, n, total)
        body.append(html)
        allstats[s["id"]] = st

    dots = "".join(
        '<button class="dot" type="button" aria-label="Go to slide %d: %s"></button>'
        % (n, esc(s["title"])) for n, s in enumerate(slides, 1))

    nav = "".join('<a href="%s">%s</a>' % (h, t) for h, t in NAV)

    page = []
    page.append("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">")
    page.append('<meta name="viewport" content="width=device-width, initial-scale=1">')
    page.append("<title>%s &mdash; Silencing the Span</title>" % esc(man["title"]))
    page.append('<meta name="description" content="%s">' % esc(man["subtitle"]))
    page.append(FAVICON)
    page.append(THEME_JS)
    page.append("<style>%s</style>\n</head>\n<body>" % CSS)
    page.append(DEFS)
    page.append('<div class="bar"><div class="in">'
                '<a class="home" href="../index.html">Silencing the Span</a>'
                '<nav>%s</nav></div></div>' % nav)
    page.append('<div class="wrap">')
    page.append("<h1>%s</h1>" % esc(man["title"]))
    page.append('<p class="sub">%s</p>' % esc(man["subtitle"]))
    page.append('<div class="car"><div class="track" id="track" '
                'aria-roledescription="carousel" aria-label="%s">'
                % esc(man["title"]))
    page.append("".join(body))
    page.append("</div>")
    page.append('<div class="ctrls">'
                '<button class="btn" id="prev" type="button">&larr; Previous</button>'
                '<button class="btn" id="next" type="button">Next &rarr;</button>'
                '<span class="count" id="cur">1 of %d</span>'
                '<div class="dots" role="group" aria-label="Choose a slide">%s</div>'
                "</div>" % (total, dots))
    page.append("</div>")

    page.append('<div class="foot">')
    page.append("<h3>Why there is no Google Maps screenshot here</h3>")
    page.append("<p>The obvious way to draw the walk would be to screenshot a "
                "mapping service. It is not done, for two reasons and only one "
                "of them is legal. The terms of the major services forbid the "
                "derivative work. The more important reason is that a picture "
                "traced off a proprietary basemap is not a source: nobody else "
                "can regenerate it, so nobody else can check it. Every line on "
                "these slides comes from a dataset with an identifier, and the "
                "code that turns those datasets into these drawings is in this "
                "repository.</p>")
    page.append("<h3>Adding or removing a slide</h3>")
    page.append("<p>The slides are declared in <code>visual-review/carousel.json</code>. "
                "Adding one is a single object in the <code>slides</code> array; "
                "removing one is deleting that object or setting "
                "<code>\"enabled\": false</code>; reordering is moving it. Then run "
                "<code>python build_carousel.py</code>. Artwork is either a named "
                "generator in <code>build_carousel.py</code> or an image file. The "
                "build refuses to run if a slide has no sources or no caveat, and "
                "refuses to run if a generator name is misspelled, so a broken "
                "slide cannot ship quietly.</p>")
    page.append("<h3>Attribution</h3>")
    page.append("<p>Building footprints and heights: New York City OpenData, "
                "dataset <code>5zhs-2jue</code>. Streets, footways, park and "
                "water geometry, and the bridge alignment: "
                "<a href=\"https://www.openstreetmap.org/copyright\">"
                "&copy; OpenStreetMap contributors</a>, ODbL 1.0. Measured "
                "sound levels: MTA document 138061. Fetch the geodata with "
                "<code>python data-collection/fetch_geodata.py</code>.</p>")
    page.append("</div>")
    page.append("</div>")
    page.append(JS)
    page.append("\n</body>\n</html>\n")
    return "\n".join(page), allstats


def main():
    with open(MANIFEST, encoding="utf-8") as fh:
        man = json.load(fh)

    errs = validate(man)
    if errs:
        print("MANIFEST INVALID:")
        for e in errs:
            print("  -", e)
        raise SystemExit(1)
    print("manifest ok:", len(man["slides"]), "slides declared,",
          sum(1 for s in man["slides"] if s.get("enabled", True)), "enabled")

    if "--check" in sys.argv:
        return

    c, u, pts = bridge_axis()
    ref = (g(40.7003, -73.9862), g(40.7069, -73.9903))
    rv = (ref[1][0] - ref[0][0], ref[1][1] - ref[0][1])
    rn = math.hypot(*rv)
    ang = math.degrees(math.acos(max(-1, min(1, abs(
        (rv[0] * u[0] + rv[1] * u[1]) / rn)))))
    print("bridge axis from %d OSM track points; bearing differs from the "
          "alignment digitised by eye in agent-model.html by %.1f degrees"
          % (len(pts), ang))

    html, stats = build(man)
    with open(OUTPAGE, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("wrote", OUTPAGE, os.path.getsize(OUTPAGE), "bytes")
    for k, v in stats.items():
        if v:
            print("  %-16s %s" % (k, {a: (round(b, 2) if isinstance(b, float) else b)
                                      for a, b in v.items() if a != "marks"}))


if __name__ == "__main__":
    main()
