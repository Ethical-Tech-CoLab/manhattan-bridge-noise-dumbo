# Community Evidence Audit

**What the people who live under it have already recorded, said and filed — and why almost none of it is in a form anyone can measure**

Document 6 of the DUMBO rail-noise research programme.
Version 1.0. Questions Q42–Q50. Methods 21–25.

---

## Part 0 — The question, and the answer

### 0.1 What was asked

> Look carefully at Reddit and other local resident resources where someone may have crowd-sourced recordings of train noise while in the Brooklyn Bridge Park under the Manhattan Bridge.

The premise is a good one. [`FIELD-CAPTURE-PROTOCOL.md`](FIELD-CAPTURE-PROTOCOL.md) argues that four properties of this soundscape survive an uncalibrated recording chain — **spectral shape, temporal envelope, headway distribution and train attribution** — because each is either a *ratio* or a *timestamp*, and an unknown fixed gain cancels out of a ratio and does not touch a timestamp. If that argument is right, then somebody's phone video, shot for entirely unrelated reasons, is a partial substitute for captures C1, C2 and C3 at zero cost and zero delay.

So the search was worth running.

### 0.2 What was found

**No public, locatable, crowd-sourced audio recording of the Manhattan Bridge train pass-by, made in Brooklyn Bridge Park or anywhere else in DUMBO, exists in any repository this search could reach.** Not on Reddit, not on Freesound, not in the NYU sensor-network corpus, not in any municipal dataset. Consumer video exists in quantity, but none of it is indexed, described or licensed in a way that makes it findable *as an acoustic record* rather than as a picture of a bridge.

That is a negative result, and this programme registered [Method 20](README.md) — a deliberate negative-result search — precisely because absence of evidence is a finding rather than a failure.

**But the interesting part is not the absence. It is the reason for the absence.**

### 0.3 The finding

> **Three independent instruments for recording urban noise in New York City — the city's complaint system, the city's flagship acoustic research corpus, and the city's noise code — each contain no category for rail.**
>
> The absence is not a coincidence of three organisations. It is one absence, inherited three times, because the second and third were both built from the first.

Rail noise in New York City is not under-reported. It is **unreportable**. A resident standing in Brooklyn Bridge Park under a train measured by the MTA itself at **87.50 dB(A) equivalent level and 98.90 dB(A) maximum** cannot file a complaint that names what they are hearing, because the complaint form has no box for it. A machine-listening model trained on 18,510 annotated clips from a 55-sensor citywide network cannot label the sound, because the label does not exist in the taxonomy. And the taxonomy does not contain it because — in the authors' own words — it was constructed "through consultation with the New York Department of Environmental Protection **and the New York noise code**."

This is the same shape as the finding already recorded in [`IDEA-CONCEPT.md`](IDEA-CONCEPT.md): the MTA's own governing statute, Public Authorities Law § 1204-a, has a category for elevated structures and **no standard in it**. That was one blank cell in one statute. This document establishes that the blank cell propagated.

**Four instruments. Same gap. One of them is the reason for the other three.**

### 0.4 Why this matters more than a recording would have

A found recording would have been useful. This is more useful, for a reason specific to how this programme argues.

Every document here has had to explain why a problem this loud has produced so little documentation. The available explanations were unsatisfying — institutional inattention, jurisdictional buck-passing, the general difficulty of measuring things. Those are motives, and motives are weak evidence.

This is a **mechanism**. It is specific, it is verifiable, and it makes a prediction that can be checked: if the taxonomy is the constraint, then complaint volume about elevated rail should be near zero *everywhere in the city*, including under the elevated lines in Queens, Brooklyn and the Bronx where hundreds of thousands of people live — and it should be near zero *regardless of how bad the noise is*, because the variable being measured is the form, not the phenomenon.

That is testable. See **Method 21**.

### 0.5 Source ratings used here

Same scale as the rest of the programme. Credibility **1** (an anonymous forum post) to **5** (a primary agency document, a primary dataset queried directly, or a peer-reviewed measurement). Depth of reading marked **VERIFIED** (read in full, or in the case of a dataset, queried directly by this programme), **SNIPPET** (search extract only) or **UNVERIFIED**.

**Two claims in this document are rated 5/5 `VERIFIED` on the strength of queries this programme ran itself** against the NYC Open Data Socrata API. The queries are printed in full in Part 2 so that anyone can re-run them and get the same answer, or a different one. That is a stronger warrant than this programme usually has, and it is confined to Part 2. Everything in Part 3 is weaker and is rated accordingly.

**One claim is deliberately left as an open question rather than asserted.** The legal mechanism in Part 2.4 — why the noise code omits rail — is the kind of claim that requires a lawyer reading primary statute, and this programme is not that. It is written as Q42, not as a finding.

---

## Part 1 — Method

### 1.1 What was searched

Fourteen searches through the Tavily API, plus two direct queries against the NYC Open Data Socrata endpoint, plus direct content extraction from nine pages.

| Channel | Searched | Result |
|---|---|---|
| Reddit | Domain-restricted search, plus the direct JSON API | Threads exist; **no recordings**. See 1.3 for a caveat about access. |
| Freesound.org | Tag and text search for NYC subway, elevated, Manhattan Bridge | Subway interiors and generic NYC transit only. Nothing located under the Manhattan Bridge. |
| SONYC / NYU acoustic sensor network | Project pages, both dataset papers, the Zooniverse citizen-science portal | 150M+ clips exist. **No rail class in the taxonomy.** Part 2.3. |
| NYC Open Data 311 | Socrata API, queried directly, citywide and geographically | **No rail complaint category exists.** Part 2.2. |
| NYC DEP education programme | The Sound and Noise Education Module and its ArcGIS StoryMap | A real 12-site citizen-science dataset **in the wrong end of the park.** Part 3.1. |
| Local press | Brooklyn Paper, Brooklyn Bridge Parents, Brownstoner, Patch | Substantial resident testimony, 2008 to 2025. Part 3.2. |
| Petitions | Change.org | Three relevant petitions, one specific to this bridge. Part 3.3. |
| Social video | Instagram, YouTube, travel blogs | Uncalibrated dB claims and one useful qualitative observation. Part 3.4. |
| Community governance | Brooklyn Community Board 2, DUMBO Neighborhood Alliance, DUMBO Action Committee | Named actors identified; minutes not retrieved. Method 24. |

