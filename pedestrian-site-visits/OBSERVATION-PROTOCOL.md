# Document 11 — The pedestrian observation protocol

**Ten things a person walking through DUMBO can count, each of which moves a number this repository currently invents. With a submission path that keeps provenance, and the arithmetic that makes a null result worth reporting.**

Ethical Tech CoLab · v1.0

---

## Why this document exists

This repository has a lopsided evidence base and has said so since Document 7.
Everything about **trains** is measured: 1,073 weekday crossings, a 58-second
daytime headway, 87.50 dB(A) at the dog run, all 5/5 VERIFIED from agency
sources. Almost everything about **people** is modelled: group sizes, walking
speeds, dwell times, itineraries, who is carrying a baby, whether anyone has a
dog. Those are rated 1/5 and they are the reason no absolute exposure figure
has ever been published here.

The gap will not close by more arithmetic. Document 8's cohort model proved
that: ten free parameters against twenty-four data points, 9,248 parameter sets
fitting equally well, and a worker/visitor split that swings by more than a
factor of 1.5 across all of them. **A departure curve carries no job titles.**
No amount of further fitting supplies a fact that was never observed.

What closes it is somebody standing on a corner with a clicker.

This document is the list of what to click. It exists because that person needs
to know three things before they start, and none of them is obvious:

1. **Which number their count would move**, so the hour is not wasted on
   something already known or already unusable.
2. **What rating their count would carry**, so they can see in advance whether
   it will be believed.
3. **What a result of zero means** — because several of these observations will
   return zero, and a volunteer who thinks zero is a failed session will stop
   after one.

---

## The rule that governs the whole list

> **An absence, counted, is data. An absence, remembered, is not.**

This is the single most useful idea here and it came from an operator's own
remark, which is worth quoting because it is exactly the shape of thing that
usually gets discarded:

> People ride the subway every day, so do I. I *never* see dogs being brought
> on the subway. I mean, in a year, maybe 1 time of everyday travels.

As stated, that is a recollection, and this repository rates operator
recollections of events **2/5**. It cannot be used. It is not weak because the
operator is unreliable; it is weak because nobody wrote anything down, so there
is no denominator and no way for it to have come out otherwise.

Now write it down. A year of weekday round trips is roughly 500 rides. One dog
in 500 is 0.2%, and a count of one event in 500 trials carries a computable
95% interval of **0.005% to 1.1%**. That is a *sharper* number than most of
what this repository has about people, and it costs nothing but a note on a
phone twice a day.

**The same observation went from unusable to load-bearing purely by acquiring a denominator.** That is what this protocol is for.

### The arithmetic of a zero

Observers stop when they see nothing, because nothing feels like no result. It
is not. If an event does not occur in `n` independent trials, the 95% upper
bound on its rate is close to `3 / n` — the statistical rule of three.

| Trials with zero events | 95% upper bound on the rate |
| --- | --- |
| 20 | 15% |
| 50 | 6% |
| 100 | 3.0% |
| 250 | 1.2% |
| 500 | 0.6% |
| 1,000 | 0.3% |

So a session that sees nothing still bounds the thing it did not see, and the
bound tightens with effort in a way the observer can watch happening. **Record the denominator even when the numerator is zero.** A count of "0 dogs" is
worthless. A count of "0 dogs in 143 boardings observed between 08:10 and 09:05
at York St, northbound platform" is a published figure.

---

## What makes a count usable here

Every observation below has to satisfy five conditions, and they are listed
first because an hour spent counting the wrong way is an hour that produces a
number nobody can use — including a number that is *wrong in a way nobody can
detect*, which is worse than no number at all.

1. **A mechanical rule.** The decision to click must not require judgement. "A
   dog" is mechanical. "A tourist" is not — so the protocol below never asks
   anyone to classify a tourist, and asks instead for something visible.
2. **A denominator.** Every count is a count *out of* something. Rides taken,
   minutes elapsed, people passing the line. Without it the count is an anecdote
   with a number attached.
