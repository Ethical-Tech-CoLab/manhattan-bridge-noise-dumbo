"""Fetch the open geodata the carousel slides are drawn from.

Nothing here is traced off a proprietary basemap. Google Maps imagery is not
used: its terms forbid the derivative work, and an image nobody else can
re-derive is not a citable source, which is the whole discipline of this
repository.

Sources
  NYC OpenData 5zhs-2jue   BUILDING (footprint, height_roof, ground_elevation)
  OpenStreetMap / Overpass streets, footways, park, water, station entrances
                           (c) OpenStreetMap contributors, ODbL 1.0
"""
import json
import os
import subprocess
import sys
import time

UA = "manhattan-bridge-noise-dumbo-research/1.0"
OUT = os.path.join("data-collection", "geo")

# The corridor: the East River shoreline, DUMBO, Vinegar Hill, and the
# Manhattan Bridge Brooklyn approach as far inland as the viaduct runs.
#
# TWO EXTENTS, DELIBERATELY, because they answer different questions.
#
# STUDY is the ground a pedestrian actually covers, and everything walkable,
# routable or measured is fetched over it. Its west edge was -73.9975 until
# the walkable map was built, which is 0.0055 deg east of the far end of
# Brooklyn Bridge Park Pier 1: the drawn walk terminated at Pier 1 because
# that is where the DATA stopped, not because that is where the walk stops.
# The old edge cut the pier in half and nothing reported it, because a
# clipped bbox returns fewer rows rather than an error.
#
# CONTEXT extends north across the East River. Nothing there is walked and
# nothing there is measured; it exists so the far shore and the full river
# span can be drawn behind the near field instead of the model ending in
# empty air at the water's edge. Buildings only - see fetch_osm.
STUDY_N, STUDY_S = 40.7085, 40.6955
STUDY_W, STUDY_E = -74.0030, -73.9775

CONTEXT_N, CONTEXT_S = 40.7175, 40.6955
CONTEXT_W, CONTEXT_E = -74.0030, -73.9775

# Kept as the names the rest of the file already used.
NORTH, SOUTH = STUDY_N, STUDY_S
WEST, EAST = STUDY_W, STUDY_E


def curl(url, data=None):
    # Overpass returns 406 Not Acceptable without an explicit Accept header,
    # and the failure surfaces as a JSON decode error two frames away.
    cmd = ["curl.exe", "-s", "--compressed", "-A", UA,
           "-H", "Accept: application/json"]
    if data is not None:
        cmd += ["--data-urlencode", "data=" + data]
    cmd.append(url)
    for attempt in range(4):
        p = subprocess.run(cmd, capture_output=True)
        body = p.stdout.decode("utf-8", "replace")
        if body.strip().startswith(("{", "[")):
            return body
        time.sleep(3 * (attempt + 1))
    raise RuntimeError("no JSON from " + url + "\n" + body[:300])


def fetch_buildings():
    """Every footprint in the CONTEXT extent, tagged by which extent it is in.

    `near` is the flag the drawing code reads. A near building is one a
    pedestrian can stand next to and is drawn at full detail; a far building
    is across the river, is never walked past, and exists only as skyline.
    Carrying the flag here rather than recomputing a bbox test in each
    consumer means the two extents cannot drift apart.
    """
    where = "within_box(the_geom, %f, %f, %f, %f)" % (
        CONTEXT_N, CONTEXT_W, CONTEXT_S, CONTEXT_E)
    url = ("https://data.cityofnewyork.us/resource/5zhs-2jue.geojson"
           "?$where=" + where.replace(" ", "%20").replace(",", "%2C") +
           "&$limit=6000")
    body = curl(url)
    gj = json.loads(body)
    feats = gj.get("features", [])
    print("buildings fetched:", len(feats))
    keep = []
    for f in feats:
        p = f.get("properties") or {}
        g = f.get("geometry") or {}
        if not g.get("coordinates"):
            continue
        try:
            h = float(p.get("height_roof") or 0)
        except (TypeError, ValueError):
            h = 0.0
        try:
            ge = float(p.get("ground_elevation") or 0)
        except (TypeError, ValueError):
            ge = 0.0
        try:
            yr = int(float(p.get("construction_year") or 0))
        except (TypeError, ValueError):
            yr = 0
        lat, lon = _centroid(g)
        near = (STUDY_S <= lat <= STUDY_N) and (STUDY_W <= lon <= STUDY_E)
        keep.append({
            "bin": p.get("bin"),
            "h": round(h, 1),
            "ge": round(ge, 1),
            "yr": yr,
            "near": 1 if near else 0,
            "geom": g,
        })
    print("  near (walkable study extent):", sum(x["near"] for x in keep))
    print("  far  (across-river context):", sum(1 - x["near"] for x in keep))
    return keep