### 1.2 What "found" would have meant

A recording counts as usable to this programme if it is (a) publicly retrievable, (b) locatable to a receptor position with better than about 50 m confidence, (c) long enough to contain at least one complete pass-by including both tails, and (d) accompanied by enough description to establish that the loud thing in it is a train rather than a truck, a boat or the wind.

**Nothing found meets all four.** Several items meet (a) and (d). None meets (c) with any confidence, because none is described as a recording at all — they are videos of a view, which happen to have a train in them.

### 1.3 A limitation to state at the top

**Reddit was not fully searched, and this document should not be read as having cleared it.**

Direct programmatic access returned HTTP 403, and the interactive fetch returned an interstitial verification page. Reddit's public JSON endpoints now reject unauthenticated automated requests. What was searched was Tavily's index *of* Reddit, which is a snapshot of what a crawler saw, not the live site, and it does not include comment trees — which is exactly where a link to a recording would be posted.

So the honest statement is: **no recording surfaced through a search of Reddit's indexed post titles and bodies.** A human being logged in, reading comment threads in r/AskNYC, r/Brooklyn, r/nyc and r/NYCapartments, might well find one. That is **Method 23**, and it is cheap.

The threads that did surface are consistent in tone and content — see Part 3.2 — but none contains a recording, and this programme has not read their comments.

---

## Part 2 — The structural finding

### 2.1 What is claimed

Three claims, in descending order of how well this programme can support them:

1. **NYC 311 has no complaint category for rail or subway noise, citywide.** Rated **5/5 `VERIFIED`** — queried directly, query printed below.
2. **The SONYC urban sound taxonomy has no rail class**, and its authors state it was built from the NYC DEP and the New York noise code. Rated **4/5 `VERIFIED`** for the taxonomy, **5/5 `VERIFIED`** for the quoted derivation.
3. **The reason both are true is that the NYC Noise Code does not reach the MTA.** Rated **2/5 `UNVERIFIED`** and written as **Q42**, not as a finding.

### 2.2 NYC 311 — the query and the answer

The 311 Service Requests dataset is the city's primary record of what New Yorkers complain about. It is the dataset that gets cited when anyone says noise is New York's number one quality-of-life complaint.

**Query 1 — what noise categories exist in DUMBO's ZIP code.**

```
https://data.cityofnewyork.us/resource/erm2-nwe9.json
  ?$select=complaint_type,count(unique_key)
  &$where=incident_zip='11201'
      and complaint_type like 'Noise%'
      and created_date>'2020-01-01T00:00:00'
  &$group=complaint_type
  &$order=count_unique_key DESC
```

| Complaint type | Count, ZIP 11201, since 2020 |
|---|---|
| Noise - Residential | 25,545 |
| Noise | 8,113 |
| Noise - Street/Sidewalk | 7,989 |
| **Noise - Helicopter** | **4,990** |
| Noise - Vehicle | 3,659 |
| Noise - Commercial | 3,346 |
| Noise - Park | 285 |
| Noise - House of Worship | 24 |

**Helicopters have their own category. Houses of worship have their own category. Rail does not appear.**

The generic `Noise` bucket does not rescue it. Its descriptors, same ZIP and period, are: construction before/after hours (3,893), construction equipment (1,237), air conditioning and ventilation (698), barking dog (696), jackhammering (502), alarms (473), **ice cream truck (180)**, lawn care equipment (175), private carting (151), manufacturing (54), boat engine or music (22), other animals (9), and "other noise sources, use comments" (4).

**There is a descriptor for ice cream trucks and a descriptor for other animals. There is none for trains.**

**Query 2 — is this a Brooklyn artefact, or is it citywide?**

```
https://data.cityofnewyork.us/resource/erm2-nwe9.json
  ?$select=complaint_type,descriptor,count(unique_key)
  &$where=created_date>'2020-01-01T00:00:00'
      and (upper(descriptor) like '%SUBWAY%'
        or upper(descriptor) like '%TRAIN%'
        or upper(descriptor) like '%RAIL%'
        or upper(complaint_type) like '%SUBWAY%'
        or upper(complaint_type) like '%TRAIN%')
  &$group=complaint_type,descriptor
  &$order=count_unique_key DESC
```

Citywide, all complaint types, since 2020, every category whose name contains "subway", "train" or "rail":

| Complaint type | Descriptor | Count |
|---|---|---|
| Illegal Parking | Detached Trailer | 9,571 |
| General Construction/Plumbing | Safety Netting/Guard Rails — Damaged/Inadequate/None (6 storeys or less) | 1,175 |
| Street Condition | Guard Rail — Street | 812 |
| BEST/Site Safety | Safety Netting/Guard Rails — Damaged/Inadequate/None (over 6 storeys) | 679 |
| Highway Condition | Guard Rail — Highway | 173 |
| Sewer | Damage Structure/Railing | 61 |
| Bridge Condition | Guard Rail — Bridge | 56 |
| Street Condition | Guide Rail | 1 |

**Every match is a guard rail or a trailer.** There is no rail-transit category anywhere in the New York City 311 taxonomy, for any complaint type, citywide.

**Query 3 — the geography that makes it concrete.**

Within a 500 m circle centred on the Brooklyn Bridge Park Main Street section and the Manhattan Bridge Brooklyn anchorage — a circle that contains the dog run where the MTA measured **87.50 dB(A) Leq** and **98.90 dB(A) Lmax**, and the DUMBO Archway where it measured **81.33** and **91.80** — there have been **4,055 noise complaints since 2020**.

The top categories are loud music and parties (720 on streets, 395 commercial, 369 residential), engine idling (588), construction (261), car and truck music (220), banging and pounding (190), loud talking (169), helicopters (133), **ice cream trucks (117)**, and **barking dogs (95)**.

