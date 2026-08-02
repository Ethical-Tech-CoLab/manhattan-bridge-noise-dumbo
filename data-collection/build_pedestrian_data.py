"""Build the pedestrian-denominator dataset for the DUMBO noise corridor.

Answers a question the train-frequency work could not: how many people are
actually under the bridge. It does not answer it completely. It closes the
arrival-rate half of Little's Law and leaves the dwell-time half open.

Four independent sources, no API key required for any of them:

  1. MTA Subway Hourly Ridership: Beginning 2025   data.ny.gov 5wq4-mkjj
     ENTRIES ONLY. Riders who entered a complex. This is people LEAVING
     DUMBO on foot-to-subway, not arriving.

  2. MTA Subway Origin-Destination Ridership Estimate: Beginning 2026
     data.ny.gov 28vm-gjqr
     ARRIVALS. Destination is INFERRED from return-swipe patterns, not
     observed. This is the inflow of subway riders becoming pedestrians.

  3. Brooklyn Bridge Automated Pedestrian Counts   NYC 6fi9-q3ta
     Hourly, DIRECTIONAL, on the Manhattan approach. DEAD SINCE 2019.

  4. PLUTO tax-lot records                          NYC 64uk-42ks
     Residential units in the corridor. Current. Units are a tax fact;
     the people in them are an assumption.

Usage:
    python data-collection/build_pedestrian_data.py [--no-inject]

Writes data-collection/pedestrian-data.json and injects it into
visual-review/frequency-dashboard.html between the /*PEDDATA*/ markers.
"""

import argparse
import calendar
import json
import os
import sys
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_JSON = os.path.join(HERE, "pedestrian-data.json")
DASHBOARD = os.path.join(REPO, "visual-review", "frequency-dashboard.html")

NY_STATE = "https://data.ny.gov/resource/"
NY_CITY = "https://data.cityofnewyork.us/resource/"

DS_ENTRIES = "5wq4-mkjj"
DS_OD = "28vm-gjqr"
DS_WALKWAY = "6fi9-q3ta"
DS_PLUTO = "64uk-42ks"

# The two stations that discharge pedestrians into the affected corridor.
# York St is the F platform above the Rutgers Tunnel -- no bridge train stops
# there, which is exactly why it was useless as a place to measure the source
# and is useful as a receptor origin.
STATIONS = {
    "235": {"name": "York St (F)", "lat": 40.701397, "lon": -73.98675,
            "role": "DUMBO / Vinegar Hill; the eastern gateway"},
    "173": {"name": "High St (A,C)", "lat": 40.699337, "lon": -73.99053,
            "role": "Brooklyn Bridge Park north end; the western gateway"},
}

# Reference month. The O-D estimate is published to month 5 of 2026; entries
# run later. Both are pinned to the same month so they can be compared.
REF_YEAR = 2026
REF_MONTH = 5

# The walkway counter died in 2019. 2019 is the last complete year.
WALKWAY_YEAR = 2019

# EU 2002/49/EC Annex I. Same periods as the train dashboard, so the two
# halves of the exposure fraction line up.
PERIODS = [("Daytime", 7, 19), ("Evening", 19, 23), ("Night", 23, 7)]

# Study area. Stated as explicit coordinates rather than borrowed from a
# census geography, because no census geography matches this corridor.
# Nested boxes so the reader can see how much the answer depends on where
# the line is drawn.
BOXES = {
    "core": {
        "label": "DUMBO and Vinegar Hill",
        "lat": (40.6995, 40.7045), "lon": (-73.9955, -73.9820),
        "note": "Water to the BQE. Includes Farragut Houses, directly under the bridge approach",
    },
    "corridor": {
        "label": "Affected corridor",
        "lat": (40.6980, 40.7060), "lon": (-74.0005, -73.9800),
        "note": "York St station to the Brooklyn Bridge Park water entrance",
    },
    "wide": {
        "label": "Wide catchment",
        "lat": (40.6950, 40.7090), "lon": (-74.0050, -73.9750),
        "note": "Adds the Brooklyn Heights and Downtown Brooklyn edges",
    },
}

# Occupancy assumptions. These are the weakest numbers in the file and are
# reported as a bracket for that reason. DUMBO's unit mix is heavily studio
# and one-bedroom, so citywide household size would overstate it.
OCCUPANCY_RATE = 0.92
HH_SIZE_LOW = 1.7
HH_SIZE_HIGH = 2.3


