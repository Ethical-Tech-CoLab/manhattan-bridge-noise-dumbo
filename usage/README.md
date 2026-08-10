# Usage: what this investigation cost, and how that was established

**Dashboard:** [`usage-dashboard.html`](usage-dashboard.html) &middot;
**Data:** [`usage-data.json`](usage-data.json) &middot;
**Generator:** [`build_usage_data.py`](build_usage_data.py)

This directory answers a question about the study rather than a question about
the bridge: what did producing this repository consume, and what would have to
be instrumented to answer that properly next time.

It is deliberately separable. Nothing in `build_usage_data.py` knows about the
Manhattan Bridge. Point it at another working directory and it produces the
same JSON and the same page.

```
python usage/build_usage_data.py                # this repository
python usage/build_usage_data.py --list         # every session in the store
python usage/build_usage_data.py --cwd C:\Dev\Other
python usage/build_usage_data.py --session <uuid> --no-inject
```

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
dashboard cannot reach it. There is no API to ask: the store is a local SQLite
file and nothing uploads it.

The temptation is to say nothing, because the number that results still looks
like a total. It is not one.
**Every figure on the dashboard is exact for this repository and a floor for the project.**
The page now says so in three places: on the cost tile, in a card that names
the four repositories, and in the wrong-list.
What can be seen from here is fetched anyway &mdash; commit counts and dates
live on GitHub &mdash; so the card shows a repository with twelve commits and
the words "not measured" in the two columns that matter. A stated hole is
evidence. An unstated one is an understatement.

`usage/export_session.py` closes it. It runs on the other machine, needs no
checkout and no dependencies, and writes one JSON file per session into
`usage/contrib/`, from which the generator merges. It carries counts,
timestamps, durations, model names and prices, and carries
**no prompt text, responses, file contents, turn labels or summaries.**
A contribution says what was
spent, not what was said. The generator refuses any file whose per-request
costs do not sum to its stated total, and skips any file describing the session
it is already reading live, because counting both would double the page.

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
time*. Exercising the merge on two unrelated local sessions found 325 seconds
of it &mdash; five and a half minutes during which two machines were genuinely
generating at once, which a naive sum would have counted as eleven.

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
9. **Retention is not guaranteed.** The store held one project cleanly. Nothing
   promises it will next month, and a case study whose evidence expires is an
   anecdote.
10. **The totals are a floor, not a total.** The store is per machine and this
    project was worked on from two. Four sibling repositories contribute
    nothing to any figure here until someone runs the exporter on the other
    machine. Worse, nothing on this page can detect a *third* machine nobody
    remembered: the merge can only be as complete as the set of files it was
    handed, and its completeness is asserted by a person rather than measured.

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
