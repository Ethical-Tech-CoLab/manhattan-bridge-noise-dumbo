# Usage: what this investigation cost, and how that was established

**Dashboard:** [`usage-dashboard.html`](usage-dashboard.html) &middot;
**Data:** [`usage-data.json`](usage-data.json) &middot;
**Generator:** [`usage-calc`](https://github.com/Ethical-Tech-CoLab/usage-calc)

This directory answers a question about the study rather than a question about
the bridge: what did producing this repository consume, and what would have to
be instrumented to answer that properly next time.

**The generator no longer lives here.** It was written in this repository,
proved on this repository, and has now been extracted to
[Ethical-Tech-CoLab/usage-calc](https://github.com/Ethical-Tech-CoLab/usage-calc)
so that any project can run it. This directory keeps what is specific to this
study: the styled page, the data behind it, the contributed exports from the
other machine, and the method below.

The extraction was itself the test. Both the old in-repo generator and the
extracted module were run over **one frozen copy of the store**, and their
payloads agree on every substantive key — including the cross-machine merge, at
8,203 requests and $1,502.14 either way. The page you can open above is now
produced entirely by the module.

```
pip install git+https://github.com/Ethical-Tech-CoLab/usage-calc.git

usage-calc build                 # regenerate this repository's dashboard
usage-calc sessions              # every session in the local store
usage-calc query --days 7        # what this machine has been doing lately
usage-calc verify                # drive the page in a browser and check it
usage-calc export --all --out .  # run on ANOTHER machine, copy into contrib/
```

Configuration lives in [`../usage-calc.json`](../usage-calc.json), which is
where the four sibling repositories are named.

**Re-running `build` splices new numbers into the existing page rather than replacing it**, so this repository's own styling and masthead survive
regeneration. That was verified byte-for-byte at cutover: everything outside
the payload was unchanged.

## Why a noise study carries a usage page at all

**From tokens to public infrastructure.** Every infrastructure system becomes
governable at the moment it becomes measurable. Electricity became governable
through the kilowatt-hour, telecommunications through the minute and the
megabit, cloud computing through the CPU-hour and the gigabyte of egress. The
unit is never only a technical detail; it is the language in which allocation,
pricing and accountability can be argued at all.

Machine inference is entering that stage now, and GitHub has published the
unit. That is what makes this page possible, and it is why the page sits inside
a research repository about a bridge rather than in a billing tool.

The connection to the rest of this work is not decorative. This programme's
central finding about DUMBO is that
**the noise is unmeasured and therefore ungoverned**
&mdash; NYC 311 has no category that can accept a rail-noise
complaint, so the exposure cannot be counted, so it cannot be budgeted against.
The same argument, applied to this repository's own production, produces this
directory. A research programme that argues measurement precedes governance and
then declines to measure itself is making an exception for the only party it
controls.

**The pull quote, and it is the reason the page exists:** the AI age will not
only be defined by who has access to models. It will also be defined by who can
afford inference, who can measure it, who can govern it, and who benefits from
the systems built on top of it. This repository was produced for
**$437.35 of list-price inference** by one person who did not have to ask
anyone for the budget. Both halves of that sentence are the finding.

### The unit is documented, and that is recent

GitHub Docs, *Usage-based billing for organizations and enterprises*, retrieved
4 August 2026:

> Each token is priced based on the model used, and the total is converted into
> AI credits, where 1 AI credit = $0.01 USD.

The same sentence appears in *Models and pricing for GitHub Copilot*, which
also states that all listed prices are **per 1 million tokens** &mdash;
independently confirming the `batch_size` of 1,000,000 found in the client's own
`models.json`. Both pages state that Copilot CLI usage is billed in AI credits;
code completions are not.

| Source | Rating |
| --- | --- |
| GitHub. (2026). *Usage-based billing for organizations and enterprises*. GitHub Docs. [Link](https://docs.github.com/en/copilot/concepts/billing/usage-based-billing-for-organizations-and-enterprises) | 5/5 VERIFIED |
| GitHub. (2026). *Models and pricing for GitHub Copilot*. GitHub Docs. [Link](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing) | 5/5 VERIFIED |
| Rodriguez, M. (2026, April 27). *GitHub Copilot is moving to usage-based billing*. The GitHub Blog. [Link](https://github.blog/news-insights/company-news/github-copilot-is-moving-to-usage-based-billing/) | 4/5 SNIPPET |

**The public term is AI credits.** `nano-AIU`, the field this directory's
extractor actually reads, is a telemetry subunit that appears in the local
store and in no public billing page. It is used here because it is what the
data contains, and it is converted to credits and to dollars for anything
quotable. Anyone citing this work should cite credits.

## Where the numbers come from

| Field | Source | Rating |
| --- | --- | --- |
| Requests, models, tokens, cost, duration, turn, sub-agent id | `~/.copilot/session-store.db`, table `assistant_usage_events` | 5/5 VERIFIED |
| Per-model token prices | `models.json`, written beside the client's debug log | 5/5 VERIFIED |
| One AIU = one US cent | GitHub Docs, quoted above; corroborated by matching against vendor list prices | 5/5 VERIFIED |
| Commits, line counts, file counts, word counts | `git` in this repository | 5/5 VERIFIED |
| Energy per request | Oviedo et al., *Joule*, 2025 | 5/5 for the figure, 2/5 applied here |
| Household electricity | US EIA, *Electricity use in homes* | 5/5 VERIFIED |

### The unit

The store prices each request in **nano-AIU**, and no local file states what an
AIU is. It was originally taken here to be one US cent on the strength of four
independent agreements with published vendor list prices:

| Model | Catalogue rate, in / out | Vendor list price |
| --- | --- | --- |
| `claude-sonnet-4.5` | 300 / 1500 | $3.00 / $15.00 per 1M |
| `claude-haiku-4.5` | 100 / 500 | $1.00 / $5.00 per 1M |
| `claude-opus-4.6` | 500 / 2500 | $5.00 / $25.00 per 1M |
| cache channels, all Anthropic models | 0.1x base read, 1.25x base write | the published cache multiples |

That was published as
**a strong inference and explicitly not documentation, rated 4/5.**
It has since been checked against GitHub's own billing
documentation, quoted above, which states the identity directly. The rating is
raised to 5/5.

**This is not a withdrawal and should not be counted as one.** The inference was
correct; what changed is that it stopped being an inference. It is recorded here
because a rating that silently improves is as much a drift as a rating that
silently degrades, and because the arithmetic above is now an independent check
on the documentation rather than a substitute for it &mdash; three models and
both cache ratios reproduce the documented cent from a completely different
direction.

### The rule the generator enforces

Cost and token totals are read from `token_details_json`, **not** from the
`input_tokens` and `cache_write_tokens` columns beside it. The script recomputes
the cost of every row from the details and refuses to write output if any row
disagrees with the cost the client recorded. On the current data all rows
reconcile exactly.

## Five traps, in the style of the seven in `data-collection`

**Trap 1: the obvious log is the wrong log.** `main.jsonl` in the extension's
debug directory is not the usage record; it holds session lifecycle events. It
is easy to find, it looks authoritative, and a search that stops there concludes
that no usage data exists. The store is in `~/.copilot`, not in
`%APPDATA%\Code`.

**Trap 2: the columns and the details disagree, silently.** For rows where the
initiator is `compaction`, `cache_write_tokens` is `0` while
`token_details_json` records the real figure &mdash; in this project's data,
several hundred thousand tokens on some rows. Summing the columns produces a
number with no error and no warning that under-counts both tokens and cost. Only
the details reconcile to `total_nano_aiu`.

**Trap 3: `input_tokens` is not the fresh prompt.** It is
`fresh + cache_read + cache_write`. Subtracting only `cache_read` and then
adding a cache-write charge double-counts the written tokens; in this data that
inflates the total by about fourteen per cent while looking entirely reasonable.
The fresh-input figure lives only in the details, under `tokenType: "input"`.

**Trap 4: summing `duration_ms` over-counts wall time.** Sub-agents run beside
the main agent, so their durations overlap it. The generator merges the
intervals instead: here the sum is about nine per cent above the union. Report
the union, or say which one is being reported.

**Trap 5: a timestamp is UTC and a working day is not.**
Nineteen per cent of the requests in this store fall between 00:00 and 04:00
UTC, which is the previous evening in New York. Cutting days on UTC midnightmoves those to the following date. On one day here that is the difference
between 404 requests and 80 &mdash; a five-fold misattribution, with no error
and nothing on the page to suggest anything is wrong. The generator cuts on
**local** midnight, using the platform's own zone database via
`datetime.astimezone()` rather than a named zone, so anyone who runs it gets
their own days and no timezone package is required. The resolved zone name and
offset are written into the JSON and printed on the page, because a day
boundary that is not stated cannot be checked.

## The day-by-day split, and one column that is not a measurement

The dashboard reports each day twice: what a model was **generating**, and what
was left over. They are not the same kind of number and the panel says so.

**Model active time is measured.** It is the union of every request's
`[ts - duration, ts]` interval, by trap 4 above. Nothing about it depends on
any choice made afterwards.

**Person active time is a residual, not an observation.** There is no keystroke
or focus telemetry in this store, and none is invented here. Within a sitting
either a model was working or it was not, so the panel reports

    person = engaged - model

which holds by construction and can never go negative. What it cannot do is
tell reading from absence. It over-counts when somebody walked away mid-sitting
and under-counts the reading done after a sitting's last request, so it errs in
both directions rather than bounding the truth on one side. That is worse than
a bound and better than a guess, and it is the reason the column is labelled on
the page as a residual rather than as time.

**The sensitivity is the argument, not a caveat attached to it.** A sitting ends
at a pause longer than the idle cut-off, and there is no correct cut-off, so the
page offers four and lets a reader move between them. Across 2 min to 30 min:

| | 2 min | 5 min | 10 min | 30 min |
| --- | --- | --- | --- | --- |
| Model hours | 14.39 | 14.39 | 14.39 | 14.39 |
| Person hours | 3.31 | 4.31 | 7.41 | 11.17 |
| Person share | 18.7% | 23.1% | 34.0% | 43.7% |
| Sittings | 102 | 62 | 30 | 18 |

Those figures are a snapshot of one generator run and this document does not
regenerate itself; the dashboard is the authority and its selector will show
the current values. What is not a snapshot is the **shape**: the model row is
flat by construction, and the generator refuses to write output if it ever
stops being flat, because a model figure that moves with the cut-off means the
interval arithmetic is double-counting somewhere. It did, once &mdash; two
sittings could overlap when a long sub-agent request finished after the pause
that ended the previous one, and the overlap was counted twice. Twelve seconds
across the whole corpus, invisible to the `engaged = model + person` check
because it inflated both sides equally, and caught only because a paragraph
conditional on flatness silently declined to render.

Model hours do not move at all. Person hours move by a factor of 3.4 under a
decision nobody can justify from the data. That difference is the whole reason
one column is evidence and the other is an inference, and it is far more useful
printed than hidden behind a single default. The finding that survives every
setting is that **the person is the smaller half of an engaged day**, which is
the same conclusion as finding 3 below, now stated with its sensitivity
attached.

Two arithmetic notes, stated rather than smoothed over. A sitting is counted
from when its first request **started**, not when that request returned;
otherwise the first inference of a sitting falls outside its own engaged window
and the residual can go negative. That is also why the daily engaged total runs
slightly above the single active-time figure elsewhere on the page, which
measures gaps between requests. And the day totals reconcile exactly to the
page totals for requests, turns and cost &mdash; the generator refuses to write
output if they do not.

## Three findings that were not the point of the exercise

**1. Compaction is a first-class cost centre.** It is invisible in every other
account. The requests whose only job is to summarise the conversation so it
keeps fitting in a context window cost more than every request the user typed,
and several times everything delegated to sub-agents. It produces no output
anyone reads. It is the strongest argument in this data for keeping sessions
short and scoped, and no interface surfaces it.

**2. Reading is voluminous and cheap; writing is tiny and expensive.** Cache
reads are the overwhelming majority of tokens billed and roughly half the money.
Output is well under one per cent of tokens and about a fifth of the money.
Fresh, uncached input &mdash; what a reader intuitively pictures as "the prompt"
&mdash; is a rounding error. Any cost model built on prompt length is modelling
the wrong quantity.

**3. Almost all engaged time was spent waiting for a model.** Two independent
measurements agree: engaged time inferred from gaps between requests, and busy
time computed from request durations, land within about ten per cent of each
other. Budgeting this class of work in person-hours budgets the wrong resource.

## Two numbers, and why both still have to be quoted

| | |
| --- | --- |
| **AI-credit cost** | tokens priced at the published per-model rates and converted at 1 credit = $0.01 |
| **Premium requests** | the older subscription unit, one per user-initiated turn, at the recorded multiplier |

These differ by more than two orders of magnitude, and they cannot be
reconciled: **nothing available to a client maps one onto the other.** Quoting
the first alone overstates what any individual subscriber paid this month.
Quoting the second alone hides what was consumed. The dashboard prints both,
adjacent, and refuses to derive a third number from them.

**One thing has changed since that rule was written.** GitHub announced on
27 April 2026 that Copilot is moving to usage-based billing, and the current
documentation describes AI credits as the billing unit. On that reading the
credit figure is now *the* number and premium requests are legacy accounting
retained for continuity. The rule is kept anyway, for a reason that is about
this repository rather than about GitHub:
**the premium-request column is the only figure here that a reader can check against a bill they have seen.**
A page that dropped it would become unfalsifiable by its own audience at exactly
the moment it started claiming a dollar total. It is demoted, not deleted, and
the dashboard labels it as the legacy unit.

## The number this page deliberately does not compute

Two of them, in fact. The first is below; the second is a completion rate.

The dashboard now carries a **plan coverage** panel, built from the session's
own todo list — a second SQLite file the CLI keeps beside the billing store,
keyed by the same session id, so the plan joins to the money.

The obvious headline from that list is *153 of 153 items done*.
**That figure is not reported, and would not be worth reporting.**
It reads 100 % because of how a working list is used rather than how the work
went: items are closed as the session goes, so anything abandoned was either
closed or never written down. The rate measures tidying. A number that reads
100 % for every session, forever, separates nothing, and publishing it would
have been worse than publishing nothing at all.

What is reported is **coverage weighted by spend**: the share of billed requests
made on a day that had any plan written for it. For this project that is
**about 91 %**, with three working days — 7, 9 and 10 August — carrying
**roughly 430 requests and no plan at all.**
Those days are named on the page rather than smoothed away, because that is
where unplanned spend hides. The exact counts move with every rebuild, for the
reason given in entry 8 below; the dashboard is the current figure and this
paragraph is the shape of it.

A second caveat sits on the same panel. How long an item stayed open is mostly
**not measurable**: the store's `updated_at` defaults to `created_at`, so an
item created and closed without an intervening status change records a
zero-second lifetime, which means *never observed in progress* and not *done
instantly*. That is **119 of the 153 items**. The median is therefore quoted
over the 34 items where it is real, with that count printed beside it.
Averaging the other 119 in as zeroes would have halved it and produced a
fiction.

Coverage measures whether a plan was **written**, not whether it was followed.
It is a floor on deliberateness, not a measure of it.

---

A cost is meaningless without a comparator, and the obvious comparator —
what the same work would have cost from a consultancy —
**is not computed here**,
because doing it properly requires an entirely separate evidence base:
published labour rates, obligated contract dollars, and a scope map from
countable repository artifacts to billable work packages.

That is [Document 9, the procurement comparison](../procurement/README.md),
with its own dashboard at
[`procurement-dashboard.html`](../procurement/procurement-dashboard.html).

It reaches a conclusion that constrains how this page may be read.
**The measured $437.35 on this page must never be divided into a consultancy estimate to produce a saving ratio**,
because the numerator is 5/5 measured and
the denominator is 1/5 invented. Document 9 states that refusal as its opening
card. It also prices the human direction this ledger cannot see — between eleven
and thirteen hours of active attention, which at four different published and
stated rates comes to **between 4.8 and 30.5 times the entire metered inference cost**. The multiple never falls below five, whichever rate is chosen.

## Energy

No joules reach a client. The energy panel multiplies a published per-query
figure by an exact request count, which makes it an estimate stapled to a fact.

> we estimate a median energy per query of 0.34 Wh (IQR: 0.18-0.67) for
> frontier-scale models (>200 billion parameters) ... Extending to test-time
> scaling scenarios with 15x more tokens per typical query, the median energy
> rises 13-fold to 4.32 Wh

&mdash; Oviedo, Kazhamiaka, Choukse, Kim, Luers, Nakagawa, Bianchini and Lavista
Ferres, *Energy Use of AI Inference: Efficiency Pathways and Test-Time Compute*,
*Joule*, 2025.
[Publication page.](https://www.microsoft.com/en-us/research/publication/energy-use-of-ai-inference-efficiency-pathways-and-test-time-compute)

**Neither published regime describes this workload.** The regimes are separated
by output length. These requests are short in output and extremely long in
input, and nearly all of that input is served from a prompt cache, which is a
different computation from a fresh prefill. The bracket spans a factor of
twenty-four and no arithmetic available here narrows it. What would narrow it is
a per-request energy figure returned by the server, which is the one item on the
instrumentation list a client cannot supply for itself.

## The store is per machine, and this project outgrew one machine

Everything above is read from `~/.copilot/session-store.db` on **one** machine.
Four sibling repositories &mdash; `dumbo-district-3d`, `manhattan-bridge-3d`,
`brooklyn-bridge-3d` and `williamsburg-bridge-3d` &mdash; are part of the same
project and were worked on from a second one. Their cost is real and this
dashboard could not reach it. There is no API to ask: the store is a local
SQLite file and nothing uploads it.

The temptation was to say nothing, because the number that results still looks
like a total. It was not one. Until those four repositories were exported,
every figure here was
**exact for this repository and a floor for the project**,
and the page said so on the cost tile, in a card naming the four,
and in the wrong-list. What could be seen from here was fetched anyway
&mdash; commit counts and dates live on GitHub &mdash; so the card showed
repositories with commits and the words "not measured" in the two columns that
mattered. A stated hole is evidence. An unstated one is an understatement.

`usage-calc export` closed it. It runs on the other machine as a single
standalone script, needs no checkout and no dependencies, and writes one JSON
file per session into `usage/contrib/`, from which the generator merges. It
carries counts, timestamps, durations, model names and prices, and carries
**no prompt text, responses, file contents, turn labels or summaries.**
A contribution says what was
spent, not what was said. The generator refuses any file whose per-request
costs do not sum to its stated total, and skips any file describing the session
it is already reading live, because counting both would double the page.

`usage-calc report` is the companion, meant to be run on the contributing
machine. It reads the contributions directory and prints the merge to a
terminal without writing `usage-data.json` or touching the dashboard &mdash;
which is the right shape there, because that machine holds no session for
*this* repository and running the full generator would publish a dashboard
headlined by a bridge repo. It states its scope before its first number for the
same reason: run here it omits the primary session, so its total is the
contribution side of the merge ($878.52) rather than the project total.

### What the gap turned out to be worth

Four contributions arrived and the totals moved by more than half. Figures
below are the snapshot of 2026-08-10; the live page recomputes them, and this
session's own requests keep landing in the left-hand column:

| | this repository | all five, merged |
| --- | --- | --- |
| Requests | 4,711 | 8,086 |
| Turns | 70 | 121 |
| Cost | $599.62 | $1,484.30 |
| Model work | 16.75 h | 28.20 h |
| Model wall | 14.95 h | 24.65 h |

**The unmerged figure was 40 per cent of the number.** Anyone quoting it as
the project's cost would have understated it by two and a half times, and
nothing on the page would have looked wrong.

Two properties of the merged data are worth stating because neither was
predictable from this repository alone. All four sibling repositories were
worked on **within a single day**, 2026-08-09, which is why that one day
carries close to $900 and 13 engaged hours against a median day of about
1.5 h. And
**3.56 h of model work &mdash; 12.6 per cent &mdash; ran concurrently**,
two machines generating at the same wall-clock moment. That is
the figure a summed total would have hidden.

### Merging is not adding

**Money is additive and a person is not.**

| Quantity | Across machines | Why |
| --- | --- | --- |
| Requests, tokens, cost | **Sum** | Two machines spending at once really do spend twice |
| Model work seconds | **Sum** | Both models really were generating |
| Model wall time | **Union** | Only one minute of clock passed |
| Engaged time | **Union of sittings** | One person, who cannot be at two keyboards at once |
| Person time | **Recomputed** from the merged clock | Never the sum of per-machine residuals |

Summing per-machine person-hours is the specific error this design exists to
avoid: it inflates the weakest column on the page, and it does it invisibly.
The gap between the sum and the union is reported directly as *concurrent
time*, and in the real data it is 3.56 h.

### The cut-off belongs to the person, not to the keyboard

The first working merge got this subtly wrong, and the error was only visible
because two cards on the same page disagreed by nine minutes about the same
quantity. Sittings were being cut **per source** and then unioned. That applies
the idle cut-off to a machine: a three-minute gap counts as engaged when both
requests land on one keyboard and as a pause when the second lands on the
other &mdash; which is the same person turning to the other screen.

It contradicts the rule in the table above while appearing to implement it.
The cut is now taken over the pooled stream, and the two readings are both
published so the choice is checkable rather than buried:

| Cut-off | Per machine | Pooled | Bridged |
| --- | --- | --- | --- |
| 2 min | 30.88 h | 30.91 h | +2.2 min |
| 5 min | 32.07 h | 32.23 h | +9.5 min |
| 10 min | 35.54 h | 35.71 h | +10.1 min |
| 30 min | 39.62 h | 39.98 h | +21.4 min |

The gap widens with the cut-off, which is the signature of the mechanism
rather than of a rounding error: a longer cut-off bridges more gaps, so it
bridges more cross-machine ones. The verifier now asserts pooled is never
below per-machine, so this cannot quietly revert.

## Nothing has to be collected in advance

A reasonable worry, given how much of the above is about exporting and
merging, is that this telemetry only exists because it was gathered on
purpose. It is not. The client writes `assistant_usage_events` as it goes,
one row per request, and `sessions.repository` and `sessions.cwd` record
which project each row belongs to. Nothing needs to be running, scheduled or
remembered. `usage-calc export` exists to move that record *between
machines*, not to create it.

So a question like "what has this machine been doing this week, by project"
is answerable at any moment, retrospectively, for work nobody instrumented.
`usage-calc query` asks it:

```
usage-calc query                  # last 7 days, by project/session
usage-calc query --days 30
usage-calc query --by day         # or model, or repo
usage-calc query --all --json
```

It is read-only, snapshots the store before reading so it is safe to run
while the CLI is working, and needs no checkout of anything.

### Two aggregations that look obvious and are wrong

The reason this is a script rather than a line of SQL is that the two
natural `SUM()`s both mislead, and neither announces it.

**`SUM(duration_ms)` overstates model time.** Sub-agent requests run *beside*
the main agent, not after it, so their durations overlap in wall-clock time.
The first version of this query, written in a single pass, reported 16.79 h
for this repository's session against a true union of 14.99 h &mdash;
**12 per cent high**, and higher still over a week of heavy sub-agent use
(15.2 per cent). The tool unions the intervals and prints both figures with
the reason for the difference, because a reader who has just run `SUM` needs
to know why the numbers disagree.

**`SUM(input_tokens)` disagrees with the billing detail.** `token_details_json`
is a list of per-channel entries carrying their own rates; it is what
reconciles to the recorded cost, and it disagrees with the flat columns on
compaction rows. The tool reads the details and falls back to columns only
where the details are absent.

The tool and the dashboard are independent implementations. Filtered to the
dashboard's generation timestamp they agree exactly &mdash; 4,711 requests,
70 turns, $599.62, 14.948 h &mdash; on all four measures. That agreement is
the check that either of them is right.

### What is retained, and the part that is not established

Usage rows in this store go back to 2026-08-01, which is when this project
began, and the first row is the first request of the session rather than an
arbitrary cut. **Nothing has been pruned in the ten days since**, and the
daily series is continuous over that span. Sessions from 2026-06-16 survive
with their turns intact but carry no usage rows at all, which is most
consistent with the telemetry table arriving after them rather than with
their usage being deleted.

What that does **not** establish is the absence of a longer retention window.
This store contains no usage older than ten days, so a thirty- or ninety-day
policy would be invisible here and this evidence cannot exclude it. Anyone
depending on a long historical window should export periodically rather than
assume the store is an archive &mdash; which is what `usage-calc export`
already does, and is a second reason to run it that has nothing to do with
having two machines.

## Where this is likely to be wrong

1. **The dollar figure is a list-price equivalent, not a bill.** See "two
   numbers" above. If one figure from this work is quoted, both should be.
2. **The credit-to-dollar conversion is documented; its application here is not.**
   GitHub states that 1 AI credit = $0.01. It does not state that the
   `total_nano_aiu` column in a local CLI store is denominated in the same
   credit. That step is still an inference, and it is the one an auditor should
   attack first.
3. **Engaged time cannot distinguish thinking from absence.** It also cannot see
   time spent reading output after the last request of a sitting, which is
   exactly when a reader of a research document would spend it.
4. **The daily person column errs in both directions and is not a bound.** It is
   engaged minus model, so it inherits everything in entry 3 and adds nothing to
   correct it. Read the model column as the measurement and the person column as
   the part that is left, and read both across the cut-off selector rather than
   at one setting. Anyone quoting a person-hours figure from this page should
   quote the range, not the default.
5. **The dates are a property of this store, not of the project.** "Research
   started" is the first request recorded in this session's rows, and any
   thinking, reading or writing done before or outside it is invisible. "Last
   updated" prefers the most recent commit, which means committing this
   dashboard changes the number the dashboard displays &mdash; the same
   self-measurement problem as entry 7, in a place where it is easier to miss.
6. **The energy panel applies a source outside its stated domain.** Rated 2/5 as
   applied, and the bracket is reported instead of a point estimate for that
   reason.
7. **The output side counts artifacts and appraises nothing.** This repository
   has withdrawn several published claims; each withdrawal improved the work and
   reduced the word count. A cost-per-word figure prices typing.
8. **The instrument measures itself.** Building this dashboard cost requests
   that appear in the next run of the generator, so the totals were already
   stale when they rendered. A self-measuring instrument cannot record its own
   last measurement.
9. **Retention is not guaranteed, and it has only been tested to ten days.**
   The store held one project cleanly and pruned nothing over the span this
   work occupies. But it contains no usage older than ten days, so a
   thirty- or ninety-day expiry policy would be invisible here and this
   evidence cannot exclude one. Nothing promises the rows will be there next
   month, and a case study whose evidence expires is an anecdote.
10. **The totals cover every machine anyone remembered.** The store is per
    machine and this project was worked on from two; the second one's four
    repositories are now merged in, and they turned out to be 60 per cent of
    the project. That is exactly why the residual risk matters: nothing on
    this page can detect a *third* machine nobody remembered. The merge can
    only be as complete as the set of files it was handed, and its
    completeness is asserted by a person rather than measured.
11. **Concurrent time is measured; simultaneous attention is not.** The page
    reports 3.56 h during which two machines were generating at once. It does
    not follow that a person was attending to both. The concurrency figure
    corrects the *clock*; it says nothing about how divided the direction was,
    and if anything it is a reason to read the person residual as even softer
    on those hours than elsewhere.
12. **Plan coverage sees whether a plan existed, not whether it was any good.**
    A day with forty unrelated todos scores the same as a day that was
    genuinely thought through. It is a floor on deliberateness. Nor does it
    reach the other machine: the four sibling repositories contribute their
    spend to this page but their todo lists live in that machine's own state
    directory, so the coverage figure is scoped to this session's requests
    while the fleet totals beside it are not.
13. **Three uncovered days is not automatically three days of waste.** Some work
    is one long obvious task and writing it down would be ceremony. The figure
    is a question worth asking, not a verdict already reached.

## Process note: a claim this directory made and withdrew

Kept at the end rather than the beginning. It is a note about how the work was
done, and putting it above the ledger asked every reader to absorb a retracted
claim before reaching a single figure.

The first conclusion reached about this project's own usage was that there was
none to read. The VS Code extension writes a debug log at
`%APPDATA%\Code\User\workspaceStorage\<hash>\GitHub.copilot-chat\debug-logs\<session>\main.jsonl`,
and that file was inspected and found to contain nineteen `session_start`
records and nothing else. The conclusion drawn from it was:

> There are no per-request rows, no model names, no token counts, no costs.
> The environment does not record the thing that is being asked for, so the
> dashboard's first job is to say so.

That is withdrawn. It was the wrong file. The Copilot CLI keeps a separate
store at `~/.copilot/session-store.db`, and its `assistant_usage_events` table
carries one row per request issued to a model, with the model id, the token
count on each billing channel, the cost, the wall duration, the turn index and
the id of the tool call that spawned any sub-agent request.

The error is recorded rather than quietly fixed because of what it nearly
produced. "The data does not exist" is a comfortable finding: it is
unfalsifiable, it flatters the investigator, and it would have been published
as the central result of a case study whose entire purpose was measurement.
It is also the exact inverse of the claim this page now makes &mdash; that the
unit is documented, the ledger is readable, and the reason so little work of
this kind is published is not that the data is missing.
