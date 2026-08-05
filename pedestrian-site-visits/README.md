# Field media: what a consumer phone actually recorded under the bridge

**Page:** [`media.html`](media.html) &middot;
**Data:** [`media-data.json`](media-data.json) &middot;
**Analysis:** [`build_media_data.py`](build_media_data.py) &middot;
**Renderer:** [`build_media_page.py`](build_media_page.py) &middot;
**Harness:** [`verify_media.js`](verify_media.js)

This is the first material in this programme that was not retrieved from
somebody else. On 3 and 4 August 2026 an observer stood under the Manhattan
Bridge in DUMBO with a Samsung Galaxy S23+ and filmed the buildings that wall
the corridor on both sides of the alignment. Separately, an hour later, he
stood with the phone's stopwatch and tapped a lap every time train noise
started or stopped.

Every other document here argues from records: MTA memoranda, GTFS feeds,
Socrata datasets, GSA rate schedules, a HAER survey. This one argues from
fourteen taps on a screen, about two minutes of by-product audio, and a set of
photographs of a place this repository had until now only modelled.

## 0. What was corrected in v1.1, and why it matters more than what was kept

**Version 1.0 made a cross-instrument claim that is withdrawn.**
It is quoted in full in section 5 rather than deleted. The short
form: the audio duty cycle was used to refute one of the two possible readings
of the stopwatch, and it cannot, because the two are independent samples
**62.4 minutes apart with no overlap**.

The correction came from the operator, and it arrived as three statements of
intent:

> The stopwatch is an independent sample. There is no correlation between it
> and any video or audio also supplied.

> It is somewhat imprecise because a human operator decided when to start and
> stop the stopwatch. It was an indicator that there is a very small amount of
> time between noise from the train tracks. I will redo this with better
> documentation.

> The video was primarily used to show the buildings that create an echo
> chamber around the bridge near the water. That was the main value of them.
> It was not to be used for audio precision.

These are rated **5/5**. Every other piece of testimony in this document is
rated 2/5, because a recollection about what happened can be wrong. These are
not recollections about events. They are statements about *intent* from the
only person in a position to know it, and no analysis performed afterwards can
overrule them.

**A measurement can only be read for the purpose it was taken for.** The
analysis that produced v1.0 never asked what the captures were *for*. It
treated a video shot to photograph buildings as an acoustic instrument, and it
treated a hand-timed indicator as a data series to be reconciled with that
instrument. Both files are real and both numbers were computed correctly. The
inference joining them was invented by the analyst, not supplied by the field.

The net effect:
**this document's centre of gravity moves from the audio to the photographs.**
The buildings forming the echo chamber are the
thing the session was for, and they are the thing it delivered.

**Better capture is already scheduled.** The operator is re-running the
stopwatch with documentation of which tap was which, and capturing audio with
a microphone shield and an audio meter later this week. The acoustic content
here is superseded rather than supplemented when that arrives, which is the
reason to demote it now rather than defend it.

```
python pedestrian-site-visits/make_derivatives.py    # masters -> web/
python pedestrian-site-visits/build_media_data.py    # -> media-data.json
python pedestrian-site-visits/build_media_page.py    # -> media.html
node   pedestrian-site-visits/verify_media.js        # both themes
```

## 1. The refusal, first

**Nothing in this directory is a decibel.** That is not modesty. It is the
condition under which the material is admissible at all.

A phone running Android's default capture path applies automatic gain control.
A compressor that pulls the level down during a loud passage and lets it back
up afterwards writes its own release curve into the file. Anything computed
from the absolute value of those samples is a measurement of Samsung's
compressor. The microphone response is unknown and is not flat, and phone MEMS
capsules are routinely high-passed in hardware &mdash; which is exactly where
bridge structural radiation lives, so a spectrum from this material would be
missing the part that matters with no way to tell from the file that it is
missing. There was no calibration and no windscreen, and
[Document 5](../FIELD-CAPTURE-PROTOCOL.md) named both as the things that decide
whether a session is worth anything.

What survives all three is **timing**. AGC changes how loud a sample is; it
does not change when the sample was written. Onsets, durations, gaps and rates
are recoverable from a file whose absolute scale is worthless. Every
quantitative claim below is one of those four, and the unit on every chart is
`dBFS` &mdash; a number about the file &mdash; never `dB(A)`.

