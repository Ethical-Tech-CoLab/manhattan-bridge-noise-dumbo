# The Bridge Next Door

## A Two-Site Comparative Survey of Received Rail Noise in the Public Outdoor Space Beneath the Williamsburg and Manhattan Bridges

**Ethical Tech CoLab — Research Programme, Document 3**
Draft v1.1 · August 2026 · revised after adversarial review

---

## 0. About this document

### 0.1 Relationship to the companion documents

This is the third document in a series.

| Document | Asks |
|---|---|
| `IDEA-CONCEPT.md` | What is the problem in DUMBO, who is responsible, and what has never been asked? |
| `PRECEDENT-AND-MATERIALS.md` | What has the world already built, and what transfers to a suspension bridge? |
| **`WILLIAMSBURG-COMPARATOR.md`** | **There is a second bridge with the same owner, the same operator, the same division of rolling stock and the same statute. What does it already tell us, and what would measuring it establish?** |

`PRECEDENT-AND-MATERIALS.md` §8.3 recorded a gap it could not close:

> No quantified acoustic result from any rail-carrying suspension bridge was located anywhere in this survey.

It then named the obvious place to look and admitted it had not looked:

> If any comparator exists, it is that one — and this survey did not look.

This document looks.

### 0.2 Method

Same method as the companions, and the same rubric.

**Source credibility, 1–5.** 5 = peer-reviewed or primary agency/statutory document. 4 = technical report from a research institution. 3 = conference paper, trade technical press, agency secondary. 2 = advocacy, vendor, or enthusiast-technical. 1 = tertiary encyclopaedia, news aggregation, social media.

**One declared exception.** Haight & Patel (2005) is a conference paper, which the rubric places at 3. It is rated **5/5** here because its second author is the Director of East River Bridges at NYCDOT — the owner of both structures — writing about work he directed, which makes it a primary account by the responsible agency rather than third-party commentary. The exception is declared rather than applied silently, and a reader who disagrees should read every claim sourced to it at 3/5.

**Verification state.** `VERIFIED` = the source was opened and the passage supporting the claim was read. `SNIPPET` = only an abstract, search result or quoted excerpt was seen. `UNVERIFIED` = the citation is recorded but nothing was read.

**Locus.** New in this document, and adopted from the methodological finding filed as issue #11 against the previous two. Every quantitative or dispositive claim below states **which passage of the source it comes from**, and quotes it. The finding that prompted this: *all five errors found across the first two documents had a single cause — a source summarised from its abstract rather than read to its conclusions.* A verification state that records retrieval but not depth of reading did not catch any of them. Quoting the locus is the cheap control.

**A note on what this document is not.** It is not a measurement report. **No measurements were taken.** It is a design for a study, plus an inventory of what already exists. Every number below came from somebody else's instrument, and the central argument is precisely that the measurement that would settle the question has not been made by anyone.

### 0.3 Notation

Acoustic quantities are written in code style to keep them out of the prose and out of the markdown:

- `Leq` — equivalent continuous sound level, energy average over a stated period.
- `Leq(1)` — the above over one hour.
- `L10(1)`, `L50`, `L90` — levels exceeded 10%, 50%, 90% of the time in one hour. `L90` approximates the residual background. `L10(1)` is the CEQR metric.
- `Lmax` — maximum level during an event.
- `SEL` — sound exposure level: the total acoustic energy of a single event, normalised to one second. **The critical metric in this document**, for reasons given in §5.3.
- `dB(A)` — A-weighted. `dB(lin)` — unweighted. These are not interchangeable and the difference is enormous at low frequency: A-weighting discards **50.4 dB at 20 Hz** and **30.2 dB at 50 Hz**.
- `TL`, `IL` — transmission loss, insertion loss.

Structural and institutional abbreviations: **NYCDOT** (owns both bridges), **NYCT** (MTA New York City Transit, operates the trains), **C&D** (MTA Construction & Development), **CEQR** (City Environmental Quality Review), **PAL § 1204-a** (N.Y. Public Authorities Law § 1204-a, the Rapid Transit Noise Code), **HAER** (Historic American Engineering Record), **MHW** (mean high water).

---

## Part 1 — Why this bridge, and why this is not merely "another case study"

### 1.1 The problem with a single site

Everything established in `IDEA-CONCEPT.md` describes one bridge. That is a fundamental methodological weakness and it has a specific consequence: **for every causal claim about why DUMBO is loud, there is no counterfactual.**

The document asserts, with reasonable evidence, that the Manhattan Bridge is loud because it is an open-deck, unballasted, direct-fastened steel structure with jointed rail, described by an environmental impact statement as an "efficient radiator," discharging into a hard-surfaced street canyon. Every one of those is plausible. **None is isolated.** They co-occur. With one site and one set of measurements there is no way to attribute the received level among them, and `PRECEDENT-AND-MATERIALS.md` Part 2 had to downgrade an entire "bridge penalty" argument from a quantified class to qualitative risk factors for exactly this reason.

A second site does not fix this by itself. A second site that holds most variables constant and moves one does.

### 1.2 What the Williamsburg Bridge holds constant

This is the point. The comparison is unusually clean, and the reason is institutional rather than scientific: both bridges happen to be owned, operated, maintained, regulated and litigated by the same entities.

| Variable | Manhattan Bridge | Williamsburg Bridge | Held? |
|---|---|---|---|
| Bridge owner | NYCDOT | NYCDOT | **Yes** |
| Rail operator | MTA NYCT | MTA NYCT | **Yes** |
| Rolling stock division | B Division | B Division | **Yes — but see below** |
| Maintenance regime | NYCT Maintenance of Way | NYCT Maintenance of Way | **Yes** |
| Governing noise statute | PAL § 1204-a | PAL § 1204-a | **Yes** |
| Municipal noise code | NYC Noise Control Code | NYC Noise Control Code | **Yes** |
| Environmental review regime | CEQR | CEQR | **Yes** |
| Structure type | Suspension | Suspension | **Yes** |
| Crossing | East River | East River | **Yes** |
| Era | Opened 1909 | Opened 1903 | Near |
| Major reconstruction | c. 1982–2004 | c. 1990–2006, ongoing | Near |
| Deck type at track | Open, unballasted steel | Open, unballasted steel | Near — **to be verified** |
| Regional climate | Identical | Identical | **Yes** |
| Receptor land use | Dense residential waterfront + signature park | Dense residential waterfront + signature park | **Yes** |
| **Track position** | **Outboard, cantilevered, 2 per side** | **Central, between two roadways** | **NO** |
| **Track count** | **4** | **2** | **NO** |
| Car class and consist length | Unknown | Unknown | **UNKNOWN — not held** |
| Speed over structure | Unknown | Unknown | **UNKNOWN — not held** |
| Service frequency | Unknown | Unknown | **UNKNOWN — not held** |
| Rail and wheel condition, joint inventory | Partially documented | Undocumented | **UNKNOWN — not held** |
| Structural mobility and damping | Undocumented | Undocumented | **UNKNOWN — not held** |
| Approach geometry, curvature | Undocumented | Documented profile kink at towers | **NO** |
| Receptor distance, height, local propagation field | Open waterfront and street canyon | Open waterfront and street canyon | **Similar in kind, not matched** |
| Road traffic on the structure | Present | Present, 8 lanes | **NO — not matched** |
| Services | B, D, N, Q | J, M, Z | No |

**What this table is, and what it is not.** It is the strongest institutional and regulatory control available between any two rail structures anywhere in the surveyed literature. It is **not** a controlled experiment, and the two blocks of rows below the double line are the reason.

The nine "not held" and "unknown" rows are not confounds that careful design removes. They are **inseparable from bridge identity**. Fleet assignment, speed, consist length, rail condition, joint count, structural mobility, road traffic and receptor geometry all change together with the bridge, and no amount of `SEL` normalisation constructs the counterfactual in which the Williamsburg Bridge has outboard tracks.

**Therefore: this document proposes a two-site comparative survey, not a matched-pair natural experiment.** A between-bridge difference cannot be attributed to track position. What the survey can do is (a) establish the magnitude and character of received rail noise in a second piece of public outdoor space under the same operator and statute, (b) test whether the DUMBO levels are exceptional or typical, and (c) determine whether a difference exists that is *large enough to be worth explaining* — which is the precondition for, not a substitute for, an identification study.

**This framing is a correction.** Draft v1.0 of this document called the design a matched pair and described the bottom rows as "the experiment." An adversarial review identified that as the document's central error, and it is left visible here rather than quietly rewritten. The original sentence read: *"The three rows at the bottom are the experiment. Everything above them is the control."* It was wrong, and it was wrong in the direction that flatters the study.

### 1.3 The variable of interest, and why it is worth surveying

**Track position is the most consequential geometric difference between these two bridges, and it is the exact variable on which the worldwide literature is silent.**

