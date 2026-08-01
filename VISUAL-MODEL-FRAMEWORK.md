# Drawing What We Do Not Know

## A Provenance-Tagged Visual Model Framework for the Manhattan and Williamsburg Bridge Track Structures

**Ethical Tech CoLab — Research Programme, Document 4**
Draft v1.1 · August 2026 · revised after adversarial review

---

## 0. About this document

### 0.1 Relationship to the companion documents

| Document | Asks |
|---|---|
| `IDEA-CONCEPT.md` | What is the problem in DUMBO, who is responsible, and what has never been asked? |
| `PRECEDENT-AND-MATERIALS.md` | What has the world already built, and what transfers to a suspension bridge? |
| `WILLIAMSBURG-COMPARATOR.md` | There is a second bridge with the same owner, the same operator, the same division of rolling stock and the same statute. What does it already tell us, and what would measuring it establish? |
| **`VISUAL-MODEL-FRAMEWORK.md`** | **Every argument in the first three documents is an argument about a cross-section nobody has drawn. Can we build that drawing from open data and open tools — and can we make it admit what it does not know?** |

The three preceding documents converge on a single unstated dependency.

`IDEA-CONCEPT.md` asks what fastening system the Manhattan Bridge uses and cannot say. `PRECEDENT-AND-MATERIALS.md` concludes that physical access to the underside is the binding constraint on every intervention it surveys, and that the world literature on elevated-structure noise does not cover this structural type. `WILLIAMSBURG-COMPARATOR.md` proposes a matched-pair measurement study whose entire logic rests on one geometric proposition — that the Williamsburg Bridge's flanking roadway decks stand between the rail and a receptor below, and the Manhattan Bridge's outboard tracks do not — and then concedes, in its own list of weaknesses, that this proposition is inferred rather than documented.

All three are blocked on the same missing object: **a described cross-section.** Not a photograph, not an artist's impression, not a massing model. A section that states where each component is, at what elevation, relative to every other component and to a person standing underneath.

This document is about building that object, and about the fact that the honest version of it is mostly empty.

### 0.2 Method

Same rubric and same discipline as the companions.

**Source credibility, 1–5.** 5 = peer-reviewed or primary agency/statutory document. 4 = technical report from a research institution, or an industry consensus standard published by a recognised standards body. 3 = conference paper, trade technical press, agency secondary. 2 = advocacy, vendor, or enthusiast-technical. 1 = tertiary encyclopaedia, news aggregation, social media.

**Verification state.** `VERIFIED` = the source was opened and the passage supporting the claim was read. `SNIPPET` = only an abstract, search result or quoted excerpt was seen. `UNVERIFIED` = the citation is recorded but nothing was read.

**Locus.** Every quantitative or dispositive claim states which passage of the source it comes from, and quotes it. This control was adopted in Document 3 after all five errors found across Documents 1 and 2 turned out to have one cause: a source summarised from its abstract rather than read to its conclusions. It is retained here, and this document extends the same idea from citations to geometry, which is its central proposal.

**A note on what this document is not.** It is not a model. **No survey was conducted, no point cloud was captured, no photograph was taken.** It is a specification for a model, an inventory of the data that could feed one, a proposal for how such a model should represent its own uncertainty, and one small working reference implementation. Everything below that reads like a result about a bridge is a result about a *document* about a bridge.

### 0.3 Notation

Acoustic quantities follow Document 3 and are written in code style throughout: `Leq`, `L10(1)`, `Lmax`, `SEL`, `dB(A)`, `dB(lin)`, `TL`, `IL`.

Geometry and information-modelling terms:

- `LOD` — Level of Development, the AIA and BIMForum scale `LOD 100` to `LOD 500` describing how completely and reliably a model element has been developed. **Not** "level of detail," although the two are constantly confused; the LOD scale is about reliability of the information, not about polygon count.
- `LOA` — Level of Accuracy, the USIBD scale `LOA10` to `LOA50` describing the metric tolerance to which an existing condition has been captured or represented.
- `GOG`, `GOI`, `GOA` — Grade of Generation, of Information, and of Accuracy, the parallel scales developed in the heritage-BIM literature.
- `IFC` — Industry Foundation Classes, the open interchange schema for built-asset data, published as ISO 16739.
- `SfM` — structure from motion, the photogrammetric technique that recovers camera positions and sparse geometry from an unordered set of overlapping photographs. `MVS` — multi-view stereo, the densification step that follows it.
- `DEM`, `DSM` — digital elevation model (bare earth) and digital surface model (first return, including structures).
- `LiDAR` — light detection and ranging. Airborne unless stated.
- `UAS`, `UA` — uncrewed aircraft system, uncrewed aircraft. The terms used by the FAA and by the NYPD rule discussed in §3.4.

Institutional abbreviations follow Document 3: **NYCDOT** owns both bridges, **NYCT** operates the trains, **C&D** is MTA Construction & Development, **CEQR** is City Environmental Quality Review, **HAER** is the Historic American Engineering Record, **FOIL** is the New York State Freedom of Information Law.

---

## Part 1 — Why a model, and which question it is supposed to answer

### 1.1 The wrong reason to build one

There is an obvious and bad reason to produce a 3D model at this stage of a research programme, which is that it looks like progress. A rendered bridge with a shaded noise plume over DUMBO would be circulated, screenshotted, and believed. It would be believed in exact proportion to how good it looked, and in no proportion at all to how much of it was known.

This is not a hypothetical failure mode. It is the normal outcome. The companion documents already contain an instance of the same pathology in a different medium: an abstract that said "up to 6.8 dB" was propagated into Document 2 as a finding, when the paper's conclusions said the opposite. A rendering is an abstract with better production values.

So the framework proposed here begins from a constraint rather than a capability: **the model must be no more persuasive than it is justified.** Everything in Part 5 follows from that sentence.

### 1.2 The right reason: the section geometry governs what the structure radiates

The strongest argument for building the model is not communication. It is that in the published vibro-acoustic literature, the transverse geometry of an elevated rail structure is a first-order determinant of how much noise the structure itself radiates — and the share of the total that our structure radiates is unknown.

Li, Dai, Zhu and Thompson, *Comparison of vibration and noise characteristics of urban rail transit bridges with box-girder and U-shaped sections*, **Applied Acoustics 186 (2022) 108494** — rubric **5/5**, `VERIFIED`, full text read. Thompson is the author of the standard reference work on railway noise; this is as close to authoritative as this subject gets.

The method they use is exactly the chain this document is trying to make possible:

> "A coupled track-bridge model is introduced to obtain the rail vibration and the power input to the bridge through the rail fasteners. A three-dimensional vibro-acoustic finite element method is applied to obtain the noise radiated from the bridge and the rail subjected to sets of multiple forces acting on them."

And the result, from the conclusions, not the abstract:

> "The single-box and twin box girders produce an average of 8.3 and 11.6 dB(A) less noise from the bridge itself than the U-shaped girder because the mobilities of the U-shaped bridge beneath the rails are greater than those of the box girders."

Read that carefully. Three bridges, same track, same trains, same barriers, same roughness excitation. The **only** difference is the shape of the cross-section. The spread in **structure-radiated** noise is **8.3 to 11.6 dB(A)**.

Draft v1.0 then wrote:

> For comparison, the entire abatement inventory in the MTA's statutory § 1204-a report — the one quoted at length in Documents 1 and 3 — offers 5–7 dB(A) for traction motor work and, in its own words, "resilient rail fastener installation on steel elevated structures (3–5 dBA)."
>
> **The cross-section is worth more decibels than the fasteners.** And nobody has drawn ours.

**That comparison is invalid and is withdrawn.** It compares two quantities that are not the same quantity. The 8.3 and 11.6 dB(A) figures are the change in **noise radiated by the bridge structure alone**. The MTA's 3–5 dB(A) fastener figure is a claim about **total** received noise. A decibel of a component is not a decibel of a total, and the same paper says so in the very next finding: rail noise there is about 10 dB above bridge noise, so **removing the bridge's radiation entirely would move the total by about 0.4 dB** — 10·log₁₀(1 + 10^(−10/10)) = 0.41. On those three bridges, an 11.6 dB swing in the bridge component is worth a fraction of a decibel at the receptor.

This is the fifth instance in this repository of the same failure: a number lifted out of the scope in which it was measured. It is recorded here rather than deleted, because the pattern is the finding.

**What survives, and it is a stronger argument than the one it replaces:**

