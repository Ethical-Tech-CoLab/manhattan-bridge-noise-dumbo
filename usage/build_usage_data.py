#!/usr/bin/env python3
"""Extract per-request model usage for one project from the Copilot CLI session store.

This script is deliberately generic. It hardcodes nothing about the Manhattan
Bridge study; point it at any working directory that has been worked on with
the Copilot CLI and it will produce the same JSON shape.

    python usage/build_usage_data.py                     # this working directory
    python usage/build_usage_data.py --cwd C:\\Dev\\Other
    python usage/build_usage_data.py --session <uuid>
    python usage/build_usage_data.py --list              # what sessions exist
    python usage/build_usage_data.py --no-inject         # JSON only

WHERE THE NUMBERS COME FROM

    ~/.copilot/session-store.db, table assistant_usage_events.

    One row per request actually issued to a model, carrying the model id,
    the token count on each billing channel, the cost in nano-AIU, the wall
    duration, which turn it belonged to, and - where the request came from a
    sub-agent - the id of the tool call that spawned it.

THE ONE RULE THAT MATTERS

    Cost and token totals are read from token_details_json, NOT from the
    input_tokens / cache_write_tokens columns beside it.

    The columns disagree with the details on compaction rows. See
    usage/README.md, trap 2. The details reconcile to the stored
    total_nano_aiu on every row; the script asserts this and refuses to
    write output if it ever stops being true.
"""

import argparse
import datetime as dt
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# One AIU is one US cent. Established in usage/README.md by matching the
# per-model prices in the client's own models.json against three vendor list
# prices that agree to the cent, and against the published cache ratios.
CENTS_PER_AIU = 1.0
NANO = 1_000_000_000

# Idle cut-offs, in seconds, at which "active time" is reported. There is no
# correct value, which is the point of reporting several.
IDLE_CUTOFFS = (120, 300, 600, 1800)

# ---------------------------------------------------------------------------
# Energy. NONE OF THIS IS MEASURED.
#
# No joule count reaches a client. What follows applies published per-query
# figures to a request count, which is an ESTIMATE STAPLED TO A FACT, and the
# dashboard says so in those words. Every constant carries the sentence it was
# read from so a reader can check it rather than trust it.
# ---------------------------------------------------------------------------
ENERGY_SOURCE = {
    "title": "Energy Use of AI Inference: Efficiency Pathways and Test-Time Compute",
    "authors": "Oviedo, Kazhamiaka, Choukse, Kim, Luers, Nakagawa, Bianchini, "
               "Lavista Ferres",
    "venue": "Joule, 2025 (Microsoft Research)",
    "url": "https://www.microsoft.com/en-us/research/publication/"
           "energy-use-of-ai-inference-efficiency-pathways-and-test-time-compute",
    "rating": "5/5 VERIFIED for the figures; 2/5 for their application here",
    "locus": "we estimate a median energy per query of 0.34 Wh (IQR: 0.18-0.67) "
             "for frontier-scale models (>200 billion parameters) ... Extending "
             "to test-time scaling scenarios with 15x more tokens per typical "
             "query, the median energy rises 13-fold to 4.32 Wh",
}
ENERGY_SCENARIOS = [
    ("Traditional query, IQR low", 0.18),
    ("Traditional query, median", 0.34),
    ("Traditional query, IQR high", 0.67),
    ("Test-time scaling, median", 4.32),
]
# "The average U.S. household consumes about 10,500 kilowatthours (kWh) of
# electricity per year." - US EIA, Electricity use in homes. 5/5 VERIFIED.
HOUSEHOLD_KWH_PER_YEAR = 10500
HOUSEHOLD_SOURCE = {
    "locus": "The average U.S. household consumes about 10,500 kilowatthours "
             "(kWh) of electricity per year.",
    "url": "https://www.eia.gov/energyexplained/use-of-energy/"
           "electricity-use-in-homes.php",
    "venue": "US Energy Information Administration",
}


def energy(requests):
    """Bracket the electricity, and refuse to collapse it to one number.

    The spread between the first and last scenario is a factor of 24. Quoting
    any single value from that range as THE energy cost of this project would
    be false precision dressed as accounting.
    """
    per_day = HOUSEHOLD_KWH_PER_YEAR / 365.0
    rows = []
    for name, wh in ENERGY_SCENARIOS:
        kwh = requests * wh / 1000.0
        rows.append(
            {
                "scenario": name,
                "wh_per_request": wh,
                "kwh": round(kwh, 3),
                "household_hours": round(kwh / per_day * 24, 2),
            }
        )
    return {
        "requests": requests,
        "scenarios": rows,
        "spread": round(rows[-1]["kwh"] / rows[0]["kwh"], 1),
        "measured": False,
        "why_neither_regime_fits": (
            "The published regimes are separated by output length. This "
            "workload is not separated that way: its requests are short in "
            "output and extremely long in input, and almost all of that input "
            "is served from a prompt cache. The bracket below is therefore "
            "wider than the truth in one direction and narrower in another, "
            "and no arithmetic available here can close it."
        ),
        "source": ENERGY_SOURCE,
        "household_source": HOUSEHOLD_SOURCE,
    }