On the Manhattan Bridge the four subway tracks are the **outermost elements of the structure**. They are carried on cantilevered framing outboard of the trusses, they overhang toward the neighbourhoods on both sides, and their loading is eccentric — which is the documented origin of the bridge's twenty-two-year torsional pathology.

On the Williamsburg Bridge the two subway tracks are in the **dead centre**, flanked on both sides by four-lane roadways which were reconstructed with **closed-rib orthotropic steel deck**, and outboard of those by the stiffening truss, and outboard of that by the footwalks.

Stated as a hypothesis rather than a fact: **the Williamsburg Bridge's flanking roadway decks may interrupt part of the path from rail source to receptor, where the Manhattan Bridge's outboard tracks have nothing between them and the neighbourhood.**

Three qualifications have to travel with that sentence and did not in draft v1.0.

**First, the geometry is unverified.** Whether a horizontal deck at approximately rail elevation stands in any sightline to a receptor below depends on relative *vertical* positions that no located source states. `VISUAL-MODEL-FRAMEWORK.md` §3.2 exists to resolve exactly this, and until it does, the hypothesis is geometric speculation.

**Second, a deck is not a barrier.** Barrier performance depends on wavelength, edge path difference, source height, receiver angle and source extent. At low frequencies diffraction around the deck edge will substantially defeat any shielding. At higher frequencies a deck may block direct wheel–rail radiation while itself becoming a structure-borne radiator, and the truss is open, so paths remain. A steel deck rigidly connected to the same floor system that carries the track is as plausibly a *radiator* as a shield.

**Third, and decisively, a difference would not identify the mechanism.** Fleet spectrum, rail roughness, joint condition, speed and structural mobility can all produce a Williamsburg advantage of any size and any spectral shape. The survey cannot separate them.

If the flanking decks are doing acoustic work, the Williamsburg Bridge is a **full-scale, in-service, century-old instance of an incidental shielding geometry** of the kind `PRECEDENT-AND-MATERIALS.md` §3.5 and §3.6 could only discuss from foreign viaduct literature — worth characterising even though the survey cannot prove causation.

And if it is *not* — if South Williamsburg is just as loud at matched distance — the conclusion is narrower than draft v1.0 claimed. **A null result would say only that this particular incidental geometry, an uninstrumented 1903 arrangement of vibrating steel decks at unknown elevations, is not delivering measurable benefit.** It would say nothing about a purpose-designed barrier, screen or enclosure, which is a different object with different edge geometry, different mass, different damping and different placement. Draft v1.0 wrote that a null result would mean "the option class should be de-prioritised." That inference does not follow and is withdrawn.

**Either result changes what should be built. That is the test of a worthwhile experiment.**

### 1.4 The honest limits of the pairing

Three differences are not controlled and must be handled analytically rather than pretended away.

1. **Service frequency and consist differ.** J/M/Z headways and train lengths are not B/D/N/Q headways and train lengths. This **fatally contaminates any comparison of `Leq` or `L10(1)`** between the two sites, because those metrics integrate over time and therefore reward or punish a site for how many trains run. §5.3 addresses this and it is the single most important methodological point in the document.

2. **Track count differs, 4 versus 2.** More tracks means more source, but also a wider structure and different modal behaviour. Track count and track position are **partially confounded** in this pairing and cannot be fully separated by two sites alone.

3. **Receptor geometry differs.** DUMBO's receptors sit in a street canyon close to and below the Brooklyn approach. South Williamsburg's sit across an open waterfront. This is not a nuisance variable to be eliminated — it is itself one of the things worth measuring — but it means "which neighbourhood is louder" is the **wrong question**. The right question is posed in §5.2.

---

## Part 2 — What the two bridges actually are

### 2.1 An asymmetry worth stating up front

**The comparator is better documented than the subject.**

`IDEA-CONCEPT.md` §13 concedes that its structural description of the Manhattan Bridge rests on a **tertiary source rated 1/5** — a well-referenced encyclopaedia article whose own primaries were never opened. For the Williamsburg Bridge, this document located a conference paper **co-authored by the Director of East River Bridges at NYCDOT**, which is a 5/5 primary-agency source, `VERIFIED`, read in full.

That is an uncomfortable position: the study now knows more about the bridge it is using as a control than about the bridge it is trying to fix. It is also an argument for doing this work, because the Williamsburg paper demonstrates that documentation at this quality **exists for East River bridges** and therefore probably exists for the Manhattan Bridge too, in a form that has simply not been retrieved.

### 2.2 The Williamsburg Bridge, from the primary source

> **Source.** Haight, R. and Patel, J., *Reconstruction of the Williamsburg Bridge.* Roger Haight, P.E., Project Manager, Parsons Corporation; **Jay Patel, P.E., Director of East River Bridges, New York City Department of Transportation.** Published by AISC (World Steel Bridge Symposium, 2005). **Rubric 5/5. `VERIFIED` — full text read.**

**Locus — overall geometry.** Verbatim:

> "The main suspended span is 1,600 feet long, with side spans each 596.5 feet... The anchorages are each 114.25 feet long. The Manhattan Approach viaduct is the longer of the two approach viaducts at 2,090.25 feet; the Brooklyn Approach viaduct is approximately 1,557 feet long. Four cables suspend the stiffening truss approximately 135 feet above mean high water level in the East River. **The stiffening truss is 67 feet wide and approximately 40 feet deep and is pinned at each main tower.**"

**Locus — the track position claim, which is load-bearing for this entire document.** Verbatim:

> "**The central section of the bridge, which contains two subway lines**, underwent a track/signal and structural support steel rehabilitation as well."

and

> "**Two subway tracks cross the Williamsburg Bridge** from the first subterranean station in Manhattan to the first elevated station in Brooklyn."

and, from the figure annotation of the main span section drawing, listing elements across the section:

> "NORTH FOOTWALK · CL.TRK J1 · CL.TRK J2 · NEW STIFFENERS (TYP) · **NEW BMT TRACKS** · SOUTH PEDESTRIAN WALKWAY · **NEW TRACK STRINGER COLUMN AND BRACING** · REPAIR FLOORBEAM, TRUSS BOTTOM CHORD, LATERAL BRACING (TYP)"

Two tracks, centre section, carried on **track stringers** on **stringer columns and bracing** — not on ballast. Centreline designations J1 and J2.

**Locus — the flanking roadways.** Verbatim:

> "The North and South Roadways each consist of four lanes... The existing roadways were constructed of open steel grid deck and concrete-filled grid deck at various locations... replaced with a **closed rib orthotropic deck system**."

This matters acoustically in two opposite directions and the document should not pretend otherwise. A closed-rib orthotropic deck is a **large, stiff, continuous steel plate**, and orthotropic decks are themselves known radiators of traffic-induced noise. So the flanking structure is simultaneously a **potential shield** for rail noise and a **potential source** of road noise. Disentangling them is a measurement problem, addressed in §6.4.

**Locus — the track geometry defect and the speed restriction.** Verbatim:

> "the dead load on the main suspended span has increased since the bridge was first built, and the profile has flattened, causing a **slight kink in the subway track profile at each main tower**... **Subway trains were required to reduce speed when riding over these profile kinks.**"

and the remedy:

> "Ten passes, for a total of **1,116 adjustments**, were required to raise the profile 21 inches at midspan."

**Locus — an NYCT track geometry tolerance, quotable and rare.** Verbatim:

> "NYCT specifies that the **maximum curvature in a 31-foot chord (the centerline-to-centerline distance of the wheel trucks) is +/-1/4 inch**."

This is a hard number from the operator on allowable track geometry deviation. `IDEA-CONCEPT.md` Q2 asks for the joint and fixation inventory; this is the adjacent tolerance against which any such inventory would be judged, and it was not previously in the corpus.

**Locus — and the finding with the largest practical consequence in this section.** Verbatim:

> "**Two traveling maintenance platforms were installed for inspection and maintenance of the main span. The traveling maintenance platforms are approximately 119 feet wide and 17 feet long**, in order to inspect one complete panel point without needing to move the platform."

`PRECEDENT-AND-MATERIALS.md` Part 7 concluded that **access, not acoustics, is the scarce resource**, and Part 10 Method 10 asks for an access and approval matrix because no option is approval-free. The sister bridge, owned by the same agency, **already has a permanent, powered, 119-foot-wide traveling under-deck platform system running on installed rails.** Whatever the acoustic result turns out to be, this is a directly relevant precedent for how you get people, sensors or equipment under an East River suspension bridge on a routine basis — and it is NYCDOT's own.

Other verified figures: four main cables of **7,696 wires each**; **815,000 lb** of steel plating added to strengthen the main towers; rocker arms replaced with **2,500 kip** pot/sliding bearings designed for **±16 inches** of longitudinal movement; anchorage bearings **1,200 kip**; over **7,000,000 lb** of steel replaced or added; total reconstruction cost **approximately $900 million**.

