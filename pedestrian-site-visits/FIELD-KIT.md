# Field kit — the RØDE session card

**Companion to [`FIELD-CAPTURE-PROTOCOL.md`](../FIELD-CAPTURE-PROTOCOL.md) (Document 5).** That document was written for a bare Samsung Galaxy S23+ and is honest about what a phone cannot do. This card covers the gear that arrived afterwards, and it exists because **that gear changes the verdict in Part 3 of Document 5 more than the upgrade Document 5 itself recommended.**

Read the first two sections before leaving the house. The rest is usable standing up, on a phone.

---

## 0. The one instruction that matters most

**Speak a slate into every recording, at the moment you start it, and say what the capture is FOR.**

> "Six August, thirteen-oh-four. Unit A, north position, Brooklyn Bridge Park Main Street section. Gain fixed at *[value]*, GainAssist off, furry fitted. This is for the direction array — paired with unit B, sixty metres south."

Fifteen seconds. It is the single highest-value habit available, and it is here because of the most expensive mistake this repository has made.

Document 10 v1.0 published a finding that joined the stopwatch series to the audio clips. Every number in it was computed correctly. It was withdrawn because the two datasets were **captured an hour apart for different reasons and were never joined in the field** — and nothing in the analysis could see that, because purpose is not a property of a waveform. It is only recoverable from the person holding the microphone, at the time.

`CAPTURE_INTENT` in `build_media_data.py` rates operator statements of *purpose* at **5/5**, against **2/5** for operator recollections of *events*. Nobody but you can say what a capture was for, and no analysis done afterwards can overrule you. But that only holds if you say it **then**, not later.

**A measurement can only be read for the purpose it was taken for.** Slate the purpose, or the file is worth less than it cost to make.

---

## 1. What the new gear actually changes

### The Wireless Pro is not a better microphone. It is a different *instrument class*.

Rated **4/5 `SNIPPET`** — retailer and review listings agree on the specification; RØDE's own product page was not fetched directly.

| Property | Why it matters here |
|---|---|
| **32-bit float recording onboard each transmitter, 32 GB** | The recording is written **inside the transmitter**, not through the phone. The phone's speech DSP chain — the thing Document 5 Part 3 spends four pages warning about — is not in the signal path at all. |
| **32-bit float cannot clip** | *"prevent digital clipping, and ensure noise-free normalizing, even on very quiet recordings."* A 98.9 dB(A) peak beside a 65 dB(A) baseline stops being a gain-staging problem. |
| **Two transmitters, SMPTE/LTC timecode-synchronised** | Two microphones, in two places, on one clock. **This is the feature that makes three of the open questions measurable.** See §4. |
| **Omnidirectional capsules, 260 m range** | Omni is the right pattern for level and timing work. It is the wrong pattern for separating the structure from the street — that is the NTG's job. |

**The claim that this removes automatic gain control from the primary record is an inference from the architecture, not a tested fact. Rate it 3/5 until the bench test in §3 says otherwise.** Onboard recording *should* bypass the phone entirely; whether **GainAssist** also touches the internal file is not documented anywhere retrieved. Turn GainAssist off regardless, and let the bench test settle it.

### Why this is arguably better than the UMIK-1 that Document 5 §3.1 recommended

The UMIK-1 wins on one axis and one only: it ships with an **individual serial-numbered calibration file**, so it can produce absolute SPL and a corrected spectrum. That remains the only route to a defensible decibel.

The Wireless Pro wins on every other axis for the questions actually open here: fixed gain path, no clipping at any level, no phone in the chain, **two synchronised channels**, and forty hours of storage. Document 5 §3.1 should be updated to say so.

### The VideoMic NTG is the *characterisation* instrument

Rated **4/5 `SNIPPET`**, same basis. Supercardioid, USB-C (functions as a class-compliant interface), continuously variable gain, high-pass filter at **75 Hz or 150 Hz**, **−20 dB pad**, **safety channel**, **high-frequency boost**.