> **In the 500 m around the loudest measurement in this entire research programme, four thousand and fifty-five noise complaints have been filed since 2020, and not one of them can be about the train.**
>
> **The dog run generated 95 complaints about barking dogs. The MTA measured 98.90 dB(A) peaks from trains at that same dog run. The dogs are complainable. The trains are not.**

*Query rated 5/5 `VERIFIED`. Run 2026 against the live Socrata endpoint. Counts will drift as the dataset grows; the presence or absence of a category will not.*

**A caveat that must travel with this.** The absence of a category does not mean no resident ever complained about a train. It means that when they did, the complaint was either refused, or absorbed into a category that misdescribes it, or — most likely — routed to the MTA's own customer channels, which are not public data. The MTA's own § 1204-a report was triggered by a letter from an elected official's office, not by a 311 record, and the report itself states the office "has been in contact with the MTA New York City Transit (NYCT) since 2022." **The complaints exist. The public record of them does not.** Where they went instead is **Method 22**.

### 2.3 SONYC — the same gap, inherited

Sounds of New York City is the most serious attempt anyone has made to measure this city's noise continuously and at scale. It is an NYU-led, NSF-funded project with collaborators at Ohio State, it has deployed **more than 55 low-cost acoustic sensor nodes** across Manhattan, Brooklyn and Queens, and it has recorded **more than 150 million 10-second audio clips since 2016**.

It is exactly the resource the user's question was reaching for: a genuine, large, public, citizen-annotated corpus of New York City sound, with volunteers from the Zooniverse platform doing the labelling.

**Its taxonomy has eight coarse classes and twenty-three fine classes. None of them is rail.**

The eight coarse classes, from the published baseline results table:

| # | Coarse class |
|---|---|
| 1 | engine |
| 2 | machinery-impact |
| 3 | non-machinery-impact |
| 4 | powered-saw |
| 5 | alert-signal |
| 6 | music |
| 7 | human-voice |
| 8 | dog |

*Rated 4/5 `VERIFIED` — read from the DCASE 2020 SONYC-UST-V2 paper (Cartwright et al.) and cross-checked against the DCASE 2019 challenge results and the project's own baseline repository, which list the identical eight.*

And the derivation, quoted exactly from the SONYC-UST v1 paper (Cartwright et al., 2019):

> "Through consultation with the New York Department of Environmental Protection (DEP) and the New York noise code, we constructed a small, two-level urban sound taxonomy [...] consisting of 8 coarse-level and 23 fine-level sound categories, e.g., the coarse `alert signals` category contains four fine-level categories: `reverse beeper`, `car alarm`, `car horn`, `siren`."

And, two sentences later, the mechanism stated outright:

> "**The chosen sound categories map to categories of interest in the noise code**; they were limited to those that seem likely discernible by novice annotators; and we kept the number of categories small enough so that they can all be visible at once in an annotation interface."

*Both rated 5/5 `VERIFIED` — the paper was extracted and these passages read directly.*

**This is the transmission mechanism, stated by the authors themselves.** The researchers did the responsible thing — they aligned their labels to the city's own regulatory categories so that their output would be actionable by the agency that enforces them. They say so explicitly, and they were right to. The consequence is that the corpus inherited the code's blind spot. A sensor placed in DUMBO would record the trains faithfully at 10-second resolution, forever, and every clip would be annotated as `engine`, or as `machinery-impact`, or as nothing at all.

**The same paper independently corroborates the 311 finding**, in its own account of what the noise code covers:

> "For example, jackhammers can only operate on weekdays; pet owners are held accountable for their animals' noises; ice cream trucks may only play their jingles while in motion; blasting a car horn is restricted to situations of imminent danger."

Jackhammers, pets, ice cream trucks, car horns. Those are — exactly, and in the same order of prominence — four of the 311 descriptors tabulated in 2.2: *Noise: Jack Hammering (NC2)*, *Noise, Barking Dog (NR5)*, *Noise, Ice Cream Truck (NR4)*, *Car/Truck Horn*. **The chain from noise code to complaint form to research taxonomy is visible in the vocabulary itself.**

### 2.3.1 The bias SONYC set out to fix, and the deeper one it inherited

SONYC's own stated motivation makes the finding sharper. From the same paper:

> "After a city resident complains about noise, the New York City Department of Environmental Protection (DEP) sends an inspector to investigate the complaint. [...] **Unfortunately, this complaint-driven enforcement approach results in a mitigation response biased to neighborhoods who complain the most, not necessarily the areas in which noise causes the most harm.**"

That is an excellent diagnosis and the project was built to correct it — replace complaint-driven attention with continuous sensing, so that noise gets measured where it is worst rather than where people are loudest about it.

> **But the correction only reaches sources the taxonomy can name.**
>
> **SONYC set out to remove the bias toward neighbourhoods that complain, and inherited a deeper bias toward sources that *can be* complained about. For a source with no category, continuous sensing produces exactly as much evidence as the complaint system did: none.**

This is not a criticism of SONYC, which is a serious project that made its derivation explicit in print — which is the only reason this finding is available at all. It is an observation about what happens when a measurement system is aligned to an enforcement schema: **it inherits the schema's silences along with its priorities.**

Two further observations, both rated **3/5** and both flagged as inference rather than finding:

- **Sensor placement.** The papers state sensors are in Manhattan, Brooklyn and Queens with "the highest concentration around New York University's Manhattan campus." Whether any sensor was ever within earshot of an elevated structure is not established here and is **Method 25**. The spatial metadata is quantised to a city block and released, so this is answerable from the public dataset without contacting anyone.
- **The audio may still be there.** 150 million clips is a very large number and the sensors ran continuously. If any node was within range of an elevated line, the *sound* of elevated rail is almost certainly in the corpus. It is simply **unfindable by label**, which for a dataset of that size is operationally the same as not existing — unless someone searches it by acoustic similarity instead. That is a real, tractable, and rather interesting piece of work, and it is **Method 25**.