def _centroid(g):
    """Mean vertex of the outer ring, which is all the near/far test needs."""
    polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
    xs, ys = [], []
    for poly in polys:
        if not poly:
            continue
        for pt in poly[0]:
            xs.append(pt[0])
            ys.append(pt[1])
    if not xs:
        return 0.0, 0.0
    return sum(ys) / len(ys), sum(xs) / len(xs)


OVERPASS = "https://overpass-api.de/api/interpreter"

# Walkable and drawable ground, over the STUDY extent only. The far shore is
# never routed over, so pulling lower Manhattan's street network would add
# weight to every consumer for geometry no agent can ever stand on.
Q = """
[out:json][timeout:120];
(
  way["highway"](%(s)f,%(w)f,%(n)f,%(e)f);
  way["railway"="subway"](%(s)f,%(w)f,%(n)f,%(e)f);
  way["natural"="water"](%(s)f,%(w)f,%(n)f,%(e)f);
  way["natural"="coastline"](%(s)f,%(w)f,%(n)f,%(e)f);
  way["leisure"="park"](%(s)f,%(w)f,%(n)f,%(e)f);
  way["man_made"="pier"](%(s)f,%(w)f,%(n)f,%(e)f);
  way["man_made"="bridge"](%(s)f,%(w)f,%(n)f,%(e)f);
  node["railway"="station"](%(s)f,%(w)f,%(n)f,%(e)f);
  node["railway"="subway_entrance"](%(s)f,%(w)f,%(n)f,%(e)f);
);
out body geom;
"""

# The structure itself, over the CONTEXT extent, so the span can be drawn
# river-crossing to river-crossing instead of stopping at the study edge.
# Restricted to ways carried ON a bridge, so this cannot quietly re-import
# the Manhattan street grid the query above deliberately excludes.
QSPAN = """
[out:json][timeout:120];
(
  way["railway"="subway"]["bridge"](%(s)f,%(w)f,%(n)f,%(e)f);
  way["highway"]["bridge"]["name"~"Manhattan Bridge"](%(s)f,%(w)f,%(n)f,%(e)f);
  way["man_made"="bridge"](%(s)f,%(w)f,%(n)f,%(e)f);
);
out body geom;
"""

KEEP_WAY_TAGS = ("highway", "railway", "natural", "leisure", "name",
                 "man_made", "footway", "bridge", "tunnel", "layer", "area")


def _way(el):
    t = el.get("tags") or {}
    return {
        "id": el["id"],
        "tags": {k: t[k] for k in KEEP_WAY_TAGS if k in t},
        "geom": [[round(p["lon"], 6), round(p["lat"], 6)]
                 for p in el["geometry"]],
    }