3. **A stated position and time.** Not "under the bridge" — a corner, and a
   clock time. Two of this repository's existing photographs were re-filed
   entirely once their embedded position and timestamp were read, because those
   two fields changed what the frames could be used for.
4. **A stated purpose, written before the count.** Document 10 v1.1 withdrew a
   published headline because two correctly-computed datasets were joined that
   had never been joined in the field. The defence against repeating that is to
   record what a capture was *for* at the moment it is taken. **A measurement can only be read for the purpose it was taken for**, and only the person who
   took it can say what that was.
5. **Whatever went wrong.** The single most useful line in any submission is the
   one describing the thing that spoiled it. An operator's disclosure that his
   hand may have covered a microphone is why one recording is correctly labelled
   rather than silently wrong.

---

## The ten observations

Ordered by how much they move, not by how easy they are. The two at the top are
the two the whole exposure argument is blocked on.

### O1 — Dwell: how long a person stays

**Registered as Method 28. The single blocking unknown for any absolute exposure figure in this repository.**

| | |
| --- | --- |
| **What you count** | Pick a line across a footway. For each person crossing it inbound, note the clock time. Watch for the same person crossing back out, note that time. Stop at 90 minutes. |
| **Denominator** | People who crossed inbound during the session, including the ones you never saw leave. |
| **Where** | Any single cordon line: the top of the York St stairs, the Washington St / Water St corner, the park entrance at Old Dock St. |
| **Moves** | The cohort model's dwell distribution (`data-collection/build_cohort_model.py`), and through it every occupancy figure on the frequency dashboard. |
| **Would be rated** | 4/5 if the cordon line and session bounds are stated; 2/5 without them. |
| **A null means** | There is no null. Every session produces a distribution. |

**Why it is first.** Little's Law gives `L = λW`. This repository has measured
`λ` — arrivals, from MTA origin-destination data, 4/5 — and has never measured
`W`. A commuter walking from York St to Water St is exposed for four minutes; a
family on the lawn for three hours. Both currently count once, and they differ
by a factor of forty.

**The trap, stated because it would inflate the answer tenfold.** Measure dwell
*in the park* and apply it *corridor-wide* and every exposure figure grows by
about an order of magnitude while looking like a measurement. Say where the
cordon was.

**What the model most needs is the bottom of the distribution, not the mean.**
The agent model's shortest-dwell decile sits at a modelled 430 s — about seven
train crossings. Everything the arrival-process result rests on depends on that
being roughly right. Q63 asks whether a cohort exists whose corridor time
approaches a single 58-second headway, because if one does, several published
nulls stop holding. Count the *fast* people carefully; they are the ones the
model is least sure about and most exposed to being wrong about.

---

### O2 — Dogs boarding a train

**The observation that prompted this document.** Directly tests a constant in
the agent model against the reasoning printed beside it.

| | |
| --- | --- |
| **What you count** | Dogs, of any size, entering or leaving a subway car you can see into. Note whether the animal is in a carrier or on a lead. |
| **Denominator** | Rides taken, or better, boardings observed — people who got on the same car. |
| **Where** | Anywhere on the system. The B, D, N and Q are the noise-relevant lines; York St (F) and High St (A/C) are the corridor's own stations and neither carries a bridge train. Record which line. |
| **Moves** | `PERSONAS[*].dogRate` in `visual-review/agent-model.html`, and through it the noise-sensitive-dog class in the susceptibility layer. |
| **Would be rated** | 4/5 with a denominator. 2/5 as a recollection, which is what it is now. |
| **A null means** | A great deal. See the rule of three above. |

**The specific thing it would settle, and there is a live discrepancy.** The
model's schema comment read, until this document was written:

> `dogRate  0..1  probability this group brings a dog. Near zero for anyone
> arriving by subway: the MTA requires a dog to travel in a container, so dogs
> in the corridor are walked from home rather than carried off a train.`

The reasoning is sound. But the three personas that arrive **by subway** carry
`dogRate` values of 0.02, 0.04 and 0.01 — and 4% is not "near zero" if the
observed rate is nearer 0.2%. **The model's own documentation and its own constants disagree by up to a factor of twenty, and nobody has noticed because nobody has counted.** One commuter with a notes app settles it.

