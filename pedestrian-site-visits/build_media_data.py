"""Read the captured site-visit media and extract what can be measured from it.

Runs against the files in this directory and writes `media-data.json`, which
`media.html` renders. Nothing here is hand-typed; if a number appears on the
page it came out of a file.

WHAT THIS CAN AND CANNOT DO
---------------------------
The recordings are from a Samsung Galaxy S23+ with automatic gain control that
cannot be disabled in the stock camera app. That has one consequence that
governs every acoustic number below:

    ABSOLUTE LEVEL IS NOT RECOVERABLE. Nothing here is a decibel.

What survives an uncalibrated, auto-gained chain is *timing* - when a level
rises, how long it stays up, and when it falls. That is the only acoustic
quantity this script computes, and every level it prints is dBFS (decibels
relative to digital full scale), which is a property of the recording and not
of the air. `FIELD-CAPTURE-PROTOCOL.md` Part 2 sets out why timing survives
and level does not.

AGC ALSO DISTORTS TIMING, in a specific and known direction: it pulls loud
passages down and pushes quiet passages up, which COMPRESSES the apparent
contrast between a train and its background. An event boundary found in an
auto-gained recording is therefore biased *late* at onset and *early* at
offset - the measured durations below are a floor, not an estimate.

TWO SILENT FAILURES GUARDED HERE
--------------------------------
1. Android names a video file at recording START and writes `creation_time`
   at file CLOSE. The two differ by the clip duration plus a finalisation
   delay. Taking either one as "the time of capture" without saying which
   misplaces every clip on a timeline by up to a minute - which is most of a
   headway. Both are recorded, and the consistency between them is asserted.

2. `ffmpeg -af astats` and similar report levels per-frame in a way that
   depends on frame size. Windowing is done here explicitly, in numpy, at a
   stated window and hop, so the numbers do not move if a codec changes.

3. A QUIET SITE AND AN OBSTRUCTED MICROPHONE PRODUCE THE SAME MONO ENVELOPE.
   Mixing to mono before looking destroys the only evidence that separates
   them, and the mono result looks entirely reasonable either way. The two
   channels are kept and compared, because a hand covers one microphone port
   and not both equally, while a quiet site moves both channels down together.

   An obstruction that never lifts defeats that test too - it moves the clip's
   own baseline with it - so it is looked for a second way, BETWEEN clips, on
   three indicators a hand moves in known directions and quiet does not:
   floor up, dynamic range down, inter-channel correlation down.

   This was written because the operator reported, after the first analysis
   run, possibly covering the microphone during one recording. The test is
   therefore checking a recollection rather than generating one, and it was
   free to come out against it. It did not: all three indicators picked the
   same clip unanimously, and that clip is now excluded from every statistic
   rather than caveated after the fact.
"""

import hashlib
import io
import json
import math
import os
import re
import subprocess
import sys
import wave

import numpy as np

try:
    import imageio_ffmpeg
    FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:                                        # pragma: no cover
    FFMPEG = "ffmpeg"

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# Analysis window. 50 ms with 25 ms hop resolves a train onset to well inside
# the human "did it just get loud" threshold while still averaging over enough
# samples that a single wind gust does not register as an event.
WIN_S = 0.050
HOP_S = 0.025

# An event is a run of windows above the floor + THRESH_DB. The floor is the
# clip's own 10th-percentile level, so the threshold is relative to that clip's
# own background and no cross-clip calibration is implied.
THRESH_DB = 6.0
MIN_EVENT_S = 1.5      # shorter than this is a car door, a voice, a footfall
MIN_GAP_S = 1.5        # two peaks closer than this are one event

# Hand-recorded from the capture session. Anything the file itself can supply
# is read from the file; only what a person had to write down appears here.
SESSIONS = {
    "20260803_190055.jpg": ("2026-08-03 19:00:55", "still",
                            "Under the bridge, evening"),
    "20260803_190152.jpg": ("2026-08-03 19:01:52", "still",
                            "Under the bridge, evening"),
    "canyon-buildings-20260804_115319.mp4": ("2026-08-04 11:53:19", "video",
                                             "The canyon, walking"),
    "canyon-buildings2-20260804_115505.mp4": ("2026-08-04 11:55:05", "video",
                                              "The canyon, continued"),
    "grassy-knoll-20260804_115626.mp4": ("2026-08-04 11:56:26", "video",
                                         "Grassy knoll, south of the bridge"),
    "grassy-knoll-20260804_120225.jpg": ("2026-08-04 12:02:25", "still",
                                         "Grassy knoll, south of the bridge"),
    "clock-screenshot_20260804_130719_Clock.jpg": ("2026-08-04 13:07:19",
                                                   "screenshot",
                                                   "Stopwatch, paused"),
    "Timer Lap start time for train noise-accumulated time.txt":
        ("2026-08-04 13:07:19", "data", "Stopwatch lap export"),
}


# Field notes from the operator, recorded verbatim and AFTER the first analysis
# run. They are recollection, not measurement, and they are rated as such - but
# a recollection that can be TESTED against the recording is worth far more
# than one that cannot, and both of these can be. `channel_asymmetry()` runs
# those tests and is free to disagree with the person who made the recording.
#
# Why this matters more than it looks: an obstructed microphone and a quiet
# site produce the same mono envelope. Without the note nobody would have
# thought to look, and the null in the grassy-knoll clip would have been read
# as a property of the grassy knoll.
OPERATOR_NOTES = {
    "grassy-knoll-20260804_115626.mp4": [
        {"claim": "I may have had my hand over the microphone for the drop "
                  "out period.",
         "rating": 2, "status": "OPERATOR RECOLLECTION",
         "tested_by": "sustained divergence between the two channels"},
        {"claim": "Turned phone upside down at some point.",
         "rating": 2, "status": "OPERATOR RECOLLECTION",
         "tested_by": "a sustained sign change in the channel difference"},
    ],
}