### 2.3 The Manhattan Bridge, and one very important recent finding

The structural description remains as recorded in `IDEA-CONCEPT.md` §4.1 at rubric 1/5 and is not restated here. But this review located a source that document did not have, and it is significant enough to change priorities.

> **Source.** Rutgers Center for Advanced Infrastructure and Transportation (CAIT), *CAIT Research Helps NYC Engineers Monitor Structural Health of Manhattan Bridge*, 3 June 2021. Research leads **Dr. Franklin Moon** and **Dr. Sougata Roy**, Rutgers Dept. of Civil and Environmental Engineering; project funded through a National University Transportation Center grant; **conducted with NYCDOT**. **Rubric 3/5** — institutional research communication, not the underlying paper. **`VERIFIED` — full page read.** The underlying technical report was **not** retrieved and is retrieval priority 1 (§10.2).

This matters for four reasons.

**First, it partially answers Q2 — and Q2 was rated blocking.** `IDEA-CONCEPT.md` §4.2 could establish only that a systemwide MTA policy statement made continuous welded rail *unlikely* on elevated structures, and stated plainly that the bridge's actual joint inventory was undocumented in any located source. CAIT went and measured it. Verbatim:

> "the team performed limited vibration tests at the Manhattan Approach, **on each of the transit beams that support a set of rails**. The goal of this study was to characterize the response of the bridge due to the **misalignment of bolted rail joints**, which introduced strong vibration as trains crossed them."

**Bolted rail joints exist on the Manhattan Bridge and they are misaligned.** That is no longer an inference from policy.

**Second, a severity classification and a magnitude already exist.** Verbatim:

> "the researchers examined the bridge response using **magnetically mounted accelerometers**. The accelerometers were roved around to identify different levels of vibration associated with various bolted rail joints. Based on these results, they developed a criteria and organized the various rail joints into **fair, poor, and severe**... the more severely misaligned splices resulted in more vibration on the bridge, **almost double that of the fair splices**. This was further corroborated by the long-term stress measurements."

A factor of approximately two in structural vibration response between a *fair* joint and a *severe* one, on this bridge, measured. **This is an association between joint-condition class and structural response — not a demonstrated treatment effect.** CAIT ran no before-and-after maintenance trial, isolated no causal path, and reported no acoustic outcome. What it establishes is that the variation exists and is large, which is the precondition for asking whether treating it would help, not an answer to that question. It is also, notably, **the same thing the DUMBO residents' original 2022 suggestion was about**, which the MTA declined as infeasible (`IDEA-CONCEPT.md` §5.5).

The claim must be bounded honestly, and draft v1.0 did not bound it enough. This is **structural vibration on transit beams**, not radiated sound at a receptor, and the two are related by a radiation efficiency that nobody has measured. A 2:1 vibration ratio does not entail 6 dB at the Archway; it need not entail any change at the Archway. Draft v1.0 called this "the strongest quantitative evidence yet located that a purely maintenance-based intervention has meaningful headroom." **That is withdrawn.** The correct statement is that it is the strongest quantitative evidence yet located that **joint condition on this bridge varies enough to be worth testing acoustically** — which makes Method 12 and Q25 more valuable, and makes no claim about efficacy.

**Third, it describes a self-accelerating degradation loop.** Dr. Roy, verbatim:

> "Rails at joints always get hammered by crossing wheels and experience more wear. The rail wear increases hammering. Repeated hammering loosens the bolted rail joints, increases stress fluctuations in the bolts, and the bolts fail in fatigue. With lost bolts the rails go more out of alignment — increasing vibration."

If correct, **the structural response from this mechanism degrades progressively between maintenance interventions.** Draft v1.0 wrote that "noise from this mechanism gets worse monotonically," which the quoted passage does not support — it describes a structural wear loop, not a monotonic receptor-noise trajectory, and receptor noise depends on radiation efficiency, other sources and propagation as well. What can be said is that residents' reports of worsening conditions, recorded in `IDEA-CONCEPT.md` Part 2 and generally treated as subjective, have **a documented physical mechanism that is consistent with them.**

**Fourth, and most disruptive to the existing programme: the problem may not be on the span at all.** Dr. Moon, verbatim:

> "Often times when people think about signature bridges they focus mainly on the signature spans. It turns out that **many of the problems these days are actually on the approach spans**."

CAIT's tests were performed **at the Manhattan Approach**. The Manhattan Bridge's Brooklyn approach viaduct is the structure that runs directly over and alongside DUMBO. `IDEA-CONCEPT.md` and `PRECEDENT-AND-MATERIALS.md` have both been organised implicitly around the suspended span.

**If the receptor-relevant noise in DUMBO is dominated by the approach viaduct rather than the suspended span, then `PRECEDENT-AND-MATERIALS.md` issue #9 — the suspension-bridge literature gap — is substantially less damaging than it appeared**, because an approach viaduct is a conventional steel elevated structure of exactly the type the worldwide literature does cover. This would be good news, and it is testable. It is posed as Q23.

And a scale figure, verbatim: the bridge "carries approximately **1,000 trains** and hundreds of thousands of passengers daily."

---

## Part 3 — What data already exists for the Williamsburg Bridge

This part answers the question as asked: *what is available by doing deep research?* The short answer is **more than expected, none of it fit for purpose, and the gaps are informative.**

### 3.1 Measured sound levels on the bridge — the Domino Sugar FEIS

This is the most substantial existing dataset located.

> **Source.** *Domino Sugar Rezoning Final Environmental Impact Statement, Chapter 20: Noise.* New York City Department of City Planning / applicant, 2010. Field measurements by **AKRF, Inc.**, October 2007 and February–March 2010. **Rubric 5/5** — primary CEQR document. **`VERIFIED` — chapter read in full.**

**Locus — instrumentation, quoted so that a replication can match it:**

> "a Brüel & Kjær Type 4189 ½-inch microphone connected to a Brüel & Kjær Model 2260 Type 1 (according to ANSI Standard S1.4-1983) sound level meter. This assembly was mounted at a height of **5 feet above the ground surface** on a tripod and at least 6 feet away from any large sound-reflecting surface... Measured quantities included Leq, L1, L10, L50, and L90... All measurement procedures conformed to the requirements of ANSI Standard S1.13-1971 (R2005)."

**Locus — the measurement on the bridge itself. Table 20-7, Site 10:**

| Site | Location | Period | `Leq` | `L1` | `L10` | `L50` | `L90` |
|---|---|---|---|---|---|---|---|
| 10 | **Pedestrian walkway of Williamsburg Bridge** | Weekday PM | **82.5** | **92.3** | **86.5** | **78.6** | **75.7** |

All values dB(A). For orientation, `IDEA-CONCEPT.md` §1.2 records MTA measurements near the Manhattan Bridge Brooklyn anchorage in the **81–87 dB(A) `Leq`** range with maxima near 98 dB.

**The `L90` of 75.7 dB(A) is the most striking number in the table.** It says that on the Williamsburg Bridge walkway, the level exceeded ninety percent of the time is itself approaching the level at which the CEQR machinery starts imposing 30+ dB of façade attenuation on new housing. There is effectively no quiet interval. Note that at a position on a bridge carrying eight lanes of road traffic, `L90` is simply the lower-percentile ambient — it should **not** be read as a train-free or road-free background, and the report gives no basis for decomposing it.

**Locus — the derived level at bridge height, and the assumptions inside it:**

> "the L10(1) was determined at the location on the project site closest to the bridge, which would be the southern façade of Site D at a height level with the bridge. This L10(1) was determined in two ways: (1) projecting the value measured at Site 11 south and up to Site D, and (2) projecting the value measured at Site 10 north to Site D. In both cases **it was assumed that the measured levels were dominated by noise generated by the Williamsburg Bridge and a 3 dBA drop-off per doubling of distance from the bridge**. These methods yielded L10(1) values of **74.6 and 73.5**, respectively."

Two independent projections agreeing within 1.1 dB is reassuring about internal consistency and says nothing about accuracy, since both used the same assumed propagation law. A 3 dB per doubling law is a **line-source** assumption. It is defensible for a long train on a long bridge and it is an assumption, not a measurement.

**Locus — and here is the disqualifying limitation, stated by the authors themselves:**

> "**Traffic was the dominant noise source at all eleven sites**, and the values shown reflect the level of vehicular activity on the adjacent streets."

and, on the purpose of the two bridge-related sites:

> "in order to determine the maximum noise that would result from **automobile and subway traffic** on the Williamsburg Bridge... Sites 10 and 11 were used **solely for the purpose of determining the building attenuation required** by reason of their proximity to the Williamsburg Bridge, and are therefore **not presented in the No Action and future with the proposed project scenarios**."

**The subway is never separated from the road traffic.** Site 10 is on the bridge walkway, metres from four lanes of moving vehicles, measuring both. The number is a combined level.