def fetch(base, dataset, params, label, timeout=240):
    url = base + dataset + ".json?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "dumbo-noise-research/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            rows = json.loads(r.read().decode("utf-8", "replace"))
        print("  [%s] %s: %d rows" % (r.status, label, len(rows)), flush=True)
        return rows
    except Exception as exc:
        print("  [ERR] %s: %s" % (label, exc), flush=True)
        return []


def dow_counts(year, month):
    """How many Mondays, Tuesdays ... in the month. Socrata date_extract_dow
    is 0=Sunday. calendar.weekday is 0=Monday. Convert."""
    counts = {d: 0 for d in range(7)}
    for day in range(1, calendar.monthrange(year, month)[1] + 1):
        counts[(calendar.weekday(year, month, day) + 1) % 7] += 1
    return counts


def daytype(dow):
    if dow == 0:
        return "Sunday"
    if dow == 6:
        return "Saturday"
    return "Weekday"


def period_of(hour):
    for name, start, end in PERIODS:
        if start < end:
            if start <= hour < end:
                return name
        elif hour >= start or hour < end:
            return name
    return "Night"


def blank_profile():
    return {dt: [0.0] * 24 for dt in ("Weekday", "Saturday", "Sunday")}


def get_entries():
    """Typical-day ENTRIES by day type and hour. People leaving the corridor."""
    print("1. Hourly entries (%s)" % DS_ENTRIES, flush=True)
    last = calendar.monthrange(REF_YEAR, REF_MONTH)[1]
    where = (
        "station_complex_id in ('%s') AND transit_timestamp >= '%04d-%02d-01T00:00:00' "
        "AND transit_timestamp <= '%04d-%02d-%02dT23:59:59'"
        % ("','".join(STATIONS), REF_YEAR, REF_MONTH, REF_YEAR, REF_MONTH, last)
    )
    rows = fetch(NY_STATE, DS_ENTRIES, {
        "$select": ("station_complex_id,date_extract_dow(transit_timestamp) AS dow,"
                    "date_extract_hh(transit_timestamp) AS hh,sum(ridership) AS riders"),
        "$where": where,
        "$group": "station_complex_id,dow,hh",
        "$limit": "50000",
    }, "entries %04d-%02d" % (REF_YEAR, REF_MONTH))
    if not rows:
        return None

    ndow = dow_counts(REF_YEAR, REF_MONTH)
    per_station = {sid: blank_profile() for sid in STATIONS}
    for r in rows:
        sid = r["station_complex_id"]
        if sid not in per_station:
            continue
        dow, hh = int(r["dow"]), int(r["hh"])
        # Monthly total for this (dow, hour) divided by how many of that dow
        # the month contained -> a typical day.
        per_station[sid][daytype(dow)][hh] += float(r["riders"]) / ndow[dow]

    # Weekday profile is the sum of five weekdays; divide back to one.
    for sid in per_station:
        for hh in range(24):
            per_station[sid]["Weekday"][hh] /= 5.0
    return per_station


def get_arrivals():
    """Typical-day ARRIVALS by day type and hour. People entering the corridor.

    estimated_average_ridership is already 'averaged by day of week over the
    calendar month', so summing over origins for one (month, day_of_week,
    hour) gives a typical-day figure directly. No division needed.
    """
    print("2. Origin-destination arrivals (%s)" % DS_OD, flush=True)
    rows = fetch(NY_STATE, DS_OD, {
        "$select": ("destination_station_complex_id,day_of_week,hour_of_day,"
                    "sum(estimated_average_ridership) AS arr"),
        "$where": ("destination_station_complex_id in ('%s') AND year=%d AND month=%d"
                   % ("','".join(STATIONS), REF_YEAR, REF_MONTH)),
        "$group": "destination_station_complex_id,day_of_week,hour_of_day",
        "$limit": "50000",
    }, "arrivals %04d-%02d" % (REF_YEAR, REF_MONTH))
    if not rows:
        return None

    names = {"Sunday": "Sunday", "Saturday": "Saturday"}
    per_station = {sid: blank_profile() for sid in STATIONS}
    wk_seen = {sid: set() for sid in STATIONS}
    for r in rows:
        sid = r["destination_station_complex_id"]
        if sid not in per_station:
            continue
        dname = r["day_of_week"]
        hh = int(r["hour_of_day"])
        dt = names.get(dname, "Weekday")
        per_station[sid][dt][hh] += float(r["arr"])
        if dt == "Weekday":
            wk_seen[sid].add(dname)

    for sid in per_station:
        n = len(wk_seen[sid]) or 1
        for hh in range(24):
            per_station[sid]["Weekday"][hh] /= n
    return per_station