The MTA's `dB(A)` figures used everywhere else in this repository come from a
calibrated meter. **Nothing here is comparable to them**, and the temptation to
put the two on one axis should be resisted permanently.

## 2. What was captured

| capture | kind | where | length |
| --- | --- | --- | --- |
| `20260803_190055.jpg` | still | under the bridge, evening | &mdash; |
| `20260803_190152.jpg` | still | under the bridge, evening | &mdash; |
| `canyon-buildings-20260804_115319.mp4` | video | the canyon, walking | 61.8 s |
| `canyon-buildings2-20260804_115505.mp4` | video | the canyon, continued | 46.7 s |
| `grassy-knoll-20260804_115626.mp4` | video | the lawn, south of the bridge | 10.3 s |
| `grassy-knoll-20260804_120225.jpg` | still | the lawn, south of the bridge | &mdash; |
| `clock-screenshot_20260804_130719_Clock.jpg` | screenshot | stopwatch, paused | &mdash; |
| `Timer Lap start time...txt` | data | fourteen laps, exported | &mdash; |

The masters total 224.7 MB and are **not committed**. One of them is 114 MB,
which is over GitHub's hard per-file limit, and putting a quarter of a gigabyte
of phone footage into a research repository serves nothing. What ships is a
poster frame and an extracted audio track per video and a resized still per
photograph: 4.1 MB, a factor of 55. Every master is fingerprinted by SHA-256 in
`media-data.json` and on the page, so a master supplied later can be checked
against the one that was actually analysed.

Every capture carried GPS and full EXIF and none of it was stripped.

### The `.gitignore` nearly shipped a page of broken images

The patterns excluding the masters were written as `grassy-knoll-*.jpg` and
similar. A gitignore pattern with no leading slash **matches at any depth**, so
those patterns also matched the derivatives inside `web/` and silently excluded
them. The page would have been committed with every image broken and no error
anywhere in the build.

Caught by `git add -A -n pedestrian-site-visits` before committing, and fixed
by anchoring each pattern with a leading `/`. The slashes are load-bearing and
there is a comment in the file saying so.

## 3. Where the captures actually stood

Placed in the frame the rest of this repository already uses: distance along
the fitted track axis, and perpendicular distance from it. Chainage zero is the
DUMBO Archway, which is itself one of the four points the MTA measured.

| capture | chainage | offset | side | nearest MTA point |
| --- | --- | --- | --- | --- |
| `20260803_190152.jpg` | &minus;124.7 m | 161.9 m | WSW | Front and Pine St, 170 m |
| `20260803_190055.jpg` | &minus;121.6 m | 159.0 m | WSW | Front and Pine St, 167 m |
| `canyon-buildings-...mp4` | +74.7 m | 37.6 m | ENE | DUMBO Archway, 90 m |
| `canyon-buildings2-...mp4` | +91.5 m | 26.4 m | ENE | DUMBO Archway, 100 m |
| `grassy-knoll-...115626.mp4` | +138.3 m | 27.0 m | WSW | DUMBO Archway, 139 m |
| `grassy-knoll-...120225.jpg` | +163.6 m | 81.6 m | WSW | DUMBO Archway, 178 m |

The axis is imported from `build_carousel.py` rather than reimplemented, so
these numbers cannot drift from the drawings in
[the noise canyon](../visual-review/noise-canyon.html). It is fitted to 21
OpenStreetMap nodes tagged `railway=subway` on the bridge and is straight to
within 12.5 m over the 1,757 m it was fitted across.

**Two of the video captures stand 26 m and 27 m from the track.**
**Three of the four points anyone has ever measured are further from it.**
That is
not a claim these captures are better sited &mdash; they carry no calibration
and the MTA's do. It does mean geometry is not the reason nothing here is
comparable with a decibel.

### Two guards that exist because the first version was wrong

**The compass label was typed and it was backwards.** The first version of the
geometry table hard-coded `"north-east" if t > 0`. Probing the fitted axis
showed positive offset actually points 246.9&deg;, west-south-west, toward the
river. A refit that flipped the sign would have silently inverted every row.
The bearing is now derived from the fitted axis at runtime on a 16-point
compass.

