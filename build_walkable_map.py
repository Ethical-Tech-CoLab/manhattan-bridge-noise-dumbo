"""Build visual-review/walkable-map.html from the open geodata in this repo.

A walkable model of DUMBO from the York Street F platform to Brooklyn Bridge
Park Pier 1, drawn from surveyed building footprints and the open street and
footway network, with the four measured points standing where they actually
stand rather than where they were digitised by eye.

WHY THIS EXISTS

Every spatial claim in this repository until now was made against one of two
things: a footprint set drawn in plan, or positions typed to four decimal
places off a basemap. Four decimal places of latitude is about 11 m. The
canyon is 91 m wide. An 11 m error is an eighth of the width of the thing
being described, and it was never measured because there was nothing to
measure it against. This page is that something.

WHAT IS REAL HERE AND WHAT IS NOT

  SURVEYED   building footprints and roof heights - NYC OpenData 5zhs-2jue,
             the city's own building file, height_roof and ground_elevation
  MAPPED     streets, footways, steps, park paths, piers, the shoreline -
             OpenStreetMap, crowd-mapped, good but not a survey
  MEASURED   four sound levels, at the four points the MTA instrumented
  INFERRED   the bridge deck elevation. No public source gives it over DUMBO.
             It is drawn hatched, in a different colour, and the page says so.
  INVENTED   everything the walking figures do. They are a population model,
             not an observation, and no count in this repository has ever
             established how many people are here.

Nothing is traced off a proprietary basemap. Every line is re-derivable with
data-collection/fetch_geodata.py and redrawable with this file.

    python build_walkable_map.py            build the page
    python build_walkable_map.py --stats    print the derived figures only
"""
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
GEO = os.path.join(ROOT, "data-collection", "geo")
OUTPAGE = os.path.join(ROOT, "visual-review", "walkable-map.html")

# The same local grid as agent-model.html and build_carousel.py. Sharing it is
# the whole point: a position on this map and a position in the agent model are
# the same number, so the two can disagree visibly instead of quietly.
LAT0, LON0 = 40.7020, -73.9900
MX = 111320 * math.cos(math.radians(LAT0))
MY = 110540

FT = 0.3048

# MTA's own instrumented sessions. Levels 5/5 VERIFIED and quoted in
# IDEA-CONCEPT.md; positions 2/5, digitised by us from the memo's descriptions.
# That asymmetry is the reason the offset table on this page exists.
ANCHORS = [
    ("dogrun", "Brooklyn Bridge Dog Run", 40.7042, -73.9930, 87.50, 98.90),
    ("archway", "DUMBO Archway", 40.7036, -73.9887, 81.33, 91.80),
    ("library", "Adams Street Library", 40.7027, -73.9878, 84.65, 98.10),
    ("frontpine", "Front and Pine Street", 40.7028, -73.9880, None, 94.40),
]

STATIONS = [
    ("york", "York St (F)", 40.701397, -73.98675),
    ("high", "High St (A,C)", 40.699337, -73.99053),
]

# The walk, as build_carousel.py already defines it, extended along the water.
WALK = [
    ("York Street F station", 40.70135, -73.98665),
    ("Water Street at the Archway", 40.70355, -73.98885),
    ("Main Street at the water", 40.70395, -73.99385),
    ("Empire Fulton Ferry lawn", 40.70325, -73.99560),
    ("Fulton Ferry Landing", 40.70305, -73.99585),
    ("Pier 1 promenade", 40.70055, -73.99730),
]

# agent-model.html's place list, verbatim, so this page can measure how far
# each eyeballed position sits from the ground it is supposed to name. Kept as
# a copy on purpose: if the agent model moves a place, the two disagree and the
# disagreement is the finding.
#
# The last field is agent-model.html's own `indoor` flag. It carries the whole
# weight of the test below. A shop inside a building footprint is correct and
# a viewpoint inside one cannot be, and without the flag both read as the same
# number. Copied from the model rather than judged here.
AGENT_PLACES = [
    ("york", "York St (F)", 40.7013, -73.9866, 0),
    ("high", "High St (A/C)", 40.6997, -73.9906, 0),
    ("bbwalk", "Brooklyn Bridge walkway exit", 40.6998, -73.9905, 0),
    ("ferry", "Fulton Ferry Landing", 40.7030, -73.9958, 0),
    ("washst", "Washington St view", 40.7037, -73.9903, 0),
    ("pebble", "Pebble Beach", 40.7042, -73.9938, 0),
    ("carousel", "Jane's Carousel", 40.7033, -73.9954, 0),
    ("mainpark", "Main Street Park lawn", 40.7040, -73.9945, 0),
    ("pier1", "Pier 1 lawn and promenade", 40.7008, -73.9975, 0),
    ("archway", "DUMBO Archway", 40.7036, -73.9887, 0),
    ("dogrun", "Brooklyn Bridge Dog Run", 40.7042, -73.9930, 0),
    ("empire", "Empire Stores", 40.7029, -73.9945, 1),
    ("waterst", "Water Street shops", 40.7033, -73.9900, 1),
    ("frontst", "Front Street shops", 40.7024, -73.9885, 1),
    ("timeout", "Time Out Market", 40.7030, -73.9948, 1),
    ("icecream", "Old Fulton eateries", 40.7032, -73.9960, 1),
    ("cafe", "Front Street cafes", 40.7025, -73.9882, 1),
    ("offices", "DUMBO offices", 40.7026, -73.9890, 1),
]

WALKABLE = {
    "footway", "pedestrian", "path", "steps", "living_street", "residential",
    "service", "unclassified", "tertiary", "secondary", "cycleway",
    "tertiary_link", "secondary_link", "track",
}

# Drawn width in metres per highway class. Not surveyed. These are drawing
# conventions so the plan reads, and the page says so rather than implying a
# carriageway survey nobody did.
ROADW = {
    "motorway": 14.0, "motorway_link": 8.0, "trunk": 12.0, "trunk_link": 7.0,
    "primary": 12.0, "primary_link": 7.0, "secondary": 10.0,
    "secondary_link": 6.0, "tertiary": 9.0, "tertiary_link": 6.0,
    "residential": 8.0, "living_street": 7.0, "unclassified": 7.0,
    "service": 4.5, "pedestrian": 6.0, "footway": 2.4, "path": 2.0,
    "steps": 2.0, "cycleway": 2.4, "track": 3.0, "corridor": 2.0,
}

# Metres, ground to underside of the deck over DUMBO. INFERRED, 1/5. See
# VISUAL-MODEL.md: no public source gives the deck elevation here, and it is
# the only object in the massing frame that is not surveyed to the roof.
DECK_H = 27.0
DECK_W = 36.0


def g(lat, lon):
    return ((lon - LON0) * MX, (lat - LAT0) * MY)


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


_cache = {}


def geodata():
    if "b" not in _cache:
        for name in ("buildings.json", "osm.json"):
            p = os.path.join(GEO, name)
            if not os.path.exists(p):
                raise SystemExit(
                    "missing %s\nrun: python data-collection/fetch_geodata.py"
                    % p)
        with open(os.path.join(GEO, "buildings.json"), encoding="utf-8") as fh:
            _cache["b"] = json.load(fh)
        with open(os.path.join(GEO, "osm.json"), encoding="utf-8") as fh:
            _cache["o"] = json.load(fh)
    return _cache["b"], _cache["o"]


# ---------------------------------------------------------------------------
# Geometry
# ---------------------------------------------------------------------------

def simplify(pts, tol):
    """Douglas-Peucker. Iterative, because a 600-point pier recurses deep."""
    if len(pts) < 3:
        return list(pts)
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        if b <= a + 1:
            continue
        ax, ay = pts[a]
        bx, by = pts[b]
        dx, dy = bx - ax, by - ay
        n = math.hypot(dx, dy)
        worst, wi = -1.0, -1
        for i in range(a + 1, b):
            px, py = pts[i]
            if n < 1e-9:
                d = math.hypot(px - ax, py - ay)
            else:
                d = abs(dy * px - dx * py + bx * ay - by * ax) / n
            if d > worst:
                worst, wi = d, i
        if worst > tol and wi > 0:
            keep[wi] = True
            stack.append((a, wi))
            stack.append((wi, b))
    return [p for p, k in zip(pts, keep) if k]


def ring_area(r):
    """Signed area, positive counter-clockwise."""
    s = 0.0
    for i in range(len(r)):
        x1, y1 = r[i]
        x2, y2 = r[(i + 1) % len(r)]
        s += x1 * y2 - x2 * y1
    return s / 2.0


def centroid(r):
    a = ring_area(r)
    if abs(a) < 1e-9:
        return (sum(p[0] for p in r) / len(r), sum(p[1] for p in r) / len(r))
    cx = cy = 0.0
    for i in range(len(r)):
        x1, y1 = r[i]
        x2, y2 = r[(i + 1) % len(r)]
        f = x1 * y2 - x2 * y1
        cx += (x1 + x2) * f
        cy += (y1 + y2) * f
    return (cx / (6 * a), cy / (6 * a))


def pt_in_ring(p, r):
    x, y = p
    inside = False
    n = len(r)
    for i in range(n):
        x1, y1 = r[i]
        x2, y2 = r[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xi = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < xi:
                inside = not inside
    return inside


def seg_dist(p, a, b):
    px, py = p
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    L = dx * dx + dy * dy
    if L < 1e-12:
        return math.hypot(px - ax, py - ay)
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / L))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def dist_to_ring(p, r):
    """Zero inside; otherwise metres to the nearest edge."""
    if pt_in_ring(p, r):
        return 0.0
    return min(seg_dist(p, r[i], r[(i + 1) % len(r)]) for i in range(len(r)))


# ---------------------------------------------------------------------------
# Buildings
# ---------------------------------------------------------------------------

def buildings():
    """Footprints in local metres, split near / far.

    Near footprints keep 0.6 m of detail because a pedestrian stands against
    them. Far footprints are across the river, are never approached, and are
    simplified to 6 m - they exist to give the far bank a silhouette, and
    carrying their doorways would be weight for nothing.
    """
    b, _ = geodata()
    near, far = [], []
    for rec in b["buildings"]:
        gm = rec["geom"]
        polys = ([gm["coordinates"]] if gm["type"] == "Polygon"
                 else gm["coordinates"])
        isnear = bool(rec.get("near", 1))
        for poly in polys:
            if not poly:
                continue
            ring = [g(pt[1], pt[0]) for pt in poly[0]]
            if len(ring) > 1 and ring[0] == ring[-1]:
                ring = ring[:-1]
            ring = simplify(ring, 0.6 if isnear else 6.0)
            if len(ring) < 3:
                continue
            if ring_area(ring) < 0:
                ring.reverse()
            h = rec["h"] * FT
            ge = rec["ge"] * FT
            if h <= 0:
                continue
            if not isnear and h < 12.0:
                # Across the river, below about four storeys, a footprint
                # contributes nothing a viewer can resolve and costs the same
                # bytes as one that does.
                continue
            (near if isnear else far).append({
                "bin": rec["bin"], "h": h, "ge": ge,
                "yr": rec.get("yr") or 0, "ring": ring,
            })
    return near, far


# ---------------------------------------------------------------------------
# Ways
# ---------------------------------------------------------------------------

def ways():
    """Classify every OSM way into what it is for on this page."""
    _, o = geodata()
    out = {"road": [], "foot": [], "steps": [], "rail": [], "span": [],
           "water": [], "park": [], "pier": [], "coast": []}
    for w in o["ways"]:
        t = w["tags"]
        pts = [g(p[1], p[0]) for p in w["geom"]]
        if len(pts) < 2:
            continue
        hw = t.get("highway")
        rw = t.get("railway")
        nat = t.get("natural")
        name = t.get("name") or ""
        if rw == "subway":
            kind = "span" if t.get("bridge") == "yes" else "rail"
        elif hw in ("footway", "path", "pedestrian", "cycleway", "corridor"):
            kind = "foot"
        elif hw == "steps":
            kind = "steps"
        elif hw:
            kind = "road"
        elif nat == "water":
            kind = "water"
        elif nat == "coastline":
            kind = "coast"
        elif t.get("leisure") == "park":
            kind = "park"
        elif t.get("man_made") == "pier":
            kind = "pier"
        else:
            continue
        closed = (t.get("area") == "yes" or kind in ("water", "park")
                  or (len(pts) > 3 and pts[0] == pts[-1]
                      and kind in ("pier",)))
        tol = 1.2 if kind in ("foot", "steps", "road", "span", "rail") else 2.5
        s = simplify(pts, tol)
        if len(s) < 2:
            continue
        rec = {"p": s, "n": name}
        if kind == "road":
            rec["w"] = ROADW.get(hw, 6.0)
            rec["hw"] = hw
        elif kind in ("foot", "steps"):
            rec["w"] = ROADW.get(hw, 2.2)
            rec["hw"] = hw
        if closed:
            rec["c"] = 1
        out[kind].append(rec)
    return out


