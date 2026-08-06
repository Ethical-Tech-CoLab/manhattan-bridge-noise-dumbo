# 9. What this would have cost to buy

A procurement comparison for the Manhattan Bridge / DUMBO rail-noise
investigation. Companion to [Document 8, usage and cost](../usage/README.md),
which measured what this corpus cost to *produce*. This one asks the other
half of the question: what would the same deliverable have cost to *buy*.

**Interactive:** [procurement-dashboard.html](procurement-dashboard.html)

**Data:** [rates.json](rates.json) - [awards.json](awards.json) -
[procurement-data.json](procurement-data.json)

**Scripts:** [fetch_rates.py](fetch_rates.py) -
[fetch_awards.py](fetch_awards.py) -
[build_procurement_data.py](build_procurement_data.py)

---

## The claim this document exists to refuse

There is an obvious headline available here and it is wrong.

> This investigation cost $437.35 in metered inference. A consultancy would
> have charged six figures for the same work. Therefore the saving is roughly
> three orders of magnitude.

That is withdrawn before it is made. It fails in three independent ways, and
each failure is large enough on its own to invalidate the ratio.

**It compares a measured number to an invented one.** The $437.35 is a
reconciled per-request ledger rated 5/5 VERIFIED. The six-figure comparator is
an hours estimate multiplied by a rate. The rates are 5/5.
**The hours are 1/5 INVENTED.**
Nobody has ever built a comparable corpus under a timesheet
that this programme could read. Dividing a measured numerator by an invented
denominator produces an invented ratio wearing a measured number's clothes.

**It omits the human term entirely.** The billing ledger prices model
inference. It does not price the person who specified the work, rejected
outputs, caught the errors, and made every judgement call recorded in
`plan.md`. That person's time is the single largest cost in this project and
it appears in the ledger as exactly zero.

