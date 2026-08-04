#!/usr/bin/env python3
"""Fetch awarded labour rates from GSA's public ceiling-rates index.

Source
------
https://buy.gsa.gov/pricing/api/v3/search/ceilingrates/

This is the search backend behind the "Hourly Labor Ceiling Rates" page at
https://buy.gsa.gov/pricing/qr/mas . It replaced calc.gsa.gov, which now
redirects to buy.gsa.gov. It needs no API key and no account.

Every row is a labour category on a live GSA Multiple Award Schedule
contract, together with the ceiling rate the government may be charged for
it. The index name returned on each hit carries a build timestamp, which
this script records, so a run can be dated even though the endpoint itself
is not versioned.

THE TRAP THIS SCRIPT EXISTS TO AVOID
------------------------------------
Two independent silent failures sit on this endpoint.

1.  hits.total.value saturates at 10000 and reports relation "gte". A
    naive read takes 10000 as the population size. For "project manager"
    the true count is 12,916, recovered here by summing exact per-band
    counts. Any percentile computed against the saturated figure is wrong
    and carries no warning.

2.  page_size caps at about 1000 rows and the default ordering is
    current_price ASCENDING. Asking for 1000 rows of a 12,916-row
    population therefore returns the 1000 CHEAPEST, not a sample. A median
    taken from that slice is not a median of anything.

Both are avoided the same way: sweep the price axis in bands using the
filter=price_range:LO,HI parameter, which returns relation "eq", and pull
each band whole. Bands holding more than PAGE rows are subdivided until
they fit. The population is then complete and the percentiles are exact.

WHAT A CEILING RATE IS NOT
--------------------------
It is the maximum a vendor may charge under the schedule. It is not what
an agency pays after task-order competition, and it is not what a private
client pays. Both directions of error are argued in procurement/README.md.
Neither is corrected here: replacing a published number with an estimate
would trade a verified figure for an invented one.

Usage
-----
    python procurement/fetch_rates.py
    python procurement/fetch_rates.py --quiet
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://buy.gsa.gov/pricing/api/v3/search/ceilingrates/"
UA = "Mozilla/5.0 (compatible; manhattan-bridge-noise-dumbo/1.0)"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "rates.json")

PAGE = 1000           # rows the endpoint will actually return in one call
CEIL = 100000.0       # upper bound of the price sweep, in dollars per hour
SAMPLE = 24           # illustrative rows retained per group
BIN = 10.0            # histogram bin width, dollars per hour
FULL_ROWS = 200       # keep every row for a group no larger than this

# (label, keyword, matcher, exclude, field). The matcher decides which
# returned rows belong to the group and the exclude removes near-homographs:
# the index does a loose full-text match and will hand back "Computer Data
# Architect II" and "Architectural Historian" for the keyword "architect".
QUERIES = [
    # --- named vendors, matched on vendor_name -------------------------
    ("vendor:accenture", "ACCENTURE", r"^ACCENTURE", None, "vendor_name"),
    ("vendor:ey", "ERNST", r"^ERNST", None, "vendor_name"),
    ("vendor:deloitte", "DELOITTE", r"^DELOITTE", None, "vendor_name"),
    ("vendor:kpmg", "KPMG", r"^KPMG", None, "vendor_name"),
    ("vendor:booz", "BOOZ ALLEN", r"^BOOZ", None, "vendor_name"),
    # --- disciplines, matched on labor_category ------------------------
    ("disc:program-manager", "program manager", r"\bprogram manager\b", None, "labor_category"),
    ("disc:project-manager", "project manager", r"\bproject manager\b", None, "labor_category"),
    ("disc:sme", "subject matter expert", r"subject matter expert", None, "labor_category"),
    ("disc:data-scientist", "data scientist", r"\bdata scientist\b", None, "labor_category"),
    ("disc:data-engineer", "data engineer", r"\bdata engineer\b", None, "labor_category"),
    ("disc:data-analyst", "data analyst", r"\bdata analyst\b", None, "labor_category"),
    ("disc:software-engineer", "software engineer",
     r"\bsoftware (engineer|developer)\b", None, "labor_category"),
    ("disc:web-developer", "web developer",
     r"\bweb (developer|designer)\b", None, "labor_category"),
    ("disc:technical-writer", "technical writer",
     r"\btechnical writer\b", None, "labor_category"),
    ("disc:gis-analyst", "GIS analyst", r"\bgis\b", None, "labor_category"),
    # Acoustics is deliberately searched twice on two different keywords,
    # because the whole population is small enough that a single keyword
    # missing one row would move the median.
    ("disc:acoustical", "acoustical", r"acoustic", None, "labor_category"),
    ("disc:noise", "noise", r"noise", None, "labor_category"),
    # "architectural" is dominated by ARCHITECTURAL HISTORIANS doing
    # cultural-resource survey work, and "architect" by IT architects.
    # Neither designs buildings. Both are excluded by name.
    ("disc:architect-building", "architectural", r"\barchitect(ural|s)?\b",
     r"historian|histor|data|solution|enterprise|system|software|cloud|network|"
     r"security|technical|computer|erp|infrastructure|information|application|"
     r"integration|devops|platform|\bit\b", "labor_category"),
    ("disc:architect-historian", "architectural", r"architectural histor",
     None, "labor_category"),
    ("disc:environmental-scientist", "environmental scientist",
     r"environmental scientist", None, "labor_category"),
    ("disc:civil-engineer", "civil engineer", r"civil engineer", None, "labor_category"),
    ("disc:attorney", "attorney", r"\battorney\b", r"non.?attorney", "labor_category"),
]

KEEP = (
    "id", "vendor_name", "labor_category", "current_price", "next_year_price",
    "min_years_experience", "education_level", "worksite", "sin",
    "schedule", "idv_piid", "business_size", "contract_start", "contract_end",
)

STATE = {"index": "", "calls": 0, "unresolved": []}


def get(url, tries=4):
    for n in range(tries):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=120) as fh:
                STATE["calls"] += 1
                return json.loads(fh.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            if n == tries - 1:
                raise
            print("  retry %d after %s" % (n + 1, exc), file=sys.stderr)
            time.sleep(2 * (n + 1))
    raise RuntimeError("unreachable")


def query(keyword, lo, hi, size):
    """One call. Returns (count, exact, rows).

    `exact` is False when the endpoint saturates its counter at 10000 and
    reports relation "gte". A saturated band is never accepted as complete;
    sweep() subdivides it until every sub-band reports "eq".
    """
    q = urllib.parse.urlencode({
        "keyword": keyword, "page": 1, "page_size": size,
        "filter": "price_range:%g,%g" % (lo, hi),
    })
    doc = get(API + "?" + q)
    hits = doc.get("hits", {})
    total = hits.get("total", {})
    raw = hits.get("hits", [])
    if raw and not STATE["index"]:
        STATE["index"] = raw[0].get("_index", "")
    return (total.get("value", 0), total.get("relation") == "eq",
            [h["_source"] for h in raw])


def sweep(keyword, lo, hi, depth=0):
    """Pull every row in [lo, hi), subdividing any band the page cap cannot hold."""
    n, exact, rows = query(keyword, lo, hi, PAGE)
    if exact and n == 0:
        return []
    if exact and n <= PAGE:
        if len(rows) != n:
            raise RuntimeError("band [%g,%g) said %d, returned %d"
                               % (lo, hi, n, len(rows)))
        return rows
    if depth > 24 or hi - lo < 0.02:
        # Prices are quoted to the cent, so a band narrower than two cents
        # holding more than PAGE rows means PAGE identical prices. Take what
        # the endpoint gives and RECORD the shortfall rather than looping
        # forever or pretending the band came back whole.
        STATE["unresolved"].append(
            {"keyword": keyword, "lo": lo, "hi": hi, "count": n,
             "exact": exact, "got": len(rows)})
        print("  UNRESOLVED band [%g,%g): %d rows (exact=%s), %d retrieved"
              % (lo, hi, n, exact, len(rows)), file=sys.stderr)
        return rows
    mid = lo + (hi - lo) / 2.0
    return sweep(keyword, lo, mid, depth + 1) + sweep(keyword, mid, hi, depth + 1)


def dedupe(rows):
    """Drop rows seen twice.

    price_range is inclusive at BOTH ends, so a row priced exactly at a
    split point is returned by the band below it and the band above it.
    Summing band counts without this over-states the population: the naive
    three-band probe that motivated this script reported 12,916 project
    managers where the deduplicated sweep finds 12,913.
    """
    seen, out = set(), []
    for r in rows:
        k = r.get("id")
        if k is None:
            k = (r.get("vendor_name"), r.get("labor_category"),
                 r.get("current_price"), r.get("idv_piid"),
                 r.get("min_years_experience"), r.get("sin"))
        if k in seen:
            continue
        seen.add(k)
        out.append(r)
    return out


def pct(vals, p):
    if not vals:
        return None
    if len(vals) == 1:
        return vals[0]
    k = (len(vals) - 1) * p
    f = int(k)
    c = min(f + 1, len(vals) - 1)
    return vals[f] + (vals[c] - vals[f]) * (k - f)


def summarise(rows):
    v = sorted(r["current_price"] for r in rows)
    if not v:
        return {"n": 0}
    return {
        "n": len(v),
        "min": round(v[0], 2),
        "p10": round(pct(v, 0.10), 2),
        "p25": round(pct(v, 0.25), 2),
        "median": round(pct(v, 0.50), 2),
        "p75": round(pct(v, 0.75), 2),
        "p90": round(pct(v, 0.90), 2),
        "max": round(v[-1], 2),
        "mean": round(sum(v) / len(v), 2),
    }


def histogram(rows):
    """Counts per BIN-dollar band, so the whole distribution ships compactly."""
    h = {}
    for r in rows:
        b = int(r["current_price"] // BIN) * int(BIN)
        h[b] = h.get(b, 0) + 1
    return {str(k): h[k] for k in sorted(h)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    def say(*a):
        if not args.quiet:
            print(*a, flush=True)

    out = {
        "source": API,
        "page_reference": "https://buy.gsa.gov/pricing/qr/mas",
        "fetched": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "index": "",
        "note": ("Ceiling rates on live GSA Multiple Award Schedule contracts. "
                 "A ceiling rate is the maximum chargeable under the schedule, "
                 "not a paid price and not a commercial price."),
        "groups": {},
    }

    say("%-30s %8s %8s %8s   %s" % ("group", "pulled", "deduped", "kept", "median"))
    say("-" * 72)

    for label, keyword, pattern, exclude, field in QUERIES:
        raw = sweep(keyword, 0.0, CEIL)
        rows = dedupe(raw)
        rx = re.compile(pattern, re.I)
        ex = re.compile(exclude, re.I) if exclude else None
        kept = [r for r in rows
                if rx.search(str(r.get(field, "")))
                and not (ex and ex.search(str(r.get(field, ""))))
                and isinstance(r.get("current_price"), (int, float))
                and r["current_price"] > 0]
        kept.sort(key=lambda r: r["current_price"])
        trimmed = [{k: r.get(k) for k in KEEP} for r in kept]

        g = {
            "keyword": keyword, "matcher": pattern, "exclude": exclude,
            "field": field,
            "pulled": len(raw), "deduped": len(rows), "kept": len(kept),
            "stats": summarise(kept),
            "histogram_bin": BIN,
            "histogram": histogram(kept),
        }
        if len(trimmed) <= FULL_ROWS:
            g["rows"] = trimmed          # small sets ship whole
        elif len(trimmed) <= SAMPLE:
            g["sample"] = trimmed
        else:
            # An evenly spaced sample across the SORTED population, so the
            # illustration is a spread and not the cheapest N.
            step = (len(trimmed) - 1) / float(SAMPLE - 1)
            g["sample"] = [trimmed[int(round(i * step))] for i in range(SAMPLE)]
        out["groups"][label] = g
        med = g["stats"].get("median")
        say("%-30s %8d %8d %8d   %s" % (label, len(raw), len(rows), len(kept),
                                        ("$%.2f" % med) if med else "-"))

    out["index"] = STATE["index"]
    out["api_calls"] = STATE["calls"]
    out["unresolved_bands"] = STATE["unresolved"]
    if not out["index"]:
        raise SystemExit("no index name returned; the endpoint shape has changed")

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    say("\nindex     %s" % out["index"])
    say("api calls %d" % STATE["calls"])
    if STATE["unresolved"]:
        say("UNRESOLVED bands: %d" % len(STATE["unresolved"]))
    say("wrote     %s (%d bytes)" % (OUT, os.path.getsize(OUT)))


if __name__ == "__main__":
    main()