> Section geometry is a first-order determinant of structure-radiated noise. Whether that matters at the receptor depends entirely on **what share of the total the structure contributes** — and on the Manhattan Bridge that share is unknown.

Which promotes a method that Document 1 listed as merely useful into a **prerequisite**. `IDEA-CONCEPT.md` Method 1 — instrumented source apportionment separating wheel/rail noise from structure-radiated noise — is not one investigation among several. Until it returns a number, nobody can say whether geometry-led intervention on this structure is worth 10 dB or worth 0.4 dB, and no design-build proposal that skips it is defensible. The model this document specifies is what makes that apportionment interpretable; the apportionment is what tells us whether the model's geometry matters. Neither is optional and they are not sequential.

### 1.3 The caveat that has to travel with that finding

Document 2 established a transferability test and it applies to its own strongest citation as much as to anyone else's.

The three bridges in the Applied Acoustics comparison are **concrete**. A concrete box girder and a riveted steel truss carrying open-deck jointed rail are not the same acoustic object, and the paper's other headline finding makes the mismatch explicit:

> "the rail noise level is about 10 dB larger than the bridge noise for the three bridge designs when averaged over the field positions considered in this study. The total noise is therefore dominated by the rail noise which is mainly influenced by the barrier effect but is not affected by the stiffness of the bridge structure."

On a concrete viaduct, structure-radiated noise is 10 dB below rail noise and the structure's stiffness barely matters. That is very probably **not** the case on a lightweight steel truss with no ballast, which is precisely the configuration where the elevated-structure literature reports the largest structure-borne contributions. Document 2 §4 already collected the qualitative reasons.

So the correct statement is narrower than the headline, and it is the one this document will use:

> **In a validated model of an elevated rail structure, changing only the transverse section geometry moved structure-radiated noise by 8.3 to 11.6 dB(A), while moving total noise by very little, because on those concrete bridges rail noise dominated by about 10 dB. The sensitivity was measured on concrete box and U-girders and does not transfer numerically to a steel truss. What transfers is a conditional: section geometry is a first-order variable for the structure-radiated component, and therefore matters at the receptor if and only if that component is a significant share of the total. On the Manhattan Bridge that share has never been measured.**

That is the argument for the model, and it is also the argument for measuring before designing. Not that the model will look good. That the thing we do not know is the thing that decides whether anything else we do is worth doing.

### 1.4 The second reason: the fastener is the model's input, not its ornament

One clause of the method quotation above deserves separating out, because it converts a documentation gap into a modelling blocker.

> "...to obtain the rail vibration and **the power input to the bridge through the rail fasteners.**"

The fastener is not a fine detail to be added at the end. In this class of model it is the interface across which all energy enters the structure.

Draft v1.0 wrote: *"Its dynamic stiffness* is *the boundary condition."* **That is wrong terminology and it is withdrawn.** A fastener is a **coupling element** — a transfer path between rail and structure, characterised by dynamic stiffness, damping and preload, which together set how much power crosses it and in which bands. The boundary conditions of a vibro-acoustic model of this bridge are something else entirely: the tower and pier supports, the bearings, the cable and suspender connections, the joints to the approach structures, and wherever the modeller truncates the domain. Both matter. They are not the same thing, and a model that gets the fastener right and the truncation wrong will still be wrong.

The correct statement: **change the fastener and you change how much power enters the structure, and therefore every structure-radiated number downstream.**

There is a second consequence, which cuts against this document's own thesis and belongs here rather than buried in Part 11. **Geometry cannot supply any of the three fastener parameters.** No scan, no drawing, no `LOD 400` model yields dynamic stiffness, loss factor or clamping preload — those come from a specification, a manufacturer's data sheet, or a laboratory or in-situ dynamic test. So the claim that reaching a given geometric level of detail "makes the model an acoustic input" is false as stated. Geometry is necessary and it is not sufficient. The framework in Part 5 tracks what is *known* about geometry; a parallel and equally important register tracks what is known about **material and interface properties**, and this programme has essentially nothing in it.

`IDEA-CONCEPT.md` §4.2 lists as Q2 — flagged blocking — the question of what fastening system the Manhattan Bridge actually uses. Three documents later it is still unanswered. Document 3 found the nearest thing to a partial answer, from Rutgers CAIT working with NYCDOT: the bridge has **bolted rail joints**, classified fair, poor and severe, and

> "the more severely misaligned splices resulted in more vibration on the bridge, almost double that of the fair splices."

That is a statement about joints, not fastenings, and it is about condition, not specification.

**Conclusion for the framework:** a model of this bridge cannot become a usable acoustic input from geometry alone. The fastener's dynamic properties require a records request, a specification, or a test — none of which is a modelling task and none of which scanning solves. Filed as Method 15 (records) and, for the test route, as a dependency of `IDEA-CONCEPT.md` Method 1.

### 1.5 The third reason, which connects back to Document 1's brief

The original brief for this research programme named robotic on-site fabrication and robotic maintenance as areas to reason about. Document 2 concluded that access to the underside is the binding constraint on every intervention it surveyed, and Document 3 found that NYCDOT already operates

> "Two traveling maintenance platforms ... approximately 119 feet wide and 17 feet long, in order to inspect one complete panel point without needing to move the platform"

on the sister bridge.

A robot — whether it is depositing material, installing a damper, or inspecting a joint — needs geometry, and it needs it in a specific form: **a tolerance envelope, a coverage guarantee, and a bound on localisation uncertainty relative to the surface it will touch.** Those are task requirements, not document-delivery requirements. A path planner needs to know where an interface is to within the compliance of its end effector; a fixture designer needs to know a flange width to within its clamp travel.

The nearest published vocabulary is BIMForum's `LOD 350`, the level at which an element's

> "quantity, size, shape, location, orientation, and interfaces with adjacent or dependent Model Elements can be measured."

Two qualifications, both of which draft v1.0 omitted.

**First, LOD 350 is a coordination definition, not a robotics requirement.** It exists so that trades can detect clashes with each other's work. Nothing in the specification is about machine localisation, and a robot may well need far tighter local accuracy on the 300 mm it is working on than LOD 350 implies, while needing nothing at all about the rest of the span.

**Second, and more important: a robot does not need a model to have geometry.** It can obtain the geometry it needs from a task-specific survey of the work zone, or generate it live from onboard sensing — lidar, structured light, contact probing, force feedback. Mobile manipulation on unmodelled infrastructure is an active field precisely because prior models are usually absent or wrong. So the absence of a public `LOD 350` model is **not** a blocker on robotic intervention.

Draft v1.0 claimed otherwise:

> "The first obstacle to the robotic-maintenance thesis is not actuation, not materials, not power, not certification. It is that no public description of the work surface exists at the resolution a machine would need to touch it. The geometry gap precedes the robotics question by two levels of development."

**Both sentences are withdrawn.** "Two levels of development" treats LOD as a sequential maturity ladder, which BIMForum explicitly denies — the 2024 specification states that `LOD 500` "does not indicate a higher level than 400." And "the first obstacle" was asserted without any comparison against actuation, power, certification, access or the union rules governing work on a NYCDOT structure, several of which are plainly harder.

**What survives is narrower and still worth stating.** Nobody can currently *specify* a robotic intervention on this bridge from public information — not scope it, not price it, not choose an end effector, not write a procurement document — because no public description of the work surface exists at the resolution any of those tasks require. That is a **planning and procurement** blocker, not a technical one, and the way through it is a task-specific survey of a representative bay rather than a full-structure model. Part 4 sets out how far the public record actually reaches.

---

## Part 2 — What already exists

Every row below was queried, not assumed. Negative results are recorded at equal length to positive ones because rediscovering them is the expensive part.

### 2.1 The HAER result

The Historic American Engineering Record is the natural first stop for measured drawings of landmark American structures, and both bridges are recorded in it. The Library of Congress collection API was queried directly for each survey.

| Bridge | HAER survey | Photographs | Measured drawings |
|---|---|---|---|
| Brooklyn Bridge | `ny1234` | 90 | **1 sheet** — "Plan, elevation, detail at Manhattan tower" |
| Manhattan Bridge | `ny0980` · HAER NY-164 | 11 plus 1 colour | **none** |
| Williamsburg Bridge | `ny1263` · HAER NY-165 | 9 | **none** |

Rubric **5/5** (primary collection metadata), `VERIFIED` by direct API query.

