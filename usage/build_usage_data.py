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
        "channels": channels,
        "models": group(events, "model", "model"),
        "initiators": group(events, "initiator", "initiator"),
        "efforts": group(events, "effort", "effort"),
        "agents": agents,
        "turns": turns,
        "counterfactual": counterfactual(events),
        "energy": energy(len(events)),
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