**On inter-annotator agreement.** The V2 paper reports Krippendorff's alpha of **0.36** for the crowdsourced annotations, which the authors themselves call "rather low," attributing it to distant events with poor signal-to-noise and the difficulty of disambiguating sounds without visual confirmation. This is relevant beyond SONYC: it is a quantified estimate of how unreliable crowd annotation of urban sound is even when the annotators are motivated volunteers working from a fixed taxonomy. It is a reason to be sceptical of *any* crowd-sourced acoustic claim, including the ones inventoried in Part 3.

### 2.4 The mechanism — stated as a question, not a finding

Why does the New York City Noise Code not reach elevated rail?

The apparent answer has two independent limbs, and **this programme cannot responsibly assert either**:

- **The MTA is a New York State public benefit corporation, not a city agency**, and the general position is that city ordinances do not bind state authorities in the exercise of their statutory functions. This is why § 1204-a exists at all: the State legislature had to write the MTA its own noise statute, because the city's did not apply. The blank cell for elevated structures in that statute is documented in [`IDEA-CONCEPT.md`](IDEA-CONCEPT.md).
- **Federal preemption under the Noise Control Act of 1972** removes rail noise from state and local control — but the implementing regulation, **40 CFR Part 201**, is titled *Noise Emission Standards for Transportation Equipment; **Interstate Rail Carriers***. A rapid transit system operating wholly within one state is not obviously an interstate rail carrier. So preemption may not apply, which would mean the gap is not federally required but merely inherited.

If the second limb is right, the position is worse than "nobody is allowed to regulate this." It is **"somebody could, and nobody has."**

That distinction decides whether this programme's eventual recommendation is a request for a federal waiver or a request that the city amend a form. Those are wildly different asks. **Q42** and **Method 24**.

*Rated 2/5 `UNVERIFIED`. Assembled from secondary summaries and the title of one federal regulation. No primary statute was read in full. A reader with legal training should assume this paragraph is wrong until they have checked it, and this programme would like to be told.*

---

## Part 3 — What does exist: the inventory

Nothing here is a usable recording. All of it is evidence of something.

### 3.1 The NYC DEP citizen-science dataset — right park, wrong end

**This is the single most important item in the inventory, and the most dangerous.**

The NYC Department of Environmental Protection runs a **Sound and Noise Education Module** with a published lesson, "Conducting a Case Study: Brooklyn Bridge Park," backed by an ArcGIS StoryMap containing a real, geolocated, twelve-site noise dataset collected in Brooklyn Bridge Park.

| Property | Value |
|---|---|
| Publisher | NYC Department of Environmental Protection, Education Office |
| Published | 24 August 2022 |
| Data collected | **19 July 2019, 12:00–13:00** |
| Sites | **12**, around Pier 3 and Pier 4 |
| Instrument | **Arduino Science Journal** (a phone app) |
| Mean outside berm | **52 dB** |
| Mean inside berm | **48 dB** |
| Range outside berm | **48 to 65 dB** |
| Range inside berm | **41 to 54 dB** |

*Rated 4/5 `VERIFIED` — the StoryMap was extracted and read in full. Rated 4 rather than 5 because it is an education product rather than a measurement report: no instrument calibration, no weighting network, no averaging time, and no integration period are stated anywhere.*

**Why it is important:** it is proof that municipally-sanctioned, phone-based, citizen-collected acoustic data in Brooklyn Bridge Park already exists, is publishable, and is considered legitimate by the city's own environmental agency. Every objection this programme has raised about phone measurement, the DEP has already waved through in a lesson plan for schoolchildren. **That is a precedent worth having** when proposing Methods 11 and 21. It also happens to endorse the same two tools [`FIELD-CAPTURE-PROTOCOL.md`](FIELD-CAPTURE-PROTOCOL.md) discusses, noting that "while both applications can be used, the Arduino Science Journal is more student friendly, while the NIOSH application provides the most accurate data."

**Why it is dangerous:** it measures the wrong end of the park, and it does not say so in a way anyone would notice.

Brooklyn Bridge Park is **85 acres and roughly 1.3 miles long**. The DEP study sites are at **Pier 3 and Pier 4**, at the *southern* end, where the dominant source is the Brooklyn–Queens Expressway and the object of study is the sound-attenuation berm. The Manhattan Bridge crosses the *northern* end, about **a mile away**, past Piers 2 and 1, past the Fulton Ferry landing, past Jane's Carousel. The MTA's dog run measurement is in the Main Street section, at the far northern tip.

> **Two published, official, geolocated noise datasets both describe "Brooklyn Bridge Park."**
>
> **One says 48 to 52 dB. The other says 87.50 dB(A) Leq with 98.90 dB(A) peaks.**
>
> **They differ by about 35 dB — a factor of over three thousand in sound energy — and both are correct, because they are a mile apart and measuring different sources.**

Anyone who searches for noise data in Brooklyn Bridge Park will find the DEP StoryMap first. It is an official city product, it has a map, it has charts, it is written for a general audience, and it is optimised for search. The MTA memorandum is a scanned internal document numbered 138061. **The finding of record for this park, as far as the open web is concerned, is that it is a quiet place where a clever berm solved the noise problem.**

This is not a criticism of the DEP lesson, which is good and does what it set out to do. It is an observation about what happens when a park is treated as a unit of analysis and it is a mile long. **Q43.**

### 3.2 Resident testimony — an eighteen-year record

The strongest crowd-sourced material found is not acoustic. It is testimonial, and it is remarkably consistent across two decades.

**Brooklyn Paper, "Deaf in DUMBO," by Sarah Portlock, 2008.** Rated **3/5 `VERIFIED`** — local press, read in full, no methodology, but it quotes named officeholders on the record.

> "I've lost some hearing as a result [of working and living here]," said DUMBO Neighborhood Association President Karen Johnson, who used to live on Plymouth Street, hard by the Manhattan Bridge with its truck traffic and B, D, N, and Q trains.
>
> "I moved out of DUMBO because the noise was too much," she said.