**An axis is only a description where the fit lives.** A straight line fitted
to a railway says nothing about that railway outside the span of the fitted
points. `geo_context()` records the fitted span and asserts every capture falls
inside it. All do; `captures_within_fit` is `true`. An offset quoted outside
that range would be measuring distance from an imaginary line.

## 4. The stopwatch, and the inference the whole reading rests on

Fourteen laps, 12:59:00 to 13:07:19, one observer. The stopwatch records a lap
every time the observer judged train noise to start **or** stop, so the file
contains fourteen durations alternating between noise and quiet.

**It does not record which kind the first lap was, and nobody wrote it down.**
Both interleavings are arithmetically valid and they give
opposite answers.

| | odd laps are quiet | odd laps are noise |
| --- | --- | --- |
| events counted | 7 | 7 |
| mean event | 12.8 s | 51.0 s |
| median event | 7.3 s | 45.4 s |
| event spread, CV | 1.060 | 0.227 |
| gap spread, CV | 0.227 | 1.060 |
| implied duty cycle | 20.1% | 79.9% |

The cycle, and therefore the rate, is the same either way &mdash; 63.8 s,
56.4 an hour. Everything else inverts.

**The tie is broken on a property of the railway, not a preference.**
**Headway is scheduled and event duration is not.**
Trains are dispatched to a timetable, so
gaps between them should cluster; how long a given train sounds loud depends on
its speed, its length, which of four tracks it is on and where the observer is
standing, so events should scatter. The reading whose *quiet* intervals cluster
more tightly is the reading in which the quiet intervals are really quiet
intervals.

The two differ by **4.67&times;** in exactly that respect. Under the accepted
reading the gaps have CV 0.227 and the events scatter at 1.060. Under the
rejected reading those swap, which would mean the railway runs to no timetable
while every train sounds loud for almost exactly the same length of time.

That is a strong argument and it is still an inference. It is the load-bearing
assumption in this document and it is listed first in section 9.

**It now rests on that one argument alone.** Version 1.0 gave it a second and
apparently independent prop &mdash; an audio duty ceiling that seemed to rule
the other reading out. That prop is withdrawn in section 5, so the confidence
attached to the pairing, and to the event durations and duty cycle hanging off
it, drops with it. The data file marks the pairing `"confidence": "WEAK"` and
`"sole_support": true`.

### The operator's own reading points the other way

The operator describes the session as an indicator that there is

> a very small amount of time between noise from the train tracks.

That is ambiguous between two things **this stopwatch cannot separate**. It
may mean the *gaps* are short, which would favour the rejected pairing, where
gaps average 12.8 s. It may mean the *cycle* is short, which is
pairing-independent and is already established at 63.8 s &mdash; a train about
every minute, which anyone might reasonably describe that way.

It is recorded, not resolved. Reading it either way would be choosing the
answer. The ambiguity is itself the argument for re-running the stopwatch with
documentation, which the operator has said he will do.

### Only the cycle is pairing-independent

The cycle, and therefore the event rate, is identical under both pairings. It
is the one quantity here that does not depend on the tie-break, and it is the
only one carried forward into section 8.

### One event does not fit and it is not hidden

Lap 2 is 41.09 s against 18.63 s for the next longest of the seven and a median
of 7.3 s &mdash; a 5.6&times; outlier on the median. It is the first event of
the session, which is where a settling error would sit: a stopwatch started on
a train already passing, or a missed tap that makes one recorded duration span
two real intervals.

The lap was **not** dropped and the reading was **not** re-chosen to remove it.
The mean of the accepted reading is 12.8 s and the median 7.3 s, a gap this one
lap almost entirely accounts for, which is why the median is quoted beside the
mean throughout.

## 5. The audio, which is a by-product and is treated as one

The audio analysed here is the sound track of video shot to photograph
buildings.
**It was not captured for acoustic precision and is not used as though it was.**
It is used for exactly one thing that it can carry: showing
that one recording's microphone misbehaved, which is a claim about the
recording chain rather than about the corridor.