The two bridges that carry subway trains have no measured drawings in the national record. Their neighbour, which carries none, has one. The Williamsburg set is attributed to Jet Lowe, 1991.

This is not a total loss. HAER photography is large-format, deliberately composed for documentation, and archivally scanned, which makes it a legitimate `SfM` input — see §3.3. But a photograph is a picture of a bridge, not a description of one, and no amount of processing turns eleven exterior views into a section.

### 2.2 The one real section source

`WILLIAMSBURG-COMPARATOR.md` §2.2 established that a single document contains genuine transverse information for either bridge: Haight and Patel, *Reconstruction of the Williamsburg Bridge*, AISC 2005, rubric **5/5** — co-authored by the Director of East River Bridges at NYCDOT.

For the framework, the relevant content is its figure annotations, which name the components of the section:

> `NORTH FOOTWALK` · `CL.TRK J1` · `CL.TRK J2` · `NEW STIFFENERS (TYP)` · `NEW BMT TRACKS` · `SOUTH PEDESTRIAN WALKWAY` · `NEW TRACK STRINGER COLUMN AND BRACING` · `REPAIR FLOORBEAM, TRUSS BOTTOM CHORD, LATERAL BRACING (TYP)`

and one dimension in prose:

> "The stiffening truss is 67 feet wide and approximately 40 feet deep and is pinned at each main tower."

That is the entire verified transverse dimensional content available for either East River subway bridge. **Two numbers — one width, one depth — and both describe the envelope rather than locating anything inside it.**

A methodological caution that must be carried into any use of this figure: PDF text extraction does not preserve spatial order. The labels above are known to exist in the drawing; their left-to-right and top-to-bottom arrangement as extracted is an artefact of the extraction, not evidence about the bridge. Any element placed on the basis of extracted label order is `ASSUMED`, not `INFERRED`. This distinction is exactly what Part 5 is built to carry.

### 2.3 Citywide 3D data

| Dataset | Content | Status |
|---|---|---|
| 2017 NYC Topobathymetric LiDAR | 1 ft `DEM` and `DSM` plus classified point cloud; Quantum Spatial for NYC DoITT | Available — NYC Open Data, NYS GIS clearinghouse, NOAA S3 bucket `noaa-nos-coastal-lidar-pds`, OpenTopography |
| NYC 3D Model by Community District | Every building present in 2014, from the DoITT 2014 aerial survey | Available. **Buildings only** — no bridge structure |
| OpenStreetMap | Both bridges as tagged ways, including rail alignment | Almost certainly available; the Overpass API returned HTTP 406 without a user agent and then 504 gateway timeouts from two mirrors during this review. Recorded as `UNVERIFIED` |
| USGS 3DEP | National elevation coverage | Available, coarser than the city product |

The NYC 3D Model is more useful than it first appears, and for a reason unrelated to the bridge. Receptor-side acoustics in DUMBO depends on the surrounding buildings — they are the reflecting and shielding surfaces that determine what a person in Brooklyn Bridge Park actually receives. A building-only model is the *right* dataset for that half of the problem and it is complete.

For the bridge itself it contributes nothing.

### 2.4 What NYCDOT holds and does not publish

Record drawings, shop drawings, inspection reports and the rehabilitation contract documents for both bridges exist. They are the only plausible route to the level of detail this programme needs, and none of them are public.

This is a FOIL question, not a research question, and it is filed as Method 15. It is worth noting the asymmetry it creates: the single most valuable geometric artifact in this entire framework is one records request away, and every open-data route described in Part 3 is a workaround for not having made it.

---

## Part 3 — The occlusion problem, and four ways past it

### 3.1 The problem, stated precisely

Every citywide 3D dataset New York publishes is captured from an aircraft looking down. An aircraft sees the **top of the deck**.

The geometry that governs this entire research programme is, without exception, underneath it:

- the floor beams and their spacing
- the track stringers and the stringer-to-floorbeam connection
- the rail fastening assembly
- the truss bottom chord and lateral bracing
- the outboard cantilever framing on the Manhattan Bridge, which carries the tracks nearest the neighbourhood
- the clearance envelope over the streets of DUMBO
- any existing shielding, screening or debris containment already installed

Each of these is in the deck's optical shadow from above and its acoustic shadow from the receptor below at the same time, which is a coincidence worth pausing on: **the surfaces that matter most acoustically are exactly the ones an aerial survey cannot see.** Downward radiation is the mechanism, and downward-facing is the geometry.

This is not a resolution limit. Denser LiDAR does not fix it. It is line of sight. **There is a hard floor at `LOD 200` for every free public dataset covering these bridges, and it is geometric, not financial.**

### 3.2 Route one: the walkway

Both bridges carry public pedestrian walkways running the full length of the structure, alongside the track zone. On the Williamsburg Bridge the AISC paper describes

> "a new footwalk/bikeway system that is barrier-free"

and names both a north footwalk and a south pedestrian walkway.

This is the same property that makes the acoustic protocol in Document 3 §6.5 cheap: **the measurement that matters can be taken from public space, with no permission from anybody.** A camera, an afternoon, and a walk.

Walkway-level `SfM` will not see the underside either. What it will see, and what nothing else available will, is:

- the *relative vertical positions* of walkway, roadway deck, track and truss, which is the single weakest link in the shielding hypothesis of Document 3
- the truss members from inside the structure
- the trackside face of whatever screening exists
- the actual sightline from a walkway position to a receptor position below

That list is short but it is targeted precisely at the propositions the companion documents cannot support. It should be executed on the Williamsburg Bridge first, because the Williamsburg Bridge is where the inference is load-bearing.

Filed as Method 16.

### 3.3 Route two: rephotogrammetry of the HAER negatives

Eleven and nine large-format documentation photographs, respectively, taken by a professional architectural photographer with archival intent, are a better `SfM` input than most casual imagery. They are also thirty-five years old, which for a structure is close to irrelevant at the massing scale and completely relevant at the condition scale.

The limitation is baseline. Documentation photography is composed for legibility, not for reconstruction; the views are unlikely to have the overlap and the varied vantage points a solver needs. Whether they are sufficient is an empirical question that costs one afternoon of processing to answer, since the images are public domain and the software is free.

Filed as Method 17, priority low, cost near zero.

### 3.4 Route three: UAS, and the regulatory wall

Uncrewed aircraft are the obvious answer to an occlusion problem, and the bridge-inspection literature is now substantial: UAS photogrammetry of bridge undersides is routine practice in several state DOTs, and comparative studies report accuracies competitive with terrestrial survey.

In New York City it is a different proposition, and the primary source is unambiguous.

NYPD Unmanned Aircraft Permit Application Portal, official FAQ — rubric **5/5**, `VERIFIED`:

> "Prior to July XX, 2023, section 10-126(c) of the New York City Administrative Code prohibited most take-off and landings of unmanned aircraft (UA) within New York City. The Department's new rule, 38 RCNY 24, creates a procedure by which the public may submit applications to launch and land UA, including drones, within the City."

> "Currently, UA may only launch or land from locations designated by the Department of Transportation (DOT), or from specific model aircraft fields designated by the NYC Department of Parks and Recreation."

> "Applicants must submit a completed application at least 30 days in advance of the date of the first proposed take-off or landing."

> "all applications must propose an UA operator who have obtained a Remote Pilot Certificate pursuant to Part 107 of Title 14 of the CFR."

> "Drone operators are required to have certain documents on hand ... including the take-off/landing permit issued, a copy of the prerequisite insurance policy, documentation of FAA authorization to operate an UA and any relevant waivers, and a government-issued photo ID."

And, importantly for anyone budgeting the attempt:

> "An UA take-off and landing permit alone does not constitute a reservation or grant exclusive use of the location listed on the permit."

So the stack is: a Part 107 certificate, an insurance policy, FAA airspace authorisation for Class B airspace over the East River between two international airports, a 30-day NYPD application, and separate permission for whatever ground you launch from. Add that both structures are critical infrastructure under active security posture.

**The finding is a comparison, not a prohibition.** The walkway route requires a camera. The UAS route requires four permissions from three agencies and a 30-day lead time, and it is the *only* route that reaches the underside without NYCDOT's cooperation. Which means the underside — the acoustically decisive surface — is behind an institutional gate no matter which way you approach it.

That is the same conclusion Document 2 reached from a completely different direction when it identified access as the binding constraint on intervention. It is now also the binding constraint on *description*. Filed as Q34.