def get_walkway():
    """Typical-day Brooklyn Bridge walkway flow, both directions, 2019."""
    print("3. Brooklyn Bridge walkway (%s)" % DS_WALKWAY, flush=True)
    rows = fetch(NY_CITY, DS_WALKWAY, {
        "$select": ("date_extract_dow(hour_beginning) AS dow,date_extract_hh(hour_beginning) AS hh,"
                    "sum(pedestrians) AS ped,sum(towards_brooklyn) AS tobk,"
                    "sum(towards_manhattan) AS tomn,count(*) AS n"),
        "$where": ("hour_beginning >= '%d-01-01T00:00:00' AND hour_beginning < '%d-01-01T00:00:00'"
                   % (WALKWAY_YEAR, WALKWAY_YEAR + 1)),
        "$group": "dow,hh",
        "$limit": "500",
    }, "walkway %d" % WALKWAY_YEAR)
    if not rows:
        return None

    out = {k: blank_profile() for k in ("total", "to_brooklyn", "to_manhattan")}
    hours_seen = {dt: 0 for dt in ("Weekday", "Saturday", "Sunday")}
    for r in rows:
        dow, hh = int(r["dow"]), int(r["hh"])
        dt = daytype(dow)
        # n is the number of distinct hours observed for this (dow, hour)
        # slot across the year -- i.e. how many of that weekday had data.
        n = float(r["n"]) or 1.0
        out["total"][dt][hh] += float(r["ped"] or 0) / n
        out["to_brooklyn"][dt][hh] += float(r["tobk"] or 0) / n
        out["to_manhattan"][dt][hh] += float(r["tomn"] or 0) / n
        if hh == 0:
            hours_seen[dt] += 1

    for key in out:
        for hh in range(24):
            out[key]["Weekday"][hh] /= 5.0
    return out


def get_residents():
    """Residential units in each nested study box, from tax-lot records."""
    print("4. PLUTO residential units (%s)" % DS_PLUTO, flush=True)
    result = {}
    for key, box in BOXES.items():
        where = ("latitude between %f and %f AND longitude between %f and %f AND unitsres > 0"
                 % (box["lat"][0], box["lat"][1], box["lon"][0], box["lon"][1]))
        rows = fetch(NY_CITY, DS_PLUTO, {
            "$select": "count(*) AS lots,sum(unitsres) AS units,sum(unitstotal) AS total_units",
            "$where": where,
        }, "pluto %s" % key)
        if not rows:
            continue
        units = int(float(rows[0].get("units") or 0))
        occupied = units * OCCUPANCY_RATE
        result[key] = {
            "label": box["label"],
            "note": box["note"],
            "bbox": {"lat": list(box["lat"]), "lon": list(box["lon"])},
            "lots": int(float(rows[0].get("lots") or 0)),
            "units_res": units,
            "units_total": int(float(rows[0].get("total_units") or 0)),
            "residents_low": int(round(occupied * HH_SIZE_LOW)),
            "residents_high": int(round(occupied * HH_SIZE_HIGH)),
        }
    return result


def to_periods(profile):
    """Collapse a 24-hour profile into EU day / evening / night totals."""
    out = {}
    for dt, hours in profile.items():
        acc = {}
        for name, _, _ in PERIODS:
            acc[name] = 0.0
        for hh in range(24):
            acc[period_of(hh)] += hours[hh]
        out[dt] = {k: round(v, 1) for k, v in acc.items()}
    return out


def combine(per_station):
    """Sum the two stations into one corridor profile."""
    out = blank_profile()
    for sid in per_station:
        for dt in out:
            for hh in range(24):
                out[dt][hh] += per_station[sid][dt][hh]
    return out


def rounded(profile):
    return {dt: [round(v, 1) for v in hours] for dt, hours in profile.items()}