The detector was written and run before the stopwatch file was parsed. An
excursion is a stretch at least 1.5 s long sitting at least 6 dB above the
clip's own rolling median, with excursions less than 1.5 s apart merged.

**It is a level excursion, not a train.** The detector cannot distinguish a
train from a truck, from the operator's own footsteps as he walked, from
clothing against the handset, or from wind. On a corridor carrying heavy road
traffic under the same deck, recorded by someone walking through it, this is
not a marginal caveat.

Across 108.4 s of usable recording: **4 excursions, longest 10.10 s**, and the
duty cycle never exceeds **44%** at any detection threshold tested.

Those are statements about three files. They are not statements about the
corridor, and the next section withdraws the claim that treated them as such.

### The withdrawal

Version 1.0 of this document said:

> **That refutes the rejected reading robustly. It does not confirm the other.**
> The rejected stopwatch reading requires the corridor to be under
> train noise about 80% of the time with each event lasting about 51 s. The
> audio ceiling is 44% and the longest excursion of any kind is 10.10 s.

**That is withdrawn.** It was the strongest-sounding result in the document
and it was not a result at all. Two independent reasons kill it, either of
which is sufficient.

**First, the two instruments do not overlap.** The operator states there is no
correlation between the stopwatch and any video or audio supplied. The file
timestamps agree without being asked:

| instrument | from | to |
| --- | --- | --- |
| audio, 3 video clips | 11:53:19 | 11:56:36 |
| stopwatch | 12:59:00 | 13:07:19 |
| **gap** | **62.4 min** | **zero overlap** |

A duty cycle measured in one window places no constraint on a duty cycle in
another window an hour away. The arithmetic was right; the inference joining
the two was invented here and was never in the data.

That the operator's statement and the file timestamps agree is the strongest
form this evidence could take, **because they could have disagreed**. The
check is in [`build_media_data.py`](build_media_data.py) as `separation()`,
and it hard-exits if the two ever overlap.

**Second, and independently, the video was never an acoustic instrument.** It
was shot to record the buildings forming the echo chamber near the water. Its
audio track is a by-product of a visual record, captured while walking, and
cannot characterise an acoustic environment however carefully it is processed.

### What survives

Each instrument constrains itself and nothing else. Concretely:

- **The duty ceiling has no consumer.** Its only use was the refutation above.
  It is retained in the data as a property of three files and is used for
  nothing.
- **The threshold sweep is kept for the opposite reason it was built.** On the
  same audio it runs from 44% down to zero depending only on where the
  threshold is put. That is worth publishing as a caution against anyone
  &mdash; including this repository, which did it &mdash; quoting a single
  duty figure from uncalibrated audio.
- **The obstruction finding in section 6 is unaffected**, and section 6 says
  why.

## 6. A microphone was obstructed, and finding that out was worth more than the clip

After the recordings were made the operator volunteered two recollections about
the lawn clip:

> I may have had my hand over the microphone for the drop out period.

> Turned phone upside down at some point.

Both are rated **2/5, OPERATOR RECOLLECTION**. Recording a recollection as
evidence would be circular. Recording it as a *hypothesis* and then testing it
is not, and both tests were written after the recollection and were free to
disagree with it.

### The mono mixdown had to be undone first

The pipeline was mixing to mono. That destroys the only evidence that separates
a quiet site from an obstructed microphone, because both produce the same
envelope. A stereo decode path was added specifically to make the question
answerable.

### The first result was negative, and checking it found a blind spot

`channel_asymmetry()` found no sustained divergence in `|L-R|` and no sustained
sign change in `(L-R)`. Before accepting that, the detector was checked for
power: channel correlation runs 0.83&ndash;0.92, so the channels are genuinely
separable and the test could have fired. Printing the full envelope showed
**no drop-out at all** &mdash; the clip sits inside a 5.9 dB band for its
entire 10.2 s.

That looked like a clean negative. It is not, because the test has a blind
spot:
**it measures each clip against its own median, so an obstruction that never**
**lifts moves the baseline with it and becomes invisible.**

### The between-clip test, on three indicators that disagree by design

A hand over a microphone raises the noise floor, compresses the dynamic range,
and decorrelates the channels. A genuinely quiet site *lowers* the floor and
leaves the channels agreeing. The indicators point opposite ways for the two
explanations, which is what makes them a test rather than a description.