### 3.5 Route four: the maintenance platforms

The AISC paper documents two traveling maintenance platforms on the Williamsburg Bridge, approximately 119 ft by 17 ft, sized to inspect one complete panel point without repositioning.

A platform that exists to put a human inspector under the deck is, without modification, a platform that can put a camera or a scanner there. This is the cheapest conceivable route to `LOD 350` underside geometry on either bridge, it uses equipment the owner already operates, and it requires exactly one thing this programme does not have: NYCDOT's cooperation.

Which makes it the first thing to ask for. Filed as Method 18.

---

## Part 4 — The ladder, mapped to the standards that already exist

### 4.1 Why use an existing scale

It would be easy to invent a five-rung scale for this project. It would also be a mistake, because two consensus scales already exist, they are widely used in the industries that would execute a design-build project on this bridge, and using them makes the framework's claims legible to the people who would have to act on them.

**BIMForum / AIA Level of Development**, LOD Specification 2024 Part I — rubric **4/5** (industry consensus standard), `VERIFIED`, definitions read in full:

| `LOD` | Definition, quoted |
|---|---|
| 100 | "may be graphically represented in the Model with a symbol or other generic representation, but does not satisfy the requirements for LOD 200" |
| 200 | "generically and graphically represented within the Model with approximate quantity, size, shape, location, and orientation" |
| 300 | "graphically represented within the Model such that its quantity, size, shape, location, and orientation can be measured" |
| 350 | "...and interfaces with adjacent or dependent Model Elements can be measured" |
| 400 | "graphically represented within the Model with detail sufficient for fabrication, assembly, and installation" |
| 500 | "a graphic representation of an existing or as-constructed condition developed through a combination of observation, field verification, or interpolation" |

**USIBD Level of Accuracy**, Document C120 Guide v2.0 (2016) — rubric **4/5**, `VERIFIED`:

| `LOA` | Upper range | Lower range |
|---|---|---|
| LOA10 | user defined | 5 cm |
| LOA20 | 5 cm | 15 mm |
| LOA30 | 15 mm | 5 mm |
| LOA40 | 5 mm | 1 mm |
| LOA50 | 1 mm | 0 |

with the note attached to the table: "Specified at the 95 percent confidence level." The scale is derived from the five tolerance ranges of DIN 18710 and organised by CSI UniFormat.

Two features of these standards matter enormously here and are developed in Part 5.

### 4.2 The ladder for these two bridges

The rungs below are the project's own, but each is stated in terms of the standard scales so it can be commissioned rather than merely described.

**L0 — Site and context.** Shorelines, street network, parcels, terrain, receptor park boundaries, surrounding building massing. Equivalent to `LOD 100`–`LOD 200` for context objects. **Availability: complete.** NYC Open Data, OpenStreetMap, USGS 3DEP, NYC 3D Model by Community District.

**L1 — Bridge massing.** Towers, cables, deck envelope, approach viaducts. `LOD 200`, `LOA10`–`LOA20`. **Availability: good.** 2017 topobathymetric LiDAR at 1 ft resolution, classified point cloud.

**L2 — Structural system.** Trusses, floor beams, stringers, cantilever framing, lateral bracing, and the clearance envelope. `LOD 300`. **Availability: partial and lopsided.** For the Williamsburg Bridge, one dimensioned prose statement and a set of named components from the AISC figures. For the Manhattan Bridge, nothing above rubric 1/5. This is where the aerial data stops being able to help at all, for the reason given in §3.1.

**L3 — Track assembly.** Rails, joints, bearers, guard rails, fastening layout, the stringer-to-rail interface. `LOD 350`. **Availability: almost none.** Element names from one figure annotation; the Rutgers CAIT work confirms bolted joints exist on the Manhattan Bridge approach and classifies their condition, which is a statement about state rather than geometry.

**L4 — Component schematics.** Fastener type, clip, pad, tie plate, bolt pattern, torque. `LOD 400`. **Availability: none.** No public source for either bridge.

The brief that opened this research programme asked for a visual review reaching "down to the schematics of screws." The honest answer, four documents in, is that L4 is a records request rather than a modelling exercise — and per §1.4 it is also the level at which the model would become an acoustic input rather than an illustration.

### 4.3 The Heritage framework applies

The USIBD specification provides two sets of suggested accuracy levels:

> "The second is the 'Heritage' Framework which is intended for use on heritage applications that, generally speaking, have higher LOA requirements."

Both bridges are designated historic structures. Both are more than a century old, riveted, and repeatedly modified. Any documentation programme on either should be specified against the Heritage framework, which is a small point with a real budgetary consequence and one that a proposal writer will otherwise miss.

---

## Part 5 — The contribution: carrying provenance alongside accuracy

### 5.1 What the existing standards already require, and nobody does

Two clauses in the standards quoted above are doing more work than they appear to.

The first is in the BIMForum definition of `LOD 500`, which is the level that applies to any model of an existing structure:

> "developed through a combination of observation, field verification, **or interpolation**. **The level of accuracy shall be noted or attached to the Model Element.**"

Not attached to the model. Attached to **the element**. Per component. That is already a requirement, in a consensus standard, published for over a decade. And the definition explicitly contemplates interpolation as a legitimate source of geometry — which is honest, and which is precisely why the accuracy note is mandatory.

The second is the USIBD distinction between two kinds of accuracy:

> "Measured Accuracy represents the standard deviation range that is to be achieved from the final measurements taken regardless of the method used to acquire those measurements. Represented Accuracy represents the standard deviation range that is to be achieved once the measured data is processed into some other form such as line work or a model."

> "The primary distinction is that error will always be introduced when measured data is processed into, or 'represented' as, some other form of deliverable."

So the industry has already separated *how well you measured it* from *how much of that survived into the drawing*, and requires both to be stated per element.

**Neither requirement is met by any public-facing model of a New York bridge, and neither could be met by this project, because both presuppose that a measurement happened.**

### 5.2 What LOA does not cover, and why that is not LOA's fault

`LOA` is a metric scale. It answers: given that this element was measured, how close is the number to reality? Its lowest rung, `LOA10`, is "user defined to 5 cm."

Draft v1.0 wrote that there is "no rung for" unmeasured geometry and called this "a defect discovered in LOA." **That is withdrawn, and it was an unfair reading of the standard.** `LOA` is explicitly a metric-accuracy framework for captured data. An element that was never measured has no measured accuracy — the correct value is **null**, not a low rung, and a standard is not defective for declining to assign a number to something it does not describe. Inventing an `LOA05` for reasoning would corrupt the scale by putting inference and measurement on one axis, which is precisely the error this section is trying to avoid.

The real gap is therefore not inside `LOA` at all. It is that **nothing in the delivery chain requires the unmeasured elements to be labelled as such**, so a model containing both surveyed and reasoned geometry ships as a single undifferentiated object. `LOD 500` gets closest — it mandates that "the level of accuracy shall be noted or attached to the Model Element" — but says nothing about what to attach when the answer is "we did not measure this; we reasoned it from a sentence."

So the proposal here is **complementary lineage metadata**, sitting beside `LOA` rather than extending it:

- `LOA` answers *how well was it measured*, and is null when nothing was measured.
- Provenance answers *where did this geometry come from*, and is never null.

Applied to the section of the Manhattan Bridge — the bridge this entire programme exists to address — the honest statement is that **no transverse dimension is available at better than rubric 1/5 from a tertiary encyclopaedia, a limitation `IDEA-CONCEPT.md` §4.1 already concedes about itself at line level.**

### 5.3 Prior art, and why no novelty is claimed

The idea of tagging model elements with their reliability is not new, and it would be dishonest to present it as such. The heritage-BIM literature has been working on this for a decade.

- Banfi, *BIM orientation: grades of generation and information for different type of analysis and management process*, ISPRS Archives XLII-2/W5 (2017), 57–64 — introduces `GOG`, `GOI` and `GOA` for heritage models. Rubric **4/5**, `SNIPPET`.
- Brumana, Banfi, Cantini, Previtali, Della Torre, *HBIM level of detail-geometry-accuracy and survey analysis for architectural preservation*, ISPRS Archives XLII-2/W11 (2019), 293. Rubric **4/5**, `SNIPPET`.
- The concept of a Level of Reliability for heritage models appears across the review literature, and practitioner guidance already describes the intent plainly: every piece of information in a heritage model can be tagged on a scale "from 'reliable and trusted' through 'you can't necessarily count on this information'." Rubric **2/5** (practice blog), `SNIPPET`.