def die(msg):
    print("USAGE EXTRACT FAILED: " + msg, file=sys.stderr)
    sys.exit(1)


def default_db():
    return os.path.join(os.path.expanduser("~"), ".copilot", "session-store.db")


def open_snapshot(path):
    """Copy the store, and its WAL, so a live CLI cannot change it under us."""
    if not os.path.exists(path):
        die("no session store at " + path)
    tmp = tempfile.mkdtemp(prefix="usagedb-")
    for ext in ("", "-wal", "-shm"):
        src = path + ext
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(tmp, "session-store.db" + ext))
    con = sqlite3.connect(os.path.join(tmp, "session-store.db"))
    con.row_factory = sqlite3.Row
    return con, tmp


def pick_session(con, args):
    rows = con.execute(
        "SELECT id, cwd, repository, branch, created_at, updated_at FROM sessions"
    ).fetchall()
    counts = dict(
        con.execute(
            "SELECT session_id, COUNT(*) FROM assistant_usage_events GROUP BY session_id"
        ).fetchall()
    )
    if args.list:
        print("%-38s %6s  %s" % ("session", "reqs", "cwd"))
        for r in sorted(rows, key=lambda r: r["created_at"] or ""):
            print("%-38s %6d  %s" % (r["id"], counts.get(r["id"], 0), r["cwd"] or "-"))
        sys.exit(0)
    if args.session:
        hit = [r for r in rows if r["id"] == args.session]
        if not hit:
            die("no session " + args.session)
        return hit[0]
    want = os.path.normcase(os.path.abspath(args.cwd or ROOT))
    hit = [r for r in rows if r["cwd"] and os.path.normcase(os.path.abspath(r["cwd"])) == want]
    if not hit:
        die(
            "no session recorded for %s. Run with --list to see what exists." % want
        )
    # Most requests wins, so a stray one-shot session cannot shadow the real one.
    hit.sort(key=lambda r: counts.get(r["id"], 0), reverse=True)
    return hit[0]