**It compares different deliverables.** What a firm sells includes things this
corpus does not contain: professional liability, a licensed signature, a
named partner who can be deposed, and - critically - **field measurement**. See
[what was not delivered](#what-was-not-delivered), below. Comparing a desk
study to a contracted engagement and calling the difference a saving is
comparing a manuscript to a building.

This is the same over-claim this repository has already withdrawn three times:
in Phase 9 (the park-phase finding), Phase 10 (the weekday-morning worst case)
and Phase 12 (the fitted propagation model). It is recorded here in advance
because the fourth occurrence would have been the easiest one to publish.

---

## Three instruments, deliberately never averaged

| | Instrument | What it measures | Rating |
| --- | --- | --- | --- |
| **A** | USASpending prime awards | Dollars actually obligated on federal noise-study contracts | 5/5 VERIFIED |
| **B** | Hours x GSA schedule rates | A bottom-up build of this scope at published rates | rates 5/5, **hours 1/5** |
| **C** | Copilot billing telemetry | What the inference actually cost | 5/5 VERIFIED |

They are reported side by side and **never combined into a single figure**.
A and B disagree by a factor of about three, and that disagreement is the
result of this document, not a defect in it. Averaging them would destroy the
only informative thing here.

---

## Instrument B: what the delivered scope prices at

### The rate source

GSA publishes awarded ceiling rates for Multiple Award Schedule contracts at
a login-free endpoint. Index `ceilingrates-2026-08-04_02-00-02`. The rates are
awarded ceilings on federal schedule contracts, inclusive of the Industrial
Funding Fee, for the current contract year.

Cross-validated against a large schedule holder's own published rate card
(SIN 54151S, current contract year). The card carries the note:

> Prices include the 0.75% Industrial Funding Fee (IFF).

Year 10 OFFSITE, from the holder's own PDF, matched against the GSA index:

| Category | Vendor card | GSA index |
| --- | --- | --- |
| Subject Matter Expert 1 | $322.29 | $322.29 |
| Subject Matter Expert 2 | $391.45 | $391.45 |
| Subject Matter Expert 3 | $480.91 | $480.91 |
| Project Manager | $365.72 | $365.72 |
| Enterprise Architect | $322.29 | $322.29 |
| Program Manager | $505.82 | $505.82 |
| Technical Writer | $169.49 | $169.49 |

Identical to the cent across seven independently checked categories. That
raises the index from a convenient aggregate to a **5/5 VERIFIED** instrument
and removes any need to parse vendor PDFs to build the model.

### The rate ladder

Three rungs, and one deliberately missing.

| Rung | Basis |
| --- | --- |
| Whole-schedule upper quartile | 75th percentile of awarded ceiling rates for the discipline, across every holder |
| Whole-schedule median | Median across all awarded holders of the matching category |
| Whole-schedule 10th percentile | The cheapest decile of awarded holders on the same schedule |

**There is no nearshore rung, and its absence is deliberate.** Eight sources
were retrieved for nearshore and offshore blended rates. Every one of them was
a marketing page published by a firm selling nearshore delivery. Not one
carried a method, a sample size, or a definition of what was being averaged.
A number of that provenance rated against this repository's own rubric is 1/5,
and 1/5 numbers do not go in tables next to 5/5 numbers without a warning
larger than the number. The whole-schedule 10th percentile is substituted and
labelled as exactly what it is:
**the cheapest decile of firms that hold this specific schedule**,
not an offshore quote.

### The scope, as work packages

Six packages, each sized from something countable in the repository - words of
document, lines of code, appraised sources, artifacts - and each given a
productivity band rather than a point rate.

| Package | Hours | Discipline used for the rate |
| --- | --- | --- |
| Source retrieval and appraisal | 125 - 374 | Data analyst |
| Document authorship, cited | 250 - 650 | Technical writer |
| Data acquisition and pipelines | 48 - 121 | Data engineer |
| Quantitative modelling | 102 - 254 | Data scientist |
| Interactive artifacts | 360 - 901 | Software engineer |
| Site generation and publication | 128 - 319 | Web developer |

Plus two overheads applied as percentages: review and quality assurance at
10-20% (101 - 524 h, priced as a subject matter expert), and engagement
management at 12-22% (122 - 576 h, priced as a project manager).

**Total: 1,235 to 3,717 hours.** A span of three to one. That span is honest -
it is the width of the productivity assumptions - and it is the reason no
point estimate appears anywhere in this document.

### The result

| Rung | Delivered scope |
| --- | --- |
| Whole-schedule upper quartile | $251,112 - $786,920 |
| Whole-schedule median | $203,009 - $635,441 |
| Whole-schedule 10th percentile | $131,046 - $408,987 |

### What moves it

Sensitivity, widest band first, as a share of that package's own midpoint:

| Package | Band width | Share of midpoint |
| --- | --- | --- |
| Review and quality assurance | $98,076 | 17.3% |
| Interactive artifacts | $84,656 | 23.6% |
| Engagement management | $79,409 | 14.5% |
| Source retrieval and appraisal | $58,369 | 13.9% |
| Document authorship, cited | $46,376 | 12.4% |

The largest single uncertainty is **not** the research and not the code. It is
**how much review the work receives**. That is worth stating plainly: the term
that most changes what this would have cost to buy is the term that most
changes whether it would have been right.

---

## What was not delivered

The comparison above prices a **desk study**. This corpus contains no measured
acoustic data of its own, no counted pedestrians, no licensed design and no
legal opinion. A firm asked for "a noise study of the Manhattan Bridge in
DUMBO" would deliver those, and a client would expect them.

| Not delivered | Hours | Median rate | Why it is missing |
| --- | --- | --- | --- |
| Field acoustic measurement (Methods 11, 28, 31; captures C1-C5) | 80 - 200 | $131.21 | Five capture campaigns plus instrument calibration, analysis and reporting. |
| Pedestrian origin-destination and dwell survey (Method 28) | 120 - 320 | $108.13 | Timed cordon counts across three day types. The single blocking unknown for any absolute exposure figure. |
| Licensed architectural and structural design | 200 - 600 | $142.01 | Nothing in this repository is a design. A design-build proposal needs a licensed architect and a structural engineer of record. |
| Preemption opinion (Q42) | 8 - 40 | $137.66 | Whether 40 CFR Part 201 preempts municipal regulation of a wholly intrastate rapid transit system. One lawyer, one day. |

| Rung | Not-delivered scope |
| --- | --- |
| Whole-schedule upper quartile | $71,777 - $207,785 |
| Whole-schedule median | $52,975 - $151,556 |
| Whole-schedule 10th percentile | $36,079 - $102,979 |

Published here as a distinction between the two columns:

> **None of these four disciplines has a matching category on the holder's own rate card.** [...] For the upper-quartile rung the model substitutes the whole-schedule 75th percentile for that discipline and says so in the data file. That is a weaker figure than the delivered-scope upper-quartile column, which is drawn from matched, cent-for-cent verified categories.

**That is withdrawn.** There is no such distinction, because
**the delivered-scope column is not drawn from matched categories either.**
The model carried a lookup
that consulted one holder's own published categories before falling back to the
whole-schedule 75th percentile, and **that lookup never returned a match once** —
not for any of the eight delivered disciplines and not for any of the four
below. Every figure in every upper-quartile column, in both tables, has always
been the whole-schedule 75th percentile.

The cause is the same taxonomy problem this document already reports from the
other direction: **holders publish internal job titles, not discipline names.**
The categories on an individual card read `Cyber Programmer 1` and
`Business Functions Consultant 1`, which no discipline regex can match, so the
fallback was not a fallback — it was the only path.

**No number moves.** Every rate in both tables is the figure it always was; what
changes is the description of where it came from, the name of the rung, and the
field name in the data file, which is now `rate_upper_why` and reads
`whole-schedule 75th percentile` for every discipline. The dead lookup has been
removed rather than left in place, because a branch that never returns is a
claim the model does not honour.
**The upper quartile remains a genuine 5/5 figure** —
it is drawn from the same GSA awarded-ceiling index as the other two
rungs, and that index is independently cross-validated above. It is simply not,
and never was, a vendor-specific number.

**The model refuses to emit an all-in figure.** Adding the two columns would
produce a number describing a deliverable that does not exist, and it would
look more authoritative than either column alone. The two are reported
separately, permanently.

This is also the honest answer to "what did the money buy". The delivered
column is what the metered inference substituted for. The not-delivered column
is what it did not, and cannot.

---

## Instrument A: what buyers actually paid

Bottom-up estimates are the weakest form of cost evidence, because the analyst
choosing the hours already knows what answer they want. So the model carries a
second, independent instrument that assumes no hours at all.

USASpending publishes obligated dollars on real federal contracts. Filtering
on noise and acoustic study keywords across product-service codes B (special
studies), C (architect and engineering) and R (professional services), award
types A-D, 2015-01-01 to 2026-08-01:

| | Amount |
| --- | --- |
| n | 56 awards |
| minimum | $5,900 |
| 10th percentile | $11,659 |
| 25th percentile | $21,579 |
| **median** | **$68,441** |
| 75th percentile | $201,658 |
| 90th percentile | $377,285 |
| maximum | $1,740,857 |
| mean | $186,409 |

These are dollars that changed hands. No hours are assumed, no productivity is
invented, and no analyst chose them.

---

## What a design practice charges to define a problem

Asked directly what an architecture or design-build practice would have charged
for a study of this shape, the obvious move is to price it the way this document
prices everything else: hours multiplied by a published schedule rate.

**That move is unavailable, and the reason is the more interesting half of the answer.** Architectural and engineering services are not bought on price. The
statutory note to 40 U.S.C. §1103 is explicit that the schedule route is closed
to them:

> Architectural and engineering services (as defined in section 1102 of title 40,
> United States Code) **shall not be offered under multiple-award schedule > contracts** entered into by the Administrator of General Services [...] unless
> such services [...] are awarded in accordance with the selection procedures set
> forth in chapter 11 of title 40, United States Code.

And chapter 11 selects on qualifications, with price entering only afterwards.
§1103(d) directs the agency head to rank at least three firms by competence;
§1104(a) then has the agency negotiate compensation **with the firm already chosen**. Price is not a selection criterion, so there is no awarded ceiling rate
for architecture the way there is for a data engineer or a project manager.

This is the **fifth** time this corpus has run into the same shape: an absence in
a classification system that makes a real thing unaskable. The others were the
noise code's missing rail category inherited by 311 and SONYC, the blank cell on
form 1204-a, the twelve thousand project managers against seven acoustical
engineers, and the schedule holders who publish job titles rather than
disciplines. This one is the strongest of the five, because it is not an
oversight — **it is deliberate federal policy, and it is written down.**

### So the rung is priced with instrument A instead

A second population of USASpending awards: product-service code C, award
descriptions naming a **study** rather than a building, same period and award
types as the noise population. It is kept separate and never pooled — the two
answer different questions, and a combined percentile would answer neither.

| | Amount |
| --- | --- |
| n | 123 awards |
| minimum | $11,210 |
| 25th percentile | $78,843 |
| **median** | **$243,899** |
| 75th percentile | $590,235 |
| 90th percentile | $1,823,006 |
| maximum | $11,666,796 |

**3.6 times the median federal noise study.** A design practice is not paid to
write a report; it is paid to run a process that ends in a decision, and that
costs more.

The population is dominated by one award description — the **design charrette**,
108 of 123 — which is a practice being paid to sit with a client and establish
what the problem is before anything is designed. That is the closest commercial
analogue this study has, so the dominance is the population converging on the
right thing rather than a contaminant. It is broken out on the dashboard so a
reader can judge that rather than take it. The charrette sub-population medians
at $238,452, within 2.3% of the whole.

### And a published rate ladder, since the schedule has none

Public bodies that appoint an A-E panel publish the rate schedule as an exhibit
to the appointing resolution. One such resolution — a New York public authority's
2025-2027 A-E appointment, five firms, each with its own ladder — gives:

| Labour title, as printed | Hourly rate |
| --- | --- |
| Principal | $275 |
| Principal, MEP engineering services | $250 |
| Senior project manager | $250 |
| Project manager | $220 |
| Principal, engineered solutions | $200 |
| Senior project architect/engineer | $190 |
| Managing member | $190 |
| Partner-in-charge, architectural services | $180 |
| Principal structural engineer, PE | $180 |
| Senior environmental scientist | $180 |
| Project architect | $140 |

**5/5 as published rates. 2/5 as a guide to the New York City market.** An
upstate county panel is not a Brooklyn signature practice; the direction of the
difference is obvious and its size is not. The ladder is therefore used for one
purpose only — as a published reference point beside a single stated rate — and
it is not multiplied by anything.

---

## The disagreement, quantified and unreconciled

Convert the awards to implied hours at the model's own blended rate of
$147.31/h, against a bottom-up midpoint of 2,846 hours:

| Award percentile | Amount | Implied hours | As % of bottom-up low |
| --- | --- | --- | --- |
| 25th | $21,579 | 146 | 11% |
| median | $68,441 | 464 | 34% |
| 75th | $201,658 | 1,369 | 99% |
| 90th | $377,285 | 2,561 | 186% |
| maximum | $1,740,857 | 11,817 | 857% |

The bottom-up low lands at about **99% of the award 75th percentile**. On the
population of federal noise studies actually purchased, a corpus of this size
prices like an **upper-quartile** engagement.

Two readings survive this, and **neither is chosen**:

1. **The hours are too generous.** Nine documents and seven artifacts is a lot
   of output, but output is not effort, and the productivity bands were set by
   the same person who wanted the answer to be large.
2. **The awards buy narrower deliverables.** A $68,441 federal noise study is
   very likely one site, one campaign, one report - not a nine-document corpus
   with six interactive artifacts and a method register.

Both are plausible. Resolving between them requires a timesheet from a firm
that has built a comparable corpus, and no such document was found. The
disagreement is therefore **published as the finding** rather than smoothed
into a range.

---

## The transparency asymmetry

One large schedule holder's published GSA Advantage price file is five pages
long and contains **no rates at all**. The file's final page carries a legal
notice restricting internal use of the rate card.

The same contract's awarded labour categories appear in GSA's own ceiling-rate
index — dozens of them, retrievable without a login, an account or a key. Both
facts are true simultaneously. The restriction is real and the data is public.

This is not an accusation; it is a note about where public information lives.
A researcher who accepts the vendor's own published file as the authoritative
public record concludes that the rates are not disclosed. A researcher who
queries the awarding agency's index concludes that they are. The second
researcher is right, and would have had no reason to look if the first
document had not so specifically declined to help.

The same shape as the SONYC taxonomy finding in
[Document 6](../COMMUNITY-EVIDENCE-AUDIT.md) and the 1204-a blank cell in
[Document 1](../IDEA-CONCEPT.md):
**the absence is inherited, and it is findable elsewhere if you stop asking the party with the least interest in answering.**

---

## Twelve thousand project managers and seven acoustical engineers

Labour categories on the GSA schedule matching each discipline:

| Discipline | Categories on schedule | Median rate |
| --- | --- | --- |
| Project manager | 12,825 | $151.95 |
| Subject matter expert | 10,330 | $201.97 |
| Program manager | 8,591 | $183.37 |
| Technical writer | 4,467 | $95.76 |
| Software engineer | 3,686 | $138.26 |
| Data analyst | 1,749 | $114.81 |
| Data scientist | 1,180 | $167.81 |
| Environmental scientist | 218 | $108.13 |
| Civil engineer | 217 | $117.15 |
| GIS analyst | 200 | $101.29 |
| Architect (building) | 46 | $142.01 |
| **Acoustical engineer** | **7** | **$131.21** |

Seven. Across the entire federal professional-services schedule, from five
firms, ranging $68.95 to $172.65.

This is a **procurement-side instance of the same taxonomy blindness** this
programme documented on the complaint side. A federal buyer who wants an
acoustical engineer on schedule has seven categories to choose from and will
very likely buy a "subject matter expert" or an "environmental scientist"
instead - because those categories exist in abundance and the specific one
barely does. The work then gets done, and gets *recorded* as something else.

Consequence for Instrument A:
**the 56-award population is almost certainly an undercount**,
because acoustic work bought under a generic category is invisible
to a keyword-and-PSC search. Direction of bias is known; magnitude is not.
Stated, not corrected.

Note also that a project manager costs more per hour than an acoustical
engineer ($151.95 against $131.21). The scarce specialist is cheaper than the
abundant coordinator.

---

## The human term

What the billing ledger does not price. **Every figure in this section is derived at build time** by `build_procurement_data.py` from the usage ledger and the rate
files. Three of them used to be typed here by hand, and they went stale by close
to a factor of two the moment the engagement continued past the day they were
written.

| | |
| --- | --- |
| Wall-clock span of the engagement | 127.4 hours |
| Metered model inference | 12.31 hours summed, 11.10 once overlap is removed |
| Estimated active human attention | 11.7 - 13.4 hours |

The active-attention figure is **2/5 UNVERIFIED**. It is derived from request
timestamps and inter-request gaps, not from a stopwatch, and it cannot
distinguish a person reading output carefully from a person who walked away. The
band is the same measure at idle cutoffs of 120 s and 300 s.

### The same hours, at four different rates

| Rate applied | Per hour | Cost of direction | Times the metered bill |
| --- | --- | --- | --- |
| Operator's stated rate | $1,000.00 | $11,654 - $13,348 | 26.6x - 30.5x |
| Top of the published A-E schedule | $275.00 | $3,204 - $3,670 | 7.3x - 8.4x |
| Subject-matter expert, schedule upper quartile | $255.79 | $2,981 - $3,414 | 6.8x - 7.8x |
| Lowest principal on the same A-E schedule | $180.00 | $2,097 - $2,402 | 4.8x - 5.5x |

**One of those four rows is not evidence, and it is the first one.**
The operator's rate is a statement by the person who did the work about what that
person's hour is worth. It is rated
**5/5 as a stated rate and 0/5 as a market observation** —
the same way this repository rates every operator statement of intent. It is
**3.64 times** the highest rate on the five-firm published A-E schedule above, and
**3.91 times** the subject-matter-expert upper quartile on the GSA index. Those
ratios are printed rather than smoothed away, because a stated rate sitting nearly
four times above every published comparator is a claim a reader is entitled to
discount, and burying it in a blended average would deny them that.

The four are never averaged. Averaging a valuation with three observations
launders the valuation, which is the same failure this document refuses at the
level of the three instruments.

### What survives whichever rate is picked

At **every** rate tested, including the lowest, the human hours cost several times
more than the model:

> The direction of this work costs between **4.8 and 30.5 times** the entire
> metered inference bill of $437.35, and the multiple never falls below five.

Any framing of this project's economics that reports only the inference cost is
understating it by close to an order of magnitude at best, and by a factor of
thirty at the operator's own valuation — before any allowance for the fact that
the direction required domain judgement the model demonstrably did not supply.
Several claims in this repository were withdrawn because a human noticed they
were wrong.

---

## Where this document is likely to be wrong

1. **The hours are invented.** This is the largest weakness by a wide margin
   and it is first deliberately. Six packages, each with a productivity band,
   each band chosen by the author. The bands are wide (three to one overall)
   precisely because they are not knowledge, but a wide invented band is still
   an invented band. Nothing in the delivered-scope table is stronger than
   this term, and every dollar figure inherits it.

2. **The scope map is arguable.** Whether "interactive artifacts" is one
   package or four, and whether a research corpus needs 10% or 20% review,
   are judgement calls that swing the answer by more than $150,000 combined.
   A different analyst with the same rates would produce a different number.

3. **GSA schedule rates are ceilings, not prices.** Awarded ceiling rates are
   the maximum a holder may charge on that schedule. Actual task-order pricing
   is routinely discounted below ceiling, and the discount is not public. The
   consultancy rung is therefore an **upper bound on that rung**, not a quote.

4. **The award population is filtered by keyword and PSC.** As set out above,
   acoustic work bought under generic labour categories does not appear. n=56
   is a floor. It is also federal-only: this is a municipal problem, and city
   and state procurement is not in this dataset at all.

5. **Federal rates are not New York City rates.** The GSA schedule prices work
   for federal buyers under federal contracting overhead. A private client in
   New York, or the MTA under its own procurement rules, faces a different
   market. The direction of the difference is not known.

6. **The active-human-hours figure is inferred from timestamps.** 2/5. A gap
   between requests is not proof of attention, and simultaneous attention to
   something else is invisible. This term is load-bearing for the human-cost
   comparison in the section above.

7. **"Not delivered" is a list, not an estimate of a designed campaign.** The
   four items were sized by analogy, not scoped. A real field acoustic campaign
   at this site might cost substantially more than the band shown, because
   working over a live four-track river crossing owned by the MTA involves
   access, flagging and insurance that a generic estimate does not capture.

8. **This document compares a finished artifact to a hypothetical engagement, and finished artifacts flatter themselves.**
   The corpus that exists is the
   one that survived. A firm's engagement would have included work this
   project simply abandoned, and this project's abandoned work does not appear
   in its own hours estimate either. The asymmetry is not quantified.

---

## The question this opens

**Q55.** **What does a research corpus cost, and against what?**
This document establishes that the question has no single answer, because the
three available instruments disagree by a factor of about three and each
measures something different. A per-request billing ledger measures inference
and nothing else. A bottom-up build at published rates measures an analyst's
beliefs about productivity. Obligated contract dollars measure what buyers with
budgets actually chose to pay for deliverables nobody here has seen.

The open part is the one that would make this transferable:
**is there any published, methodologically stated dataset of hours-to-deliverable for research and analysis engagements?**
Eight searches for nearshore blended rates returned
eight vendor marketing pages. Searches for consultancy timesheet data returned
nothing usable at all. If such a dataset exists, it collapses the largest
weakness in this document — the 1/5 hours term — into a 4/5 or 5/5 one, and
converts a disagreement into a measurement. If it does not exist, that absence
is itself worth recording, because it means
**every published claim about what AI-assisted research saves is resting on the same invented denominator this document refuses to hide.**
Method 37 is executed; this is what executing it found that it could not
answer.

---

## Reproducing this

```bash
python procurement/fetch_rates.py           # ~4 min, 346 API calls, no key
python procurement/fetch_awards.py          # ~1 min, no key
python usage/build_usage_data.py            # reads the local billing store
python procurement/build_procurement_data.py
```

The first three write `rates.json`, `awards.json` and `usage/usage-data.json`.
The fourth combines them, writes `procurement-data.json`, and injects the
result into `procurement-dashboard.html`.

**What a fresh clone cannot re-run.** Stated so the reproducibility claim above
is not larger than it is. `fetch_rates.py` sweeps the schedule by discipline
and, separately, can sweep it by a named holder. The discipline sweep is the
one every figure in this document rests on and it runs from a clean checkout
with no configuration. The holder sweep does not: its query terms are read
from an untracked `procurement/vendor_terms.json`, and with that file absent —
which is the normal state of this repository — those groups are simply skipped
and nothing downstream changes, because
**no rate published here is derived from a holder-specific query.**
The cross-validation described in
[The rate source](#the-rate-source) was checked by hand against a published
card, not by that code path.

`rates.json` carries **no vendor name and no contract number** for any row. A
contract number resolves to a holder in a single search, so the two are one
field for this purpose and neither is carried. This is a study of published
rates and not of firms, and the file is exactly as useful for that without
them: every statistic here is computed over discipline and price, and both
survive. It does mean a reader cannot audit *which* holders a percentile was
drawn from — only that it was drawn from every holder on the schedule, which
is what the rung now claims.

Two silent failure modes in the GSA endpoint are guarded in `fetch_rates.py`
and both were hit live during development:

- `hits.total.value` **saturates at 10,000** and reports `relation: "gte"`.
  Taken at face value it undercounts project managers by 2,913.
- `page_size` caps near 1,000 and default ordering is price **ascending**, so
  1,000 rows of a 12,913-row population is **the cheapest thousand**, not a
  sample.

Both are avoided by sweeping the price axis in bands. `price_range` is
inclusive at both ends, so rows priced exactly on a band boundary return twice
and are deduplicated on record id - a naive three-band probe reports 12,916
project managers where the deduplicated sweep finds 12,913.

One more, in `fetch_awards.py`: `curl.exe -d $body` in PowerShell mangles JSON
bodies and returns a parse error from the API. Use a real HTTP client.