Draft v1.0 claimed that this mechanism "has not been applied to transport infrastructure acoustics." **That claim is withdrawn.** Two of the three sources above are `SNIPPET` — their full scope was not read — and the negative search that would be needed to support the claim is the one filed as Method 20, which has not been done. A claim of novelty cannot rest on a search that the same document schedules as future work.

What is offered instead is a **proposed project-specific application**, novelty unassessed:

1. **The consumer is different here, which changes what the metadata has to carry.** The heritage literature's consumer is a conservator. Here the consumer is an acoustic analysis whose most sensitive geometric input, per §1.2, is the least documented. Whether the heritage schemas already accommodate that is exactly what Method 20 should determine, and if they do, this project should adopt one rather than mint another.

2. **Provenance is carried separately from accuracy rather than folded into it.** `LOA` measures error given a measurement; provenance records the source class independent of stated precision. §5.2 explains why merging them would be a mistake.

3. **The provenance scale is the same scale used for the prose.** This is the part specific to this programme rather than to the field. Documents 1 through 3 rate every citation 1–5 for credibility and `VERIFIED`/`SNIPPET`/`UNVERIFIED` for depth of reading. If a model element carries the same two fields, a reader can move between the written argument and the drawing without changing units, and a single reviewer can attack both with one method. Small idea, useful consequence: **the model becomes part of the citation apparatus rather than an illustration of it.**

### 5.4 The schema

Proposed as an `IFC` property set, `Pset_ResearchProvenance`, attachable to any `IfcElement`, and equally expressible as a GeoJSON property block or a plain column in a spreadsheet. The point is that it is trivial; the point is that it is *there*.

| Property | Type | Values |
|---|---|---|
| `SourceRef` | text | Citation key resolving to the document's source list |
| `SourceCredibility` | integer | 1–5, the same rubric as the prose |
| `VerificationState` | enum | `VERIFIED`, `SNIPPET`, `UNVERIFIED` — how deeply the source was read |
| `GeometryProvenance` | enum | `MEASURED`, `DOCUMENTED`, `INFERRED`, `ASSUMED` — what supports the shape |
| `GeometrySupportNote` | text | What the source does and does not establish about this element's geometry |
| `Locus` | text | The exact passage the geometry rests on, quoted |
| `ObservationDate` | date | When the source observed the structure — not when it was published, and not today |
| `CurrentApplicability` | enum | `CURRENT`, `SUPERSEDED`, `UNKNOWN` — whether the observed condition is believed to still hold |
| `AcousticRelevance` | text | Why this element matters to the noise question, or that it does not |
| `MeasuredAccuracy` | enum | `LOA10`–`LOA50`, or null where nothing was measured |
| `RepresentedAccuracy` | enum | `LOA10`–`LOA50`, or null |

**The two enums are independent, and keeping them independent is the whole point.** A source can be fully `VERIFIED` — opened, read, passage quoted — and still support a `GeometryProvenance` of `ASSUMED`, because a sentence establishing that an element exists says nothing about where it is. The reference implementation in Part 8 got this wrong in its first version by collapsing both into one field, which is how eight components came to be labelled "verified" on the strength of a source that located none of them.

**`ObservationDate` and `CurrentApplicability` exist because a document describes a moment.** The AISC paper describes the Williamsburg Bridge as reconstructed to 2005; the CAIT work reports instrumentation from around 2021; a 2005 statement that two traveling maintenance platforms were installed is not a 2026 statement that two traveling maintenance platforms are operational. Without these fields a model silently presents twenty-year-old observations as present conditions, which is a different failure from the provenance failure and just as easy to make.

`GeometryProvenance` is the new field and its four values are defined as:

- **`MEASURED`** — the geometry derives from an instrument reading of the actual structure. Carries an `LOA`. **No element of either bridge is at this level.**
- **`DOCUMENTED`** — *this element's* position or dimension is stated numerically in a source that was read. Carries the source's rubric and a locus, not an `LOA`, because the source's own accuracy is generally unstated. **No element of either bridge is at this level either.** The Williamsburg Bridge has two stated dimensions — a 67 ft truss width and an approximately 40 ft truss depth — but both describe the overall envelope and neither locates any element within it, so the truss members that carry them are `INFERRED`, not `DOCUMENTED`. That distinction is the difference between a drawing and a claim about a drawing.
- **`INFERRED`** — the element's *existence* is documented but its position or dimension is reasoned. All 13 Williamsburg components and 10 of the 14 Manhattan components.
- **`ASSUMED`** — the element is placed by engineering judgement with no source statement locating it at all. Four components, all on the Manhattan Bridge: both outboard cantilever assemblies, the floor system, and the rail-joint marker — the last of which sits on a `VERIFIED` 3/5 source that establishes joints exist without locating one, which is exactly the case the two-field schema exists to represent.

### 5.5 The rendering rules

A provenance property that only appears in a properties palette is a property nobody reads. The framework's second requirement is that provenance is **visible in the geometry itself**, so that the picture cannot be circulated without its uncertainty.

| State | Render |
|---|---|
| `MEASURED` / `DOCUMENTED` | Solid fill, solid outline, full opacity |
| `INFERRED` | Reduced opacity, dashed outline |
| `ASSUMED` | Low opacity, dotted outline, and excluded from any dimension callout |

Plus three interaction requirements:

- **Filter by provenance.** The reader must be able to switch `ASSUMED` and `INFERRED` geometry off and see what is left. The filter must **hide** the geometry, not merely fade it: a faded outline is still a shape a reader will trace, and the honest experience of switching both off on this project is an empty frame. This is the single most useful feature and it is close to free to implement.
- **Locus on selection.** Clicking any element shows the quoted passage its geometry rests on, or states that there is none.
- **A standing tally.** The counts of each state, displayed permanently, not buried in a methods appendix.

The rule that follows from all of this, and that this programme adopts:

> **No dimension may be annotated on any element whose `GeometryProvenance` is `ASSUMED`.** If we do not know where it is, we do not get to say how big it is.

---

## Part 6 — The toolchain

### 6.1 An all-open-source path

No proprietary licence anywhere in the chain, so the result can be published under the same terms as the written research and rebuilt by anyone who disputes it. This is not ideological; it is the condition under which a red team can actually check the work.

| Stage | Tool | Licence | Role |
|---|---|---|---|
| Geospatial base | QGIS | GPL | Georeferencing, terrain, parcels, receptor boundaries |
| Point cloud | CloudCompare | GPL | LiDAR handling, registration, cleanup, cloud-to-cloud comparison |
| Photogrammetry | Meshroom, COLMAP | MPL-2.0, BSD | `SfM` and `MVS` from walkway photography |
| Cloud to BIM | Cloud2BIM | Open source, arXiv 2503.11498 | Automated point cloud to `IFC` conversion |
| BIM core | IfcOpenShell | LGPL | `IFC` read and write; the interchange spine |
| Modelling | Blender with Bonsai | GPL | Component authoring, level-of-detail control, rendering |
| Parametric CAD | FreeCAD 1.0 | LGPL | L4 parametric parts, once a specification exists |
| Coordination | Speckle | Apache-2.0 | Versioned model sharing and review |
| Acoustic mapping | NoiseModelling, Université Gustave Eiffel | GPL-3.0 | CNOSSOS-EU outdoor propagation |
| Web delivery | glTF, Three.js | MIT | The reviewable artifact itself |

`IFC` is the right interchange format rather than a mesh format, and the reason is recent: IFC 4.3 extends the schema to infrastructure including bridges and alignments, and has been adopted as an ISO standard in the 16739-1 series. Rubric **3/5** via secondary sources, `SNIPPET`; the exact ISO edition year should be confirmed against buildingSMART before it is cited in a proposal. FHWA has published bridge information model standardisation guidance in the same lineage (HIF-16-011), rubric **5/5**, `SNIPPET`, and is the natural authority to cite in an American infrastructure context.

### 6.2 Where the toolchain will mislead you

Stated up front, because the failure mode of a good-looking pipeline is unearned confidence.

**NoiseModelling implements CNOSSOS-EU, whose rail source model is calibrated on European at-grade and ballasted track.** A 1903 open-deck steel suspension bridge with jointed rail on stringers is outside its domain. It will still return a number, formatted identically to a number that means something.

