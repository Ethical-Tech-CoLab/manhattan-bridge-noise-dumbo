# Field Capture Protocol — What a Consumer Phone Can and Cannot Contribute

**Document 5 of the DUMBO rail-noise research programme.**
**Version 1.0 — 1 August 2026.**
**Status: proposed method, not executed. Nothing in this document has been carried out.**

Instrument specified: **Samsung Galaxy S23+**, plus a named optional upgrade under USD 150.

---

## Part 0 — How to read this document

### 0.1 What this document is for

Documents 1 through 4 of this programme make a large number of claims that are hedged, and the hedging almost always traces to the same root: **the MTA published levels and threw away everything else.** Its DUMBO survey (doc 138061) gives, per receptor, a session `Leq`, a peak `Lmax`, a train-free baseline, a session duration and a train count. Five numbers. From those five numbers this programme has extracted about as much as arithmetic allows, including one result the MTA did not publish (`IDEA-CONCEPT.md` §1.7, the derived event duration).

Everything else in the acoustic model is invented. The spectrum is invented. The envelope shape is a chosen convention. The impact-transient rate is a fabrication with no source at all. The service pattern in the continuous audio loop is a session mean rendered as a metronome.

**A phone in a park can fix most of that, and it can fix it this month.**

### 0.2 The claim this document is built on

> **The Galaxy S23+ is a poor sound level meter and an excellent sound recorder, and this programme does not need another sound level meter.**

That is the whole strategic argument, and it is worth stating carefully because it inverts the usual instinct.

The usual instinct is to install a decibel app, stand in the park, and try to confirm the MTA's numbers. **Do not do this as the primary activity.** It is the one measurement where a phone is weakest, it is the one measurement already made by a party with calibrated equipment and a statutory obligation, and the MTA's figures are rated **5/5 VERIFIED** in this programme. Reproducing them badly adds nothing; failing to reproduce them badly is worse, because it invites a fight this programme would lose on instrumentation grounds.

What the phone *can* deliver is the four things the MTA's five-number table discarded:

| What | Needs absolute calibration? | Currently in this programme |
|---|---|---|
| **Spectral shape** of a pass-by | **No** — shape is relative | **Wholly fabricated.** The largest single invention in the repository. |
| **Temporal envelope** of a pass-by | **No** — shape is relative | A chosen convention, `n = 1.5`, explicitly "chosen, not measured". |
| **Headway distribution** across a session | **No** — pure event timing | A session *mean* rendered as a regular rhythm. |
| **Attribution** — which service, which direction, how many cars | **No** — video and timestamps | Absent. The MTA normalises for none of it. |

Every row in that table is a **relative or temporal** measurement. Relative and temporal measurements survive an uncalibrated recording chain, because a fixed unknown gain cancels out of a ratio and does not touch a timestamp at all.

That is the opening this document exploits.

### 0.3 Source ratings used here

Same scale as the rest of the programme. Credibility **1** (a forum post) to **5** (a primary agency document or peer-reviewed measurement), and depth of reading marked **VERIFIED** (read in full), **SNIPPET** (read only the retrieved extract), or **UNVERIFIED** (located but not read).

**Most hardware and app claims in Parts 2 and 4 are `SNIPPET`.** They came from search extracts, not from hands-on testing of an S23+, which this programme does not possess. Part 4.6 therefore specifies a bench test to establish the ones that matter, on the actual handset, before any field trip. **Do not skip it.** If the bench test contradicts this document, the bench test is right.

---

## Part 1 — The five captures, in priority order

Ranked by *value to this programme per hour of effort*, not by how interesting they are.

| # | Capture | Kit | Time | What it closes |
|---|---|---|---|---|
| **C1** | **Spectrum of a pass-by** | Phone, windscreen | 30 min | The largest fabrication in the repository. |
| **C2** | **Temporal envelope of a pass-by** | Phone, windscreen | Same session as C1 | Breaks the closed loop in §1.7. **The highest-value item epistemically.** |
| **C3** | **Headway distribution over 90 minutes** | Phone, windscreen, power bank | 90 min, unattended | Weakness #4 of the audio demo. Needs **no calibration whatsoever**. |
| **C4** | **Attribution — service, direction, consist** | Phone video + timestamps + GTFS-RT | Same session as C3 | Weakness #3. A dataset that does not appear to exist anywhere. |
| **C5** | **Photogrammetry of the underside** | Phone, scale bar | An afternoon | Method 16. The 3D model contains **zero measured elements**. |

### C1 — The spectral shape of a pass-by

**The problem it solves.** `visual-review/acoustic-demo.html` states plainly, in its own interface: *"No third-octave spectrum has ever been published for either bridge"*, and so the sound is synthesised noise with a level envelope pinned to published measurements. The page also warns that *"Two sounds can share an A-weighted level and be entirely different experiences"*, and that nothing on it should be used to argue about annoyance, speech interference, or which frequencies a treatment should target.