This is precisely the same defect that `IDEA-CONCEPT.md` Q1 identifies in the DUMBO evidence base, arrived at independently on a different bridge by a different consultant fifteen years earlier. **Neither of New York's two rail-carrying suspension bridges has a published measurement that isolates the rail contribution.** That is a striking gap, it is now documented on both bridges, and it is the reason §6 is built around event-synchronous measurement.

### 3.2 The MTA's own statutory noise report

> **Source.** *New York City Transit Noise Reduction Report*, MTA, prepared pursuant to the Rapid Transit Noise Code and **Public Authorities Law § 1204-a**. Covering 2023 with 2024 projections. **Rubric 5/5** — primary agency document filed under statutory duty. **`VERIFIED` — full text read.**

This is the report the statute compels. Its own abstract states the duty, verbatim:

> "**Any and all subway noise measurements made during the previous period shall be included**, with, whenever possible, analyses of such measurements."

**Finding: the Williamsburg Bridge appears zero times.**

A term-frequency count of the full report text: `Williamsburg` — **0**. `Manhattan Bridge` — **8**. `DUMBO` — **6**.

The DUMBO matter is documented at length, including the entire internal referral chain, because a State Assembly Member wrote to the Chairman and CEO. The report also contains a complete measurement memorandum for a different site entirely, verbatim:

> "In response to noise complaints from residents at Brightwater Towers Condominium, on August 2, 2023, Environmental Services collected noise measurements of passing subway trains on the elevated structures for the F and Q lines... The average `LEQ` for the F trains on the Jamaica-179th street bound track... is **85.1 dB(A)**, with an average `LMAX` of **94.6 dB(A)**. The highest `LEQ` measured was **87.8 dB(A)** and the highest `LMAX` measured was **97.1 dB(A)**. The F train produces elevated peaks on the **400 Hz, 500 Hz, 2kHz, and 6.3kHz** bands during screeching... the background `LEQ` was measured at **56.3 dB(A)** for a three-and-a-half-minute lull between train arrivals."

Three things follow.

**One — this is spectral data from the operator on an open steel elevated structure**, and the named bands are consistent with the rail-damper target range that `PRECEDENT-AND-MATERIALS.md` §4.1 identifies as 400 Hz to 2 kHz. It is the only MTA spectral information located in three documents of research.

**Two — it demonstrates the measurement is trivial for them.** One field engineer, one afternoon, one location, a Type 1 meter. The barrier to measuring the Williamsburg Bridge is not cost, capability or access. In 2023 they responded to **14** noise and vibration complaints across Brooklyn and Queens.

**Three — the absence of Williamsburg is evidence about this report, and at most about complaint routing. It is not evidence about the noise.** The § 1204-a report is complaint-driven and escalation-driven. DUMBO appears in it because a resident wrote in, an Assembly Member escalated to the Chairman, and Government & Community Relations became involved. A zero term count in one reporting year cannot establish that no complaint or request about the Williamsburg Bridge was ever made — only that none surfaced in the reviewed report. Q28 turns the underlying issue into a research question, because how environmental attention gets allocated is a question with a literature.

**Also verified from this report**, because it bears on the companion documents:

- MTA's own abatement effectiveness figures: traction motor retrofit **5–7 dB(A)**; **"resilient rail fastener installation on steel elevated structures (3–5 dBA noise reduction)"**; ring damped wheels **15–20 dB(A)** on screech; rail welding **9–10 dB(A)**. The 3–5 figure is one side of the contradiction recorded at `IDEA-CONCEPT.md` §5.1.
- Flat wheels: "In some cases, the increase can be **as great as 10 dBA**."
- Programme spend: **$32,849,385.24 materials and $124,800,000.00 labour** in the reporting year; projected **$32,882,460.52 and $162,240,000.00**. A labour-to-materials ratio of **3.8:1 rising to 4.9:1**, which independently corroborates the 4–6× ratio recorded at `IDEA-CONCEPT.md` §9.3 from a different source.
- MTA organises noise into four categories: "1) in-car, 2) **elevated structures**, 3) curve and brake screech and 4) stations." **There is no bridge category.** A suspension bridge carrying four tracks is administratively an "elevated structure," the same as a conventional viaduct.

### 3.3 Community evidence

> **Source.** *Reduce Williamsburg Bridge Subway Noise for South Williamsburg & Domino Park*, Change.org petition, started by Shane Barratt, Williamsburg resident. Created **16 June 2026**; **16 signatures** at retrieval. **Rubric 2/5** — advocacy. **`VERIFIED`.**

Cited not as evidence of noise level but as evidence that **the same complaint exists at the second site**, which is a precondition for the comparison being socially as well as physically meaningful. Verbatim:

> "Excessive subway noise from trains crossing the Williamsburg Bridge is adversely affecting residents, families, workers, and visitors around Domino Square and the South Williamsburg waterfront. The J/M/Z trains pass over the bridge frequently, including early mornings, late nights, and peak commuting hours. For people living near the bridge, **using Domino Square Park, walking dogs, working from home, visiting local businesses, or spending time with children outdoors**, the repeated **screeching and rumbling** is disruptive and, at times, overwhelming."

The requested actions are worth recording because they were arrived at independently by a resident and they map closely onto the option classes the research programme reached by literature survey: track inspection and maintenance, **rail grinding or welding**, **lubrication on curves**, noise and vibration studies, **sound-dampening materials**, and "evaluation of modern noise-reduction technologies used on other elevated rail systems."

Named decision-makers: Antonio Reynoso (former Brooklyn Borough President), **Emily Gallagher (NY Assembly District 50)**, **Julia Salazar (NY Senate District 18)**, **Lincoln Restler (NYC Council District 33)**.

**A political observation with practical consequence.** The DUMBO matter escalated through **Assembly Member Jo Anne Simon, AD-52**. The Williamsburg matter names **AD-50**. But **Council Member Lincoln Restler, District 33, represents both** DUMBO and this stretch of Williamsburg waterfront. There is therefore **one elected official with a constituency interest in both bridges**, which is the natural sponsor for a two-site study and, as far as this review can determine, has not been approached as such.

The petition's scale — 16 signatures — should be read carefully. It is two months old at the time of writing. It is weak evidence of prevalence and strong evidence of existence.

### 3.4 What is explicitly not available

Recorded so that the next researcher does not repeat the search.

- **No noise measurement isolating subway from road traffic on either bridge**, from any source, at any date.
- **No Williamsburg Bridge entry in the MTA § 1204-a report** for the reviewed year.
- **No vibration or modal study of the Williamsburg Bridge** located. The CAIT work is Manhattan Bridge only.
- **No published sound measurement in Domino Park itself** — the FEIS measured the bridge walkway and surrounding streets before the park existed.
- **No spectral data of any kind for the Williamsburg Bridge.**
- **No `SEL` or event-based metric for either bridge, anywhere.** Every located measurement is `Leq`, `L10`, `L50`, `L90` or `Lmax`.
- The USDOT report **"Performance of Rail Fastening Systems on an Open-Deck Bridge"** (ROSA-P `dot/35570`, 1 Feb 2018) is directly on point for both bridges and **could not be retrieved** — the repository returned HTTP 403 on the PDF. **`SNIPPET`**, retrieval priority 2.

---

## Part 4 — The regulatory finding: outdoor space is orphaned

This part was not planned. It emerged from reading the Domino FEIS against the DUMBO material and it is, in this author's judgement, the most consequential non-acoustic finding in the document.

### 4.1 What the city actually did about Williamsburg Bridge noise

It required thicker windows. Verbatim, from the FEIS:

> "**With the resultant noise level from the Williamsburg Bridge of 74.6 being very close to the 75 dBA threshold, the south and west facades would require 31 dBA of attenuation rather than 30 dBA.**"

That is the whole of it. The determination that the bridge produces roughly 74.6 dB(A) `L10(1)` at the façade of a new residential building triggered a **building envelope specification**, enforced through a Restrictive Declaration on the developer, requiring **31 dB(A)** of composite window-and-wall attenuation to hold interiors at or below 45 dB(A).

Nothing was asked of the bridge. Nothing was asked of the operator. The noise source was treated, correctly under the rules as written, as an immutable environmental given — and the entire regulatory response was to require **a private party to buy better glazing**.

### 4.2 And for the park, nothing

Here is the gap. **CEQR's attenuation machinery only operates on building envelopes.** A park has no envelope. Domino Park, Domino Square, the Archway, the Brooklyn Bridge Park lawns and the DUMBO dog run cannot be issued a Restrictive Declaration requiring 31 dB(A) of window attenuation, because they have no windows.

For outdoor space the guidance offers a target and then, in the same breath, excuses itself from it:

> "While the 55 dBA L10(1) guideline is a worthwhile goal for outdoor areas requiring serenity and quiet, due to the level of activity present at most open space areas and parks throughout New York City (except for areas far away from traffic..."

