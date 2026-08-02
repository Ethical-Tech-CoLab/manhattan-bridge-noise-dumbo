#!/usr/bin/env python3
"""
bridge_schedule.py - scheduled train traversals of the Manhattan Bridge.

Answers: how many trains cross the Manhattan Bridge per hour, by day type?

Source: MTA GTFS static feed. Free, no API key, no registration.
        http://web.mta.info/developers/data/nyct/subway/google_transit.zip

Run:    python bridge_schedule.py
        (downloads ~5 MB, takes about a minute, needs only the stdlib)

WHY NOT GOOGLE MAPS: Google Maps' transit data for NYC is a redistribution
of this same MTA feed. The Google Maps Platform Terms of Service prohibit
scraping, bulk export and long-term storage of the results, which is exactly
what a week-long frequency study requires. Going to Google means paying for,
and accepting restrictions on, a copy of a file the MTA gives away.

See data-collection/README.md for the traps this script exists to avoid.
"""

import csv
import collections
import io
import os
import sys
import urllib.request
import zipfile

GTFS_URL = "http://web.mta.info/developers/data/nyct/subway/google_transit.zip"

# Chokepoints. Keyed on stop_id, NEVER on stop_name - see README.md trap 2.
#   Grand St  D22 - the last Manhattan stop on the north (B/D) tracks
#   Canal St  Q01 - the last Manhattan stop on the south (N/Q) tracks
# Every Manhattan Bridge train stops at exactly one of these. DeKalb Av does
# NOT work: the D and the N run express and skip it - see README.md trap 3.
GRAND = {"D22N", "D22S"}
CANAL = {"Q01N", "Q01S"}

# R and W cross via the Montague St tunnel, not the bridge. Excluded.
BRIDGE_ROUTES = {"B", "D", "N", "Q"}


def fetch_gtfs(dest):
    if os.path.isdir(dest) and os.path.exists(os.path.join(dest, "stop_times.txt")):
        print("using cached GTFS in %s" % dest)
        return
    print("downloading %s" % GTFS_URL)
    with urllib.request.urlopen(GTFS_URL, timeout=180) as r:
        blob = r.read()
    print("  %d bytes" % len(blob))
    os.makedirs(dest, exist_ok=True)
    zipfile.ZipFile(io.BytesIO(blob)).extractall(dest)
    print("  extracted to %s" % dest)


def read_csv(path):
    # MTA ships a UTF-8 BOM. utf-8-sig or the first column name is mangled.
    with open(path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            yield row


def collect(gtfs_dir):
    trips = {}
    for r in read_csv(os.path.join(gtfs_dir, "trips.txt")):
        if r["route_id"] in BRIDGE_ROUTES:
            trips[r["trip_id"]] = (r["route_id"], r["service_id"])

    # (service_id, hour) -> count ; and (service_id, route_id) -> count
    hourly = collections.Counter()
    per_route = collections.Counter()
    services = set()

    for r in read_csv(os.path.join(gtfs_dir, "stop_times.txt")):
        stop = r["stop_id"]
        if stop not in GRAND and stop not in CANAL:
            continue
        t = trips.get(r["trip_id"])
        if t is None:
            continue
        route, service = t
        # A B/D only counts at Grand St, an N/Q only at Canal St. Without this
        # a route that touches both platforms would be counted twice.
        if route in ("B", "D") and stop not in GRAND:
            continue
        if route in ("N", "Q") and stop not in CANAL:
            continue
        # GTFS times run past 24:00:00 for after-midnight service.
        hour = int(r["departure_time"].split(":")[0]) % 24
        hourly[(service, hour)] += 1
        per_route[(service, route)] += 1
        services.add(service)

    return hourly, per_route, sorted(services)


def report(hourly, per_route, services):
    print()
    print("SCHEDULED MANHATTAN BRIDGE TRAVERSALS")
    print("all four tracks, both directions, B + D + N + Q")
    print()

    head = "  hr  " + "  ".join("%-18s" % s for s in services)
    print(head)
    print("  " + "-" * (len(head) - 2))
    for h in range(24):
        cells = []
        for s in services:
            n = hourly[(s, h)]
            gap = ("%.0fs" % (3600.0 / n)) if n else "-"
            cells.append("%4d  (%7s)   " % (n, gap))
        print("  %02d  %s" % (h, "".join(cells)))

    print()
    print("  daily totals")
    for s in services:
        print("    %-10s %5d traversals" % (s, sum(hourly[(s, h)] for h in range(24))))

    print()
    print("  by route")
    for s in services:
        parts = ["%s %d" % (r, per_route[(s, r)]) for r in sorted(BRIDGE_ROUTES)]
        print("    %-10s %s" % (s, "   ".join(parts)))
    print()
    print("  NOTE: a route showing 0 does not run that day at all.")
    print("  NOTE: this is SCHEDULE. Actual traversals differ, and neither this")
    print("        feed nor the realtime feed contains non-revenue moves (work")
    print("        trains, put-ins, lay-ups), which cross the bridge and make noise.")


def main():
    gtfs_dir = os.path.join(os.environ.get("TEMP", "/tmp"), "mta_gtfs_static")
    fetch_gtfs(gtfs_dir)
    hourly, per_route, services = collect(gtfs_dir)
    if not services:
        print("no bridge trips found - the feed layout may have changed", file=sys.stderr)
        return 1
    report(hourly, per_route, services)
    return 0


if __name__ == "__main__":
    sys.exit(main())