| clip | floor, dBFS | range, dB | correlation | flagged |
| --- | --- | --- | --- | --- |
| **grassy-knoll** &mdash; **excluded** | **&minus;17.9** | **3.5** | **0.826** | **3 of 3** |
| canyon-buildings | &minus;22.9 | 10.8 | 0.920 | 0 |
| canyon-buildings2 | &minus;24.2 | 7.6 | 0.885 | 0 |

**All three picked the same clip, unanimously.** Three indicators over three
clips cannot carry a p-value and none is claimed. The consequence does not
depend on resolving the cause: a clip that looks like that is unusable either
way.

The clip is excluded **at source**, before any statistic is computed, not
caveated afterwards. A caveat below a number does not stop the number being
quoted. The audio span in this document is 108.40 s rather than 118.68 s
because of it.

## 7. A null shorter than a headway is not a finding

The lawn clip is *closer* to the track than either canyon clip (27.0 m against
37.6 m and 26.4 m) and detected zero excursions. That has the shape of a
result. It is not one.

| clip | analysed | trains expected | observed | P(zero) by luck |
| --- | --- | --- | --- | --- |
| grassy-knoll | 10.3 s | 0.16 | 0 | **84.8%** |
| canyon-buildings2 | 46.7 s | 0.75 | 2 | 47.3% |
| canyon-buildings | 61.8 s | 0.99 | 2 | 37.2% |

At 57.7 trains an hour a 10.3 s window has an 84.8% chance of containing no
train at all regardless of how loud the site is. `detectability()` computes
this for every clip and marks the uninformative ones, so a zero count can never
silently become a claim about quiet.

This test was added after noticing the proximity, and it would have caught the
error even if the obstruction test had not.

## 8. The rate agrees with the timetable, within a wide interval

The accepted reading counts 7 events in 446.45 s, or **56.4 an hour**. The MTA
schedule for the same weekday window puts 8 trains across the bridge, or
**57.7 an hour**.

Seven events is a small sample. The 95% Poisson interval runs from
**13.8 to 99.0** an hour and the scheduled rate sits inside it.

This is the only figure here that touches an external source, and the direction
matters: the observed rate *could* have landed outside the interval, which
would have said the stopwatch reading was wrong. It did not. That is weak
positive evidence and it is reported as weak. It rules out gross error; it does
not establish agreement to a few per cent.

## 8.1 What was asked for and is not separately here

The capture list requested an **audio recording at Adams and John Street** as a
distinct file. No audio-only file exists in the material handed over.

That material appears instead to be *inside* the canyon videos. Both were shot
at 40.7044, &minus;73.9885 &mdash; the John Street block &mdash; and the poster
frame of the first carries a `John St / DUMBO Historic District` street sign
with the bridge deck filling the top third of the frame. Their audio tracks are
extracted and published as `.m4a`, so the recording exists; it is simply not a
separate capture.

This is recorded rather than quietly reconciled because the difference matters
for what comes next. A separate audio capture would have been made with the
phone held still and pointed. A video's audio track was made by someone walking
and turning. The second is worse for anything spectral and no worse for
anything temporal, which is all that is claimed from it.

## 8.2 Measured against the protocol this repository wrote for itself

| capture | asked for | status |
| --- | --- | --- |
| C1 spectrum | third-octave spectrum of a pass-by | **Not satisfied.** No windscreen, unknown response, AGC active |
| C2 envelope | measured envelope, to open the section 1.7 closed loop | **Partly, not usefully.** Durations usable; AGC deforms the rise and decay that section 1.7 assumes a shape for |
| C3 headway | ninety minutes of event timing | **Partly.** 446 s of stopwatch and 108 s of audio |
| C4 attribution | events matched to identified trains via GTFS-RT | **Not attempted** |
| C5 photogrammetry | structure-from-motion of the under-deck | **Not satisfied** |

[Document 5](../FIELD-CAPTURE-PROTOCOL.md) specified five captures before any
of this existed. This session satisfies none completely and two partly. That is
the honest score, and it is worth stating plainly because the temptation with
first field data is to let its existence stand in for its adequacy.