> **Source.** NYC Parks, Chapter 13: Noise, FEIS for a Queens parks project (`12DPR005Q`). **Rubric 4/5.** **`SNIPPET`** — this passage was seen in a search result and **the document was not opened.** Flagged for retrieval; the sentence is truncated mid-clause and its completion materially affects how strong this finding is. **Do not cite this further until it is read.**

The structure of the outcome, however, does not depend on that one quotation, because it is visible directly in the Domino FEIS: **Site 10 and Site 11 were used "solely for the purpose of determining the building attenuation required"** and were explicitly excluded from the No Action and With Action analyses. The bridge's contribution was measured **only** to size windows.

**So: the loudest identified source in the study area was measured, quantified at 82.5 dB(A) `Leq` on the structure, projected to 74.6 dB(A) `L10(1)` at the new façades — and the sole regulatory consequence was one additional decibel of required glazing performance.**

The people in the park are outside the analysis. Literally.

### 4.3 Why this is the right frame for a design-build proposal

`IDEA-CONCEPT.md` Part 3 establishes that responsibility for the Manhattan Bridge is split between NYCDOT and NYCT with no party owning the received noise. This part adds a complementary observation on the receptor side, and it must be stated at the scope the evidence actually supports:

> **In the one environmental review examined here, the identified consequence of 82.5 dB(A) on the Williamsburg Bridge was façade attenuation on a private developer. No outdoor-source mitigation was identified, and the two bridge-side monitoring positions were excluded from the impact analysis by design.**

Draft v1.0 generalised this to "the environmental review system that governs everything built near these bridges has no mechanism to protect outdoor public space, and knows it." **That is withdrawn.** It rests on one project outcome plus a truncated search-result snippet from a parks FEIS that was never opened, and it is exactly the locus failure this document's method note claims to have eliminated. One project outcome establishes what happened in that project. It does not establish that no CEQR provision, parks policy, health regulation, nuisance doctrine or other instrument exists.

**Whether the generalisation is true is Q29, and Method 14 exists to answer it.** Until that review is done, the finding is a single documented instance, and it should be presented as one.

Even at that reduced scope it is useful, because the instance is directly on point: the receptor of concern is a park, the source is a subway on a suspension bridge, and the regulatory output was a window specification.

That is the gap a design-build project would plausibly be filling. Not a code violation — there is no violated code, which is exactly `IDEA-CONCEPT.md` Q11 and the § 1204-a Category IV blank.

And it is why the measurement proposed in Part 6 should be taken **in the parks, at ear height, where people actually sit** — not only at façades. Every existing measurement on both bridges was taken either on the structure or at a building line, because those are the places the rules care about.

---

## Part 5 — Designing the inference

### 5.1 What kind of study this is

A **two-site observational comparison**, not an experiment, because the difference of interest — track position — was fixed in 1903 and cannot be randomised, reversed or replicated.

Draft v1.0 called this "a natural experiment with a single treated and single control unit." **That framing is withdrawn.** A natural experiment requires that assignment be plausibly independent of the outcome and that everything else be comparable. Here everything else is *not* comparable: fleet, speed, consist, service frequency, rail and joint condition, structural mobility, damping, approach geometry, road traffic and receptor propagation field all change together with the bridge, and §1.2 now lists them. There is no counterfactual and no identification strategy.

What the survey can actually deliver, stated at the level the design supports:

1. **Magnitude.** What people in a second piece of public outdoor space, under the same operator and the same statute, are actually exposed to. Currently unknown; no measurement exists in Domino Park.
2. **Character.** Matched event spectra from two structures of the same class. This is where the diagnostic value lies, and it is descriptive value, not causal value.
3. **A screening result.** Whether a difference exists that is large enough to be worth explaining. If the two sites are within a couple of decibels at matched geometry, no expensive identification study is warranted. If they differ by 10 dB, one is.

It cannot deliver "outboard track position costs X dB," and any output phrased that way is a misuse of the data.

### 5.2 The right question

Not *"is DUMBO louder than South Williamsburg?"* That confounds source, path, distance, service and receptor geometry, and would produce a headline with no engineering content.

The question is:

> **At matched slant distance from the nearest rail, matched elevation relative to the track, and matched propagation path class, does a single train event on the Manhattan Bridge deliver more acoustic energy to a receptor than a single train event on the Williamsburg Bridge — and if so, in which frequency bands, and does that difference survive normalisation for car class, consist length, axle count and speed?**

The "in which bands" clause is the payload, and it is a **diagnostic** payload, not a proof. If the flanking decks shield, the difference should be selective rather than flat — a barrier of any geometry attenuates short wavelengths more effectively than long ones. A selective difference is therefore *consistent with* shielding and would justify the instrumented apportionment study that could test it. A spectrally flat difference would point away from a geometric path effect and toward a source-side difference such as fleet, rail condition or joint count. No difference would remove the motivation for either.

None of these outcomes identifies a mechanism, for the reason given in §1.2 and §5.1. Fleet spectra differ; rail roughness differs; structural mobility differs. The survey narrows the hypothesis space; it does not close it.

### 5.3 The metric: why `SEL` is necessary, and why it is not sufficient

**This is the most important methodological point in the document, and draft v1.0 overstated it.**

Every existing measurement located on both bridges — MTA's, AKRF's, the CEQR framework itself — reports `Leq`, `L10(1)`, `L50`, `L90` or `Lmax`.

`Leq` integrates energy over a period, so it rises when more trains run. The B/D/N/Q services over the Manhattan Bridge and the J/M/Z services over the Williamsburg Bridge do not run at the same frequency or the same consist length. **A difference in `Leq` between the two sites would be substantially a measure of the timetable.** That is a real limitation for the question asked here, and it is not a defect in the metric: `Leq` is the correct measure of *exposure*, which is what health guidance and most regulation are about.

`L10(1)` is a **percentile**, not a time-integrated energy quantity — draft v1.0 grouped it with `Leq` under "time-integrated," which is wrong. It is the level exceeded 10% of the hour, and it is the CEQR metric, so it must continue to be reported whatever else is measured.

`Lmax` avoids the timetable problem but discards nearly all the information in the event — it is one sample of one instant and is heavily influenced by a single flat wheel.

The metric this survey needs in addition is **`SEL`**, the sound exposure level of a single train passage: the total A-weighted, and separately unweighted third-octave, energy of the event normalised to one second. `SEL` characterises **the event**, independent of how often events occur.

**And here is the qualification draft v1.0 omitted entirely.** `SEL` does not isolate "the bridge." Event `SEL` depends on consist length, axle count, speed, traction or coasting state, wheel roughness, joint crossings within the measurement window, and the analyst's choice of event window. A longer train produces a higher `SEL` at identical per-axle emission. Raw `SEL` compared between two bridges running different services would substitute a fleet-and-consist confound for a timetable confound.

So the requirement is `SEL` **plus covariates recorded per event**: car class, consist length, axle count, direction, track, speed, and whether the pass-by was under power. Comparison is then made within matched strata, or `SEL` is modelled with those covariates as terms. Both are standard; neither is optional.

Draft v1.0 asserted that "the entire New York evidence base on these two bridges is expressed in units that cannot support a cross-site comparison." **That is withdrawn.** The correct statement is narrower:

> No located document on either bridge reports `SEL`, which is standard practice in rail noise assessment internationally. Without it, the existing `Leq` and `L10(1)` records cannot be used to compare per-event emission between the two sites — though they remain valid and legally operative measures of exposure, and must be reported alongside any `SEL` survey rather than replaced by it.

### 5.4 Matching, concretely

Receptor pairs must be matched on:

1. **Slant distance** from nearest running rail, ±10%.
2. **Vertical angle** to the track, since the outboard/central difference is expressed largely in elevation angle and shielding geometry.
3. **Path class** — direct line-of-sight, singly diffracted, or reflected. These must not be mixed within a pair.
4. **Ground and façade context** — hard urban surface versus open water frontage. Where this cannot be matched, it must be recorded and the pair analysed separately.
5. **Height above grade** — one pair at 1.5 m for outdoor public space, one at a residential façade height.

Pairs should be **replicated at three distances** on each bridge so that a propagation slope is measured rather than assumed. The Domino FEIS assumed 3 dB per doubling; nobody has checked it on either bridge.

### 5.5 What would falsify what

Stated in advance, per the method note in `IDEA-CONCEPT.md` §0.1 and the pre-declaration principle in `PRECEDENT-AND-MATERIALS.md` Method 7.