def build():
    entries = get_entries()
    arrivals = get_arrivals()
    walkway = get_walkway()
    residents = get_residents()

    if not (entries and arrivals and walkway and residents):
        print("\nFAILED: one or more sources returned nothing.", flush=True)
        return None

    ent_all = combine(entries)
    arr_all = combine(arrivals)

    data = {
        "generated_for": "Manhattan Bridge / DUMBO rail-noise study",
        "reference_month": "%04d-%02d" % (REF_YEAR, REF_MONTH),
        "walkway_year": WALKWAY_YEAR,
        "periods": [{"name": n, "start": s, "end": e} for n, s, e in PERIODS],
        "stations": {sid: dict(meta) for sid, meta in STATIONS.items()},
        "sources": {
            "entries": {"id": DS_ENTRIES, "host": "data.ny.gov",
                        "title": "MTA Subway Hourly Ridership: Beginning 2025",
                        "measures": "entries only"},
            "arrivals": {"id": DS_OD, "host": "data.ny.gov",
                         "title": "MTA Subway Origin-Destination Ridership Estimate: Beginning 2026",
                         "measures": "inferred destinations"},
            "walkway": {"id": DS_WALKWAY, "host": "data.cityofnewyork.us",
                        "title": "Brooklyn Bridge Automated Pedestrian Counts Demonstration Project",
                        "measures": "directional hourly counts, ended 2019"},
            "pluto": {"id": DS_PLUTO, "host": "data.cityofnewyork.us",
                      "title": "Primary Land Use Tax Lot Output (PLUTO)",
                      "measures": "residential units"},
        },
        "entries_by_station": {sid: rounded(p) for sid, p in entries.items()},
        "arrivals_by_station": {sid: rounded(p) for sid, p in arrivals.items()},
        "entries_hourly": rounded(ent_all),
        "arrivals_hourly": rounded(arr_all),
        "walkway_hourly": {k: rounded(v) for k, v in walkway.items()},
        "entries_periods": to_periods(ent_all),
        "arrivals_periods": to_periods(arr_all),
        "walkway_periods": {k: to_periods(v) for k, v in walkway.items()},
        "entries_periods_by_station": {sid: to_periods(p) for sid, p in entries.items()},
        "arrivals_periods_by_station": {sid: to_periods(p) for sid, p in arrivals.items()},
        "residents": residents,
        "occupancy": {"rate": OCCUPANCY_RATE, "hh_low": HH_SIZE_LOW, "hh_high": HH_SIZE_HIGH},
    }
    return data


MARK = "/*PEDDATA*/"


def inject(data):
    if not os.path.exists(DASHBOARD):
        print("  dashboard not found, skipping injection", flush=True)
        return False
    with open(DASHBOARD, encoding="utf-8") as fh:
        html = fh.read()
    first = html.find(MARK)
    second = html.find(MARK, first + len(MARK))
    if first < 0 or second < 0:
        print("  PEDDATA markers not found in dashboard; skipping injection", flush=True)
        return False
    payload = MARK + "\nconst PED = " + json.dumps(data, separators=(",", ":")) + ";\n"
    html = html[:first] + payload + html[second:]
    with open(DASHBOARD, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("  injected %d bytes into %s" % (len(payload), os.path.basename(DASHBOARD)), flush=True)
    return True


def summarise(d):
    print("\n" + "=" * 72)
    print("PEDESTRIAN DENOMINATOR, typical day, EU 2002/49/EC periods")
    print("Subway figures %s. Walkway figures %d (counter dead)." % (d["reference_month"], d["walkway_year"]))
    print("=" * 72)
    hdr = "%-10s %10s %10s %12s %12s" % ("Day type", "Arrivals", "Entries", "Walkway->BK", "Walkway->MN")
    for dt in ("Weekday", "Saturday", "Sunday"):
        print("\n" + dt)
        print("  " + hdr[10:])
        for name, _, _ in PERIODS:
            print("  %-9s %10.0f %10.0f %12.0f %12.0f" % (
                name,
                d["arrivals_periods"][dt][name], d["entries_periods"][dt][name],
                d["walkway_periods"]["to_brooklyn"][dt][name],
                d["walkway_periods"]["to_manhattan"][dt][name]))
    print("\nResidents")
    for key, r in d["residents"].items():
        print("  %-20s %5d lots  %6d units  -> %5d to %5d residents" % (
            r["label"], r["lots"], r["units_res"], r["residents_low"], r["residents_high"]))
    print("\nWhat this still does not give you: dwell time. Little's Law is")
    print("L = lambda * W. These numbers are lambda. W is unmeasured, so the")
    print("number of people present at any moment remains unknown.")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--no-inject", action="store_true", help="write JSON only")
    args = ap.parse_args()

    print("Building pedestrian denominator dataset\n", flush=True)
    data = build()
    if data is None:
        return 1

    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(data, fh, separators=(",", ":"))
    print("\n  wrote %s (%d bytes)" % (os.path.basename(OUT_JSON), os.path.getsize(OUT_JSON)), flush=True)

    if not args.no_inject:
        inject(data)
    summarise(data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
