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

# --------------------------------------------------------------------------
# A SECOND POPULATION: what a design practice is paid to define a problem.
#
# Asked what a design-build or architecture practice would charge for a
# study like this one, the obvious move is to price it the way the rest of
# instrument B prices everything -- hours by a published schedule rate.
# THAT MOVE IS UNAVAILABLE, AND NOT BY ACCIDENT. Architectural and
# engineering services are procured under the Brooks Act by qualifications
# rather than price, and the statutory note to 40 U.S.C. 1103 says the
# schedule route is closed to them outright:
#
#   "Architectural and engineering services ... shall not be offered under
#    multiple-award schedule contracts entered into by the Administrator of
#    General Services ... unless such services ... are awarded in accordance
#    with the selection procedures set forth in chapter 11 of title 40"
#
# So the instrument that prices every other discipline in this comparison
# is, by statute, not how this one is bought. What survives is instrument
# A: obligated dollars on awards that actually happened. This population
# is those awards, restricted to PSC "C" (architect and engineering) and
# to descriptions naming a STUDY rather than a building.
#
# It is kept separate from the noise population and never pooled with it.
# The two answer different questions -- "what does a noise study sell for"
# and "what does a design practice charge to define a problem" -- and a
# combined percentile would answer neither.
# --------------------------------------------------------------------------
DESIGN_PSC = ["C"]
DESIGN_KEYWORDS = [
    "feasibility study design",
    "concept design study",
    "planning and feasibility study",
    "design charrette",
    "architectural programming study",
    "site investigation and concept",
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


def fetch(keyword, psc=None):
    rows, page = [], 1
    while page <= MAX_PAGES:
        doc = post({
            "filters": {
                "keywords": [keyword],
                "award_type_codes": AWARD_TYPES,
                "psc_codes": psc or PSC,
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


def stats_for(awards):
    v = sorted(a["amount"] for a in awards)
    if not v:
        return {"n": 0}
    return {
        "n": len(v),
        "min": round(v[0], 2), "max": round(v[-1], 2),
        "p10": round(pct(v, 0.10), 2), "p25": round(pct(v, 0.25), 2),
        "median": round(pct(v, 0.50), 2), "p75": round(pct(v, 0.75), 2),
        "p90": round(pct(v, 0.90), 2),
        "mean": round(sum(v) / len(v), 2),
        "total": round(sum(v), 2),
    }


def gather(keywords, psc, say):
    """Collect one population. Dedupe is per population, deliberately.

    A single award can legitimately answer both questions -- an A-E study
    of a rail corridor is both a noise study and a design study -- and
    dropping it from the second population because the first saw it first
    would make the result depend on which query ran earlier.
    """
    seen, awards = set(), []
    say("%-38s %7s %7s" % ("keyword", "rows", "new"))
    say("-" * 56)
    for kw in keywords:
        rows = fetch(kw, psc)
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
        say("%-38s %7d %7d" % (kw, len(rows), new))
    awards.sort(key=lambda a: a["amount"])
    return awards


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    def say(*a):
        if not args.quiet:
            print(*a, flush=True)

    say("POPULATION 1 - noise and acoustic studies")
    awards = gather(KEYWORDS, PSC, say)
    stats = stats_for(awards)

    say("")
    say("POPULATION 2 - architect-engineer problem-definition studies")
    design = gather(DESIGN_KEYWORDS, DESIGN_PSC, say)
    design_stats = stats_for(design)

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
        "design": {
            "filters": {"keywords": DESIGN_KEYWORDS, "psc_codes": DESIGN_PSC,
                        "award_type_codes": AWARD_TYPES,
                        "time_period": {"start": START, "end": END}},
            "note": ("Architect-engineer awards whose description names a STUDY "
                     "rather than a building. Priced this way because the GSA "
                     "multiple-award schedule is closed to A-E services by the "
                     "statutory note to 40 U.S.C. 1103, so the hours-times-rate "
                     "instrument used for every other discipline in this "
                     "comparison is not how this one is bought."),
            "stats": design_stats,
            "awards": design,
        },
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)

    say("")
    say("%-8s %14s %14s" % ("", "noise", "design"))
    for k in ("n", "min", "p10", "p25", "median", "p75", "p90", "max", "mean"):
        say("  %-7s %14s %14s" % (k, stats.get(k), design_stats.get(k)))
    say("wrote %s (%d bytes)" % (OUT, os.path.getsize(OUT)))


if __name__ == "__main__":
    main()