| Hypothesis | Consistent with | Inconsistent with |
|---|---|---|
| **H1** Central track position with flanking decks provides material shielding | `SEL` difference favours Williamsburg at matched geometry, with the difference growing at frequencies whose wavelength is small relative to the calculated edge path difference — a threshold that must be computed from the section once §3.2 of the visual framework establishes it, not assumed | Difference is null, or favours Manhattan Bridge, or is spectrally flat |
| **H2** The outboard cantilever radiates more low-frequency energy | Manhattan Bridge shows relatively more energy below ~125 Hz at matched geometry | Low-frequency content is comparable |
| **H3** Jointed-rail impact dominates the receptor-relevant signature | Event spectra show broadband impulsive structure correlating with joint crossings; `SEL` varies markedly between trains matched on class, consist and speed | Spectra are dominated by steady rolling and screech components |
| **H4** The receptor-relevant noise in DUMBO comes mainly from the approach viaduct, not the suspended span | Levels along the Brooklyn approach exceed those at matched distance from the suspended span | The suspended span dominates |
| **H5** Track/joint condition, not structure, drives the difference | Within-bridge variation across joint condition classes is comparable to between-bridge variation | Between-bridge variation dominates |

**A warning that applies to all five.** These are consistency tests, not identification tests. Per §1.2, every one of the confounds listed in the "not held" block of the control table could produce the pattern in the "consistent with" column without the hypothesis being true. Draft v1.0 headed these columns "Supported if" and "Falsified if"; that overstated what a two-site survey can do and the headings are corrected. H1 in particular cannot be established by this survey at all — only rendered plausible or implausible enough to justify the instrumented apportionment study that would actually test it.

The 250 Hz threshold that appeared in draft v1.0's H1 row was **not sourced from anything** and is withdrawn. Barrier performance is governed by the Fresnel number, which depends on wavelength and the path-difference geometry; with the section geometry unknown, no crossover frequency can be stated.

**H5 deserves emphasis because it is the cheap outcome.** If CAIT's fair-to-severe factor of two in structural response translates to a comparable spread in radiated `SEL`, then the *within*-bridge variation caused by maintenance state could be as large as anything track position explains — and the intervention would be a maintenance programme, not a construction project. That result would be inconvenient for a design-build proposal and would be the most valuable result the study could produce.

---

## Part 6 — The measurement protocol

Deliberately specified to be executable by a two-person team with commodity equipment, because §3.2 establishes that the MTA does this work in an afternoon and the barrier is therefore not technical.

### 6.1 Instrumentation

- **Two matched Type 1 sound level meters**, third-octave capable, 20 Hz to 10 kHz, synchronised clocks, simultaneous unweighted and A-weighted capture. Matching the Domino FEIS instrument class (B&K 2260 or modern equivalent) preserves comparability with the 2007–2010 baseline.
- **Continuous raw audio capture** alongside the meter, so that events can be re-analysed, mis-triggered events rejected, and third-octave `SEL` recomputed later. The absence of raw time histories is the specific defect that `IDEA-CONCEPT.md` §3.2 files a FOIL request over; do not reproduce it.
- **Triaxial accelerometers**, magnetically mounted, on the structure where accessible — the same technique CAIT used, chosen deliberately for comparability with their dataset.
- **Event log**: time, service, direction, track, consist length, and observed speed.
- **Weather**: wind speed, direction, temperature, humidity, per the ANSI conditions the FEIS records.

### 6.2 Locations

**Williamsburg Bridge, Brooklyn side.** Domino Park and Domino Square at ear height where people sit; the South Williamsburg waterfront at three slant distances; a residential façade on the south-facing frontage nearest the bridge — ideally the same Site D geometry the FEIS projected to, which converts a projection into a measurement.

**Williamsburg Bridge, Manhattan side.** The Lower East Side approach, which is a control for a different receptor geometry under the same structure.

**Manhattan Bridge, Brooklyn side.** The Archway, the dog run, the library forecourt and Front/Pine — the receptors already named in `IDEA-CONCEPT.md` — plus matched distances beneath and alongside the **Brooklyn approach viaduct** specifically, to test H4.

**Both bridges.** A walkway position replicating Domino FEIS Site 10, since that is the only existing point with a published historical value. Re-occupying it gives a **nineteen-year repeat observation** — not a change measurement. Instrument, road traffic volume and mix, fleet, rail condition, season, weather and time of day all differ, and none of the 2007 covariates were published. Any difference must be reported as an observation requiring comparability controls, not attributed to time.

**Controls.** At least one position per neighbourhood shielded from the bridge but otherwise comparable, to establish the residual background that `L90` only approximates.

### 6.3 Timing

Both bridges within the same week, ideally the same day using two teams, under comparable weather. Include a **late-night window**, because the petitions on both bridges emphasise early morning and late night, service frequency is lower, road traffic is much lower, and **rail noise is therefore best isolated from road noise in the small hours** without needing any modelling assumption.

### 6.4 Separating rail from road — the defect in every prior study

The Domino FEIS's own limitation, stated by its authors, was that "traffic was the dominant noise source at all eleven sites" and that the subway was never separated from it. Doing better is not difficult; it is simply never done. But draft v1.0 claimed more for this protocol than it can deliver, and the claim is corrected below.

1. **Event-gating with background subtraction.** Train passages are discrete, identifiable and loggable. Compute `SEL` over the event window, compute the energy in the inter-event intervals, and **subtract the background energy from the event window** rather than reporting the gated total. Without that subtraction the gated event still contains whatever road traffic was present during it. Road traffic is quasi-stationary; rail is transient; but "transient" does not mean "alone."
2. **Simultaneous road-vehicle logging** at each position, so that event windows contaminated by a heavy vehicle, a motorcycle or a siren can be excluded rather than averaged in. This is the item that actually does most of the work and it was missing from draft v1.0.
3. **Night measurement**, where road flow is minimal — a check on items 1 and 2, not a substitute for them.
4. **Speed and axle detection** per event, so that `SEL` can be normalised per §5.3.
5. **Near-source microphones**, positioned on the walkway close to the track, to characterise the emission independently of the receptor-side mixture.
6. **Spectral discrimination.** Road traffic and rail differ in spectral signature, and the MTA's own 400 Hz / 500 Hz / 2 kHz / 6.3 kHz screech peaks are a useful rail indicator. They are an *indicator*, not a fingerprint: braking road vehicles and structural resonances also produce mid- and high-frequency tonal content.
7. **Structure-mounted accelerometers**, for transfer-path work.

**A correction on what item 7 can show.** Draft v1.0 stated: *"Signal arriving at the receptor that is coherent with rail-induced structural vibration is rail-borne. This is the definitive discriminator."* **That is physically wrong and is withdrawn.**

Airborne wheel–rail noise and structure-radiated noise are driven by the *same* excitation — the train. Both will be coherent with a structure-mounted accelerometer during a pass-by. Coherence demonstrates **common excitation, not propagation path**. It separates train-caused energy from road-caused energy, which is useful, but it does not separate airborne rail noise from structural radiation, which is the apportionment question `IDEA-CONCEPT.md` Q1 actually asks.

Separating those two paths requires measured accelerometer-to-microphone transfer functions, ideally with independent structural excitation while no train is present, and realistically requires the beamforming or near-field array methods of `IDEA-CONCEPT.md` Method 1. It is out of scope for a survey conducted from public space.

Draft v1.0 concluded: *"All four together settle it."* **They do not.** Items 1 through 6 give a defensible separation of **train-caused from road-caused** energy, which is more than any prior study of either bridge achieved and is sufficient for the survey's purpose. They do not settle source apportionment within the train-caused component.

### 6.5 Cost and access

No access to the track, the structure, or any MTA or NYCDOT property is required for the microphone positions — all are public parks, sidewalks and publicly accessible bridge walkways. **This is the only part of the entire research programme that requires no agency permission**, which is a notable contrast with every option in `PRECEDENT-AND-MATERIALS.md` Part 3 and 4.

Accelerometer mounting on the structure **does** require NYCDOT permission and should be treated as a separable phase-2 enhancement, not a precondition. If it cannot be obtained, items 1 through 6 of §6.4 still stand — and per the correction in §6.4, they are the items doing the work in any case.

---

## Part 7 — The questions this opens

Continuing the numbering from `PRECEDENT-AND-MATERIALS.md`, which ended at Q22.

**On the word "novel."** Draft v1.0 attached phrases like "not found posed anywhere" to several of these. That claim is narrowed here, following the same narrowing applied to `IDEA-CONCEPT.md` Part 10 after its own review. Several of the questions below are **standard questions in railway acoustics** — source apportionment between rail and structure, the effect of joint and rail condition on radiated noise, empirical propagation laws, single-event `SEL` characterisation. Railway acoustics has asked all of these for decades. What is not found is any instance of them being **asked of these two structures**, in this city, at these receptors, with a comparison between the pair. That is a claim about a gap in the record for a specific pair of assets, not a claim of conceptual originality, and it is the only claim a search of this scope can support. Q31 is not a research question at all — it is an asset-inventory request, and it is listed here because it gates several of the others. Absence claims below are bounded by the searches recorded in Part 10.

