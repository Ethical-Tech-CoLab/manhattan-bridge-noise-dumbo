# Establishing train frequency over the Manhattan Bridge

Two scripts that answer a question this programme has been asserting an answer
to without ever deriving it: **how many trains actually cross the Manhattan Bridge, and when?**

| Script | Answers | Cost |
|---|---|---|
| `bridge_schedule.py` | What is scheduled, by hour and day type | One 5 MB download, about a minute |
| `bridge_realtime.py` | What actually ran | Polls; a week takes a week |
| `build_dashboard_data.py` | Per-event data for the interactive dashboard | Seconds, after the download |

Neither needs an API key, an account, or a payment method. Both use only the
Python standard library except `bridge_realtime.py`, which needs
`pip install gtfs-realtime-bindings protobuf`.

**Interactive view:**
[`visual-review/frequency-dashboard.html`](../visual-review/frequency-dashboard.html)

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

### By noise period

Periods follow the EU Environmental Noise Directive 2002/49/EC Annex I default
split, quoted verbatim: *"the day is 12 hours, the evening four hours and the
night eight hours... the default values are 07.00 to 19.00, 19.00 to 23.00 and
23.00 to 07.00 local time."* (5/5 `VERIFIED`, primary text.)

| Day type | Period | Trains | Per hour | Hourly range | Mean headway | North / south |
|---|---|---|---|---|---|---|
| Weekday | Daytime | 739 | 61.6 | 58-67 | 58 s | 372 / 367 |
| Weekday | Evening | 192 | 48.0 | 34-57 | 75 s | 93 / 99 |
| Weekday | Night | 142 | 17.8 | 12-42 | 203 s | 71 / 71 |
| Saturday | Daytime | 406 | 33.8 | 31-36 | 106 s | 204 / 202 |
| Saturday | Evening | 135 | 33.8 | 32-36 | 107 s | 67 / 68 |
| Saturday | Night | 126 | 15.8 | 12-26 | 229 s | 62 / 64 |
| Sunday | Daytime | 403 | 33.6 | 29-36 | 107 s | 203 / 200 |
| Sunday | Evening | 128 | 32.0 | 30-35 | 113 s | 63 / 65 |
| Sunday | Night | 120 | 15.0 | 12-24 | 240 s | 59 / 61 |

**Direction is very nearly balanced in every period** - within a few percent
everywhere. Whatever asymmetry exists in the noise is not an asymmetry of
traffic.

**Note the weekday night range: 12 to 42.** The night period runs to 07:00, so
the 06:00 hour sits inside it, and on a weekday that hour carries 42 crossings.
Under the `Lden` convention the night period carries a +10 dB penalty and the
evening +5 dB, on the reasoning that the same sound does more harm at those
hours. That makes 06:00-07:00 the single most heavily weighted busy hour of the
day, and it is invisible in any framing that starts the day at 06:00. *(The
+5/+10 weightings are 3/5 `SNIPPET` - the Directive's formula is an image in
the source PDF and was read from secondary summaries. No penalty is applied to
any number in this repository; these are counts of events, not levels.)*

### The dashboard

[`visual-review/frequency-dashboard.html`](../visual-review/frequency-dashboard.html)
presents all of the above interactively - by hour, by route, by direction, by
day type - and lets you vary the coincidence window and the overlap model. It
is self-contained: no build step, no server, no network, no dependencies.

Rebuild its embedded data with `python build_dashboard_data.py`.

---

## Three findings that were not being looked for

### 1. Peak park use and peak train frequency are out of phase - narrowed

An earlier version of this file published the following:

> **Peak park use and peak train frequency are out of phase.** Brooklyn Bridge
> Park is most heavily used on weekend afternoons. That is when bridge traffic
> is at its **lowest** daytime value: 34-36 per hour on a Saturday against
> 57-66 per hour on a weekday afternoon - a factor of about 1.8.
>
> Person-exposure is attendance multiplied by event rate, and the two move in
> opposite directions across the week.

**The arithmetic is right. The generalisation is withdrawn.** It silently
assumed one receptor population - park visitors - and then spoke as if that
were the affected population.

The affected corridor is much larger than the park. It runs from the York St
station down to the water entrance to Brooklyn Bridge Park, and it contains at
least three populations with different daily and weekly rhythms:

| Population | Peak presence | Relationship to train rate | Phase |
|---|---|---|---|
| Residents | Every hour | Exposure tracks traversals directly; weekday is worst, and the daytime period alone carries 69% of the weekday total | **In phase** |
| Commuters and workers | Weekday morning and evening peaks | Peak corridor pedestrian flow coincides with the 24-hour maximum train rate | **In phase** |
| Park visitors and tourists | Weekend afternoons | Heaviest attendance against the lowest daytime train rate | Out of phase |

**There is no single phase relationship, because there is no single receptor population.** Two of the three are in phase; the withdrawn claim generalised
from the one that is not.

The sharper consequence: **the worst case is not the park.** It is the corridor
on a weekday morning, when the train rate is at its 24-hour maximum - **67 crossings between 08:00 and 09:00, a 54-second headway** - and the corridor is
carrying commuters. The original framing could not see that case, because it
was only looking at the park.

**What is verified and what is not.** The train rates are 5/5 `VERIFIED`. The
*presence* of people is 1/5 `UNVERIFIED`: no pedestrian count has been taken
anywhere in this corridor, by this programme or, so far as it has found, by
anyone. The phase argument is therefore a statement about which question to
ask, not an exposure estimate. **No exposure estimate should be built until the denominator is counted.**

There is also a resolution here of the premise correction above. York St is an
`F` train station and no train crossing this bridge stops there, so it is
useless as a place to *measure the source*. It is nonetheless the pedestrian
gateway to the affected corridor. **It matters as a receptor origin, not as a source** - which is why it felt relevant, and why measuring trains there would
still have measured the wrong thing.

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

How large is the effect? An earlier version of this file answered that with the
following table:

> | Day | Merged pairs | Traversals | Distinct events | Loss |
> |---|---|---|---|---|
> | Weekday | 67 | 1,073 | 1,006 | 6.2% |
> | Saturday | 21 | 667 | 646 | 3.1% |
> | Sunday | 22 | 651 | 629 | 3.4% |

**That is withdrawn.** It is not a weak lower bound, as was claimed at the
time. It is not a bound at all - it is an artefact of the feed's time
resolution, and it should never have been published as a quantity.

**Every scheduled departure in this feed falls on an exact :00 or :30 second.**
Across 1,073 weekday traversals there are exactly **two** distinct sub-minute
values. The schedule is quantised to 30 seconds, so the gap between two
consecutive crossings is never recorded as 1 s, or 4 s, or 12 s - the entire
range in which two trains would actually merge acoustically is empty by
construction.

The consequence is directly demonstrable, and
[`visual-review/frequency-dashboard.html`](../visual-review/frequency-dashboard.html)
demonstrates it live: set the overlap model to **Schedule** and drag the
coincidence window from 1 s to 29 s. The answer does not move - it sits at
50.3 events/hr the whole way - and then jumps to 33.0 the instant you cross
30 s. **Counting coincidences in the schedule measures the scheduler's rounding, not the railway.**

### What can honestly be said instead

Since the schedule cannot locate the answer, bracket it with two models that do
not depend on it. For the weekday daytime period (61.6 trains/hr) at a 6-second
coincidence window:

| Model | Assumption | Events/hr | Merging |
|---|---|---|---|
| **Regular** | Perfectly even spacing - least merging physically possible | 61.6 | 0% |
| **Poisson** | Maximum disorder - most merging plausible | 55.6 | 9.8% |

The Poisson figure is `N * exp(-lambda*w)` with `lambda = N/3600`. It is
defensible as a ceiling on merging because the superposition of several
semi-independent streams tends toward Poisson (Palm-Khintchine), and four
tracks is enough for that to be directionally right. Real operation is more
regular than Poisson and less regular than a metronome, so **the true value lies inside the bracket** - and the bracket narrows sharply at night, where
low rates make coincidence rare regardless of model.

At a 6-second window the merging ceiling is **9.8% by day, 7.7% in the evening, 2.9% at night**. So the discrepancy in the table above - the MTA
counting 28-42/hr against a scheduled 53-67/hr - is **too large to be explained by acoustic merging alone**. Merging can account for at most about
a tenth of it. That does not rule explanation 3 out, but it does mean
explanation 1 or 2 must be doing most of the work.

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