**The president of the neighbourhood association moved out of the neighbourhood.** That is not a decibel level, and this programme should not pretend it is one. It is a datum of a different kind, and the same article supplies several more:

- A resident posted a copy of the Brooklyn Bridge Park environmental study in a grocery store window at Washington and Front Streets under the heading **"Deaf and DUMBO."** Resident-led dissemination of agency evidence, in 2008, by hand, in a shop window.
- **DumboNYC.com maintained a running list of contractors who could insulate apartments against the noise.** This is crowd-sourced mitigation: the community organised its own private, per-household, self-funded response, because no public one was available. Every double-glazed window in DUMBO is a privately financed noise barrier, and nobody has ever added up what they cost. **Q44.**
- Furniture maker Eric Manigan: the noise "rocks the whole neighborhood [...] There's a serious noise issue, especially in the summer when people want to sleep with their windows open. If the noise wakes you up one or two times a night, you're ragged."
- And the observation that matters most for the design brief, from then-DUMBO Improvement District Executive Director Kate Kerrigan, on the district's effort to reclaim the spaces under and around the bridge as public areas:

> "**the main problem is the cacophony**"

> **The noise is not merely a nuisance in the public space under the bridge. It is the binding constraint on creating public space under the bridge at all.**

That reframes the design problem. Mitigation is not only about relieving the people already there — it is about **how much unusable land it unlocks**, in one of the most valuable waterfront districts in the United States. That is a quantity an economist could estimate, and it is the argument most likely to move a capital budget. **Q45, Method 24.**

Kerrigan also supplies the acclimatisation observation, which recurs throughout this literature and bears directly on why the problem persists:

> "it's always interesting to hear other people's reactions to the noise, because when you're living or working down here you get used to it."

**Reddit threads.** Rated **1/5 `SNIPPET`** — titles and indexed excerpts only, comments not read, see 1.3.

- r/AskNYC, "Living next to Manhattan bridge — train noise" (2019) — a prospective tenant in Two Bridges, the Manhattan side of the same bridge, asking how bad it is.
- r/NYCapartments, "How bad is it to live next to the train tracks in Brooklyn?" — indexed excerpt: "No amount of soundproofing or insulation will really dampen the sound and if you work from home you'll constantly be apologizing about the [noise]."

These are worth **nothing** as measurement and are worth **something** as evidence that the question is asked repeatedly by people about to sign a lease. **This programme should not cite them for any physical claim.**

### 3.3 The petitions — residents converging on the engineering

Three Change.org petitions were located. One is specific to this bridge.

**"Reduce noise pollution in DUMBO from Manhattan Bridge train."** Started **16 November 2025** by Katy Gaul-Stigge. **98 verified signatures** as of this search. Addressed to the DUMBO Action Committee (Elizabeth Johnson) and the DUMBO Neighborhood Alliance (Doreen Gallo). Rated **3/5 `VERIFIED`** — read in full; a petition is self-reported and unrefereed, but it is a primary statement of resident position and the signature count is platform-verified.

The petition proposes five mitigations. They are listed here **exactly as written by the resident**:

| Resident's proposal | What the engineering literature calls it | Covered in |
|---|---|---|
| "Welding the tracks" | Continuous welded rail; elimination of joint impact | `PRECEDENT-AND-MATERIALS.md` |
| "Lubrication of the tracks" | Top-of-rail friction modifiers; gauge-face lubrication for curve squeal | `PRECEDENT-AND-MATERIALS.md` |
| "Rubber insulation on tracks and wheels" | Resilient fastenings, rail dampers, resilient wheels | `PRECEDENT-AND-MATERIALS.md` |
| "Insulation and covering below of the tracks (could also reduce hazards from falling from the tracks)" | Under-deck absorptive treatment and shrouding | `PRECEDENT-AND-MATERIALS.md`, Track A |
| "Use of lighter cars" | Unsprung mass reduction | `PRECEDENT-AND-MATERIALS.md` |

> **A resident with no stated engineering training, writing a petition, independently produced substantially the same intervention list that this programme assembled from the international elevated-transit literature.**

This is worth saying plainly for two reasons. First, it is a **check on the programme**: the design space is not exotic or contrarian, and an interested layperson reaches the same five levers. Second, it disposes of a familiar deflection. The community is not asking for the impossible, and it is not asking for the line to be closed. It is asking for **welded rail, lubrication, resilient components, under-deck treatment and lighter vehicles** — every one of which is standard practice somewhere in the world, and several of which the MTA already does elsewhere on its own system.

The parenthesis is worth noting too: *"could also reduce hazards from falling from the tracks."* The resident has independently identified that an under-deck treatment is also a debris-containment measure, which is a co-benefit that materially changes the cost case because it can be charged partly to a different budget line. That is a sophisticated observation and this programme had not made it. **Q46.**

**Two claims in the petition need correcting, and the corrections matter.**

**Claim 1: "passing every five minutes during peak hours."**

The MTA's own session data gives mean headways across all four tracks of **85.3 s at the DUMBO Archway, 87.1 s at the dog run, and 126.2 s at the Adams Street Library** — that is, roughly **1.4 to 2.1 minutes**. The resident's estimate is **two to three times too long**.

The resident is under-reporting the frequency of the thing they are complaining about. This is a mild but real finding about perception: what is recalled as an intermittent intrusion every five minutes is, by measurement, an event every ninety seconds. (A partial explanation: a resident may be counting only trains on one line, or in one direction, while the MTA counted every train on all four tracks. The perceptual point stands regardless.) **Q47.**

**Claim 2: "often exceeding OSHA safe noise levels of 90 decibels."**

The **OSHA permissible exposure limit of 90 dBA is an eight-hour time-weighted average** for occupational exposure, not an instantaneous ceiling. Peaks of 98.90 dB(A) lasting a few seconds every ninety seconds do not straightforwardly "exceed OSHA," and an unsympathetic reader will use that to dismiss the whole petition. **This programme should not repeat the claim in that form.**

But the reach for OSHA is itself the finding.