It is directional. That is the whole reason to carry it. See §5, DUMBO Archway.

---

## 2. Settings — decide these now, write them down, never change them mid-campaign

### Wireless Pro

| Setting | Value | Reason |
|---|---|---|
| **Record to** | **Transmitter internal memory, 32-bit float** | The primary record. Everything else is a backup. |
| **GainAssist** | **OFF** | Non-negotiable. GainAssist is an automatic level feature. The entire reason this gear is worth carrying to DUMBO is that the gain is *fixed*, and GainAssist silently undoes it. |
| **Gain** | Fixed, mid-scale, **written in the log** | With 32-bit float the value barely matters for headroom. It matters enormously for the future: see §7. |
| **Timecode** | **ON, both units synced before leaving** | If the units are not synced, the two-point array in §4 produces nothing. Sync at home, not at the site. |
| **Sample rate** | Highest available (48 kHz) | |
| **Windshields** | **Furry, both units, always** | Brooklyn Bridge Park is exposed waterfront. Document 5 §4.7: *"Without a windscreen, low-frequency data captured on an exposed waterfront is not train noise. It is wind."* Low frequency is exactly where a steel bridge radiates. |

### VideoMic NTG

| Setting | Value | Reason |
|---|---|---|
| **High-pass filter** | **FLAT (off)** | This is the setting most likely to be got wrong, because 75 Hz is the *correct* choice for almost every other use of this microphone. Here it is wrong. RØDE's own description says the filter exists to *"roll off low-frequency noise from common sources such as air conditioners and traffic."* On this project **the low frequency is the subject, not the noise.** A filter cannot be undone afterwards. |
| **If wind is corrupting the take** | 75 Hz, **and log it** | Never 150 Hz for this work. A take with the filter engaged is usable for timing and duty cycle and is **not** usable for spectrum. |
| **High-frequency boost** | **OFF** | It colours the spectrum, which is the thing being measured. |
| **Pad (−20 dB)** | **OFF** | Max SPL is far above a 99 dB(A) pass-by. The pad only reduces resolution. |
| **Safety channel** | **ON when recording into the phone** | Free insurance on the secondary record. Redundant on the 32-bit float path, harmless there. |

---

## 3. The bench test — fifteen minutes, before travelling

This is Document 5 §4.6 Test A, applied to the new chain. **It converts the 3/5 inference in §1 into a verified fact for your specific units, and it is the one test that can save an entire field session.**

1. Put a steady sound in the room at moderate level — a fan, or a fixed tone. Do not touch it.
2. Start a **32-bit float recording on the transmitter itself**, with GainAssist off.
3. Twenty seconds of just the steady source. Then something **loud** for ten seconds — vacuum cleaner, or clap hard and close. Then remove it. Twenty seconds more.
4. Transfer the file and look at the amplitude of the *steady* source before, during and after the loud event.

**If the steady source dips when the loud sound arrives and creeps back over a few seconds, automatic gain is active and the configuration has failed.** Find the setting, disable it, repeat.

**If it stays flat, the gain is fixed** — and that single result is what makes every duration, decay and ratio in §4 admissible.

Then, quickly: **Test B** — confirm the file really is 32-bit float at 48 kHz by reading the header, not the app's label. **Test C** — with both transmitters running and synced, clap once with them touching, and confirm the clap lands at the same timecode in both files. That verifies the array before it is depended upon in the field.

---

## 4. The three questions this gear can answer, and how

All three are **relative or temporal**. That is not a coincidence — it is the reason they are answerable at all. An unknown microphone sensitivity cancels out of a ratio and does not touch a timestamp. Absolute SPL is still out of reach (§7); none of these need it.

### Item 4 — which direction is the train going?

**Two transmitters, separated along the line of the track, at the same perpendicular distance from it.**

