"""Produce web-publishable derivatives of the site-visit captures.

WHY THIS EXISTS
---------------
The masters total about 235 MB and the largest single file is 114 MB. GitHub
rejects any file over 100 MB outright, so committing the masters is not a
choice that is available. It would also be the wrong choice if it were: a
research page that takes 235 MB to open is a page nobody opens.

So the masters stay local and are recorded by SHA-256 in `media-data.json`,
and what is committed is a set of derivatives small enough to serve:

    stills   long edge 1600 px, quality 82
    posters  one frame per clip, same treatment
    audio    mono 48 kbps AAC - the acoustically relevant track, whole

THE AUDIO IS NOT DOWNSAMPLED IN TIME. Every second of every clip's sound is
committed. That matters: the acoustic argument on the page is about WHEN the
level rises and for how long, and a reader has to be able to listen to the
same thing the envelope was computed from. Video is where the bytes are and
video is what is dropped; the evidence is kept.

Re-encoding to 48 kbps is itself a loss, and it is a loss in exactly the
dimension the page already refuses to use - absolute level. It does not
affect timing, which is the only quantity claimed.
"""

import json
import os
import subprocess
import sys

try:
    import imageio_ffmpeg
    FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:                                        # pragma: no cover
    FFMPEG = "ffmpeg"

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(HERE, "web")

LONG_EDGE = 1600
JPEG_Q = 4          # ffmpeg -q:v scale, 2 = best, 31 = worst
AUDIO_KBPS = 48

# Poster frame offsets, in seconds. Chosen to land on something legible rather
# than on whatever frame happens to be first - a walking clip usually opens on
# a blur. Any clip not listed uses 1.0 s.
POSTER_AT = {
    "canyon-buildings-20260804_115319.mp4": 3.0,
    "canyon-buildings2-20260804_115505.mp4": 2.0,
    "grassy-knoll-20260804_115626.mp4": 2.0,
}


def run(args):
    r = subprocess.run(args, capture_output=True, text=True, errors="replace")
    if r.returncode != 0:
        raise SystemExit("ffmpeg failed:\n%s" % r.stderr[-1500:])


def still(src, dst):
    run([FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-i", src,
         "-vf", "scale='min(%d,iw)':-2" % LONG_EDGE,
         "-q:v", str(JPEG_Q), dst])


def poster(src, dst, at):
    run([FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-ss", str(at),
         "-i", src, "-frames:v", "1",
         "-vf", "scale='min(%d,iw)':-2" % LONG_EDGE,
         "-q:v", str(JPEG_Q), dst])


def audio(src, dst):
    run([FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-i", src,
         "-vn", "-ac", "1", "-c:a", "aac", "-b:a", "%dk" % AUDIO_KBPS, dst])


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    os.makedirs(WEB, exist_ok=True)

    data_path = os.path.join(HERE, "media-data.json")
    with open(data_path, encoding="utf-8") as fh:
        data = json.load(fh)

    total_src = total_web = 0
    for rec in data["files"]:
        name = rec["name"]
        src = os.path.join(HERE, name)
        stem = os.path.splitext(name)[0]
        total_src += rec["bytes"]
        rec["web"] = {}

        if name.lower().endswith((".jpg", ".jpeg", ".png")):
            dst = os.path.join(WEB, stem + ".jpg")
            still(src, dst)
            rec["web"]["image"] = "web/" + os.path.basename(dst)
            rec["web"]["image_bytes"] = os.path.getsize(dst)
            total_web += os.path.getsize(dst)

        elif name.lower().endswith(".mp4"):
            p = os.path.join(WEB, stem + "-poster.jpg")
            poster(src, p, POSTER_AT.get(name, 1.0))
            rec["web"]["poster"] = "web/" + os.path.basename(p)
            rec["web"]["poster_bytes"] = os.path.getsize(p)

            a = os.path.join(WEB, stem + ".m4a")
            audio(src, a)
            rec["web"]["audio"] = "web/" + os.path.basename(a)
            rec["web"]["audio_bytes"] = os.path.getsize(a)
            total_web += os.path.getsize(p) + os.path.getsize(a)

        for k, v in sorted(rec["web"].items()):
            if k.endswith("_bytes"):
                continue
            print("  %-30s -> %-46s %6.2f MB"
                  % (name[:30], os.path.basename(v),
                     rec["web"][k + "_bytes"] / 1e6))

    data["derivatives"] = {
        "long_edge_px": LONG_EDGE,
        "jpeg_q": JPEG_Q,
        "audio_kbps": AUDIO_KBPS,
        "master_bytes": total_src,
        "web_bytes": total_web,
        "ratio": round(total_src / total_web, 1) if total_web else None,
        "masters_committed": False,
        "why": ("The largest master is %.0f MB and GitHub rejects files over "
                "100 MB. Masters are kept locally and identified by SHA-256; "
                "audio is committed in full because timing is the only "
                "acoustic quantity claimed."
                % (max(f["bytes"] for f in data["files"]) / 1e6)),
    }

    with open(data_path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=1, sort_keys=True)

    print("\nmasters %.1f MB -> web %.1f MB  (%.0fx smaller)"
          % (total_src / 1e6, total_web / 1e6, total_src / total_web))
    if total_web > 12e6:
        raise SystemExit("web derivatives total %.1f MB, which is too heavy "
                         "for a research page" % (total_web / 1e6))
    return 0


if __name__ == "__main__":
    sys.exit(main())