**C2 remains the one that matters.** Section 1.7 of
[Document 1](../IDEA-CONCEPT.md) solves event duration under an *assumed*
envelope shape, and the continuous mode of the acoustic demonstration converges
on the published `L`&#8202;`eq` because that is the number the shape was solved
from. That loop is still closed. This material does not open it, because AGC
deforms precisely the rise and decay the assumption is about. A UMIK-1 over
USB-C, about USD 100&ndash;150 with a serial-numbered calibration file, still
does.

**The equipment gap is closing this week.** The operator has stated he will
capture with a microphone shield and an audio meter. A shield addresses the
wind and handling noise that make C1 unsatisfiable; a meter addresses the
absolute scale that makes everything on this page a ratio. When that material
arrives, C1 and C2 become answerable for the first time, and the acoustic
content of this document is replaced rather than extended.

## 9. Where this is likely to be wrong

1. **The pairing inference is load-bearing and it is an inference.** Everything
   the stopwatch contributes rests on deciding which laps were noise. The
   tie-break is principled and the ratio is 4.67&times;, but it is one
   observer, fourteen laps, and no independent record of what the first tap
   meant. **It had a second prop in v1.0 and no longer does.** If the pairing
   is wrong, the event durations and the duty cycle are wrong together. The
   *rate* survives either way, because the cycle is identical under both.
2. **The stopwatch is an indicator, not an instrument, and its author says so.**
   A human decided when to start and stop it, which puts reaction time,
   anticipation and attention into every lap with no way to separate them. It
   is being re-run with documentation. Nothing derived from it should be
   treated as settled until that happens.
3. **The audio is a by-product of a visual record.** Every acoustic
   characterisation drawn from it has been withdrawn. What remains is one
   finding about the recording chain. If even that is over-read &mdash; if the
   between-clip test is picking up something about the lawn rather than
   something about the microphone &mdash; then the audio contributes nothing
   at all, and the honest position would be that only the photographs and the
   geometry survive.
2. **The observer knew what the study is about.** The same person who has been
   writing about train noise for weeks decided, in real time, when train noise
   started and stopped. Expectancy effects are not controlled for and cannot be
   recovered from the file.
3. **A level excursion is not a train.** Trucks, footsteps, clothing rustle and
   wind all qualify. Some of the four excursions may not be trains.
4. **Four excursions is not a sample.** Every audio statistic rests on four
   events in under two minutes of usable recording. Little survives that being
   an unrepresentative two minutes.
5. **The exclusion rests on three indicators over three clips.** No
   significance is claimed and none is available. With a different third clip
   the unanimity might not hold.
6. **The rate agreement could easily be coincidence.** An interval running from
   13.8 to 99.0 an hour would have accepted a very wide range of observed
   rates.
7. **The schedule is not the service.** Every timetable comparison inherits the
   known problems of GTFS static: no non-revenue moves, a plan rather than an
   observation, and departure times quantised to the half minute.
8. **The geometry rests on a fitted axis and digitised anchors.** The MTA memos
   give locations as descriptions, not coordinates. The offsets are good to
   tens of metres, not to metres.
9. **One handset, two days, one observer, one weather condition.** Nothing here
   establishes anything about a different season, time of day, wet rail, or a
   different phone.
10. **The largest error in v1.0 was not arithmetic.**
    Every number in the withdrawn claim was
    computed correctly. What was wrong was joining two things that were never
    joined in the field.
    **That failure mode is invisible to every check this directory runs**
    &mdash; the tests verify that numbers are computed
    correctly and that pages render, not that an inference between two
    datasets was licensed by how they were collected. The only defence is
    asking the person who captured the material what each capture was for, and
    that only happened here after publication.
11. **The operator notes came from the person who made the recording**, after
    the fact, with knowledge of what the recording was for.
    They are rated 2/5 for that reason. The between-clip test does not depend
    on them; it would have flagged the clip had they never been offered.
    **The statements of intent in section 0 are a different kind of thing**
    and are rated 5/5 &mdash; nobody else can say what a capture was for.

## 10. What this changes, and what it does not

It does **not** change any published number about the bridge. No decibel here,
no exposure figure, no revision to any MTA-derived quantity.