**CNOSSOS handles a barrier by diffraction over an obstacle.** It does not model a steel structure re-radiating as a surface. Per §1.2, structure re-radiation is the mechanism this programme most needs modelled, and it is the one thing the free propagation tool does not do. The methodologically correct pairing is `NoiseModelling` for propagation from a source position to a receptor, and a separate vibro-acoustic finite element step of the kind Li et al. describe for what the structure itself emits — and that second step needs `LOD 300` geometry and a fastener stiffness, neither of which exists.

**Use the propagation model for relative geometry, not absolute level.** "Does moving this screen 3 m change the shadow over the dog run" is a fair question. "How many decibels" is not.

**Photogrammetry produces confident geometry from bad inputs.** `SfM` will reconstruct a plausible fastener that does not exist, and the reconstruction will not look any different from a correct one. Scale must come from a measured reference physically in frame, never from the solver, and the resulting `RepresentedAccuracy` must be validated against independent measurements — the USIBD specification calls this Representation Validation and treats it as a separate step from Measurement Validation, correctly.

**Cloud2BIM and every automated scan-to-BIM tool were developed on buildings.** Planar walls, orthogonal rooms, repeated storeys. A riveted lattice truss violates every assumption in that family of algorithms. It should be tried, because it is free, and it should be expected to fail.

---

## Part 7 — What a model of this is actually for

Three distinct uses get conflated, and they have different data requirements. Separating them is the difference between a fundable proposal and a wish.

### 7.1 Communication

Showing a resident, a council member or a Community Board what is above them and why it is loud. Requires L1 and honest labelling. **Achievable now.** This is the only one of the three that current data supports, and it is the purpose of the reference implementation in Part 8.

### 7.2 Coordination

`PRECEDENT-AND-MATERIALS.md` Method 10 proposed an interface matrix: for every candidate intervention, which asset owner's component does it touch, and who must therefore approve it. Document 2 identified this as the cheapest high-value method in the programme, and it is now filed as repository issue #8.

An interface matrix is a geometric question wearing an institutional costume. "Does this damper attach to NYCDOT steel or NYCT track?" is answered by a model at `LOD 350`, where interfaces between adjacent elements can be measured, and cannot be answered reliably at any lower level.

**Requires L3. Not achievable without a records request or underside access.** This is the strongest argument for Method 15 and Method 18, because it converts a modelling wish into an approvals dependency that a project sponsor already understands.

### 7.3 Simulation

Feeding a vibro-acoustic model of the kind validated in Applied Acoustics 2022. Requires L3 geometry *and* a fastener dynamic stiffness *and* a rail roughness spectrum *and* a validated radiation model for a lattice truss, the last of which Document 2 established does not exist in the literature for this structural type.

**Requires L3 plus L4 plus new physics. Not achievable, and should not be promised.** A proposal that quietly implies this capability is the failure mode this framework exists to prevent.

---

## Part 8 — The reference implementation

`visual-review/section-problem.html` is a single self-contained HTML file, no build step, no dependencies, no network access, and it implements Part 5 at the smallest scale that demonstrates it.

**What it does.** It draws schematic transverse sections of both bridges. Every component carries **two independent fields** — `VerificationState`, how deeply the source was read, and `GeometryProvenance`, what actually supports the drawn shape — plus a source reference with rubric, a quoted locus, an observation date, a note stating what the source does and does not support geometrically, and a note on acoustic relevance. Provenance is rendered in the geometry — solid green, dashed amber, dotted red — and can be filtered, so a reader can switch the assumed and inferred geometry off and see what remains. A receptor sightline overlay draws the straight line from each track to the receptor position. Four further tabs carry the level-of-detail ladder with an auditable test at each rung, the source inventory including the HAER negative result, the toolchain with its failure modes, and the limitations. A running tally states how many components sit in each state.

**The result, and it is worse than draft v1.0 reported.** Of 27 components across both bridges: **0 `MEASURED`, 0 `DOCUMENTED`, 23 `INFERRED`, 4 `ASSUMED`.** Not one element of either section is drawn at a position that any source states. Switching off both the inferred and the assumed geometry leaves an empty frame, which is the most honest single output the artifact produces.

Draft v1.0 reported "8 `VERIFIED`, 10 `INFERRED`, 9 `ASSUMED`" and added that "9 of 14 components on the Manhattan Bridge are placed by reasoning rather than stated by any source." Both are wrong. The first used one conflated field where the schema in Part 5 defines two, and marked components "verified" because their *source* had been read — the truss envelope does not verify a chord position, "the central section" does not verify a track offset, "four cables" does not verify a transverse coordinate, and the CAIT article does not locate a rail joint. The second undercounted, because `INFERRED` components are placed by reasoning too; the correct figure for the Manhattan Bridge is 14 of 14. **Both are recorded in Part 11 items 13 and 14 rather than quietly replaced, and the artifact violating its own document's schema is itself the most useful thing this exercise produced.**

**What it does not do.** It computes no acoustics. The sightline is a straight line, which is a statement about geometry and not about sound. Both sections are schematic and **not to scale**; the only two transverse dimensions stated in any located source — the Williamsburg Bridge's 67 ft truss width and approximately 40 ft truss depth — are not drawn in proportion to each other, and no dimension is annotated on any component, per the rule in §5.5. There is no L4 content because no public source has any, and §1.4 establishes that L4 geometry would not be sufficient even if it existed. And it encodes one author's inferences, assigned by the same person who drew the geometry — a conflict whose only mitigation is that every inference is labelled and every source is named, so that a reviewer can attack them individually rather than having to attack the picture as a whole. A reviewer did, and eight assignments changed.

**The productive use of it is as a shopping list.** Every red component is an argument for a specific records request, and the tally is the size of the gap between what this programme claims to understand and what it can show.

---

## Part 9 — The questions this opens

Continuing the numbering from `WILLIAMSBURG-COMPARATOR.md`, which ended at Q31.

**Q32.** What is the *measured* transverse section of the Manhattan Bridge at midspan, at a tower, and at the Brooklyn approach? Every acoustic argument in this programme depends on it and no source above rubric 1/5 states any of it. **Blocking.**

**Q33.** What are the relative *vertical* positions of the Williamsburg Bridge's track, roadway deck, walkway and truss bottom chord? This determines whether the shielding hypothesis of Document 3 is even geometrically possible. **Blocking on Document 3.**

**Q34.** Is there any route to underside geometry on either bridge that does not require NYCDOT's cooperation or a four-agency UAS permission stack? If the answer is no, then the description problem and the intervention problem have the same gatekeeper, and that should be stated plainly to any sponsor.

**Q35.** Does the 8.3–11.6 dB(A) section-geometry sensitivity measured on concrete girders have any analogue on a steel truss? Document 2 found no quantified acoustic result from any rail-carrying suspension bridge; this is the same gap seen from the modelling side.

**Q36.** What is the dynamic stiffness of the rail fastening assembly actually installed on each bridge? Per §1.4 this is the model's boundary condition, not a detail.

**Q37.** Do the existing traveling maintenance platforms on the Williamsburg Bridge have an analogue on the Manhattan Bridge, and what is their instrument payload capacity? This determines whether Method 18 is a request or a proposal.

**Q38.** Has any transport agency anywhere published a provenance-tagged or reliability-tagged model of an existing structure for public review? The heritage sector has; a negative result for transport would strengthen the contribution claim in §5.3 and a positive one would correct it.

**Q39.** What `LOA` does walkway-based `SfM` actually achieve on a lattice truss under bridge lighting conditions, and is it enough to resolve Q33? This is an empirical question answerable in one afternoon.

**Q40.** Does NYCDOT hold the 1980s–1990s rehabilitation contract drawings for both bridges in a form releasable under FOIL, and what is the fee schedule? The single highest-value unknown in this document is an administrative one.

**Q41.** If a robotic maintenance or deposition system were proposed for an under-deck task on this structure, what geometric tolerance, surface coverage and localisation uncertainty would it actually require — and does any precedent robotic infrastructure intervention document the geometry it needed, or did it survey the work zone itself? Draft v1.0 asserted `LOD 350` from the BIMForum definition; §1.5 withdrew that, since LOD is a coordination vocabulary rather than a robotics requirement and onboard sensing may make prior geometry unnecessary. The open question is the requirement, not the LOD label.

---

## Part 10 — Methods

Continuing from Document 3, which ended at Method 14.