def parse_ts(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def load_events(con, sid):
    rows = con.execute(
        "SELECT * FROM assistant_usage_events WHERE session_id=? ORDER BY created_at, id",
        (sid,),
    ).fetchall()
    if not rows:
        die("session %s has no usage events" % sid)
    events = []
    for r in rows:
        raw = r["token_details_json"]
        if not raw:
            die("row %s carries no token_details_json; totals would be a guess" % r["id"])
        details = json.loads(raw)
        chans, nano = {}, 0
        for e in details:
            per_token = e["costPerBatch"] // e["batchSize"]
            n = e["tokenCount"] * per_token
            nano += n
            chans[e["tokenType"]] = {
                "tokens": e["tokenCount"],
                "price_nano_per_token": per_token,
                "nano_aiu": n,
            }
        stored = r["total_nano_aiu"] or 0
        if nano != stored:
            die(
                "row %s: token_details_json sums to %d nano-AIU but the row says %d. "
                "The reconciliation this script depends on has broken."
                % (r["id"], nano, stored)
            )
        events.append(
            {
                "id": r["id"],
                "turn": r["turn_index"],
                "model": r["model"],
                "agent_id": r["agent_id"],
                "initiator": r["initiator"],
                "endpoint": r["api_endpoint"],
                "effort": r["reasoning_effort"],
                "finish": r["finish_reason"],
                "multiplier": r["request_multiplier"],
                "reasoning": r["reasoning_tokens"] or 0,
                "duration_ms": r["duration_ms"] or 0,
                "ttft_ms": r["time_to_first_token_ms"],
                "at": r["created_at"],
                "ts": parse_ts(r["created_at"]).timestamp(),
                "chans": chans,
                "nano": nano,
            }
        )
    return events


def tok(ev, kind):
    return ev["chans"].get(kind, {}).get("tokens", 0)


def usd(nano):
    return nano / NANO * CENTS_PER_AIU / 100.0


def busy_union(events):
    """Seconds during which at least one request was in flight.

    Sub-agents run beside the main agent, so summing duration_ms double counts.
    """
    iv = sorted((e["ts"] - e["duration_ms"] / 1000.0, e["ts"]) for e in events)
    merged = []
    for a, b in iv:
        if merged and a <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    return sum(b - a for a, b in merged), len(merged)


def active_time(events):
    ts = sorted(e["ts"] for e in events)
    gaps = [ts[i + 1] - ts[i] for i in range(len(ts) - 1)]
    out = []
    for cut in IDLE_CUTOFFS:
        out.append(
            {
                "cutoff_s": cut,
                "active_s": round(sum(g for g in gaps if g <= cut), 1),
                "sittings": sum(1 for g in gaps if g > cut) + 1,
            }
        )
    return out


# ---------------------------------------------------------------------------
# Day-by-day. Three things have to be right here or the table lies quietly.
#
# 1. THE DAY BOUNDARY IS LOCAL, NOT UTC. In this project 19% of requests land
#    between 00:00 and 04:00 UTC, which is the previous evening where the work
#    happened. Splitting on UTC days files a fifth of the work under the wrong
#    date - one day in this run moves by a factor of five. Local days are taken
#    from the PLATFORM's own zone database via astimezone(), not from zoneinfo:
#    zoneinfo needs the tzdata package, which a clean Windows Python does not
#    have, and a build script that dies on a bare interpreter is a landmine.
#    astimezone() also gets daylight saving right, which a fixed offset cannot.
#
# 2. A SITTING STARTS WHEN ITS FIRST REQUEST STARTED, not when that request
#    returned. Otherwise the first inference of every sitting sits outside the
#    engaged window and the person/model split can go negative.
#
# 3. THE MODEL FIGURE IS A UNION, NOT A SUM. Sub-agents run beside the main
#    agent, so adding durations double-counts wall time that only passed once.
# ---------------------------------------------------------------------------

def busy_intervals(events):
    """Merged wall-clock intervals during which at least one request was in flight."""
    iv = sorted((e["ts"] - e["duration_ms"] / 1000.0, e["ts"]) for e in events)
    merged = []
    for a, b in iv:
        if merged and a <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    return [(a, b) for a, b in merged]


def sitting_intervals(events, cutoff):
    """Clusters of requests, split wherever the pause between two exceeds cutoff."""
    ev = sorted(events, key=lambda e: e["ts"])
    groups, cur = [], [ev[0]]
    for prev, nxt in zip(ev, ev[1:]):
        if nxt["ts"] - prev["ts"] > cutoff:
            groups.append(cur)
            cur = [nxt]
        else:
            cur.append(nxt)
    groups.append(cur)
    return merge([
        (min(e["ts"] - e["duration_ms"] / 1000.0 for e in g), g[-1]["ts"])
        for g in groups
    ])


def merge(intervals):
    """Union of a set of intervals.

    LOAD-BEARING, NOT TIDINESS. Two sittings can overlap: a sub-agent request
    that runs for minutes completes after the pause that ended the previous
    sitting, so the next sitting's start - which is when its first request
    STARTED - can precede the previous sitting's end. Summing such a list
    without merging counts the overlap twice, and the error is small enough to
    hide. It showed up here as model hours drifting 12 seconds across idle
    cut-offs they cannot logically depend on at all.
    """
    out = []
    for a, b in sorted(intervals):
        if out and a <= out[-1][1]:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return [(a, b) for a, b in out]


def clip(intervals, lo, hi):
    """The parts of intervals that fall inside [lo, hi), merged."""
    out = []
    for a, b in intervals:
        s, e = max(a, lo), min(b, hi)
        if e > s:
            out.append((s, e))
    return merge(out)


def intersect(xs, ys):
    """Overlap of two interval lists, merged. Both are small; O(n*m) is fine."""
    out = []
    for a0, a1 in xs:
        for b0, b1 in ys:
            s, e = max(a0, b0), min(a1, b1)
            if e > s:
                out.append((s, e))
    return merge(out)


def span(intervals):
    return sum(b - a for a, b in intervals)


def local_day_bounds(ts):
    """Epoch seconds for local midnight either side of the instant at ts."""
    local = dt.datetime.fromtimestamp(ts).astimezone()
    start = local.replace(hour=0, minute=0, second=0, microsecond=0)
    return start.timestamp(), (start + dt.timedelta(days=1)).timestamp()


def daily(events, turns):
    """One row per local calendar day on which a request was issued.

    Within a sitting either a model was working or it was not, so

        engaged = model + person

    holds by construction and the person figure can never come out negative.
    That identity is the whole reason the split is defensible; what it does
    NOT do is prove the person was present. See "person_note" - the residual
    over-counts when somebody walked away mid-sitting and under-counts the
    reading done after a sitting's last request, which is exactly when a
    reader of a research document does it.
    """
    busy = busy_intervals(events)
    union_total = span(busy)
    sits = {c: sitting_intervals(events, c) for c in IDLE_CUTOFFS}

    buckets = {}
    for e in events:
        key = dt.datetime.fromtimestamp(e["ts"]).astimezone().date().isoformat()
        buckets.setdefault(key, []).append(e)

    starts = {}
    for t in turns:
        d = parse_ts(t["started"]).astimezone().date().isoformat()
        starts[d] = starts.get(d, 0) + 1

    rows = []
    for day in sorted(buckets):
        evs = buckets[day]
        lo, hi = local_day_bounds(evs[0]["ts"])
        times = {}
        for c in IDLE_CUTOFFS:
            eng = clip(sits[c], lo, hi)
            mod = intersect(busy, eng)
            e_s, m_s = span(eng), span(mod)
            times[str(c)] = {
                "engaged_s": round(e_s, 1),
                "model_s": round(m_s, 1),
                "person_s": round(max(0.0, e_s - m_s), 1),
                "sittings": len(eng),
            }
        rows.append(
            {
                "date": day,
                "requests": len(evs),
                "turns_started": starts.get(day, 0),
                "nano_aiu": sum(e["nano"] for e in evs),
                "usd": round(usd(sum(e["nano"] for e in evs)), 2),
                "tokens": sum(
                    tok(e, k)
                    for e in evs
                    for k in ("input", "cache_read", "cache_write", "output")
                ),
                "first": dt.datetime.fromtimestamp(evs[0]["ts"]).astimezone().isoformat(),
                "last": dt.datetime.fromtimestamp(evs[-1]["ts"]).astimezone().isoformat(),
                "times": times,
            }
        )

    # Model time cannot depend on how long a pause has to be before it stops
    # counting - it is a union of intervals that were measured. If it moves
    # with the cut-off, the interval arithmetic is double-counting somewhere,
    # which is how the overlapping-sittings bug was found. Assert it rather
    # than hope, and check the total against the figure the rest of the page
    # already publishes.
    for c in IDLE_CUTOFFS:
        got = sum(r["times"][str(c)]["model_s"] for r in rows)
        if abs(got - union_total) > 1.0:
            die(
                "daily model time sums to %.1f s at the %d s cut-off but the "
                "measured union is %.1f s. The interval arithmetic is wrong."
                % (got, c, union_total)
            )
    return rows


def local_zone():
    """What the platform calls the local zone, and its offset now.

    Reported rather than assumed: a day-by-day table is meaningless until the
    reader knows whose midnight was used to cut it.
    """
    now = dt.datetime.now().astimezone()
    off = now.utcoffset() or dt.timedelta(0)
    mins = int(off.total_seconds() // 60)
    return {
        "name": now.tzname(),
        "utc_offset": "%+03d:%02d" % (mins // 60, abs(mins) % 60),
    }


def dates(events):
    """When the research started, and when it was last touched.

    THESE ARE TWO DIFFERENT QUESTIONS AND THEY HAVE DIFFERENT ANSWERS. The
    last request is when a model last ran; the last commit is when the
    published work last changed. A reader asking "is this current" means the
    second. Both are reported because quoting either alone is misleading -
    a session can burn requests without publishing anything, and a commit can
    land long after the reasoning behind it.
    """
    first = parse_ts(events[0]["at"]).astimezone()
    last = parse_ts(events[-1]["at"]).astimezone()
    commit = git("log", "-1", "--pretty=format:%aI")
    first_commit = git("log", "--reverse", "--pretty=format:%aI")
    first_commit = first_commit.splitlines()[0] if first_commit else ""
    return {
        "started": first.isoformat(),
        "started_source": "first request issued in this session",
        "last_request": last.isoformat(),
        "last_commit": commit,
        "first_commit": first_commit,
        "calendar_days": (last.date() - first.date()).days + 1,
        "active_days": len({
            dt.datetime.fromtimestamp(e["ts"]).astimezone().date() for e in events
        }),
        "generated": dt.datetime.now().astimezone().isoformat(),
    }


def read_contributions(primary_sid):
    """Load usage exported from other machines, if any are present.

    The store is per-machine. This project was also worked on from a second
    machine, in four sibling repositories, and no API exists to ask that
    machine for its numbers - the store is a local SQLite file. So
    `export_session.py` runs over there and drops JSON here.

    A contribution is trusted only as far as it checks out: the format and
    version must match, and the per-request costs must sum to the stated
    total. A file that fails either is refused rather than quietly halved.
    """
    d = os.path.join(HERE, "contrib")
    if not os.path.isdir(d):
        return []
    out = []
    for name in sorted(os.listdir(d)):
        if not name.endswith(".json"):
            continue
        path = os.path.join(d, name)
        with open(path, encoding="utf-8") as fh:
            c = json.load(fh)
        if c.get("format") != "mbd-usage-contribution":
            die("%s is not a usage contribution file" % name)
        if c.get("version") != 1:
            die("%s is contribution version %s; this generator reads 1"
                % (name, c.get("version")))
        if c.get("session_id") == primary_sid:
            # The primary session is read from the live store. Counting an
            # export of it as well would double every figure on the page.
            print("  skipping %s: it is this session, already counted" % name)
            continue
        cols = c["columns"]
        idx = {k: cols.index(k) for k in cols}
        events, tot = [], 0
        for r in c["requests"]:
            g = lambda k: r[idx[k]] if k in idx else 0
            nano = r[idx["nano"]]
            tot += nano
            ts = r[idx["ts"]]
            events.append({
                "ts": ts,
                "at": dt.datetime.fromtimestamp(ts, dt.timezone.utc)
                        .strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "duration_ms": r[idx["duration_ms"]],
                "model": r[idx["model"]],
                "turn": "%s:%s" % (c["session_id"][:8], r[idx["turn"]]),
                "agent_id": "sub" if g("sub") else None,
                "initiator": "imported",
                "effort": None,
                "multiplier": None,
                "reasoning": g("reasoning"),
                "nano": nano,
                "chans": {k: {"tokens": g(k)} for k in
                          ("input", "cache_read", "cache_write", "output")
                          if g(k)},
            })
        stated = c["totals"]["nano_aiu"]
        if tot != stated:
            die("%s: its %d requests sum to %d nano-AIU but the file states %d. "
                "Truncated or edited; refusing to merge it."
                % (name, len(events), tot, stated))
        if len(events) != c["totals"]["requests"]:
            die("%s: %d request rows but the file states %d"
                % (name, len(events), c["totals"]["requests"]))
        events.sort(key=lambda e: e["ts"])
        out.append({"meta": c, "events": events, "file": name})
    return out


def fleet(primary_label, primary_meta, primary_events, contribs):
    """Everything spent on this project, across every machine that worked on it.

    ONE RULE GOVERNS THIS WHOLE BLOCK: money is additive and a person is not.

    Requests, tokens and cost can simply be added - two machines spending at
    once spend twice as much. Wall-clock time cannot. If both machines were
    generating at 14:32, then two models really were working, so model WORK
    seconds add up; but only one minute of clock passed, so model WALL time is
    a union. And there is only one person, who cannot be at two keyboards at
    once, so engaged time is a union too and person time must be computed from
    the merged clock rather than summed per machine.

    Summing person time across machines is the error this function exists to
    avoid. It would inflate the one column on the page that is already the
    weakest, and it would do it invisibly.
    """
    if not contribs:
        return None

    sources = [{"label": primary_label, "meta": primary_meta, "events": primary_events,
                "primary": True}]
    for c in contribs:
        sources.append({
            "label": c["meta"].get("project") or c["file"],
            "meta": {"machine": c["meta"].get("machine"),
                     "repository": c["meta"].get("repository"),
                     "session": c["meta"].get("session_id"),
                     "file": c["file"]},
            "events": c["events"],
            "primary": False,
        })

    rows, all_events, all_busy = [], [], []
    for s in sources:
        evs = s["events"]
        busy = busy_intervals(evs)
        nano = sum(e["nano"] for e in evs)
        rows.append({
            "project": s["label"],
            "machine": s["meta"].get("machine") or "this machine",
            "primary": s["primary"],
            "requests": len(evs),
            "turns": len({e["turn"] for e in evs if e["turn"] is not None}),
            "subagent_requests": sum(1 for e in evs if e.get("agent_id")),
            "nano_aiu": nano,
            "usd": round(usd(nano), 2),
            "tokens": sum(tok(e, k) for e in evs
                          for k in ("input", "cache_read", "cache_write", "output")),
            "model_s": round(span(busy), 1),
            "first": dt.datetime.fromtimestamp(evs[0]["ts"]).astimezone().isoformat(),
            "last": dt.datetime.fromtimestamp(evs[-1]["ts"]).astimezone().isoformat(),
            "days": len({dt.datetime.fromtimestamp(e["ts"]).astimezone().date()
                         for e in evs}),
            "models": sorted({e["model"] for e in evs}),
        })
        all_events.extend(evs)
        all_busy.extend(busy)

    all_events.sort(key=lambda e: e["ts"])
    union_busy = merge(all_busy)
    model_wall = span(union_busy)
    model_work = sum(r["model_s"] for r in rows)

    times = {}
    for c in IDLE_CUTOFFS:
        sits = merge([iv for s in sources
                      for iv in sitting_intervals(s["events"], c)])
        eng = span(sits)
        mod = span(intersect(union_busy, sits))
        times[str(c)] = {
            "engaged_s": round(eng, 1),
            "model_s": round(mod, 1),
            "person_s": round(max(0.0, eng - mod), 1),
            "sittings": len(sits),
        }

    total_nano = sum(r["nano_aiu"] for r in rows)
    return {
        "sources": sorted(rows, key=lambda r: -r["nano_aiu"]),
        "totals": {
            "projects": len(rows),
            "machines": len({r["machine"] for r in rows}),
            "requests": sum(r["requests"] for r in rows),
            "turns": sum(r["turns"] for r in rows),
            "nano_aiu": total_nano,
            "usd": round(usd(total_nano), 2),
            "tokens": sum(r["tokens"] for r in rows),
            "days": len({dt.datetime.fromtimestamp(e["ts"]).astimezone().date()
                         for e in all_events}),
        },
        "time": {
            "model_work_s": round(model_work, 1),
            "model_wall_s": round(model_wall, 1),
            "concurrent_s": round(model_work - model_wall, 1),
            "span_s": round(all_events[-1]["ts"] - all_events[0]["ts"], 1),
            "cutoffs": list(IDLE_CUTOFFS),
            "default_cutoff_s": 300,
            "times": times,
        },
        "days": daily(all_events, [{"started": e["at"]} for e in all_events
                                   if e.get("turn") is not None]),
        "note": (
            "Money is additive and a person is not. Requests, tokens and cost "
            "are summed across machines. Wall-clock time is not: model time is "
            "the union of intervals across every machine, and engaged time is "
            "the union of sittings, because one person cannot be at two "
            "keyboards at once. Summing person-hours per machine would inflate "
            "the weakest column on this page and do it invisibly."
        ),
    }


def siblings():
    """The sibling repositories whose usage this store cannot see.

    Four 3D repositories are part of this project and were worked on from a
    second machine. Their cost is real and this dashboard cannot reach it: the
    usage store is a local SQLite file, per machine, with no API to query.

    Rather than let that silently shrink the published total, the repositories
    are named, what CAN be seen from here is fetched (commits and dates, which
    live on GitHub), and the part that cannot is labelled as missing. A stated
    hole is evidence; an unstated one is an understatement.

    Network failure is not fatal - the names and the caveat still publish.
    """
    names = [
        "dumbo-district-3d",
        "manhattan-bridge-3d",
        "brooklyn-bridge-3d",
        "williamsburg-bridge-3d",
    ]
    owner = "Ethical-Tech-CoLab"
    rows = []
    for n in names:
        row = {"repo": "%s/%s" % (owner, n), "name": n, "commits": None,
               "first_commit": None, "last_commit": None, "reachable": False}
        try:
            raw = subprocess.run(
                ["gh", "api", "repos/%s/%s/commits?per_page=100" % (owner, n)],
                capture_output=True, text=True, timeout=30,
            )
            if raw.returncode == 0:
                cs = json.loads(raw.stdout)
                if isinstance(cs, list) and cs:
                    dates = sorted(c["commit"]["author"]["date"] for c in cs)
                    row.update(commits=len(cs), first_commit=dates[0],
                               last_commit=dates[-1], reachable=True)
        except Exception:
            pass
        rows.append(row)
    return {
        "rows": rows,
        "fetched": dt.datetime.now().astimezone().isoformat(),
        "why": (
            "These repositories are part of the same project and were worked "
            "on from a second machine. The usage store is a local SQLite file "
            "with no API to query, so their requests, tokens and cost are not "
            "in any figure on this page. Commit counts come from GitHub, which "
            "is why they are visible when the spend is not. To fold them in, "
            "run usage/export_session.py on that machine and drop the files "
            "into usage/contrib/."
        ),
        "caveat": (
            "Every total on this page is therefore a FLOOR for the project as "
            "a whole, and an exact figure only for the repository it was "
            "generated in."
        ),
    }


def group(events, key, label="key"):
    out = {}
    for e in events:
        k = e[key]
        d = out.setdefault(
            k,
            {
                label: k,
                "requests": 0,
                "nano_aiu": 0,
                "duration_ms": 0,
                "reasoning": 0,
                "input": 0,
                "cache_read": 0,
                "cache_write": 0,
                "output": 0,
            },
        )
        d["requests"] += 1
        d["nano_aiu"] += e["nano"]
        d["duration_ms"] += e["duration_ms"]
        d["reasoning"] += e["reasoning"]
        for c in ("input", "cache_read", "cache_write", "output"):
            d[c] += tok(e, c)
    for d in out.values():
        d["usd"] = round(usd(d["nano_aiu"]), 4)
    return sorted(out.values(), key=lambda d: -d["nano_aiu"])


def counterfactual(events):
    """What the same traffic would have cost with no prompt cache.

    Every cached token is charged at the model's own full input price instead
    of its cache-read or cache-write price. Output is untouched.
    """
    price_in, real, naive = {}, 0, 0
    for e in events:
        c = e["chans"]
        if "input" in c:
            price_in[e["model"]] = c["input"]["price_nano_per_token"]
    missing = sorted({e["model"] for e in events} - set(price_in))
    for e in events:
        real += e["nano"]
        p = price_in.get(e["model"])
        for kind, ch in e["chans"].items():
            if kind == "output" or p is None:
                naive += ch["nano_aiu"]
            else:
                naive += ch["tokens"] * p
    return {
        "actual_usd": round(usd(real), 2),
        "uncached_usd": round(usd(naive), 2),
        "ratio": round(naive / real, 3) if real else None,
        "models_without_an_input_price_sample": missing,
    }


LABEL_SKIP = re.compile(r"^\s*<(skill-context|system|environment)", re.I)


def turn_labels(con, sid, limit=96):
    out = {}
    try:
        rows = con.execute(
            "SELECT turn_index, user_message FROM turns WHERE session_id=?", (sid,)
        ).fetchall()
    except sqlite3.Error:
        return out
    for r in rows:
        msg = (r["user_message"] or "").strip()
        if not msg or LABEL_SKIP.match(msg):
            out[r["turn_index"]] = "(tool or skill context, not a typed request)"
            continue
        one = " ".join(msg.split())
        out[r["turn_index"]] = one[:limit] + ("..." if len(one) > limit else "")
    return out


def git(*args):
    try:
        return subprocess.run(
            ["git"] + list(args), cwd=ROOT, capture_output=True, text=True, timeout=60
        ).stdout.strip()
    except Exception:
        return ""


def outputs():
    """The other half of the ledger: what the project has to show for it.

    Volume is not value. The dashboard says so; this only counts.
    """
    commits = []
    log = git("log", "--pretty=format:%h|%aI|%s")
    for line in [l for l in log.splitlines() if l.strip()]:
        h, iso, subj = line.split("|", 2)
        commits.append({"sha": h, "at": iso, "subject": subj})
    ins = dele = 0
    for line in git("log", "--pretty=tformat:", "--numstat").splitlines():
        p = line.split("\t")
        if len(p) >= 3 and p[0].isdigit() and p[1].isdigit():
            ins += int(p[0])
            dele += int(p[1])
    files, by_ext, total_bytes, words = git("ls-files").splitlines(), {}, 0, 0
    for f in files:
        ext = os.path.splitext(f)[1].lower() or "(none)"
        by_ext[ext] = by_ext.get(ext, 0) + 1
        p = os.path.join(ROOT, f)
        if os.path.exists(p):
            total_bytes += os.path.getsize(p)
            if ext == ".md":
                try:
                    with open(p, encoding="utf-8") as fh:
                        words += len(fh.read().split())
                except OSError:
                    pass
    return {
        "commits": list(reversed(commits)),
        "commit_count": len(commits),
        "insertions": ins,
        "deletions": dele,
        "tracked_files": len(files),
        "files_by_ext": dict(sorted(by_ext.items(), key=lambda kv: -kv[1])),
        "bytes": total_bytes,
        "markdown_words": words,
    }


def offered_models(used):
    """How many models the client offered, against how many were used.

    models.json is written beside the CLI debug log. Absent it, we say so
    rather than guessing a roster.
    """
    base = os.path.join(
        os.environ.get("APPDATA", ""), "Code", "User", "workspaceStorage"
    )
    best = None
    for dirpath, _dirs, names in os.walk(base) if os.path.isdir(base) else []:
        if "models.json" in names:
            p = os.path.join(dirpath, "models.json")
            if best is None or os.path.getmtime(p) > os.path.getmtime(best):
                best = p
    if not best:
        return {"offered": None, "used": sorted(used), "source": None}
    try:
        with open(best, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        return {"offered": None, "used": sorted(used), "source": None}
    roster = []
    for m in data:
        tp = (m.get("billing") or {}).get("token_prices", {}).get("default") or {}
        roster.append(
            {
                "id": m.get("id"),
                "vendor": m.get("vendor"),
                "input_price": tp.get("input_price"),
                "output_price": tp.get("output_price"),
                "picker": m.get("model_picker_enabled", False),
                "used": m.get("id") in used,
            }
        )
    return {
        "offered": len(roster),
        "selectable": sum(1 for r in roster if r["picker"]),
        "used": sorted(used),
        "roster": sorted(roster, key=lambda r: -(r["input_price"] or 0)),
        "source": "models.json written by the client",
    }


def build(args):
    con, tmp = open_snapshot(args.db)
    try:
        sess = pick_session(con, args)
        sid = sess["id"]
        events = load_events(con, sid)
        labels = turn_labels(con, sid)
    finally:
        con.close()
        shutil.rmtree(tmp, ignore_errors=True)

    contribs = read_contributions(sid)

    chans = {}
    for e in events:
        for kind, ch in e["chans"].items():
            k = (e["model"], kind, ch["price_nano_per_token"])
            d = chans.setdefault(
                k,
                {
                    "model": e["model"],
                    "type": kind,
                    "price_nano_per_token": ch["price_nano_per_token"],
                    "tokens": 0,
                    "nano_aiu": 0,
                },
            )
            d["tokens"] += ch["tokens"]
            d["nano_aiu"] += ch["nano_aiu"]
    channels = sorted(chans.values(), key=lambda d: -d["nano_aiu"])
    for c in channels:
        c["usd"] = round(usd(c["nano_aiu"]), 4)
        c["usd_per_1m"] = round(c["price_nano_per_token"] * 1e6 / NANO / 100.0, 4)

    total_nano = sum(e["nano"] for e in events)
    ts = sorted(e["ts"] for e in events)
    union_s, blocks = busy_union(events)

    turns = []
    for t in sorted({e["turn"] for e in events}, key=lambda x: (x is None, x)):
        sub = [e for e in events if e["turn"] == t]
        turns.append(
            {
                "index": t,
                "label": labels.get(t, ""),
                "started": min(e["at"] for e in sub),
                "requests": len(sub),
                "nano_aiu": sum(e["nano"] for e in sub),
                "usd": round(usd(sum(e["nano"] for e in sub)), 3),
                "duration_ms": sum(e["duration_ms"] for e in sub),
                "reasoning": sum(e["reasoning"] for e in sub),
                "input": sum(tok(e, "input") for e in sub),
                "cache_read": sum(tok(e, "cache_read") for e in sub),
                "cache_write": sum(tok(e, "cache_write") for e in sub),
                "output": sum(tok(e, "output") for e in sub),
                "subagent_requests": sum(1 for e in sub if e["agent_id"]),
            }
        )

    agents = [a for a in group(events, "agent_id", "agent") if a["agent"]]
    for a in agents:
        first = min(e["at"] for e in events if e["agent_id"] == a["agent"])
        a["started"] = first
        a["turn"] = next(e["turn"] for e in events if e["agent_id"] == a["agent"])
        a["models"] = sorted({e["model"] for e in events if e["agent_id"] == a["agent"]})

    data = {
        "schema": "copilot-usage/1",
        "generated_at": dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "generator": "usage/build_usage_data.py",
        "project": {
            "name": os.path.basename(ROOT),
            "cwd": sess["cwd"],
            "repository": sess["repository"],
            "branch": sess["branch"],
        },
        "session": {
            "id": sid,
            "created_at": sess["created_at"],
            "updated_at": sess["updated_at"],
        },
        "units": {
            "aiu_is": "one US cent",
            "nano_aiu_per_aiu": NANO,
            "note": "AIU prices in the store match the per-model prices the client "
            "publishes in models.json, which in turn match three vendor list "
            "prices to the cent. See usage/README.md.",
        },
        "totals": {
            "requests": len(events),
            "turns": len({e["turn"] for e in events}),
            "models": len({e["model"] for e in events}),
            "subagents": len({e["agent_id"] for e in events if e["agent_id"]}),
            "subagent_requests": sum(1 for e in events if e["agent_id"]),
            "nano_aiu": total_nano,
            "aiu": round(total_nano / NANO, 3),
            "usd": round(usd(total_nano), 2),
            "tokens": {
                "input": sum(tok(e, "input") for e in events),
                "cache_read": sum(tok(e, "cache_read") for e in events),
                "cache_write": sum(tok(e, "cache_write") for e in events),
                "output": sum(tok(e, "output") for e in events),
                "reasoning": sum(e["reasoning"] for e in events),
            },
            "premium_requests": sum(
                1 for e in events if e["initiator"] == "user"
            ),
            "multipliers": sorted({e["multiplier"] for e in events if e["multiplier"]}),
        },
        "time": {
            "first_request": events[0]["at"],
            "last_request": events[-1]["at"],
            "wall_span_s": round(ts[-1] - ts[0], 1),
            "inference_sum_s": round(sum(e["duration_ms"] for e in events) / 1000.0, 1),
            "inference_union_s": round(union_s, 1),
            "busy_blocks": blocks,
            "active": active_time(events),
        },
        "dates": dates(events),        "days": {
            "zone": local_zone(),
            "cutoffs": list(IDLE_CUTOFFS),
            "default_cutoff_s": 300,
            "person_note": (
                "Person time is a RESIDUAL, not a measurement. No keystroke or "
                "focus telemetry exists in this store. Within a sitting either "
                "a model was working or it was not, so engaged minus model is "
                "the time somebody could have been reading, typing or thinking "
                "- and it counts the same if they walked away. It also misses "
                "the reading done after a sitting's last request, so it errs in "
                "both directions rather than bounding the truth on one side."
            ),
            "rows": daily(events, turns),
        },
        "channels": channels,
        "models": group(events, "model", "model"),
        "initiators": group(events, "initiator", "initiator"),
        "efforts": group(events, "effort", "effort"),
        "agents": agents,
        "turns": turns,
        "counterfactual": counterfactual(events),
        "fleet": fleet(
            (sess["repository"] or os.path.basename(str(sess["cwd"]).rstrip("\\/"))
             or "this project").split("/")[-1],
            {"machine": None, "repository": sess["repository"], "session": sid},
            events,
            contribs,
        ),        "energy": energy(len(events)),
        "siblings": siblings(),        "energy": energy(len(events)),
        "catalogue": offered_models({e["model"] for e in events}),
        "outputs": outputs(),
        "not_measured": [
            ["Energy", "No joules are recorded anywhere in this data. The "
             "energy panel applies a published per-query figure to a request "
             "count. It is an estimate stapled to a fact, and the two ends of "
             "its own bracket differ by a factor of 24."],
            ["Water and embodied carbon", "Downstream of energy, and not "
             "derivable from it without a site-specific PUE and WUE."],
            ["What was actually paid", "The store prices tokens. A Copilot "
             "subscription bills premium requests. The two are not the same "
             "number and this data cannot bridge them."],
            ["Human time", "No keystroke or focus telemetry exists here. The "
             "active-time figures are inferred from gaps between requests."],
            ["Value", "Nothing here measures whether any of the output was "
             "worth having."],
        ],
    }
    return data


def inject(path, data):
    """Rewrite the payload between the /*USAGE*/ markers, leaving all else alone."""
    if not os.path.exists(path):
        print("  no dashboard at %s, skipping injection" % path)
        return
    with open(path, encoding="utf-8") as fh:
        html = fh.read()
    marker = "/*USAGE*/"
    if html.count(marker) != 2:
        die("expected exactly two %s markers in %s, found %d"
            % (marker, os.path.basename(path), html.count(marker)))
    a = html.index(marker) + len(marker)
    b = html.index(marker, a)
    payload = json.dumps(data, separators=(",", ":"), ensure_ascii=True)
    out = html[:a] + payload + html[b:]
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(out)
    print("  injected %d bytes into %s" % (len(payload), os.path.basename(path)))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", default=default_db())
    ap.add_argument("--session")
    ap.add_argument("--cwd")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--out", default=os.path.join(HERE, "usage-data.json"))
    ap.add_argument("--dashboard", default=os.path.join(HERE, "usage-dashboard.html"))
    ap.add_argument("--no-inject", action="store_true")
    args = ap.parse_args()

    data = build(args)
    with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, indent=1)
        fh.write("\n")
    t = data["totals"]
    print("session %s" % data["session"]["id"])
    print("  %d requests over %d turns, %d models, %d sub-agents"
          % (t["requests"], t["turns"], t["models"], t["subagents"]))
    print("  %s AIU = $%s at list price" % (t["aiu"], t["usd"]))
    print("  tokens: %d cache-read, %d cache-write, %d output, %d fresh input"
          % (t["tokens"]["cache_read"], t["tokens"]["cache_write"],
             t["tokens"]["output"], t["tokens"]["input"]))
    print("  inference %.2f h summed, %.2f h union; wall span %.2f h"
          % (data["time"]["inference_sum_s"] / 3600,
             data["time"]["inference_union_s"] / 3600,
             data["time"]["wall_span_s"] / 3600))
    print("  wrote %s" % os.path.relpath(args.out, ROOT))
    if not args.no_inject:
        inject(args.dashboard, data)


if __name__ == "__main__":
    main()