**What has been done about it, and what deliberately has not.** The model page now carries the disagreement on its own face — the schema comment states the constants and says plainly that they are not near zero, and the weaknesses list records the factor of twenty. **The constants have not been changed.** Replacing one unmeasured number with another unmeasured number chosen to match the prose would make the page self-consistent and no more true, and it would remove the visible disagreement that is currently the most useful property of this input. The disagreement is left standing until a count closes it.

Three outcomes, all publishable:

- **Observed rate near zero.** The comment is right, the constants are too high,
  the dog-walking population in the corridor is almost entirely resident, and
  the susceptibility layer's dog class should be driven from resident numbers
  rather than from transit arrivals.
- **Observed rate near 2-4%.** The constants are right and the comment is
  over-stated. Say so and delete the comment.
- **Observed rate varies by line or hour.** The most interesting outcome, and
  the one neither the comment nor the constants can currently express.

---

### O3 — Arrivals over the Brooklyn Bridge walkway

**The dataset that died. There is a real hole here and it is dated.**

| | |
| --- | --- |
| **What you count** | People passing a line at the Brooklyn end of the walkway, split by direction. Ten-minute blocks. |
| **Denominator** | Minutes counted. |
| **Where** | The walkway descent at Washington St / Prospect St, where the bridge path lands. |
| **Moves** | The pedestrian accumulation curve in `data-collection/build_pedestrian_data.py`, which currently carries walkway arrivals from a **2019** profile because the counter stopped. |
| **Would be rated** | 4/5 for a stated line, direction split and block length. |
| **A null means** | Not applicable; this one always returns a number. |

NYC OpenData's hourly directional Brooklyn Bridge walkway counter
(`6fi9-q3ta`) **has published nothing since 2019**. Its 2019 profile is still
what this repository uses, and it is doing so across a pandemic, a tourism
collapse and a recovery. Nobody knows the size or the sign of the error.

There is no live pedestrian counter anywhere near DUMBO. All ten of NYC DOT's
pedestrian-capable sensors are elsewhere. The live counters here are
**bike-only** — including one named "Manhattan Bridge Ped Path" whose
`travelmodes` field reads `bike`.

Two hours at the landing, done twice, would be the most recent walkway
pedestrian data in existence for this location.

---

### O4 — Group size and composition

| | |
| --- | --- |
| **What you count** | Parties crossing a line. For each: heads in the party, and whether it includes a pram, a wheelchair or a walking aid, a dog on a lead, or a child under about three being carried. |
| **Denominator** | Parties counted. |
| **Where** | Any of the O1 cordon lines. Rides along with O1 at no extra cost. |
| **Moves** | `PERSONAS[*].group` weights in the agent model — currently **invented and rated 1/5** — and the "carried infant" and "mobility" shares in the susceptibility layer. |
| **Would be rated** | 4/5 for the observable attributes. |
| **A null means** | A zero count of prams or wheelchairs is itself the finding. See the note below. |

**Three of the six susceptibility classes are not observable and this observation cannot supply them.** A pram is visible; hyperacusis, autism and a
cancer history are not. Those three will stay at national prevalence, and the
protocol says so rather than implying a street count could reach them. This is
Method 42's honest half.

**A zero count of prams under the bridge would be the most important result in this document.** The agent model's own weakness list already states the problem:
nobody in the model is prevented from coming at all. If the noise is why a
parent does not push a pram under the bridge, then the people most sensitive to
it are the ones most likely to be **missing**, and the model would report that
as low exposure rather than as exclusion. A pram count that comes back near
zero under the span and normal two blocks away is the difference between those
two readings — and it is a comparison, so it needs no instrument.

---

### O5 — Trains audible, and whether two overlap

**Answers a question the published schedule provably cannot.**

