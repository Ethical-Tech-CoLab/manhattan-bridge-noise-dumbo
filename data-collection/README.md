# Establishing train frequency over the Manhattan Bridge, and who is under it

Six scripts that answer four questions this programme had been asserting
answers to without ever deriving them: how many trains actually cross the
Manhattan Bridge and when, **how many people are underneath to hear them**,
**how long each of them stays**, and **what space they are standing in.**

| Script | Answers | Cost |
|---|---|---|
| `bridge_schedule.py` | What is scheduled, by hour and day type | One 5 MB download, about a minute |
| `bridge_realtime.py` | What actually ran | Polls; a week takes a week |
| `build_dashboard_data.py` | Per-event train data for the interactive dashboard | Seconds, after the download |
| `build_pedestrian_data.py` | **How many people are underneath, and when** | Four API pulls, about a minute |
| `build_cohort_model.py` | **How long they stay, and how badly that is identified** | About six minutes of arithmetic |
| `fetch_geodata.py` | **What shape of space they are standing in** | Two API pulls, about a minute |

None needs an API key, an account, or a payment method. All use only the
Python standard library except `bridge_realtime.py`, which needs
`pip install gtfs-realtime-bindings protobuf`.

**Interactive views:**
[`visual-review/frequency-dashboard.html`](../visual-review/frequency-dashboard.html),
[`visual-review/agent-model.html`](../visual-review/agent-model.html)
and [`visual-review/noise-canyon.html`](../visual-review/noise-canyon.html)

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

