#!/usr/bin/env python3
"""
build_dashboard_data.py - per-event traversal data for the frequency dashboard.

bridge_schedule.py counts trains per hour. That is not the same as counting
NOISE EVENTS per hour, because two trains crossing together are heard as one.
This script emits every individual traversal - route, direction, chokepoint and
time - so the merge computation can be done downstream against an adjustable
coincidence window and an adjustable chokepoint-to-bridge travel time.

Output: dashboard-data.json, consumed by visual-review/frequency-dashboard.html

Run: python build_dashboard_data.py
"""

import csv
import json
import os
import sys

import bridge_schedule as bs

ROUTES = ["B", "D", "N", "Q"]


def main():
    gtfs = os.path.join(os.environ.get("TEMP", "/tmp"), "mta_gtfs_static")
    bs.fetch_gtfs(gtfs)

    trips = {}
    for r in bs.read_csv(os.path.join(gtfs, "trips.txt")):
        if r["route_id"] in bs.BRIDGE_ROUTES:
            trips[r["trip_id"]] = (r["route_id"], r["service_id"])

    # events[service] = [[route_idx, dir_idx, chokepoint_idx, seconds], ...]
    #   dir_idx        0 = north (toward Manhattan), 1 = south (toward Brooklyn)
    #   chokepoint_idx 0 = Grand St (B/D), 1 = Canal St (N/Q)
    events = {}
    for r in bs.read_csv(os.path.join(gtfs, "stop_times.txt")):
        stop = r["stop_id"]
        if stop not in bs.GRAND and stop not in bs.CANAL:
            continue
        t = trips.get(r["trip_id"])
        if t is None:
            continue
        route, service = t
        if route in ("B", "D") and stop not in bs.GRAND:
            continue
        if route in ("N", "Q") and stop not in bs.CANAL:
            continue
        h, m, s = (int(x) for x in r["departure_time"].split(":"))
        events.setdefault(service, []).append([
            ROUTES.index(route),
            0 if stop.endswith("N") else 1,
            0 if stop in bs.GRAND else 1,
            (h * 3600 + m * 60 + s) % 86400,
        ])

    for v in events.values():
        v.sort(key=lambda e: e[3])

    feed_version = ""
    fi = os.path.join(gtfs, "feed_info.txt")
    if os.path.exists(fi):
        for r in bs.read_csv(fi):
            feed_version = r.get("feed_version", "")
            break

    out = {
        "routes": ROUTES,
        "directions": ["north", "south"],
        "chokepoints": ["Grand St (B/D)", "Canal St (N/Q)"],
        "feed_version": feed_version,
        "events": events,
    }
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "dashboard-data.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, separators=(",", ":"))

    print("feed %s" % feed_version)
    for k in sorted(events):
        print("  %-9s %5d traversals" % (k, len(events[k])))
    print("wrote %s (%d bytes)" % (path, os.path.getsize(path)))

    inject(here, out)
    return 0


def inject(here, out):
    """Inline the data into the dashboard, between the /*DATA*/ markers.

    The dashboard has to stay self-contained - no build step, no server, no
    network - so the data lives inside the HTML rather than being fetched.
    """
    html = os.path.join(here, "..", "visual-review", "frequency-dashboard.html")
    if not os.path.exists(html):
        print("dashboard not found, skipping inject")
        return
    with open(html, encoding="utf-8") as f:
        txt = f.read()
    marker = "/*DATA*/"
    a = txt.find(marker)
    b = txt.find(marker, a + len(marker))
    if a < 0 or b < 0:
        print("DATA markers not found, skipping inject")
        return
    blob = "const DATA=" + json.dumps(out, separators=(",", ":")) + ";"
    txt = txt[:a + len(marker)] + blob + txt[b:]
    with open(html, "w", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    print("injected %d bytes into %s" % (len(blob), os.path.normpath(html)))


if __name__ == "__main__":
    sys.exit(main())
