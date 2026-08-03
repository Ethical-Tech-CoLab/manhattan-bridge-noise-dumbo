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
NORTH, SOUTH = 40.7085, 40.6955
WEST, EAST = -73.9975, -73.9775


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
    where = "within_box(the_geom, %f, %f, %f, %f)" % (NORTH, WEST, SOUTH, EAST)
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
        keep.append({
            "bin": p.get("bin"),
            "h": round(h, 1),
            "ge": round(ge, 1),
            "yr": yr,
            "geom": g,
        })
    return keep


OVERPASS = "https://overpass-api.de/api/interpreter"

Q = """
[out:json][timeout:90];
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


def fetch_osm():
    q = Q % {"s": SOUTH, "w": WEST, "n": NORTH, "e": EAST}
    body = curl(OVERPASS, data=q)
    o = json.loads(body)
    els = o.get("elements", [])
    print("osm elements fetched:", len(els))
    ways, nodes = [], []
    for el in els:
        t = el.get("tags") or {}
        if el["type"] == "way" and el.get("geometry"):
            ways.append({
                "id": el["id"],
                "tags": {k: t[k] for k in
                         ("highway", "railway", "natural", "leisure", "name",
                          "man_made", "footway", "bridge", "tunnel", "layer",
                          "area") if k in t},
                "geom": [[round(p["lon"], 6), round(p["lat"], 6)]
                         for p in el["geometry"]],
            })
        elif el["type"] == "node":
            nodes.append({
                "id": el["id"],
                "tags": {k: t[k] for k in ("railway", "name", "network") if k in t},
                "lon": round(el["lon"], 6), "lat": round(el["lat"], 6),
            })
    return {"ways": ways, "nodes": nodes}


def main():
    os.makedirs(OUT, exist_ok=True)
    what = sys.argv[1] if len(sys.argv) > 1 else "all"

    if what in ("all", "buildings"):
        b = fetch_buildings()
        p = os.path.join(OUT, "buildings.json")
        with open(p, "w", encoding="utf-8") as fh:
            json.dump({"bbox": [WEST, SOUTH, EAST, NORTH],
                       "source": "NYC OpenData 5zhs-2jue BUILDING",
                       "count": len(b), "buildings": b}, fh)
        print("wrote", p, os.path.getsize(p), "bytes")

    if what in ("all", "osm"):
        o = fetch_osm()
        o["bbox"] = [WEST, SOUTH, EAST, NORTH]
        o["source"] = "OpenStreetMap via Overpass, (c) OSM contributors, ODbL 1.0"
        p = os.path.join(OUT, "osm.json")
        with open(p, "w", encoding="utf-8") as fh:
            json.dump(o, fh)
        print("wrote", p, os.path.getsize(p), "bytes",
              "| ways", len(o["ways"]), "nodes", len(o["nodes"]))


if __name__ == "__main__":
    main()