Three more, specific to the corridor geometry, are in
[the geodata section below](#what-shape-of-space-they-are-standing-in).

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

#### That replacement is also withdrawn

The paragraph immediately above was written before any pedestrian data existed.
It is now measurable, and it is wrong.

> **The worst case is not the park.** It is the corridor on a weekday morning,
> when the train rate is at its 24-hour maximum.

**That is withdrawn.** The 08:00 hour does carry the most trains - 67. It
carries **46% of the corridor's daily maximum number of people**. Multiply the
two and it scores **50 out of 100** on the exposure index. The actual maximum is
**14:00**, with about 3,780 people present against 62 crossings.

| Day type | Trains peak | People peak | Exposure peak | Index at 08:00 | Index at 13:00 |
|---|---|---|---|---|---|
| Weekday | 08:00 | 13:00 | **14:00** | 50 | 97 |
| Saturday | 13:00 | 13:00 | **13:00** | 23 | 100 |
| Sunday | 13:00 | 14:00 | **15:00** | 19 | 100 |

**This programme has now made the same error twice, in opposite directions.**
The first framing optimised on attendance alone and concluded the concern was
the park on a weekend afternoon. The correction optimised on train rate alone
and concluded it was the corridor on a weekday morning.
**Exposure is the product, and the product peaks in between**
- in the early afternoon, on every day of the week.

All three day types peak within two hours of each other despite carrying very
different train rates. The reason is that
**train rate is nearly flat from 07:00 to 19:00**
while presence changes by a factor of four inside the same window.
Where people are matters more than where trains are, and only one of those two
had ever been measured.

The index is deliberately **relative** - each day type scaled to its own
maximum. No absolute person-event figure is published, because presence here is
a lower bound covering only subway-delivered transients, and multiplying a lower
bound by a train count produces a number that looks authoritative and is not.

**What is verified and what is not.** The train rates are 5/5 `VERIFIED`.
Presence is 2/5, up from the 1/5 this section carried until the denominator work
below was done.
**No pedestrian has been counted directly anywhere in this corridor.**
What changed is that arrival rate is now derivable
from fare data, so the exposure index is a statement about shape rather than a
guess. An absolute exposure figure still cannot be published, because dwell time
is unmeasured and residents are not in the accumulation at all.

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

## Counting the denominator

`build_pedestrian_data.py` answers a question the train work could not:
**how many people are actually under the bridge, and when.**

It does not answer it completely. It closes one half of the problem and names
the other half precisely.

### The direction trap

The obvious move is to pull turnstile data at York St and High St. That
measures **the wrong direction**, and nothing in the data says so.

MTA's own column definition for the hourly ridership feed, quoted verbatim:

> Total number of riders that **entered** a subway complex via OMNY or
> MetroCard at the specific hour and for that specific fare type.

Entries are people *leaving* the corridor on foot-to-subway. The question was
about people *arriving*. Over a whole day the two roughly balance, so a daily
total would have looked fine. **By hour they are close to opposite** - at a
residential station, entries peak when residents leave and exits peak when they
return. Using entries as a proxy for arrivals produces a curve with the peak in
the wrong place.

The fix is the **Origin-Destination Ridership Estimate**, a separate MTA feed
that carries an inferred destination for each trip. Summed over all origins with
destination York St or High St, it gives arrivals by hour and day of week.

### Four sources, none of which counts a pedestrian

| Source | Host | Dataset | Gives | Rating |
|---|---|---|---|---|
| MTA Subway Hourly Ridership: Beginning 2025 | `data.ny.gov` | `5wq4-mkjj` | Entries, hourly, observed | 5/5 `VERIFIED` |
| MTA Subway Origin-Destination Ridership Estimate: Beginning 2026 | `data.ny.gov` | `28vm-gjqr` | Arrivals, hourly by day of week, **inferred** | 4/5 `VERIFIED` |
| Brooklyn Bridge Automated Pedestrian Counts | `data.cityofnewyork.us` | `6fi9-q3ta` | Walkway flow, hourly, **directional** | 4/5 `VERIFIED` |
| PLUTO tax lots | `data.cityofnewyork.us` | `64uk-42ks` | Residential units | 5/5 `VERIFIED` |

**None needs an API key.** All four were pulled with `urllib` and no
credentials. The Census API, by contrast, now refuses key-less requests with
`Missing Key`, which is why resident counts come from tax lots rather than ACS.

### What it found

Typical day, corridor total for both stations, EU 2002/49/EC periods:

| Day type | Period | Arrive by subway | Enter subway | Walkway to Brooklyn | Walkway to Manhattan |
|---|---|---|---|---|---|
| Weekday | Daytime | 18,074 | 16,401 | 7,147 | 6,605 |
| Weekday | Evening | 2,877 | 4,692 | 462 | 492 |
| Weekday | Night | 1,379 | 848 | 63 | 74 |
| Saturday | Daytime | 16,105 | 13,956 | 10,895 | 10,176 |
| Saturday | Evening | 2,615 | 4,320 | 875 | 751 |
| Saturday | Night | 1,106 | 1,046 | 68 | 108 |
| Sunday | Daytime | 14,551 | 12,106 | 8,886 | 8,008 |
| Sunday | Evening | 2,066 | 4,068 | 639 | 567 |
| Sunday | Night | 816 | 778 | 55 | 83 |

Subway figures are May 2026.
**Walkway figures are 2019, because the counter died in 2019**
and no live pedestrian counter exists anywhere near DUMBO. Of the
ten pedestrian-capable sensors NYC DOT currently operates, the nearest is at
Willis Avenue in the Bronx. The Brooklyn Bridge and Manhattan Bridge counters
that are still live are **bicycle-only** - including one named "Manhattan Bridge
Ped Path", which counts bikes.

### The corridor fills in the morning and empties in the evening

Net flow, arrivals minus entries, weekday:

| Hour | 06 | 07 | 08 | 09 | 10 | 12 | 14 | 16 | 18 | 20 | 22 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Net | +374 | +511 | +546 | **+800** | +590 | +183 | -14 | -332 | -454 | **-590** | -303 |

That is the signature of a **destination** district, not a dormitory. A purely
residential neighbourhood would show the opposite.
**The people under the bridge during the busiest train hours are**
**disproportionately not the people who live there.**
They are workers and visitors, and they are the population least
likely to appear at a community board meeting.

### A cross-check that was not designed in

Over a full day, arrivals and entries at the same two stations should balance.
They do:

| Day type | Arrivals (inferred) | Entries (observed) | Closure error |
|---|---|---|---|
| Weekday | 22,330 | 21,942 | +1.77% |
| Saturday | 19,827 | 19,322 | +2.61% |
| Sunday | 17,433 | 16,952 | +2.84% |

Two datasets built by entirely different methods - one counting fare
transactions, one inferring destinations from return swipes - agree to within
3% at the level of two station complexes.

**They are not fully independent.** The origin-destination estimate is scaled to
match total system ridership. But that scaling is system-wide, not per-station,
so agreement at this level is still informative. The residual is carried through
as the uncertainty band on the accumulation curve in the dashboard, rather than
being discarded.

The walkway figures were checked the same way: the typical-day profile implies
6,013,344 pedestrians in 2019 against a published annual sum of 6,011,174, a
0.04% difference attributable to rounding.

### Residents

| Study area | Lots | Homes | Residents |
|---|---|---|---|
| DUMBO and Vinegar Hill | 231 | 6,314 | 9,875-13,360 |
| Affected corridor | 376 | 10,128 | 15,840-21,431 |
| Wide catchment | 822 | 20,279 | 31,716-42,910 |

**Homes are a tax fact. Residents are an assumption** - units multiplied by 92%
occupancy and a household size of 1.7 to 2.3, reported as a range for that
reason and rated 2/5.

The boxes are stated as explicit coordinates in the script rather than borrowed
from a census geography, because **no census geography matches this corridor**.
DUMBO is not its own Neighborhood Tabulation Area; it sits inside `BK0202
Downtown Brooklyn-DUMBO-Boerum Hill`, an area of about 2.2 square kilometres.
Using that NTA would have overstated the affected population several times over
while appearing more official.

The "DUMBO and Vinegar Hill" box includes **Farragut Houses**, which sits
directly under the bridge approach. That is deliberate. It is public housing,
it is the closest large residential population to the structure, and any
framing that treats this as a question about loft conversions and a park has
already excluded the people most exposed.

### Little's Law, half solved

The number of people present in an area is `L = lambda * W` - arrival rate
multiplied by mean dwell time.

**This work produces lambda. It does not produce W.** A commuter walking from
York St to an office on Water St is exposed for four minutes. A family on the
Brooklyn Bridge Park lawn is exposed for three hours. Both count once in the
arrival figures.

Until dwell time is measured, the accumulation curve is
**a lower bound on transient presence, not a headcount**,
and it omits, in rough order of size:

- **Residents**, who are present whether or not they touch a turnstile. Almost
  certainly the largest omission, and the population whose exposure is
  continuous rather than episodic.
- **Walkway arrivals** - about 7,700 toward Brooklyn on a typical weekday in
  2019. Unknown today.
- **Every other mode** - the ferry at Fulton Ferry Landing, the B25 and B67, Citi
  Bike, private car, the Brooklyn Heights stair.
- **Mode-swapping.** Anyone who arrives by subway and leaves on foot over the
  bridge is counted arriving and never leaving. The small closure error suggests
  these flows roughly cancel. It does not prove it.

### Where this section is likely to be wrong

**The origin-destination hour is probably the origin hour, not the arrival hour.**
MTA's column description says only "the hour of the day in which the
subway trips occurred". If it is the entry hour, every arrival figure is
timestamped 10-25 minutes early, which shifts the accumulation curve left by
part of an hour. This has not been confirmed with MTA.

**Not everyone who arrives at High St is going to DUMBO.** High St also serves
Brooklyn Heights, and no allocation has been attempted. The same is true of
York St and Vinegar Hill. Arrivals are attributed to the corridor in full,
which overstates it.

**The walkway counter was on the Manhattan approach**, not the Brooklyn end.
Pedestrians who turned back mid-span are counted as heading to Brooklyn.

**2019 predates the 2021 promenade reconfiguration** that moved cyclists off the
walkway onto the roadway. Pedestrian volumes and behaviour will have changed in
ways the 2019 figures cannot show.

**One month is not a year.** May 2026 was chosen because it is the most recent
month present in both MTA feeds. Seasonality in a corridor with this much
tourist traffic is likely to be large and is not characterised.

---

## Who is actually here, hour by hour

The pedestrian work above produces a **flow**. Exposure needs a **stock**. Those
are different quantities and the gap between them is dwell time, which nobody
has measured in DUMBO.

`build_cohort_model.py` closes that gap by inference rather than measurement,
and the honest headline is that it half succeeds. It recovers a defensible
figure for *how many non-residents are present at a given hour*. It cannot
recover *who they are*, and the reason it cannot is a permanent property of the
data, not a limitation of the search.

### The model

Four cohorts, each with its own arrival profile and its own dwell
distribution. Presence at hour `h` is the arrivals in every earlier hour
multiplied by the probability that a person who arrived then has not yet left.

| Cohort | Arrival shape | Dwell | Source of the dwell figure |
| --- | --- | --- | --- |
| Workers | Gaussian, fitted | 8.5 h, sd 1.6 | assumed working day |
| Visitors | Gaussian, fitted | 2.31 h mean | Louisville waterfront survey, binned |
| Transients | follows the arrival curve | 0.35 h | assumed pass-through |
| Residents | present unless away | schedule, fitted | PLUTO units, corridor boxes |

The visitor dwell distribution is not a guess. It is a published survey with
seven duration bins, stratified by whether the respondent lived locally, and it
is applied at a 45% out-of-town share. Its mean is 2.31 h. What it is not is a
survey of Brooklyn.

Residents come from the PLUTO tax-lot count established in the section above:
**15,840 to 21,431 in the affected corridor, midpoint 18,636**. The corridor
box deliberately includes Farragut Houses.

### What it is fitted to

The only observable is the MTA hourly **entries** series - people leaving the
corridor through a turnstile. The model computes implied departures from its
own cohort presence and compares. The fit is a coarse grid over ten parameters
followed by two refinement passes.

| Day | RMS fit error | Same, over the resident window | Cost of the visitor prior |
| --- | --- | --- | --- |
| Weekday | 0.186 | 0.092 | +0.053 |
| Saturday | 0.127 | 0.014 | +0.064 |
| Sunday | 0.150 | 0.013 | +0.031 |

Ten free parameters against twenty-four data points is a generous ratio. A
good fit here is close to guaranteed and is therefore
**not evidence that the cohort structure is right**. It is evidence only that
the structure is capable of producing the observed curve, which is a much
weaker statement.

### The visitor prior, and what it costs

An unconstrained fit pushed the visitor arrival peak to a narrow spike at
19:00, which zeroed visitors during the day and let the long-dwell worker
cohort absorb every daytime arrival. Saturday came out with
**fifteen visitors**, which is absurd - a Saturday has more visitors than a
Tuesday, not four hundred times fewer.

Two constraints were declared:

- visitor arrivals peak no later than **16:00**
- the visitor arrival distribution has standard deviation of at least **2.0 h**

Justification is the FEIS, which places peak park attendance in the early to
mid Sunday afternoon. Saturday visitors moved from 15 to 2,153, Sunday from 9
to 2,944.

A declared prior that improves a result is exactly the kind of move this
programme is supposed to distrust, so **the prior is priced**. The script also
sweeps a strictly larger unconstrained grid and reports how much better the
unconstrained best fit is. That difference is the third column above: between
+0.031 and +0.064 RMS. The prior costs almost nothing in fit and changes the
answer by two orders of magnitude, which is the signature of a
**flat likelihood surface** rather than of a prior overriding evidence.

### The finding: cohort labels are not identifiable

The script does not report a point estimate. It sweeps the parameter grid and
collects **every** parameter set whose fit is within 10% of the best, then
reports the range of outcomes across that admissible family.

| Day | Admissible sets | Non-residents at 14:00 | of which workers | of which visitors |
| --- | --- | --- | --- | --- |
| Weekday | 9,248 | 6,029 to 7,338 | 3,629 to 5,490 | 1,460 to 2,313 |
| Saturday | 2,791 | 5,775 to 6,516 | 3,462 to 4,374 | 1,881 to 2,330 |
| Sunday | 11,590 | 5,932 to 6,820 | 2,619 to 3,911 | 2,541 to 3,137 |

Read the columns against each other. The **total** is pinned to about plus or
minus 10%. The **split inside it** swings by more than a factor of one and a
half on a weekday, across parameter sets that fit the observed data equally
well.

The reason is not subtle once stated.
**A departure curve carries no job titles.** Someone who is in the corridor for
eight hours looks identical whether they came to work or came for the day. The
only thing that distinguishes a worker from a visitor in this model is the
*shape* of their arrival, and a smooth aggregate curve can be decomposed into
two smooth components in a great many ways.

A degeneracy test makes this concrete. It measures the share of fitted worker
arrivals landing between 06:00 and 10:00 - if the "worker" cohort does not
arrive in the morning, the label is not doing any work.

| Day | Worker arrivals in the morning window | Verdict |
| --- | --- | --- |
| Weekday | 96% | label supported |
| Saturday | **33%** | **DEGENERATE - do not read this as workers** |
| Sunday | 63% | weak |

Saturday's best fit puts the "worker" arrival standard deviation at 5.6 h,
which is approaching uniform across the whole day. That parameter sits on the
edge of its grid and wants to go further. It has not been chased, because
chasing it would produce a smoother number that means even less: a cohort
arriving uniformly across a day is not a cohort, it is a residual.

**Consequence for anything downstream.** Total non-resident presence may be
quoted. The worker/visitor split may not be quoted at all on a Saturday, and
should be quoted only as a range on the other two days.

### The other thing the curve is not

Total presence, including residents, peaks in the evening on every day type -
weekday 13:00, Saturday 09:00, Sunday 13:00 for the totals, but the shape is
dominated by residents being at home. **That is not an exposure curve.**
Residents at home are indoors, behind a facade, and the one indoor measurement
in the record comes from a building whose occupants had already paid privately
to isolate it.

The non-resident curve peaks at 12:00 weekday, 14:00 Saturday, 15:00 Sunday,
which is consistent with the exposure-index result in the section above and
was arrived at by a completely different route.

### Where this section is likely to be wrong

**The dwell distribution is from Louisville, Kentucky.** It is real, published
and stratified. It is also about a different park, in a different city, on a
different river, with a different mix of tourists and no elevated railway over
it. This is the largest single transfer in the model and it is load-bearing.

**Ten parameters against twenty-four points.** The fit quality reported above
is close to meaningless as validation. The identifiability sweep is the only
part of this section that constitutes evidence about anything.

**Entries are still entries.** The model is fitted to the same series whose
direction trap is documented above. If the origin-destination hour is the entry
hour rather than the arrival hour, every arrival is timestamped early and the
fitted arrival Gaussians absorb the error silently.

**Residents are a stock with no measured schedule.** The away-fraction, leave
hour and return hour are all fitted, which means the resident cohort is the
most flexible object in the model and will absorb misfit from everywhere else.

**Nothing here is a headcount.** Presence is modelled. The word "modelled"
should survive every act of quotation, and if it does not, this section has
done net harm.

---

## Where the people go, not merely how many there are

`../visual-review/agent-model.html` is the next term again. The cohort model
supplies a duration; it has no position. Exposure is an integral of level along
a path, so a duration without a path is still not exposure.

The agent model is a demonstration of that mechanism and
**not a measurement of DUMBO**. It carries its own weaknesses list on the page.
Two results from building it are worth recording here because they bear on the
data work:

**A propagation model over the four MTA measurement points cannot be fitted.**
The three near-bridge sites agree with ideal line-source spreading to within
0.15 dB, which looks like a result and is not one: a Monte-Carlo test that
jitters the digitised positions by plus or minus 10 m puts the fitted decay
exponent anywhere between 0.7 and 22.3. The agreement is coincidence.

**Distance does not order the measurements, and that is robust.** The DUMBO
Archway sits directly under the structure and is the quietest of the four. The
Brooklyn Bridge Park site several hundred metres away is the loudest, and
exceeds a line-source prediction fitted to the near sites by about 17 dB. This
survives any plausible correction to the positions. It matters because
under-deck treatment - the intervention most often proposed, including in the
November 2025 residents' petition - would be applied where the measured problem
is smallest.

## What shape of space they are standing in

`fetch_geodata.py` answers the last question the other five leave open. The
frequency work established how often trains cross; the pedestrian and cohort
work established roughly how many people are underneath and for how long.
Neither says anything about the space itself, and the space is what turns a
source level into a received level.

Two public sources, no key, no account:

| Source | Supplies | Rows |
|---|---|---|
| NYC OpenData `5zhs-2jue` BUILDING | Footprint polygon, `height_roof`, `ground_elevation`, `construction_year` | 960 footprints in the corridor |
| OpenStreetMap via Overpass, ODbL 1.0 | Streets, footways, parks, water, coastline, piers, the subway alignment, station nodes | 2,826 ways and 9 nodes |

`build_carousel.py` in the repository root draws
[`../visual-review/noise-canyon.html`](../visual-review/noise-canyon.html) from
them. Slides are declared in `../visual-review/carousel.json`; the build refuses
to run if any slide lacks a source or a caveat.

**Three traps, in the same style as the four above.**

**Trap 5. Overpass returns 406 for a reason that has nothing to do with the query.**
Adding `Accept: application/json` is necessary and not sufficient. The
request also failed with a User-Agent containing parentheses and a semicolon -
the shape every browser uses - which trips the endpoint's request filtering. The
same query with a plain token User-Agent succeeds. The failure looks like a
malformed query and is not one.

**Trap 6. The building footprint dataset most search results point at is dead.**
`qb5r-6dgf` and `nqwf-w8eh` both return nothing. `5zhs-2jue` is the live one and
is the only one of the three that carries `the_geom`. Query it with
`within_box(the_geom, north, west, south, east)` - note the argument order.

**Trap 7. Chainage measured from a fitted axis can start in the river.** The
alignment is fitted by principal components to the OpenStreetMap track geometry,
which returns a centroid on the river span. Selecting a window around `s = 0`
then silently returns four buildings instead of seventy-six, with no error. The
origin has to be slid along the fitted axis to a landmark on land - here the
DUMBO Archway, which is also one of the four MTA measurement points.

**What came out of it that was not the point of it.**

The alignment this repository had digitised by eye for the agent model and the
alignment fitted to the open track geometry **differ in bearing by 2.3 degrees**.
That is an independent check on a number that had never had one.

Of the 77 objects in the massing frame, **76 are surveyed to the roof and one is not**,
and the one that is not is the elevated structure. No public source gives
the deck elevation over DUMBO. The drawing therefore renders 76 buildings as
solid geometry rated 5/5 and the bridge as a hatched assumed band rated 1/5 -
which is the honest rendering, and is also the argument.

Along the 1,482 m walk from the York Street F platform to Pier 1,
**347 m lies within a measured band - 23.4 per cent** - and those bands are drawn
as wide as the position uncertainty in the MTA memos rather than as points.

---

```bash
# What is scheduled. No dependencies beyond the standard library.
python bridge_schedule.py

# What is running right now.
pip install gtfs-realtime-bindings protobuf
python bridge_realtime.py --once

# What actually ran, over a week. Resumable - re-running with the same
# --out file reloads and continues.
python bridge_realtime.py --poll 30 --out bridge_week.csv

# Who is underneath. Four public datasets, no API key, no dependencies
# beyond the standard library. Writes pedestrian-data.json and injects
# it into the dashboard.
python build_pedestrian_data.py

# Per-event train data for the dashboard.
python build_dashboard_data.py

# Who is here at each hour, and for how long. Fits four cohorts to the
# observed departure curve, sweeps for identifiability, writes
# cohort-data.json and injects it into the dashboard. Takes about six
# minutes; --no-inject writes the JSON only.
python build_cohort_model.py

# What shape of space they are standing in. Building footprints with
# surveyed roof heights, and the street, park, water and footway network.
# Writes geo/buildings.json and geo/osm.json.
python fetch_geodata.py

# Then, from the repository root, draw the corridor from that geodata.
cd ..
python build_carousel.py
```

A 30 s poll against an 85-300 s headway samples every train several times
before it arrives. Shorter intervals gain nothing and are less polite to a
free public endpoint.