That single missing dataset blocks most of the design conversation the programme exists to start. **You cannot specify a barrier, an absorber, a damping treatment or a resilient fastener without knowing which octaves carry the energy.** Every mitigation option in `PRECEDENT-AND-MATERIALS.md` is frequency-selective. Selecting among them without a spectrum is guessing.

**Why a phone is sufficient.** A spectrum for *design* purposes is a shape: where are the peaks, is the energy in the 50–125 Hz structural-radiation region or the 500–2000 Hz wheel/rail region, is there a discrete tonal component, is there a broadband impact signature. The absolute offset of that shape is irrelevant to all of those questions, and the absolute offset is the only thing an uncalibrated chain gets wrong.

**One caveat that is not optional.** The phone's microphone has its own frequency response, and it is not flat. This means the *measured* shape is the true shape convolved with an unknown response. For the mid-range this is a modest distortion. **Below about 100 Hz and above about 10 kHz it may be severe**, and MEMS mics in phones are routinely high-passed in hardware to suppress handling and wind noise. Since low-frequency structural radiation is exactly what a bridge problem is about, **this is the most dangerous limitation in this entire document.** Part 4.7 is the mitigation.

**Procedure.**

1. Position per Part 6. Phone on a small tripod, mic port unobstructed, **windscreen fitted** (Part 4.7 — non-negotiable outdoors).
2. Record continuously through **at least 10 complete pass-bys**, including at least 30 s of clean background before the first and after the last.
3. Do not touch the phone during recording. Handling noise is broadband and will contaminate the transient analysis.
4. Note the wall-clock start time to the second (Part 5).
5. Uncompressed WAV only. **Never a lossy codec** — see Part 4.3.

### C2 — The temporal envelope, and why it matters more than it looks

**This is the item that most changes the standing of the programme's own work,** and it deserves explaining properly.

`IDEA-CONCEPT.md` §1.7 derives the equivalent event duration from the published energy balance:

`Te = ( T · 10^(Leq/10) − T · 10^(Lbase/10) ) / ( N · ( 10^(Lmax/10) − 10^(Lbase/10) ) )`

Across the three public outdoor sessions this yields **5.70 s, 6.28 s and 7.25 s** — a spread of only 1.04 dB in event energy, across different places, days, train counts and session lengths. That mutual consistency is real and it is the strongest derived result in the repository.

But it rests on an **assumed envelope shape**, `L(t) = Lmax − 15·log10(1 + (t/τ)²)`, with `τ = Te/2`. The demo page is candid that this shape is *"a convention, not a measurement"* and *"Chosen, not measured"*.

Worse — and this is the substance of open issues #13 and #15 — **the whole construction is a closed loop.** The continuous audio loop's running energy average converges on the published `Leq` because `τ` was solved *from* that `Leq`. The page says so in as many words: it is *"a consistency check on the arithmetic, not independent evidence"*. A closed loop cannot be wrong and cannot be informative. It is unfalsifiable as it stands.

**A single recorded envelope opens the loop.** Measure the actual `L(t)` of a real pass-by, fit the decay, and one of two things happens, both of which are publishable:

- **The measured envelope matches the assumed shape.** The derivation ceases to be self-referential. `Te` becomes a corroborated quantity rather than a definition, and §1.7 upgrades from arithmetic to a result.
- **It does not match.** Then §1.7's numbers are wrong by a stated factor, the audio demo's duty cycles are wrong, and the programme retracts them under its own correction discipline. **This outcome is more valuable than the first**, because it is the only route by which this programme can currently discover it is wrong about something it invented.

Either way, an hour in a park settles a question that no amount of further reasoning can settle. That is the definition of a good measurement.

**Procedure.** C1 and C2 are the same recording. The distinction is analytical, not operational: C1 asks what frequencies, C2 asks what shape over time. Record once, analyse twice.

The one recording requirement C2 adds is **fixed gain**. See Part 4.4. If automatic gain control is active, the envelope you measure is the AGC's envelope and not the train's, and the recording is worthless for this purpose. It will still look and sound perfectly fine, which is what makes this failure mode dangerous.

### C3 — The headway distribution

**The problem it solves.** The continuous mode of the audio demo runs the measured headway — 87.1 s at the Brooklyn Bridge Park dog run, derived as 26 trains in 37 min 45 s. Its own weakness #4 states the objection:

> The loop is a *mean* rendered as a *rhythm*, and the regularity you hear is an artifact of that.

Real service scatters, bunches behind delays, differs by direction and by service, and thins overnight. A regular loop may materially misrepresent the experience in either direction: real bunching could produce sustained periods far worse than the mean suggests, and real gaps could produce genuine respite the loop denies.

**Why this is the cheapest item in the programme.** It requires **no calibration, no windscreen strictly, and no attendance.** It is a list of timestamps. A 90-minute recording, an amplitude threshold, and a peak-picking script produce the actual interval distribution — mean, spread, and the shape of the tail. The phone could be under a jacket in a bag and the data would still be good.