# Statements of INTENT from the operator, recorded verbatim. These are not
# recollections that can be tested against a recording - they are the reason
# each capture exists, and they are decisive because a measurement can only be
# read for the purpose it was taken for.
#
# They arrived after the first analysis run and they invalidated part of it.
# That is the correct order of events, not a failure of it: an analyst who
# never asks what a capture was FOR will happily compute a precise number from
# a file that cannot carry one.
CAPTURE_INTENT = [
    {"subject": "the stopwatch",
     "claim": "The stopwatch is an independent sample. There is no correlation "
              "between it and any video or audio also supplied.",
     "rating": 5, "status": "OPERATOR STATEMENT OF INTENT",
     "consequence": "No quantity derived from the stopwatch may be compared "
                    "with any quantity derived from the audio. The file "
                    "timestamps agree: the last video ends at 11:56:36 and "
                    "the stopwatch does not start until 12:59:00."},
    {"subject": "the stopwatch",
     "claim": "It is somewhat imprecise because a human operator decided when "
              "to start and stop the stopwatch. It was an indicator that there "
              "is a very small amount of time between noise from the train "
              "tracks. I will redo this with better documentation.",
     "rating": 5, "status": "OPERATOR STATEMENT OF INTENT",
     "consequence": "The stopwatch is an indicator, not an instrument. Its "
                    "own author has scheduled its replacement."},
    {"subject": "the video",
     "claim": "The video was primarily used to show the buildings that create "
              "an echo chamber around the bridge near the water. That was the "
              "main value of them. It was not to be used for audio precision.",
     "rating": 5, "status": "OPERATOR STATEMENT OF INTENT",
     "consequence": "The video is a VISUAL record of the canyon geometry. Its "
                    "audio track is a by-product. It may be used to establish "
                    "that the recording chain misbehaved; it may not be used "
                    "to characterise the acoustic environment."},
    {"subject": "what comes next",
     "claim": "Better audio will be captured later this week with a microphone "
              "shield and an audio meter.",
     "rating": 5, "status": "OPERATOR STATEMENT OF INTENT",
     "consequence": "The by-product audio is superseded before anything was "
                    "built on it. That is the reason to demote it now rather "
                    "than defend it."},
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def probe(path):
    """Pull container metadata out of ffmpeg's stderr banner."""
    r = subprocess.run([FFMPEG, "-hide_banner", "-i", path],
                       capture_output=True, text=True, errors="replace")
    txt = r.stderr
    out = {}
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", txt)
    if m:
        out["duration_s"] = (int(m.group(1)) * 3600 + int(m.group(2)) * 60
                             + float(m.group(3)))
    m = re.search(r"creation_time\s*:\s*(\S+)", txt)
    if m:
        out["creation_time"] = m.group(1)
    m = re.search(r"location\s*:\s*([+-][\d.]+)([+-][\d.]+)", txt)
    if m:
        out["lat"] = float(m.group(1))
        out["lon"] = float(m.group(2))
    m = re.search(r"Video: (\w+).*?, (\d+)x(\d+)", txt)
    if m:
        out["video_codec"] = m.group(1)
        out["width"] = int(m.group(2))
        out["height"] = int(m.group(3))
    m = re.search(r"Audio: (\w+).*?, (\d+) Hz, (\w+)", txt)
    if m:
        out["audio_codec"] = m.group(1)
        out["sample_rate"] = int(m.group(2))
        out["channels"] = m.group(3)
    m = re.search(r"com\.android\.version\s*:\s*(\S+)", txt)
    if m:
        out["android_version"] = m.group(1)
    return out


def exif(path):
    """GPS and capture time from a JPEG, using Pillow only."""
    try:
        from PIL import Image, ExifTags
    except ImportError:                                  # pragma: no cover
        return {}
    out = {}
    try:
        with Image.open(path) as im:
            out["width"], out["height"] = im.size
            raw = im.getexif()
            if not raw:
                return out
            tags = {ExifTags.TAGS.get(k, k): v for k, v in raw.items()}
            for key in ("DateTimeOriginal", "DateTime"):
                if tags.get(key):
                    out["exif_time"] = str(tags[key])
                    break
            if tags.get("Model"):
                out["model"] = str(tags["Model"]).strip()
            gps = raw.get_ifd(0x8825)
            if gps:
                def dms(v):
                    return float(v[0]) + float(v[1]) / 60 + float(v[2]) / 3600
                if 2 in gps and 4 in gps:
                    lat, lon = dms(gps[2]), dms(gps[4])
                    if str(gps.get(1, "N")).upper().startswith("S"):
                        lat = -lat
                    if str(gps.get(3, "E")).upper().startswith("W"):
                        lon = -lon
                    out["lat"], out["lon"] = round(lat, 6), round(lon, 6)
    except Exception as exc:
        out["exif_error"] = str(exc)
    return out


def decode_audio(path, sr=16000, stereo=False):
    """Decode a clip's audio to float32 at `sr`, mono or per-channel.

    16 kHz is deliberate. Rail rolling noise and wheel squeal both sit well
    below 8 kHz, so nothing acoustically relevant is lost, and the array stays
    small enough to keep the whole analysis in memory.

    The stereo path exists because the two channels are the only evidence that
    can distinguish a quiet SITE from an obstructed MICROPHONE. Mixing to mono
    first destroys it, and the mono result looks entirely reasonable either
    way - which is what makes the mistake worth guarding.
    """
    ac = "2" if stereo else "1"
    cmd = [FFMPEG, "-hide_banner", "-loglevel", "error", "-i", path,
           "-vn", "-ac", ac, "-ar", str(sr), "-f", "wav", "-"]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0 or not r.stdout:
        raise SystemExit("audio decode failed for %s: %s"
                         % (path, r.stderr.decode("utf-8", "replace")[:400]))
    with wave.open(io.BytesIO(r.stdout), "rb") as w:
        frames = w.readframes(w.getnframes())
        width = w.getsampwidth()
        nch = w.getnchannels()
    if width != 2:
        raise SystemExit("expected 16-bit PCM from ffmpeg, got %d bytes" % width)
    a = np.frombuffer(frames, dtype="<i2").astype(np.float32) / 32768.0
    if stereo:
        if nch != 2:
            raise SystemExit("asked for stereo, ffmpeg gave %d channels" % nch)
        a = a.reshape(-1, 2)
        return a[:, 0].copy(), a[:, 1].copy(), sr
    return a, sr


def channel_asymmetry(path):
    """Look for microphone obstruction and for the phone being turned over.

    THE OPERATOR REPORTED BOTH, AFTER THE ANALYSIS WAS FIRST RUN. That order
    matters: this test was written to check a recollection, not to produce one,
    and it can come out against the recollection.

    Two different artefacts, two different signatures, and neither is acoustic:

      OBSTRUCTION. A hand covers one microphone port, not both equally. That
      drives the two channels apart and holds them apart for as long as the
      hand is there. A quiet site moves both channels DOWN TOGETHER, so the
      difference stays near zero. The signature is a sustained excursion in
      |L - R|, not in the level.

      INVERSION. Turning the phone over swaps which physical microphone feeds
      which channel. The level is unaffected. What changes is the SIGN of
      (L - R), which flips and then stays flipped. A single sustained sign
      change partway through a clip is the signature; noise crossing zero
      repeatedly is not.

    Neither test can prove the cause. Both can show whether the recording is
    consistent with a claim about the site, and a clip failing either one
    cannot carry an acoustic conclusion whatever the cause turns out to be.
    """
    L, R, sr = decode_audio(path, stereo=True)
    n = min(len(L), len(R))
    L, R = L[:n], R[:n]
    _, dbl = envelope(L, sr)
    _, dbr = envelope(R, sr)
    m = min(len(dbl), len(dbr))
    dbl, dbr = dbl[:m], dbr[:m]
    if m < 8:
        return None
    diff = dbl - dbr

    # Obstruction. Judge the excursion against the clip's own quiet baseline
    # rather than an absolute threshold, since channel trim varies by handset.
    base = float(np.median(diff))
    dev = np.abs(diff - base)
    spread = float(np.percentile(dev, 50)) or 1e-6
    # Sustained means at least a second, not a single window.
    run_min = max(1, int(1.0 / HOP_S))
    hot = dev > max(3.0, 4.0 * spread)
    runs, i = [], 0
    while i < m:
        if hot[i]:
            j = i
            while j < m and hot[j]:
                j += 1
            if j - i >= run_min:
                runs.append({"start_s": round(i * HOP_S, 2),
                             "end_s": round(j * HOP_S, 2),
                             "dur_s": round((j - i) * HOP_S, 2),
                             "peak_db": round(float(dev[i:j].max()), 1)})
            i = j
        else:
            i += 1

    # Inversion. Compare the first and last thirds; a genuine flip separates
    # them, while noise about zero does not.
    third = max(2, m // 3)
    head, tail = float(np.median(diff[:third])), float(np.median(diff[-third:]))
    flipped = bool(head * tail < 0 and abs(head) > 0.5 and abs(tail) > 0.5)

    return {
        "corr": round(float(np.corrcoef(L, R)[0, 1]), 4),
        "median_diff_db": round(base, 2),
        "diff_iqr_db": round(float(np.percentile(dev, 75)), 2),
        "head_median_db": round(head, 2),
        "tail_median_db": round(tail, 2),
        "sign_flip": flipped,
        "obstruction_runs": runs,
        "obstructed_s": round(sum(r["dur_s"] for r in runs), 2),
        "obstructed_pct": (round(100.0 * sum(r["dur_s"] for r in runs)
                                 / (m * HOP_S), 1) if m else None),
        "trace_diff_db": [round(float(v), 2)
                          for v in diff[::max(1, m // 300)]][:300],
    }


def envelope(x, sr):
    """RMS level per window, in dBFS."""
    win = max(1, int(WIN_S * sr))
    hop = max(1, int(HOP_S * sr))
    n = 1 + max(0, (len(x) - win) // hop)
    if n < 2:
        return np.zeros(0), np.zeros(0)
    idx = np.arange(win)[None, :] + hop * np.arange(n)[:, None]
    frames = x[idx]
    rms = np.sqrt(np.mean(frames * frames, axis=1) + 1e-20)
    return np.arange(n) * HOP_S, 20.0 * np.log10(rms)


def find_events(t, db):
    """Runs above the clip's own background, merged and filtered.

    Returns (events, floor_db, threshold_db). The floor is the 10th percentile
    of the clip, which is a background estimate that survives a clip where
    noise is present most of the time - a mean or a median would not.
    """
    if len(db) == 0:
        return [], None, None
    floor = float(np.percentile(db, 10))
    thr = floor + THRESH_DB
    above = db > thr
    events = []
    start = None
    for i, a in enumerate(above):
        if a and start is None:
            start = i
        elif not a and start is not None:
            events.append([start, i])
            start = None
    if start is not None:
        events.append([start, len(above)])

    merged = []
    for e in events:
        if merged and (e[0] - merged[-1][1]) * HOP_S < MIN_GAP_S:
            merged[-1][1] = e[1]
        else:
            merged.append(e)

    out = []
    for a, b in merged:
        dur = (b - a) * HOP_S
        if dur < MIN_EVENT_S:
            continue
        seg = db[a:b]
        # An event touching either end of the clip was already running when
        # recording started, or had not finished when it stopped. Its duration
        # is a FLOOR and must never be pooled with complete ones as if it were
        # a measurement.
        truncated = (a == 0) or (b >= len(db))
        out.append({
            "start_s": round(a * HOP_S, 2),
            "end_s": round(b * HOP_S, 2),
            "dur_s": round(dur, 2),
            "truncated": bool(truncated),
            "peak_dbfs": round(float(seg.max()), 1),
            "mean_dbfs": round(float(seg.mean()), 1),
            "rise_db": round(float(seg.max()) - floor, 1),
        })
    return out, round(floor, 1), round(thr, 1)


def duty_sweep(db):
    """Fraction of time above floor+X, for a range of X.

    ORIGINAL PURPOSE, NOW WITHDRAWN: this sweep existed to test whether the
    audio could decide between the two stopwatch readings. It cannot, and the
    reason is not statistical. The stopwatch is an independent sample taken
    62 minutes after the last video ended, and the operator states there is no
    correlation between them. A number computed here says nothing about a
    number computed there.

    WHAT IT IS STILL FOR: showing that the duty figure is an artefact of the
    threshold. It runs from tens of per cent down to zero across seven
    thresholds on the same audio. That is worth publishing as a caution
    against anyone - including this repository - quoting a single duty figure
    from uncalibrated audio as though it were a property of the site.
    """
    if len(db) == 0:
        return []
    floor = float(np.percentile(db, 10))
    return [{"thresh_db": x,
             "duty_pct": round(100.0 * float(np.mean(db > floor + x)), 1)}
            for x in (3, 4, 5, 6, 8, 10, 12)]



def analyse_clip(path):
    x, sr = decode_audio(path)
    t, db = envelope(x, sr)
    events, floor, thr = find_events(t, db)
    # Downsample the envelope for the page. 400 points is more than a chart
    # 900 px wide can resolve, and keeps the payload small.
    if len(db) > 400:
        edges = np.linspace(0, len(db), 401).astype(int)
        trace = [round(float(db[a:b].max()), 1)
                 for a, b in zip(edges[:-1], edges[1:]) if b > a]
    else:
        trace = [round(float(v), 1) for v in db]
    active = sum(e["dur_s"] for e in events)
    total = float(len(db) * HOP_S)
    return {
        "sample_rate": sr,
        "analysed_s": round(total, 2),
        "floor_dbfs": floor,
        "threshold_dbfs": thr,
        "peak_dbfs": round(float(db.max()), 1),
        "median_dbfs": round(float(np.median(db)), 1),
        "trace_dbfs": trace,
        "events": events,
        "n_events": len(events),
        "n_complete": sum(1 for e in events if not e["truncated"]),
        "active_s": round(active, 2),
        "duty_pct": round(100.0 * active / total, 1) if total else None,
        "duty_sweep": duty_sweep(db),
        "channels": channel_asymmetry(path),
    }


def constant_obstruction(clips):
    """Look for an obstruction that never lifts.

    `channel_asymmetry()` has a blind spot, and it is the one that matters
    here. It measures divergence against each clip's OWN median, so it detects
    a hand ARRIVING or LEAVING. A hand present for the whole recording moves
    the median with it and the test reports nothing - the same "all clear" it
    reports for a clean clip.

    A constant obstruction is therefore only visible BETWEEN clips, on three
    indicators that a hand moves in known directions and a quiet site does not:

      FLOOR        up.   Skin against a microphone port is a broadband source.
      RANGE        down. That source is always on, so it fills in the quiet.
      CORRELATION  down. Handling noise at one port is not the sound field at
                   the other, so the two channels stop agreeing.

    A genuinely quiet site moves the floor DOWN and leaves correlation alone.
    The two hypotheses therefore separate, which is the only reason this is
    worth computing rather than asserting.

    This ranks; it does not decide. Three indicators over three clips is not a
    test with a p-value, and it is not reported as one.
    """
    rows = []
    for name, a in clips.items():
        ch = a.get("channels") or {}
        rows.append({
            "clip": name,
            "floor_dbfs": a["floor_dbfs"],
            "range_db": round(a["peak_dbfs"] - a["floor_dbfs"], 1),
            "corr": ch.get("corr"),
        })
    if len(rows) < 2 or any(r["corr"] is None for r in rows):
        return None

    hi_floor = max(rows, key=lambda r: r["floor_dbfs"])["clip"]
    lo_range = min(rows, key=lambda r: r["range_db"])["clip"]
    lo_corr = min(rows, key=lambda r: r["corr"])["clip"]
    agree = hi_floor == lo_range == lo_corr
    for r in rows:
        r["flags"] = sum([r["clip"] == hi_floor, r["clip"] == lo_range,
                          r["clip"] == lo_corr])

    return {
        "rows": sorted(rows, key=lambda r: -r["flags"]),
        "highest_floor": hi_floor,
        "smallest_range": lo_range,
        "lowest_correlation": lo_corr,
        "all_three_agree": agree,
        "suspect": hi_floor if agree else None,
        "verdict": (
            ("All three indicators point at the same clip, %s. That is what a "
             "microphone obstructed for the WHOLE recording looks like, and it "
             "is the opposite of what a quiet site looks like - a quiet site "
             "lowers the floor and leaves the two channels agreeing. It is "
             "consistent with the operator's account and it is not proof of "
             "it: three indicators over three clips cannot carry a p-value, "
             "and no significance is claimed. The consequence does not depend "
             "on resolving the cause - the clip is excluded either way."
             % hi_floor)
            if agree else
            "The three indicators do not agree on a single clip, so there is "
            "no evidence here of an obstruction lasting a whole recording."),
    }


def detectability(clips, rate_per_hour):
    """How much a clip of a given length could ever have shown.

    A ten-second recording that contains no train is not evidence that the
    place is quiet. At a scheduled rate of about one a minute, ten seconds is
    a coin weighted heavily toward showing nothing, and reporting "0 events"
    beside a 60 s clip's "2 events" invites exactly the wrong comparison.

    Poisson, which is the right null here for the same Palm-Khintchine reason
    the frequency dashboard uses it: several independent routes superposed
    look Poisson at a point even though each is scheduled.
    """
    if not rate_per_hour:
        return None
    lam = rate_per_hour / 3600.0
    out = []
    for name, a in clips.items():
        dur = a["analysed_s"]
        exp = lam * dur
        p0 = math.exp(-exp)
        out.append({
            "clip": name,
            "analysed_s": dur,
            "expected_events": round(exp, 2),
            "p_zero_pct": round(100.0 * p0, 1),
            "observed": a["n_events"],
            "informative": bool(p0 < 0.5),
        })
    out.sort(key=lambda r: r["analysed_s"])
    weak = [r for r in out if not r["informative"] and r["observed"] == 0]
    return {
        "rate_per_hour": rate_per_hour,
        "clips": out,
        "note": ("A null in a clip shorter than a headway is not a finding. "
                 "Of the clips here, %d had a better-than-even chance of "
                 "containing no train at all regardless of how loud the site "
                 "is, so their zero counts carry no information about the "
                 "site and are not used for anything."
                 % len(weak)),
        "uninformative_nulls": [r["clip"] for r in weak],
    }


# ---------------------------------------------------------------------------
# The stopwatch
# ---------------------------------------------------------------------------

STOPWATCH = "Timer Lap start time for train noise-accumulated time.txt"


def parse_stopwatch(path):
    laps = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            m = re.match(r"\s*(\d+)\s+(\d+):(\d+\.\d+)\s+(\d+):(\d+\.\d+)\s*$",
                         line)
            if m:
                laps.append({
                    "lap": int(m.group(1)),
                    "lap_s": int(m.group(2)) * 60 + float(m.group(3)),
                    "total_s": int(m.group(4)) * 60 + float(m.group(5)),
                })
    if not laps:
        raise SystemExit("no laps parsed from %s" % path)

    # The export is a cumulative column and a difference column. They must
    # agree, or one of them has been transcribed rather than exported.
    for i, lp in enumerate(laps):
        expect = laps[i - 1]["total_s"] + lp["lap_s"] if i else lp["lap_s"]
        if abs(expect - lp["total_s"]) > 0.02:
            raise SystemExit("lap %d does not reconcile: %.2f vs %.2f"
                             % (lp["lap"], expect, lp["total_s"]))
    return laps


def pair_stopwatch(laps):
    """Decide which laps are noise and which are the quiet between.

    THIS IS AN INFERENCE, NOT A READING. The export records button presses and
    not what the presses meant. The observer alternated start/end, but nothing
    in the file says whether lap 1 ran from "timer started" to "first train
    audible" or from "first train audible" to "first train gone". The two
    readings are exact complements and they differ enormously - one puts the
    site under train noise 20% of the time, the other 80%.

    So both are computed, and the choice between them is made on a stated
    test rather than on which one is more striking.

    THE TEST: quiet gaps are set by the timetable and should therefore cluster;
    event durations are set by train length, speed, direction and distance and
    should therefore scatter. Whichever assignment puts the TIGHTER
    distribution on the gaps is the one where the gaps are really gaps. The
    ratio of the two coefficients of variation is reported, so a reader can
    see how decisive the test was rather than being told that it was.

    This is still an inference and the page says so. It is corroborated
    independently by the audio envelopes, which measure event duration
    directly and were not used to make this choice.
    """
    def stats(vals):
        a = np.array(vals, dtype=float)
        return {
            "n": len(a),
            "values": [round(float(v), 2) for v in a],
            "min": round(float(a.min()), 2),
            "max": round(float(a.max()), 2),
            "mean": round(float(a.mean()), 2),
            "median": round(float(np.median(a)), 2),
            "sd": round(float(a.std(ddof=1)), 2) if len(a) > 1 else None,
            "cv": (round(float(a.std(ddof=1) / a.mean()), 3)
                   if len(a) > 1 and a.mean() else None),
        }

    seq = [lp["lap_s"] for lp in laps]
    readings = {}
    for name, off in (("odd_quiet", 0), ("odd_noise", 1)):
        quiet = seq[0::2] if off == 0 else seq[1::2]
        noise = seq[1::2] if off == 0 else seq[0::2]
        q, n = stats(quiet), stats(noise)
        cycle = q["mean"] + n["mean"]
        readings[name] = {
            "quiet": q,
            "noise": n,
            "cycle_s": round(cycle, 2),
            "events_per_hour": round(3600.0 / cycle, 1) if cycle else None,
            "duty_pct": round(100.0 * n["mean"] / cycle, 1) if cycle else None,
            # Lower is tighter. The test compares this across the two readings.
            "gap_cv": q["cv"],
        }

    a, b = readings["odd_quiet"], readings["odd_noise"]
    chosen = "odd_quiet" if a["gap_cv"] <= b["gap_cv"] else "odd_noise"
    other = "odd_noise" if chosen == "odd_quiet" else "odd_quiet"
    ratio = (readings[other]["gap_cv"] / readings[chosen]["gap_cv"]
             if readings[chosen]["gap_cv"] else None)

    return {
        "laps": laps,
        "n_laps": len(laps),
        "span_s": round(laps[-1]["total_s"], 2),
        "readings": readings,
        "chosen": chosen,
        "rejected": other,
        "cv_ratio": round(ratio, 2) if ratio else None,
        "basis": ("The reading whose quiet intervals cluster more tightly is "
                  "taken as the one in which the quiet intervals are really "
                  "quiet intervals, because headway is scheduled and event "
                  "duration is not."),
        # The tie-break above once had a second, independent prop: an audio
        # duty ceiling that appeared to rule the other reading out. That prop
        # is withdrawn - the audio is a separate sample an hour away - so the
        # pairing now rests on ONE argument, and the confidence attached to
        # everything downstream of it drops accordingly.
        "sole_support": True,
        "confidence": "WEAK",
        "operator_account": (
            "The operator's own reading of the session is that it showed "
            "'a very small amount of time between noise from the train "
            "tracks'. That is ambiguous between two things this stopwatch "
            "cannot separate: short GAPS, which would favour the rejected "
            "pairing, or a short CYCLE, which is pairing-independent and is "
            "already established at %.1f s. It is recorded rather than "
            "resolved."
            % (readings[chosen]["cycle_s"] or 0.0)),
        "pairing_independent": (
            "The cycle, and therefore the event rate, is identical under both "
            "pairings. It is the only quantity here that does not depend on "
            "the tie-break, and it is the only one carried forward."),
        "superseded": (
            "The operator has stated this will be re-run with documentation "
            "of which tap was which. When that happens the tie-break stops "
            "being an inference and this section is replaced, not amended."),
    }


# ---------------------------------------------------------------------------
# The schedule, for the exact clock windows that were observed
# ---------------------------------------------------------------------------

def geo_context(files):
    """Place every GPS-carrying capture against the repository's own geometry.

    The captures arrived with embedded GPS, which means they can be checked
    against the four points the MTA measured at rather than described by name.
    A place name is not a position: "the grassy knoll" and "under the bridge"
    are both a hundred metres wide, and every acoustic claim in this repository
    is distance-dependent.

    The axis, the projection and the chainage origin are IMPORTED from
    `build_carousel.py` rather than reimplemented, so this file cannot drift
    away from the drawings. Chainage zero is the DUMBO Archway - itself an MTA
    measurement point - and across-track is signed, so the sign answers on its
    own whether a capture is north-east or south-west of the track centreline.
    """
    sys.path.insert(0, ROOT)
    try:
        import build_carousel as bc
    except Exception as exc:                       # pragma: no cover
        print("  geo: build_carousel not importable (%s)" % exc)
        return None

    c, u, pts = bc.bridge_axis()
    bearing = math.degrees(math.atan2(u[0], u[1])) % 360.0

    # The sign of the across-track coordinate means nothing until it is tied to
    # a compass direction, and it is NOT safe to type one in: the fitted axis
    # can flip on a refit, at which point a hard-coded "north-east" silently
    # becomes wrong for every row. Derive it from the axis actually fitted.
    # Positive t is the left normal of u.
    POINTS = ["north", "north-north-east", "north-east", "east-north-east",
              "east", "east-south-east", "south-east", "south-south-east",
              "south", "south-south-west", "south-west", "west-south-west",
              "west", "west-north-west", "north-west", "north-north-west"]

    def compass(deg):
        return POINTS[int((deg % 360.0) / 22.5 + 0.5) % 16]

    pos_deg = math.degrees(math.atan2(-u[1], u[0])) % 360.0
    neg_deg = (pos_deg + 180.0) % 360.0
    pos_dir, neg_dir = compass(pos_deg), compass(neg_deg)

    # The axis is a straight line fitted to a curved-in-principle railway. It
    # is only usable over the range where the fitted points actually lie, and
    # only if they are straight there. Both are measured, not assumed.
    fit_s, fit_t = [], []
    for p in pts:
        s, t = bc.chain(p, c, u)
        fit_s.append(s)
        fit_t.append(t)
    fit_lo, fit_hi = min(fit_s), max(fit_s)
    straightness = max(abs(t) for t in fit_t)

    def place(lat, lon):
        p = bc.g(lat, lon)
        s, t = bc.chain(p, c, u)
        near, nd = None, None
        for key, name, alat, alon, leq, lmax in bc.ANCHORS:
            a = bc.g(alat, alon)
            d = math.hypot(p[0] - a[0], p[1] - a[1])
            if nd is None or d < nd:
                near, nd = (key, name, leq, lmax), d
        return s, t, near, nd

    rows = []
    for f in files:
        if "lat" not in f or "lon" not in f:
            continue
        s, t, near, nd = place(f["lat"], f["lon"])
        rows.append({
            "name": f["name"],
            "kind": f["kind"],
            "lat": f["lat"], "lon": f["lon"],
            "chainage_m": round(s, 1),
            "offset_m": round(t, 1),
            "abs_offset_m": round(abs(t), 1),
            "side": pos_dir if t > 0 else neg_dir,
            "nearest_anchor": near[1],
            "nearest_anchor_m": round(nd, 1),
            "anchor_leq_dba": near[2],
            "anchor_lmax_dba": near[3],
        })
    rows.sort(key=lambda r: r["chainage_m"])

    anchors = []
    for key, name, alat, alon, leq, lmax in bc.ANCHORS:
        s, t, _, _ = place(alat, alon)
        anchors.append({"key": key, "name": name,
                        "chainage_m": round(s, 1), "offset_m": round(t, 1),
                        "abs_offset_m": round(abs(t), 1),
                        "leq_dba": leq, "lmax_dba": lmax})

    # The spread of the captures along and across the track, which is what
    # decides whether they can be treated as one place or several.
    spread_s = max(r["chainage_m"] for r in rows) - min(r["chainage_m"]
                                                        for r in rows)
    spread_t = max(r["abs_offset_m"] for r in rows) - min(r["abs_offset_m"]
                                                          for r in rows)

    return {
        "axis_bearing_deg": round(bearing, 2),
        "axis_source": "OSM ways tagged railway=subway + bridge=yes, %d nodes"
                       % len(pts),
        "axis_fitted_from_m": round(fit_lo, 0),
        "axis_fitted_to_m": round(fit_hi, 0),
        "axis_straightness_m": round(straightness, 2),
        "captures_within_fit": bool(rows and
                                    min(r["chainage_m"] for r in rows) >= fit_lo
                                    and max(r["chainage_m"] for r in rows)
                                    <= fit_hi),
        "positive_offset_bearing_deg": round(pos_deg, 1),
        "positive_offset_dir": pos_dir,
        "negative_offset_dir": neg_dir,
        "origin": "DUMBO Archway (chainage zero, also an MTA measurement "
                  "point)",
        "captures": rows,
        "anchors": anchors,
        "chainage_spread_m": round(spread_s, 1),
        "offset_spread_m": round(spread_t, 1),
        "axis_note": ("A straight axis fitted to a railway is only a "
                      "description of that railway where the fitted points "
                      "lie. These span %.0f m to %.0f m of chainage and are "
                      "straight to within %.1f m over that run, and every "
                      "capture falls inside it, so no offset here is an "
                      "extrapolation. Offsets quoted outside that range would "
                      "be measuring distance from an imaginary line."
                      % (fit_lo, fit_hi, straightness)),
        "note": ("Phone GPS in a street canyon under a steel deck is the worst "
                 "case for multipath. These positions are good to tens of "
                 "metres, not metres, and no claim here turns on a difference "
                 "smaller than that. The video coordinates are also stored to "
                 "4 decimal places by Android - about 11 m - so they cannot "
                 "be more precise than that even if the fix were perfect."),
    }


def schedule_window(start_hms, dur_s, service="Weekday"):
    """Scheduled bridge traversals overlapping one observed window.

    Reads `data-collection/dashboard-data.json`, which is built from MTA's own
    published GTFS. Events are timed at the last station BEFORE the bridge -
    Grand St for B/D, Canal St for N/Q - so a departure there precedes the
    audible pass-by at a DUMBO receptor by the run time plus dwell.

    THAT OFFSET IS NOT APPLIED. It is not published, this programme has not
    measured it, and inventing it would put a fabricated number between an
    observation and a schedule and then compare them. The count over a window
    is robust to a constant offset; the phase is not, and no phase claim is
    made anywhere here.
    """
    path = os.path.join(ROOT, "data-collection", "dashboard-data.json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        d = json.load(fh)
    evs = d["events"].get(service)
    if not evs:
        return None
    h, m, s = (int(x) for x in start_hms.split(":"))
    t0 = h * 3600 + m * 60 + s
    t1 = t0 + dur_s
    hits = [e for e in evs if t0 <= e[3] < t1]
    by_route = {}
    by_dir = {}
    for e in hits:
        by_route[d["routes"][e[0]]] = by_route.get(d["routes"][e[0]], 0) + 1
        by_dir[d["directions"][e[1]]] = by_dir.get(d["directions"][e[1]], 0) + 1
    return {
        "service": service,
        "feed_version": d.get("feed_version", ""),
        "window_start": start_hms,
        "window_s": round(dur_s, 2),
        "n_scheduled": len(hits),
        "by_route": by_route,
        "by_direction": by_dir,
        "per_hour": round(3600.0 * len(hits) / dur_s, 1) if dur_s else None,
        "times_s": sorted(e[3] for e in hits),
    }


def derivatives(files):
    """Map each master capture to the web-sized files that stand in for it.

    The page cannot hard-code these names. A derivative that is renamed, or one
    that make_derivatives.py failed to write, would then show as a broken image
    on a published page rather than as an error here - and a page of broken
    images is exactly the failure mode this repository has already shipped once
    via an unanchored .gitignore pattern. So the map is built by LOOKING, and
    every master that should have a derivative is checked for one.

    Masters are excluded from git by size; the derivatives are what ships. If
    the two ever disagree the build stops.
    """
    web = os.path.join(HERE, "web")
    if not os.path.isdir(web):
        raise SystemExit("no web/ directory - run make_derivatives.py first")
    have = set(os.listdir(web))

    out, missing = {}, []
    for f in files:
        name = f["name"]
        stem, ext = os.path.splitext(name)
        if f["kind"] == "video":
            want = {"poster": stem + "-poster.jpg", "audio": stem + ".m4a"}
        elif f["kind"] in ("still", "screenshot"):
            want = {"image": name}
        else:
            continue
        got = {}
        for role, fn in want.items():
            if fn in have:
                got[role] = {
                    "file": "web/" + fn,
                    "bytes": os.path.getsize(os.path.join(web, fn)),
                }
            else:
                missing.append("%s: no %s (%s)" % (name, role, fn))
        out[name] = got

    if missing:
        raise SystemExit("derivatives missing:\n  " + "\n  ".join(missing))

    master_b = sum(f["bytes"] for f in files if f["name"] in out)
    web_b = sum(d["bytes"] for roles in out.values() for d in roles.values())
    return {
        "files": out,
        "n": sum(len(r) for r in out.values()),
        "master_bytes": master_b,
        "web_bytes": web_b,
        "shrink_x": round(master_b / web_b, 1) if web_b else None,
        "note": ("The masters are not in this repository. One video is 114 MB, "
                 "which is over GitHub's hard file limit, and committing the "
                 "set would put a quarter of a gigabyte of phone footage into "
                 "a research repository to no purpose. What ships is a poster "
                 "frame and an audio track per video and a resized still per "
                 "photograph. Every master is fingerprinted by SHA-256 above, "
                 "so a master supplied later can be checked against what was "
                 "actually analysed."),
    }


def separation(files, sw):
    """Seconds between the end of the last video and the start of the stopwatch.

    The operator states the stopwatch is an independent sample uncorrelated
    with any video or audio. That statement is decisive on its own. This
    function exists so the page does not have to take it on trust: the file
    timestamps say the same thing, and a reader can check the arithmetic.

    A statement of intent and a file timestamp agreeing is the strongest form
    this evidence can take, because they could have disagreed.
    """
    ends = []
    for f in files:
        # Only audio-bearing captures matter here. The comparison being
        # severed is between the audio and the stopwatch; a still photograph
        # taken at 12:02 has no bearing on it.
        if f.get("start_local") and f.get("duration_s") and f.get("audio"):
            h, m, s = (int(x) for x in f["start_local"].split(":"))
            ends.append((h * 3600 + m * 60 + s + f["duration_s"], f["name"]))
    if not ends or not sw.get("start_local_approx"):
        return None
    last_end, last_name = max(ends)
    h, m, s = (int(x) for x in sw["start_local_approx"].split(":"))
    sw_start = h * 3600 + m * 60 + s
    gap = sw_start - last_end
    return {
        "last_media_name": last_name,
        "last_media_end_local": "%02d:%02d:%02d" % (
            int(last_end // 3600), int(last_end % 3600 // 60), int(last_end % 60)),
        "stopwatch_start_local": sw["start_local_approx"],
        "gap_s": round(gap, 1),
        "gap_min": round(gap / 60.0, 1),
        "overlap_s": 0.0 if gap > 0 else round(-gap, 1),
        "note": ("The two instruments share no overlap at all. The operator's "
                 "statement that they are uncorrelated and the file "
                 "timestamps agree, and they could have disagreed."),
    }

def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    files = []
    for name in sorted(os.listdir(HERE)):
        path = os.path.join(HERE, name)
        if not os.path.isfile(path) or name.endswith((".py", ".json", ".js",
                                                      ".html", ".md")):
            continue
        when, kind, place = SESSIONS.get(name, ("", "unknown", ""))
        rec = {
            "name": name,
            "kind": kind,
            "place": place,
            "filename_time": when,
            "bytes": os.path.getsize(path),
            "sha256": sha256(path),
        }
        if name.lower().endswith((".mp4", ".mov")):
            rec.update(probe(path))
            rec["audio"] = analyse_clip(path)
        elif name.lower().endswith((".jpg", ".jpeg", ".png")):
            rec.update(exif(path))
        files.append(rec)
        print("  %-46s %7.1f MB  %s" % (name[:46], rec["bytes"] / 1e6, kind))

    # ------------------------------------------------------------------
    # The filename/creation_time reconciliation, asserted rather than assumed.
    # ------------------------------------------------------------------
    recon = []
    for f in files:
        if f.get("duration_s") and f.get("creation_time") and f["filename_time"]:
            import datetime as dt
            start = dt.datetime.strptime(f["filename_time"], "%Y-%m-%d %H:%M:%S")
            close = dt.datetime.strptime(f["creation_time"][:19],
                                         "%Y-%m-%dT%H:%M:%S")
            close_local = close - dt.timedelta(hours=4)   # EDT on these dates
            lag = (close_local - start).total_seconds() - f["duration_s"]
            recon.append({"name": f["name"], "finalise_lag_s": round(lag, 2)})
            f["start_local"] = start.strftime("%H:%M:%S")
            f["end_local"] = (start + dt.timedelta(seconds=f["duration_s"])
                              ).strftime("%H:%M:%S")
    lags = [r["finalise_lag_s"] for r in recon]
    if lags and (min(lags) < 0 or max(lags) > 10):
        raise SystemExit("filename and creation_time do not reconcile: %s"
                         % recon)

    sw = pair_stopwatch(parse_stopwatch(os.path.join(HERE, STOPWATCH)))

    # ------------------------------------------------------------------
    # Schedule comparison, for each observed window.
    # ------------------------------------------------------------------
    # 2026-08-04 is a Tuesday, so the Weekday service applies. Asserted, not
    # assumed, because a holiday would silently select the wrong timetable.
    import datetime as dt
    if dt.date(2026, 8, 4).weekday() > 4:
        raise SystemExit("2026-08-04 is not a weekday; service selection wrong")

    # The stopwatch ran for span_s and the screenshot that ends it is stamped
    # 13:07:19 with the timer paused and 52.29 s showing on an unlapped
    # fifteenth interval. Working backwards gives the start. The gap between
    # pausing and screenshotting is NOT known, so this start time carries an
    # unknown positive error and is stated as approximate everywhere.
    sw_visible_extra = 52.29
    sw_end = dt.datetime(2026, 8, 4, 13, 7, 19)
    sw_start = sw_end - dt.timedelta(seconds=sw["span_s"] + sw_visible_extra)
    sw["start_local_approx"] = sw_start.strftime("%H:%M:%S")
    sw["end_local_approx"] = sw_end.strftime("%H:%M:%S")
    sw["start_is_approximate"] = True
    sw["schedule"] = schedule_window(sw["start_local_approx"],
                                     sw["span_s"] + sw_visible_extra)

    for f in files:
        if f.get("start_local") and f.get("duration_s"):
            f["schedule"] = schedule_window(f["start_local"], f["duration_s"])

    all_vids = [f for f in files if f.get("audio")]

    # A clip that cannot be trusted must be dropped BEFORE any statistic is
    # taken over it, not caveated afterwards. Everything below - the span, the
    # excursion durations, the duty ceiling - is computed over `vids`, and the
    # excluded clip is kept in `files` so the page can still show it and say
    # why it is not being used.
    co = constant_obstruction({f["name"]: f["audio"] for f in all_vids})
    excluded = {co["suspect"]} if co and co.get("suspect") else set()
    vids = [f for f in all_vids if f["name"] not in excluded]
    for f in all_vids:
        f["excluded_from_analysis"] = f["name"] in excluded
        if f["name"] in excluded:
            f["exclusion_reason"] = (
                "Every indicator of a microphone obstructed for the whole "
                "recording points at this clip, and the operator "
                "independently reported covering the microphone. It is shown "
                "but is not used in any statistic.")

    obs_events = sum(f["audio"]["n_events"] for f in vids)
    obs_span = sum(f["audio"]["analysed_s"] for f in vids)
    sched_in_vid = sum(f["schedule"]["n_scheduled"] for f in vids
                       if f.get("schedule"))
    # Truncated excursions are floors, not measurements, and are pooled
    # separately. Mixing them in would drag the median down by exactly the
    # amount the recording happened to miss.
    complete = sorted(e["dur_s"] for f in vids for e in f["audio"]["events"]
                      if not e["truncated"])
    cut = sorted(e["dur_s"] for f in vids for e in f["audio"]["events"]
                 if e["truncated"])
    longest = max([e["dur_s"] for f in vids for e in f["audio"]["events"]]
                  or [0.0])
    active_total = sum(f["audio"]["active_s"] for f in vids)

    # The duty cycle moves a lot with the detection threshold, so a single
    # figure cannot carry a conclusion.
    #
    # WITHDRAWN REASONING, kept here because the code is the record: this was
    # a ceiling, and a ceiling was supposed to be able to refute any stopwatch
    # reading that predicted a higher duty. That inference is dead. It required
    # the two instruments to be measuring the same thing, and they are not -
    # they are separated by an hour and the operator states they are
    # uncorrelated. The value is still computed because the SWEEP is worth
    # showing; the ceiling itself no longer refutes anything.
    duty_ceiling = max(
        [s["duty_pct"] for f in vids for s in f["audio"]["duty_sweep"]] or [0.0])

    ch = sw["readings"][sw["chosen"]]
    rej = sw["readings"][sw["rejected"]]

    # Proves the independence the operator asserts, from the timestamps, so a
    # reader does not have to take either the operator's word or mine.
    sep = separation(files, sw)
    if sep and sep["gap_s"] <= 0:
        raise SystemExit(
            "separation(): the stopwatch overlaps the media by %.1f s. The "
            "independence argument on this page assumes it does not. Fix the "
            "argument, not this check." % sep["overlap_s"])

    # The rate agreement must be quoted with its own sampling error or it
    # invites the reader to believe seven events settle something to 2%.
    # Poisson: sd of a count of n is sqrt(n), so the 95% band on the rate is
    # roughly +-2/sqrt(n) of itself.
    n_sw = ch["noise"]["n"]
    rate_sw = ch["events_per_hour"]
    band = 2.0 / np.sqrt(n_sw) if n_sw else None
    sched = sw.get("schedule") or {}

    out = {
        "schema": "site-visit-media/1",
        "generator": "pedestrian-site-visits/build_media_data.py",
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "ffmpeg": os.path.basename(FFMPEG),
        "analysis": {"window_s": WIN_S, "hop_s": HOP_S,
                     "threshold_db": THRESH_DB,
                     "min_event_s": MIN_EVENT_S, "min_gap_s": MIN_GAP_S},
        "files": files,
        "derivatives": derivatives(files),
        "geo": geo_context(files),
        "operator_notes": OPERATOR_NOTES,
        "constant_obstruction": co,
        "excluded_clips": sorted(excluded),
        "detectability": detectability(
            {f["name"]: f["audio"] for f in files if "audio" in f},
            sched.get("per_hour")),
        "stopwatch": sw,
        "rate_check": {
            "observed_per_hour": rate_sw,
            "observed_n": n_sw,
            "observed_span_s": sw["span_s"],
            "scheduled_per_hour": sched.get("per_hour"),
            "scheduled_n": sched.get("n_scheduled"),
            "ci95_low": round(rate_sw * (1 - band), 1) if band else None,
            "ci95_high": round(rate_sw * (1 + band), 1) if band else None,
            "agrees": (bool(sched.get("per_hour")
                            and rate_sw * (1 - band) <= sched["per_hour"]
                            <= rate_sw * (1 + band)) if band else None),
            "note": ("Seven events is a small sample and the interval is "
                     "correspondingly wide. This rules out gross error - it "
                     "does not establish agreement to a few per cent."),
        },
        "corroboration": {
            "STATUS": "WITHDRAWN",
            "withdrawn_claim": (
                "The audio was analysed without reference to the stopwatch, "
                "and it refutes the reading that was rejected."),
            "withdrawn_because": (
                "The claim required the audio and the stopwatch to be "
                "measuring the same thing. They are not. The operator states "
                "the stopwatch is an independent sample with no correlation "
                "to any video or audio, and the file timestamps agree: the "
                "last video ended at %s and the stopwatch did not start until "
                "%s, a gap of %.0f minutes. A duty cycle measured in one "
                "window places no constraint on a duty cycle in another."
                % (sep["last_media_end_local"], sep["stopwatch_start_local"],
                   sep["gap_min"]) if sep else "No overlap between instruments."),
            "second_reason": (
                "Independently of the timing, the video was not captured for "
                "acoustic precision. The operator states its purpose was to "
                "show the buildings that form the echo chamber near the "
                "water. Its audio track is a by-product of a visual record, "
                "shot while walking, and cannot carry a duty cycle for the "
                "site under any pairing of instruments."),
            "what_survives": (
                "Each instrument still constrains itself and nothing else. "
                "The audio numbers below describe three files. The stopwatch "
                "numbers describe eight minutes of one person's judgement. "
                "Neither is transported to the other anywhere on the page."),
            # Retained so the withdrawal can be checked rather than believed.
            "audio_n_excursions": obs_events,
            "audio_n_complete": len(complete),
            "audio_n_truncated": len(cut),
            "audio_span_s": round(obs_span, 2),
            "audio_complete_durations": complete,
            "audio_truncated_durations": cut,
            "audio_longest_s": round(longest, 2),
            "audio_median_complete_s": (round(float(np.median(complete)), 2)
                                        if complete else None),
            "audio_duty_pct": (round(100.0 * active_total / obs_span, 1)
                               if obs_span else None),
            "stopwatch_median_event_s": ch["noise"]["median"],
            "stopwatch_duty_pct": ch["duty_pct"],
            "rejected_duty_pct": rej["duty_pct"],
            "rejected_mean_event_s": rej["noise"]["mean"],
            "duty_ceiling_pct": duty_ceiling,
            "scheduled_in_video_windows": sched_in_vid,
        },
        "separation": sep,
        "capture_intent": CAPTURE_INTENT,
    }

    path = os.path.join(HERE, "media-data.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print("\nwrote %s (%d bytes)" % (path, os.path.getsize(path)))
    return out


if __name__ == "__main__":
    main()
