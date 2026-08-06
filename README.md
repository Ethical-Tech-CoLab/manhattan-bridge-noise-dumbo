# Silencing the Span

**Defining the Manhattan Bridge rail-noise problem in DUMBO for a design-build intervention.**

An Ethical Tech CoLab research project.

**Read it in a browser: [ethical-tech-colab.github.io/manhattan-bridge-noise-dumbo](https://ethical-tech-colab.github.io/manhattan-bridge-noise-dumbo/)** — the opening page states the problem and puts every interactive demonstration in front of you; [`research.html`](research.html) holds the evidence underneath it, with every document rendered for reading and the work still to be done set out in priority order.

---

## What this is

A rigorous problem-definition document about noise from NYC Subway **B, D, N and Q** services crossing the **Manhattan Bridge** and received in **DUMBO, Brooklyn**.

It is **not a design**. It is the artifact that must exist *before* a design can be honestly procured: a statement of what is known, what is claimed but unevidenced, and what has never been asked.

**Start with [`IDEA-CONCEPT.md`](IDEA-CONCEPT.md).** It is self-contained, ~19,600 words, 14 parts. Five further documents extend it — see [Documents](#documents).

## Three headline findings

**1. The problem is measured, severe, and confirmed by two independent agencies eighteen years apart.**

| Receptor | Level | Source |
|---|---|---|
| Adams Street Library | **84.65 dB(A) Leq**, 98.1 max | MTA, Dec 2023 |
| Brooklyn Bridge Park dog run | **87.50 dB(A) Leq**, 98.9 max | MTA, Dec 2023 |
| DUMBO Archway | 81.33 dB(A) Leq, 91.8 max | MTA, Dec 2023 |
| Front & Pine Streets | **94.4 dB(A)** vs 68.2 background | MTA, Jun 2022 |
| John & Adams Streets | **L10(1) ≈ 81 dBA** | Brooklyn Bridge Park FEIS, May 2005 |

The 2005 FEIS also measured **trains at 77 dBA against vehicular traffic at 63 dBA** — a 14 dB separation, meaning roughly 96% of the acoustic energy is rail — and an **L10−L90 spread of 16 dBA** against 4 dBA at a Brooklyn-Queens Expressway control site, the signature of an event-dominated field. Trains cross roughly **every 76 seconds**, about 20 hours a day.

**2. Twenty-one years of measurement without mitigation — and a blank cell in a statute helps explain it.**

**N.Y. Public Authorities Law § 1204-a** ("Rapid transit noise code") expressly covers *elevated structures*, protects *"any person who is within range of subway noise,"* prescribes worst-case measurement, and sets a 4/8/12-year compliance schedule. Its Sound Level Table has four categories. Three carry numbers.

> **IV. ELEVATED STRUCTURES — "Sound level to be established"** — 10% / 30% / 60%

No evidence was found that the level was ever established. The Manhattan Bridge is an elevated structure. Category IV is its category. Category IV has no standard.

**3. That blank cell is not an isolated omission. It propagated — and the result is that rail noise in New York City is not under-reported, it is *unreportable*.**

Three further instruments for recording urban noise in this city each contain **no category for rail**:

| Instrument | What it is | Rail category |
|---|---|---|
| **NYC 311** | The city's complaint system — the dataset cited whenever anyone says noise is New York's top quality-of-life complaint | **None.** Citywide, all complaint types, since 2020: every category matching "subway", "train" or "rail" is a **guard rail or a trailer**. |
| **SONYC** | NYU's NSF-funded acoustic sensor network. 55+ sensors, **150M+ recorded clips**, 18,510 citizen-annotated | **None.** 8 coarse and 23 fine classes. There is a class for `dog`. There is none for rail. |
| **NYC Noise Code** | The city's noise ordinance | **None** — and the SONYC authors state their taxonomy was built *"through consultation with the New York Department of Environmental Protection **and the New York noise code**."* |

Within **500 m of the Brooklyn Bridge Park dog run** — where the MTA measured **87.50 dB(A) Leq and 98.90 dB(A) peaks** — residents have filed **4,055 noise complaints since 2020**, and **not one of them can be about the train**. That circle produced 117 complaints about ice cream trucks and **95 about barking dogs**. The dogs at the dog run are complainable. The trains over it are not.

This is a **mechanism**, not a motive. Nobody decided to ignore elevated rail noise; the category was never created, and every downstream instrument inherited the absence. It also yields the first remedy in this programme that a resident could act on this month: **amending a taxonomy is a far smaller ask than solving the noise, and it would start generating the missing evidence immediately.** See [`COMMUNITY-EVIDENCE-AUDIT.md`](COMMUNITY-EVIDENCE-AUDIT.md) — including the queries, printed in full so they can be re-run, and Part 7 on why the causal chain joining the three is the weakest joint in the argument.

### And one result derived here rather than found

The MTA never published how long a train event lasts — but it published enough to determine it. Solving the session energy balance for the three public outdoor measurements gives equivalent event durations of **5.70, 6.28 and 7.25 seconds**: three sessions, different days, different places, baselines 21 dB apart, agreeing to within **1.04 dB of event energy**. Run the same arithmetic on the *indoor* rows and it breaks — which is independent corroboration that the indoor and outdoor datasets are not describing the same thing. See [`IDEA-CONCEPT.md` §1.7](IDEA-CONCEPT.md) for the derivation and its weaknesses, and [`visual-review/acoustic-demo.html`](visual-review/acoustic-demo.html) to hear it.

### And one dataset built here rather than found

**How often does a train actually cross?** Every acoustic argument in this repository depends on that number, and until now it was taken from three short MTA sessions. It is derivable exactly, for every hour of every day type, from the MTA's own published feed — free, no API key, in about a minute. **1,073 traversals on a weekday, 667 on a Saturday, 651 on a Sunday**, peaking at **67 per hour — a 54-second headway — at 08:00**. By standard noise period: **61.6/hr daytime, 48.0/hr evening, 17.8/hr night** on a weekday. See [`data-collection/`](data-collection/README.md) for the full tables and the four traps that each silently produce a wrong answer, or [`visual-review/frequency-dashboard.html`](visual-review/frequency-dashboard.html) to explore it by hour, route and direction.

Two things fell out of it that were not being looked for. **The schedule cannot answer the overlap question** — every departure in the feed sits on an exact :00 or :30 second, so counting simultaneous crossings measures the scheduler's rounding rather than the railway; an earlier 6.2% figure published here is withdrawn on that basis. And **the "peak park use is out of phase with peak train frequency" finding has been narrowed**, because the affected corridor is far larger than the park and two of its three receptor populations are *in* phase. Both corrections are documented in place.

### And one claim this repository disproved by counting

Having withdrawn the park-phase finding, this repository replaced it with a confident statement: **the worst case is the weekday morning, when the train rate is at its 24-hour maximum.** Then the pedestrian data arrived.

**That is withdrawn too.** The corridor **fills in the morning and empties in the evening** — net arrivals minus departures peak at **+800 at 09:00** and bottom out at **−590 at 20:00** — so at the 08:00 train peak only about **46%** of the day's eventual population is present. Multiply presence by train rate and the weekday 08:00 hour scores **50 out of 100 on the exposure index. The peak is 14:00**, and on Saturday and Sunday it is 13:00 and 15:00. All three land in the early afternoon, because **train rate is nearly flat from 07:00 to 19:00 while the number of people underneath changes by a factor of four in the same window.**

**The same error was made twice, in opposite directions** — first optimising on attendance alone, which pointed to the weekend afternoon; then on train rate alone, which pointed to the weekday morning. Exposure is the product of the two, and it peaks between them. Both withdrawals are on the face of [`visual-review/frequency-dashboard.html`](visual-review/frequency-dashboard.html), which now carries three.

### And one model that found the limit of its own data

`build_cohort_model.py` fits four cohorts — workers, visitors, transients, residents — to the observed departure curve, to get from a flow to a stock. It works, and then it reports that it cannot do the thing it was built to do.

**The total number of non-residents present is pinned to about ±10%. The split between workers and visitors inside that total is not identified at all** — it swings by more than half again across thousands of parameter sets that fit the data equally well. The reason is permanent, not computational: **a departure curve carries no job titles.** Someone present for eight hours looks identical whether they came to work or came for the day.

On a Saturday the model is explicitly **degenerate**: only 33% of fitted "worker" arrivals land in the morning, so the label describes nothing. The script says so in its own output rather than reporting a tidy number. **Total non-resident presence may be quoted. The worker/visitor split may not.**

### And one propagation model that was built and then rejected

Building the agent model required a noise level at every point, so a line-source propagation model was fitted to the four MTA measurement sites. The three near-bridge sites agreed with ideal line-source spreading **to within 0.15 dB**, which looked like a genuine result.

It is not one. A Monte-Carlo test jittering the eye-digitised positions by ±10 m puts the fitted decay exponent **anywhere between 0.7 and 22.3** — from no decay at all to steeper than a point source. The data cannot constrain a propagation model, and the agreement is coincidence. **The model was deleted before publication rather than after**, which is a first for this programme.

What survived the test is more useful: **distance does not order the measurements.** The DUMBO Archway, directly under the structure, is the quietest of the four. Brooklyn Bridge Park's Main Street section, several hundred metres away across open water, is the loudest — and exceeds a prediction fitted to the near sites by about **17 dB**. For it to be consistent it would have to sit roughly seven metres from the track centreline, which is not a position that exists.

**The design consequence is direct.** Under-deck treatment — the intervention most often proposed, and the first item in the November 2025 residents' petition — would be applied **where the measured problem is smallest.** That is a cheap claim to test: one afternoon, a meter and a tape measure. It is registered as Method 31.

## Documents

| Document | Asks |
|---|---|
| **[`IDEA-CONCEPT.md`](IDEA-CONCEPT.md)** | **What is the problem?** Defines the DUMBO rail-noise problem from agency evidence, establishes who is responsible under what law, and derives the questions nobody has asked of this site. Q1–Q13, Methods 0–5. |
| **[`PRECEDENT-AND-MATERIALS.md`](PRECEDENT-AND-MATERIALS.md)** | **What has the world already built?** Surveys elevated-transit noise mitigation precedent worldwide — Japan, China, Sweden, Germany, Hong Kong, Australia, Chicago — plus materials and robotics to 2026, and tests what actually transfers to a 1909 suspension bridge. Q14–Q22, Methods 6–10. |
| **[`WILLIAMSBURG-COMPARATOR.md`](WILLIAMSBURG-COMPARATOR.md)** | **There is a second bridge with the same owner, the same operator, the same division of rolling stock and the same statute. What does it already tell us, and what would measuring it establish?** A two-site comparative survey of the public outdoor space beneath both East River subway bridges. Q23–Q31, Methods 11–14. |
| **[`VISUAL-MODEL-FRAMEWORK.md`](VISUAL-MODEL-FRAMEWORK.md)** | **Every argument in the first three documents is an argument about a cross-section nobody has drawn.** Can that drawing be built from open data and open tools — and can it be made to admit what it does not know? Q32–Q41, Methods 15–20. Reference implementations: [`visual-review/section-problem.html`](visual-review/section-problem.html) and [`visual-review/model-3d.html`](visual-review/model-3d.html). |
| **[`FIELD-CAPTURE-PROTOCOL.md`](FIELD-CAPTURE-PROTOCOL.md)** | **Every acoustic claim this programme makes beyond the published levels is invented. Can a consumer phone fix that this month?** A capture protocol for a Samsung Galaxy S23+ targeting the four things the MTA's five-number table discarded — spectral shape, temporal envelope, headway distribution and train attribution — all of which survive an uncalibrated recording chain. Captures C1–C5. Advances Methods 7, 11, 16, 17 and 19. |
| **[`COMMUNITY-EVIDENCE-AUDIT.md`](COMMUNITY-EVIDENCE-AUDIT.md)** | **The people who live under it have been complaining since 2008. What have they already recorded, and why can nobody find it?** A search of Reddit, Freesound, the NYU sensor corpus, NYC Open Data, local press and petitions for crowd-sourced recordings. Finds none — and finds the structural reason: three instruments for recording city noise, no rail category in any of them. Q42–Q51, Methods 21–25 and 31. |
| **[`data-collection/README.md`](data-collection/README.md)** | **How many trains, how many people, for how long, and in what shape of space?** Six runnable scripts against MTA and NYC open data, plus the four traps that each silently produce a plausible wrong number, the direction trap in the turnstile feed, the cohort model that establishes its own non-identifiability, and the corridor geometry that establishes which object in it is unsurveyed. Methods 26–29 and 32. |
| **[`pedestrian-site-visits/README.md`](pedestrian-site-visits/README.md)** | **The first material here that was not retrieved from somebody else.** Two days of phone video, stills, by-product audio and stopwatch laps captured under the bridge, and a careful account of why none of it is a decibel. **v1.1 withdraws v1.0's headline in place** — an audio duty cycle was used to refute a stopwatch reading, and the two are independent samples 62 minutes apart. What survives is the first photographic record of the echo chamber this repository had only modelled, the geometry of every capture, one methods finding: a defective recording detected before it was disclosed, and **v1.2 adds the first direct observation of evening pedestrian presence** — two stills reassigned by operator statement of intent from the canyon material to the cohort study. Q56–Q60, Methods 38–41. Renders as [`media.html`](pedestrian-site-visits/media.html). |
| **[`usage/README.md`](usage/README.md)** | **What did producing this repository consume?** A per-request ledger read from the tool's own store, priced by billing channel, with elapsed time measured four ways that disagree by an order of magnitude and an energy figure whose own bracket spans a factor of twenty-four. Method 33. |
| **[`procurement/README.md`](procurement/README.md)** | **What would the same deliverable have cost to buy?** Three instruments — dollars actually obligated on 56 federal noise-study contracts, a bottom-up build at GSA awarded ceiling rates verified cent-for-cent against a vendor's own published card, and the metered inference ledger — reported side by side and **never averaged**, because their disagreement is the finding. Q55, Method 37. |

The second document is organised around **two research tracks, partitioned by who owns the asset you would have to touch**:

- **Track A** — NYCDOT bridge steel, the path, and the receptors. *Assumes the MTA system is not modified.*
- **Track B** — MTA rail, fixation, attachments and substrate.

**These tracks are an implementation partition, not a physical one.** Draft v1.0 of that document wrongly assigned frequency bands to owners; v1.1 withdraws it. The physical partition is excitation → radiator → path → receptor, and the two are orthogonal.

## Interactive artifacts

Seven self-contained HTML files. **No build step, no server, no network access, no dependencies** — download and double-click, or clone and open. Each is a reference implementation of the provenance discipline described in `VISUAL-MODEL-FRAMEWORK.md`, applied to a different medium. The seventh applies it to the study itself.

**Start here:** the published site at **[ethical-tech-colab.github.io/manhattan-bridge-noise-dumbo](https://ethical-tech-colab.github.io/manhattan-bridge-noise-dumbo/)**. It is two pages behind a three-item menu. [`index.html`](index.html) is the opening page and an executive summary: what the problem is, the interactive demonstrations, and what has actually been found. [`research.html`](research.html) is everything underneath it — all eleven documents with a line on what each one found, where the investigation stands, the work still to be done in priority order, and every script and dataset. **The header used to carry twelve items and now carries three**, because a table of contents and a menu are not the same object: a reader who has never heard of this problem cannot tell from "3. Comparator" whether it is worth a click. Both pages are regenerated by [`build_pages.py`](build_pages.py), which parses the method register, the question numbers and the word counts **out of this repository** rather than restating them, so the counts on the site cannot drift away from the work.

| Artifact | What it is for | What to look at first |
|---|---|---|
| **[`visual-review/section-problem.html`](visual-review/section-problem.html)** | **The 2D provenance-tagged section.** Every component of the Manhattan Bridge track zone, colour-coded and dash-coded by how well it is known, with the source rubric attached to each. | Turn off the `DOCUMENTED` filter and watch most of the drawing disappear. |
| **[`visual-review/model-3d.html`](visual-review/model-3d.html)** | **The navigable 3D model.** Both bridges, four zoom tiers from the whole crossing down to a single rail fastener, with anchored callouts, click-to-inspect components, and a live scale bar. | The tier ladder: **T0 Context → T1 Bay → T2 Track → T3 Fastener.** Then turn every provenance filter off. |
| **[`visual-review/noise-canyon.html`](visual-review/noise-canyon.html)** | **The noise canyon.** A five-slide picture essay drawn entirely from open data: the structure photographed, 76 surveyed buildings extruded around the alignment, a true section cut across the corridor, the ordinary walk in from the York Street F platform, and every point along it anyone has ever measured. | The last slide. **Four narrow bands of measured evidence against 1,482 m of walk — 23.4 per cent.** The shaded field is not quiet; it is unmeasured, and that is a different thing. |
| **[`visual-review/acoustic-demo.html`](visual-review/acoustic-demo.html)** | **The audible level demonstration.** Hear a train approach, pass and depart at the correct decibel difference against each receptor's measured background, with live A-weighted meters and CEQR threshold marks. Then run it **continuously at the measured headway**, with a logging-meter strip chart and a running energy average that converges on the published session `Leq`. | Select **Brooklyn Bridge Park dog run**, play one pass-by, and read the difference number. Then start continuous running at 20× and watch the running `Leq` settle onto 87.50. Then read why the event duration on that page is derived rather than published, and why that convergence is a closed loop rather than evidence. |
| **[`visual-review/frequency-dashboard.html`](visual-review/frequency-dashboard.html)** | **The traversal frequency and exposure dashboard.** Every B, D, N and Q crossing by hour, route and direction, split into the standard day / evening / night noise periods, with an adjustable coincidence window and three overlap models — **how many people are underneath**, from arrivals, departures, walkway flow and residents — and **how long each cohort stays**, with the identifiability sweep shown rather than hidden. | Set the overlap model to **Schedule** and drag the coincidence window from 1 s to 29 s. **The answer does not move.** Then cross 30 s and watch it jump — that is the schedule's 30-second rounding, not the railway. Then scroll to the cohort card and read the worker/visitor ranges: they overlap, and that is the finding. |
| **[`visual-review/agent-model.html`](visual-review/agent-model.html)** | **The agentic population model.** Groups — not individuals — enter DUMBO at persona-specific gateways, follow scenario itineraries, contend for capacity, and accumulate a noise dose along their actual path. Four-phase deterministic tick, seeded, with a full event log. A fifth rung models **who is standing in that dose** — reduced sound tolerance, autistic listeners with hyperacusis, over-65s, carried infants, people with a history of cancer, and dogs — and changes nobody's decibels by doing so. | The first panel: **the same itinerary started ninety seconds apart receives a different dose.** Then the arrival-process card, where multiplying bunching by 2.9× moves the dose by 0.006 dB and the reason why is the interesting part. Then the rejected-propagation panel, which is a negative result and the most important thing on the page. Then, at the susceptibility rung, the card that **refuses to compute the one number that would settle the argument** and names the single measurement that would unblock it. |
| **[`pedestrian-site-visits/media.html`](pedestrian-site-visits/media.html)** | **The field media page.** The first material in this repository that was captured rather than retrieved: two days of phone video, stills, by-product audio and stopwatch laps under the bridge. Level traces, a threshold sweep, the stopwatch laps, and where every capture stood against every point anyone has ever measured — with the operator's statements of intent for each capture carried on the page at 5/5, because a measurement can only be read for the purpose it was taken for. | The withdrawal card, which **quotes this page's own strongest claim from yesterday and kills it**: the audio and the stopwatch are independent samples 62.4 minutes apart, so neither constrains the other. Then the echo-chamber frames, which are what the video was actually for and are the first photographs here of the canyon the repository had only modelled. |
| **[`usage/usage-dashboard.html`](usage/usage-dashboard.html)** | **The usage and cost dashboard.** What producing this repository consumed, read from the tool's own per-request log: every model call priced by billing channel, elapsed time measured four ways that disagree by an order of magnitude, sub-agent and compaction overhead separated out, and an energy bracket built from a published per-query figure. Generated by a script that hardcodes nothing about this project and runs against any other. | The two bars under the ledger: **what an agent reads is nearly all of the tokens and half the money; what it writes is under one per cent of the tokens and a fifth of it.** Then the process note at the foot — **the first conclusion this dashboard reached about itself was that the data did not exist**, and it was three minutes from being published as the finding. |
| **[`procurement/procurement-dashboard.html`](procurement/procurement-dashboard.html)** | **The procurement comparison dashboard.** What the same deliverable would have cost to buy, from three instruments that are never averaged: dollars actually obligated on 56 federal noise-study contracts, a bottom-up build at GSA awarded ceiling rates verified cent-for-cent against a vendor's own published card, and the metered inference ledger. Carries a second column for the scope this repository did **not** deliver, and refuses to sum the two. | The first card, which **withdraws the headline before it is made**. Then the discipline populations near the foot: **12,825 project managers against seven acoustical engineers** on the same federal schedule — and the project manager costs more per hour than the specialist. |

### The canyon drawings, and how to change them

[`visual-review/noise-canyon.html`](visual-review/noise-canyon.html) is generated, not hand-written. Everything in it comes from three public sources and one public-domain photograph:

| Source | Supplies | Rating |
|---|---|---|
| NYC OpenData [`5zhs-2jue`](https://data.cityofnewyork.us/d/5zhs-2jue) BUILDING | 960 footprints with `height_roof` and `ground_elevation` | 5/5 VERIFIED |
| OpenStreetMap via Overpass, ODbL 1.0 | 2,826 ways and 9 nodes — streets, footways, parks, water, the subway alignment, the two station nodes | 5/5 VERIFIED |
| MTA document 138061 | The four measured sessions, positioned along the walk | 5/5 levels, 2/5 positions |
| HAER NY-127-7, Jack E. Boucher, via [Library of Congress](https://www.loc.gov/item/ny0980/) | The photograph of the structure. No known restrictions on images made by the U.S. Government. | 5/5 VERIFIED |

**Google Maps is deliberately not used**, and not only because its Terms of Service forbid the derivative work. A picture traced off a proprietary basemap **is not a source**, because nobody else can regenerate it. Everything in these drawings can be re-fetched with [`data-collection/fetch_geodata.py`](data-collection/fetch_geodata.py) and redrawn with [`build_carousel.py`](build_carousel.py).

Slides are declared in [`visual-review/carousel.json`](visual-review/carousel.json). **Adding one is a single JSON object; removing one is deleting it or setting `"enabled": false`; reordering is moving it.** The build refuses to run if any slide is missing `sources` or `caveat`, or names a generator that does not exist — so a picture without provenance cannot ship by accident.

Three cross-checks fell out of building it, and all three are worth more than the drawings:

- **The alignment digitised by eye** in `agent-model.html` and **the alignment fitted to the OpenStreetMap track geometry** differ in bearing by **2.3°**. That is an independent check on a number that had only ever been eyeballed.
- **Every building in the frame is surveyed to the roof. The bridge is not.** No public source gives the deck elevation over DUMBO, so the one object in the picture that makes the noise is drawn as a hatched assumed band rated 1/5 while its 76 neighbours are rated 5/5.
- **Of the 1,482 m walk from the York Street F platform to Pier 1, 347 m — 23.4 per cent — lies within any measured band**, and those bands are drawn as wide as the position uncertainty in the memos rather than as points.

## Data collection

**[`data-collection/`](data-collection/README.md)** — six runnable scripts that establish how often trains cross the bridge, how many people are underneath, how long they stay, and what the corridor is shaped like, from MTA and NYC open data. **No API key, no account, no payment method.**

| Script | Answers | Cost |
|---|---|---|
| **[`bridge_schedule.py`](data-collection/bridge_schedule.py)** | What is scheduled, by hour and day type | One 5 MB download, about a minute. Standard library only. |
| **[`bridge_realtime.py`](data-collection/bridge_realtime.py)** | What actually ran | Polls and de-duplicates; a week takes a week. Needs `gtfs-realtime-bindings`. |
| **[`build_dashboard_data.py`](data-collection/build_dashboard_data.py)** | Per-event train data for [`frequency-dashboard.html`](visual-review/frequency-dashboard.html) | Seconds, after the download. |
| **[`build_pedestrian_data.py`](data-collection/build_pedestrian_data.py)** | **How many people arrive in the corridor, and when** | Four API pulls, about a minute. Standard library only. |
| **[`build_cohort_model.py`](data-collection/build_cohort_model.py)** | **How long they stay — and how badly that is identified** | About six minutes of arithmetic. Standard library only. |
| **[`fetch_geodata.py`](data-collection/fetch_geodata.py)** | **What the corridor is shaped like** — surveyed building heights and the street, park, water and footway network | Two API pulls, about a minute. Standard library only. |

All verified working against the live feeds. [`data-collection/README.md`](data-collection/README.md) carries the full hourly and per-period tables, why **Google Maps is the wrong source** for this (it is downstream of the same MTA feed, and its Terms of Service prohibit the bulk extraction a frequency census requires), and **seven traps that each silently produce a plausible wrong number** — including one that undercounted a live test by 3× with no error message, and one where a fitted chainage origin lands in the river and returns four buildings instead of seventy-six.

### The denominator, partly counted

`build_pedestrian_data.py` addresses what had been the repository's largest hole: **every quantitative claim was about trains or decibels, and none was about people.**

It uses four public datasets, none of which counts a pedestrian directly, and it starts by avoiding a trap. The obvious move — pull turnstile data at York St and High St — **measures the wrong direction.** MTA's own column definition reads: *"Total number of riders that **entered** a subway complex."* Entries are people *leaving* the corridor. Over a whole day the two roughly balance so a daily total looks fine; **by hour they are close to opposite.** Arrivals come instead from the separate Origin-Destination Ridership Estimate, which carries an inferred destination per trip.

| What | Source | Typical weekday, corridor total | Rating |
|---|---|---|---|
| Arrive by subway | MTA O-D estimate `28vm-gjqr` | **22,330** | 4/5 — destinations inferred, not observed |
| Enter the subway | MTA hourly ridership `5wq4-mkjj` | **21,942** | 5/5 — observed fare transactions |
| Off the bridge walkway toward Brooklyn | NYC DOT `6fi9-q3ta` | **7,673** | 4/5 — observed and directional, **but the counter died in 2019** |
| Live in the corridor | PLUTO `64uk-42ks` | 10,128 homes, **15,840–21,431 people** | 5/5 homes, 2/5 people |

**Two datasets built by different methods agree to within 1.77%** on a weekday — a cross-check nobody designed in. The residual is carried through as the uncertainty band on the dashboard's accumulation curve rather than discarded.

**The finding that came out of it forced a third withdrawal.** The corridor fills in the morning and empties in the evening — the signature of a destination district, not a dormitory — so presence at 08:00 is only **46%** of its daily maximum. Multiply presence by train rate and the weekday 08:00 hour scores **50 out of 100**; the real peak is **14:00**. This programme had claimed 08:00 was the worst case. That is withdrawn, and it was **the same error made twice in opposite directions**: first optimising on attendance alone, then on train rate alone. Exposure is the product.

**What it still does not give you is dwell time.** Presence is `L = λW`; this work produces λ and not W. The accumulation curve is therefore a **lower bound on transient presence, not a headcount**, and it excludes residents entirely — almost certainly the largest omission, and the population whose exposure is continuous rather than episodic. **No absolute person-event figure is published anywhere in this repository**, and none should be until dwell time is measured.

### The cohort model, and the limit it found

`build_cohort_model.py` is the attempt at `W`. Four cohorts, each with an arrival profile and a dwell distribution, fitted to the observed departure curve. Visitor dwell comes from a published waterfront-park survey with seven duration bins stratified by residency, at a 45% out-of-town share, mean **2.31 h**. Residents come from the PLUTO count above.

It fits well. **That is not the point, and it is not evidence.** Ten free parameters against twenty-four hourly data points will fit almost anything; a good fit shows only that the structure *can* produce the observed curve.

So the script does not report a point estimate. It sweeps the grid, collects **every** parameter set within 10% of the best fit, and reports the range across that admissible family:

| Day | Admissible parameter sets | Non-residents present at 14:00 | of which workers | of which visitors |
|---|---|---|---|---|
| Weekday | 9,248 | 6,029–7,338 | 3,629–5,490 | 1,460–2,313 |
| Saturday | 2,791 | 5,775–6,516 | 3,462–4,374 | 1,881–2,330 |
| Sunday | 11,590 | 5,932–6,820 | 2,619–3,911 | 2,541–3,137 |

**The total is pinned. The split is not.** And a degeneracy test — what share of fitted worker arrivals actually land in the morning — gives **96% on a weekday, 63% on a Sunday, and 33% on a Saturday**. Below about half, the label describes nothing, so the script marks Saturday `DEGENERATE` in its own output.

One further honesty measure. The unconstrained fit produced fifteen visitors on a Saturday, which is absurd, so two physical priors were declared — visitor arrivals peak no later than 16:00, with a spread of at least two hours, justified by the FEIS. **The priors are then priced**: the script sweeps a strictly larger unconstrained grid and publishes what the constraint costs in fit quality. It costs between **+0.031 and +0.064 RMS** and changes the answer by two orders of magnitude, which is the signature of a flat likelihood surface rather than of a prior overriding evidence.

### The agent model, and why exposure needs a path

[`visual-review/agent-model.html`](visual-review/agent-model.html) exists because **exposure is `∫ noise(position(t)) dt`**, and the cohort model supplies `dt` with no `position(t)` at all. Every noise figure in this repository is attached to a *place*; every population figure is attached to a *polygon*; the two cannot honestly be multiplied.

Groups — not individuals — enter at persona-specific gateways, follow itinerary archetypes (*quick photo stop*, *full tour*, *tour and a meal*, *hang by the water*, *explore the shops*, *walking through*), contend for place capacity, and accumulate a dose along their actual path. The engine is a four-phase tick with a simultaneity rule, deterministic resolution in ascending `group_id`, per-group derived sub-seeds, and a full event log from which the run can be reconstructed. **The same seed produces a byte-identical run**, which is the only reason a reader can check it.

Its architecture is borrowed deliberately from a separate agent-simulation curriculum: the deterministic twin as a first-class agent rather than a mock, the capability ladder as four separate policies rather than four feature flags, and a commons observer that reports externality on parties not at the table. The headline result it was built to show is a **race condition in the precise sense** — two people, same itinerary, ninety seconds apart, different dose, because whether you are on the waterfront when a train crosses is timing and not geography.

**It is a demonstration of mechanism, not a measurement of DUMBO.** It carries an eleven-item weaknesses list on its own face and rates its inputs from 5/5 (the MTA levels, the GTFS headway) down to 1/5 (the noise field between anchors, the itineraries, the walking speeds).

### The 3D model, in more detail

`model-3d.html` answers the request to review the structure *"at a distance and at a very granular review"* through a four-tier ladder. Each tier reframes the camera, swaps the component set, and re-anchors its callouts:

| Tier | Extent | What becomes visible | Components |
|---|---|---|---|
| **T0 — Context** | ~2,400 ft | The whole crossing, the water, the shore, and the sightlines from the track zone to the DUMBO receptors | 8 (MB) / 4 (WB) |
| **T1 — Bay** | ~170 ft | One structural bay: truss panels, chords, floorbeams, the track's position within the section, and the deck arrangement that makes the two bridges different | 7 (MB) / 8 (WB) |
| **T2 — Track** | ~26 ft | Rail, tie, fastener, ballast or direct fixation, and the transverse spacing that every acoustic argument depends on | 6 |
| **T3 — Fastener** | ~2.2 ft | A single fastening assembly — clip, pad, bearer, bolt — at a scale bar reading in **inches** | 6 |

**Every component carries two independent tags**, rendered as colour and as line dash so the classification survives greyscale printing and colour-blindness: `GeometryProvenance` (`MEASURED` / `DOCUMENTED` / `INFERRED` / `ASSUMED`) and `VerificationState` (`VERIFIED` / `SNIPPET` / `UNVERIFIED`). Click any component for its source, its rubric rating, and a note on what that source can and cannot carry.

**The single most important thing in the file is what happens when you switch the filters off.** The model contains **zero `MEASURED` elements and zero elements at a `DOCUMENTED` position.** Hide `DOCUMENTED`, `INFERRED` and `ASSUMED` and the viewport goes completely empty, and the heads-up display says so: *the frame is empty. That is the finding.* Everything you can see is reasoned from photographs, historical accounts and engineering convention. Nothing is surveyed. That is the state of public knowledge about this structure, and the model is built to make it impossible to forget.

Two consequences of that, both deliberate and both stated in the interface:

- **T2 and T3 are generated from one shared template for both bridges.** They are identical because no located source describes either structure at those scales. The identity is not a modelling shortcut; it is an accurate representation of the evidence.
- **No dimension annotation is ever attached to an `ASSUMED` element**, per the rendering rules in `VISUAL-MODEL-FRAMEWORK.md` §5.5. A number next to a guess reads as a measurement, and this project has already had to withdraw claims for exactly that reason.

The sightlines drawn at T0 are **geometric only**. There is no propagation model, no attenuation, no diffraction, and no ground effect anywhere in the file.

### The audio demonstration, in more detail

The MTA's own summary of its DUMBO survey is one sentence: *"On average, the difference between the baseline and the peak sound level is 43 dB(A)."* Forty-three decibels means almost nothing to a reader and everything to a resident. `acoustic-demo.html` moves that number out of the table.

**What is real.** The levels. Every background, peak and session `Leq` on the page is transcribed from MTA doc 138061 or, for the comparator, from the Domino FEIS. The differences between them transfer to your ears exactly.

**What is not.** The timbre. **No third-octave spectrum has ever been published for either bridge**, so the sound is synthesised — generated noise whose level envelope is pinned to the published measurements. The page says this in a red banner before you can turn it on. It also says the thing that most audio demonstrations quietly omit: **a browser cannot reproduce absolute sound pressure level.** What comes out of your speakers depends on your volume knob, your hardware and your room. Only the difference is meaningful.

**A new quantitative result, produced in building it.** The MTA publishes four numbers per public session — `Leq`, peak `Lmax`, train-free baseline, and *N* trains over a duration *T* — but never how long a train event lasts. Those four numbers nonetheless *determine* it, under an energy balance:

`Te = ( T · 10^(Leq/10) − T · 10^(Lbase/10) ) / ( N · ( 10^(Lmax/10) − 10^(Lbase/10) ) )`

Solved across the three public outdoor sessions — taken at different places, on different days, with different train counts and different session lengths — the equivalent event durations converge on **5.70, 6.28 and 7.25 seconds**, a spread of only **1.04 dB** in event energy. That mutual consistency is evidence the three sessions are measuring the same physical event.

**The indoor rows do not converge at all**, and the page shows them failing rather than hiding them. 31 Washington Street resolves to half a second, because across 423 trains its Max `Lmax` is a rare outlier rather than a typical event. 56 Adams Street resolves to a 100% duty cycle — an impossible result, arising because the MTA table reports an `Leq` there identical to its Avg `Lmax`, which looks like a reporting artefact in the source and which no one appears to have queried. Both divergences are independent support for `IDEA-CONCEPT.md` §1.3: **the indoor and outdoor datasets are not describing the same thing.**

The demo shows a **modelled** level and a **rendered** level side by side. They agree to a few tenths of a decibel — and the page states plainly that this agreement is *engineered, not evidential*. It confirms the synthesis is scaled correctly. It confirms nothing about the bridge.

**Continuous running — the mode that carries the argument.** A single pass-by is an *event*. What a person sitting in Brooklyn Bridge Park experiences is a *process*: the same event, on a headway, for twenty hours a day. Those are different claims about harm, and only the second is the problem the MTA was asked about. The headway is published — it is the session duration divided by the train count — so the process is as derivable as the event is. Continuous mode runs that loop indefinitely, at the measured headway (**87 s** at the dog run, **85 s** at the DUMBO Archway, **126 s** at the Adams Street Library), summing the three nearest events so that overlapping tails are not discarded. A logging-meter strip chart draws roughly three headways of modelled history, and a **running energy average** accumulates on screen.

That running average converges on the published session `Leq` — 87.50 dB(A) at the dog run — and the page is explicit that this is a **consistency check on the arithmetic, not independent evidence**: the event duration was solved *from* that `Leq`, so the loop is closed by construction. It does not quite close exactly, and the residual is stated rather than removed: §1.7 treats each event as *replacing* the baseline for its duration, while the loop adds the event on top of a baseline that never stops, which leaves the loop 0.002 dB high at the dog run and 0.021 dB high at the DUMBO Archway.

Three further constraints on how the loop should be read:

- **The loop renders a *mean* as a *rhythm*.** Real service is not a metronome. 26 trains in 37 minutes 45 seconds is an average; the real intervals scatter, bunch behind delays, and differ by direction and service. **Nothing here should be described as "what it sounds like" without that caveat.** It is what a regular service at the measured average rate would sound like, and it also runs a daytime headway indefinitely where real service thins overnight.
- **Time compression (1×, 6×, 20×) is level-preserving.** Every interval scales by the same factor — the gaps *and* the pass-bys — so the duty cycle, and therefore the energy average, is unchanged. The only thing compression falsifies is the tempo.
- **Two receptors have the mode disabled.** Front and Pine Street and the Williamsburg Bridge walkway publish no train count and no session length, so neither has a measured headway. The button is disabled with an explanation rather than filled with a plausible guess.

The first version of this page shipped a button labelled *"Continuous, at the measured headway"* that capped the interval at thirty seconds. **That is withdrawn**, and the correction is recorded on the page itself.

### Structure of `IDEA-CONCEPT.md`

| Part | Question |
|---|---|
| 1 | What is the problem, in numbers? |
| 2 | What does it feel like to live in? |
| 3 | Who is responsible, and under what law? |
| 4 | What is physically causing it? |
| 5 | What has been tried, and how well does it work? |
| 6 | What is the design constraint nobody has named — or measured? |
| 7 | What material science could clear that constraint, if it binds? |
| 8 | Could robotics make it installable and maintainable? |
| 9 | What is the labor and maintenance model? |
| **10** | **What are the questions that have not been asked of this site?** (Q1–Q13) |
| 11 | How would we answer them? (Methods 0–5, ranked) |
| 12 | What project should be procured? |
| **13** | **Where might this document be wrong?** |
| 14 | Sources, with credibility scores and verification states |

**Parts 10 and 13 are the contribution.** Parts 1–9 are synthesis.

### Structure of `PRECEDENT-AND-MATERIALS.md`

| Part | Question |
|---|---|
| 1 | How is the option space organised, and what partitions it? |
| 2 | How much of the noise is the structure itself? |
| 3 | **Track A** — what has been built on the structure, the path and the receptor? |
| 4 | **Track B** — what has been built on track, attachments and substrate? |
| 5 | What regulatory architecture exists elsewhere that New York lacks? |
| 6 | What materials and methods are actually available in 2026? |
| 7 | What are the labour, maintenance and whole-life models? |
| 8 | **What actually transfers to a suspension bridge?** |
| **9** | **The questions this survey opens** (Q14–Q22) |
| 10 | How would we answer them? (Methods 6–10) |
| **11** | **Where might this document still be wrong?** |
| 12 | Sources, retrieval priorities, and what was explicitly not found |

**Parts 8 and 11 are the contribution.** A survey that lists what exists without testing transferability is a catalogue, not research.

### Structure of `WILLIAMSBURG-COMPARATOR.md`

| Part | Question |
|---|---|
| 1 | Why this bridge, and why is it not merely "another case study"? |
| 2 | What are the two bridges actually, structurally? |
| 3 | What data already exists for the Williamsburg Bridge? |
| **4** | **The regulatory finding: outdoor space is orphaned** |
| 5 | How do you design the inference — and which metric? |
| 6 | The measurement protocol |
| **7** | **The questions this opens** (Q23–Q31) |
| 8 | How would we answer them? (Methods 11–14) |
| **9** | **Where this document is likely to be wrong** |
| 10 | Sources, retrieval priority, and what was explicitly not found |

**Parts 4 and 5 are the contribution.** Part 4 finds a regulatory hole; Part 5 finds that the entire New York evidence base is recorded in units that cannot support the comparison anyone would want to make.

### Structure of `VISUAL-MODEL-FRAMEWORK.md`

| Part | Question |
|---|---|
| 1 | Why build a model at all, and which question is it supposed to answer? |
| 2 | What geometric data already exists — including the negative results |
| 3 | The occlusion problem, and four ways past it |
| 4 | The level-of-detail ladder, mapped to `LOD` and `LOA` |
| **5** | **Carrying provenance alongside accuracy** |
| 6 | The open-source toolchain, and where it will mislead you |
| 7 | What a model of this is actually for — three uses, three data requirements |
| 8 | The reference implementation |
| **9** | **The questions this opens** (Q32–Q41) |
| 10 | How would we answer them? (Methods 15–20) |
| **11** | **Where this document is likely to be wrong** |
| 12 | Sources, retrieval priority, and what was explicitly not found |

**Part 5 is the contribution.** Everything else is inventory.

## What the comparator study found

**1. The city measured 82.5 dB(A) on the Williamsburg Bridge walkway and responded with one extra decibel of glazing.**

The Domino Sugar rezoning FEIS recorded `Leq` **82.5 dB(A)** and `L1` **92.3** at a monitoring site on the Williamsburg Bridge pedestrian walkway. The entire regulatory consequence, in the document's own words, was that *"the south and west facades would require 31 dBA of attenuation rather than 30 dBA"* — a requirement placed on a private developer's windows.

**CEQR's attenuation machinery acted only on building envelopes here, and a park has none.** In this instance people in outdoor public space were not merely under-protected; they were outside the analysis — the FEIS says the bridge sites were used *"solely for the purpose of determining the building attenuation required."* Whether that is a system-wide gap or one project's scoping decision is **not** established: draft v1.1 withdrew the broader claim and filed it as Method 14, a proper review against the CEQR Technical Manual and the Noise Control Code. It is the frame a design-build proposal should be built on if it survives that review, because it would be a hole rather than a failure.

**2. Nobody has published the one metric that would let the two sites be compared.** `Leq` and `L10(1)` integrate or rank over a period, so they measure the *timetable* as much as the bridge; `Lmax` discards event information. **No located document on either bridge reports `SEL`**, the per-event energy metric. Draft v1.0 concluded from this that "the entire New York evidence base is in the wrong units" — **that is withdrawn.** `Leq` and `L10` are the correct units for the regulatory purpose they serve. They are simply not sufficient for a between-site comparison, and `SEL` is not sufficient either, since consist length, axle count and speed also differ.

**3. Rutgers CAIT instrumented the Manhattan Bridge and found an association between joint condition and structural response.** Working with NYCDOT, they classified bolted rail joints fair, poor and severe, and found that *"the more severely misaligned splices resulted in more vibration on the bridge, almost double that of the fair splices."* The same researchers observe that *"many of the problems these days are actually on the approach spans."* This partially answers Q2 — bolted joints exist and are misaligned. Draft v1.0 read it as evidence of maintenance "headroom"; **that is withdrawn** — there was no treatment trial and no acoustic outcome was measured. It remains the cheapest, most inconvenient possible lead for the programme.

**4. And the comparison itself is weaker than the first draft claimed.** Draft v1.0 framed this as a matched-pair natural experiment that could falsify a mechanism. It cannot. Fleet, speed, consist, service frequency, rail and joint condition, structural mobility, approach geometry and receptor propagation field all change together with the bridge. v1.1 reframes it as a **two-site comparative survey**: it can establish magnitude, character, and whether a difference exists large enough to be worth explaining. It cannot identify why.

## What the visual framework found

**1. Neither subway-carrying bridge has measured drawings in the national record. Their neighbour does.**

| Bridge | HAER survey | Photographs | Measured drawings |
|---|---|---|---|
| Brooklyn Bridge | `ny1234` | 90 | **1 sheet** |
| Manhattan Bridge | `ny0980` | 11 | **none** |
| Williamsburg Bridge | `ny1263` | 9 | **none** |

The only transverse dimensions stated in any located source for either bridge are the Williamsburg Bridge's **67 ft truss width and approximately 40 ft truss depth**, from a 2005 AISC paper co-authored by NYCDOT's Director of East River Bridges. Both describe the overall envelope; neither locates any element within the section.

**2. The occlusion problem puts a hard floor under every open dataset.** Every citywide 3D dataset New York publishes is captured from an aircraft, and an aircraft sees the top of the deck. The floor beams, stringers, fastenings, cantilever framing and clearance envelope are all underneath it. **The surfaces that matter most acoustically are exactly the ones an aerial survey cannot see** — and that is a line-of-sight limit, not a resolution limit that money would fix.

**3. Section geometry governs what the structure radiates — and we do not know how much of the total that is.** In a validated vibro-acoustic model of three elevated rail bridges differing *only* in section geometry, **structure-radiated** noise varied by **8.3 to 11.6 dB(A)** (Li, Dai, Zhu & Thompson, *Applied Acoustics* 186, 2022).

Draft v1.0 set that beside the MTA's 3–5 dB(A) fastener figure and concluded *"the cross-section is worth more decibels than the fasteners."* **That comparison is invalid and is withdrawn.** The 8.3–11.6 dB(A) is a *component* figure; the MTA's is a *total*. The same paper reports rail noise about 10 dB above bridge noise on those structures — so eliminating bridge radiation entirely would have moved the total by roughly **0.4 dB**.

What survives is stronger. Section geometry matters at the receptor **if and only if** structure radiation is a significant share of the total, and on the Manhattan Bridge that share has never been measured. This promotes **instrumented source apportionment** (`IDEA-CONCEPT.md` Method 1) from a useful investigation to a **prerequisite** — no design-build proposal that skips it is defensible.

**4. The proposal: make the model carry the same provenance rubric as the prose.** `LOD 500` already requires that accuracy be *"noted or attached to the Model Element,"* and the USIBD `LOA` scale already separates Measured from Represented Accuracy — but nothing in the delivery chain requires *unmeasured* elements to be labelled as such, so surveyed and reasoned geometry ship as one undifferentiated object. Document 4 proposes **complementary lineage metadata** carried alongside `LOA`: two independent fields, `GeometryProvenance` (`MEASURED` / `DOCUMENTED` / `INFERRED` / `ASSUMED`) and `VerificationState` (`VERIFIED` / `SNIPPET` / `UNVERIFIED`), rendered visibly in the geometry and filterable. Reliability tagging is established practice in heritage BIM; **no novelty is claimed** — whether an analogue exists for transport infrastructure is filed as Method 20 and has not been searched.

Keeping the two fields independent is the point. A source can be fully `VERIFIED` and still support no geometry at all, because a sentence establishing that an element *exists* says nothing about where it is.

Of 27 components across both sections in the reference implementation: **0 measured, 0 documented, 23 inferred, 4 assumed.** Not one element of either section is drawn where any source places it; switching off both the inferred and assumed geometry leaves an empty frame. *(Draft v1.0 reported "8 verified, 10 inferred, 9 assumed" and "9 of 14 on the Manhattan Bridge placed by reasoning." Both were wrong — the artifact had collapsed the two schema fields into one, and the second figure excluded the inferred components, which are also placed by reasoning. The corrected Manhattan figure is 14 of 14.)*

**5. Nobody can currently specify a robotic intervention on this bridge from public information.** Not scope it, not price it, not choose an end effector, not write a procurement document — because no public description of the work surface exists at the resolution any of those tasks require. Draft v1.0 called this "the first obstacle to the robotic thesis" and said the geometry gap "precedes the robotics question by two levels of development." **Both are withdrawn:** BIMForum states explicitly that `LOD 500` is not higher than `400`, so LOD is not a maturity ladder; and a robot can work from a task-specific survey or onboard sensing without any prior model. What remains is a **planning and procurement** blocker, not a technical one — and the way through it is surveying one representative bay, not modelling the structure.

**6. Geometry is necessary and nowhere near sufficient.** No scan, drawing or model at any level of detail yields dynamic stiffness, loss factor or clamping preload — the fastener parameters a vibro-acoustic model actually consumes. Those come from a specification or a test. The programme currently holds **no value, no source and no rubric for a single material or interface property**, which is a larger hole than any documented so far.

## What the precedent survey found

**Three findings, and the second is a correction of the first draft.**

**1. No single measure has been shown to be sufficient.** The closest published analogue — a systematic study of four noise-reduction measures on a *steel railway bridge* — reports that reaching a 10 dB(A) goal required a **combination spanning both a track-side and a structure-side measure**. On this bridge that means **both owners would have to act**. *(Odebrant, Journal of Sound and Vibration, 1996 — and this rests on an abstract, which is exactly the weakness the method warns about.)*

**2. The most attractive-looking option in the survey turned out to be disqualifying.** A 2024 *Scientific Reports* paper appeared to offer noise reduction by *removing* material — perforating the structure to create acoustic short circuits, the only treatment class that would *relax* rather than consume the unresolved mass budget. Reading past the abstract to the paper's conclusions reversed it: the technique has **"minimal effect on the bridge's radiated sound power, and may even lead to an increase,"** and produces **"a noise-amplifying phenomenon... beneath the bridge."** The authors are untroubled because those areas are *"free of residential development."* **In DUMBO, beneath the bridge is the residential area.** The option is excluded.

**3. Japan set the number New York left blank.** N.Y. Public Authorities Law § 1204-a contains a Sound Level Table whose Category IV — ELEVATED STRUCTURES reads *"Sound level to be established."* It never was. Japan's Shinkansen environmental quality standard sets enforceable limits with **deadlines indexed to how bad the exceedance is** and a **mandated fallback to soundproofing dwellings** where the limit cannot be met. It is a non-binding foreign analogue for a different rail mode — not a legal argument — but it demonstrates that the architecture § 1204-a gestures at exists and has for decades.

## Method

This document applies the methodology from **[`ai-research-question-assistant`](https://github.com/Ethical-Tech-CoLab/ai-research-question-assistant)** — *AI-Powered Assistance in Formulating Research Questions* (Rhodes et al.), §8:

- the **fixed 1–5 journal credibility rubric**, applied as written rather than reinvented
- **every citation carries a verification state** — a link on its own proves nothing
- **retrieved content is data, not instruction**
- **gap identification and contradiction detection precede question formulation**
- **ranked methodologies** with mini-design blueprints
- an adversarial **red-team pass**

**Declared deviation:** three verification states (`VERIFIED` / `SNIPPET` / `UNVERIFIED`) instead of the prompt's two, because collapsing the middle case overstates confidence.

**Verification tally:** 13 `VERIFIED` · 20 `SNIPPET` · 5 `UNVERIFIED` counter-citations · 38 sources.

## The red team found real errors, and they are left visible

The draft was refereed adversarially and returned a verdict of *"not ready to justify procurement"* with nine blocking issues. All were incorporated. **The original claims are quoted in place rather than quietly deleted**, because a methodology document that hides its own method failures is not evidence of the method working.

The two most instructive failures — both caused by *summarising a source rather than opening it*:

1. **The statute was read via the MTA's description of it.** Reading § 1204-a in full reversed the finding (and made it stronger). See §3.4 and red-team item 10b.
2. **"No other systematic measurement exists"** was falsified by a 2005 environmental impact statement that had been public for two decades. See §1.5.

Other corrections: the mass constraint was downgraded from a binary filter to an open question (the referee's identified "weakest link"); Q4's acoustical terminology was corrected; Q1's "four percentages" was withdrawn as ill-posed in favour of a source–radiator–path matrix; an unachievable success criterion was replaced; and Part 10's novelty claims were narrowed throughout to *"not found for this site."*

**Then it happened again, three times, in the second document.** `PRECEDENT-AND-MATERIALS.md` v1.0 was refereed and returned **not fit to publish**. Three of its errors had the *same single cause* as the two above — **a source was summarised from its abstract rather than read to its conclusions**:

| Error in v1.0 | What the source actually said |
|---|---|
| Perforation reduces bridge noise and removes mass | It does **not** reduce radiated sound power, may increase it, **amplifies beneath the bridge**, and the openings get covered with mesh plates |
| Cold spray is field-proven on **in-service** bridge steel | The bridge was **decommissioned** — and `IDEA-CONCEPT.md` §8.1 already had this right, so v1.0 contradicted its own companion |
| Track A addresses low frequency, Track B high | False — resilient fasteners are Track B and act on **low** frequency; barriers are Track A and act on **mid/high** |

Also corrected: a rail-damper figure measured in a Perth **tunnel on slab track** had been declared "the applicable figure" for an open steel deck over a river; four separate overstatements in the Japan comparison; and a recommendation to "sequence Track A first" that conflicted with the document's own gates.

**Five errors, one cause, across two documents.** That is the finding the method exists to produce. Rule 2 — *a plausible URL proves nothing; state whether you actually opened it* — is not bureaucratic overhead. **Every single failure in this repository so far has been a rule 2 failure.**

## Where further research should start

Not with more reading. **The four highest-value actions are records requests, not research** — none has been done in twenty-one years, and each closes a larger uncertainty than any literature review could:

1. **The current NYCDOT load rating**, expressed as an allowable mass / eccentric-moment / wind-area / attachment-fatigue budget at the track zone. Gates roughly half the option space. *(Q13)*
2. **The actual joint and rail-fixation inventory** across the four tracks. Not documented in any source located. *(Q2, §4.2)*
3. **The raw 2022–2024 MTA time histories**, via FOIL, to compute CEQR-compatible `L10(1)` properly. *(§3.2)*
4. **The § 1204-a Category IV records** — why was the sound level never established, and could it simply be filled in? *(Q11)*

Then the instrumented source apportionment of **Method 1**.

Two further items come from the precedent survey and are cheaper than either:

5. **A responsibility, approval and interface matrix** for the track–structure boundary — who approves, who is liable, what outage is needed, for each candidate intervention. A desk exercise measured in weeks. *(Q19, Method 10)*
6. **The full text of Odebrant 1996** — the single most load-bearing source in `PRECEDENT-AND-MATERIALS.md` is currently an abstract. *(§12, retrieval priority 1)*

And four more from the comparator study and the visual framework, of which the first two cost an email and a form:

7. **Email Moon and Roy at Rutgers CAIT** for the Manhattan Bridge instrumentation report. It is the only located measurement of *this* bridge's structural response, it is cited here at one remove from an institutional news article, and it partially answers a question flagged blocking in the first document. *(Method 12)*
8. **FOIL request to NYCDOT for record and rehabilitation drawings, both bridges.** Potentially resolves the section geometry, the vertical arrangement, and the fastening specification in a single step. The highest value-per-unit-effort action anywhere in the programme, and it has not been attempted. *(Method 15)*
9. **A two-site `SEL` survey** of the public outdoor space beneath both bridges. Requires no permission from anyone; both measurement positions are public space. A screening and characterisation exercise, not an identification study. *(Method 11)*
10. **A walkway photogrammetric survey of the Williamsburg Bridge**, targeted at the one geometric proposition the shielding hypothesis depends on: the relative *vertical* positions of track, roadway deck, walkway and truss bottom chord. A camera and an afternoon. *(Method 16)*

See also **§14 *Counter-citations*** — five works surfaced during red-teaming that bear directly on Q1–Q8 and were **not read in full**. Any team taking this forward should start there.

## What has not been done

An honest audit, because a research programme that only publishes its outputs misrepresents itself. **Thirty-three methods are specified across the six documents and the data-collection work. One has been partially executed and three have been executed.** The rest are proposals. The distinction matters, because several of the cheapest are also the most load-bearing, and their being undone is the reason so many claims in this repository are hedged.

**All four that were executed changed something, and three of them changed it against the programme's own expectation.** Method 27 — count the denominator — produced pedestrian arrival data that contradicted this repository's own claim about which hour is worst. Method 29 — the cohort model — established that a quantity this programme had been treating as recoverable is **not identifiable at all** from the available data. Method 30 — the agent model — produced a negative result about noise propagation that **withdrew a fitted model before it was published rather than after**. Method 32 — the corridor geometry — was run to draw a picture and instead established that **the only object in that picture whose position and height are unknown is the one making the noise.** It is a demonstration of the general point: **the unexecuted methods are not decoration, and executing them is not expected to be confirmatory.**

**Document 5, [`FIELD-CAPTURE-PROTOCOL.md`](FIELD-CAPTURE-PROTOCOL.md), does not add a method.** It specifies an executable route to parts of Methods 7, 11, 16, 17 and 19 using equipment the programme already has. It is also unexecuted.

**Document 6, [`COMMUNITY-EVIDENCE-AUDIT.md`](COMMUNITY-EVIDENCE-AUDIT.md), adds Methods 21–25 and 31** and is the first document here to rest partly on data this programme queried directly rather than read about. That is genuine progress and it does not change the fundamental position: **nobody from this programme has stood in Brooklyn Bridge Park with an instrument.** Section 3.5 now records one direct field observation by the author, rated 2/5 like any other unaided report and explicitly not upgraded for being ours.

### The method register, and its status

| # | Method | Document | Cost | Status |
|---|---|---|---|---|
| 0 | Documentary and structural envelope review | 1 | Records request + engineer | **Not started.** Prerequisite to everything. |
| 1 | Instrumented source apportionment | 1 | Field campaign, 2 seasons, ≥200 passages | **Not started.** The programme's stated prerequisite — nothing else is non-arbitrary without it. |
| 2 | Staged treatment with untreated control spans | 1 | Capital | Not started. Depends on 1. |
| 3 | Hybrid FE/BE + SEA model | 1 | Modelling | Not started. **Worthless uncalibrated**, so depends on 1. |
| 4 | Longitudinal health and exposure panel | 1 | IRB + several hundred participant-nights | Not started. Depends on 1 for a defensible exposure metric. |
| 5 | Hedonic property-value analysis | 1 | Desk | Not started, and **ranked last on purpose** — identification is likely infeasible here. |
| 6 | Operational modal and radiation survey of the truss | 2 | Dense instrumentation + acoustic intensity | Not started. Answers the gating structural question. |
| 7 | Full-spectrum before/after protocol | 2 | Field | Not started. Must precede any installation. |
| 8 | Receptor-elevation barrier study | 2 | Desk or scale model | Not started. **Can eliminate an expensive option class early.** |
| 9 | Comparative damping-installation study | 2 | Bench | Not started, correctly sequenced last. |
| 10 | Responsibility, approval and interface matrix | 2 | **Desk, weeks** | **Not started.** Plausibly the highest ratio of decision value to cost in the programme. |
| 11 | Two-site `SEL` survey, both bridges | 3 | **Two people, two meters, one week, no permissions** | **Not started.** The cheapest decision-relevant measurement anywhere here. Addresses Q23, Q24, Q26, Q27, Q30 at once. **A weaker phone-based route is now specified — see Document 5, Part 6.1.** |
| 12 | Retrieve the CAIT report — email Moon and Roy, Rutgers | 3 | **An email** | **Not started.** The only located measurement of this bridge's structural response is cited at one remove from a news article. |
| 13 | § 1204-a attention audit, via FOIL | 3 | A form; months of waiting | **Not started.** File first, read last. |
| 14 | Outdoor-space regulatory review | 3 | Desk, a careful reader | **Not started.** The finding most likely to have consequences outside this project. |
| 15 | FOIL to NYCDOT for record and rehabilitation drawings | 4 | **A form and a fee** | **Not started. Priority 1.** Could resolve Q32, Q33 and Q36 in one step. |
| 16 | Walkway photogrammetric survey, Williamsburg Bridge | 4 | **A camera and an afternoon** | **Not started. Priority 2.** Targets the one proposition the shielding hypothesis depends on. **Capture procedure now specified — Document 5, C5.** |
| 17 | Rephotogrammetry of the HAER photographic sets | 4 | Free software, one afternoon | Not started. Priority 4; likely to fail on baseline grounds, and cheap to establish that. |
| 18 | Approach NYCDOT re. the traveling maintenance platforms | 4 | A relationship this programme does not have | Not started. Priority 2. |
| 19 | Build and publish the provenance-tagged L1 model | 4 | Desk, existing public data | **Partially addressed, and not by the specified route.** See below. |
| 20 | Negative-result search on provenance-tagged infrastructure models | 4 | Desk | **Not started. This blocks any novelty claim**, and one has already been withdrawn for being made ahead of it. |
| 21 | **The taxonomy-blindness test** — 311 complaint density in elevated-adjacent tracts vs matched controls, citywide | 6 | **Desk, hours, free** | **Not started.** Tests the central claim of Document 6, using the same public API that produced it. **The cheapest high-value method in the programme.** Either result is publishable. |
| 22 | FOIL the complaint record — MTA NYCT and district offices | 6 | A form; months of waiting | **Not started.** The § 1204-a report already dates official contact to 2022, which makes the request specific and hard to refuse as overbroad. |
| 23 | Read the Reddit and community comment threads, logged in | 6 | **Desk, hours, free** | **Not started, and Document 6 explicitly did not do this.** Automated access returned HTTP 403. If a usable resident recording exists anywhere, this is where it is. |
| 24 | Contact the named community actors and Brooklyn CB2 | 6 | Correspondence | **Not started.** Carries a standing ethical condition — see Document 6, Method 24. |
| 25 | Interrogate the SONYC corpus by acoustic similarity rather than by label | 6 | Desk to research collaboration | **Not started.** 150M+ clips already collected and published. If elevated rail is in there unlabelled, retrieving it would produce the largest such corpus in existence from data that already exists. |
| 26 | **The traversal census** — poll MTA GTFS-realtime for one week and compare actual bridge traversals against schedule | — | **Desk, free, one week unattended** | **Tooling built and verified; the week has not been run.** [`data-collection/bridge_realtime.py`](data-collection/bridge_realtime.py). Now the *only* route to the coincidence distribution, since the schedule was shown to be quantised to 30 s and unable to answer it. |
| 27 | **Count the denominator** — establish pedestrian presence in the DUMBO corridor by hour and day type | — | **Desk first, then fieldwork** | **Partially executed.** [`build_pedestrian_data.py`](data-collection/build_pedestrian_data.py) derives arrival rate, departure rate, walkway flow and resident count from four public datasets, and the result **disproved this repository's own claim** about when the worst hour is. **The arrival rate exists. Dwell time does not**, so presence is a lower bound, not a headcount. |
| 28 | **Measure dwell time** — how long does a person actually stay in the corridor? | — | **Fieldwork, low cost** | **Not started, and now the single blocking unknown.** Presence is `L = λW`; Method 27 produced λ. Without W no absolute exposure figure can be published. A timed cordon count over a few sessions would bracket it. |
| 29 | **The cohort survival model** — infer dwell and presence by fitting cohorts to the observed departure curve | — | **Desk, six minutes of arithmetic** | **Executed, and it reports its own failure.** [`build_cohort_model.py`](data-collection/build_cohort_model.py) pins *total* non-resident presence to about ±10% and establishes that **the worker/visitor split is not identifiable from a departure curve at all**. Saturday is explicitly degenerate. It does not remove the need for Method 28; it establishes what Method 28 must supply and why no amount of further arithmetic will substitute for it. |
| 30 | **The agentic population model** — put the population on a path so that exposure can be integrated rather than multiplied | — | **Desk, built** | **Built as a mechanism demonstration, not executed as a measurement.** [`visual-review/agent-model.html`](visual-review/agent-model.html). Deterministic, seeded, event-logged, with a capability ladder. Its itineraries, group sizes and walking speeds are invented and rated 1/5, and it has been validated against nothing because there is nothing to validate it against. **Its value is that it makes the missing observation precise:** an origin-destination and dwell survey of DUMBO pedestrians. A fifth rung now also models **who is standing in the dose** — decreased sound tolerance, autistic listeners with hyperacusis, people aged 65 or over, infants who are carried, people living with a history of cancer, and dogs — **without applying a single decibel of penalty to any of them.** That restraint is the design, not a limitation: a per-class dB adjustment would be a fabricated exposure–response function wearing the costume of a measurement. What the layer reports instead is counts, person-hours, and the split between people who chose the route and people who were carried or led along it. It also raises two new methods, 42 and 43. **The model now also carries three selectable arrival processes**, and comparing them at a fixed population produced a result worth more than the feature: multiplying peak bunching by **2.9×** moves the mean dose by **0.006 dB** and never by more than 0.047 dB, and tightening the burst further until it is physically impossible *lowers* the difference rather than raising it, because dwell dominates headway. Arrival structure reaches crowding and does not reach the dose. Method 44. |
| 31 | **The decay transect** — walk outward from the structure with a meter and establish where the affected zone ends | 6 | **One afternoon, free if a meter is borrowed** | **Not started.** Nothing has ever been measured at the boundary of the affected zone because no boundary has ever been established — yet that boundary sizes the denominator for every exposure figure here. It also directly tests the anomaly that under-deck sites are the quietest of the four measured. **Three possible outcomes and all three are informative**, including the one that corrects this repository. |
| 32 | **The corridor geometry** — build the canyon from public survey data and find out which objects in it are not surveyed | 4 | **Desk, two API pulls, free** | **Executed.** [`fetch_geodata.py`](data-collection/fetch_geodata.py) and [`build_carousel.py`](build_carousel.py) produce [`noise-canyon.html`](visual-review/noise-canyon.html) from 960 NYC building footprints and 2,826 OpenStreetMap ways. **It did not produce the answer it was run for.** It was run to draw the canyon; what it established is that **76 of the 77 objects in the frame are surveyed to the roof and the one that makes the noise is not**, and that the alignment this repository had digitised by eye is within 2.3° of the alignment fitted to open track geometry. |
| 33 | **The cost of the study itself** — establish what producing this repository consumed, and specify what would have to be instrumented to answer that properly | 8 | **Desk, one SQLite read, free** | **Executed.** [`build_usage_data.py`](usage/build_usage_data.py) produces [`usage-dashboard.html`](usage/usage-dashboard.html) from the tool's own per-request log. **Its first answer was wrong and is withdrawn on the page:** the obvious log holds only session-lifecycle events, and the conclusion that no usage data existed anywhere survived until a second store was found holding one row per model request. What it establishes is that **the cost of summarising the conversation exceeded the cost of everything the user typed**, that **reading is most of the tokens and half the money while writing is under one per cent and a fifth of it**, and that **no measured joule reaches a client**, so the energy figure is an estimate whose own bracket spans a factor of twenty-four. |
| 34 | **Pin one cohort from outside the curve** — measure or import the size of a single cohort so the rest stop being interchangeable | 52 | **Desk, one free federal dataset** | **Not started.** The cohort fit is degenerate by construction: **a departure curve carries no labels**, so someone present for eight hours is identical whether they came to work or came for the day. No amount of further fitting resolves this, and the model already says so — 9,248 parameter sets fit within 10% of the best, and across them the fitted worker count at 14:00 swings 3,629–5,490 while visitors swing 1,460–2,313. **The fix is not a better fit, it is one exogenous number.** LEHD LODES Workplace Area Characteristics gives jobs by census block, free, which pins the worker cohort directly and leaves the visitor cohort as a residual rather than a guess. |
| 35 | **The resident day, and residents as an outdoor population** — model how much time a resident spends outdoors in the corridor, by resident type | 52, 53 | **Desk for the anchor, one afternoon for the local check** | **Not started.** Residents are currently modelled as a stock that is either inside the district or outside it. **Being inside the district includes being asleep indoors**, so the resident curve is a district-occupancy curve and not an exposure curve, which the model states but nothing downstream repairs. The missing term is the outdoor fraction. It is not small: at 18,636 residents, an outdoor share consistent with published leisure-walking figures puts **the unmodelled resident-outdoors population in the same range as the entire visitor cohort the model works hard to estimate.** Sub-types matter because the marginal effect is measurable — dog owners walk about 300 min/week against 168 for non-owners. |
| 36 | **The conservation audit** — close the books on the corridor and report which assumptions move the total rather than only the split | 52, 54 | **Desk, free, uses data already pulled** | **Not started.** Arrivals exceed entries by 1.77% weekday, 2.61% Saturday, 2.84% Sunday, and **that residual is currently attributed to nothing.** It bounds how wrong the arrive/leave logistics can be. The audit sweeps every declared assumption and separates those that move the corridor total from those that only redistribute it between cohorts, which is the distinction the identifiability sweep already shows is the important one. **The resident count is a floor on district population and is not a floor on pedestrians**, and conflating the two would repeat this repository's most frequent error in a new place. |
| 37 | **Price the same deliverable against what the market charges for it** — set the measured production cost beside published labour rates and against dollars actually obligated on comparable contracts | 55 | **Desk, two free federal APIs, executed** | **Executed** — [`procurement/`](procurement/README.md). Three instruments, reported side by side and never averaged: dollars actually obligated on 56 federal noise-study awards (5/5), a bottom-up build at GSA awarded ceiling rates (rates **5/5**, hours **1/5 invented**), and the metered inference ledger (5/5). The delivered desk scope prices at **$177,387–$554,466** at the whole-schedule median; the scope this repository did **not** deliver — field acoustics, the pedestrian survey, licensed design, a preemption opinion — adds **$52,975–$151,556**, and the model refuses to sum the two columns. **The result is the disagreement, not a number:** the bottom-up low lands at 114% of the award 75th percentile, and the two available readings — hours too generous, or awards buying narrower deliverables — cannot be separated without a timesheet nobody publishes. |
| 38 | **Capture at pedestrian level, and read each capture only for what it was taken for** — treat a consumer handset as a recorder of *times and images*, never of levels, and establish what a capture was FOR before computing anything from it | 56, 57 | **One afternoon, a phone already owned, executed** | **Executed, and partly withdrawn** — [`pedestrian-site-visits/`](pedestrian-site-visits/README.md). Two days of video, stills, by-product audio and stopwatch laps at 26–162 m from the fitted track axis; **two capture points stand closer to the track than three of the four points anyone has ever measured.** Nothing is reported as a decibel. **v1.0 of the document made a cross-instrument claim that is withdrawn in place:** an audio duty cycle was used to refute one reading of the stopwatch, and it cannot, because the two are independent samples **62.4 minutes apart with zero overlap** — a fact the operator stated and the file timestamps independently confirm. Independently, the video was shot to photograph the buildings forming the echo chamber and was never an acoustic instrument. **v1.2 reassigns two evening stills** to the pedestrian cohort study by operator statement of intent, establishing the first direct observation of presence in this corpus. **What survives is the first photographic record of the canyon this repository had only modelled**, the geometric placement of every capture, the first image here of the *receptor* rather than the source, the first direct observation of evening weekday presence, a rate that agrees weakly with the timetable and is the one stopwatch quantity independent of the pairing, and **one methods finding: a between-clip test flagged a defective recording before the operator disclosed it.** Against this repository's own protocol the session scores C1 not satisfied, C2 partly and not usefully, C3 partly, C4 and C5 not attempted. |
| 39 | **Direction and speed from a two-point synchronised array** — separate two timecode-locked recorders along the track axis and read the direction of travel from the *order* of the two level peaks, and the speed from the interval between them | 58 | **One afternoon, gear already owned** | **Not started.** Every level in this repository is direction-blind: the MTA memos report a receptor, not a heading, and the schedule feed reports both directions as very nearly balanced in every period, so no existing instrument can say whether a Manhattan-bound crossing sounds like a Brooklyn-bound one. Two transmitters separated 50–80 m along the fitted bearing of **336.93°**, at matched perpendicular offset, resolve it from timing alone — `v = d / (t₂ − t₁)`, with the sign giving direction. **It needs no calibration, because it uses no level.** A perpendicular-offset mismatch of 20 m contributes about 0.06 s against a signal of several seconds, so the measurement is forgiving. The session that establishes it should also log direction **by eye**, because that is what validates the array against ground truth and licenses its use unattended afterwards. |
| 40 | **Measure the decay tail, and report duration as a family indexed by threshold** — fit the envelope on a 125 ms `FAST` constant and publish time-above-threshold across a range rather than one duty-cycle number | 59 | **One quiet-hour session, plus desk** | **Not started.** This is the *"clock time versus floor time"* question, and it has never been measurable here: **automatic gain control actively destroys decay tails**, pushing gain up as the sound fades so the recorded tail flattens and reads both longer and shallower than it is. Any duty cycle computed from such a record is a statement about the compressor. A fixed-gain linear record makes time-above-`(peak − 10 dB)`, time-above-`(background + 3 dB)` and the fitted `n` and `τ` of `L(t) = Lmax − 10n·log₁₀(1 + (t/τ)²)` all computable, and **all of them are gain-independent.** It also converts Document 10's threshold sweep from a caution into a deliverable. **The measurement is background-limited**, so a quiet-hour session will measure a materially longer tail than a midday one, and the difference between the two is itself the answer to how much of the day the tail actually covers. |
| 41 | **Observe simultaneous crossings** — measure what the level does when two trains are on the bridge at once, against the +3.01 dB predicted by incoherent summation | 60 | **Observation only, during any session** | **Not started.** **The published schedule cannot answer this and never could.** Every scheduled departure in the MTA feed falls on an exact `:00` or `:30` second — 1,073 weekday traversals return only `{0: 528, 30: 545}` — so the entire 0–30 s window in which two crossings merge acoustically is *empty by construction*. That is what forced the withdrawal of the merged-pair table in this repository's own phase 9 work, and it means observation is the only available instrument. Two incoherent equal sources sum to **+3.01 dB**; a materially larger rise would indicate that simple energy summation is not what happens on a four-track suspended deck, which would be a new result. Because it is a difference between two events **in the same recording**, unknown gain cancels entirely. |
| 42 | **Count the corridor by attribute, not just by head** — a cordon tally of what is visibly true about the people passing: prams and carried infants, dogs on leads, mobility and assistance aids, apparent age band | 61 | **Rides along with Method 28 at no extra cost** | **Not started.** Every susceptibility share in [`visual-review/agent-model.html`](visual-review/agent-model.html) is a *national* prevalence applied flat to this corridor — 5.90% reporting decreased sound tolerance, 18.0% aged 65 or over, 2.2% under two, 5.40% with a history of cancer, 32% of dogs noise-sensitive — and every one of them is rated **1/5 for whether it applies here**, because nobody has ever counted who is in this corridor by any attribute at all. A flat rate is *knowably* wrong at a place whose purpose selects for a class, and the corridor is full of them: a dog run, a carousel, a lawn, and the residential blocks at Farragut Houses. **The correction is a clicker, not a study.** Method 28 already requires an observer standing at a cordon counting people; tallying four visible attributes at the same time costs nothing extra and replaces the three weakest inputs on the page. **What it cannot do is the honest half of the method:** age band, a pram and a lead are observable, and hyperacusis, autism and a cancer history are not. Those three shares stay national, and the method must publish which of the six it moved and which it did not, or it will read as having verified all of them. |
| 43 | **Convert the loudness-discomfort literature into this corridor's units** — establish what, if anything, licenses comparing a dB HL discomfort threshold to a dB(A) field level | 62 | **Desk, one afternoon — but strictly blocked on capture C1** | **Not started, and it is the one number that would make every harm claim here quantitative.** Loudness discomfort for normal-hearing listeners centres near **100 dB HL**, and hyperacusis is commonly marked at **≤ 90 dB HL**; the MTA measured **98.90 dB(A)** peaks at the Brooklyn Bridge dog run. Those look like they can be compared and **they cannot**: `dB HL` is per-frequency, pure-tone, headphone-presented and referenced to audiometric zero, while `dB(A)` is broadband, free-field and weighted by one fixed curve. The conversion needs the frequency-specific reference thresholds *and* the third-octave spectrum of the actual sound — and this repository has no spectrum for either bridge, which its own field protocol names as the largest single fabrication in the corpus. So this method is blocked on **capture C1 and nothing else**, and that is its value: it converts a vague plea for more data into one specific missing measurement. **It will not produce a clean answer even then.** A headphone threshold and a free-field broadband exposure are different measurements, so the defensible output is a bracket with its assumptions named, not a verdict — and the outcome where the bracket straddles the measured peak is as informative as either clean result. |

| 44 | **Establish whether crowding pushes people toward the noise** — measure the two feeder-line headways, the stair-to-street dispersal at York St and High St, and the capacities of the places people actually compete for | 63, 64 | **Mixed. The headways are one constant and a minute; the capacities are an afternoon; the behavioural half is a study** | **Not started, and its priority was just lowered by a result rather than by a judgement.** Three arrival processes were implemented in [`visual-review/agent-model.html`](visual-review/agent-model.html) — a uniform ramp, Poisson, and slugs on the feeder line's headway — and compared across twelve seeds with the population held identical so that only the timing moved. Bunching rose **2.9×** (14.0 → 40.0 peak groups per minute) and **the mean dose moved by 0.006 dB**, never more than 0.047 dB on any single seed, and a sweep that tightened the stair-climb spread to 0–10 s — a whole train reaching the street at once — *lowered* the difference to 0.001 dB rather than raising it. The mechanism is statable: dwell dominates headway, so even the shortest-dwell tenth eats about seven crossings and phase can shift that by at most one. **Contention is the one quantity that does respond** — up about 18%, positive in eleven of twelve seeds — and every input to it is invented: feeder headways **1/5**, stair dispersal **1/5**, place capacities **1/5**. The cheap half is genuinely cheap: `data-collection/bridge_schedule.py` line 41 reads `BRIDGE_ROUTES = {"B","D","N","Q"}` and already computes exactly this, so `{"F"}` and `{"A","C"}` produce the feeder headways by hour and day type in about a minute. **The expensive half is the one that matters and it is not a measurement of the railway at all**: whether a full bench actually sends someone toward the bridge rather than away from it is a behavioural question, and answering it wrong in the flattering direction would inflate exposure while looking like arithmetic. **Do not run the cheap half alone and report it as progress on exposure** — it has been shown not to reach the dose. |

**On Method 19.** [`visual-review/model-3d.html`](visual-review/model-3d.html) establishes the schema in a working artifact rather than a proposal, which was the method's stated purpose. **It is not the L1 model.** The specification called for 2017 LiDAR, the NYC 3D Model and OpenStreetMap assembled in QGIS and CloudCompare and exported as `IFC` with `Pset_ResearchProvenance` populated. None of that survey data is in the file — the geometry is hand-authored from photographs, historical accounts and engineering convention, which is exactly why the model contains zero `MEASURED` elements and goes empty when the filters are switched off. **Method 19 remains open.** What has been demonstrated is that the tagging discipline is implementable and legible; what has not been demonstrated is that it survives contact with real survey data.

### Retrieval priorities still outstanding

| Source | Why it matters | Blocker |
|---|---|---|
| **Odebrant, *JSV* 193(1):227–233 (1996)** | The single most load-bearing source in `PRECEDENT-AND-MATERIALS.md`, and it is still an abstract | Paywall / interlibrary loan |
| **ROSA-P `dot/35570`** | US transit noise source material | HTTP 403 on repeated attempts |
| **NYC Parks FEIS `12DPR005Q`, Ch. 13** | Part 4's regulatory finding rests partly on a quotation **truncated mid-sentence** | Retrieved only as a `SNIPPET`; not opened |
| **Banfi 2017; Brumana et al. 2019** | The entire heritage-BIM reliability-tagging precedent, and both are open-access | Read as `SNIPPET` only — the same failure mode this programme has corrected five times |
| **IFC 4.3 / ISO 16739-1** | The edition actually cited is unconfirmed | Not verified against the standard |
| **OpenStreetMap geometry for both bridges** | Would give a checkable planform | **Resolved for the Manhattan Bridge.** Overpass returns 406 unless the request carries `Accept: application/json` *and* a User-Agent free of parentheses and semicolons; with both fixed, [`fetch_geodata.py`](data-collection/fetch_geodata.py) retrieves the corridor cleanly. **The Williamsburg Bridge has not been fetched.** |
| **`IDEA-CONCEPT.md` §14 counter-citations** | Five works that bear directly on Q1–Q8 | **Surfaced during red-teaming and not read in full** |

### Questions marked blocking that are still open

- **Q2 — the actual joint and rail-fixation specification** on the four tracks. Not documented in any located source. Method 15 or Method 0.
- **Q32 — the measured transverse section of the Manhattan Bridge** at midspan, at a tower, and at the Brooklyn approach. *Every acoustic argument in this programme depends on it and no source above rubric 1/5 states any of it.*
- **Q33 — the relative vertical positions** of the Williamsburg Bridge's track, roadway deck, walkway and truss bottom chord. Determines whether Document 3's shielding hypothesis is even geometrically possible.
- **Q36 — the dynamic stiffness of the installed rail fastening assembly.** This is the acoustic model's boundary condition, not a detail.

### The largest single hole, named

`VISUAL-MODEL-FRAMEWORK.md` Part 11 item 15: **there is no material and interface property register.** The programme can describe geometry it has not measured and levels it has not recorded, but it has no compiled record of the loss factors, dynamic stiffnesses, damping ratios, bond properties or temperature dependencies of any material at any interface on either structure. Materials cannot be reasoned about without it, and no amount of further reading substitutes for a records request and a bench test.

### The one route to executing any of this cheaply

[`FIELD-CAPTURE-PROTOCOL.md`](FIELD-CAPTURE-PROTOCOL.md) specifies five captures achievable with a consumer phone from public ground, and is the only proposal in the programme that requires no permission, no funding and no relationship the programme does not already have. It does not replace Methods 1, 7 or 11 — it is pilot data intended to make the case for them.

Its strategic claim is that **the phone is a poor sound level meter and an excellent sound recorder, and this programme does not need another sound level meter.** The MTA's levels are already rated 5/5 `VERIFIED`. What is missing is everything its five-number table discarded: spectral shape, temporal envelope, headway distribution and train attribution — **all four of which are relative or temporal, and therefore survive an uncalibrated chain.**

The highest-value item is **C2, the temporal envelope**, because it is the only proposal anywhere in this repository that could establish that the programme's own derived result is wrong. `IDEA-CONCEPT.md` §1.7 solves for event duration under an *assumed* envelope shape, and the continuous audio loop then converges on the published `Leq` **because that is the number the shape was solved from** — a closed loop, which the artifact says of itself and which issues #13 and #15 exist to attack. A single measured envelope opens it.

**None of it has been executed.**

### And one route that costs nothing at all

**Method 21 is a database query.** It uses the same public NYC Open Data endpoint that produced headline finding 3, it needs no permission, no funding, no equipment and no relationship, and it directly tests the strongest new claim in the repository. If elevated-adjacent census tracts show no complaint elevation citywide, the taxonomy-blindness finding holds. If they show elevation in some proxy category, residents are routing around the missing category and **the workaround is itself the signal** — which is arguably the more useful outcome.

It is the only method here that could be completed in an afternoon by anyone reading this, and it is the first thing in this programme that a resident could act on directly.

## Status

**`IDEA-CONCEPT.md` — draft v1.2.** Revised after an adversarial review pass. v1.2 adds §1.7, a derivation of train-event duration from the MTA's published session statistics — the only result in the repository that is calculated here rather than retrieved.
**`PRECEDENT-AND-MATERIALS.md` — draft v1.1.** Revised after an adversarial review that found three material errors in v1.0 and returned a verdict of *not fit to publish*; all are corrected and left visible.
**`WILLIAMSBURG-COMPARATOR.md` — draft v1.1.** Revised after an adversarial review that returned *not fit to publish* with eight blocking issues; all corrected and left visible, with a ten-row table of withdrawn claims. Adopts the "locus" discipline: every quantitative or dispositive claim quotes the exact passage it rests on.
**`VISUAL-MODEL-FRAMEWORK.md` — draft v1.1.** Revised after an adversarial review that returned *not fit to publish* with six blocking issues; twelve claims withdrawn, and the reference implementation reworked after the review found it violating the schema defined in the document it accompanies. Extends the locus discipline from citations to model geometry.
**`FIELD-CAPTURE-PROTOCOL.md` — draft v1.0.** Not yet red-teamed. Most of its hardware and application detail is rated `SNIPPET` rather than `VERIFIED`, because no Galaxy S23+ was tested in writing it; Part 4.6 specifies a bench test that settles those claims on the actual handset, and states that where the handset disagrees with the document, the handset is right.
**`COMMUNITY-EVIDENCE-AUDIT.md` — draft v1.1.** Not yet red-teamed. Two claims are rated 5/5 `VERIFIED` on queries this programme ran directly against the NYC Open Data API, printed in full so they can be re-run. **The legal mechanism joining them is rated 2/5 `UNVERIFIED` and written as a question, not a finding** — and Part 8 names that joint as the place to attack the document first, because the finding is elegant and arrived unexpectedly, which is exactly the condition under which this programme has previously over-claimed. v1.1 adds §3.5, the first direct field observation by the author, rated 2/5 and bounded explicitly on health: **annoyance may be claimed; depression and anxiety may not.**

**`pedestrian-site-visits/README.md` — draft v1.1.** Not yet red-teamed, and **already carrying one withdrawal of its own.** v1.0 used an audio duty cycle to refute a reading of the stopwatch; v1.1 withdraws that in place, because the two are independent samples 62.4 minutes apart with zero overlap — which the operator stated and the file timestamps independently confirm. **The error was not arithmetic.** Every number was computed correctly; what was wrong was joining two datasets that were never joined in the field, and no check in the repository can catch that. The document's centre of gravity moves to what the session was actually for: **the first photographic record of the echo chamber this repository had until then only modelled from surveyed footprints.**

**Interactive artifacts — nine, all self-contained and dependency-free, plus two site pages that index them.** [`index.html`](index.html) (the opening page and executive summary) and [`research.html`](research.html) (the research index), [`section-problem.html`](visual-review/section-problem.html) (2D provenance-tagged section), [`model-3d.html`](visual-review/model-3d.html) (navigable four-tier 3D model of both bridges), [`acoustic-demo.html`](visual-review/acoustic-demo.html) (audible level demonstration with derived event durations), [`frequency-dashboard.html`](visual-review/frequency-dashboard.html) (traversal frequency, direction, overlap, pedestrian presence and cohort dwell), [`agent-model.html`](visual-review/agent-model.html) (agentic population model with dose accumulated along a path), [`noise-canyon.html`](visual-review/noise-canyon.html) (the corridor drawn from open building and street geometry), [`media.html`](pedestrian-site-visits/media.html) (the first captured field material, analysed without levels), [`usage-dashboard.html`](usage/usage-dashboard.html) (what producing all of the above consumed), [`procurement-dashboard.html`](procurement/procurement-dashboard.html) (what the same deliverable would have cost to buy). The 3D model contains **zero measured elements**; the audio demo is **synthesised, not recorded**; the dashboard **carries three of this programme's own withdrawn claims on its face**, including one the dashboard's own charts disproved after it was published; the agent model **carries a propagation model it built and then rejected**; the canyon page **draws the bridge itself as an assumed band rated 1/5** because no public source gives its elevation; the field media page **quotes its own strongest claim from the day before and withdraws it**; the usage dashboard **opens by withdrawing its own first conclusion** and reports **no measured energy at all**; the procurement dashboard **opens by withdrawing the headline it exists to make**, and its central number is rated **1/5 invented**. All say so in their own interfaces.

**[`data-collection/`](data-collection/README.md) — six scripts, all verified running against live public feeds.** The schedule figures they produce are 5/5 `VERIFIED` — read directly from MTA's own published feed and reproducible from scratch by anyone. **The pedestrian figures are mixed**: entries are 5/5 observed, arrivals are 4/5 inferred, walkway counts are 4/5 observed but **six years stale**, and resident population is 5/5 on homes and 2/5 on people. **The cohort figures are lower still and say so**: total non-resident presence is reported as a range, and the worker/visitor split is reported as not identifiable. **The corridor geometry is 5/5 on buildings and 1/5 on the bridge**, which is the finding rather than a caveat. The interpretive findings in that directory's README are rated lower and marked as such.

None is peer-reviewed. Novelty claims are provisional; measured facts are solid. **Each document's own red-team Part is the best guide to how much to trust it** — `IDEA-CONCEPT.md` Part 13, `PRECEDENT-AND-MATERIALS.md` Part 11, `WILLIAMSBURG-COMPARATOR.md` Part 9, `VISUAL-MODEL-FRAMEWORK.md` Part 11, `COMMUNITY-EVIDENCE-AUDIT.md` Part 7. The audio demo carries its own seven-item list of where it is likely to be wrong; the agent model carries a seventeen-item list; every slide of the noise-canyon page carries its own.

**No option in any document is recommended for procurement.** **No calibrated acoustic measurement has been taken and no survey has been made.** Of the forty-five methods specified across the seven documents, the data-collection work, the usage audit and the procurement comparison, **six have been executed and one partially** — Methods 29, 30, 32, 33, 37 and 38, and Method 27 — and the rest have not. See *[What has not been done](#what-has-not-been-done)*. **Everything here was a statement about documents until Method 38**, and there are now eight exceptions: the NYC Open Data queries in Document 6, the GTFS traversal figures in [`data-collection/`](data-collection/README.md), the pedestrian flow figures in the same directory, the building and street geometry behind [`noise-canyon.html`](visual-review/noise-canyon.html), one direct field observation in Document 6 §3.5, the per-request usage ledger in [`usage/`](usage/README.md), the federal rate and award data in [`procurement/`](procurement/README.md), and — **the only primary physical material in the repository** — the phone captures in [`pedestrian-site-visits/`](pedestrian-site-visits/README.md), which are admissible precisely because they are reported as ratios and times rather than as levels.

**And one thing this repository now declines to compute, deliberately.** The agent model can say who is standing in the noise and for how long, and it will not say what that does to them. A discomfort threshold is published in `dB HL` and the MTA's peaks are published in `dB(A)`; converting between them requires the third-octave spectrum of the actual sound, which does not exist for either bridge. **The refusal is worth more than the estimate would have been**, because it turns an open-ended plea for more evidence into one named missing measurement — capture C1 — and that is Method 43.

**The largest hole has moved twice, and it is now smaller and sharper each time.** It used to be that not one quantitative claim in this repository was about people. **That is no longer true** — arrival rate, departure rate, walkway flow and resident count are now derived from public data, and the exercise **disproved this repository's own claim** about which hour is worst. Then presence was `L = λW` with only λ measured; the cohort model attempted `W` and established that **the composition of the population is not recoverable from the data that exists**, however carefully it is fitted. **Dwell time still needs measuring, and now the reason is proved rather than asserted.** That is Method 28, and it remains the single blocking unknown for any design-build case.

**Everything added most recently is unreviewed, and three issues exist to attack it.** [#26](https://github.com/Ethical-Tech-CoLab/manhattan-bridge-noise-dumbo/issues/26) asks whether the cohort model's non-identifiability finding is a result or an artefact of an arbitrary 10% admissibility threshold. [#27](https://github.com/Ethical-Tech-CoLab/manhattan-bridge-noise-dumbo/issues/27) asks whether a model whose every input is invented belongs in a repository built on quoted loci. [#28](https://github.com/Ethical-Tech-CoLab/manhattan-bridge-noise-dumbo/issues/28) asks whether the propagation model was genuinely unfittable or merely digitised badly — **because a negative result asserted from four points is as vulnerable to over-claiming as a positive one**, and this programme's recorded failure mode is over-claiming.

**This repository is public.** Everything in it — including every withdrawn claim, every unexecuted method and every rating below 5/5 — is readable by the agencies it describes. That is deliberate.

## Contributing

This is a working research repository. Useful contributions, roughly in order of value:

- **Executing any of Methods 0–43** — several cost an email, a form, or an afternoon, and only six have been touched. **Method 21 costs a database query. Method 26 costs leaving a script running for a week. Method 31 — walking a transect outward from the bridge with a meter — costs one afternoon and would establish where the affected zone ends, which nobody has ever determined. Method 28 — measuring how long a person actually stays in the corridor — costs a few hours with a clicker and is now the single blocking unknown for any exposure figure, and Method 42 rides along with it at no extra cost. Method 34 costs one download of a free federal dataset and would break the degeneracy that makes the cohort labels unidentifiable.**
- Answering any of **Q1–Q64** with sourced evidence. **Q42 — whether elevated rapid transit is federally *preempted* from local noise regulation or merely *unregulated* — is the highest-value open question in the programme, and one competent lawyer could settle it in a day.**
- **Posting a recording.** If you have ever recorded a train crossing the Manhattan Bridge from Brooklyn Bridge Park, DUMBO or the Williamsburg Bridge walkway, that recording is more useful to this programme than anything in it. See [`FIELD-CAPTURE-PROTOCOL.md`](FIELD-CAPTURE-PROTOCOL.md) for what makes one usable — the bar is far lower than most people assume, because **spectral shape and event timing survive an uncalibrated phone.**
- **Falsifying** any "not found" claim — five have already failed across the first two documents, and the prior on others failing is not low
- **Reclassifying** any component's provenance state in [`visual-review/section-problem.html`](visual-review/section-problem.html) or [`visual-review/model-3d.html`](visual-review/model-3d.html). Anyone with structural knowledge of riveted lattice trusses will find components that are misclassified, and that is the point of publishing the classification
- **Correcting the acoustic synthesis in [`visual-review/acoustic-demo.html`](visual-review/acoustic-demo.html)** — particularly the assumed spectrum, which is the largest single fabrication in the repository. **A single published third-octave spectrum for either bridge would replace it with evidence.**
- **Challenging the derived event durations.** The energy balance on that page is arithmetic on four published MTA numbers, and it is either right or it is wrong. It has not been reviewed by anyone.
- **Challenging the cohort identifiability result.** [`build_cohort_model.py`](data-collection/build_cohort_model.py) claims that worker and visitor cohorts cannot be separated from an aggregate departure curve. If there is an identifying restriction that this programme has missed — a second observable, an exclusion restriction, anything — that would be a genuinely useful correction, because the negative result is currently doing real work in how the numbers are hedged.
- **Supplying an origin-destination or dwell observation for DUMBO pedestrians.** [`visual-review/agent-model.html`](visual-review/agent-model.html) is a mechanism with invented itineraries. One real survey would convert it from a demonstration into a model.
- Non-English literature (Japanese, Chinese, German elevated-transit retrofit precedent) — **narrowed** by `PRECEDENT-AND-MATERIALS.md`, which reached Japanese and Chinese institutions only through their English-language outputs, and therefore **not closed**
- Full texts for the `SNIPPET` sources, especially **Odebrant 1996** (the single most load-bearing source in the precedent survey is currently an abstract), **TCRP Report 23** and the **WHO Environmental Noise Guidelines**, which are load-bearing
- Legal research on § 1204-a implementation, NYC Noise Control Code preemption, SEQRA and nuisance doctrine — and, newly, on whether **any** instrument protects people in outdoor public space from transit noise


## License

Research content released under [CC BY 4.0](LICENSE). Cite as:

> *Silencing the Span: Defining the Manhattan Bridge Rail-Noise Problem in DUMBO for a Design-Build Intervention.* Ethical Tech CoLab, 2026.