> **The resident reached for an occupational standard — written for paid workers, in an employment relationship, protected by a mandated hearing-conservation programme, who go home at the end of a shift — because there is no civilian standard that applies to a person sitting in a public park under a state authority's railway.**
>
> **The rhetorical reach for OSHA is direct evidence of the regulatory vacuum described in Part 2.4. They cited the wrong standard because the right one does not exist.**

That is the more interesting version of the observation, and it is more useful to the residents than a correction would be. **Q48.**

**Two further petitions**, both rated **2/5 `SNIPPET`**, not read in full:

- **"DUMBO Residents Demand a Follow-Up Town Hall, Accountability, and Change!"** — **508 verified signatures**, addressed to Governor Kathy Hochul and Senators Schumer and Gillibrand. Five times the signature count of the noise-specific petition, and escalated to the state and federal level. The relationship between this and the noise petition is not established. **Method 24.**
- **"SILENCE THE SCREECH! Demanding MTA Immediate Subway Track Lubrication Implementation (NYC)"** — citywide rather than DUMBO-specific, and notable because it isolates *one* of the five interventions as the immediate ask. Whether the MTA has responded to it anywhere is not established.

**And the corroborating institutional record.** The MTA's own § 1204-a report states that the elected official's office "has been in contact with the MTA New York City Transit (NYCT) since 2022." Combined with the 2008 Brooklyn Paper article and the 2025 petition, the documented complaint record runs **2008 → 2022 → 2023–24 measurements → November 2025 petition → 2026**. Rated **5/5 `VERIFIED`** for the MTA document, **3/5** for the chain.

**Eighteen years of continuous, documented, unresolved complaint.** During which the city's complaint system acquired a dedicated category for helicopters.

### 3.4 Social video and uncalibrated dB claims

**Instagram reel, `newyorklab.co`, video credited to Jack Klein, November 2025.** Indexed caption: *"Trains clock in at 80-90 decibels every time they pass over Dumbo on the [Manhattan Bridge]."* Rated **2/5 `SNIPPET`** — caption only, retrieved through search indexing; the video itself was not viewed and Instagram requires login.

The stated range of **80–90 dB** brackets the MTA's **81.33 dB(A)** at the DUMBO Archway and sits below the **87.50** at the dog run. That is an uncalibrated phone measurement by a member of the public landing in the same band as an agency instrument.

**This is weak corroboration and must be labelled as such.** The weighting, the averaging time, the app, the position and the gain are all unknown, and [`FIELD-CAPTURE-PROTOCOL.md`](FIELD-CAPTURE-PROTOCOL.md) Part 4 sets out at length why a phone SPL reading in the 80–99 dB regime is the least trustworthy thing a phone produces — the *Cureus* 2025 evaluation of ten free Android meter apps found specifically that "accuracy declined at higher noise levels." **The agreement is very likely a coincidence of two numbers in the same decade.** It is recorded because it is the only independent quantitative statement by a member of the public that this search found, and because it is a lead: the poster made a measurement, which means the poster has a recording.

**Travel blog, Rachel's Ruminations, "Walking across the Manhattan Bridge & the Brooklyn Bridge."** Rated **2/5 `VERIFIED`** — read in full. Contains video of a pass-by taken from the pedestrian walkway. Useless for level. But it contains one sentence that is worth more than its rating:

> "Walking across the Manhattan Bridge was a pleasant experience on a Saturday morning, except when subway trains passed. The video below gives you an idea of how loud they are. **What it can't show is that the whole structure shakes when they pass.**"

An untrained observer, unprompted, identified the exact limitation of consumer capture: **the structure-borne component does not record.**

That is not a small point. This programme's working physical model is that the bridge steel is itself a radiating surface — that the problem is not only wheel-rail noise propagating through air, but a 1909 structure being driven into vibration across a large area and re-radiating. **Every consumer recording ever made of this bridge is missing that entire limb of the phenomenon**, not because of gain or codec or AGC, but because a phone microphone in the air cannot capture what a hand on a railing can feel.

So even a perfect crowd-sourced recording would have been systematically incomplete in the one dimension this programme most needs. It is an argument for accelerometry — the S23+ has an accelerometer, and while it is a poor one, a **simultaneous accelerometer and audio recording placed in contact with bridge steel or a park railing** would establish whether the two are correlated at pass-by. That costs nothing and nobody appears to have done it. **Method 21b, folded into Method 21.**

---

## Part 4 — What this changes

### 4.1 For the field capture protocol

[`FIELD-CAPTURE-PROTOCOL.md`](FIELD-CAPTURE-PROTOCOL.md) proposed five captures on the assumption that no prior material existed. That assumption is now tested and holds — **with three amendments**:

1. **C3 (headway distribution) has a partial free substitute and a target.** The MTA's counts give mean headway. The resident petition gives *perceived* headway, and the two differ by a factor of two to three. C3 should now be designed to measure **the distribution, not just the mean**, because the gap between measured regularity and perceived irregularity is itself the finding. A distribution with a long tail feels different from a metronome at the same mean.
2. **A sixth capture is warranted: C6, simultaneous vibration and audio.** Justified in 3.4. It is nearly free, uses a sensor already in the handset, and addresses the one limb of the phenomenon that no crowd-sourced recording can ever contain.
3. **The DEP precedent should be cited when proposing any phone-based measurement.** The city's own environmental agency publishes phone-collected noise data from this park, in this park, as an official educational product. That materially lowers the barrier to this programme doing the same, provided it is at least as transparent about method — which, given the DEP lesson states neither weighting nor averaging time, is not a demanding bar.

### 4.2 For the argument as a whole

The programme's central difficulty has been explaining the **documentation gap**: why a problem this loud, this old and this well-attested has produced so little measurement. Until now the answer was a list of plausible motives.

There is now a mechanism, and it is better than the motives because it is impersonal. Nobody decided to ignore elevated rail noise. **The category was never created**, and every downstream instrument that inherited the category inherited the absence — the complaint form, the research corpus, the machine-learning taxonomy, and the statutory standard.