def water_band(coast, near, far):
    """Turn the open coastline into something the renderer can fill.

    THE EAST RIVER IS NOT A POLYGON IN THIS DATA. OpenStreetMap models a
    shoreline as an OPEN way tagged natural=coastline, with the convention
    that land lies to the LEFT of the direction of travel. The only closed
    natural=water polygons in the extent are five small ponds. So a renderer
    that fills what it is given draws the ponds and leaves the river as bare
    ground - which is what the first version of this page did, and it read as
    haze rather than as water.

    Each coastline is therefore thickened to the water side and emitted as
    ONE QUAD PER SEGMENT, clamped to the modelled extent so the water stops
    where the data stops rather than running to the horizon.

    TWO THINGS HERE WERE WRONG BEFORE AND BOTH FAILED SILENTLY.

    ONE. The band was a single ring closed back on itself. Clamping its outer
    edge to a rectangle makes that ring SELF-INTERSECT, and a self-intersecting
    ring is filled differently by the two standard rules: this file's own
    point-in-polygon test is even-odd, and canvas fill is nonzero. So the
    check that chose the side and the code that drew it disagreed about which
    region the polygon even was. Per-segment quads are simple polygons, on
    which the two rules agree, and overlapping quads simply paint over each
    other.

    TWO. The side was chosen by counting buildings inside the candidate ring,
    which is a GLOBAL test on a shape that can be a thousand times longer than
    it is wide. It is now a LOCAL one: step 220 m off each side of the
    coastline at intervals and count surveyed footprints within 220 m of the
    sample. Land has buildings beside it; water does not. A shoreline where
    both sides look the same is reported and dropped, because a tie is not an
    answer and resolving it by argument order is how the eastern half of
    Brooklyn ended up under the East River.
    """
    marks = [b["ring"][0] for b in near] + [b["ring"][0] for b in far]
    cell = 240.0
    grid = {}
    for m in marks:
        grid.setdefault((int(m[0] // cell), int(m[1] // cell)), []).append(m)

    def nbrs(x, y, r):
        n = 0
        for gx in range(int((x - r) // cell), int((x + r) // cell) + 1):
            for gy in range(int((y - r) // cell), int((y + r) // cell) + 1):
                for m in grid.get((gx, gy), ()):
                    if (m[0] - x) ** 2 + (m[1] - y) ** 2 <= r * r:
                        n += 1
        return n

    bb = geodata()[1]["context_bbox"]        # [W, S, E, N], from the fetch
    x0, y0 = g(bb[1], bb[0])
    x1, y1 = g(bb[3], bb[2])
    OFF, PROBE = 3000.0, 220.0
    out = []
    for c in coast:
        p = simplify(c["p"], 8.0)
        if len(p) < 2:
            continue
        score = [0, 0]
        for i in range(0, len(p) - 1, max(1, len(p) // 30)):
            a, b = p[i], p[i + 1]
            dx, dy = b[0] - a[0], b[1] - a[1]
            L = math.hypot(dx, dy) or 1.0
            mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            for j, sign in enumerate((1, -1)):
                score[j] += nbrs(mx + sign * (dy / L) * PROBE,
                                 my - sign * (dx / L) * PROBE, PROBE)
        if score[0] == score[1]:
            print("  coastline of %d pts: %d buildings on both sides, "
                  "cannot tell water from land; dropped" % (len(p), score[0]))
            continue
        sign = 1 if score[0] < score[1] else -1

        def off(pt, dx, dy, L):
            return [min(max(pt[0] + sign * (dy / L) * OFF, x0), x1),
                    min(max(pt[1] - sign * (dx / L) * OFF, y0), y1)]

        for i in range(len(p) - 1):
            a, b = p[i], p[i + 1]
            dx, dy = b[0] - a[0], b[1] - a[1]
            L = math.hypot(dx, dy) or 1.0
            out.append({"p": [a, b, off(b, dx, dy, L), off(a, dx, dy, L)],
                        "c": 1})
    return out


# ---------------------------------------------------------------------------
# The walkable graph
# ---------------------------------------------------------------------------

def graph():
    """Nodes and undirected edges over walkable OSM ways, in local metres.

    Same rule as build_carousel.py: this is a walk UNDERNEATH the bridge, so
    the bridge's own walkway is excluded. Without that the router happily
    sends a pedestrian over the river to Manhattan and back.
    """
    _, o = geodata()
    idx, pts, adj = {}, [], {}

    def node(lon, lat):
        k = (round(lon, 6), round(lat, 6))
        if k not in idx:
            idx[k] = len(pts)
            pts.append(g(lat, lon))
        return idx[k]

    for w in o["ways"]:
        t = w["tags"]
        if t.get("highway") not in WALKABLE:
            continue
        if t.get("bridge") == "yes" and "Manhattan Bridge" in (t.get("name") or ""):
            continue
        seq = [node(p[0], p[1]) for p in w["geom"]]
        for a, b in zip(seq, seq[1:]):
            if a == b:
                continue
            d = math.dist(pts[a], pts[b])
            adj.setdefault(a, set()).add(b)
            adj.setdefault(b, set()).add(a)
    return pts, adj


def largest_component(pts, adj):
    """The walk network a person can actually reach without teleporting.

    OSM in a dense district always contains orphan fragments - a service road
    behind a loading dock that was mapped but never connected. Spawning an
    agent on one produces a figure that walks four metres back and forth for
    the whole run, which looks like a rendering bug and is not one.
    """
    seen, best = set(), []
    for s in adj:
        if s in seen:
            continue
        comp, stack = [], [s]
        seen.add(s)
        while stack:
            u = stack.pop()
            comp.append(u)
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        if len(comp) > len(best):
            best = comp
    return set(best)


def dijkstra(pts, adj, src, dst):
    import heapq
    dist = {src: 0.0}
    prev = {}
    pq = [(0.0, src)]
    done = set()
    while pq:
        d, u = heapq.heappop(pq)
        if u in done:
            continue
        done.add(u)
        if u == dst:
            break
        for v in adj.get(u, ()):
            nd = d + math.dist(pts[u], pts[v])
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
    return path, dist[dst]


def nearest_node(pts, keep, p):
    best, bi = 1e18, -1
    for i in keep:
        d = (pts[i][0] - p[0]) ** 2 + (pts[i][1] - p[1]) ** 2
        if d < best:
            best, bi = d, i
    return bi, math.sqrt(best)


# ---------------------------------------------------------------------------
# What this map is able to say about the positions it inherited
# ---------------------------------------------------------------------------

def place_report(near, pts, keep):
    """Measure every eyeballed position against surveyed ground.

    Three questions, each with a definite answer and none of them previously
    askable:

      inside   does the point lie INSIDE a surveyed building footprint? For a
               place called a lawn, a beach or a promenade that is not an
               approximation, it is a position that cannot be right.
      facade   metres to the nearest building wall.
      network  metres to the nearest node of the walkable network. A place
               nobody can walk to is a place no pedestrian model should be
               spawning anyone at.

    Nothing here is corrected automatically. A measured offset with the
    original still beside it is evidence; a quietly moved coordinate is just a
    different guess with the audit trail deleted.
    """
    rows = []
    for pid, name, lat, lon, indoor in AGENT_PLACES:
        p = g(lat, lon)
        inside = None
        fac = 1e18
        for b in near:
            d = dist_to_ring(p, b["ring"])
            if d < fac:
                fac, inside = d, b
            if d == 0.0:
                break
        ni, nd = nearest_node(pts, keep, p)
        rows.append({
            "id": pid, "name": name, "lat": lat, "lon": lon,
            "indoor": indoor,
            "x": round(p[0], 1), "y": round(p[1], 1),
            "inside": 1 if fac == 0.0 else 0,
            # An OUTDOOR place inside a building footprint. This is the only
            # cell in the table that is a defect rather than a distance.
            "impossible": 1 if (fac == 0.0 and not indoor) else 0,
            "facade": round(fac, 1),
            "bin": inside["bin"] if inside else "",
            "bh": round(inside["h"], 1) if inside else 0,
            "net": round(nd, 1),
        })
    return rows


def anchor_report(near, pts, keep):
    rows = []
    for aid, name, lat, lon, leq, peak in ANCHORS:
        p = g(lat, lon)
        fac, hit = 1e18, None
        for b in near:
            d = dist_to_ring(p, b["ring"])
            if d < fac:
                fac, hit = d, b
            if d == 0.0:
                break
        _, nd = nearest_node(pts, keep, p)
        rows.append({
            "id": aid, "name": name, "leq": leq, "peak": peak,
            "x": round(p[0], 1), "y": round(p[1], 1),
            "inside": 1 if fac == 0.0 else 0,
            "facade": round(fac, 1),
            "bin": hit["bin"] if hit else "",
            "net": round(nd, 1),
        })
    return rows


# ---------------------------------------------------------------------------
# The route, and the payload the page is drawn from
# ---------------------------------------------------------------------------

def walk_route(pts, adj, keep):
    """The named walk, routed over the real network rather than drawn as a line."""
    legs, marks, snaps, total = [], [], [], 0.0
    ids = []
    for name, lat, lon in WALK:
        i, off = nearest_node(pts, keep, g(lat, lon))
        ids.append((name, i, off))
    for (n0, i0, o0), (n1, i1, o1) in zip(ids, ids[1:]):
        path, d = dijkstra(pts, adj, i0, i1)
        if path is None:
            raise SystemExit("no walkable route from %s to %s" % (n0, n1))
        marks.append({"n": n0, "s": round(total, 1)})
        legs.append(path)
        total += d
    marks.append({"n": ids[-1][0], "s": round(total, 1)})
    snaps = [{"n": n, "off": round(o, 1)} for n, i, o in ids]
    poly = []
    for k, leg in enumerate(legs):
        poly += leg if k == 0 else leg[1:]
    return poly, round(total, 1), marks, snaps


def bridge_span():
    """Deck centreline as the mean of the tracks the deck carries.

    The centreline is MAPPED. The deck ELEVATION is not - no public source
    gives it over DUMBO, which VISUAL-MODEL.md records as the only object in
    the massing frame that is not surveyed to the roof. The page draws it in
    a different colour with a hatched soffit for exactly that reason.

    WHY THIS IS NOT A CHAINING PROBLEM. The first version of this function
    sorted the bridge-carried ways by length and joined any whose endpoints
    came within 40 m. That is the right algorithm for a route split into
    consecutive pieces and the wrong one here: the Manhattan Bridge carries
    FOUR PARALLEL TRACKS, about 10 m apart, and the end of one track is
    within 40 m of the end of its neighbour. The joiner therefore ran up
    one track and back down the next, producing a polyline that doubled
    back on itself. It threw no error and the deck simply drew as a fold.

    So the tracks are not joined at all. Every vertex of every bridge-carried
    way is projected onto the principal axis of the whole set, binned by
    chainage, and averaged across the bin. That is the deck's centreline by
    construction, and it is what the deck is: the mean of what it carries.
    """
    _, o = geodata()
    pts = []
    for w in o["ways"]:
        t = w["tags"]
        if t.get("railway") == "subway" and t.get("bridge") == "yes":
            pts += [g(p[1], p[0]) for p in w["geom"]]
    if len(pts) < 8:
        raise SystemExit("no bridge-carried subway geometry in osm.json")

    mx = sum(p[0] for p in pts) / len(pts)
    my = sum(p[1] for p in pts) / len(pts)
    sxx = syy = sxy = 0.0
    for x, y in pts:
        dx, dy = x - mx, y - my
        sxx += dx * dx
        syy += dy * dy
        sxy += dx * dy
    th = 0.5 * math.atan2(2 * sxy, sxx - syy)
    ux, uy = math.cos(th), math.sin(th)
    if uy < 0:                      # point the axis northward
        ux, uy = -ux, -uy

    bearing = (math.degrees(math.atan2(ux, uy))) % 360
    if not (325.0 <= bearing <= 350.0):
        # The published figure is 336.93 deg. Anything outside this band means
        # geometry from another structure has entered the set - which is how
        # the Williamsburg Bridge got in once. See fetch_geodata._outside.
        raise SystemExit("bridge axis fitted to %.2f deg, outside 325-350; "
                         "check the extent filter" % bearing)

    BIN = 60.0
    bins = {}
    for x, y in pts:
        s = (x - mx) * ux + (y - my) * uy
        k = int(math.floor(s / BIN))
        b = bins.setdefault(k, [0.0, 0.0, 0])
        b[0] += x
        b[1] += y
        b[2] += 1
    line = [[b[0] / b[2], b[1] / b[2]] for _, b in sorted(bins.items())]
    return simplify(line, 2.0)


def q(v, n=1):
    """Round for transport. Decimetres are finer than the data deserves."""
    return round(v, n)


def payload():
    near, far = buildings()
    W = ways()
    pts, adj = graph()
    keep = largest_component(pts, adj)
    poly, total, marks, snaps = walk_route(pts, adj, keep)

    # The graph, renumbered over the reachable component only, so the page
    # cannot spawn anybody on an orphan fragment.
    order = sorted(keep)
    remap = {n: i for i, n in enumerate(order)}
    gnodes = [[q(pts[n][0]), q(pts[n][1])] for n in order]
    gedges = []
    for n in order:
        for m in adj[n]:
            if m in remap and remap[n] < remap[m]:
                gedges.append([remap[n], remap[m]])

    def ring(r):
        return [[q(x), q(y)] for x, y in r]

    def cring(r):
        # Context geometry is silhouette. Whole metres are finer than a
        # building 900 m away across a river can be seen to.
        return [[q(x, 0), q(y, 0)] for x, y in r]

    def line(p):
        return [[q(x), q(y)] for x, y in p]

    P = {
        "grid": {"lat0": LAT0, "lon0": LON0, "mx": q(MX, 3), "my": MY},
        "near": [{"r": ring(b["ring"]), "h": q(b["h"]), "g": q(b["ge"]),
                  "y": b["yr"], "b": b["bin"]} for b in near],
        "far": [{"r": cring(b["ring"]), "h": q(b["h"], 0)} for b in far],
        "road": [{"p": line(w["p"]), "w": w["w"], "n": w["n"]} for w in W["road"]],
        "foot": [{"p": line(w["p"]), "w": w["w"]} for w in W["foot"]],
        "steps": [{"p": line(w["p"])} for w in W["steps"]],
        "park": [{"p": line(w["p"])} for w in W["park"]],
        "water": [{"p": line(w["p"])} for w in W["water"]],
        "band": [{"p": cring(w["p"])} for w in water_band(W["coast"], near, far)],
        "coast": [{"p": line(w["p"])} for w in W["coast"]],
        "pier": [{"p": line(w["p"])} for w in W["pier"]],
        "rail": [{"p": line(w["p"])} for w in W["rail"]],
        "span": line(bridge_span()),
        "deck": {"h": DECK_H, "w": DECK_W},
        "graph": {"n": gnodes, "e": gedges},
        "route": {"p": [remap[n] for n in poly], "len": total,
                  "marks": marks, "snaps": snaps},
        "anchors": anchor_report(near, pts, keep),
        "places": place_report(near, pts, keep),
        "stations": [{"id": i, "n": n, "x": q(g(la, lo)[0]), "y": q(g(la, lo)[1])}
                     for i, n, la, lo in STATIONS],
    }
    return P


# ---------------------------------------------------------------------------
# The page
# ---------------------------------------------------------------------------

CSS = """
:root {
  --cp-bg:#f7f4ef; --cp-ink:#1c1b1a; --cp-mut:#5f5b56; --cp-line:#ddd6cb;
  --cp-card:#fffdfa; --cp-accent:#8c3b2e; --cp-good:#2f6b4f; --cp-warn:#8a6d1f;
  --wm-sky-a:#b7c8dc; --wm-sky-b:#e8eef3; --wm-ground:#e2dccf;
  --wm-water:#8fb4cc; --wm-park:#b6cfa4; --wm-road:#cfc6b6; --wm-foot:#f3ede0;
  --wm-roof:#c3b8a8; --wm-wallA:#b8ac9c; --wm-wallB:#9a8e7e; --wm-wallC:#7d7264;
  --wm-far:#8d9cb0; --wm-edge:#6f665c;
  --wm-infer:#a8642c; --wm-meas:#8c3b2e; --wm-agent:#2f5f8c;
}
html[data-theme="dark"] {
  --cp-bg:#232221; --cp-ink:#ece7e0; --cp-mut:#a49d94; --cp-line:#3d3b3a;
  --cp-card:#2b2a29; --cp-accent:#e08b74; --cp-good:#78c39c; --cp-warn:#d9b558;
  --wm-sky-a:#141d29; --wm-sky-b:#2b3440; --wm-ground:#2f2c29;
  --wm-water:#16303f; --wm-park:#28402a; --wm-road:#413c36; --wm-foot:#544d43;
  --wm-roof:#544c44; --wm-wallA:#484038; --wm-wallB:#39332d; --wm-wallC:#2c2723;
  --wm-far:#222c38; --wm-edge:#8b8177;
  --wm-infer:#d98f4e; --wm-meas:#e08b74; --wm-agent:#7fb2e0;
}
* { box-sizing:border-box; }
body { margin:0; background:var(--cp-bg); color:var(--cp-ink);
  font:15px/1.62 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; }
.wrap { max-width:1180px; margin:0 auto; padding:0 22px 64px; }
.card { background:var(--cp-card); border:1px solid var(--cp-line);
  border-radius:12px; padding:22px; margin:20px 0; }
h1 { font-size:30px; line-height:1.22; margin:26px 0 8px; letter-spacing:-0.01em; }
h2 { font-size:20px; margin:0 0 10px; }
h3 { font-size:16px; margin:20px 0 6px; }
p { margin:10px 0; }
.lede { color:var(--cp-mut); font-size:16px; }
.mono { font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  font-size:13px; }
table { border-collapse:collapse; width:100%; font-size:14px; margin:12px 0; }
th,td { border-bottom:1px solid var(--cp-line); padding:7px 9px;
  text-align:left; vertical-align:top; }
th { font-weight:600; color:var(--cp-mut); font-size:12.5px;
  text-transform:uppercase; letter-spacing:0.05em; }
td.num, th.num { text-align:right;
  font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; }
.tw { overflow-x:auto; }
.bad { color:var(--cp-accent); font-weight:600; }
.ok { color:var(--cp-good); }
.warn { color:var(--cp-warn); }
ul,ol { margin:10px 0; padding-left:22px; }
li { margin:6px 0; }

/* -- the viewport ------------------------------------------------------- */
.stage { position:relative; border:1px solid var(--cp-line);
  border-radius:12px; overflow:hidden; background:var(--wm-sky-b);
  aspect-ratio:16/10; min-height:420px; }
.stage canvas { display:block; width:100%; height:100%; cursor:grab;
  touch-action:none; }
.stage canvas.drag { cursor:grabbing; }
.hud { position:absolute; pointer-events:none;
  font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  font-size:12px; line-height:1.5; }
.hud.tl { top:10px; left:10px; }
.hud.br { bottom:10px; right:10px; text-align:right; }
.hud .box { display:inline-block; background:var(--cp-card);
  border:1px solid var(--cp-line); border-radius:8px; padding:7px 10px;
  opacity:0.94; }
.bar { display:flex; flex-wrap:wrap; gap:8px; align-items:center;
  margin:12px 0 0; }
.bar .grp { display:flex; gap:0; border:1px solid var(--cp-line);
  border-radius:8px; overflow:hidden; }
button { font:inherit; font-size:13px; padding:6px 12px; cursor:pointer;
  background:var(--cp-card); color:var(--cp-ink); border:1px solid var(--cp-line);
  border-radius:8px; }
.bar .grp button { border:0; border-right:1px solid var(--cp-line);
  border-radius:0; }
.bar .grp button:last-child { border-right:0; }
button[aria-pressed="true"] { background:var(--cp-ink); color:var(--cp-card); }
button:focus-visible { outline:2px solid var(--cp-accent); outline-offset:2px; }
.lg { display:flex; flex-wrap:wrap; gap:6px 18px; margin:14px 0 0;
  font-size:13px; color:var(--cp-mut); }
.lg span { display:inline-flex; align-items:center; gap:7px; }
.sw { width:14px; height:14px; border-radius:3px; border:1px solid var(--cp-edge);
  display:inline-block; }
.note { font-size:13.5px; color:var(--cp-mut); margin-top:10px; }
.keys { font-size:13px; color:var(--cp-mut); }
kbd { font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  font-size:12px; border:1px solid var(--cp-line); border-bottom-width:2px;
  border-radius:4px; padding:1px 5px; background:var(--cp-bg); }
.rate { display:inline-block; font-size:11.5px; padding:1px 7px;
  border-radius:999px; border:1px solid var(--cp-line); color:var(--cp-mut);
  font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; }
.grid2 { display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr));
  gap:16px; }
.stat { border:1px solid var(--cp-line); border-radius:10px; padding:13px 15px; }
.stat b { display:block; font-size:25px; line-height:1.15; font-weight:650; }
.stat span { color:var(--cp-mut); font-size:13px; }
@media (max-width:760px) { .wrap { padding:0 16px 48px; } h1 { font-size:25px; }
  .stage { aspect-ratio:4/3; } }
"""


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The walkable model: DUMBO from York Street to Pier 1</title>
<meta name="description" content="A walkable model of DUMBO drawn from surveyed building footprints and the open footway network, with the four measured points standing where they actually stand.">
<style>__CSS__</style>
</head>
<body>
<div class="wrap">

<h1>The walkable model</h1>
<p class="lede">DUMBO from the York Street F platform to Brooklyn Bridge Park
Pier 1, drawn from <strong>__NNEAR__ surveyed building footprints</strong> and
the open street and footway network. Every position on this page is on the
same local grid as the agent model and the canyon drawings, so a coordinate
here and a coordinate there are the same number.</p>

<div class="card">
  <div class="grid2">__STATS__</div>
</div>

<div class="card">
  <div class="stage">
    <canvas id="vp" width="900" height="560"
            aria-label="Interactive model of DUMBO. Drag to look, scroll to zoom."></canvas>
    <div class="hud tl"><div class="box">
      <div id="h1">&#8212;</div><div id="h2">&#8212;</div><div id="h3">&#8212;</div>
    </div></div>
  </div>

  <div class="bar">
    <span class="grp">
      <button data-mode="model" aria-pressed="true">Model</button>
      <button data-mode="plan" aria-pressed="false">Plan</button>
      <button data-mode="walk" aria-pressed="false">Eye level</button>
    </span>
    <span class="grp">
      <button data-toggle="build" aria-pressed="true">Buildings</button>
      <button data-toggle="paths" aria-pressed="true">Paths</button>
      <button data-toggle="agents" aria-pressed="true">Figures</button>
      <button data-toggle="marks" aria-pressed="true">Measured points</button>
      <button data-toggle="sound" aria-pressed="false">Level wash</button>
    </span>
    <button id="tour" aria-pressed="false">Walk the route</button>
    <button id="reset">Reset view</button>
  </div>
  <p class="keys" id="keys" hidden><kbd>W</kbd><kbd>A</kbd><kbd>S</kbd><kbd>D</kbd>
    or the arrow keys to move, <kbd>Q</kbd> and <kbd>E</kbd> to turn, drag to
    look. Eye height is 1.62&#8201;m.</p>

  <div class="lg">
    <span><i class="sw" style="background:var(--wm-wallB)"></i>
      building, surveyed footprint and roof height <span class="rate">5/5</span></span>
    <span><i class="sw" style="background:var(--wm-foot)"></i>
      footway, path, steps <span class="rate">4/5</span></span>
    <span><i class="sw" style="background:var(--wm-road)"></i>
      carriageway <span class="rate">4/5</span></span>
    <span><i class="sw" style="background:var(--wm-infer)"></i>
      bridge deck, hatched &#8212; <strong>elevation inferred</strong>
      <span class="rate">1/5</span></span>
    <span><i class="sw" style="background:var(--wm-meas)"></i>
      MTA measured point <span class="rate">level 5/5, position 2/5</span></span>
    <span><i class="sw" style="background:var(--wm-agent)"></i>
      walking figure <span class="rate">1/5, invented</span></span>
  </div>

  <p class="note">The figures walk the real network and nothing else about
  them is real. They are here to show that the network is connected and where
  it goes. Their number is a constant in the source. No count of pedestrians
  in this corridor has ever been made.</p>
</div>

<div class="card">
<h2>What this page was built to settle</h2>
<p>Until this page existed, every position in this repository was typed to
four decimal places off a basemap. Four decimal places of latitude is about
11&#8201;m. The canyon under the bridge is 91&#8201;m wide, so an 11&#8201;m
error is an eighth of the width of the thing being described &#8212; and it
was never measured, because there was nothing to measure it against.</p>

<p>There is now. Each inherited position can be tested against surveyed
ground with three questions that have definite answers:</p>
<ol>
<li><strong>Does it lie inside a building?</strong> For a place the model
itself marks as outdoors, that is not an approximation. It is a position that
cannot be right.</li>
<li><strong>How far is the nearest wall?</strong></li>
<li><strong>How far is the nearest walkable path?</strong> A place nobody can
walk to is a place no pedestrian model should be spawning anybody at.</li>
</ol>

<h3>The result</h3>
<p><strong>__NIMPOSS__ of __NPLACES__</strong> places in the agent model are
marked outdoors and fall inside a surveyed building footprint:
<strong>__IMPOSSLIST__</strong>. A further __NINDOOROK__ fall inside a
footprint and are marked indoors, which is correct and is why the indoor flag
is carried here rather than judged.</p>

<p>__NANIN__ of the four points the MTA instrumented also resolve inside a
building footprint: <strong>__ANINLIST__</strong>. That is not necessarily an
error &#8212; the memo describes indoor sessions as well as outdoor ones, and
section 1.7 of the concept document already found that the indoor rows behave
differently from the outdoor ones. It is recorded here because it is
checkable and because nothing else in this repository could have checked
it.</p>

<p class="note"><strong>Nothing has been moved.</strong> Not one coordinate in
the agent model was corrected by this page. A measured offset published beside
the original is evidence; a quietly edited coordinate is a different guess
with the audit trail deleted. The corrections belong in the model, made
deliberately, with the reason recorded &#8212; not as a side effect of
building a drawing.</p>

<div class="tw"><table>
<thead><tr><th>Position inherited from the agent model</th><th>Marked</th>
<th>Against surveyed footprints</th><th class="num">m to path</th></tr></thead>
<tbody>__PLACEROWS__</tbody>
</table></div>
</div>

<div class="card">
<h2>The four measured points, on real ground</h2>
<p>Levels are quoted from the MTA's own memo and are rated 5/5. The
<em>positions</em> are ours, digitised from the memo's written descriptions,
and are rated 2/5. This table is the first time the two ratings have been
visible in the same row.</p>
<div class="tw"><table>
<thead><tr><th>Point</th><th class="num">L<sub>eq</sub> dB(A)</th>
<th class="num">peak dB(A)</th><th>Against surveyed footprints</th>
<th class="num">m to path</th></tr></thead>
<tbody>__ANCHORROWS__</tbody>
</table></div>
<p class="note">The level wash in plan view is inverse-distance weighting in
the energy domain between those four numbers. It is an interpolation, not a
propagation model, and the agent model records why one cannot be fitted here:
jittering the digitised positions by the width of their own uncertainty moves
the fitted decay exponent anywhere from 0.7 to 22.3.</p>
</div>

<div class="card">
<h2>The walk, routed rather than drawn</h2>
<p>__ROUTELEN__&#8201;m from the York Street F platform to Pier 1, computed
over the real footway network by shortest path rather than drawn as a line
between waypoints. It now continues along the water past Jane's Carousel to
Fulton Ferry Landing before turning down to Pier 1, which is the walk people
actually take and which the earlier drawing stopped short of.</p>

<p class="note"><strong>__ROUTELEN__&#8201;m and 1,482.44&#8201;m are two
different walks, not two estimates of one walk.</strong> The carousel page
publishes 1,482.44&#8201;m over five waypoints. This page adds a sixth,
Fulton Ferry Landing, because a route that stops at the water's edge leaves
out the half of the walk that goes back under the bridge &#8212; which is the
half the canyon argument is about. Nothing has been corrected. The carousel
figure is still right for the route it describes, and the two must never be
quoted against each other as though one superseded the other.</p>
<div class="grid2">
<div><h3>Where each waypoint had to be snapped</h3>
<div class="tw"><table><thead><tr><th>Waypoint</th>
<th class="num">m to nearest path node</th></tr></thead>
<tbody>__SNAPROWS__</tbody></table></div>
<p class="note">The worst is <strong>__WORSTSNAPN__ at
__WORSTSNAP__&#8201;m</strong>. That is the honest size of the gap between a
name on a map and a place a person can stand.</p></div>
<div><h3>Chainage along the walk</h3>
<div class="tw"><table><thead><tr><th>Waypoint</th>
<th class="num">m from York Street</th></tr></thead>
<tbody>__MARKROWS__</tbody></table></div></div>
</div>
</div>

<div class="card">
<h2>Two references were checked first, and neither one won</h2>
<p>This page was asked for with two examples attached: <strong>GeoLibre</strong>,
an open-source geospatial platform, and <strong>Race Condition</strong>, an
earlier project of ours that renders a marathon through a city in 3D. Both were
read properly &#8212; source, data files, build steps &#8212; before a line of
this was written. The finding has the same shape this repository keeps
producing: <strong>the thing you reach for is downstream of, and worse than,
the thing already sitting in the repository.</strong></p>

<div class="tw"><table>
<thead><tr><th></th><th>Race Condition</th><th>GeoLibre</th>
<th>This repository</th></tr></thead>
<tbody>
<tr><th>Building geometry</th><td>Way <em>centroids</em>, 2,568 points</td>
<td>Vector tiles, <span class="mono">fill-extrusion</span></td>
<td><strong>Footprint polygons, 2,342</strong></td></tr>
<tr><th>Building heights</th>
<td>A hash: <span class="mono">4 + frac(sin(x&middot;127.1 +
z&middot;311.7)&middot;43758.5453) &middot; 30</span></td>
<td>Whatever the tile source carries</td>
<td><strong>Surveyed roof height, plus ground elevation, year, BIN</strong></td></tr>
<tr><th>Area covered</th><td>Midtown Manhattan</td><td>Anywhere</td>
<td>DUMBO and the far bank</td></tr>
<tr><th>Pedestrian routing</th><td>Agents on a fixed spline</td>
<td>Driving profile only</td>
<td><strong>Footway graph, __NNODES__ nodes</strong></td></tr>
<tr><th>Ships as one file</th><td>No &#8212; needs a package install and a
build</td><td>No &#8212; its HTML export is an iframe to a hosted app</td>
<td><strong>Yes</strong></td></tr>
</tbody>
</table></div>

<p>Race Condition's own backlog says it plainly: <em>&#8220;Building heights:
synthetic&#8221;</em>. Its photoreal look does not come from its data at all &#8212;
it comes from a proprietary photogrammetry export that is not in the
repository. GeoLibre is a serious piece of work and the disqualifier is narrow
and absolute: its Python export writes an
<span class="mono">&lt;iframe&gt;</span> pointing at a hosted application, so
the artifact stops working the moment the network does. Everything in this
repository has to open from a file on disk with nothing fetched.</p>

<p><strong>What was taken from each.</strong> From Race Condition, the
<em>pattern</em> &#8212; an instanced city, agents constrained to a path, an
anchor-relative local grid in metres, one animation loop. That pattern is
sound and it is what this page is built on. From GeoLibre, one <em>pointer</em>:
its Overture Maps layer carries building footprints with a height field, which
is the plausible route to heights for the far bank, since the city file that
supplies every height here stops at the New York City line.</p>

<p class="note">The comparison is not a criticism of either project. Both are
built for a general case. This one had a city file with surveyed roof heights
already in it, and the general case cannot beat that. The transferable part is
that the check took an afternoon and would have cost weeks had the answer been
assumed the other way.</p>
</div>

<div class="card">
<h2>Where this is likely to be wrong</h2>
<ol>
<li><strong>The bridge deck elevation is invented.</strong> It is drawn at
__DECKH__&#8201;m because something had to be drawn. No public source gives
the deck elevation over DUMBO, which is why it is the only object in the
massing frame not surveyed to the roof, and why it is hatched here. Every
sightline this page appears to show under the bridge inherits that number.</li>
<li><strong>Carriageway and path widths are a drawing convention.</strong>
OpenStreetMap gives a centreline, not a kerb. The ribbons are drawn at
plausible widths so the plan reads. They are not a survey and no measurement
should be taken off them.</li>
<li><strong>The street network is crowd-mapped, not surveyed.</strong> The
building footprints are the city's own file; the paths are OpenStreetMap.
Those are not the same standard of evidence and they are drawn on the same
page, which invites reading them as if they were.</li>
<li><strong>Ground is flat at zero.</strong> The footprint file carries a
ground elevation per building and it is used for the base of each wall, but
there is no terrain surface between them. DUMBO rises away from the water;
this model does not.</li>
<li><strong>The figures are not a population.</strong> Their count is a
constant, their speed is one number, and they choose turnings at random. The
population model is a different artifact with a different and much longer
list of what is invented in it.</li>
<li><strong>Only the largest connected component is walkable here.</strong>
Orphan fragments in the network were dropped so that no figure spawns on a
disconnected stub. That is right for the drawing and it means the node count
on this page is smaller than the raw network.</li>
<li><strong>Across the river is decoration.</strong> Footprints there are
simplified to whole metres, anything under about four storeys is dropped
entirely, and none of it is walked, measured or reasoned over.</li>
<li><strong>An offset is not a correction.</strong> This page measures how
far each inherited position sits from surveyed ground. It does not establish
where the position should have been, and for the MTA points it cannot,
because the memo describes them in words rather than coordinates.</li>
<li><strong>The span stops where the data stops.</strong> The deck is drawn
only where bridge-carried track geometry was fetched, so it ends in mid-air
over Manhattan rather than at an abutment. Nothing has been extrapolated to
make it look finished.</li>
<li><strong>The evaluation of the two reference projects is a snapshot.</strong>
Both are actively developed. The finding is about the state of each on the day
it was read, and the files that carry it are named so the claim can be
re-checked rather than taken on trust.</li>
</ol>
</div>

<div class="card">
<h2>Sources, and how to rebuild every line of this</h2>
<ul>
<li><strong>Building footprints and roof heights</strong> &#8212; NYC
OpenData <span class="mono">5zhs-2jue</span>, the city's building file.
__NNEAR__ in the walkable extent, __NFAR__ across the river.
<span class="rate">5/5</span></li>
<li><strong>Streets, footways, steps, piers, parks, shoreline</strong> &#8212;
OpenStreetMap via Overpass, &copy; OpenStreetMap contributors, ODbL 1.0.
__NROAD__ carriageways and __NFOOT__ footways and steps.
<span class="rate">4/5</span></li>
<li><strong>Walkable network</strong> &#8212; derived from the above:
__NNODES__ connected nodes, __NEDGES__ edges.</li>
<li><strong>Sound levels</strong> &#8212; MTA's own instrumented sessions, as
quoted in the concept document. <span class="rate">5/5</span></li>
</ul>
<p class="note">Nothing here is traced off a proprietary basemap. Fetch the
data with <span class="mono">data-collection/fetch_geodata.py</span> and
redraw this page with <span class="mono">build_walkable_map.py</span>. Built
__BUILT__.</p>
</div>

</div>
<script>window.__WM__=/*PAYLOAD*/;</script>
<script>(function () {
'use strict';
var D = window.__WM__;
var cv = document.getElementById('vp');
var ctx = cv.getContext('2d');
var W = 0, H = 0, DPR = 1;

/* ---------------------------------------------------------------- theme */
function cvar(n) {
  return getComputedStyle(document.documentElement).getPropertyValue(n).trim();
}
function hex(h) {
  h = (h || '#888888').replace('#', '');
  if (h.length === 3) h = h[0]+h[0]+h[1]+h[1]+h[2]+h[2];
  var v = parseInt(h, 16);
  if (isNaN(v)) v = 0x888888;
  return [(v >> 16) & 255, (v >> 8) & 255, v & 255];
}
var C = {};
function readTheme() {
  var names = ['sky-a','sky-b','ground','water','park','road','foot','roof',
               'wallA','wallB','wallC','far','edge','infer','meas','agent'];
  C = {};
  names.forEach(function (n) { C[n] = hex(cvar('--wm-' + n)); });
  C.ink = cvar('--cp-ink'); C.card = cvar('--cp-card');
  C.line = cvar('--cp-line'); C.mut = cvar('--cp-mut');
}
function rgb(c) { return 'rgb(' + (c[0]|0) + ',' + (c[1]|0) + ',' + (c[2]|0) + ')'; }
function mix(a, b, t) {
  if (t < 0) t = 0; if (t > 1) t = 1;
  return [a[0]+(b[0]-a[0])*t, a[1]+(b[1]-a[1])*t, a[2]+(b[2]-a[2])*t];
}

/* ------------------------------------------------------------- geometry */
/* World is metres on the same local grid as agent-model.html and
   build_carousel.py: x east, y north, z up, origin 40.7020 N 73.9900 W.
   Sharing the grid is the point. A position here and a position there are
   the same number, so the two can disagree visibly instead of quietly. */

var ANCH = D.anchors, PLACES = D.places, GN = D.graph.n, GE = D.graph.e;

var ADJ = [];
for (var _i = 0; _i < GN.length; _i++) ADJ.push([]);
for (var _e = 0; _e < GE.length; _e++) {
  ADJ[GE[_e][0]].push(_e);
  ADJ[GE[_e][1]].push(_e);
}
var ELEN = GE.map(function (ed) {
  var a = GN[ed[0]], b = GN[ed[1]];
  return Math.hypot(b[0]-a[0], b[1]-a[1]) || 0.001;
});

var ROUTE = D.route.p.map(function (n) { return GN[n]; });
var ROUTED = [0];
for (var _r = 1; _r < ROUTE.length; _r++) {
  ROUTED.push(ROUTED[_r-1] + Math.hypot(ROUTE[_r][0]-ROUTE[_r-1][0],
                                        ROUTE[_r][1]-ROUTE[_r-1][1]));
}
var ROUTELEN = ROUTED[ROUTED.length-1] || 1;
function onRoute(s) {
  s = Math.max(0, Math.min(ROUTELEN, s));
  var lo = 0, hi = ROUTED.length - 1;
  while (lo < hi - 1) { var m = (lo+hi) >> 1; if (ROUTED[m] <= s) lo = m; else hi = m; }
  var seg = (ROUTED[hi] - ROUTED[lo]) || 1, t = (s - ROUTED[lo]) / seg;
  var a = ROUTE[lo], b = ROUTE[hi];
  return { x: a[0]+(b[0]-a[0])*t, y: a[1]+(b[1]-a[1])*t,
           h: Math.atan2(b[0]-a[0], b[1]-a[1]) };
}

/* ------------------------------------------------------------- the sound */
/* Inverse-distance weighting in the ENERGY domain over the four measured
   points, exactly as agent-model.html does it. It is an interpolation
   between four numbers. There is no propagation physics in it, and
   agent-model.html records why: a decay model fitted to these four points
   cannot be identified, because jittering the digitised positions by the
   width of their own uncertainty puts the fitted exponent anywhere from
   0.7 to 22.3. Reproduced here so the two artifacts cannot drift apart. */
function dbAt(x, y) {
  var num = 0, den = 0;
  for (var i = 0; i < ANCH.length; i++) {
    var a = ANCH[i];
    if (a.leq === null) continue;
    var d = Math.max(6, Math.hypot(x - a.x, y - a.y));
    var w = 1 / (d * d);
    num += w * Math.pow(10, a.leq / 10);
    den += w;
  }
  return den ? 10 * Math.log10(num / den) : 0;
}

/* -------------------------------------------------------------- controls */
/* The opening view looks north-west along the bridge axis from over the
   Brooklyn side: the span runs away from the camera toward Manhattan, the
   canyon buildings stand to its left, the park and the water beyond. Kept
   as constants so the reset button cannot drift from the boot state. */
var CAM0 = { x: 470, y: -300, z: 260, yaw: -0.827, pitch: -0.32, fov: 0.95 };
var PLAN0 = { cx: -210, cy: 105, scale: 0.82 };

var mode = 'model';
var show = { build: 1, paths: 1, agents: 1, marks: 1, sound: 0 };
var cam = { x: CAM0.x, y: CAM0.y, z: CAM0.z, yaw: CAM0.yaw,
            pitch: CAM0.pitch, fov: CAM0.fov };
var plan = { cx: PLAN0.cx, cy: PLAN0.cy, scale: PLAN0.scale };
var walk = { x: 0, y: 0, yaw: 0, pitch: -0.02, eye: 1.62, s: 0 };
var tour = false;
var pick = null;

/* -------------------------------------------------------- 3D projection */
var PJ = { f: 1, d: 1, cy: 0, sy: 0, cp: 0, sp: 0, ox: 0, oy: 0, oz: 0 };
function setCam(c) {
  PJ.cy = Math.cos(c.yaw); PJ.sy = Math.sin(c.yaw);
  PJ.cp = Math.cos(c.pitch); PJ.sp = Math.sin(c.pitch);
  PJ.f = (H / 2) / Math.tan(c.fov / 2);
  PJ.ox = c.x; PJ.oy = c.y; PJ.oz = c.z;
}
function P3(x, y, z) {
  var dx = x - PJ.ox, dy = y - PJ.oy, dz = z - PJ.oz;
  var ex = dx * PJ.cy - dy * PJ.sy;
  var ey = dx * PJ.sy + dy * PJ.cy;
  var d = ey * PJ.cp + dz * PJ.sp;
  if (d < 0.8) return null;
  PJ.d = d;
  var u = -ey * PJ.sp + dz * PJ.cp;
  return [W/2 + ex * PJ.f / d, H/2 - u * PJ.f / d, d];
}
function P2(x, y) {
  return [W/2 + (x - plan.cx) * plan.scale, H/2 - (y - plan.cy) * plan.scale];
}
function setMode(m) {
  if (m !== 'model' && m !== 'plan' && m !== 'walk') return;
  if (m === 'walk' && mode !== 'walk') {
    /* Enter the walk where the route starts rather than wherever the orbit
       camera happened to be, which is usually 240 m in the air. */
    var p = onRoute(walk.s);
    walk.x = p.x; walk.y = p.y; walk.yaw = p.h; walk.pitch = -0.02;
  }
  mode = m;
  var bs = document.querySelectorAll('[data-mode]');
  for (var i = 0; i < bs.length; i++) {
    bs[i].setAttribute('aria-pressed',
      bs[i].getAttribute('data-mode') === m ? 'true' : 'false');
  }
  var k = document.getElementById('keys');
  if (k) k.hidden = (m !== 'walk');
  if (m !== 'walk' && tour) {
    tour = false;
    var t = document.getElementById('tour');
    if (t) { t.setAttribute('aria-pressed', 'false');
             t.textContent = 'Walk the route'; }
  }
  draw();
}

function activeCam() { return mode === 'walk'
  ? { x: walk.x, y: walk.y, z: walk.eye, yaw: walk.yaw, pitch: walk.pitch, fov: 1.15 }
  : cam; }

var SUN = [Math.sin(2.35), Math.cos(2.35)];
/* Atmospheric haze. The first version was linear and capped at 0.88, which
   at this scene's depth range washed the far half of DUMBO out to sky
   colour: at 1,200 m it was mixing 84 per cent sky into a building that was
   still the subject of the drawing. The curve keeps near geometry saturated
   and puts the haze where distance actually is. */
function fog(col, d, near, far, cap) {
  var t = (d - near) / (far - near);
  if (t < 0) t = 0;
  if (t > 1) t = 1;
  t = t * t * (0.55 + 0.45 * t);
  return mix(col, C['sky-b'], t * (cap === undefined ? 0.62 : cap));
}

/* ------------------------------------------------------------- drawing */

function clear() {
  var gr = ctx.createLinearGradient(0, 0, 0, H);
  gr.addColorStop(0, rgb(C['sky-a']));
  gr.addColorStop(1, rgb(C['sky-b']));
  ctx.fillStyle = gr;
  ctx.fillRect(0, 0, W, H);
}

/* Flat ground features, drawn in fixed layer order at z = 0. They are
   coplanar, so sorting them against each other would be sorting noise. */
function polyPath(pts, proj) {
  var started = false;
  for (var i = 0; i < pts.length; i++) {
    var p = proj(pts[i][0], pts[i][1], 0);
    if (!p) return false;
    if (!started) { ctx.moveTo(p[0], p[1]); started = true; }
    else ctx.lineTo(p[0], p[1]);
  }
  return started;
}

function fillAreas(list, col, proj) {
  ctx.fillStyle = col;
  for (var i = 0; i < list.length; i++) {
    ctx.beginPath();
    if (polyPath(list[i].p, proj)) { ctx.closePath(); ctx.fill(); }
  }
}

/* A way drawn as a ribbon of its own width, so a footpath reads as a path
   and a carriageway reads as a road. The WIDTHS ARE A DRAWING CONVENTION,
   not a survey: OSM gives the centreline, not the kerb. */
/* A way drawn as a ribbon of its own width, so a footpath reads as a path
   and a carriageway reads as a road. The WIDTHS ARE A DRAWING CONVENTION,
   not a survey: OSM gives the centreline, not the kerb.

   scale > 0 is pixels per metre and is used in plan. scale === 0 means work
   it out per way from the projected depth. The first version used one fixed
   reference distance for the whole frame, which is correct at exactly one
   distance and draws a footpath a kilometre away as wide as a motorway. */
function ribbon(list, col, proj, scale, minpx) {
  ctx.strokeStyle = col;
  ctx.lineCap = 'round';
  ctx.lineJoin = 'round';
  for (var i = 0; i < list.length; i++) {
    ctx.beginPath();
    var started = false, w = 0;
    for (var j = 0; j < list[i].p.length; j++) {
      var p = proj(list[i].p[j][0], list[i].p[j][1], 0);
      if (!p) { started = false; continue; }
      if (!started) {
        ctx.moveTo(p[0], p[1]);
        started = true;
        w = (list[i].w || 2.2) * (scale || (PJ.f / Math.max(12, PJ.d)));
      } else ctx.lineTo(p[0], p[1]);
    }
    if (started) {
      ctx.lineWidth = Math.max(minpx, Math.min(w, 90));
      ctx.stroke();
    }
  }
}

/* ----------------------------------------------------------- the model */

var faces = [];

function pushFace(pts, col, depth, edge) {
  faces.push({ p: pts, c: col, d: depth, e: edge });
}

/* One building becomes a roof polygon and its camera-facing walls. Walls
   are culled by the sign of the dot product between the outward normal and
   the view vector, which is exact and costs two multiplies. Rings arrive
   counter-clockwise from the builder, so the outward normal of edge a->b
   is (dy, -dx). */
function addBuilding(b, far) {
  var r = b.r, n = r.length, base = far ? 0 : (b.g || 0), top = base + b.h;
  var cx = 0, cy = 0;
  for (var i = 0; i < n; i++) { cx += r[i][0]; cy += r[i][1]; }
  cx /= n; cy /= n;

  var roof = [];
  for (var i = 0; i < n; i++) {
    var p = P3(r[i][0], r[i][1], top);
    if (!p) return;
    roof.push(p);
  }
  var rd = 0;
  for (var i = 0; i < roof.length; i++) rd += roof[i][2];
  rd /= roof.length;

  if (far) {
    /* Across the river. One flat silhouette: at that range the far bank is
       a skyline, and shading each of its walls would be inventing detail a
       viewer cannot resolve and the data does not carry. */
    var sil = [];
    for (var i = 0; i < n; i++) {
      var pb = P3(r[i][0], r[i][1], 0), pt = P3(r[i][0], r[i][1], top);
      if (!pb || !pt) return;
      sil.push(pt);
    }
    for (var i = n - 1; i >= 0; i--) {
      var pb2 = P3(r[i][0], r[i][1], 0);
      if (!pb2) return;
      sil.push(pb2);
    }
    pushFace(sil, rgb(mix(C['far'], C['sky-b'],
      0.16 + 0.30 * Math.min(1, Math.max(0, (rd - 800) / 2400)))),
      rd, null);
    return;
  }

  for (var i = 0; i < n; i++) {
    var a = r[i], c = r[(i + 1) % n];
    var dx = c[0] - a[0], dy = c[1] - a[1];
    var L = Math.hypot(dx, dy) || 1;
    var nx = dy / L, ny = -dx / L;
    var mx = (a[0] + c[0]) / 2, my = (a[1] + c[1]) / 2;
    if (nx * (mx - PJ.ox) + ny * (my - PJ.oy) >= 0) continue;
    var q0 = P3(a[0], a[1], base), q1 = P3(c[0], c[1], base);
    var q2 = P3(c[0], c[1], top), q3 = P3(a[0], a[1], top);
    if (!q0 || !q1 || !q2 || !q3) continue;
    var lit = nx * SUN[0] + ny * SUN[1];
    var col = lit > 0.35 ? C['wallA'] : (lit > -0.35 ? C['wallB'] : C['wallC']);
    var d = (q0[2] + q1[2] + q2[2] + q3[2]) / 4;
    pushFace([q0, q1, q2, q3], rgb(fog(col, d, 250, 2200, 0.55)), d, 1);
  }
  pushFace(roof, rgb(fog(C['roof'], rd, 250, 2200, 0.55)), rd + 0.4, 1);
}

/* The bridge. The CENTRELINE is mapped; the DECK ELEVATION IS NOT. No
   public source gives it over DUMBO. It is drawn in the inferred colour
   with a hatched soffit so it can never be mistaken for the surveyed
   geometry beside it, which is exactly the convention model-3d.html uses. */
function addSpan() {
  var s = D.span, hh = D.deck.h, hw = D.deck.w / 2;
  var col = C['infer'];
  for (var i = 0; i < s.length - 1; i++) {
    var a = s[i], b = s[i+1];
    var dx = b[0]-a[0], dy = b[1]-a[1], L = Math.hypot(dx, dy) || 1;
    var nx = dy / L * hw, ny = -dx / L * hw;
    var q = [P3(a[0]+nx, a[1]+ny, hh), P3(b[0]+nx, b[1]+ny, hh),
             P3(b[0]-nx, b[1]-ny, hh), P3(a[0]-nx, a[1]-ny, hh)];
    if (q[0] && q[1] && q[2] && q[3]) {
      var d = (q[0][2]+q[1][2]+q[2][2]+q[3][2]) / 4;
      pushFace(q, rgb(fog(col, d, 300, 2600, 0.45)), d, 2);
    }
    var side = [P3(a[0]+nx, a[1]+ny, hh), P3(b[0]+nx, b[1]+ny, hh),
                P3(b[0]+nx, b[1]+ny, hh-4.5), P3(a[0]+nx, a[1]+ny, hh-4.5)];
    if (side[0] && side[1] && side[2] && side[3]) {
      var d2 = (side[0][2]+side[1][2]+side[2][2]+side[3][2]) / 4;
      pushFace(side, rgb(fog(mix(col, [0,0,0], 0.30), d2, 300, 2600, 0.45)), d2, 2);
    }
    var side2 = [P3(a[0]-nx, a[1]-ny, hh), P3(b[0]-nx, b[1]-ny, hh),
                 P3(b[0]-nx, b[1]-ny, hh-4.5), P3(a[0]-nx, a[1]-ny, hh-4.5)];
    if (side2[0] && side2[1] && side2[2] && side2[3]) {
      var d3 = (side2[0][2]+side2[1][2]+side2[2][2]+side2[3][2]) / 4;
      pushFace(side2, rgb(fog(mix(col, [0,0,0], 0.44), d3, 300, 2600, 0.45)), d3, 2);
    }
  }
}

/* A walking figure: one vertical quad, camera-facing by construction
   because it is built from the screen-space up axis. */
function addAgent(a) {
  var base = P3(a.x, a.y, 0), head = P3(a.x, a.y, 1.72);
  if (!base || !head) return;
  var hpx = base[1] - head[1];
  if (hpx < 1.2) return;
  var col = rgb(fog(C['agent'], base[2], 160, 900));
  if (hpx < 9) {
    var w0 = Math.max(1.1, hpx * 0.30);
    pushFace([[base[0]-w0/2, base[1]], [base[0]+w0/2, base[1]],
              [head[0]+w0/2, head[1]], [head[0]-w0/2, head[1]]],
             col, base[2] - 0.5, 3);
    return;
  }
  /* Close enough to read as a person rather than a domino. Shoulders at 0.82
     of standing height, head above; proportions are ILLUSTRATIVE and carry no
     claim, which is why nothing on this page measures a person. */
  var x = base[0], y0 = base[1];
  var sh = hpx * 0.30, hd = hpx * 0.12, lg = hpx * 0.17;
  var yS = y0 - hpx * 0.72, yN = y0 - hpx * 0.82, yH = y0 - hpx;
  pushFace([[x-lg, y0], [x+lg, y0], [x+sh, yS], [x+hd*0.7, yN],
            [x+hd, yN], [x+hd, yH], [x-hd, yH], [x-hd, yN],
            [x-hd*0.7, yN], [x-sh, yS]],
           col, base[2] - 0.5, 3);
}

/* --------------------------------------------------------- the 3D frame */

function drawModel() {
  var c = activeCam();
  setCam(c);
  LABELS = [];
  clear();

  /* Ground plane. Built as a trapezoid in FRONT of the camera rather than a
     square centred on it: a square straddles the near plane, P3 rejects the
     corners behind the camera, and what is left is a three-sided fragment
     that paints the wrong part of the frame. At eye height that fragment is
     most of the picture. */
  var far = 2600;
  var fx = Math.sin(c.yaw), fy = Math.cos(c.yaw);
  var rx = fy, ry = -fx;
  /* Half-width has to GROW with depth. A constant half-width is a rectangle
     whose far corners sit outside the frustum at a bearing the projection
     wraps above the horizon, which paints the sky brown. */
  var spread = (W / 2) / PJ.f * 1.25;
  var wn = 40, wf = far * spread;
  var corners = [
    [fx * 2 - rx * wn, fy * 2 - ry * wn],
    [fx * 2 + rx * wn, fy * 2 + ry * wn],
    [fx * far + rx * wf, fy * far + ry * wf],
    [fx * far - rx * wf, fy * far - ry * wf]
  ];
  ctx.fillStyle = rgb(mix(C['ground'], C['sky-b'], 0.16));
  ctx.beginPath();
  var ok = false, started = false;
  for (var i = 0; i < 4; i++) {
    var p = P3(c.x + corners[i][0], c.y + corners[i][1], 0);
    if (!p) { continue; }
    if (!started) { ctx.moveTo(p[0], p[1]); started = true; } else ctx.lineTo(p[0], p[1]);
    ok = true;
  }
  if (ok) { ctx.closePath(); ctx.fill(); }

  var pr = function (x, y, z) { return P3(x, y, z || 0); };
  fillAreas(D.band, rgb(C['water']), pr);
  fillAreas(D.water, rgb(C['water']), pr);
  fillAreas(D.park, rgb(C['park']), pr);

  /* scale 0 means "work the ribbon width out from the projected depth",
     which is the only way a footpath reads correctly at both 60 m and
     1,200 m in the same frame. */
  if (show.paths) {
    ribbon(D.road, rgb(C['road']), pr, 0, 1);
    ribbon(D.pier, rgb(C['foot']), pr, 0, 1);
    ribbon(D.foot, rgb(C['foot']), pr, 0, 1);
    ribbon(D.steps, rgb(C['foot']), pr, 0, 1);
  }

  /* The routed walk, laid on the ground rather than left to the plan view.
     It is the one line on this page that is an ANSWER rather than an input,
     and at eye height it is also the only thing giving the near ground a
     reason to be looked at. Emitted one segment per item so each takes its
     width from its OWN depth; a single item would size 1.5 km of route from
     the depth of its first vertex. */
  var rseg = [];
  for (var i = 1; i < ROUTE.length; i++) {
    rseg.push({ p: [ROUTE[i - 1], ROUTE[i]], w: 1.5 });
  }
  ctx.setLineDash([9, 6]);
  ribbon(rseg, rgb(C['meas']), function (x, y) { return P3(x, y, 0.08); }, 0, 2.0);
  ctx.setLineDash([]);

  faces = [];
  if (show.build) {
    var vx = Math.sin(c.yaw), vy = Math.cos(c.yaw);
    var N = D.near, cull = (mode === 'walk') ? 620 : 2400;
    for (var i = 0; i < N.length; i++) {
      var b = N[i], r0 = b.r[0];
      var dx = r0[0] - c.x, dy = r0[1] - c.y;
      var dist = Math.hypot(dx, dy);
      if (dist > cull) continue;
      /* Keep anything within the frustum plus a building's own diagonal. */
      if (dist > 40 && (dx * vx + dy * vy) < -60) continue;
      addBuilding(b, false);
    }
    var F = D.far;
    for (var i = 0; i < F.length; i++) {
      var fb = F[i], f0 = fb.r[0];
      if ((f0[0] - c.x) * vx + (f0[1] - c.y) * vy < -200) continue;
      addBuilding(fb, true);
    }
  }
  if (show.marks) addSpan();
  if (show.agents) for (var i = 0; i < AGENTS.length; i++) addAgent(AGENTS[i]);

  faces.sort(function (a, b) { return b.d - a.d; });
  var edgeCol = rgb(C['edge']);
  for (var i = 0; i < faces.length; i++) {
    var f = faces[i];
    ctx.fillStyle = f.c;
    ctx.beginPath();
    ctx.moveTo(f.p[0][0], f.p[0][1]);
    for (var j = 1; j < f.p.length; j++) ctx.lineTo(f.p[j][0], f.p[j][1]);
    ctx.closePath();
    ctx.fill();
    /* Outline near building faces. Two flat walls that happen to face the
       same way merge into one mass without this, and the whole argument of
       the page is that these are SEPARATE surveyed volumes. Faded with
       distance so the far bank does not turn into a wire drawing. */
    if (f.e === 1 && f.d < 700) {
      var bb0 = bbox(f.p);
      if (bb0[2] - bb0[0] > 7 && bb0[3] - bb0[1] > 7) {
        ctx.globalAlpha = 0.30 * (1 - f.d / 700);
        ctx.strokeStyle = edgeCol;
        ctx.lineWidth = 1;
        ctx.stroke();
        ctx.globalAlpha = 1;
      }
    }
    if (f.e === 2) {
      /* The inferred deck carries a hatch. A reader who takes one thing
         from this page should take that this band is not measured. */
      ctx.save();
      ctx.clip();
      ctx.strokeStyle = 'rgba(0,0,0,0.20)';
      ctx.lineWidth = 1;
      var bb = bbox(f.p);
      ctx.beginPath();
      for (var hx = bb[0] - (bb[3] - bb[1]); hx < bb[2]; hx += 7) {
        ctx.moveTo(hx, bb[1]); ctx.lineTo(hx + (bb[3] - bb[1]), bb[3]);
      }
      ctx.stroke();
      ctx.restore();
    }
  }

  if (show.marks) drawMarkers3D();
  drawScale();
}

function bbox(p) {
  var x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
  for (var i = 0; i < p.length; i++) {
    if (p[i][0] < x0) x0 = p[i][0]; if (p[i][0] > x1) x1 = p[i][0];
    if (p[i][1] < y0) y0 = p[i][1]; if (p[i][1] > y1) y1 = p[i][1];
  }
  return [x0, y0, x1, y1];
}

function drawMarkers3D() {
  ctx.textAlign = 'center';
  ctx.textBaseline = 'bottom';
  ctx.font = '600 12px ui-monospace,Menlo,Consolas,monospace';
  /* Nearest first, so that when two chips collide the one that survives is
     the one the viewer is closest to and most likely asking about. */
  var ord = ANCH.slice().sort(function (a, b) {
    return Math.hypot(a.x - PJ.ox, a.y - PJ.oy) - Math.hypot(b.x - PJ.ox, b.y - PJ.oy);
  });
  for (var i = 0; i < ord.length; i++) {
    var a = ord[i];
    var b = P3(a.x, a.y, 0), t = P3(a.x, a.y, 13);
    if (!b || !t) continue;
    ctx.strokeStyle = rgb(C['meas']);
    ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(b[0], b[1]); ctx.lineTo(t[0], t[1]); ctx.stroke();
    ctx.fillStyle = rgb(C['meas']);
    ctx.beginPath(); ctx.arc(t[0], t[1], 4.5, 0, 6.284); ctx.fill();
    var lab = a.leq === null ? (a.peak.toFixed(1) + ' pk') : (a.leq.toFixed(2));
    chip(t[0], t[1] - 9, lab, rgb(C['meas']));
  }
}

/* Label placement. A chip is nudged vertically until it clears every chip
   already placed; if nothing clears, it is DROPPED rather than drawn on top,
   because two overlapping numbers are worse than one number and this page
   exists to be read off. Nearest wins, since the nearest label is the one the
   viewer is most likely to be asking about. A nudged chip keeps a leader back
   to its own marker so the association is never guessed. */
var LABELS = [];
var NUDGE = [0, -19, 20, -38, 39, -57, 58];
function chip(x, y, txt, col) {
  var w = ctx.measureText(txt).width + 12;
  for (var k = 0; k < NUDGE.length; k++) {
    var yy = y + NUDGE[k];
    var r = [x - w/2, yy - 16, x + w/2, yy + 1];
    var hit = false;
    for (var i = 0; i < LABELS.length; i++) {
      var o = LABELS[i];
      if (r[0] < o[2] + 3 && r[2] > o[0] - 3 && r[1] < o[3] + 3 && r[3] > o[1] - 3) {
        hit = true; break;
      }
    }
    if (hit) continue;
    LABELS.push(r);
    if (NUDGE[k] !== 0) {
      ctx.strokeStyle = col;
      ctx.lineWidth = 0.9;
      ctx.globalAlpha = 0.55;
      ctx.beginPath();
      ctx.moveTo(x, y - 7);
      ctx.lineTo(x, NUDGE[k] < 0 ? yy + 1 : yy - 16);
      ctx.stroke();
      ctx.globalAlpha = 1;
    }
    ctx.fillStyle = C.card;
    ctx.strokeStyle = col;
    ctx.lineWidth = 1;
    roundRect(r[0], r[1], w, 17, 5);
    ctx.fill(); ctx.stroke();
    ctx.fillStyle = col;
    ctx.fillText(txt, x, yy - 3);
    return true;
  }
  return false;
}

function roundRect(x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.arcTo(x + w, y, x + w, y + h, r);
  ctx.arcTo(x + w, y + h, x, y + h, r);
  ctx.arcTo(x, y + h, x, y, r);
  ctx.arcTo(x, y, x + w, y, r);
  ctx.closePath();
}

/* ------------------------------------------------------------ plan view */

function drawPlan() {
  LABELS = [];
  ctx.fillStyle = rgb(C['ground']);
  ctx.fillRect(0, 0, W, H);
  var pr = function (x, y) { return P2(x, y); };
  fillAreas(D.band, rgb(C['water']), pr);
  fillAreas(D.water, rgb(C['water']), pr);
  fillAreas(D.park, rgb(C['park']), pr);

  if (show.sound) drawSound();

  if (show.paths) {
    ribbon(D.road, rgb(C['road']), pr, plan.scale, 1);
    ribbon(D.pier, rgb(C['foot']), pr, plan.scale, 1);
    ribbon(D.foot, rgb(C['foot']), pr, plan.scale, 0.8);
    ribbon(D.steps, rgb(C['foot']), pr, plan.scale, 0.8);
  }

  if (show.build) {
    ctx.fillStyle = rgb(C['wallB']);
    ctx.strokeStyle = rgb(C['edge']);
    ctx.lineWidth = 0.5;
    var all = D.near;
    for (var i = 0; i < all.length; i++) {
      ctx.beginPath();
      if (polyPath(all[i].r, pr)) { ctx.closePath(); ctx.fill(); }
    }
  }

  /* The span, in the inferred colour and dashed, because in plan its
     position is mapped but everything about its section is not. */
  if (show.marks) {
    ctx.strokeStyle = rgb(C['infer']);
    ctx.lineWidth = Math.max(3, D.deck.w * plan.scale);
    ctx.globalAlpha = 0.55;
    ctx.beginPath();
    for (var i = 0; i < D.span.length; i++) {
      var p = P2(D.span[i][0], D.span[i][1]);
      if (i === 0) ctx.moveTo(p[0], p[1]); else ctx.lineTo(p[0], p[1]);
    }
    ctx.stroke();
    ctx.globalAlpha = 1;
  }

  /* The routed walk. */
  ctx.strokeStyle = rgb(C['meas']);
  ctx.lineWidth = 2.4;
  ctx.setLineDash([7, 4]);
  ctx.beginPath();
  for (var i = 0; i < ROUTE.length; i++) {
    var p = P2(ROUTE[i][0], ROUTE[i][1]);
    if (i === 0) ctx.moveTo(p[0], p[1]); else ctx.lineTo(p[0], p[1]);
  }
  ctx.stroke();
  ctx.setLineDash([]);

  if (show.agents) {
    ctx.fillStyle = rgb(C['agent']);
    for (var i = 0; i < AGENTS.length; i++) {
      var p = P2(AGENTS[i].x, AGENTS[i].y);
      ctx.beginPath(); ctx.arc(p[0], p[1], 1.9, 0, 6.284); ctx.fill();
    }
  }

  if (show.marks) {
    ctx.font = '600 11.5px ui-monospace,Menlo,Consolas,monospace';
    ctx.textAlign = 'center'; ctx.textBaseline = 'bottom';
    for (var i = 0; i < ANCH.length; i++) {
      var a = ANCH[i], p = P2(a.x, a.y);
      ctx.fillStyle = rgb(C['meas']);
      ctx.beginPath(); ctx.arc(p[0], p[1], 5, 0, 6.284); ctx.fill();
      chip(p[0], p[1] - 7, a.name, rgb(C['meas']));
    }
    /* Places the model inherited. Filled where they are impossible. */
    for (var i = 0; i < PLACES.length; i++) {
      var q = PLACES[i], p2 = P2(q.x, q.y);
      ctx.beginPath(); ctx.arc(p2[0], p2[1], 3.4, 0, 6.284);
      if (q.impossible) { ctx.fillStyle = rgb(C['infer']); ctx.fill(); }
      else { ctx.strokeStyle = rgb(C['edge']); ctx.lineWidth = 1.4; ctx.stroke(); }
    }
  }

  /* Walk position. */
  if (walk.s > 0 || tour) {
    var wp = onRoute(walk.s), p3 = P2(wp.x, wp.y);
    ctx.fillStyle = rgb(C['agent']);
    ctx.beginPath(); ctx.arc(p3[0], p3[1], 6, 0, 6.284); ctx.fill();
    ctx.strokeStyle = C.card; ctx.lineWidth = 2; ctx.stroke();
  }
  drawScale();
}

/* A coarse energy-domain interpolation, rendered as a coverage wash. It is
   NOT a propagation model and the legend says so on the page. */
function drawSound() {
  var step = 14;
  for (var px = 0; px < W; px += step) {
    for (var py = 0; py < H; py += step) {
      var wx = plan.cx + (px + step/2 - W/2) / plan.scale;
      var wy = plan.cy - (py + step/2 - H/2) / plan.scale;
      var v = dbAt(wx, wy);
      var t = (v - 60) / 30;
      if (t <= 0) continue;
      ctx.fillStyle = 'rgba(160,50,30,' + (Math.min(1, t) * 0.30).toFixed(3) + ')';
      ctx.fillRect(px, py, step, step);
    }
  }
}

function drawScale() {
  var target = 120, m, px;
  if (mode === 'plan') {
    var opts = [10, 20, 50, 100, 200, 500, 1000];
    m = opts[0];
    for (var i = 0; i < opts.length; i++) {
      if (opts[i] * plan.scale <= target) m = opts[i];
    }
    px = m * plan.scale;
  } else {
    var d = 120;
    var perM = PJ.f / d;
    var opts2 = [5, 10, 20, 50, 100, 200];
    m = opts2[0];
    for (var i = 0; i < opts2.length; i++) if (opts2[i] * perM <= target) m = opts2[i];
    px = m * perM;
  }
  var x = 16, y = H - 20;
  ctx.strokeStyle = C.ink; ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(x, y - 5); ctx.lineTo(x, y); ctx.lineTo(x + px, y); ctx.lineTo(x + px, y - 5);
  ctx.stroke();
  ctx.fillStyle = C.ink;
  ctx.font = '11px ui-monospace,Menlo,Consolas,monospace';
  ctx.textAlign = 'left'; ctx.textBaseline = 'bottom';
  ctx.fillText(m + ' m' + (mode === 'plan' ? '' : ' at 120 m'), x, y - 7);
}

/* --------------------------------------------------------------- agents */
/* WHAT THESE FIGURES ARE AND ARE NOT.
   They are a demonstration that the walk network is connected and where it
   goes. They are NOT a population model. Their number is a slider, their
   speed is one constant, and nothing about them is observed: no count of
   pedestrians in this corridor has ever been made, which is Method 27 and
   still the largest hole in this programme. agent-model.html carries the
   population model, with its cohorts, its dwell distributions and its own
   long list of what is invented in it. This page deliberately does not
   duplicate that, because two population models that disagree by accident
   are worse than one that states its assumptions. */

var AGENTS = [];
var NAGENTS = 90;
var rngState = 20260101;
function rnd() {
  rngState ^= rngState << 13; rngState ^= rngState >>> 17; rngState ^= rngState << 5;
  return ((rngState >>> 0) % 100000) / 100000;
}

function spawn() {
  AGENTS = [];
  rngState = 20260101;
  if (!GE.length) return;
  for (var i = 0; i < NAGENTS; i++) {
    var e = (rnd() * GE.length) | 0;
    AGENTS.push({ e: e, t: rnd(), dir: rnd() < 0.5 ? 1 : -1,
                  v: 1.15 + rnd() * 0.45, x: 0, y: 0 });
    place(AGENTS[i]);
  }
}
function place(a) {
  var ed = GE[a.e], p = GN[ed[0]], q = GN[ed[1]];
  var t = a.dir > 0 ? a.t : 1 - a.t;
  a.x = p[0] + (q[0] - p[0]) * t;
  a.y = p[1] + (q[1] - p[1]) * t;
}
function stepAgents(dt) {
  for (var i = 0; i < AGENTS.length; i++) {
    var a = AGENTS[i];
    a.t += (a.v * dt) / ELEN[a.e];
    if (a.t >= 1) {
      var ed = GE[a.e];
      var node = a.dir > 0 ? ed[1] : ed[0];
      var opts = ADJ[node];
      if (!opts.length) { a.dir = -a.dir; a.t = 0; continue; }
      var next = opts[(rnd() * opts.length) | 0];
      if (opts.length > 1) {
        var guard = 0;
        while (next === a.e && guard++ < 6) next = opts[(rnd() * opts.length) | 0];
      }
      a.e = next;
      a.dir = (GE[next][0] === node) ? 1 : -1;
      a.t = 0;
    }
    place(a);
  }
}

/* ---------------------------------------------------------- interaction */

var drag = null;
function pos(ev) {
  var r = cv.getBoundingClientRect();
  return [(ev.clientX - r.left), (ev.clientY - r.top)];
}
cv.addEventListener('pointerdown', function (ev) {
  cv.setPointerCapture(ev.pointerId);
  cv.classList.add('drag');
  drag = { p: pos(ev), cam: { x: cam.x, y: cam.y, yaw: cam.yaw, pitch: cam.pitch },
           plan: { cx: plan.cx, cy: plan.cy },
           walk: { yaw: walk.yaw, pitch: walk.pitch } };
});
cv.addEventListener('pointermove', function (ev) {
  if (!drag) return;
  var p = pos(ev), dx = p[0] - drag.p[0], dy = p[1] - drag.p[1];
  if (mode === 'plan') {
    plan.cx = drag.plan.cx - dx / plan.scale;
    plan.cy = drag.plan.cy + dy / plan.scale;
  } else if (mode === 'walk') {
    walk.yaw = drag.walk.yaw + dx * 0.005;
    walk.pitch = clamp(drag.walk.pitch - dy * 0.004, -1.15, 0.9);
  } else {
    cam.yaw = drag.cam.yaw + dx * 0.005;
    cam.pitch = clamp(drag.cam.pitch - dy * 0.004, -1.45, -0.03);
  }
  draw();
});
function endDrag(ev) {
  if (!drag) return;
  drag = null;
  cv.classList.remove('drag');
  try { cv.releasePointerCapture(ev.pointerId); } catch (e) {}
}
cv.addEventListener('pointerup', endDrag);
cv.addEventListener('pointercancel', endDrag);
cv.addEventListener('wheel', function (ev) {
  ev.preventDefault();
  var k = Math.exp(-ev.deltaY * 0.0015);
  if (mode === 'plan') plan.scale = clamp(plan.scale * k, 0.08, 6);
  else if (mode === 'model') cam.z = clamp(cam.z / k, 18, 900);
  draw();
}, { passive: false });

function clamp(v, a, b) { return v < a ? a : (v > b ? b : v); }

var keys = {};
window.addEventListener('keydown', function (e) {
  if (e.target && /^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName)) return;
  var k = e.key.toLowerCase();
  if ('wasdqe'.indexOf(k) >= 0 || k.indexOf('arrow') === 0) {
    keys[k] = 1;
    if (mode === 'walk') e.preventDefault();
  }
});
window.addEventListener('keyup', function (e) { keys[e.key.toLowerCase()] = 0; });

function stepWalk(dt) {
  var f = 0, s = 0;
  if (keys['w'] || keys['arrowup']) f += 1;
  if (keys['s'] || keys['arrowdown']) f -= 1;
  if (keys['a'] || keys['arrowleft']) s -= 1;
  if (keys['d'] || keys['arrowright']) s += 1;
  if (keys['q']) walk.yaw -= 1.4 * dt;
  if (keys['e']) walk.yaw += 1.4 * dt;
  if (!f && !s) return false;
  var v = 1.5 * dt * 3.0;
  var fx = Math.sin(walk.yaw), fy = Math.cos(walk.yaw);
  walk.x += (fx * f + fy * s) * v;
  walk.y += (fy * f - fx * s) * v;
  return true;
}

/* --------------------------------------------------------------- frame */

var last = 0, running = true;
function frame(ts) {
  var dt = last ? Math.min(0.1, (ts - last) / 1000) : 0.016;
  last = ts;
  var moved = false;
  if (show.agents) { stepAgents(dt); moved = true; }
  if (mode === 'walk') { if (stepWalk(dt)) moved = true; }
  if (tour) {
    walk.s += 1.35 * dt;
    if (walk.s > ROUTELEN) walk.s = 0;
    var p = onRoute(walk.s);
    walk.x = p.x; walk.y = p.y;
    walk.yaw += (angDiff(p.h, walk.yaw)) * Math.min(1, dt * 2.2);
    moved = true;
  }
  if (moved) draw(); else hud();
  if (running) requestAnimationFrame(frame);
}
function angDiff(a, b) {
  var d = (a - b) % 6.283185;
  if (d > 3.14159) d -= 6.283185;
  if (d < -3.14159) d += 6.283185;
  return d;
}

function draw() {
  if (!W) return;
  if (mode === 'plan') drawPlan(); else drawModel();
  hud();
}

function hud() {
  var c = activeCam();
  var x = mode === 'plan' ? plan.cx : c.x, y = mode === 'plan' ? plan.cy : c.y;
  var db = dbAt(x, y);
  var lat = D.grid.lat0 + y / D.grid.my;
  var lon = D.grid.lon0 + x / D.grid.mx;
  document.getElementById('h1').textContent =
    lat.toFixed(5) + ' N  ' + Math.abs(lon).toFixed(5) + ' W';
  document.getElementById('h2').textContent =
    'interpolated ' + db.toFixed(1) + ' dB(A) Leq';
  document.getElementById('h3').textContent =
    mode === 'walk'
      ? ('chainage ' + walk.s.toFixed(0) + ' m of ' + ROUTELEN.toFixed(0))
      : (D.near.length + ' surveyed footprints');
}

/* ---------------------------------------------------------------- boot */

function resize() {
  DPR = Math.min(2, window.devicePixelRatio || 1);
  var r = cv.getBoundingClientRect();
  W = Math.max(200, Math.round(r.width));
  H = Math.max(160, Math.round(r.height));
  cv.width = Math.round(W * DPR);
  cv.height = Math.round(H * DPR);
  ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
  draw();
}

document.querySelectorAll('[data-mode]').forEach(function (b) {
  b.addEventListener('click', function () { setMode(b.dataset.mode); });
});
document.querySelectorAll('[data-toggle]').forEach(function (b) {
  b.addEventListener('click', function () {
    var k = b.dataset.toggle;
    show[k] = show[k] ? 0 : 1;
    b.setAttribute('aria-pressed', show[k] ? 'true' : 'false');
    draw();
  });
});
document.getElementById('tour').addEventListener('click', function () {
  tour = !tour;
  this.setAttribute('aria-pressed', tour ? 'true' : 'false');
  this.textContent = tour ? 'Stop the walk' : 'Walk the route';
  if (tour && mode !== 'walk') setMode('walk');
});
document.getElementById('reset').addEventListener('click', function () {
  cam = { x: CAM0.x, y: CAM0.y, z: CAM0.z, yaw: CAM0.yaw,
          pitch: CAM0.pitch, fov: CAM0.fov };
  plan = { cx: PLAN0.cx, cy: PLAN0.cy, scale: PLAN0.scale };
  walk.s = 0; tour = false;
  var t = document.getElementById('tour');
  t.setAttribute('aria-pressed', 'false');
  t.textContent = 'Walk the route';
  draw();
});

new MutationObserver(function () { readTheme(); draw(); })
  .observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
window.addEventListener('resize', resize);

readTheme();
spawn();
setMode('model');
resize();
requestAnimationFrame(frame);

/* Exposed only so the committed verification harness can assert against the
   same numbers the page draws, rather than re-deriving them and agreeing
   with itself. */
window.__WMAPI__ = {
  faces: function () { return faces.length; },
  agents: function () { return AGENTS.length; },
  mode: function () { return mode; },
  setMode: setMode,
  routeLen: function () { return ROUTELEN; },
  dbAt: dbAt,
  counts: function () {
    return { near: D.near.length, far: D.far.length, road: D.road.length,
             foot: D.foot.length, nodes: GN.length, edges: GE.length };
  }
};
})();
</script>
</body>
</html>
"""

JS = r"""@@JSBLOB@@"""


def stat(v, label):
    return '<div class="stat"><b>%s</b><span>%s</span></div>' % (v, label)


def emit(P):
    import datetime
    pl = P["places"]
    an = P["anchors"]
    imposs = [r for r in pl if r["impossible"]]
    indoor_ok = [r for r in pl if r["inside"] and r["indoor"]]
    anin = [r for r in an if r["inside"]]
    snaps = P["route"]["snaps"]
    worst = max(snaps, key=lambda s: s["off"])

    rows = []
    for r in pl:
        if r["impossible"]:
            v = ('<span class="bad">inside bin %s, %.0f m tall</span>'
                 % (esc(str(r["bin"])), r["bh"]))
        elif r["inside"]:
            v = '<span class="ok">inside a footprint, and marked indoors</span>'
        else:
            v = "%.1f m to the nearest wall" % r["facade"]
        net = (('<span class="warn">%.1f</span>' % r["net"]) if r["net"] > 25
               else ("%.1f" % r["net"]))
        rows.append("<tr><td>%s</td><td>%s</td><td>%s</td>"
                    "<td class=\"num\">%s</td></tr>"
                    % (esc(r["name"]),
                       "indoor" if r["indoor"] else "outdoor", v, net))
    place_rows = "\n".join(rows)

    arows = []
    for r in an:
        lv = ("%.2f" % r["leq"]) if r["leq"] is not None else "not published"
        arows.append("<tr><td>%s</td><td class=\"num\">%s</td>"
                     "<td class=\"num\">%.2f</td><td>%s</td>"
                     "<td class=\"num\">%.1f</td></tr>"
                     % (esc(r["name"]), lv, r["peak"],
                        ('<span class="bad">inside a building footprint</span>'
                         if r["inside"]
                         else "%.1f m to the nearest wall" % r["facade"]),
                        r["net"]))
    anchor_rows = "\n".join(arows)

    srows = "\n".join("<tr><td>%s</td><td class=\"num\">%.1f</td></tr>"
                      % (esc(s["n"]), s["off"]) for s in snaps)
    mrows = "\n".join("<tr><td>%s</td><td class=\"num\">%.0f</td></tr>"
                      % (esc(m["n"]), m["s"]) for m in P["route"]["marks"])

    stats = "".join([
        stat("{:,}".format(len(P["near"])),
             "surveyed footprints, walkable extent"),
        stat("{:,}".format(len(P["far"])),
             "across the river, drawn as skyline"),
        stat("{:,}".format(len(P["graph"]["n"])),
             "connected nodes of walkable network"),
        stat("%.0f&#8201;m" % P["route"]["len"],
             "York Street to Pier 1, routed"),
    ])

    html = TEMPLATE
    subs = [
        ("__STATS__", stats),
        ("__PLACEROWS__", place_rows),
        ("__ANCHORROWS__", anchor_rows),
        ("__SNAPROWS__", srows),
        ("__MARKROWS__", mrows),
        ("__NNEAR__", "{:,}".format(len(P["near"]))),
        ("__NFAR__", "{:,}".format(len(P["far"]))),
        ("__NROAD__", "{:,}".format(len(P["road"]))),
        ("__NFOOT__", "{:,}".format(len(P["foot"]) + len(P["steps"]))),
        ("__NNODES__", "{:,}".format(len(P["graph"]["n"]))),
        ("__NEDGES__", "{:,}".format(len(P["graph"]["e"]))),
        ("__ROUTELEN__", "%.0f" % P["route"]["len"]),
        ("__NIMPOSS__", str(len(imposs))),
        ("__NPLACES__", str(len(pl))),
        ("__IMPOSSLIST__", ", ".join(esc(r["name"]) for r in imposs) or "none"),
        ("__NINDOOROK__", str(len(indoor_ok))),
        ("__NANIN__", str(len(anin))),
        ("__ANINLIST__", ", ".join(esc(r["name"]) for r in anin) or "none"),
        ("__WORSTSNAP__", "%.1f" % worst["off"]),
        ("__WORSTSNAPN__", esc(worst["n"])),
        ("__DECKH__", "%.0f" % DECK_H),
        ("__BUILT__", datetime.date.today().isoformat()),
        ("__CSS__", CSS),
        ("@@JSBLOB@@", JS),
    ]
    for k, v in subs:
        html = html.replace(k, v)
    html = html.replace("/*PAYLOAD*/", json.dumps(P, separators=(",", ":")))

    left = [w for w in html.split() if w.startswith("__") and w != "__WM__"]
    if left or "@@" in html:
        raise SystemExit("unsubstituted token(s): %s" % (left[:5] or "@@"))
    return html


def main():
    P = payload()
    if "--stats" in sys.argv:
        print("near %d  far %d  road %d  foot %d  steps %d"
              % (len(P["near"]), len(P["far"]), len(P["road"]),
                 len(P["foot"]), len(P["steps"])))
        print("graph %d nodes  %d edges"
              % (len(P["graph"]["n"]), len(P["graph"]["e"])))
        print("route %.1f m" % P["route"]["len"])
        for r in P["places"]:
            if r["impossible"]:
                print("  IMPOSSIBLE: %s inside bin %s (%.0f m)"
                      % (r["name"], r["bin"], r["bh"]))
        return
    html = emit(P)
    with open(OUTPAGE, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html)
    print("wrote %s  %d bytes" % (OUTPAGE, os.path.getsize(OUTPAGE)))
    print("  near %d | far %d | nodes %d | route %.0f m"
          % (len(P["near"]), len(P["far"]), len(P["graph"]["n"]),
             P["route"]["len"]))
    bad = [r for r in P["places"] if r["impossible"]]
    print("  outdoor places inside a surveyed footprint: %d" % len(bad))
    for r in bad:
        print("    %s -> bin %s, %.0f m tall" % (r["name"], r["bin"], r["bh"]))


if __name__ == "__main__":
    main()