**Method 15 — FOIL request to NYCDOT for record and rehabilitation drawings, both bridges.**
Cost: a form and a fee. Value: potentially resolves Q32, Q33, Q36 and most of L2–L4 in a single step. This is the highest value-per-unit-effort action available anywhere in the programme and it has not been attempted. **Priority 1.**

**Method 16 — Walkway photogrammetric survey, Williamsburg Bridge, south walkway.**
Camera, tripod-free, one afternoon, no permission. Targets Q33 and Q39 specifically. Deliverable: an `SfM` reconstruction with a physically measured scale reference, published with its `RepresentedAccuracy` stated. Repeat on the Manhattan Bridge. **Priority 2.**

**Method 17 — Rephotogrammetry of the HAER photographic sets.**
Public-domain imagery, free software, one afternoon of compute. Likely to fail on baseline grounds; costs almost nothing to establish that. **Priority 4.**

**Method 18 — Approach NYCDOT regarding instrument deployment on the existing traveling maintenance platforms.**
Uses equipment the owner already operates. The cheapest conceivable route to underside geometry. Requires a relationship this programme does not yet have, which is itself a reason to start it. **Priority 2.**

**Method 19 — Build the provenance-tagged L1 model and publish it.**
2017 LiDAR plus NYC 3D Model plus OpenStreetMap, assembled in QGIS and CloudCompare, exported as `IFC` with `Pset_ResearchProvenance` populated, delivered as glTF. Achievable now with existing public data. Establishes the schema in a working artifact rather than a proposal. **Priority 3.**

**Method 20 — Negative-result literature search on provenance-tagged infrastructure models.**
Targets Q38 directly and disciplines the novelty claim in §5.3, which is currently asserted from an absence of search results rather than from a search for absence. **Priority 3.**

---

## Part 11 — Where this document is likely to be wrong

Stated by the author, before a reviewer has to. **Draft v1.1 note:** v1.0 was submitted to an adversarial review that returned *not fit to publish* with six blocking issues. All six are incorporated in the body above, with the original wording quoted in place. Items 9 through 14 below record them; items 1 to 8 were self-declared in v1.0 and are retained, with items 1 and 2 now superseded by corrections in the text.

**1. The `LOD 350` requirement for robotics in §1.5 was reasoned, not sourced — and is now withdrawn.** See item 11. Q41 remains open in a narrower form: what geometric tolerance, coverage and localisation uncertainty does a specific under-deck task actually require?

**2. The novelty claim in §5.3 rested on not having found prior art — and is now withdrawn.** v1.0 flagged this as a weakness and then made the claim anyway, which is the wrong order. Method 20 must precede any novelty statement, not follow it.

**3. Two of the three heritage-BIM citations are `SNIPPET`.** This document argues at length that abstract-level reading is the root cause of every error in the programme so far, and then cites Banfi 2017 and Brumana et al. 2019 from search results. The inconsistency is noted rather than excused. Both are open-access ISPRS Archives papers and both should be read before Part 5 is published outside this repository.

**4. The IFC 4.3 / ISO 16739-1 status is `SNIPPET` at rubric 3/5.** The claim that IFC 4.3 covers bridges is well attested across multiple secondary sources, but the exact ISO edition and its date were not confirmed against buildingSMART directly. A proposal that cites a standard should cite the standard.

**5. The reference implementation's provenance assignments are the author's judgement and have not been independently reviewed.** Someone with structural engineering knowledge of riveted lattice trusses may reasonably reclassify components in either direction. The schema is the contribution; the specific assignments are a first pass — and v1.1 reclassified eight of them after review, which is evidence for how soft they are.

**6. The occlusion argument may be too strong for the approach spans.** It is stated for the suspended spans, where the deck is high above water. Over land in DUMBO, an aerial survey with oblique imagery may capture more of the approach viaduct underside than §3.1 allows. Given the Rutgers observation that "many of the problems these days are actually on the approach spans," this is not a minor caveat — it may mean the most acoustically relevant structure is also the most photographable. It was not checked.

**7. No cost figures appear anywhere in this document.** Same weakness as Document 2. "One afternoon" is not a budget and a FOIL fee schedule was not retrieved.

**8. The framework has been demonstrated at the scale of a 2D schematic, not a 3D model.** Everything in Part 5 is designed to be schema-level and format-agnostic, and `Pset_ResearchProvenance` is expressible in `IFC` — but it has not been round-tripped through IfcOpenShell, and the claim that it survives an `IFC` export is untested.

**9. The programme's signature error appeared again, in the document written to prevent it.** §1.2 of v1.0 compared an 8.3–11.6 dB(A) change in **bridge-radiated** noise against a 3–5 dB(A) claim about **total** noise and concluded "the cross-section is worth more decibels than the fasteners." A decibel of a component is not a decibel of a total. On the source's own numbers, eliminating bridge radiation entirely would have moved the total by about 0.4 dB. The correction is in §1.2; the pattern — a number lifted out of the scope in which it was measured — is the fifth instance in this repository and is the reason `IDEA-CONCEPT.md` Method 1 is now treated as a prerequisite rather than an option.

**10. "The fastener's dynamic stiffness *is* the boundary condition" was wrong terminology.** A fastener is a coupling element; boundary conditions are supports, bearings, connections and domain truncation. Corrected in §1.4, which now also concedes the more damaging point: geometry of any resolution cannot supply dynamic stiffness, damping or preload, so no level of geometric detail alone makes this model an acoustic input.

**11. The LOD-as-maturity-ladder argument in §1.5 was doubly wrong.** "Two levels of development" treats `LOD` as sequential when BIMForum states explicitly that `LOD 500` is not higher than `400`; and "the first obstacle to the robotic-maintenance thesis" was asserted without comparison against actuation, power, certification, access or labour agreements, several of which are plainly harder. A robot can also work from task-specific survey or onboard sensing without any prior model. Both sentences are withdrawn and the claim is narrowed to a planning and procurement blocker.

**12. Part 5 presented a gap in `LOA` that is not a gap in `LOA`.** `LOA` is a metric-accuracy framework; an unmeasured element correctly has a null accuracy, not a missing low rung. v1.0 called this "a defect discovered in LOA" and proposed a "third accuracy axis," both of which misread the standard's scope. v1.1 reframes provenance as complementary lineage metadata alongside `LOA`, not an extension of it, and retitles Part 5.

**13. The reference implementation violated this document's own schema.** `section-problem.html` v1.0 carried a single `state` field taking `verified`/`inferred`/`assumed` — conflating `VerificationState`, which is about how deeply a source was read, with `GeometryProvenance`, which is about what supports a drawn shape. Eight components were marked "verified" on sources that establish only that the element exists. The truss envelope does not verify member coordinates; "the central section" does not verify a track offset; "four cables" does not verify a transverse position; the CAIT article does not locate a rail joint, and its instrumented tests were on the Manhattan side while the marker sat on a Brooklyn-side track. The artifact also asserted the Williamsburg trackform is "unballasted" as fact, which Document 3 Part 9 item 3 records as an unresolved inference. **All corrected.** The corrected tally is the more useful result: of 27 components, **0 measured, 0 documented, 23 inferred, 4 assumed** — not one element of either section is drawn where any source places it.

**14. The tally sentence was arithmetically defensible and semantically wrong.** "9 of 14 components are placed by reasoning" counted only the `ASSUMED` ones, when `INFERRED` components are also placed by reasoning. On the corrected schema the figure for the Manhattan Bridge is 14 of 14.

**15. Not yet fixed: the material and interface register does not exist.** §1.4 establishes that dynamic stiffness, damping and preload are as important as geometry and are not obtainable from it. This document specifies a provenance schema for geometry and nothing equivalent for material properties, and the programme currently holds no value, no source and no rubric for a single one of them. That is a larger hole than any of the fourteen above and it is the natural subject of the next document.

---

## Part 12 — Sources

### 12.1 Verified, full text read

