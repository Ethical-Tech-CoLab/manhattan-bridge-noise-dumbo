# Establishing train frequency over the Manhattan Bridge

Two scripts that answer a question this programme has been asserting an answer
to without ever deriving it: **how many trains actually cross the Manhattan Bridge, and when?**

| Script | Answers | Cost |
|---|---|---|
| `bridge_schedule.py` | What is scheduled, by hour and day type | One 5 MB download, about a minute |
| `bridge_realtime.py` | What actually ran | Polls; a week takes a week |

Neither needs an API key, an account, or a payment method. Both use only the
Python standard library except `bridge_realtime.py`, which needs
`pip install gtfs-realtime-bindings protobuf`.

---

## Why not Google Maps

The originating thesis was that a week of Google Maps travel data would
establish running frequency. It will not, for three reasons.

**It is the wrong direction of travel.** Google Maps does not originate NYC
transit schedules. It ingests the MTA's published GTFS feed. Querying Google
means paying for, and accepting restrictions on, a redistribution of a file
the MTA gives away with no restrictions at all. The file is linked in
`bridge_schedule.py`.

**The Terms of Service forbid the use.** Google Maps Platform ToS prohibit
scraping and bulk export, and restrict how long results may be cached. A
week-long frequency census is precisely bulk extraction and long-term
storage. *(Rated 3/5 SNIPPET - read from secondary summaries of the ToS, not
from a legal reading of the current text. If this route were ever taken
seriously the actual clause would need reading.)*

**The API returns the wrong object.** Directions and Routes return
*itineraries* - "leave at 14:12, arrive 14:31". Frequency has to be inferred
by firing thousands of queries at staggered departure times and differencing
the results. That is expensive, lossy, and prohibited, to reconstruct a number
that is stated outright in a free file.

**Conclusion: go to the MTA feed directly.** It is the upstream source for
Google's own answer.

---

## The premise correction

> A week of normal travel data would establish day-time running frequency from
> **York St** and **East Broadway**.

Both of those stations are on the **F** line, through the **Rutgers Street Tunnel**. Neither is on the Manhattan Bridge. Verified against MTA's own
`stops.txt` and `trips.txt`:

| Station | `stop_id` | Routes serving it | On the bridge? |
|---|---|---|---|
| York St | `F18` | F, FX only | **No** - Rutgers Street Tunnel |
| East Broadway | `F16` | F, FX only | **No** - Rutgers Street Tunnel |
| Grand St | `D22` | B, D | **Yes** - north tracks |
| Canal St | `Q01` | N, Q | **Yes** - south tracks |

A week spent at York St would have measured the F train, which does not cross
the bridge and contributes nothing to the noise in DUMBO. The error is easy to
make - York St is the closest station to the affected blocks, and it is the
station a resident of DUMBO uses. It is just not the station the noise comes
from.

---

## Four traps, all of which silently produce a wrong number

These are not hypothetical. Each one was hit while writing these scripts.

**Trap 1 - `stop_name` is not unique.** "Grand St" is a B/D station in
Manhattan (`D22`) *and* an L station in Williamsburg (`L12`). "DeKalb Av" is a
Brooklyn bridge-side station (`R30`) *and* an L station in Bushwick (`L16`).
"Canal St" resolves to six different `stop_id` values. Any join on station
name silently merges platforms that are miles apart. **Always key on `stop_id`.**

**Trap 2 - DeKalb Av undercounts by about half.** It looks like the natural
chokepoint: everything from the bridge passes through it. It does not stop
there. **The D and the N run express and skip DeKalb**, running Grand St or
Canal St straight to Atlantic Av. Counting at DeKalb yields roughly 1,269 of
2,524 weekly crossings and gives no error message. The correct chokepoints are
**Grand St `D22` for B/D and Canal St `Q01` for N/Q** - every bridge train
stops at one of them.

**Trap 3 - route ID is not enough.** The R and the W never touch the bridge;
they use the Montague St tunnel. Worse, the **N is not consistently a bridge train**: of 717 weekly N crossings of the East River, 584 are via the bridge
and 133 via Montague. Filtering on `route_id == "N"` overcounts. The stop pair
has to be checked.