Sound from a moving source reaches the two units at different times, and the *order* is unambiguous. Unit A peaks first, then B: the train ran A→B. Unit B first: it ran B→A.

The same measurement produces the speed for free:

> `v = d / (t_B − t_A)`, where `d` is the separation along the track axis.

- **Separation: 50–80 m.** At plausible transit speeds that gives a 4–6 second peak-to-peak difference, which is very comfortable against the ±0.5 s precision of picking the peak of a broad envelope. Below about 25 m it gets tight.
- **Keep both units at a similar perpendicular offset from the track.** If they differ, the propagation delay no longer cancels — but forgivingly so: a 20 m mismatch contributes about 0.06 s against a signal of several seconds. This is a robust measurement.
- **Track axis bearing is 336.93°**, fitted to OSM subway ways over −467 m to +1290 m of chainage, straight to within 12.5 m. Separate the units *along* that bearing, not across it.
- **Write down which unit is where, and slate it into the unit itself.** Which transmitter sat upstream is not recoverable from the audio afterwards, and without it the whole array is just two recordings.

**Also keep a paper log of direction by eye.** You are standing there; a written *"13:04:22 Manhattan-bound"* is a 5/5 direct observation. That is not redundancy — it is what **validates the array method against ground truth**, and once validated the array can be trusted unattended in a future session when nobody is watching.

### Item 3 — how long does it stay loud? ("clock time versus floor time")

This is the question the earlier recording could not answer, and the reason is specific and worth stating: **automatic gain control actively destroys decay tails.** As the sound fades the compressor pushes gain up, so the recorded tail flattens and appears both longer and shallower than it is. Any duty cycle computed from it is a statement about the compressor. Fixed-gain 32-bit float removes exactly that failure.

Everything below is gain-independent, so all of it survives having no calibration:

- **Time above (peak − 10 dB)** and **above (peak − 20 dB)** — the standard effective-duration measures, both pure differences.
- **Time above (background + 3 dB)** — needs a background recorded **at the same gain, at the same spot, on the same visit**. See the checklist; this is the step most likely to be skipped and it is required by every difference in the analysis.
- **The decay fit from Document 5 Part 8**: `L(t) = Lmax − 10n·log₁₀(1 + (t/τ)²)`, reporting fitted `n` and `τ` with confidence intervals, on a **125 ms FAST** time constant. FAST is not an arbitrary choice — it is the MTA's own at Front and Pine Street, *"due to indications that the noise impact is caused by sudden impact with a track element."* Matching their constant keeps the results comparable to theirs.
- **The threshold sweep becomes a deliverable rather than a caution.** Document 10 v1.1 retained the sweep only as a warning that a single duty figure from uncalibrated audio is really a statement about a chosen threshold. The *only* reason it was a warning was that AGC made the envelope shape untrustworthy. With a linear record, the family of durations indexed by threshold is a legitimate result — and it is a far better answer to "clock time versus floor time" than any single number.

**Practical consequence: start recording well before an event and stop well after it.** A tail truncated by the end of a clip is unrecoverable. Continuous 40-minute takes are better than event-triggered ones, and 32 GB removes any reason not to.

**One honest scheduling note.** The tail measurement is **background-limited**: it ends where the train drops into whatever else is happening. The archway background is already 68.9 dB(A). A quiet-hour return visit — early morning, or late evening while trains still run — will measure a materially longer tail than midday will, and the difference between the two is itself informative.

### Item 2 — what happens when two trains cross together?

There is a specific prediction to test. **Two incoherent sources of equal level sum to +3.01 dB.** If two overlapping crossings produce a level materially above one crossing plus 3 dB, simple energy summation is not what is happening, and something structural is — which would be a genuinely new finding. Because it is a *difference between two events in the same recording*, unknown gain cancels completely.

To make it analysable:

- **Run the GTFS-realtime poller on the phone during the session** (`data-collection/bridge_realtime.py`, `--poll`). It needs no API key.
- **Log every crossing by eye with a wall-clock time and a direction.** Simultaneous crossings are the whole point and they are obvious from the ground.
- The two-unit array shows overlaps directly, as two interleaved peak pairs.

**The published schedule cannot answer this and never could.** Every scheduled departure in the MTA feed falls on an exact `:00` or `:30` second — 1,073 weekday traversals return only `{0: 528, 30: 545}` — so the entire 0–30 s window in which two trains merge acoustically is **empty by construction**. That is what forced the withdrawal of the merged-pair table in Phase 9. Only observation settles it, which makes this session the first instrument capable of answering it at all.

---

## 5. Where to stand

Levels are MTA doc 138061 as transcribed in `IDEA-CONCEPT.md` §1.2; derived durations from §1.7; offsets from this repository's own axis fit in `media-data.json`.

| Priority | Site | Published `Leq` | `Lmax` | Distance from axis | What it is for |
|---|---|---|---|---|---|
| **1** | **Brooklyn Bridge Park, Main Street section** (dog run) | **87.50** | 98.90 | 320.5 m | The **array site**. MTA's longest public session — 26 trains in 37:45 — highest published `Leq`, unambiguously public, and open enough to separate two units along the axis. Directly comparable to a 5/5 number. |
| **2** | **DUMBO Archway** | 81.33 | 91.80 | 12.6 m | The **NTG site**, and the most interesting one. Baseline is **68.9 dB(A)** — not a quiet environment, and the acoustic demo already flags that *"Some of what is attributed to background may be distant rail."* |
| 3 | **Front and Pine Street** | *none published* | 94.40 | 7.1 m | Closest measured point to the track. The site where MTA chose FAST *because of impact with a track element* — so the **best site for the decay tail** and for spectrum. It has no published `Leq` at all. |
| 4 | **Adams Street Library** | 84.65 | 98.10 | 18.3 m | MTA ran only **18:56 and 9 trains** here. A 40-minute session is independently valuable purely as a check on whether so short a session was representative. |
| 5 | **Grassy knoll, south of the bridge** | — | — | — | Your own prior site, where the last capture was compromised by a hand over the microphone. Worth re-doing cleanly. |

**Do two sites properly rather than five badly.** On a first outing with unfamiliar gear, sites 1 and 2 are the whole trip. Forty minutes of clean continuous audio at the dog run with a working array is worth more than five rushed ten-minute takes.

**Use the NTG's directionality at the archway.** Record the same spot twice: once pointed **up at the structure**, once pointed **along the street**. The *difference between two pointings at one position* is calibration-free, and it is the only cheap way to test whether that 68.9 dB(A) background is distant rail or road traffic. The omni transmitters cannot do this. It is the reason to carry the shotgun at all.

---

## 6. The checklist

**Before leaving**

- [ ] Bench test §3 passed — automatic gain confirmed off
- [ ] Both transmitters **timecode-synced**, and the clap test in §3 Test C confirms it
- [ ] Batteries full; both TX cleared or with 40 GB free
- [ ] **Furry windshields fitted to both transmitters**
- [ ] NTG: high-pass **flat**, HF boost **off**, pad **off**
- [ ] Gain values written down before departure
- [ ] Phone clock set to network time; note any offset
- [ ] `bridge_realtime.py --poll` running, or the app ready to start
- [ ] Notebook and pen. Not a notes app — a phone in your hand is a phone not recording.
- [ ] Tape measure, long cord, or a mapped pacing count for the array separation

**At every site, every time**

