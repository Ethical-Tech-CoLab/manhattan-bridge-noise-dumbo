#!/usr/bin/env python3
"""Price this repository's delivered scope against published rate cards.

What this does
--------------
Three independent instruments are computed and REPORTED SIDE BY SIDE.
They are not averaged, because averaging a measured number with an
estimated one launders the estimate.

  A  TOP-DOWN, 5/5.  What federal buyers actually paid for noise and
     acoustic studies, from USASpending obligations (fetch_awards.py).
     No hours are assumed anywhere in this instrument.

  B  BOTTOM-UP, 2/5.  Hours by discipline multiplied by published GSA
     ceiling rates (fetch_rates.py). The RATES are 5/5 and quoted. The
     HOURS are this repository's own estimate and are the weakest term
     in the entire comparison, so they are carried as a band and
     sensitivity-swept rather than stated as a number.

  C  MEASURED, 5/5.  What this programme actually cost, from the
     client's own billing telemetry (the usage-calc module, extracted from
     this repository to github.com/Ethical-Tech-CoLab/usage-calc).

The comparison is deliberately SCOPE-MATCHED in two columns:

  DELIVERED   desk research, source synthesis, data engineering,
              modelling, interactive artifacts, publication.
  NOT DELIVERED
              field acoustic measurement, pedestrian survey, licensed
              architectural design, legal opinion. This programme has
              done NONE of it, and it is the part every absolute claim
              in the programme is blocked on.

A headline of the form "$236 versus six figures" compares column one of
instrument C with both columns of instrument A. That is the over-claim
this repository has withdrawn three times already, and the model refuses
to emit it: usd_all_in in the output always carries the not-delivered
scope alongside it.

Usage
-----
    python procurement/build_procurement_data.py
    python procurement/build_procurement_data.py --no-inject
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "procurement-data.json")
PAGE = os.path.join(HERE, "procurement-dashboard.html")
MARK = "/*PROCDATA*/"

# --------------------------------------------------------------------------
# The hours band. THIS IS THE INVENTED PART AND IT IS NAMED AS SUCH.
#
# Each package converts a MEASURED quantity from the repository into an
# hours range. The measurement is 5/5; the divisor is 1/5. Both ends of
# every band are stated so a reader can substitute their own and rerun.
#
# The per-unit figures are deliberately generous at the low end and
# conservative at the high end, because the interesting question is not
# "what is the number" but "is the ORDER right", and a band that spans a
# factor of two or three answers that while a point estimate does not.
# --------------------------------------------------------------------------
PACKAGES = [
    # key, label, measure, unit, low per unit, high per unit, discipline group
    ("retrieval", "Source retrieval and appraisal", "sources", "source",
     0.5, 1.5, "disc:sme"),
    ("authorship", "Document authorship, cited", "doc_words", "1k words",
     2.5, 6.5, "disc:technical-writer"),
    ("dataeng", "Data acquisition and pipelines", "data_sloc", "100 SLOC",
     5.0, 12.5, "disc:data-engineer"),
    ("modelling", "Quantitative modelling", "model_sloc", "100 SLOC",
     6.0, 15.0, "disc:data-scientist"),
    ("artifacts", "Interactive artifacts", "artifact_sloc", "100 SLOC",
     5.0, 12.5, "disc:software-engineer"),
    ("publication", "Site generation and publication", "site_sloc", "100 SLOC",
     4.0, 10.0, "disc:web-developer"),
]

# Overheads applied to the sum of the packages above, as fractions.
OVERHEADS = [
    ("qa", "Review and quality assurance", 0.10, 0.20, "disc:sme"),
    ("pm", "Engagement management", 0.12, 0.22, "disc:project-manager"),
]

# Scope this programme has NOT executed, priced the same way. Hours here
# come from the method register's own estimates where the register gives
# one, and are otherwise a stated guess. Rated 1/5 throughout.
NOT_DELIVERED = [
    ("field_acoustic", "Field acoustic measurement (Methods 11, 28, 31; captures C1-C5)",
     80, 200, "disc:acoustical",
     "Five capture campaigns plus instrument calibration, analysis and reporting."),
    ("ped_survey", "Pedestrian origin-destination and dwell survey (Method 28)",
     120, 320, "disc:environmental-scientist",
     "Timed cordon counts across three day types, plus analysis. The single "
     "blocking unknown for any absolute exposure figure."),
    ("architecture", "Licensed architectural and structural design",
     200, 600, "disc:architect-building",
     "Nothing in this repository is a design. A design-build proposal needs "
     "a licensed architect and a structural engineer of record."),
    ("legal", "Preemption opinion (Q42)",
     8, 40, "disc:attorney",
     "Whether 40 CFR Part 201 preempts municipal regulation of a wholly "
     "intrastate rapid transit system. One lawyer, one day, per the register."),
]

RATE_LADDER = [
    ("upper", "Whole-schedule upper quartile",
     "75th percentile of awarded ceiling rates for the discipline across every MAS holder"),
    ("median", "Whole-schedule median",
     "Median awarded ceiling rate for the discipline across every MAS holder"),
    ("low", "Whole-schedule 10th percentile",
     "Cheapest decile of awarded ceiling rates for the same discipline"),
]

# --------------------------------------------------------------------------
# A PUBLISHED ARCHITECT-ENGINEER RATE SCHEDULE.
#
# The GSA index cannot price this rung. The statutory note to 40 U.S.C.
# 1103 closes the multiple-award schedule to architectural and engineering
# services unless they are awarded under the Brooks Act procedures, and
# those procedures select on qualifications with price negotiated only
# afterwards (40 U.S.C. 1103(d), 1104(a)). There is therefore no A-E
# equivalent of the awarded ceiling rate that instrument B is built on.
#
# What exists instead is the rate schedule a public body adopts when it
# appoints its A-E panel, published as an exhibit to the resolution. The
# figures below are read from one such resolution -- a New York public
# authority's 2025-2027 A-E appointment, five firms, each exhibit carrying
# its own ladder. Rated 5/5 VERIFIED as published rates; rated 2/5 as a
# guide to what a signature design practice in New York City would charge,
# because an upstate county panel is not that market and the direction of
# the difference is knowable only in sign, not size.
#
# Only the top-of-ladder rows are carried, because the only use made of
# them is a comparison against a single stated rate for one person.
# --------------------------------------------------------------------------
AE_SCHEDULE = {
    "locus": ("Resolution 2025-14, Awarding Architecture/Engineering Contracts "
              "2025-2027, adopted; Exhibits A-C, hourly rate schedules"),
    "url": ("https://broomelandbank.org/wp-content/uploads/2025/05/"
            "2025_14_Resolution-Awarding-Architecture-Engineering-Contracts-"
            "2025-2027_Adopted.pdf"),
    "jurisdiction": "New York public authority A-E panel appointment",
    "effective": "2025",
    "rating": "5/5 VERIFIED as published rates; 2/5 as a guide to the New York City market",
    # label, hourly rate, as printed
    "top_of_ladder": [
        ("Principal", 275.0),
        ("Principal, MEP engineering services", 250.0),
        ("Principal, engineered solutions", 200.0),
        ("Managing member", 190.0),
        ("Partner-in-charge, architectural services", 180.0),
        ("Principal structural engineer, PE", 180.0),
    ],
    "other_rows": [
        ("Senior project manager", 250.0),
        ("Project manager", 220.0),
        ("Senior project architect/engineer", 190.0),
        ("Project architect", 140.0),
        ("Senior environmental scientist", 180.0),
    ],
}

# The operator's own rate for the time spent directing this work.
#
# THIS IS AN INPUT, NOT AN OBSERVATION. It is a statement by the person who
# did the work about what that person's hour is worth, and it is rated the
# way this repository rates every operator statement of intent: 5/5 as a
# statement, and not evidence of anything about a market. It is carried
# beside two rates that ARE market observations so the gap is visible
# rather than absorbed.
OPERATOR_RATE = 1000.0
OPERATOR_RATE_RATING = ("5/5 as a stated rate, 0/5 as a market observation - "
                        "it is the operator's valuation of the operator's own hour")

CODE_EXT = (".py", ".js")
DOC_GLOB = (".md",)


def _pct(vals, p):
    """Linear-interpolated percentile over a pre-sorted list."""
    if not vals:
        return 0.0
    if len(vals) == 1:
        return vals[0]
    k = (len(vals) - 1) * p
    f = int(k)
    c = min(f + 1, len(vals) - 1)
    return vals[f] + (vals[c] - vals[f]) * (k - f)


def sloc(path):
    """Non-blank, non-comment source lines. Injected data spans do not count."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError:
        return 0
    # Drop injected data payloads: they are generated, not authored.
    text = re.sub(r"/\*(DATA|PEDDATA|COHORTDATA|USAGE|PROCDATA)\*/.*?"
                  r"/\*(DATA|PEDDATA|COHORTDATA|USAGE|PROCDATA)\*/",
                  "", text, flags=re.S)
    n = 0
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("//"):
            continue
        n += 1
    return n