It also directly tests the MTA's own figures. If your observed count over 90 minutes disagrees materially with the rate implied by *"26 trains in 37 minutes 45 seconds"*, that is a finding about the survey.

**Procedure.** Record 90+ minutes continuously to uncompressed WAV. Note the start time to the second. Bring a power bank; continuous recording at 48 kHz will run the battery down and the file will be roughly 300 MB per hour in 16-bit mono, 500 MB in 24-bit. Ensure adequate free storage before starting.

### C4 — Attribution, via GTFS-realtime

**This is the item most likely to be genuinely novel, and it costs almost nothing on top of C3.**

The MTA report normalises for nothing. Weakness #3 of the demo page:

> B, D, N and Q services differ in car class, consist length and axle count, and the MTA report normalises for none of these. The derived figure is an average over an unknown mixture.

The MTA publishes **GTFS-realtime feeds covering the B, D, N and Q**, and as of `nyct-gtfs` v2.0.0 **API keys are no longer required** to access them (rated 3/5, `SNIPPET` — verify at the MTA developer portal before relying on it).

So: if your recording carries an accurate wall-clock timestamp, and you capture the GTFS-RT feed during the same window, **every acoustic event in your recording can be matched to a specific, identified train.** Service, direction, and scheduled versus actual timing.

That converts an anonymous acoustic event into an attributed one, and it makes several currently unanswerable questions answerable:

- Do B/D pass-bys differ measurably from N/Q pass-bys? If car class matters, this shows it, and it would be the first evidence that the MTA's unnormalised average conceals a real effect.
- Do northbound and southbound differ? The four tracks are not equidistant from any given receptor, so they should.
- Is the loudest event class a particular service, or a particular direction, or neither?

**Video adds the third leg.** A short 4K clip of a pass-by lets you count cars directly and read the car class from the exterior, which cross-checks the GTFS attribution rather than trusting it. Car classes assigned to these services should be **confirmed from the footage, not assumed** — this programme should not assert a rolling-stock assignment it has not verified, and fleet assignments change with deliveries.

**Procedure.** Run C3's audio recording. In parallel, poll the GTFS-RT feed to a log file — a laptop, a Raspberry Pi, or a scheduled script on any always-on machine will do; it does not need to be at the site. Separately, shoot 6–10 individual pass-bys on video for the visual cross-check. **Do not rely on the video's own audio track for any acoustic analysis** (Part 4.5).

### C5 — Photogrammetry of the underside

**The problem it solves.** `visual-review/model-3d.html` contains **zero MEASURED elements and zero DOCUMENTED-position elements**. Hide the inferred and assumed geometry and the frame is empty — the model says so in its own HUD: *"the frame is empty. That is the finding."* Method 16 (Williamsburg walkway photogrammetric survey, *"A camera and an afternoon"*, Priority 2) and Method 19 (the L1 model) both remain open.

**The hardware position.** The S23+ has no LiDAR or time-of-flight sensor; Samsung does not fit them to this line. So this is **structure-from-motion photogrammetry**, not depth sensing. RealityScan (Epic Games) runs on Android and processes in the cloud (rated 3/5, `SNIPPET`). Alternatives worth trialling include Polycam and the desktop route of shooting frames and processing in **Meshroom** or **COLMAP**, both free and open source — and the desktop route is preferable here, because a research programme should be able to state exactly what its reconstruction pipeline did.

**The one thing that decides whether this is worth doing at all.**

> **Photogrammetry produces a model with arbitrary scale.** Without a known-length object in the scene, you get a shape, not a dimension.

A shape adds nothing this programme lacks. **Dimensions are the entire point.** So:

1. **Best:** print a ChArUco or ArUco marker board on A4/Letter, mount it rigid and flat, and place it in the scene. Most pipelines detect these automatically and scale from them.
2. **Good:** place a folding rule or a steel tape, extended and rigid, in frame — ideally two, at right angles, at different depths.
3. **Fallback:** a US Letter sheet (8.5 × 11 in) or a US dollar bill (6.14 × 2.61 in), flat and fully visible.
4. **Always:** independently measure something in the scene with a tape and record it, as a check on the scaled model rather than as its source.

**Every reconstructed dimension must carry the scale source in its provenance**, per `VISUAL-MODEL-FRAMEWORK.md` §5.4. A dimension scaled from a dollar bill is not the same evidence as one scaled from a marker board, and the model's rendering rules already distinguish provenance classes visually.

**Capture procedure.** Photogrammetry rewards discipline and punishes improvisation:

- **Shoot stills, not video frames**, where possible. 50 MP full-resolution on the main camera. Video frames carry compression artefacts and rolling-shutter skew.
- **60–80% overlap** between consecutive frames. Move in a slow arc, one step at a time.
- **Three passes at three heights** where access allows, plus obliques.
- **Lock focus and exposure** between frames. Auto-exposure drift between frames degrades feature matching.
- **Use the main 50 MP camera only.** Do not mix focal lengths mid-capture; the ultrawide's distortion profile differs and mixing complicates calibration.
- **Avoid the ultrawide for anything you intend to measure.** Its barrel distortion is the largest at the frame edges, exactly where structural members will sit.
- **Overcast is ideal.** Hard shadows under a bridge deck create the highest-contrast edges in the scene, and the reconstruction will happily model the shadow rather than the steel.
- **Expert RAW** for the underside. The dynamic range between sunlit river and shadowed steel is brutal, and the default JPEG pipeline will crush the shadow detail that carries the geometry.

---

## Part 2 — The instrument, as specified

Consolidated so that any future reader knows exactly what produced the data.

| Property | Value | Rating | Note |
|---|---|---|---|
| Microphones | **Three** | 4/5 `SNIPPET` | Samsung support documentation for the S23/S23+/S23 Ultra. Warns that cases can occlude them. |
| Native capture | **48 kHz, 16-bit** typical | 3/5 `SNIPPET` | Nyquist 24 kHz, comfortably beyond the band of interest. 24-bit may be available via third-party apps; establish on-device. |
| Mic element headroom | **AOP 120–132 dB SPL** for typical MEMS parts | 4/5 `SNIPPET` | PUI Audio and Infineon give this as the general MEMS range. |
| Main camera | **50 MP** | 4/5 `SNIPPET` | 1/1.56" sensor. |
| Ultrawide | **12 MP** | 4/5 `SNIPPET` | Highest distortion; avoid for metrology. |
| Telephoto | **10 MP, 3× optical** | 4/5 `SNIPPET` | Useful for detail on inaccessible members. |
| Video | **up to 8K**; 4K60 practical | 4/5 `SNIPPET` | |
| RAW stills | **Expert RAW** app | 4/5 `SNIPPET` | Separate Samsung app; install before travelling. |
| Depth sensor | **None** | 4/5 | No LiDAR/ToF. Photogrammetry only. |
| Headphone jack | **None** | 5/5 | External mics must be USB-C or wireless. |

### 2.1 The clipping question, resolved

A reasonable worry is that a 98.9 dB(A) peak will overload a phone microphone. **It will not overload the element.** With a MEMS acoustic overload point of 120–132 dB SPL, the loudest event in the MTA dataset sits **21 to 33 dB below** the onset of 10% THD.

**The real risk is entirely downstream:** the analogue gain stage and the software gain policy. A phone tuned for speech at 60–70 dB may apply enough gain that a 99 dB event clips digitally at 0 dBFS long before the microphone itself is troubled. That is a *settings* problem, not a hardware limit, and Part 4.4 is how you solve it.

**Consequence for the field:** always check the recorded waveform for flat-topping before leaving the site. A clipped peak is unrecoverable, and it destroys both the spectrum (clipping generates harmonics that are not in the source) and the envelope (the peak is truncated). Record a test pass-by, inspect it, then commit to the long session.

---

## Part 3 — What the phone must not be used for

Stated as a prohibition because the temptation is strong and the failure is quiet.

**A 2025 study in *Cureus* evaluated the ten top-rated free Android sound-meter apps on a Samsung Galaxy A54** against a calibrated reference (rated **4/5, `VERIFIED` abstract and methods**; peer-reviewed, small, and on a mid-range Samsung rather than an S23+). Its two findings that matter here:

> Accuracy declined at higher noise levels, with Sound Meter (ABC Apps) showing the least accuracy (R² = 0.85).

> However, limitations such as reduced accuracy at higher decibels and lack of A-weighting for regulatory compliance hinder their use in professional settings.

**Accuracy is worst precisely in the regime this programme cares about.** The DUMBO public-space events run 81–99 dB(A). That is the high end, where the study reports degradation.

By contrast, the **NIOSH Sound Level Meter app** is accurate to **± 2 dBA** and meets **IEC 61672-3 Type 2** — *with a calibrated external microphone* — and was validated in a reverberant chamber at the NIOSH acoustics laboratory (rated 5/5, `SNIPPET`; CDC/NIOSH primary). **It is iOS only.** There is no Android equivalent with comparable institutional validation. This is a genuine platform asymmetry and there is no way around it on an S23+.

Therefore:

- **Do not** present any phone-derived absolute dB value as a measurement in a regulatory, comparative or adversarial context.
- **Do not** attempt to confirm, challenge or "check" the MTA's published levels with the phone. Those are rated 5/5 `VERIFIED` and were taken with proper instrumentation under a statutory obligation. Losing a fight about instrumentation would discredit the parts of this programme that are sound.
- **Do** record absolute readings anyway, as **context metadata**, clearly labelled `INDICATIVE, UNCALIBRATED`. They are useful for spotting an anomalous session and useless for anything else.
- **Do** anchor everything of substance to spectrum, envelope, timing and attribution.

### 3.1 The upgrade that changes this verdict

If USD 100–150 is available, the position changes materially.

