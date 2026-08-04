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

## The correction this directory opens with

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

## Where the numbers come from

| Field | Source | Rating |
| --- | --- | --- |
| Requests, models, tokens, cost, duration, turn, sub-agent id | `~/.copilot/session-store.db`, table `assistant_usage_events` | 5/5 VERIFIED |
| Per-model token prices | `models.json`, written beside the client's debug log | 5/5 VERIFIED |
| One AIU = one US cent | Inferred by matching the above against vendor list prices | 4/5, see below |
| Commits, line counts, file counts, word counts | `git` in this repository | 5/5 VERIFIED |
| Energy per request | Oviedo et al., *Joule*, 2025 | 5/5 for the figure, 2/5 applied here |
| Household electricity | US EIA, *Electricity use in homes* | 5/5 VERIFIED |

### The unit

The store prices each request in **nano-AIU**. Nothing states what an AIU is.
It is taken here to be one US cent, on four independent agreements:

| Model | Catalogue rate, in / out | Vendor list price |
| --- | --- | --- |
| `claude-sonnet-4.5` | 300 / 1500 | $3.00 / $15.00 per 1M |
| `claude-haiku-4.5` | 100 / 500 | $1.00 / $5.00 per 1M |
| `claude-opus-4.6` | 500 / 2500 | $5.00 / $25.00 per 1M |
| cache channels, all Anthropic models | 0.1x base read, 1.25x base write | the published cache multiples |

Three separate models and both cache ratios land on the cent. That is a strong
inference. It is still an inference, and the dashboard says so where it prints
a dollar sign.

### The rule the generator enforces

Cost and token totals are read from `token_details_json`, **not** from the
`input_tokens` and `cache_write_tokens` columns beside it. The script recomputes
the cost of every row from the details and refuses to write output if any row
disagrees with the cost the client recorded. On the current data all rows
reconcile exactly.

## Four traps, in the style of the seven in `data-collection`

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

## Two numbers, and why both have to be quoted

| | |
| --- | --- |
| **List-price token cost** | what the tokens would cost at the published per-model rates |
| **Premium requests** | what a Copilot subscription actually bills, one per user-initiated turn, at the recorded multiplier |

These differ by more than two orders of magnitude, and they cannot be
reconciled: **nothing available to a client maps one onto the other.** Quoting
the first alone overstates what anyone paid. Quoting the second alone hides what
was consumed. The dashboard prints both, adjacent, and refuses to derive a third
number from them.

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

## Where this is likely to be wrong

1. **The dollar figure is a list-price equivalent, not a bill.** See "two
   numbers" above. If one figure from this work is quoted, both should be.
2. **The AIU-to-cent identification is inferred.** Four agreements is strong
   evidence and not documentation.
3. **Engaged time cannot distinguish thinking from absence.** It also cannot see
   time spent reading output after the last request of a sitting, which is
   exactly when a reader of a research document would spend it.
4. **The energy panel applies a source outside its stated domain.** Rated 2/5 as
   applied, and the bracket is reported instead of a point estimate for that
   reason.
5. **The output side counts artifacts and appraises nothing.** This repository
   has withdrawn several published claims; each withdrawal improved the work and
   reduced the word count. A cost-per-word figure prices typing.
6. **The instrument measures itself.** Building this dashboard cost requests
   that appear in the next run of the generator, so the totals were already
   stale when they rendered. A self-measuring instrument cannot record its own
   last measurement.
7. **Retention is not guaranteed.** The store held one project cleanly. Nothing
   promises it will next month, and a case study whose evidence expires is an
   anecdote.