**Q23 — Is DUMBO's received noise dominated by the suspended span or by the Brooklyn approach viaduct?** CAIT's finding that "many of the problems these days are actually on the approach spans," combined with the fact that their Manhattan Bridge tests were performed at the Manhattan Approach, makes this the highest-value question in this document. **If the approach dominates, the suspension-bridge literature gap largely dissolves and the worldwide elevated-transit precedent becomes directly applicable.** Not found posed for this structure.

**Q24 — Does the Williamsburg Bridge's central track position, flanked by orthotropic roadway decks, produce a measurable shielding benefit, and with what spectral shape?** The incidental-enclosure question. Draft v1.0 claimed that "no study of any bridge located anywhere addresses shielding by a co-located roadway deck" — an unbounded negative that no search can support, and it is withdrawn. The bounded form: no such study was located in this survey, and none was located for either East River structure. Note also that this question cannot be answered by the survey in Part 6; answering it requires the geometry to be drawn and the paths to be separated.

**Q25 — How much of the received level is attributable to rail joint condition rather than to structure?** A standard question in railway acoustics, asked here of a specific pair of assets. CAIT establishes a factor of about two in structural response between fair and severe joints. The translation from that to radiated sound at a receptor is unmeasured **at these sites** and is the difference between a maintenance programme and a capital project.

**Q26 — What is the actual propagation law from each bridge to its receptors?** Standard method, site-specific gap. Both the Domino FEIS and, by implication, the DUMBO analyses assume simple geometric spreading. On a structure this long, this high, over water, into a street canyon on one side and open frontage on the other, this is an assumption nobody has tested at either site.

**Q27 — What is the `SEL` signature of a single train event on each bridge?** `SEL` is the standard single-event metric in transit noise assessment, including in FTA guidance. It is trivial to obtain, has not been obtained at either site in any located record, and is the only basis on which the two sites can be compared at all.

**Q28 — Why was DUMBO measured and Williamsburg not, and what does the answer say about how environmental attention is allocated?** The § 1204-a report is complaint- and escalation-driven. DUMBO reached the Chairman's office via an Assembly Member. This is a procedural-justice question with a real literature, and it is directly answerable from agency records. **It is also the question most likely to be uncomfortable and most likely to change behaviour.**

**Q29 — Does any mechanism in New York environmental review protect outdoor public space from a pre-existing transportation noise source?** Part 4 suggests the answer is no: the machinery acts on building envelopes, and parks have none. If confirmed against the statute and the CEQR Technical Manual rather than inferred from two FEIS chapters, this is a legal finding of some weight, and it is the natural companion to the § 1204-a Category IV blank in `IDEA-CONCEPT.md` Q11.

**Q30 — Has the level at the Williamsburg Bridge walkway changed since 2007?** Re-occupying Domino FEIS Site 10 yields a nineteen-year repeat observation at near-zero marginal cost. It is a repeat observation and not a change measurement: the 2007 instrument, exact position, height, weather and traffic conditions are not recoverable from the FEIS, so any difference confounds real change with methodological difference. Given CAIT's self-accelerating joint-degradation mechanism a measurable increase is a plausible prediction, and a repeat observation is the cheapest way to see whether one is worth pursuing properly.

**Q31 — Can the Williamsburg Bridge's existing traveling maintenance platforms serve as the access model, or even the physical platform, for under-deck acoustic work on either bridge?** Not a research question — an asset-inventory and feasibility question, listed here because it gates the cost of almost every physical option in `PRECEDENT-AND-MATERIALS.md`. NYCDOT already owns and operates two 119-foot-wide traveling platforms on the sister structure, and that survey concluded access is the binding constraint. The two facts were not found connected in any located document; they may well be connected inside NYCDOT, which is what makes Method 15 worth filing.

---

## Part 8 — Methods

Continuing from Methods 6–10 in `PRECEDENT-AND-MATERIALS.md`.

**Method 11 — The two-site `SEL` survey.** Part 6 as specified. Two people, two meters, one week, no agency permission for the core protocol. **This is the cheapest decision-relevant measurement available anywhere in the programme** and it addresses Q23, Q24, Q26, Q27 and Q30 simultaneously — as a screening and characterisation exercise, not as an identification study.

**Method 12 — Retrieve the CAIT technical report and, if possible, the underlying data.** The news item is rubric 3/5 and reports a study whose full results are not public in the located material. The accelerometer dataset from the Manhattan Approach transit beams, if obtainable, is directly relevant to Method 6 (modal and radiation survey) and may reduce its scope substantially. Contact points are named: Dr. Franklin Moon and Dr. Sougata Roy, Rutgers CAIT. **Cost: an email.**

**Method 13 — The § 1204-a attention audit.** Request, under FOIL, the complaint and measurement records underlying the annual reports across all filed years, for all locations. Establishes the trigger threshold empirically and answers Q28. Extends the existing FOIL in `IDEA-CONCEPT.md` §3.2 rather than duplicating it.

**Method 14 — The outdoor-space regulatory review.** Desk research against the CEQR Technical Manual, the NYC Noise Control Code and PAL § 1204-a to test Q29 properly. Requires a lawyer or a careful reader, no fieldwork, and it is the finding most likely to have consequences outside this project.

**Sequencing.** Methods 12 and 14 are desk work and should start immediately; neither has a dependency. Method 11 is the field core. Method 13 is slow — FOIL responses take months — so it should be filed first and read last.

---

## Part 9 — Where this document is likely to be wrong

Written before external review, in the format the companions use. **Draft v1.1 note:** an adversarial review of v1.0 returned *not fit to publish* with eight blocking issues. All are incorporated in the body above, with the original wording quoted in place rather than deleted. Items 1, 2, 4, 5 and 8 below were already self-declared in v1.0 and the reviewer independently reached most of them; items 9 through 12 are new and come from the review.

1. **The shielding hypothesis may be naive.** Treating flanking orthotropic roadway decks as a "barrier" assumes a geometry that has not been drawn, let alone modelled. The decks are at approximately track level, not above it; the receptor is far below and to the side; the dominant path may pass beneath the deck entirely, through the truss, in which case the decks shield nothing and H1 was never plausible. A deck rigidly connected to the floor system carrying the track may also be a *radiator* rather than a shield. **This is the weakest link in Part 1 and it should be checked against a section drawing before any measurement is funded.** It is also precisely what the visualization companion is for.

2. **"Same trains" was asserted in v1.0 and is not established.** Both services are B Division and therefore share a car gauge, but B/D/N/Q and J/M/Z do not necessarily run the same car classes, and car class affects wheel condition, damping, truck design, consist length and event duration. **This should have been checked and was not.** v1.1 removes the claim from the subtitle, §0.1 and the control table, and adds car class and consist length to the protocol as per-event covariates. Until an inventory exists, fleet is an uncontrolled variable, not a control.

3. **The Williamsburg trackform is inferred, not documented.** The AISC paper establishes "track stringers" and a "track stringer column and bracing" system, and Contract 6 rehabilitated "track stringers and support system, signal system, and rails." That is strong evidence of an unballasted, stringer-supported, direct-fastened arrangement. It is **not** a fastening specification, and the fastener type is the single most acoustically relevant detail. `IDEA-CONCEPT.md` Q2 asks this of the Manhattan Bridge; it must be asked of both.

4. **Part 4's regulatory finding rests partly on a `SNIPPET`.** The NYC Parks FEIS quotation is truncated mid-sentence and was not opened. v1.0 generalised from it to a claim about the whole review system; v1.1 withdraws that generalisation and reduces the finding to the single documented Domino instance. The strength of any broader claim should be re-assessed only once Method 14 is complete.

5. **The CAIT finding is reported at one remove.** Everything in §2.3 comes from an institutional news article about a study, not the study. Rubric 3/5. The "almost double" figure, the fair/poor/severe classification and the approach-span claim are all as reported by the researchers to a communications office. They are plausible and consistent, and they are **not** the primary record. Method 12 exists to fix this. v1.1 additionally withdraws v1.0's inference that this demonstrates maintenance "headroom" — it is an association between condition class and structural response, with no treatment trial and no acoustic outcome.

6. **`SEL` may be harder to obtain cleanly than §5.3 implies.** On a bridge carrying road traffic continuously, defining the event window and the baseline to subtract is not trivial, and at a site with an `L90` of 75.7 dB(A) the residual may be high enough to contaminate the event integral. The night-measurement provision mitigates this and does not eliminate it.

7. **One elected official covering both sites is a convenience, not a finding.** §3.3's observation about Council District 33 is a political opportunity, not evidence, and it is included because it is actionable — not because it is research.

8. **Two units is two units, and this is the objection that matters most.** No amount of careful matching turns a comparison of one structure against another into an estimate of a causal effect. Source, structure and path all change together with bridge identity. **A between-bridge `SEL` difference cannot identify track position, shielding, or a "bridge penalty," and v1.0's framing as a matched-pair experiment claimed that it could.** v1.1 reframes the design as a two-site comparative survey throughout. The survey establishes magnitude, character and whether a difference exists large enough to be worth explaining. It does not construct the counterfactual, and no design available to an unfunded researcher does.