A **miniDSP UMIK-1** is a USB measurement microphone supplied with an **individual, serial-numbered calibration file** giving its actual frequency response. Connected to the S23+ over USB-C — with **USB Audio Recorder PRO**, which is the Android app most consistently reported to handle class-compliant USB audio interfaces — it provides:

- A **known frequency response**, which can be divided out. This removes the single most dangerous limitation in Part 1 (C1), the unknown microphone response at low frequency.
- A **known sensitivity**, which makes absolute SPL defensible rather than indicative.
- A **fixed, documented gain path** that does not include a speech-optimised DSP chain.

**This is the highest-value equipment purchase available to the programme**, by a wide margin, and it is cheaper than a single hour of an acoustic consultant's time. It would move the spectrum from `ASSUMED` to `MEASURED` with a provenance chain that survives scrutiny.

Rated 3/5 `SNIPPET` on the specific Android compatibility claim. **Verify UMIK-1 + USB Audio Recorder PRO on the actual S23+ before depending on it in the field** — USB audio class support on Android is device-specific and has historically been inconsistent.

---

## Part 4 — Software, and how to configure it

### 4.1 What to install

| App | Role | Why this one |
|---|---|---|
| **RecForge II** | **Primary recorder** | Its own FAQ documents an explicit **"Disable AGC"** option, and it records uncompressed WAV with selectable sample rate and bit depth. The explicit AGC control is the deciding feature. |
| **Audio Spectrum Analyzer** (F-Droid, `org.woheller69.audio_analyzer_for_android`) | **Field spectrum check** | **Open source.** For a research programme this is the point: the processing chain is inspectable, so the document can state what was done to the signal rather than guess. |
| **Spectroid** | Alternative live FFT | Free, responsive, widely used. Closed source, so prefer the F-Droid analyzer for anything of record. |
| **Expert RAW** (Samsung) | RAW stills | Needed for the high-dynamic-range underside shots. |
| **RealityScan** (Epic) | Photogrammetry, in-field | Cloud processing. Convenient; the desktop route is more defensible. |
| **Meshroom** or **COLMAP** (desktop) | Photogrammetry, of record | Free, open source, reproducible, and the pipeline can be described exactly. |
| **Audacity** or **Python + `numpy`/`scipy`** (desktop) | Analysis | Audacity for inspection; a script for anything reported. |

**Do not use Samsung Voice Recorder for anything analytical.** It is tuned for speech and applies processing that is neither documented nor disableable. It is fine for spoken field notes, and should be used for those.

### 4.2 Sample rate and bit depth

**48 kHz, 24-bit if available, 16-bit otherwise.** 48 kHz gives a 24 kHz Nyquist limit, far above anything relevant. There is no benefit to 96 kHz here and it doubles the file size on a long unattended session.

Bit depth matters more than sample rate for this application. The full excursion at the dog run is roughly **34 dB** (65.0 dB(A) background to 98.9 dB(A) peak). 16-bit offers about 96 dB of dynamic range, so 34 dB fits with enormous margin **provided the gain is fixed and sensible**. 24-bit simply buys tolerance for setting the gain conservatively — which you should, because you cannot re-record a clipped peak.

### 4.3 Format: uncompressed, without exception

**Record WAV. Never MP3, AAC, Opus or any lossy format, for any recording intended for analysis.**

This is not audiophile fussiness. Lossy codecs are **psychoacoustic**: they work by discarding content a listener is predicted not to notice, principally through masking. A train pass-by is a loud broadband event, which means it is an *excellent* masker, which means a lossy encoder will discard a great deal during exactly the moments of interest. The reconstruction sounds fine and its spectrum is systematically falsified. **The distortion is largest at the peak** — the part being measured.

### 4.4 Automatic gain control: the setting that decides everything

**If AGC is active, the recording is worthless for C1 and C2, and it will not be obvious.**

AGC continuously adjusts gain to keep levels in a comfortable range. Applied to a 34 dB excursion it does precisely the wrong thing: it pulls the peak down and pushes the background up, **compressing the very ratio being measured**. The envelope you then recover is the AGC's release curve, not the train's decay. The recording will sound entirely normal.

Android exposes an audio source for this. From the Android CDD and developer documentation (rated **5/5, `SNIPPET`**; primary platform documentation):

> Most of the audio sources (including DEFAULT) apply processing to the audio signal. To record raw audio select UNPROCESSED. Some devices do not support unprocessed input.

Support is device-specific and queryable via `AudioManager.getProperty("PROPERTY_SUPPORT_AUDIO_SOURCE_UNPROCESSED")`. Where unavailable, `VOICE_RECOGNITION` is the commonly recommended fallback, as it typically bypasses more of the voice-call processing chain than `MIC` or `DEFAULT`.

**In RecForge II**, its FAQ specifies the combination:

> Set the recording source to "Front Microphone" and enable the "Disable AGC" option.