- [ ] **Slate the purpose into each unit** (§0) before anything else
- [ ] **Two minutes of background, same gain, before the first train** — required by every difference calculation
- [ ] Photograph the setup, and a photograph looking back at the bridge from the microphone position
- [ ] GPS reading, plus a description tied to a fixed landmark. GPS alone is not adequate under a structure.
- [ ] Microphone height above grade, and what it is standing on. Ground reflection changes the spectrum materially.
- [ ] Wind, temperature, weather; anything overhead
- [ ] Note every confounding source **with its time** — helicopters, boats, BQE, buskers, construction, the carousel
- [ ] Log every crossing: **wall-clock time, direction, and whether anything else was crossing with it**
- [ ] **Two minutes of background again at the end**, same gain — it brackets any drift

**Array-specific**

- [ ] Both units at a similar perpendicular distance from the track
- [ ] Separation measured, not estimated, and along bearing **336.93°**
- [ ] Which unit is at which end, slated into that unit and written down
- [ ] Neither unit left out of sight

**Before packing up**

- [ ] Recordings actually stopped and files present on both units
- [ ] Log photographed, so it exists twice

---

## 7. What this still cannot do — and the free thing that keeps the door open

**There is still no calibration, so there is still no decibel.** A microphone with unknown sensitivity produces a linear, unclipped, honest record of *relative* level. It does not produce SPL. Absolute values need an acoustic calibrator — a 94/114 dB reference at 1 kHz — and nothing in this kit is one.

**Do not close the gap by anchoring to the MTA's published levels.** Scaling this session so the dog run reads 87.50 dB(A) would make every subsequent comparison to MTA data circular, and this repository has already caught itself in exactly that closed loop once, in the acoustic demonstration. Publishing a number that was assumed and then rediscovered is worse than publishing no number, because it looks like corroboration.

**But one free habit makes a future calibration retroactive.** If the gain is **fixed and documented and identical across every session**, then a single calibration measurement taken at any point in the future converts **every recording ever made with that setting** into absolute SPL, backwards. If the gain is nudged between sites, that link is severed permanently and no amount of later work restores it.

**So: pick a gain, write it down, and do not touch it again.** It costs nothing today and it is the difference between a pile of relative recordings and a calibratable archive.

**On recording people.** Omnidirectional microphones running for forty minutes in a public park will capture conversation. The standing commitment holds: publish derived data — spectra, envelopes, event times, durations — and do not publish raw audio containing intelligible speech. This programme argues for the interests of the people it would incidentally record, so it carries that burden voluntarily.

---

## 8. Where this document is likely to be wrong

1. **Both specification tables are 4/5 `SNIPPET`.** They come from retailer listings and review sites that agree with each other, not from RØDE's own documentation or from the units in your hand. Where the hardware contradicts this card, **the hardware is right.** The button legends in particular were read partly from photographs.
2. **Whether GainAssist touches the internal 32-bit float file is unknown.** It is asserted here that onboard recording bypasses the phone; it is *not* asserted that it bypasses every automatic feature in the transmitter. The bench test in §3 is the only thing that settles this, and if it fails, most of §4 fails with it.
3. **The transmitter capsules are speech-optimised omnidirectional lavalier microphones.** Their frequency response is certainly not flat and is probably shaped in the presence region. This is harmless for timing, duration, decay and level *differences*. It means **no spectrum from these units may be published except as a difference spectrum** (train minus background), where the response cancels.
4. **No transit speed is assumed anywhere in §4, deliberately** — the array measures speed rather than needing it. But the recommended 50–80 m separation was chosen assuming speeds of order 10–15 m/s, and that assumption has no source behind it. If crossings turn out much faster, widen the separation.
5. **The +3.01 dB prediction for two trains assumes incoherent equal sources.** Two trains on different tracks, at different distances, in different directions are not equal sources. The prediction is a reference line to measure against, not an expected result.
6. **Site priority is argued from the MTA's session lengths and published levels, not from what is actually accessible today.** Construction, closures, events and weather all outrank this ordering.
7. **This card has not been used in the field.** Everything in it is reasoning from specifications and from Document 5. The first session that uses it should be treated as a test *of it*, and it should be corrected from what actually happened — in place, by quoting what was wrong, in the usual way.