9. **The hypothesis table's frequency threshold was invented.** v1.0's H1 row specified a shielding effect "concentrated above ~250 Hz." No source supports that number and it is withdrawn. A crossover frequency follows from the Fresnel number, which requires the path-difference geometry, which is unknown.

10. **Coherence was misdescribed as a path discriminator.** v1.0 claimed that receptor signal coherent with structural vibration is structure-borne. It is not: airborne and structure-borne components share the same excitation and both will cohere with a structure-mounted accelerometer. §6.4 is corrected and the claim that the four techniques "settle it" is withdrawn.

11. **A null result would not condemn the shielding option class.** v1.0 said that if South Williamsburg is as loud at matched distance, "the option class should be de-prioritised." An incidental 1903 arrangement of vibrating steel decks at unknown elevations is not a purpose-designed barrier, and its failure would not generalise. Withdrawn in §1.3.

12. **The question set is less novel than the phrasing implies.** Several of Q23–Q31 are conventional railway-acoustics questions (notably Q25, Q26, Q27, Q30) or asset-inventory requests rather than research questions (Q31). Methods 11–14 are conventional survey, records-request and legal-review methods. The defensible claim throughout is **"not found asked of these two sites,"** which is how `IDEA-CONCEPT.md` Part 10 was itself narrowed after its own red team, and the same narrowing applies here.

---

## Part 10 — Sources

### 10.1 Verified primary sources

| # | Source | Rubric | State |
|---|---|---|---|
| 1 | Haight, R. & Patel, J. (NYCDOT Director of East River Bridges), *Reconstruction of the Williamsburg Bridge*, AISC / World Steel Bridge Symposium, 2005 | 5 | `VERIFIED` |
| 2 | *Domino Sugar Rezoning FEIS, Ch. 20: Noise*, NYC DCP / AKRF Inc., 2010 | 5 | `VERIFIED` |
| 3 | *New York City Transit Noise Reduction Report*, MTA, pursuant to PAL § 1204-a, 2023 reporting year | 5 | `VERIFIED` |
| 4 | Rutgers CAIT, *CAIT Research Helps NYC Engineers Monitor Structural Health of Manhattan Bridge*, 3 June 2021 (Moon & Roy) | 3 | `VERIFIED` |
| 5 | Change.org, *Reduce Williamsburg Bridge Subway Noise for South Williamsburg & Domino Park*, 16 June 2026 | 2 | `VERIFIED` |
| 6 | Library of Congress HAER collection metadata, surveys `ny1263` (Williamsburg, HAER NY-165), `ny0980` (Manhattan, HAER NY-164), `ny1234` (Brooklyn) | 5 | `VERIFIED` |

### 10.2 Retrieval priority

1. **The CAIT technical report** behind source 4. Everything in §2.3 depends on it, and §2.3 is the most consequential section in the document.
2. **USDOT, *Performance of Rail Fastening Systems on an Open-Deck Bridge***, ROSA-P `dot/35570`, 1 Feb 2018. Directly on point for both bridges. HTTP 403 on retrieval. `SNIPPET`.
3. **NYC Parks FEIS `12DPR005Q` Ch. 13** — to complete the truncated quotation underlying Part 4. `SNIPPET`.
4. **NYCDOT Contract 6 record drawings** (Williamsburg subway reconstruction) and the equivalent Manhattan Bridge track drawings — the fastening specification for both bridges. Records request, not literature.
5. **NYCDOT bridge condition reports** for both structures.

### 10.3 Explicitly not found

Searched for and not located. Each is a falsifiable claim; per `IDEA-CONCEPT.md` §14 and repository issue #5, the prior on these failing is not low.

- Any measurement, anywhere, separating subway from roadway noise on either bridge.
- Any `SEL` or event-normalised metric for either bridge.
- Any third-octave spectrum for the Williamsburg Bridge.
- Any modal, damping or vibration study of the Williamsburg Bridge.
- Any sound measurement taken inside Domino Park.
- Any two-bridge comparative study of NYC East River rail crossings.
- **Any HAER measured drawing for either the Williamsburg or the Manhattan Bridge** — see the visualization companion, §2.

---

## Provenance

**Claims made in this document, and what each rests on.**

1. *Williamsburg carries two central tracks; Manhattan carries four outboard tracks.* — Williamsburg side `VERIFIED` at 5/5 from source 1, three independent loci including a section-drawing annotation. **Manhattan side rests on `IDEA-CONCEPT.md` §4.1, rubric 1/5.** Asymmetric and stated as such in §2.1.
2. *Site 10, Williamsburg Bridge walkway, `Leq` 82.5 dB(A).* — `VERIFIED`, source 2, Table 20-7, quoted.
3. *The measurement does not separate rail from road.* — `VERIFIED`, source 2, authors' own words, quoted twice.
4. *Williamsburg appears zero times in the MTA § 1204-a report.* — `VERIFIED`, source 3, full-text term count. **Scope limit: one reporting year.** Other years were not obtained and may differ.
5. *Bolted rail joints on the Manhattan Bridge are misaligned; severe joints roughly double the vibration of fair ones.* — Source 4, rubric 3/5, one remove from the primary. Quoted verbatim. **Do not treat as a measured acoustic result.**
6. *The regulatory response to Williamsburg Bridge noise was 31 dB(A) of façade attenuation and nothing else.* — `VERIFIED` from source 2. The generalisation to "outdoor space is unprotected" is **partly** `SNIPPET`-supported and flagged in Part 9 item 4.
7. *NYCDOT operates two 119-ft traveling maintenance platforms on the Williamsburg Bridge.* — `VERIFIED`, source 1, quoted.
8. *No `SEL` metric exists for either bridge.* — A negative claim from an exhaustive-intent search. **Falsifiable and probably the easiest claim in this document to disprove.**

**What this document does not contain.** No measurements. No cost figures. No recommended intervention. No claim that either bridge violates any standard, because `IDEA-CONCEPT.md` Q11 establishes that for elevated structures there is no standard to violate. **And, as of v1.1, no claim that the comparison identifies a cause.**

**Claims withdrawn between v1.0 and v1.1.** All are quoted in place in the body rather than deleted, and all are restated in Part 9.

| # | Withdrawn claim | Where | Why |
|---|---|---|---|
| 1 | The study is a "matched-pair" natural experiment that can falsify a mechanism | Title, §1.2, §5.1 | Source, structure and path all change with bridge identity; there is no counterfactual |
| 2 | The two bridges run "the same trains" | Subtitle, §0.1, §1.2 | B Division is a loading gauge, not a fleet assignment |
| 3 | "The entire New York evidence base is in the wrong units" | §5.3 | `Leq`, `L10`, `L90` are correct for their regulatory purpose; `SEL` is additionally necessary, not a replacement |
| 4 | A shielding effect "concentrated above ~250 Hz" | §5.5 | No source; a crossover frequency requires the path-difference geometry, which is unknown |
| 5 | A null Williamsburg result would justify de-prioritising the shielding option class | §1.3 | An incidental 1903 arrangement is not a purpose-designed barrier |
| 6 | Accelerometer/microphone coherence discriminates structure-borne from airborne paths | §6.4 | Both components share the train as excitation and both will cohere |
| 7 | The environmental review system "has no mechanism to protect outdoor public space, and knows it" | §4.3 | Rests on one FEIS outcome plus an unopened snippet; scoped to that instance pending Method 14 |
| 8 | CAIT demonstrates maintenance "headroom" and a monotonic condition-response relation | §2.3 | No treatment trial, no acoustic outcome, three ordered classes |
| 9 | Q24's "no study of any bridge located anywhere" | Q24 | Unbounded negative; narrowed to the searches recorded in Part 10 |
| 10 | A "nineteen-year change measurement for free" | §6.2, Q30 | Repeat observation; the 2007 instrument, position and conditions are not recoverable |

**Method note.** Per issue #11, every quantitative claim above carries a quoted locus. Two claims in this document could not be given one — the NYC Parks quotation (truncated, unopened) and the Manhattan Bridge structural figures (inherited at 1/5) — and both are named in Part 9 rather than smoothed over.

**Review note.** Draft v1.0 was submitted to an adversarial review that returned *not fit to publish* with eight blocking issues, on the same pattern as the reviews of `IDEA-CONCEPT.md` and `PRECEDENT-AND-MATERIALS.md`. The recurring cause identified in issue #11 — reading at abstract level rather than at the locus — is not the cause here. **The cause in this document is different, and worth recording separately: over-claiming inferential strength from a design that does not support it.** v1.0 knew the design was weak, said so in Part 9 item 8, and then wrote the rest of the document as though it were strong. That failure mode is filed as its own methodological finding.

---

*Ethical Tech CoLab. Released under CC BY 4.0. Not peer-reviewed. Part 9 is the best guide to how much to trust the rest.*