**Trap 4 - static and realtime disagree about `stop_id`.** The static feed
identifies the Canal St N/Q platform as `Q01`. The realtime feed was observed
emitting `R23` for the same trains. Filtering realtime on the static ID
returned 16 traversals where the true figure was 48 - **a 3x undercount, with no error and no warning**. `bridge_realtime.py` accepts both.

---

## The result

`bridge_schedule.py` output, feed `20260731-149-st-hostos`, valid
2026-05-26 to 2026-09-07. All four tracks, both directions.

| Hour | Weekday | headway | Saturday | headway | Sunday | headway |
|---|---|---|---|---|---|---|
| 00 | 16 | 225s | 17 | 212s | 16 | 225s |
| 01-04 | 12 | 300s | 12 | 300s | 12 | 300s |
| 05 | 15 | 240s | 14 | 257s | 13 | 277s |
| 06 | 42 | 86s | 26 | 138s | 24 | 150s |
| 07 | 58 | 62s | 31 | 116s | 29 | 124s |
| **08** | **67** | **54s** | 32 | 112s | 31 | 116s |
| 09 | 65 | 55s | 32 | 112s | 32 | 112s |
| 10 | 59 | 61s | 32 | 112s | 32 | 112s |
| 11 | 60 | 60s | 35 | 103s | 34 | 106s |
| 12 | 60 | 60s | 34 | 106s | 35 | 103s |
| 13 | 60 | 60s | 36 | 100s | 36 | 100s |
| 14 | 62 | 58s | 34 | 106s | 34 | 106s |
| 15 | 58 | 62s | 36 | 100s | 36 | 100s |
| 16 | 62 | 58s | 34 | 106s | 34 | 106s |
| 17 | 66 | 55s | 36 | 100s | 36 | 100s |
| 18 | 62 | 58s | 34 | 106s | 34 | 106s |
| 19 | 57 | 63s | 36 | 100s | 35 | 103s |
| 20 | 53 | 68s | 34 | 106s | 32 | 112s |
| 21 | 48 | 75s | 33 | 109s | 31 | 116s |
| 22 | 34 | 106s | 32 | 112s | 30 | 120s |
| 23 | 21 | 171s | 21 | 171s | 19 | 190s |

**Daily totals: Weekday 1,073 - Saturday 667 - Sunday 651.**

Per-route daily traversals:

| Day | B | D | N | Q | Total |
|---|---|---|---|---|---|
| Weekday | 220 | 296 | 242 | 315 | 1,073 |
| Saturday | **0** | 216 | 171 | 280 | 667 |
| Sunday | **0** | 216 | 171 | 264 | 651 |

**The B does not run weekends at all.** Weekend service is not "the same trains
less often" - the route mix changes, and with it the car classes, so the
weekend acoustic signature is not the weekday one attenuated.

---

## Three findings that were not being looked for

### 1. Peak park use and peak train frequency are out of phase

Brooklyn Bridge Park is most heavily used on weekend afternoons. That is when
bridge traffic is at its **lowest** daytime value: 34-36 per hour on a
Saturday against 57-66 per hour on a weekday afternoon - a factor of about
1.8.

Person-exposure is attendance multiplied by event rate, and the two move in
opposite directions across the week. Any exposure estimate that uses a
weekday headway with weekend attendance, or the reverse, will be wrong in a
direction that depends on which error it made. This programme has not built
such an estimate, and should not build one without resolving this.

### 2. The MTA's own train counts do not match the MTA's own schedule

From the section 1204-a noise sessions already recorded in `IDEA-CONCEPT.md`
section 1.2:

| Site | Trains counted | Session length | Implied rate | Implied headway |
|---|---|---|---|---|
| BBP dog run | 26 | 37:45 | 41.3/hr | 87s |
| DUMBO Archway | 18 | 25:35 | 42.2/hr | 85s |
| Adams St Library | 9 | 18:56 | 28.5/hr | 126s |