**Whether that maps cleanly onto the S23+'s three microphones is not established here** and must be settled by the bench test in 4.6.

Additionally, in Samsung system settings, disable every call and voice enhancement available — "Clear Call" and any noise-reduction or adaptive-audio feature. Put the phone in **airplane mode** during recording where GTFS logging does not depend on it: this removes both radio interference and interruption risk.

### 4.5 Video audio is not measurement audio

**Never analyse the audio track of a video clip.** Camera apps apply wind-noise reduction, AGC and directional processing tuned for consumer video, none of it documented or disableable.

**Record audio separately and in parallel**, and synchronise afterwards with a clap or other sharp transient at the start of each clip. This is the standard dual-system approach and it costs nothing. Note that on many handsets a second app cannot hold the microphone while the camera is recording — **this may require two devices**, and if so, the audio device is the one that matters and the video can come from anything, including an older phone.

### 4.6 The bench test — do this before travelling

**Ten minutes at home. It converts every `SNIPPET` claim in Part 4 into a `VERIFIED` one for your specific handset.**

**Test A — is AGC actually off?**

1. Put a steady, unchanging sound source in the room at moderate level — a fan, or a tone from a speaker at fixed volume. Do not touch it for the duration.
2. Start recording with your intended settings.
3. Let 20 s pass. Then introduce a **loud** sound for about 10 s — a vacuum cleaner, or a second speaker. Then remove it. Let 20 s more pass.
4. Open the file in Audacity and look at the amplitude of the *steady* source before, during and after.

**If the steady source's level dips when the loud sound appears and then creeps back up over a few seconds, AGC is active and the configuration has failed.** Change source or app and repeat. **If it stays flat throughout, the gain is fixed** and you are ready.

This test is decisive, needs no special equipment, and catches the one failure that would otherwise waste an entire field session.

**Test B — headroom.** Record something considerably louder than you expect in the field and confirm the waveform is not flat-topped. Adjust input gain down until it is not.

**Test C — which microphone.** Record while covering each microphone port in turn and note which selection in the app corresponds to which physical port. Cases and screen protectors can occlude them.

**Test D — does the format survive?** Confirm the output file really is uncompressed PCM WAV at the stated rate and depth, by inspecting the header rather than trusting the app's label.

### 4.7 Wind: the cheapest large improvement available

**Fit a windscreen. This is the single highest-value item in this document per dollar spent.**

Wind noise across a bare microphone port is broadband but strongly **low-frequency**-weighted — and low frequency is exactly where bridge structural radiation lives and exactly where the interesting acoustics of this problem sit. **Without a windscreen, low-frequency data captured on an exposed waterfront is not train noise. It is wind.** It will look like a plausible rumble and it will be an artefact.

Brooklyn Bridge Park is an exposed waterfront site. This is not a marginal concern there.

A foam windscreen sized to the handset, or a fur "deadcat" over the mic port, costs a few dollars. Record and log wind conditions for every session regardless, and treat any session with sustained wind above a light breeze as **suspect for low-frequency content** no matter what protection was fitted.

---

## Part 5 — Metadata, without which the recordings are much less useful

Log for every session. A recording without this is a curiosity; with it, it is data.

| Field | Why |
|---|---|
| **Wall-clock start, to the second, and the clock source** | The hinge for the entire GTFS-RT attribution in C4. Set to network time and note any offset. |
| **Position** | GPS from the phone, **plus** a description tied to a fixed landmark, plus a photograph looking back at the bridge from the mic position. GPS alone is not adequate under a structure. |
| **Height and mounting** | Mic height above grade, and what it sat on. Ground reflection changes the spectrum materially. |
| **Orientation** | Which way the mic port faced. Smartphone directional response is documented as non-trivial in the NIOSH literature. |
| **Weather** | Wind speed and direction, temperature, humidity, precipitation. Affects both propagation and wind-noise contamination. |
| **Full device and app configuration** | Handset, OS build, app and version, audio source, sample rate, bit depth, AGC state, windscreen type. |
| **Confounding sources** | Helicopters, boats, BQE traffic, buskers, construction, events. **Note the time of each.** The DUMBO Archway baseline of 68.9 dB(A) is already not a quiet environment. |
| **Bench-test result** | Which configuration passed Test A, and when it was last confirmed. |

**On the ethics of recording in public space.** These sites are busy with residents and tourists, and continuous audio recording in a public park will capture conversation. This programme's interest is entirely in the trains. Recommended practice: state the retention and processing policy in the session log before recording; **do not publish raw audio containing intelligible speech**; publish derived data — spectra, envelopes, event timestamps — and short excerpts audited for speech. Where a longer excerpt must be published, high-pass or notch the vocal band, or select a passage with no one nearby. This is a burden the programme should accept voluntarily, because it is arguing for the interests of the people who would be incidentally recorded.

---

## Part 6 — Where to stand

Match the MTA's own receptors so the data is directly comparable. Levels below are from MTA doc 138061 as transcribed in `IDEA-CONCEPT.md` §1.2, with derived durations from §1.7.