| | |
| --- | --- |
| **What you count** | Standing in one place for ten minutes: how many times bridge-train noise starts, and for each, whether a second one began before the first had faded. |
| **Denominator** | Minutes. |
| **Where** | A single fixed spot, stated. Do it at three: under the span, one block off, three blocks off. |
| **Moves** | Method 41 (the two-train case) and the merged-event question behind the section 1.7 duration derivation. |
| **Would be rated** | 3/5 — the judgement of "audible" is not fully mechanical, and the protocol should not pretend otherwise. |
| **A null means** | Zero overlaps in a stated number of minutes bounds the overlap rate by the rule of three. |

**Why no amount of schedule analysis reaches this.** Every scheduled departure
in the MTA feed falls on an exact `:00` or `:30` second. Across 1,073 weekday
traversals the sub-minute values are `{0: 528, 30: 545}` — two distinct values,
nothing else. The gap histogram has 154 pairs at 0 s, 279 at 30 s, 198 at 60 s,
and **nothing between 0 and 30**. The entire range in which two trains merge
acoustically is empty by construction. A merged-pair table computed from that
feed was published here once and withdrawn for exactly this reason.

So the only way to find out whether two trains on the bridge sound like one
event twice as loud, or one event twice as long, is for a person to stand there
and notice. Energy addition predicts `+3.01 dB` for two identical sources; what
a listener reports may differ, and the difference between those two is a real
finding either way.

---

### O6 — Where the canyon stops

| | |
| --- | --- |
| **What you count** | Walk a straight line away from the span. At each intersection, wait for a train and note whether you could hold a normal conversation through it: yes / with effort / no. |
| **Denominator** | Intersections, and trains waited for at each. |
| **Where** | Three radials: inland up Washington St, east along Water St, and south-west to Fulton Ferry. |
| **Moves** | Method 31, the decay transect, and Q51 — where the affected zone ends. |
| **Would be rated** | 3/5. It is a perceptual scale, not a decibel, and it must never be converted into one. |
| **A null means** | If conversation is unaffected at every point including directly beneath, that contradicts an agency measurement of 87.50 dB(A) and the recording chain or the session should be checked before anything is published. |

This is the one observation an uncalibrated human is **better** at than a cheap
instrument. Speech interference is a defined, well-studied effect; a phone's
automatic gain control actively destroys the decay tail that a listener hears
without difficulty. The protocol asks for the perceptual judgement and forbids
the conversion, because converting it would manufacture a decibel out of an
opinion.

The corpus asserts a "noise canyon" — 17 buildings cut, 91.22 m between nearest
facades, height-to-width 0.29 — entirely from surveyed footprints. **Nobody has walked out of it and recorded where it stopped.**

---

### O7 — The photograph stop

**Comes directly from an operator observation about evening tourists.**

| | |
| --- | --- |
| **What you count** | Parties that stop to photograph, and roughly how long they stop for: under 30 s, 30 s to 2 min, over 2 min. |
| **Denominator** | Parties passing the same point. |
| **Where** | The Washington St / Water St view of the bridge; the Main St park entrance; the Empire Stores frontage. |
| **Moves** | The long tail of the dwell distribution (Method 28) and the visitor scenario weights in the agent model. |
| **Would be rated** | 4/5. |
| **A null means** | Not applicable. |

A photograph stop is dwell in place, at a fixed location, at a known distance
from the track. It is the mechanism by which visitor dwell gets its tail, and
the tail is what makes visitor exposure differ from commuter exposure. It is
also trivially countable and requires no interaction with anybody.

Two existing photographs in this corpus were re-filed into the pedestrian cohort
study once it was established what they had been taken for — evening tourists on
a weekday. Their embedded position and timestamp survived; a count would have
survived better.

---

### O8 — Ear-covering

| | |
| --- | --- |
| **What you count** | People visibly covering their own ears, or covering a child's ears, during a pass-by. |
| **Denominator** | People present during the pass-by, and pass-bys observed. |
| **Where** | Directly under the span, and at one control point three blocks away. |
| **Moves** | The susceptibility layer's refusal. It does not supply a dose-response, but it is the only *behavioural* evidence of intolerance that requires no instrument and no interview. |
| **Would be rated** | 3/5. The behaviour is unambiguous; attributing it to the train is an inference. |
| **A null means** | Genuinely informative. A rate of zero under the span would be evidence against the strongest version of the intolerance claim, and this repository should want to know that. |