What it changes:

- **The echo chamber is photographed.** Until now
  [the noise canyon page](../visual-review/noise-canyon.html) drew the corridor
  from 76 surveyed footprints and OpenStreetMap ways, with nobody having stood
  in it. These frames are the first photographic record here of the geometry
  that page models. They do not measure it; they show that the modelled canyon
  and the built canyon are the same place.
  **This was the purpose of the session and it is what the session delivered.**
- **The receptor is photographed.** The lawn frame is the only image in this
  repository showing people, in the corridor, under the deck, including a
  family group with a pushchair. It is not a count. It is the population the
  cohort model has only ever inferred from turnstile arithmetic.
- **The captures are placed against the measured points.** Two stand 26 m and
  27 m from the fitted track axis, closer than three of the four points anyone
  has ever measured. That is geometry from embedded GPS and is unaffected by
  everything withdrawn above.
- **The observed rate agrees with the timetable at this location**, weakly, in
  the first check of the schedule against anything observed on the ground. It
  is the one stopwatch quantity that does not depend on the pairing.
- **One recording is known to be defective, and was known before disclosure.**
  That is a finding about method, not about DUMBO, and it is the
  only thing the by-product audio establishes.

What it explicitly does **not** change, after the withdrawal in section 5:

- **There is no measured duty cycle for this corridor.** The 44% figure is a
  property of three files and constrains nothing.
- **There is no empirical anchor on event duration.** v1.0 offered one by
  placing the stopwatch median beside the longest audio excursion and calling
  the pair a range. Those are two unrelated samples an hour apart and that
  range is withdrawn. Section 1.7 of [Document 1](../IDEA-CONCEPT.md) remains
  unchecked against anything observed.

## 11. The question this opens

**Q56.** **Which way does automatic gain control bias a duty cycle, and by how much?**

This question was framed in v1.0 to defend a number that is now withdrawn. It
is kept, and its value has changed rather than disappeared: it is no longer
about rescuing one figure, it is about whether **any** duty cycle can be
computed from consumer capture &mdash; including from the shielded, metered
capture arriving this week, which will still run through a compressor unless
the capture path is explicitly changed.

A duty cycle of this kind is computed by counting the fraction of a clip
sitting above a threshold relative to that clip's own rolling median.

**That estimator and automatic gain control interact, and the interaction has**
**a sign.**
A compressor pulls loud passages down toward the median and lets quiet
stretches back up. Both movements shrink the measured excursion above the
median. So a duty cycle computed from AGC-processed audio is **biased low**,
and by an unknown amount.

The direction is arguable from first principles. The magnitude is not. It could
be 1% or it could be 20%, and nothing in this repository distinguishes those.

**This is answerable on a bench, in an afternoon, for nothing.** Play a
synthetic signal with a known duty cycle through a speaker, record it on the
same handset through the same default capture path, and compute the same
statistic. The known input gives the answer directly. Repeat under
`AudioSource.UNPROCESSED` &mdash; which [Document 5](../FIELD-CAPTURE-PROTOCOL.md)
establishes is queryable on Android &mdash; and the difference between the two
runs isolates the compressor from everything else in the chain.

Three outcomes, all useful:

- The bias is small, and duty cycles from consumer capture are usable with a
  stated correction.
- The bias is large, and **no duty figure from a phone means anything** unless
  the capture path is changed first &mdash; which would apply to the new
  material as much as to the old.
- The bias depends on the signal, in which case no duty cycle of this kind is
  computable from consumer capture at all, and Document 5's claim that
  *relative* quantities survive an uncalibrated chain needs narrowing.

**There is no way to find out this is wrong except by running it**, and it
should be run *before* the shielded capture rather than after, because it
determines whether that capture needs `UNPROCESSED` enabled to be worth
taking.

## 12. Ethics

People appear in two frames at a distance, in a public park, incidentally and
unidentifiably. No frame was selected for a person in it, no face is resolvable
at the published size, and the published audio carries no intelligible speech.

That is the position [Document 5](../FIELD-CAPTURE-PROTOCOL.md) set out and it
is carried voluntarily: this programme argues for the interests of the people it
would incidentally record, so it takes the burden rather than waiting to be
made to.