def html_sloc(path):
    """Lines of hand-written HTML/CSS/JS in a self-contained artifact."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError:
        return 0
    text = re.sub(r"/\*(DATA|PEDDATA|COHORTDATA|USAGE|PROCDATA)\*/.*?"
                  r"/\*(DATA|PEDDATA|COHORTDATA|USAGE|PROCDATA)\*/",
                  "", text, flags=re.S)
    return sum(1 for ln in text.splitlines() if ln.strip())


def words(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return len(fh.read().split())
    except OSError:
        return 0


def count_sources(paths):
    """Count sources the way this repository actually marks them.

    The corpus cites by NAME AND QUOTED LOCUS in tables, not by hyperlink:
    across nine documents there are twelve distinct external URLs and 249
    lines carrying a 1/5-to-5/5 source rating. Counting URLs would have
    reported seven sources for a body of work built on several hundred.

    The rule is mechanical: a line carrying an N/5 rating is one appraised
    source. It over-counts, because the rubric's own definition lines carry
    ratings too, and it under-counts where one table row appraises several
    documents at once. Neither is corrected; the hours band is wide enough
    to absorb both and narrowing it would imply a precision that is not
    there.
    """
    rating = re.compile(r"\b[1-5]\s*/\s*5\b")
    loci = re.compile(r"^\s*>", re.M)
    rated = quoted = 0
    urls = set()
    urlrx = re.compile(r"https?://[^\s)>\]\"']+")
    for p in paths:
        try:
            with open(p, "r", encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError:
            continue
        rated += sum(1 for ln in text.splitlines() if rating.search(ln))
        quoted += len(loci.findall(text))
        for m in urlrx.finditer(text):
            u = m.group(0).rstrip(".,;:")
            if "ethical-tech-colab" in u.lower():
                continue
            urls.add(u)
    return rated, quoted, len(urls)


def inventory():
    """Measure the delivered corpus. Every figure here is counted, not guessed."""
    md = []
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in
                   (".git", "read", "__pycache__", "assets", "node_modules")]
        for f in files:
            if f.endswith(DOC_GLOB):
                md.append(os.path.join(base, f))
    md.sort()

    data_scripts = ["data-collection/bridge_schedule.py",
                    "data-collection/bridge_realtime.py",
                    "data-collection/build_dashboard_data.py",
                    "data-collection/build_pedestrian_data.py",
                    "data-collection/fetch_geodata.py",
                    "procurement/fetch_rates.py",
                    "procurement/fetch_awards.py"]
    model_scripts = ["data-collection/build_cohort_model.py",
                     "procurement/build_procurement_data.py"]
    site_scripts = ["build_pages.py", "build_carousel.py", "make_hero.py",
                    "check_markdown.py"]
    artifacts = [os.path.join("visual-review", f)
                 for f in sorted(os.listdir(os.path.join(ROOT, "visual-review")))
                 if f.endswith(".html")]
    artifacts += ["usage/usage-dashboard.html"]
    harnesses = ["visual-review/verify_carousel.js"]

    # The usage generator and its verifier were written for this deliverable and
    # were later extracted to Ethical-Tech-CoLab/usage-calc so other projects
    # could use them. They are no longer files in this repository, and sloc()
    # returns 0 for a path that does not exist - so leaving them in the lists
    # would have quietly dropped 1,248 lines from a published total between two
    # versions of the same dashboard, making the delivered work look smaller
    # than it was for a reason that has nothing to do with the work.
    #
    # The last counted values are therefore recorded here, at the commit that
    # removed them, and still counted. This is a stated figure rather than a
    # measured one and is labelled as such in the payload.
    EXTRACTED = {
        "usage/build_usage_data.py": 993,
        "usage/verify_usage.js": 255,
    }

    def total(rel_paths, fn):
        return sum(fn(os.path.join(ROOT, p)) for p in rel_paths)

    doc_words = sum(words(p) for p in md)
    rated, quoted, urls = count_sources(md)
    inv = {
        "documents": len(md),
        "doc_words": doc_words,
        "sources": rated,
        "quoted_loci": quoted,
        "external_urls": urls,
        "data_sloc": total(data_scripts, sloc),
        "model_sloc": total(model_scripts, sloc)
                      + EXTRACTED["usage/build_usage_data.py"],
        "site_sloc": total(site_scripts, sloc) + total(harnesses, sloc)
                     + EXTRACTED["usage/verify_usage.js"],
        "artifact_sloc": total(artifacts, html_sloc),
        "artifacts": len(artifacts),
        "scripts": len(data_scripts) + len(model_scripts) + len(site_scripts)
                   + len(EXTRACTED),
        "extracted": {
            "note": "Written for this deliverable, since extracted to "
                    "github.com/Ethical-Tech-CoLab/usage-calc. Counted at the "
                    "value measured immediately before removal, not re-measured "
                    "at each build.",
            "files": EXTRACTED,
            "sloc": sum(EXTRACTED.values()),
        },
    }
    inv["total_sloc"] = (inv["data_sloc"] + inv["model_sloc"]
                         + inv["site_sloc"] + inv["artifact_sloc"])
    return inv


def measure_for(key, inv):
    """Convert a package measure into the units its productivity band uses."""
    if key == "sources":
        return inv["sources"]
    if key == "doc_words":
        return inv["doc_words"] / 1000.0
    return inv[key] / 100.0


def rate_for(rates, group, kind):
    g = rates["groups"].get(group)
    if not g or not g["stats"].get("n"):
        return None
    st = g["stats"]
    if kind == "median":
        return st["median"]
    if kind == "low":
        return st["p10"]
    return None


def upper_quartile_rate_for(rates, group):
    """The upper-quartile rung.

    Every discipline prices from the 75th percentile of awarded ceiling
    rates across the whole schedule.

    An earlier version of this function first consulted one individual
    holder's own published categories and used a name-matching one where
    it existed, falling back to the percentile otherwise. That branch
    never fired once -- not for any of the eight delivered disciplines
    and not for any of the four not delivered -- because holders publish
    internal job titles ("Cyber Programmer 1", "Business Functions
    Consultant 1") rather than discipline names. It is removed rather
    than left in place: a lookup that never returns is a claim the model
    does not honour, and it made the output describe a substitution that
    was in fact the only path ever taken.
    """
    g = rates["groups"].get(group)
    if g and g["stats"].get("n"):
        return g["stats"]["p75"], "whole-schedule 75th percentile"
    return None, "unpriced"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-inject", action="store_true")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    with open(os.path.join(HERE, "rates.json"), encoding="utf-8") as fh:
        rates = json.load(fh)
    with open(os.path.join(HERE, "awards.json"), encoding="utf-8") as fh:
        awards = json.load(fh)
    with open(os.path.join(ROOT, "usage", "usage-data.json"), encoding="utf-8") as fh:
        usage = json.load(fh)

    inv = inventory()

    # ---- instrument B: bottom-up -----------------------------------------
    packages, lo_h, hi_h = [], 0.0, 0.0
    for key, label, measure, unit, plo, phi, group in PACKAGES:
        q = measure_for(measure, inv)
        h_lo, h_hi = q * plo, q * phi
        lo_h += h_lo
        hi_h += h_hi
        vr, vwhy = upper_quartile_rate_for(rates, group)
        packages.append({
            "key": key, "label": label, "group": group,
            "measure": measure, "quantity": round(q, 2), "unit": unit,
            "per_unit_low": plo, "per_unit_high": phi,
            "hours_low": round(h_lo, 1), "hours_high": round(h_hi, 1),
            "rate_upper": vr, "rate_upper_why": vwhy,
            "rate_median": rate_for(rates, group, "median"),
            "rate_low": rate_for(rates, group, "low"),
        })

    base_lo, base_hi = lo_h, hi_h
    for key, label, flo, fhi, group in OVERHEADS:
        h_lo, h_hi = base_lo * flo, base_hi * fhi
        lo_h += h_lo
        hi_h += h_hi
        vr, vwhy = upper_quartile_rate_for(rates, group)
        packages.append({
            "key": key, "label": label, "group": group,
            "measure": "fraction of packages above", "quantity": None,
            "unit": "share", "per_unit_low": flo, "per_unit_high": fhi,
            "hours_low": round(h_lo, 1), "hours_high": round(h_hi, 1),
            "rate_upper": vr, "rate_upper_why": vwhy,
            "rate_median": rate_for(rates, group, "median"),
            "rate_low": rate_for(rates, group, "low"),
        })

    def cost(pkgs, rung):
        lo = sum((p["hours_low"] or 0) * (p["rate_" + rung] or 0) for p in pkgs)
        hi = sum((p["hours_high"] or 0) * (p["rate_" + rung] or 0) for p in pkgs)
        return round(lo, 2), round(hi, 2)

    delivered = {r: dict(zip(("low", "high"), cost(packages, r)))
                 for r, _, _ in RATE_LADDER}

    # ---- the scope that was not delivered ---------------------------------
    nd = []
    for key, label, h_lo, h_hi, group, why in NOT_DELIVERED:
        vr, vwhy = upper_quartile_rate_for(rates, group)
        nd.append({
            "key": key, "label": label, "group": group, "why": why,
            "hours_low": h_lo, "hours_high": h_hi,
            "rate_upper": vr, "rate_upper_why": vwhy,
            "rate_median": rate_for(rates, group, "median"),
            "rate_low": rate_for(rates, group, "low"),
        })
    not_delivered = {r: dict(zip(("low", "high"), cost(nd, r)))
                     for r, _, _ in RATE_LADDER}

    # ---- sensitivity: which package moves the total -----------------------
    mid = {p["key"]: (p["hours_low"] + p["hours_high"]) / 2.0 for p in packages}
    rate_mid = {p["key"]: p["rate_median"] or 0 for p in packages}
    total_mid = sum(mid[k] * rate_mid[k] for k in mid)
    sens = []
    for p in packages:
        k = p["key"]
        share = (mid[k] * rate_mid[k] / total_mid) if total_mid else 0
        span = ((p["hours_high"] - p["hours_low"]) * rate_mid[k]) if rate_mid[k] else 0
        sens.append({"key": k, "label": p["label"],
                     "share_of_midpoint": round(share, 4),
                     "band_width_usd": round(span, 2)})
    sens.sort(key=lambda s: -s["band_width_usd"])

    # ---- where the two instruments disagree, quantified --------------------
    #
    # The bottom-up estimate for the DELIVERED desk scope lands well above
    # the median federal noise-study award. That disagreement is the most
    # interesting output of this model and it is not reconciled here.
    # Either the hours band is too generous, or the awards buy a narrower
    # deliverable than nine documents, seven artifacts and six datasets.
    # Both are live. What the model can do is turn the disagreement into a
    # number: the hours each award percentile implies at the same blended
    # rate the bottom-up estimate uses.
    hours_mid = (lo_h + hi_h) / 2.0
    blended = (total_mid / hours_mid) if hours_mid else 0
    implied = {}
    for k in ("p25", "median", "p75", "p90", "max"):
        amt = awards["stats"].get(k)
        implied[k] = {
            "usd": amt,
            "hours_at_blended": round(amt / blended, 1) if blended else None,
            "share_of_bottom_up_low": round(amt / delivered["median"]["low"], 3)
            if delivered["median"]["low"] else None,
        }
    crosscheck = {
        "blended_rate_usd_per_hour": round(blended, 2),
        "bottom_up_hours": {"low": round(lo_h, 1), "mid": round(hours_mid, 1),
                            "high": round(hi_h, 1)},
        "awards_imply": implied,
        "reading": ("The bottom-up band and the award distribution do not agree. "
                    "They are reported side by side and neither is adjusted to "
                    "meet the other."),
    }

    # ---- instrument C: what it actually cost ------------------------------
    t = usage["time"]

    # ---- the design-practice rung -----------------------------------------
    #
    # Answers "what would a design practice charge for this?" with the one
    # instrument that is legally available for the question. See the
    # AE_SCHEDULE comment and fetch_awards.py for why instrument B is not.
    dz = awards.get("design", {})
    dstats = dz.get("stats", {"n": 0})
    dsub = {}
    for a in dz.get("awards", []):
        dsub.setdefault(a["matched"], []).append(a["amount"])
    design = {
        "stats": dstats,
        "note": dz.get("note"),
        "filters": dz.get("filters"),
        "by_keyword": [
            {"keyword": k, "n": len(v), "median": round(_pct(sorted(v), 0.5), 2),
             "min": round(min(v), 2), "max": round(max(v), 2)}
            for k, v in sorted(dsub.items(), key=lambda kv: -len(kv[1]))
        ],
        "examples": [
            {k: a[k] for k in ("amount", "description", "agency", "psc", "matched")}
            for a in dz.get("awards", [])
            if dstats.get("p25") and dstats["p25"] <= a["amount"] <= dstats.get("p90", 0)
        ][:12],
        "ratio_to_noise_median": (
            round(dstats["median"] / awards["stats"]["median"], 2)
            if dstats.get("median") and awards["stats"].get("median") else None),
        "why_not_instrument_b": (
            "The statutory note to 40 U.S.C. 1103 bars architectural and "
            "engineering services from GSA multiple-award schedule contracts "
            "unless awarded under the Brooks Act procedures, and those select "
            "on qualifications with compensation negotiated only after "
            "selection. There is no A-E awarded ceiling rate to multiply by."),
        "ae_schedule": {
            "locus": AE_SCHEDULE["locus"],
            "url": AE_SCHEDULE["url"],
            "jurisdiction": AE_SCHEDULE["jurisdiction"],
            "effective": AE_SCHEDULE["effective"],
            "rating": AE_SCHEDULE["rating"],
            "top_of_ladder": [{"label": l, "usd_per_hour": r}
                              for l, r in AE_SCHEDULE["top_of_ladder"]],
            "other_rows": [{"label": l, "usd_per_hour": r}
                           for l, r in AE_SCHEDULE["other_rows"]],
            "top_min": min(r for _, r in AE_SCHEDULE["top_of_ladder"]),
            "top_max": max(r for _, r in AE_SCHEDULE["top_of_ladder"]),
        },
    }

    # ---- the direction term, derived rather than typed --------------------
    #
    # This block used to be three numbers typed into procurement/README.md.
    # They went stale the moment the engagement continued past the day they
    # were written, which is the failure mode build_pages.py exists to stop
    # everywhere else on this site. They are derived here now.
    #
    # The hours band is the active-attention measure from the usage ledger
    # at its two tightest idle cutoffs. It is 2/5: it is inferred from gaps
    # between request timestamps and cannot tell a person reading carefully
    # from a person who walked away.
    act = {a["cutoff_s"]: a for a in t["active"]}
    h_lo = act[120]["active_s"] / 3600.0
    h_hi = act[300]["active_s"] / 3600.0
    sme_rate, _ = upper_quartile_rate_for(rates, "disc:sme")
    ae_lo = design["ae_schedule"]["top_min"]
    ae_hi = design["ae_schedule"]["top_max"]
    direction_rates = [
        ("operator", "Operator's stated rate", OPERATOR_RATE, OPERATOR_RATE_RATING),
        ("ae_top", "Top of a published A-E schedule", ae_hi,
         AE_SCHEDULE["rating"]),
        ("ae_low", "Lowest principal on the same schedule", ae_lo,
         AE_SCHEDULE["rating"]),
        ("sme", "Subject-matter expert, schedule upper quartile", sme_rate,
         "5/5 VERIFIED - published GSA awarded ceiling rate"),
    ]
    metered = usage["totals"]["usd"]
    direction = {
        "hours_low": round(h_lo, 2),
        "hours_high": round(h_hi, 2),
        "hours_basis": ("Active attention from the usage ledger, at idle cutoffs "
                        "of 120 s and 300 s. Sittings %d and %d respectively."
                        % (act[120]["sittings"], act[300]["sittings"])),
        "hours_rating": "2/5 UNVERIFIED - inferred from request timestamps, not a stopwatch",
        "wall_span_h": round(t["wall_span_s"] / 3600.0, 2),
        "inference_sum_h": round(t["inference_sum_s"] / 3600.0, 2),
        "inference_union_h": round(t["inference_union_s"] / 3600.0, 2),
        "metered_inference_usd": metered,
        "rates": [
            {"key": k, "label": lab, "usd_per_hour": r, "rating": rat,
             "usd_low": round(h_lo * r, 2), "usd_high": round(h_hi * r, 2),
             "times_metered_low": round(h_lo * r / metered, 1) if metered else None,
             "times_metered_high": round(h_hi * r / metered, 1) if metered else None}
            for k, lab, r, rat in direction_rates if r
        ],
        "operator_over_ae_top": round(OPERATOR_RATE / ae_hi, 2),
        "operator_over_sme": round(OPERATOR_RATE / sme_rate, 2) if sme_rate else None,
        "reading": ("The operator's rate is a stated input and the other three are "
                    "market observations. They are listed together so the gap is "
                    "visible; they are never averaged and the stated rate is never "
                    "described as what the market pays."),
    }

    measured = {
        "usd": usage["totals"]["usd"],
        "requests": usage["totals"]["requests"],
        "turns": usage["totals"]["turns"],
        "subagents": usage["totals"]["subagents"],
        "models": usage["totals"]["models"],
        "wall_span_h": round(t["wall_span_s"] / 3600.0, 2),
        "inference_sum_h": round(t["inference_sum_s"] / 3600.0, 2),
        "inference_union_h": round(t["inference_union_s"] / 3600.0, 2),
        "counterfactual_uncached_usd": usage["counterfactual"]["uncached_usd"],
        "generated_at": usage["generated_at"],
    }

    out = {
        "schema": "procurement-comparison/1",
        "generated_at": usage["generated_at"],
        "generator": "procurement/build_procurement_data.py",
        "inventory": inv,
        "rate_ladder": [{"key": k, "label": l, "note": n} for k, l, n in RATE_LADDER],
        "rate_populations": {
            k: {"n": g["stats"]["n"], "min": g["stats"]["min"], "max": g["stats"]["max"],
                "median": g["stats"]["median"]}
            for k, g in rates["groups"].items() if g["stats"].get("n")
        },
        "packages": packages,
        "delivered": delivered,
        "not_delivered_packages": nd,
        "not_delivered": not_delivered,
        "hours": {"low": round(lo_h, 1), "high": round(hi_h, 1)},
        "sensitivity": sens,
        "crosscheck": crosscheck,
        "measured": measured,
        "design": design,
        "direction": direction,
        "awards": {
            "n": awards["stats"]["n"],
            "stats": awards["stats"],
            "source": awards["source"],
            "filters": awards["filters"],
            "note": awards["note"],
            "examples": [a for a in awards["awards"]
                         if a["amount"] >= awards["stats"]["p25"]][:12],
        },
        "rates_provenance": {
            "source": rates["source"], "index": rates["index"],
            "fetched": rates["fetched"], "note": rates["note"],
        },
        "ratings": {
            "instrument_a_awards": "5/5 VERIFIED - obligated dollars on real federal contracts",
            "instrument_b_rates": "5/5 VERIFIED - published GSA ceiling rates",
            "instrument_b_hours": "1/5 INVENTED - this repository's own estimate, carried as a band",
            "instrument_c_measured": "5/5 VERIFIED - the client's own billing telemetry",
            "not_delivered_hours": "1/5 INVENTED - no scoping exercise has been done",
            "design_awards": "5/5 VERIFIED - obligated dollars on real federal A-E awards",
            "ae_schedule": AE_SCHEDULE["rating"],
            "operator_rate": OPERATOR_RATE_RATING,
            "direction_hours": "2/5 UNVERIFIED - inferred from request timestamps",
        },
    }

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)

    print("INVENTORY")
    for k in ("documents", "doc_words", "sources", "quoted_loci", "external_urls",
              "artifacts", "scripts",
              "data_sloc", "model_sloc", "site_sloc", "artifact_sloc", "total_sloc"):
        print("  %-16s %s" % (k, format(inv[k], ",")))
    print("\nHOURS  %.0f to %.0f" % (lo_h, hi_h))
    print("\nDELIVERED SCOPE")
    for k, label, _ in RATE_LADDER:
        d = delivered[k]
        print("  %-32s $%12s  to  $%s"
              % (label, format(int(d["low"]), ","), format(int(d["high"]), ",")))
    print("\nSCOPE NOT DELIVERED")
    for k, label, _ in RATE_LADDER:
        d = not_delivered[k]
        print("  %-32s $%12s  to  $%s"
              % (label, format(int(d["low"]), ","), format(int(d["high"]), ",")))
    print("\nWHAT IT ACTUALLY COST         $%s  (%s requests, %.1f h inference)"
          % (format(measured["usd"], ","), format(measured["requests"], ","),
             measured["inference_sum_h"]))
    print("\nWHAT BUYERS ACTUALLY PAID     n=%d  median $%s  p25 $%s  p75 $%s"
          % (awards["stats"]["n"], format(int(awards["stats"]["median"]), ","),
             format(int(awards["stats"]["p25"]), ","),
             format(int(awards["stats"]["p75"]), ",")))
    print("\nWHAT A DESIGN PRACTICE IS PAID TO DEFINE A PROBLEM")
    print("  n=%d  p25 $%s  median $%s  p75 $%s   (%sx the noise-study median)"
          % (design["stats"]["n"], format(int(design["stats"]["p25"]), ","),
             format(int(design["stats"]["median"]), ","),
             format(int(design["stats"]["p75"]), ","),
             design["ratio_to_noise_median"]))
    for b in design["by_keyword"]:
        print("    %-34s n=%-4d median $%s"
              % (b["keyword"], b["n"], format(int(b["median"]), ",")))
    print("  no schedule rate exists for this rung: %s"
          % design["why_not_instrument_b"].split(".")[0])

    print("\nTHE DIRECTION TERM   %.1f - %.1f active hours" %
          (direction["hours_low"], direction["hours_high"]))
    for r in direction["rates"]:
        print("  %-46s $%7.2f/h  ->  $%9s - $%-9s  (%sx - %sx metered)"
              % (r["label"], r["usd_per_hour"],
                 format(int(r["usd_low"]), ","), format(int(r["usd_high"]), ","),
                 r["times_metered_low"], r["times_metered_high"]))

    print("\nSENSITIVITY (widest band first)")
    for s in sens[:5]:
        print("  %-34s band $%-10s  %.1f%% of midpoint"
              % (s["label"], format(int(s["band_width_usd"]), ","),
                 100 * s["share_of_midpoint"]))
    print("\nCROSS-CHECK  blended $%.2f/h, bottom-up midpoint %.0f h"
          % (crosscheck["blended_rate_usd_per_hour"],
             crosscheck["bottom_up_hours"]["mid"]))
    for k, v in crosscheck["awards_imply"].items():
        print("  award %-7s $%-11s implies %8s h  (%.0f%% of the bottom-up low)"
              % (k, format(int(v["usd"]), ","),
                 format(int(v["hours_at_blended"]), ","),
                 100 * (v["share_of_bottom_up_low"] or 0)))
    print("\nwrote %s (%d bytes)" % (OUT, os.path.getsize(OUT)))

    if not args.no_inject and os.path.exists(PAGE):
        inject(out)


def inject(data):
    with open(PAGE, "r", encoding="utf-8") as fh:
        html = fh.read()
    # A page that mentions the marker in its own prose will have three of
    # them, and a non-greedy match will then splice out everything between
    # the prose and the script. That happened once, silently, and the page
    # rendered empty with no console error. Count first.
    seen = html.count(MARK)
    if seen != 2:
        raise SystemExit(
            "expected exactly 2 %s markers in %s, found %d. A marker in prose "
            "will be spliced by the injection." % (MARK, PAGE, seen))
    payload = MARK + "\nconst PROC = " + json.dumps(data, sort_keys=True) + ";\n" + MARK
    new, n = re.subn(re.escape(MARK) + r".*?" + re.escape(MARK), lambda m: payload,
                     html, count=1, flags=re.S)
    if not n:
        raise SystemExit("injection markers %s not found in %s" % (MARK, PAGE))
    if new.count("const PROC = ") != 1:
        raise SystemExit("injection left %d PROC declarations in %s"
                         % (new.count("const PROC = "), PAGE))
    with open(PAGE, "w", encoding="utf-8") as fh:
        fh.write(new)
    print("injected into %s (%d bytes)" % (PAGE, os.path.getsize(PAGE)))


if __name__ == "__main__":
    main()