The susceptibility layer refuses to compare the MTA's 98.90 dB(A) peak against
the loudness-discomfort levels in the audiology literature, because dB(A) and
dB HL are not the same units and bridging them needs a third-octave spectrum
that does not exist for this bridge. That refusal is correct and it leaves the
layer with no behavioural evidence at all. This is the cheapest available.

**The control point is not optional.** Ear-covering happens for reasons other
than trains. Without a comparison point the count means nothing.

---

### O9 — Windows facing the bridge

| | |
| --- | --- |
| **What you count** | On one block face directly exposed to the span, and one sheltered block face at similar height and season: windows open, windows closed. |
| **Denominator** | Windows visible. |
| **Where** | Stated block faces, stated side, stated hour, mild weather only. |
| **Moves** | Q44 — the private mitigation spend nobody has ever summed. |
| **Would be rated** | 2/5, and it is here honestly at 2/5 rather than being dressed up. |
| **A null means** | No difference between exposed and sheltered faces is a real result and would count against the private-mitigation story. |

DumboNYC.com maintained a list of insulation contractors. Residents have been
paying privately to solve this since at least 2008, and the total has never been
added up. An open/closed window ratio is a crude proxy and its confounders are
obvious — orientation, sun, rent tier, whether the unit has air conditioning.
It is included because it is the only route to Q44 that does not require asking
anybody for their receipts, and because stating a weak observation as weak is
cheaper than pretending it is unavailable.

---

### O10 — The York St to water's edge walk

**Already in the backlog as a drawn route. This is the counted version.**

| | |
| --- | --- |
| **What you count** | Walk from the York St F platform straight to the water, then along the shoreline past Jane's Carousel to Fulton Ferry Landing. Log: elapsed time at each named waypoint, trains audible en route, and the points where the sound noticeably changes. |
| **Denominator** | The walk itself; repeat it at three different hours. |
| **Where** | The route above, which is the walk people actually take. |
| **Moves** | The corridor transit-time assumption in the agent model, O6's decay question, and the drawn walk in the noise canyon carousel, which currently stops at the water's edge. |
| **Would be rated** | 4/5 for the timings, 3/5 for the audibility notes. |
| **A null means** | Not applicable. |

This route crosses the one geometry this programme keeps asserting and has never
walked end to end: it goes under the bridge, out from under it, and back into
its shadow at Fulton Ferry. It is the cheapest single trip that touches four
open questions at once.

---

## How to submit an observation, and how provenance is kept

### The requirement

An observation that arrives without provenance cannot be used, and this
repository would rather refuse it than quietly downgrade everything around it.
So the submission path is built to make the provenance fields **structurally required** rather than politely requested.

### Route 1 — a GitHub issue form (preferred)

Two forms live in [`.github/ISSUE_TEMPLATE/`](../.github/ISSUE_TEMPLATE):

| Form | For |
| --- | --- |
| **Field observation** | A count. Requires which observation, where, when, the denominator, the raw numbers, what it was for, and what went wrong. |
| **Correction** | A claim on this site that is wrong. Requires where it appears, what is wrong, and what it should say. |

The correction form matters as much as the observation form and nobody asked
for it. This corpus has withdrawn published claims **twenty times**, every one
of them found internally. There has never been an inbound route for a reader to
file one, which means the self-correction record measures this programme's
appetite for finding its own errors and nothing about anybody else's ability to
find them.

**What GitHub gives the provenance for free**, and it is the reason this route
is preferred over any form service:

- an **identified author** — an account with a history, not an anonymous post
- a **server-side timestamp** the submitter cannot set
- an **immutable reference** — issue number and permalink, citable from a
  document the way every other source in this repository is
- a **public edit history** — if a submission is later changed, the change is
  visible, which is exactly the property a research record needs and exactly
  the property an email thread lacks
- **no third party**: nothing passes through a form vendor's database

### Route 2 — email

For anyone without a GitHub account, or who does not want their name attached
to a public repository. Send the same fields. They will be transcribed into an
issue.