| Receptor | Published `Leq` | Max `Lmax` | Baseline | Session | Trains | Derived `Te` | Headway |
|---|---|---|---|---|---|---|---|
| **Brooklyn Bridge Park dog run** | **87.50** | 98.90 | 65.0 | 0:37:45 | 26 | 6.278 s | 87.1 s |
| **Adams Street Library** | **84.65** | 98.10 | 48.1 | 0:18:56 | 9 | 5.702 s | 126.2 s |
| **DUMBO Archway** | **81.33** | 91.80 | 68.9 | 0:25:35 | 18 | 7.253 s | 85.3 s |

**Start at the dog run.** It has the longest public-space session, the most trains, the highest published `Leq`, and it is the receptor the audio demo defaults to. It is also unambiguously public open space.

**The Adams Street Library session is only 18 minutes 56 seconds and 9 trains.** That is a thin basis for a published figure, and a longer recording there would be independently useful as a check on whether such a short session is representative.

**The DUMBO Archway is the hardest site to interpret** and the most interesting. Its baseline is 68.9 dB(A) — the demo page flags this directly, noting that this *"is not a quiet environment"* and that *"Some of what is attributed to background may be distant rail."* A recording there could settle that, because the *spectrum* of the background will show whether it is rail or traffic even though the *level* cannot.

### 6.1 The Williamsburg comparator

`WILLIAMSBURG-COMPARATOR.md` makes the case that the Williamsburg Bridge is the correct control: same operator, same system, same rolling stock classes, similar suspension structure, different noise-housing configuration.

**Capturing the same protocol at both bridges on the same day, with the same handset and the same settings, is worth more than either site alone.** Every unknown in the chain — microphone response, gain, app processing — is *identical* across the two, so it cancels in the comparison. A phone that cannot tell you the absolute level at either site can tell you the **difference** between them with real confidence.

This is Method 11 (*"Two-site `SEL` survey, both bridges"*, described in the register as *"The cheapest decision-relevant measurement anywhere here"*) executed with a phone instead of two sound level meters. It is a weaker instrument for that method, and it is available immediately.

---

## Part 7 — Legal, safety and access

**Not legal advice.** Confirm current rules before travelling; these are pointers, not clearances.

- **Brooklyn Bridge Park, the DUMBO Archway and public sidewalks are public space**, and photography from public space is generally lawful in New York City. All five captures are designed to be performed from public ground.
- **Do not enter the bridge structure, track areas, or any MTA or NYCDOT non-public area.** Nothing in this document requires it, and Method 18 exists precisely because access of that kind requires a relationship the programme does not have.
- **Drones are prohibited in New York City parks** and takeoff/landing within the city is heavily restricted. **No capture here uses one.**
- **Tripods and extended setups** in park property may require notification or a permit, particularly if the activity appears commercial. Brooklyn Bridge Park is managed by a dedicated corporation with its own rules; check before an unattended 90-minute deployment.
- **Do not leave equipment unattended in a way that could be mistaken for an abandoned package.** For the C3 long session, stay with the device. This is both a courtesy and a practical precaution near a major crossing.
- **Hearing.** Sustained exposure at these levels is not trivial. The published Max `Lmax` at the dog run is **98.90 dB(A)**. If a session runs to several hours, consider protection — noting the irony that a researcher documenting a noise problem may need it, which is itself an observation worth recording.

---

## Part 8 — From files to findings

A capture that is never analysed is not a contribution. Minimum analytical path per capture:

**C1 — spectrum.** Extract a window centred on each peak and a matched window of background. Compute one-third-octave band levels for both. Report the **difference spectrum** — train minus background, band by band. The difference is the robust quantity: the microphone response and the unknown gain both appear in each term and largely cancel. Report the mean and spread across at least 10 events. **Label the absolute ordinate as uncalibrated and relative.**

**C2 — envelope.** Compute a short-time A-weighted level with a **125 ms** time constant, matching the FAST weighting the MTA used at Front and Pine Street *"due to indications that the noise impact is caused by sudden impact with a track element"*. Normalise each event to its own peak and align on the peak. Overlay all events. Then fit `L(t) = Lmax − 10n·log10(1 + (t/τ)²)` and report **fitted `n` and `τ` with confidence intervals**. Compare `n` against the assumed 1.5 and `τ` against the derived values in the table in Part 6. **Report the comparison whichever way it comes out.**

**C3 — headway.** Threshold the broadband envelope, pick peaks, enforce a minimum separation, and produce the list of inter-arrival intervals. Report mean, standard deviation, minimum, maximum, and a histogram. Compare the mean against the MTA-derived headway for that receptor. **The spread is the finding**, because the audio demo currently assumes it is zero.

**C4 — attribution.** Join event timestamps to the GTFS-RT log within a tolerance window. Group events by service and by direction. Test whether peak level, `SEL` and envelope width differ by group. **State the group sizes**; with a 90-minute session these will be small and the analysis should be treated as exploratory rather than confirmatory.