| Source | Rubric | Contributes |
|---|---|---|
| Li, Dai, Zhu, Thompson — *Comparison of vibration and noise characteristics of urban rail transit bridges with box-girder and U-shaped sections*, Applied Acoustics 186 (2022) 108494 | 5/5 | The 8.3–11.6 dB(A) section-geometry sensitivity; the coupled track-bridge to vibro-acoustic FE method; the fastener as power-input interface; the rail-dominance caveat |
| BIMForum, *Level of Development Specification 2024, Part I* | 4/5 | `LOD 100`–`LOD 500` definitions; the `LOD 500` per-element accuracy requirement; the pointer to USIBD `LOA` |
| USIBD, *Level of Accuracy Specification Guide*, Document C120 v2.0 (2016) | 4/5 | `LOA10`–`LOA50` tolerance ranges at 95% confidence; Measured versus Represented Accuracy; the Heritage framework; DIN 18710 and UniFormat lineage |
| NYPD Unmanned Aircraft Permit Application Portal, official FAQ, and 38 RCNY 24 | 5/5 | The NYC UAS permission stack; NYC Admin Code § 10-126(c); 30-day lead time; Part 107, insurance and FAA prerequisites |
| Library of Congress HAER collection API, surveys `ny0980`, `ny1263`, `ny1234` | 5/5 | The measured-drawing negative result for both subway-carrying bridges |
| Haight and Patel, *Reconstruction of the Williamsburg Bridge*, AISC 2005 | 5/5 | Section element names; the 67 ft by 40 ft stiffening truss; the traveling maintenance platforms; the barrier-free footwalk system |
| Rutgers CAIT and NYCDOT, Manhattan Bridge instrumentation, 2021 | 3/5 | Bolted joints exist and are classified fair, poor, severe; roughly double the vibration at severe splices; approach spans named as the current problem |

### 12.2 Snippet only — retrieval priority

1. **Banfi (2017), ISPRS Archives XLII-2/W5, 57–64** — `GOG`, `GOI`, `GOA`. Open access. Read before publishing Part 5.
2. **Brumana, Banfi, Cantini, Previtali, Della Torre (2019), ISPRS Archives XLII-2/W11, 293** — HBIM level of detail, geometry, accuracy. Open access. Same.
3. **buildingSMART, IFC 4.3 and the ISO 16739-1 series** — confirm edition and date directly.
4. **FHWA, HIF-16-011, *Bridge Information Model Standardization*, Volumes I and II** — the American authority for infrastructure BIM standardisation.
5. **Cloud2BIM, arXiv 2503.11498** — read the assumptions before assuming it applies to a truss.
6. **UAS bridge-inspection accuracy literature** — several reviews located, none read to conclusions. Relevant only if Method 18 and Method 16 both fail.

### 12.3 Explicitly not found

- Any measured drawing, section or general arrangement of either the Manhattan or Williamsburg Bridge in any public collection.
- Any published 3D model of either bridge below deck level.
- Any provenance-tagged or reliability-tagged model of transport infrastructure published for public review. This is an absence of search results, not a verified negative — see Part 11 items 2 and 3, and Method 20. **No claim of novelty rests on it.**
- Any statement of the rail fastening specification for either bridge.
- Any cost figure for bridge documentation work in New York City.
- Verified OpenStreetMap geometry for either bridge. The Overpass API returned HTTP 406 without a user agent and then 504 gateway timeouts from `overpass-api.de` and `overpass.kumi.systems` during this review. Recorded as a tooling failure, not a data absence.

---

## Provenance

This document was produced in August 2026 as the fourth output of an Ethical Tech CoLab research programme on rail noise in DUMBO, Brooklyn. It reports no measurements, no survey and no model. Every geometric statement about either bridge is sourced to a document, and where no document exists that is stated rather than filled in.

Eight claims carry the weight of the argument and each is recorded with its locus in Part 12:

1. Changing only the transverse section geometry of an elevated rail bridge moved **structure-radiated** noise by 8.3 to 11.6 dB(A) in a validated vibro-acoustic model — Li, Dai, Zhu and Thompson, Applied Acoustics 186 (2022), conclusions, `VERIFIED`. The result is for concrete girders, does not transfer numerically to steel, and is a **component** figure that must not be compared against total-noise figures; §1.2 and §1.3.
2. The rail fastener is the interface through which power enters the bridge in that model class — same source, method statement, `VERIFIED`. It is a coupling element, not a boundary condition, and its dynamic properties are not obtainable from geometry; §1.4.
3. `LOD 500` already requires that a level of accuracy be noted or attached to each model element, and `LOD 500` is explicitly *not* a higher level than `LOD 400` — BIMForum LOD Specification 2024 Part I, `VERIFIED`.
4. `LOA` separates Measured from Represented Accuracy and is scoped to captured data — USIBD C120 v2.0, `VERIFIED`. §5.2 proposes complementary lineage metadata alongside it and no longer characterises the absence of an unmeasured category as a defect.
5. Neither the Manhattan nor the Williamsburg Bridge has measured drawings in HAER; the Brooklyn Bridge has one sheet — Library of Congress collection API, `VERIFIED` by direct query.
6. The only stated transverse dimensions available for either bridge are the Williamsburg Bridge's 67 ft stiffening truss width and approximately 40 ft depth — Haight and Patel, AISC 2005, `VERIFIED`. Both describe the envelope; neither locates any element within the section.
7. UAS operation in New York City requires an NYPD permit under 38 RCNY 24 with 30 days' notice, a Part 107 certificate, insurance and FAA authorisation — NYPD permit portal FAQ, `VERIFIED`.
8. Reliability tagging of model elements is established practice in heritage BIM — Banfi 2017 and Brumana et al. 2019, both `SNIPPET`. This is the weakest of the eight. **No novelty claim now rests on it**, because v1.1 withdrew the claim that the mechanism has not been applied to transport infrastructure; see Part 11 items 2 and 3, and Method 20.

**Claims withdrawn between v1.0 and v1.1.** All are quoted in place in the body rather than deleted, and all are restated in Part 11.

| # | Withdrawn claim | Where | Why |
|---|---|---|---|
| 1 | "The cross-section is worth more decibels than the fasteners" | §1.2 | Compares a bridge-only component figure against a total-noise figure; on the source's own numbers eliminating bridge radiation entirely moves the total ~0.4 dB |
| 2 | The fastener's dynamic stiffness "*is* the boundary condition" | §1.4 | A fastener is a coupling element; boundary conditions are supports, bearings, connections and truncation |
| 3 | Reaching a geometric level of detail makes the model an acoustic input | §1.4, §1.5 | Geometry cannot supply dynamic stiffness, damping or preload |
| 4 | "The geometry gap precedes the robotics question by two levels of development" | §1.5 | BIMForum states `LOD 500` is not higher than `400`; LOD is not a maturity ladder |
| 5 | Geometry is "the first obstacle" to robotic maintenance | §1.5 | Asserted without comparison against actuation, power, certification, access or labour agreements |
| 6 | `LOA` has a defect: "no rung for unmeasured geometry" | §5.2, Part 5 title | `LOA` is scoped to captured data; unmeasured is correctly null, not a low rung |
| 7 | Provenance as "a third accuracy axis" | Part 5 title, §5.3 | It is not an accuracy axis; it is lineage metadata carried alongside accuracy |
| 8 | The mechanism "has not been applied to transport infrastructure acoustics" | §5.3 | Two of three prior-art sources are `SNIPPET` and the negative search is filed as future work |
| 9 | "8 `VERIFIED`, 10 `INFERRED`, 9 `ASSUMED`" and "9 of 14 placed by reasoning" | Part 8, artifact | Conflated two schema fields into one, and undercounted reasoning by excluding `INFERRED` |
| 10 | HAER photographs are "calibrated" | artifact | No camera calibration data accompanies them |
| 11 | Level-of-detail availability as percentages (100/85/35/8/0 %) | artifact | Fabricated precision with no denominator; replaced with an auditable count at each rung |
| 12 | The Williamsburg trackform is "unballasted", stated as fact | artifact | An inference from element names; Document 3 Part 9 item 3 records it as unresolved |

**Review note.** Draft v1.0 was submitted to an adversarial review that returned *not fit to publish* with six blocking issues. The most damaging finding is recorded as Part 11 item 9: **this document, written specifically to stop unsupported numbers travelling further than their evidence, contained an unsupported number of exactly the kind it was written to stop.** The correction is not a patch. It changes the programme's priority order, promoting instrumented source apportionment from a useful investigation to a prerequisite for any design-build proposal.

The reference implementation is `visual-review/section-problem.html`. It is schematic, not to scale, computes no acoustics, and should not be used for engineering purposes. Its component classifications were reworked in v1.1 after the review found it violating the schema defined in Part 5 of its own accompanying document.

Released under CC BY 4.0. Corrections, and particularly reclassifications of any component's provenance state, are welcome as repository issues.
