# Usage exported from other machines

The dashboard in this directory reads `~/.copilot/session-store.db`, which is
**local to one machine**. This project was also worked on from a second
machine, in four sibling repositories:

- `dumbo-district-3d`
- `manhattan-bridge-3d`
- `brooklyn-bridge-3d`
- `williamsburg-bridge-3d`

That work cost real money and is invisible here. There is no API to ask the
other machine for it — the store is a local SQLite file and nothing uploads it.
So the numbers on the dashboard are an **exact figure for this repository and a
floor for the project**, and the dashboard says so rather than letting the gap
pass unremarked.

## Closing the gap

On the other machine:

```
curl -O https://raw.githubusercontent.com/Ethical-Tech-CoLab/manhattan-bridge-noise-dumbo/main/usage/export_session.py
python export_session.py --list
python export_session.py --all --out .
```

Copy the resulting `*.json` files into this directory, then re-run
`python usage/build_usage_data.py` and `python usage/build_glance_band.py`.

No repository checkout is needed on that machine — `export_session.py` is a
single standard-library file.

## What a contribution file contains

Counts, timestamps, durations, model names and prices. **No prompt text, no
responses, no file contents, no turn labels, no session summaries.** A
contribution can be read end to end by anyone and reveals what was spent, not
what was said. Every file carries `"contains_prompt_text": false`, and the
exporter has no code path that would make it true.

## What the generator checks before trusting one

- `format` and `version` must match.
- The per-request costs must sum to the total the file states, and the row
  count must match the count it states. A truncated or hand-edited file is
  refused, not silently halved.
- A contribution whose `session_id` is the session being read live is skipped,
  because counting both would double every figure on the page.

## How merged time is computed, and why it is not a sum

**Money is additive and a person is not.** Requests, tokens and cost are summed
across machines — two machines spending at once really do spend twice.
Wall-clock time is not summed:

- **Model work seconds** add up. If both machines were generating at 14:32,
  two models really were working.
- **Model wall time** is a *union*. Only one minute of clock passed.
- **Engaged time** is a *union of sittings*, because there is one person and
  they cannot be at two keyboards at once.
- **Person time** is then computed from that merged clock, never by adding the
  per-machine residuals together.

Summing person-hours per machine is the specific error this design exists to
avoid: it would inflate the weakest column on the page, and it would do it
invisibly. The difference is reported directly as *concurrent time* — the
wall-clock seconds during which more than one machine was generating.
