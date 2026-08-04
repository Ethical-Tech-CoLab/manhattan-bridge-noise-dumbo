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

> This investigation cost $236.61 in metered inference. A consultancy would
> have charged six figures for the same work. Therefore the saving is roughly
> three orders of magnitude.

That is withdrawn before it is made. It fails in three independent ways, and
each failure is large enough on its own to invalidate the ratio.

**It compares a measured number to an invented one.** The $236.61 is a
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

Cross-validated against Accenture Federal Services' own published rate card
(GSA MAS `GS-35F-540GA`, SIN 54151S, modification PA-0045 dated 9/25/2024,
contract period 12 July 2022 to 11 July 2027). The card carries the note:

> Prices include the 0.75% Industrial Funding Fee (IFF).

Year 10 OFFSITE, from the vendor's own PDF, matched against the GSA index:

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
| Named global consultancy | Accenture Federal Services awarded ceiling rates, by category |
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
| Named global consultancy | $219,377 - $686,531 |
| Whole-schedule median | $177,387 - $554,466 |
| Whole-schedule 10th percentile | $114,516 - $356,900 |

### What moves it

Sensitivity, widest band first, as a share of that package's own midpoint:

| Package | Band width | Share of midpoint |
| --- | --- | --- |
| Review and quality assurance | $85,291 | 17.2% |
| Interactive artifacts | $74,715 | 23.8% |
| Engagement management | $69,046 | 14.5% |
| Source retrieval and appraisal | $50,290 | 13.7% |
| Document authorship, cited | $38,313 | 11.8% |

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
| Named global consultancy | $71,777 - $207,785 |
| Whole-schedule median | $52,975 - $151,556 |
| Whole-schedule 10th percentile | $36,079 - $102,979 |

**None of these four disciplines has a matching category on the vendor's own rate card.**
Accenture Federal Services publishes no acoustical engineer, no
survey field staff, no licensed architect and no attorney. For the consultancy
rung the model substitutes the whole-schedule 75th percentile for that
discipline and says so in the data file (`rate_vendor_why`). That is a weaker
figure than the delivered-scope consultancy column, which is drawn from
matched, cent-for-cent verified categories.

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

## The disagreement, quantified and unreconciled

Convert the awards to implied hours at the model's own blended rate of
$147.80/h, against a bottom-up midpoint of 2,476 hours:

| Award percentile | Amount | Implied hours | As % of bottom-up low |
| --- | --- | --- | --- |
| 25th | $21,579 | 146 | 12% |
| median | $68,441 | 463 | 39% |
| 75th | $201,658 | 1,364 | 114% |
| 90th | $377,285 | 2,552 | 213% |
| maximum | $1,740,857 | 11,778 | 981% |

The bottom-up low lands at about **114% of the award 75th percentile**. On the
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

Ernst & Young LLP holds GSA contract `GS-00F-290CA`, period 8 September 2015
to 7 September 2030, current through modification PS-0041 effective 2 April
2026. Its published GSA Advantage price file is five pages long and contains
**no rates at all**. Page 5 reads:

> Use of or reference to the rate card or any information contained herein is
> limited to EY's GPS Federal US48. Use of or reference to the rate card or any
> information contained herein by other EY BU must be approved in advance of
> such use or reference by David M. Lewandoski, Director of Federal Contract
> Management.

The same contract's awarded labour categories appear in GSA's own ceiling-rate
index - **56 of them**, retrievable without a login, an account or a key. Both
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

What the billing ledger does not price:

| | |
| --- | --- |
| Wall-clock span of the engagement | 72.4 hours |
| Metered model inference | 6.86 - 7.47 hours |
| Estimated active human attention | roughly 9 - 11 hours |

The active-attention figure is **2/5 UNVERIFIED**. It is derived from request
timestamps and inter-request gaps, not from a stopwatch, and it cannot
distinguish a person reading output carefully from a person who walked away.

At the consultancy subject-matter-expert rate of $201.97/h, 10 hours of human
direction is about **$2,020** - roughly **eight and a half times** the entire
metered inference cost of $236.61. Any framing of this project's economics
that reports only the inference cost is understating the true cost by close to
an order of magnitude, before any allowance for the fact that the direction
required domain judgement that the model demonstrably did not supply. Three
claims in this repository were withdrawn because a human noticed they were
wrong.

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