That is a more precise claim, a more testable one, and a considerably more actionable one. **"Amend the taxonomy" is a smaller ask than "solve the noise", it costs almost nothing, and it would begin generating the missing evidence immediately and at no cost to this programme or anyone else.**

It is also, notably, the first thing this programme has found that a resident could act on this month.

---

## Part 5 — New questions

Continuing the series. Q1–Q41 are in Documents 1–4.

**Q42.** Is elevated rapid-transit noise in New York City *preempted* from local regulation by the Noise Control Act of 1972, or is it merely *unregulated*? 40 CFR Part 201 is titled for **interstate rail carriers**; a rapid transit system operating wholly within one state may not be one. If it is not preempted, the City could regulate it and has chosen not to — which makes the remedy a municipal one and changes the entire advocacy strategy. **This is the highest-value unanswered question in the programme, and it is a desk question answerable by one competent lawyer in a day.**

**Q43.** What is the correct spatial unit for a soundscape claim? Two official datasets describe "Brooklyn Bridge Park" and differ by 35 dB because they are a mile apart. How many other municipal noise findings are unit-of-analysis artefacts of exactly this kind, and is there a defensible minimum reporting requirement — a receptor coordinate rather than a park name?

**Q44.** What has DUMBO already spent, privately, on noise mitigation? Every acoustic window, every insulated wall, every contractor on the DumboNYC list represents private capital deployed against a public externality. **Nobody has summed it.** If the figure approaches the cost of source-side mitigation, the entire economic argument inverts — the neighbourhood has already paid for the fix, in the least efficient possible way, one apartment at a time.

**Q45.** How much land under and around the Manhattan Bridge is unusable *because of noise alone*? The DUMBO Improvement District's own executive director named "the cacophony" as the main obstacle to reclaiming those spaces. Value that acreage at DUMBO waterfront rates and the mitigation cost may be trivially recovered — which converts this from a quality-of-life request into a land-value proposition.

**Q46.** Can under-deck acoustic treatment be co-justified as debris containment? A resident raised it unprompted. If a single intervention satisfies both an acoustic objective and a falling-object safety objective, it can draw on two budget lines and two regulatory rationales, and its cost-effectiveness threshold falls accordingly.

**Q47.** Why do residents perceive a 90-second headway as five minutes? Is the mechanism habituation, recall bias, per-line rather than per-track counting, or a genuine perceptual property of intermittent high-level events? This matters because **mitigation that reduces peak level but not event frequency may be perceived very differently from mitigation that does the reverse** — and nobody has established which residents would prefer.

**Q48.** What standard *should* apply to a person in a public park beneath a state authority's elevated railway? The resident petition reached for OSHA, an occupational standard, because nothing else was available. CEQR outdoor-serenity criteria apply to discretionary city actions, not to ongoing transit operation. **The gap is real, and naming the standard that ought to fill it is a legitimate research output.**

**Q49.** Does the SONYC corpus contain elevated rail? 150 million clips, 55+ sensors, spatial metadata released at city-block resolution. If any sensor was within range of an elevated structure, the audio exists and is merely unlabelled. Retrieving it by acoustic similarity rather than by label would produce, at a stroke, the largest corpus of elevated-rail noise recordings in existence — from data that has already been collected, already been paid for, and already been published.

**Q50.** Where did the complaints actually go? 311 cannot receive them. The MTA's § 1204-a report was triggered by an elected official's letter and references contact "since 2022." **The complaint record exists inside the MTA and inside council offices, and it is not public.** What is its volume, and what is its distribution over time?

---

## Part 6 — New methods

Continuing the register. Methods 0–20 are in Documents 1–5. **None of Methods 0–20 has been executed.** These five are added in full awareness of that.

**Method 21 — The taxonomy-blindness test.** *Desk. Hours. Free. Answers Q42 partially and tests the core claim of Part 2.*

Query the 311 dataset for noise complaint density in census tracts adjacent to elevated structures citywide — the Astoria line, the Brighton line, the Jamaica line, the Flushing line, the Bronx elevateds — and compare against matched tracts with no elevated structure. **The prediction of Part 2 is that there is no difference**, because the variable being measured is the availability of a complaint category, not the presence of noise. If elevated-adjacent tracts *do* show elevated complaint volume in some proxy category, the taxonomy is being worked around and the workaround is itself the signal, which is arguably more useful. Either result is publishable. This is the cheapest high-value method in the entire programme and it requires nothing but the API already used in Part 2.

**Method 22 — FOIL the complaint record.** *Desk. Weeks. Free. Answers Q50.*

Freedom of Information Law request to MTA New York City Transit for the volume and dates of customer complaints referencing Manhattan Bridge noise, 2015 to present, and to the relevant Council and State Senate district offices for constituent correspondence on the same. The § 1204-a report already establishes that such contact exists and dates it to 2022, which makes the request specific and hard to refuse as overbroad.

**Method 23 — Read the comment threads.** *Desk. Hours. Free. Closes the gap declared in 1.3.*

A logged-in human reading r/AskNYC, r/Brooklyn, r/nyc, r/NYCapartments and r/BrooklynBridgePark for recordings, and the DUMBO Neighborhood Alliance and DUMBO Action Committee channels for the same. **This document explicitly did not do this and should not be read as having cleared it.** If a usable recording exists anywhere, this is where it is.

**Method 24 — Contact the named actors.** *Correspondence. Weeks. Free.*

Katy Gaul-Stigge (petition author), Doreen Gallo (DUMBO Neighborhood Alliance), Elizabeth Johnson (DUMBO Action Committee), the DUMBO Improvement District, and Brooklyn Community Board 2. Purposes: establish whether recordings exist in community hands; establish what the MTA said at the York Street town hall; retrieve CB2 minutes and testimony; and open the possibility that this programme's outputs are useful to the people who would have to use them.

**A standing condition on this method.** These are residents, not subjects. Any contact must offer something before it asks for anything, must not represent this programme as more established than it is, and must make clear that its central artifacts are **synthetic** — the 3D model contains zero measured elements and the audio demonstration reproduces a mean rather than a sound. The programme has failed red-team review five times for over-claiming from thin reading. **Doing that to a community that has been asking for help since 2008 would be a different and worse kind of error.**

