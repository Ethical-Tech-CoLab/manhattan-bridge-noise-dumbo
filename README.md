# Silencing the Span

**Defining the Manhattan Bridge rail-noise problem in DUMBO for a design-build intervention.**

An Ethical Tech CoLab research project.

---

## What this is

A rigorous problem-definition document about noise from NYC Subway **B, D, N and Q** services crossing the **Manhattan Bridge** and received in **DUMBO, Brooklyn**.

It is **not a design**. It is the artifact that must exist *before* a design can be honestly procured: a statement of what is known, what is claimed but unevidenced, and what has never been asked.

**Read [`IDEA-CONCEPT.md`](IDEA-CONCEPT.md).** It is self-contained, ~19,600 words, 14 parts.

## Two headline findings

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

## Structure

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

## Where further research should start

Not with more reading. **The four highest-value actions are records requests, not research** — none has been done in twenty-one years, and each closes a larger uncertainty than any literature review could:

1. **The current NYCDOT load rating**, expressed as an allowable mass / eccentric-moment / wind-area / attachment-fatigue budget at the track zone. Gates roughly half the option space. *(Q13)*
2. **The actual joint and rail-fixation inventory** across the four tracks. Not documented in any source located. *(Q2, §4.2)*
3. **The raw 2022–2024 MTA time histories**, via FOIL, to compute CEQR-compatible `L10(1)` properly. *(§3.2)*
4. **The § 1204-a Category IV records** — why was the sound level never established, and could it simply be filled in? *(Q11)*

Then the instrumented source apportionment of **Method 1**.

See also **§14 *Counter-citations*** — five works surfaced during red-teaming that bear directly on Q1–Q8 and were **not read in full**. Any team taking this forward should start there.

## Status

**Draft v1.1.** Revised after an adversarial review pass. Not peer-reviewed. Novelty claims are provisional; measured facts are solid. The document's own Part 13 is the best guide to how much to trust it.

## Contributing

This is a working research repository. Useful contributions, roughly in order of value:

- Answering any of Q1–Q13 with sourced evidence
- **Falsifying** any "not found" claim in §14 — two have already failed, and the prior on others failing is not low
- Non-English literature (Japanese, Chinese, German elevated-transit retrofit precedent), a known and material gap
- Full texts for the 20 `SNIPPET` sources, especially **TCRP Report 23** and the **WHO Environmental Noise Guidelines**, which are load-bearing
- Legal research on § 1204-a implementation, NYC Noise Control Code preemption, SEQRA and nuisance doctrine

## License

Research content released under [CC BY 4.0](LICENSE). Cite as:

> *Silencing the Span: Defining the Manhattan Bridge Rail-Noise Problem in DUMBO for a Design-Build Intervention.* Ethical Tech CoLab, 2026.
