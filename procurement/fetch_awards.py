#!/usr/bin/env python3
"""Fetch what noise and acoustic studies actually SOLD for, from USASpending.

Source
------
https://api.usaspending.gov/api/v2/search/spending_by_award/

USASpending publishes every federal prime award. No key, no account. The
figures here are OBLIGATED DOLLARS on real contracts, not list prices, so
they sit a rung above the ceiling rates in fetch_rates.py: a ceiling rate
is what a vendor MAY charge, an obligation is what an agency DID pay.

Why this exists
---------------
The alternative way to price a study is hours multiplied by a rate, and
the hours are invented. This dataset removes the invented term for one
whole column of the comparison: it says what the market charged for a
named deliverable, with the deliverable named in the award description.

Selection rule, stated so it can be attacked
--------------------------------------------
Awards are selected by keyword against the award description AND by
Product/Service Code, so the filter is mechanical rather than a hand-pick.
PSC "C" is Architect and Engineering services; "R" is professional,
administrative and management support; "B" is special studies and
analysis, not R&D. Equipment purchases sit under other codes and drop out.
That rule still admits work that is not comparable to this programme
(a bombing-range noise study is not a bridge). Nothing is hand-removed;
the incomparable rows are kept, listed, and argued about in the prose,
because silently deleting the rows that spoil an average is the failure
this repository exists to avoid.

WHAT THIS IS NOT
----------------
Federal only. The MTA, NYCDOT and NYCDEP are state and city bodies and
do not appear in USASpending at all, so the single most relevant buyer of
a Manhattan Bridge noise study is missing from the only dataset that
records what such studies cost. That gap is the largest weakness in the
procurement comparison and is stated as such.

Usage
-----
    python procurement/fetch_awards.py
    python procurement/fetch_awards.py --quiet
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

API = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
UA = "Mozilla/5.0 (compatible; manhattan-bridge-noise-dumbo/1.0)"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "awards.json")

START = "2015-01-01"
END = "2026-08-01"
PSC = ["B", "C", "R"]          # studies and analysis, A&E, professional services
AWARD_TYPES = ["A", "B", "C", "D"]   # definitive contracts and orders
PAGE = 100
MAX_PAGES = 6

KEYWORDS = [
    "noise study",
    "acoustical study",
    "noise and vibration",
    "noise monitoring",
    "acoustical consulting services",
    "noise analysis",
    "acoustic assessment",
    "environmental noise",
]

FIELDS = ["Award ID", "Recipient Name", "Award Amount", "Description",
          "Awarding Agency", "Awarding Sub Agency", "Start Date", "End Date",
          "psc_description", "generated_internal_id"]


def post(body, tries=4):
    data = json.dumps(body).encode("utf-8")
    for n in range(tries):
        try:
            req = urllib.request.Request(API, data=data, headers={
                "Content-Type": "application/json", "User-Agent": UA})
            with urllib.request.urlopen(req, timeout=180) as fh:
                return json.loads(fh.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            if n == tries - 1:
                raise
            print("  retry %d after %s" % (n + 1, exc), file=sys.stderr)
            time.sleep(3 * (n + 1))
    raise RuntimeError("unreachable")


def fetch(keyword):
    rows, page = [], 1
    while page <= MAX_PAGES:
        doc = post({
            "filters": {
                "keywords": [keyword],
                "award_type_codes": AWARD_TYPES,
                "psc_codes": PSC,
                "time_period": [{"start_date": START, "end_date": END}],
            },
            "fields": FIELDS, "page": page, "limit": PAGE,
            "sort": "Award Amount", "order": "desc", "subawards": False,
        })
        got = doc.get("results", [])
        rows.extend(got)
        if not doc.get("page_metadata", {}).get("hasNext"):
            break
        page += 1
    return rows


def pct(vals, p):
    if not vals:
        return None
    if len(vals) == 1:
        return vals[0]
    k = (len(vals) - 1) * p
    f = int(k)
    c = min(f + 1, len(vals) - 1)
    return vals[f] + (vals[c] - vals[f]) * (k - f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    def say(*a):
        if not args.quiet:
            print(*a, flush=True)

    seen, awards = set(), []
    say("%-34s %7s %7s" % ("keyword", "rows", "new"))
    say("-" * 52)
    for kw in KEYWORDS:
        rows = fetch(kw)
        new = 0
        for r in rows:
            key = r.get("generated_internal_id") or (
                r.get("Award ID"), r.get("Recipient Name"), r.get("Award Amount"))
            if key in seen:
                continue
            seen.add(key)
            amt = r.get("Award Amount")
            if not isinstance(amt, (int, float)) or amt <= 0:
                continue
            awards.append({
                "award_id": r.get("Award ID"),
                "recipient": r.get("Recipient Name"),
                "amount": round(float(amt), 2),
                "description": (r.get("Description") or "").strip(),
                "agency": r.get("Awarding Agency"),
                "sub_agency": r.get("Awarding Sub Agency"),
                "start": r.get("Start Date"),
                "end": r.get("End Date"),
                "psc": r.get("psc_description"),
                "matched": kw,
            })
            new += 1
        say("%-34s %7d %7d" % (kw, len(rows), new))

    awards.sort(key=lambda a: a["amount"])
    v = [a["amount"] for a in awards]
    stats = {
        "n": len(v),
        "min": round(v[0], 2), "max": round(v[-1], 2),
        "p10": round(pct(v, 0.10), 2), "p25": round(pct(v, 0.25), 2),
        "median": round(pct(v, 0.50), 2), "p75": round(pct(v, 0.75), 2),
        "p90": round(pct(v, 0.90), 2),
        "mean": round(sum(v) / len(v), 2),
        "total": round(sum(v), 2),
    } if v else {"n": 0}

    out = {
        "source": API,
        "fetched": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "filters": {"keywords": KEYWORDS, "psc_codes": PSC,
                    "award_type_codes": AWARD_TYPES,
                    "time_period": {"start": START, "end": END}},
        "note": ("Federal prime awards only. State and city buyers, including "
                 "the MTA, NYCDOT and NYCDEP, do not appear in USASpending."),
        "stats": stats,
        "awards": awards,
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)

    say("")
    for k in ("n", "min", "p10", "p25", "median", "p75", "p90", "max", "mean"):
        say("  %-7s %s" % (k, stats.get(k)))
    say("wrote %s (%d bytes)" % (OUT, os.path.getsize(OUT)))


if __name__ == "__main__":
    main()