def fetch_osm():
    q = Q % {"s": STUDY_S, "w": STUDY_W, "n": STUDY_N, "e": STUDY_E}
    body = curl(OVERPASS, data=q)
    o = json.loads(body)
    els = o.get("elements", [])
    print("osm elements fetched:", len(els))
    ways, nodes = [], []
    seen = set()
    for el in els:
        t = el.get("tags") or {}
        if el["type"] == "way" and el.get("geometry"):
            ways.append(_way(el))
            seen.add(el["id"])
        elif el["type"] == "node":
            nodes.append({
                "id": el["id"],
                "tags": {k: t[k] for k in ("railway", "name", "network") if k in t},
                "lon": round(el["lon"], 6), "lat": round(el["lat"], 6),
            })

    qs = QSPAN % {"s": CONTEXT_S, "w": CONTEXT_W,
                  "n": CONTEXT_N, "e": CONTEXT_E}
    body = curl(OVERPASS, data=qs)
    spans, rejected = [], []
    for el in json.loads(body).get("elements", []):
        if el.get("type") != "way" or not el.get("geometry"):
            continue
        if el["id"] in seen:
            continue
        if _outside(el["geometry"], CONTEXT_W, CONTEXT_S, CONTEXT_E, CONTEXT_N):
            rejected.append(el)
            continue
        spans.append(el)
    print("span ways beyond the study extent:", len(spans))
    if rejected:
        # Not an error. See _outside for why this filter has to exist.
        names = sorted({(el.get("tags") or {}).get("name") or str(el["id"])
                        for el in rejected})
        print("  rejected %d way(s) leaving the context extent: %s"
              % (len(rejected), ", ".join(names)))
    ways += [_way(el) for el in spans]
    return {"ways": ways, "nodes": nodes}


def _outside(geom, w, s, e, n):
    """True if any vertex lies outside the requested box.

    Overpass `out geom` returns a way's ENTIRE geometry whenever the way
    touches the bounding box, not the portion inside it. Asking for bridges
    over a box whose corner clips the Williamsburg Bridge therefore returns
    the whole Williamsburg Bridge - 1.5 km of track running 1.5 km east of
    anything that was asked for, tagged exactly like the geometry that was
    wanted, with no error and no warning.

    That is not hypothetical. It happened when the context extent was pushed
    north to reach the Manhattan anchorage: the BMT Jamaica Line arrived, and
    because it runs east-west while the Manhattan Bridge runs north-south, the
    principal-axis fit of the bridge alignment swung from 337.26 deg to
    43.41 deg. A bearing that is wrong by 294 degrees is obvious. A bearing
    wrong by four would not have been, and nothing downstream checks it.
    """
    return any(not (w <= p["lon"] <= e and s <= p["lat"] <= n) for p in geom)


def main():
    os.makedirs(OUT, exist_ok=True)
    what = sys.argv[1] if len(sys.argv) > 1 else "all"

    if what in ("all", "buildings"):
        b = fetch_buildings()
        p = os.path.join(OUT, "buildings.json")
        with open(p, "w", encoding="utf-8") as fh:
            json.dump({"bbox": [STUDY_W, STUDY_S, STUDY_E, STUDY_N],
                       "context_bbox": [CONTEXT_W, CONTEXT_S,
                                        CONTEXT_E, CONTEXT_N],
                       "source": "NYC OpenData 5zhs-2jue BUILDING",
                       "count": len(b),
                       "near": sum(x["near"] for x in b),
                       "buildings": b}, fh)
        print("wrote", p, os.path.getsize(p), "bytes")

    if what in ("all", "osm"):
        o = fetch_osm()
        o["bbox"] = [STUDY_W, STUDY_S, STUDY_E, STUDY_N]
        o["context_bbox"] = [CONTEXT_W, CONTEXT_S, CONTEXT_E, CONTEXT_N]
        o["source"] = "OpenStreetMap via Overpass, (c) OSM contributors, ODbL 1.0"
        p = os.path.join(OUT, "osm.json")
        with open(p, "w", encoding="utf-8") as fh:
            json.dump(o, fh)
        print("wrote", p, os.path.getsize(p), "bytes",
              "| ways", len(o["ways"]), "nodes", len(o["nodes"]))


if __name__ == "__main__":
    main()