**C5 — geometry.** Reconstruct, scale from the marker board, and export. Compare at least one reconstructed dimension against the independently tape-measured check. **Report the discrepancy.** Then, and only then, consider whether any element can be promoted from `INFERRED` to `MEASURED` in `model-3d.html` — and if so, update the provenance filter counts, because the model's HUD currently reports zero measured elements and that number is load-bearing.

### 8.1 What must be filed with any result

Per this programme's discipline: every quantitative claim carries a quoted locus; every source carries a credibility rating and a depth-of-reading marker; **and any figure that supersedes an existing published figure must quote the old one in place and mark it withdrawn rather than deleting it.** If C2 contradicts §1.7, §1.7 is not edited silently.

---

## Part 9 — Where this document is likely to be wrong

1. **Most of the hardware and app detail is `SNIPPET`, not `VERIFIED`.** It came from search results, and no S23+ was tested in writing this. The bench test in 4.6 exists because of that, and where the handset contradicts this document, **the handset is right**.

2. **The microphone's frequency response is unknown and is not flat.** This is the deepest problem with C1. Phone MEMS microphones are commonly high-passed in hardware, and the low-frequency region that a structural-radiation problem most concerns is the region most likely to be misrepresented. **The difference-spectrum method reduces this but does not eliminate it**, because the response affects both terms identically only if it is time-invariant — which it is, but the *masking* of a genuinely absent low-frequency component by a hardware filter is not something differencing can recover. **The UMIK-1 upgrade in 3.1 is the real answer and this document should not pretend otherwise.**

3. **`PROPERTY_SUPPORT_AUDIO_SOURCE_UNPROCESSED` may return false on this handset.** In that case there is no documented route to genuinely unprocessed capture and the fallback is `VOICE_RECOGNITION`, which is a convention rather than a guarantee. Test A would still pass or fail honestly, but a pass would only establish that gain is *stable*, not that the signal is *unprocessed* — spectral shaping could remain.

4. **The 2025 *Cureus* study was conducted on a Galaxy A54, not an S23+**, with pure tones in a controlled room rather than broadband transients outdoors, and tested apps rather than raw capture. Generalising its "accuracy declines at higher levels" finding to this use is **an inference, not a result.** It is used here to justify caution, which is the safe direction to be wrong in.

5. **GTFS-RT attribution assumes the feed's timing is accurate enough to match acoustic events.** Subway real-time predictions are known to drift, and the relevant question is not when a train was predicted at a station but when it physically crossed a point on the bridge, which the feed does not directly report. **The matching tolerance may turn out to be wider than the headway**, in which case C4 fails entirely and only the video attribution survives. This is the least certain item in this document.

6. **The list of receptors assumes the MTA's stated locations can be reoccupied accurately.** They are given as street addresses and place names, not coordinates. Standing "at the DUMBO Archway" is not a position to a metre, and spectrum and level both vary substantially over a few metres near a reflecting surface. **Any comparison to the MTA's figures inherits an unquantified position error.**

7. **C3 and C4 assume acoustic events can be cleanly separated.** At an 85 s headway with a ~7 s event this is comfortable. But with four tracks and two directions, **simultaneous or overlapping passages must occur**, and the peak-picking will merge them into one event. This will bias the measured headway distribution long and the count low. The analysis should detect and report merged events rather than quietly counting them as one.

8. **The whole document assumes a phone recording will be accepted as evidence by anyone who matters.** It may not be. Its realistic standing is as **pilot data that justifies a properly instrumented campaign** — Methods 1, 7 and 11 — rather than as a substitute for one. It is written to make that escalation easier to argue for, not to avoid it.

---

## Related documents

- [`README.md`](README.md) — programme overview, artifact index, and the register of what has not been done
- [`IDEA-CONCEPT.md`](IDEA-CONCEPT.md) — the problem, the measured evidence base, and §1.7's derived event duration
- [`PRECEDENT-AND-MATERIALS.md`](PRECEDENT-AND-MATERIALS.md) — worldwide precedent and materials options
- [`WILLIAMSBURG-COMPARATOR.md`](WILLIAMSBURG-COMPARATOR.md) — the same-system comparator study
- [`VISUAL-MODEL-FRAMEWORK.md`](VISUAL-MODEL-FRAMEWORK.md) — provenance schema and rendering rules for the 3D model
- [`visual-review/acoustic-demo.html`](visual-review/acoustic-demo.html) — the artifact this protocol would most directly improve
- [`visual-review/model-3d.html`](visual-review/model-3d.html) — the model that currently contains zero measured elements

**Methods this protocol would advance:** 7 (full-spectrum before/after — establishes the "before"), 11 (two-site survey, in a weaker instrument but available now), 16 (walkway photogrammetric survey), 17 (rephotogrammetry, by supplying a modern control set), 19 (the L1 model, by supplying its first measured elements).