**Method 25 — Interrogate the SONYC corpus.** *Desk to research collaboration. Months. Free to low cost. Answers Q49.*

Two stages. First, from the released spatial metadata, determine whether any sensor was ever within acoustic range of an elevated structure — answerable from public data alone. If yes, second: retrieve candidate clips by acoustic similarity rather than by label, using the same OpenL3 embeddings the project's own baseline uses. Contact the SONYC team at NYU regardless of the outcome, because the taxonomy finding in Part 2.3 is something they would want to know and they are the people best placed to fix it.

---

## Part 7 — Where this document is likely to be wrong

**1. Reddit was not properly searched.** Stated in 1.3 and repeated here because it is the single largest hole. The user asked specifically about Reddit; automated access was blocked; what was searched was a crawler's index of post titles and bodies, not comment trees, and comment trees are where links live. **A negative result on Reddit has not been established.** Method 23.

**2. "No recording exists" is unprovable and is not what is claimed.** What is claimed is that none surfaced through fourteen searches across nine channels. Instagram, TikTok and YouTube are all substantially opaque to text search for acoustic content — a video of a train passing overhead is described by its view, not its sound. **There is almost certainly usable audio on those platforms right now, and it is unfindable by the methods used here.** Locating it needs a human scrolling, or a platform API, or acoustic search. This is a limitation of method, not a property of the world.

**3. The legal mechanism in Part 2.4 is the weakest thing here and is doing significant load-bearing work.** It is rated 2/5 `UNVERIFIED` and written as a question. But the whole narrative of Part 2 leans on it: the *reason* the taxonomies lack rail is asserted to be the noise code, and the reason the noise code lacks rail is asserted to be preemption or state-authority status. **If that is wrong, the finding degrades from a causal chain to a correlation between three lists.** The 311 and SONYC observations survive independently; the story connecting them may not. Q42, Method 24.

**4. The SONYC taxonomy claim is well-supported at the coarse level and only partly at the fine level.** The eight coarse classes were read from a results table and cross-checked across three independent sources. The derivation from the noise code is quoted twice, directly, from the authors. **But the twenty-three fine classes were not individually enumerated** — only the four under `alert-signal` are quoted, because the full taxonomy is published as a figure rather than as text and the extraction returned no image. The absence of a rail class at fine level is therefore inferred from the coarse structure, from the four fine classes that are visible, and from the absence of any rail mention anywhere in either paper. **That is strong but not conclusive**, and it should be checked against the dataset's own annotation schema — which is public — before the claim is repeated. Folded into Method 25.

**5. The 311 finding proves the absence of a category, not the absence of complaints.** Stated in 2.2 and worth restating, because the rhetorical temptation to elide the two is strong and the elision would be a serious error. Residents complained; the record went elsewhere. The correct statement is **"the public complaint record is structurally incapable of representing this problem,"** not "nobody complained."

**6. The 500 m circle is a judgement, not a boundary.** It was chosen to contain the dog run, the Archway and the Brooklyn anchorage. A larger radius would sweep in more of Brooklyn Heights and Vinegar Hill and change every count. **The counts are illustrative; the categorical absence is not sensitive to the radius**, and it is the categorical absence that carries the argument.

**7. The petition is treated generously.** It has 98 signatures. This document quotes it at length, tabulates its proposals against the engineering literature, and draws two findings from its errors. A hostile reader would say 98 signatures in a neighbourhood of roughly 5,000 people is weak evidence of community priority, and they would have a point. **It is quoted because of what it says, not because of how many signed it**, and the number is stated plainly for that reason. The 508-signature town hall petition is larger but was not read in full, and its relationship to the noise issue is not established.

**8. The 2008 Brooklyn Paper article is eighteen years old.** Karen Johnson and Kate Kerrigan may no longer hold those positions or those views. The buildings named have been joined by others. **What the article establishes is that the complaint is old, not that its current form matches its 2008 form.** The article is also a newspaper feature, not a study; its "80 decibels at John and Adams" figure is attributed to the Brooklyn Bridge Park environmental study rather than independently measured, and that study is already in this programme's evidence base at a higher rating.

**9. The DEP dataset critique may be unfair in one direction.** The lesson is explicit that it studies Pier 3 and the berm, and it never claims to characterise the whole park. **The failure mode described in 3.1 is a search-and-citation failure, not an authoring failure**, and the criticism is of how the document will be found and used rather than of what it says. It is included because the misuse is foreseeable and this programme would rather flag it than be the one to commit it.

**10. The convergence between the petition's five proposals and the engineering literature is presented as a check on the programme.** It is at least as likely that the resident read a news article about noise mitigation, or asked a search engine, in which case the two lists share a source and the convergence is not independent. **This is not a validation.** It is presented as one, mildly, and the reader should discount it accordingly.

**11. Everything here is a search result.** Not a single claim in Parts 3 to 6 rests on anyone from this programme standing in Brooklyn Bridge Park. The programme's standing remains what it was: **a desk study that has not measured anything.** This document adds two directly-queried datasets to that, which is genuine progress, and it does not change the fundamental position.

---

## Part 8 — Status

**Version 1.0. Not red-teamed.**

Every prior document in this programme failed its first red-team review, and always in the same way: **over-claiming from abstract-level reading**. This document has a specific exposure to that failure mode, and it is worth naming it before someone else does.

The finding in Part 2 is genuinely satisfying. It explains something that needed explaining, it is elegant, it connects four institutions, and it arrived unexpectedly from a search for something else. **Those are precisely the conditions under which this programme has previously over-claimed.** The 311 and SONYC observations are solid and were verified directly. **The causal chain joining them is not**, and if the chain breaks, what remains is three lists that happen to lack the same item.

The document has been written to fail safely if that happens. But it should be attacked at that joint first.

---

*Document 6 of the DUMBO rail-noise research programme. See [`README.md`](README.md) for the full index.*