**This route has weaker provenance and the difference is stated on the record, not smoothed over.** An email has no public timestamp, no public edit history,
and the transcription is performed by someone with an interest in the result. A
transcribed observation is therefore filed at **one rating step below** the same
observation submitted directly, and the issue says that it was transcribed and
by whom. A submitter who wants the higher rating can open the issue themselves.

Nothing is published under a submitter's name without explicit consent, and
consent to publish a *count* is not consent to publish a *name*.

### How a submission gets rated

Inbound observations go through the same rubric as everything else. Nothing is
rated higher for being ours, and nothing is rated lower for being a stranger's.

| Rating | What earns it |
| --- | --- |
| **5/5** | Not reachable by a street count. Reserved for agency measurement and for statements of an operator's own intent. |
| **4/5** | A count with a stated rule, a stated position and time, and a denominator. |
| **3/5** | A count involving a perceptual judgement (O5, O6, O8), or a count missing one provenance field. |
| **2/5** | A recollection, however confident. A count without a denominator. A transcribed email lacking a field. |
| **1/5** | An impression. Not published as a number. |

**Statements of intent are the exception and they are rated 5/5.** Nobody but
the person who took a measurement can say what it was for, and no analysis
performed afterwards can overrule them. That rule was written after an
operator's correction retired a published headline here, and it applies to
inbound submissions identically.

---

## Where this document is likely to be wrong

1. **Nobody has run any of these.** Every estimate of what an observation would
   cost in time, and every claim about what it would move, is a prediction. The
   first real session will find that some of these rules are not as mechanical
   as they read at a desk. O5's "audible" and O8's "covering their ears" are the
   two most likely to fail that way.

2. **The observations are not independent of the models they would correct.**
   The list was assembled by reading this repository's own weakness lists, so it
   is shaped to fill the holes this programme already knows about. An
   observation programme designed by someone who had never read these documents
   would probably count different things — and the things it counted instead
   would be the more interesting list.

3. **Volunteer counts have a selection problem this document does not solve.**
   People who volunteer to count noise-related things in DUMBO are not a random
   sample of people in DUMBO. They are more likely to be residents, more likely
   to be annoyed, and more likely to count at the times that annoy them. Every
   observation above inherits that, and only O1 and O3 have an obvious defence
   (fixed session bounds set in advance).

4. **The rule of three assumes independence, and rides are not independent.** A
   commuter counting dogs on 500 rides is counting the same route, the same
   hours and often the same carriage. The effective sample is smaller than 500
   and by an unknown factor. The bound in the table above is therefore
   optimistic, and the direction of the error is known even though its size is
   not.

5. **O9 is weak and is included anyway.** Its confounders are not controlled and
   probably cannot be by this method. It earns its place only because Q44 has no
   cheaper route, and a reader is entitled to skip it.

6. **A submission path is not a submission.** Building the form is the easy half.
   Nothing here establishes that anyone will use it, and the honest prior is
   that most such channels receive nothing. If it receives nothing, that is a
   finding about this programme's reach and should be published as one rather
   than quietly dropped.

7. **This document asks people to do unpaid work for a research programme that has no funding and no institutional standing.** It should not represent
   itself as more established than it is, and the standing condition applies:
   any approach to the community here must offer something before it asks for
   anything.

---

## Questions this raises

**Q65.** What is the rate at which dogs board subway trains on the B, D, N, Q,
F, A and C, and does it differ by line, hour or station? The corridor's dog
population is currently derived from a container rule and a national prevalence
figure, with no observation between them. *Method 45.*

**Q66.** Does the pram and wheelchair rate under the span differ from the rate
two blocks away at the same hour? A difference would be the first direct
evidence that the noise is excluding people rather than merely exposing them,
which is a claim the agent model is currently structurally unable to make.
*Method 46.*

**Q67.** Do two trains crossing together produce one event or two to a listener
standing beneath? Energy addition predicts `+3.01 dB`; the schedule cannot
answer it at all, because its departure times are quantised to `:00` and `:30`
and the merge window is empty by construction. *Method 47, and it rides along
with Method 41.*
