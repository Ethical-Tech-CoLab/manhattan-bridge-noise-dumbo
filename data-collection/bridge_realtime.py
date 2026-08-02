#!/usr/bin/env python3
"""
bridge_realtime.py - ACTUAL train traversals of the Manhattan Bridge.

The static feed gives the schedule. This gives what ran.

Source: MTA GTFS-realtime. Free, no API key as of 2025 (verified by direct
        anonymous fetch, HTTP 200, see data-collection/README.md).
          https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm
          https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw

Needs:  pip install gtfs-realtime-bindings protobuf

Run once:        python bridge_realtime.py --once
Run for a week:  python bridge_realtime.py --poll 30 --out bridge_week.csv

WHY POLLING: a single snapshot only contains trains currently in service with
live predictions - roughly a 30 to 60 minute lookahead. It is NOT a day's
worth of data. To cover a week you must poll continuously and de-duplicate
by trip_id, which is what --poll does. A 30 s interval is ample against an
85 to 300 s headway and is polite to the endpoint.
"""

import argparse
import csv
import os
import sys
import time
import urllib.request

try:
    from google.transit import gtfs_realtime_pb2
except ImportError:
    sys.exit("pip install gtfs-realtime-bindings protobuf")

FEEDS = {
    "bdfm": "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm",
    "nqrw": "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw",
}

# TRAP: the realtime feed does not use the same stop_id as the static feed for
# the Canal St N/Q platform. Static says Q01. Realtime was observed emitting
# R23. Filtering on the static id alone silently dropped two of the four
# tracks and undercounted by 3x. Accept both.
GRAND = {"D22N", "D22S"}
CANAL = {"Q01N", "Q01S", "R23N", "R23S"}
BRIDGE_ROUTES = {"B", "D", "N", "Q"}

FIELDS = ["trip_id", "route_id", "stop_id", "direction", "chokepoint",
          "predicted_epoch", "predicted_local", "observed_at"]


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "manhattan-bridge-noise-research/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def scan():
    """Return {(trip_id, stop_id): row} for bridge traversals in this snapshot."""
    out = {}
    now = int(time.time())
    for name, url in FEEDS.items():
        msg = gtfs_realtime_pb2.FeedMessage()
        msg.ParseFromString(fetch(url))
        for ent in msg.entity:
            if not ent.HasField("trip_update"):
                continue
            tu = ent.trip_update
            route = tu.trip.route_id
            if route not in BRIDGE_ROUTES:
                continue
            for stu in tu.stop_time_update:
                stop = stu.stop_id
                if route in ("B", "D") and stop not in GRAND:
                    continue
                if route in ("N", "Q") and stop not in CANAL:
                    continue
                t = stu.arrival.time or stu.departure.time
                if not t:
                    continue
                out[(tu.trip.trip_id, stop)] = {
                    "trip_id": tu.trip.trip_id,
                    "route_id": route,
                    "stop_id": stop,
                    "direction": "north" if stop.endswith("N") else "south",
                    "chokepoint": "Grand St" if stop.startswith("D22") else "Canal St",
                    "predicted_epoch": t,
                    "predicted_local": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t)),
                    "observed_at": now,
                }
    return out


def once():
    rows = sorted(scan().values(), key=lambda r: r["predicted_epoch"])
    now = time.time()
    fut = [r for r in rows if r["predicted_epoch"] >= now]
    print("%d bridge traversals in snapshot, %d still ahead" % (len(rows), len(fut)))
    for r in fut[:20]:
        print("  %s  %s  %-9s %-5s  in %5.1f min"
              % (r["predicted_local"][11:], r["route_id"], r["chokepoint"],
                 r["direction"], (r["predicted_epoch"] - now) / 60.0))
    gaps = [fut[i + 1]["predicted_epoch"] - fut[i]["predicted_epoch"] for i in range(len(fut) - 1)]
    gaps = [g for g in gaps if g > 0]
    if gaps:
        print("\n  headway across all four tracks: mean %.0fs  min %ds  max %ds  (n=%d)"
              % (sum(gaps) / len(gaps), min(gaps), max(gaps), len(gaps)))
        print("  a minimum near zero means two trains crossed together and would")
        print("  be heard on the ground as ONE event, not two.")


def poll(interval, out_path):
    """Poll until interrupted, de-duplicating by (trip_id, stop_id).

    A trip's prediction is refined as it approaches. We keep the LAST
    prediction seen for each trip, which is the most accurate one.
    """
    seen = {}
    if os.path.exists(out_path):
        with open(out_path, encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f):
                seen[(r["trip_id"], r["stop_id"])] = r
        print("resuming, %d traversals already recorded" % len(seen))

    print("polling every %ds -> %s   (ctrl-c to stop and write)" % (interval, out_path))
    try:
        while True:
            try:
                batch = scan()
            except Exception as e:
                print("  fetch failed (%s), retrying next tick" % e, flush=True)
                time.sleep(interval)
                continue
            new = sum(1 for k in batch if k not in seen)
            seen.update(batch)
            # flush: without it Python buffers when stdout is a pipe and a
            # week-long run looks hung.
            print("  %s  +%-3d new  %d total"
                  % (time.strftime("%H:%M:%S"), new, len(seen)), flush=True)
            write(out_path, seen)
            time.sleep(interval)
    except KeyboardInterrupt:
        write(out_path, seen)
        print("\nstopped. %d unique traversals in %s" % (len(seen), out_path))


def write(path, seen):
    rows = sorted(seen.values(), key=lambda r: int(r["predicted_epoch"]))
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--once", action="store_true", help="one snapshot to stdout")
    ap.add_argument("--poll", type=int, metavar="SECONDS", help="poll forever at this interval")
    ap.add_argument("--out", default="bridge_traversals.csv")
    a = ap.parse_args()
    if a.poll:
        poll(a.poll, a.out)
    else:
        once()


if __name__ == "__main__":
    main()