The weekday daytime schedule is **53-67/hr**. Weekend midday is **32-36/hr**.
Every measured session falls **below the weekday schedule**, and two of the
three fall **above the weekend schedule**.

Three candidate explanations, none verified:

1. The sessions were conducted at weekends or off-peak. This would fit 28.5
   and partly fit 41-42.
2. Service was rerouted during the measurement window.
3. **The observer counted audible events, not trains.** On a four-track
   crossing, two trains passing together are heard as one.

### 3. Explanation 3 would undermine this programme's own derived result

`IDEA-CONCEPT.md` section 1.7 derives event duration as

```
Te = (T*10^(Leq/10) - T*10^(Lbase/10)) / (N*(10^(Lmax/10) - 10^(Lbase/10)))
```

`N` is the train count, in the denominator. **If `N` is an event count rather than a train count, and events merge, then `N` is an undercount and `Te` is overestimated.** The published 5.70 / 6.28 / 7.25 s figures would then be
durations *per audible event* - which would also help explain why three
independent sites agree as closely as they do, since merging is a smoothing
operation.

How large is the effect? From the schedule, traversals falling within 6 s of
another traversal *at the same chokepoint*:

| Day | Merged pairs | Traversals | Distinct events | Loss |
|---|---|---|---|---|
| Weekday | 67 | 1,073 | 1,006 | 6.2% |
| Saturday | 21 | 667 | 646 | 3.1% |
| Sunday | 22 | 651 | 629 | 3.4% |

**That is a lower bound and it is a weak one.** It only counts pairs at the
same chokepoint, because a B/D at Grand St and an N/Q at Canal St reach the
bridge after different and unmeasured travel times, so cross-pair coincidence
cannot be computed from the schedule. It also inherits the schedule's coarse
time granularity - every coincidence found was at 0-3 s and none between 3 s
and 20 s, which is an artefact of scheduling to the minute, not a property of
the railway.

A single live snapshot showed a **minimum observed gap of 3 s** and two D
trains predicted at the identical second. **The real coincidence rate is an empirical question that only `bridge_realtime.py`, run for a week, can answer** - and it bears directly on whether section 1.7 is measuring what it
claims to measure.

---

## What these scripts still do not give you

**Schedule is not service.** `bridge_schedule.py` reports what is planned.
Delays, reroutes, planned weekend work and incidents all move the real number.

**Neither feed contains non-revenue moves.** Work trains, put-ins, lay-ups and
equipment moves cross the bridge and make noise - in some cases more noise,
since work equipment is not designed for ride quality. They appear in no
public feed. **Every figure here is a systematic undercount of acoustic events by an unknown amount.**

**Realtime is prediction, not observation.** `stop_time_update` carries the
MTA's estimate of when a train will reach a platform. It is revised as the
train approaches, and `bridge_realtime.py` keeps the last revision, but it is
never a measurement.

**A platform is not the bridge.** Grand St and Canal St are near the bridge,
not on it. Converting a platform time to a time over Brooklyn Bridge Park
needs a travel-time offset that has not been measured. For *rate* and
*headway* this cancels. For aligning a specific train to a specific acoustic
event - capture C4 in `FIELD-CAPTURE-PROTOCOL.md` - it does not, and it is
the reason C4 is the least certain capture in that document.

**Confidence.** The GTFS-derived numbers are 5/5 VERIFIED: they come from
MTA's own published feed, read directly, and both scripts reproduce them from
scratch. The Google Maps ToS position is 3/5 SNIPPET. The three findings
above are 2/5 UNVERIFIED interpretations of verified numbers, and the third is
written as a challenge rather than a claim.

---

## Usage

```bash
# What is scheduled. No dependencies beyond the standard library.
python bridge_schedule.py

# What is running right now.
pip install gtfs-realtime-bindings protobuf
python bridge_realtime.py --once

# What actually ran, over a week. Resumable - re-running with the same
# --out file reloads and continues.
python bridge_realtime.py --poll 30 --out bridge_week.csv
```

A 30 s poll against an 85-300 s headway samples every train several times
before it arrives. Shorter intervals gain nothing and are less polite to a
free public endpoint.
