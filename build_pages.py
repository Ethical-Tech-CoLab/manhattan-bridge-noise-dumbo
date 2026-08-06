#!/usr/bin/env python3
"""
build_pages.py - regenerate the GitHub Pages site from the repository itself.

The site has two parts:

    index.html      the organising page: where the investigation stands,
                    what has been found, what is still to be done, and a
                    link to everything else.

    read/*.html     one rendered page per markdown document, so that the
                    research is readable in a browser without cloning the
                    repository or trusting GitHub's markdown viewer.

Everything countable on those pages is PARSED OUT OF THE REPOSITORY at build
time - method counts and their statuses, question numbers, word counts, file
sizes, the commit date. Nothing is typed in by hand, because hand-typed counts
go stale silently and this programme has already published stale counts twice.

The markdown files remain authoritative. These pages are rendered copies and
say so.

Usage:
    pip install markdown
    python build_pages.py

Re-run after editing any document. Commit the output.
"""

import io
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

try:
    import markdown
except ImportError:
    sys.exit("This script needs the 'markdown' package:  pip install markdown")

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = "Ethical-Tech-CoLab/manhattan-bridge-noise-dumbo"
BLOB = "https://github.com/" + REPO + "/blob/main/"
ISSUES = "https://github.com/" + REPO + "/issues/"

# ---------------------------------------------------------------------------
# What is in the repository
# ---------------------------------------------------------------------------

# (source path, output slug, short title, nav label, one-line description)
DOCS = [
    ("README.md", "readme", "Repository README", "README",
     "The argument in brief, the document index, and the method register with "
     "its honest status column."),
    ("IDEA-CONCEPT.md", "idea-concept", "1. Idea and concept", "1. Concept",
     "What is the problem? Defines it from agency evidence, establishes who is "
     "responsible under what law, and derives the questions nobody has asked of "
     "this site."),
    ("PRECEDENT-AND-MATERIALS.md", "precedent-and-materials",
     "2. Precedent and materials", "2. Precedent",
     "What has the world already built? Elevated-transit noise mitigation in "
     "Japan, China, Sweden, Germany, Hong Kong, Australia and Chicago - and what "
     "actually transfers to a 1909 suspension bridge."),
    ("WILLIAMSBURG-COMPARATOR.md", "williamsburg-comparator",
     "3. Williamsburg comparator", "3. Comparator",
     "There is a second bridge with the same owner, operator, rolling stock and "
     "statute. What does it already tell us, and what would measuring it "
     "establish?"),
    ("VISUAL-MODEL-FRAMEWORK.md", "visual-model-framework",
     "4. Visual model framework", "4. Visual model",
     "Every argument in the first three documents is an argument about a "
     "cross-section nobody has drawn. Can that drawing be built from open data - "
     "and made to admit what it does not know?"),
    ("FIELD-CAPTURE-PROTOCOL.md", "field-capture-protocol",
     "5. Field capture protocol", "5. Field capture",
     "Every acoustic claim beyond the published levels is invented. Can a "
     "consumer phone fix that this month?"),
    ("COMMUNITY-EVIDENCE-AUDIT.md", "community-evidence-audit",
     "6. Community evidence audit", "6. Community",
     "The people who live under it have been complaining since 2008. What have "
     "they already recorded, and why can nobody find it?"),
    ("data-collection/README.md", "data-collection", "7. Data collection",
     "7. Data",
     "How many trains, how many people, and for how long? Runnable scripts "
     "against MTA and NYC open data - and the traps that each silently produce a "
     "plausible wrong number."),
    ("pedestrian-site-visits/README.md", "pedestrian-site-visits",
     "10. Field media", "10. Field media",
     "The first material here that was not retrieved from somebody else: two "
     "days of phone video, stills, by-product audio and stopwatch laps under "
     "the bridge - and a v1.1 that withdraws v1.0's headline in place."),
    ("usage/README.md", "usage", "8. AI usage and cost", "8. AI Usage",
     "What did producing this repository consume? A per-request ledger read "
     "from the tool's own store, set against the argument that inference is "
     "becoming metered infrastructure - and what follows from measuring it."),
    ("procurement/README.md", "procurement", "9. What this would have cost to buy",
     "9. Procurement",
     "What would the same deliverable have cost from a large schedule holder or the "
     "cheapest decile of the same schedule? Three instruments, reported side "
     "by side and never averaged - and the disagreement between them is the "
     "result."),
]

# What each document FOUND, as against what it asks. One line each, shown on
# the research hub so a reader can choose a document by its result rather than
# by its title.
#
# EVERY LINE HERE IS A STATEMENT ALREADY PUBLISHED ELSEWHERE ON THIS SITE - in
# the README's headline findings, in the document's own abstract, or in the
# method register. Nothing in this table is a new claim, and nothing in it may
# say more than the document it points at. A hub that summarises by
# paraphrasing is a hub that drifts away from what it indexes; the build
# fails below if a document has no entry, so adding a document forces the
# question "what did it find?" to be answered rather than skipped.
HIGHLIGHTS = {
    "readme": "The register with its honest status column: <b>{methods} "
              "methods specified, {done} executed or partly.</b> It does not "
              "hide the ratio.",
    "idea-concept": "The MTA measured the noise, in DUMBO, at named "
                    "addresses, and published the levels. <b>The levels are "
                    "high and nothing followed.</b>",
    "precedent-and-materials": "Floating slab track, constrained-layer "
                               "damping, rail dampers and parapet treatments "
                               "all exist and work &mdash; <b>on structures "
                               "that were designed to carry them.</b> This "
                               "one was built in 1909 and its load budget is "
                               "the constraint everything else answers to.",
    "williamsburg-comparator": "A second bridge with the same owner, "
                               "operator, rolling stock and statute is the "
                               "cheapest control this problem will ever get, "
                               "and <b>nobody has measured the pair.</b>",
    "visual-model-framework": "A drawing can be built from open data, and the "
                              "useful part is what it refuses to draw: "
                              "<b>turn every provenance filter off and the "
                              "viewport goes empty.</b> That is the state of "
                              "public knowledge.",
    "field-capture-protocol": "Five captures, a phone already owned, and no "
                              "permission needed. <b>C2, the temporal "
                              "envelope, is the one measurement that could "
                              "prove this repository wrong.</b>",
    "community-evidence-audit": "Within 500&nbsp;m of the MTA's own "
                                "measurement, residents filed <b>4,055 noise "
                                "complaints since 2020 and not one of them "
                                "can be about the train.</b> There is no "
                                "category for it.",
    "data-collection": "Six scripts, and four traps that each silently "
                       "produce a plausible wrong number. <b>The turnstile "
                       "feed's <code>entries</code> field means people "
                       "leaving, not arriving</b>, and reading it the natural "
                       "way inverts the day.",
    "pedestrian-site-visits": "The first material here that was captured "
                              "rather than retrieved &mdash; and <b>v1.1 "
                              "withdraws v1.0's headline</b>, because two "
                              "correctly-computed datasets were joined that "
                              "had never been joined in the field.",
    "usage": "<b>Human direction time costs about eight and a half times the "
             "entire metered inference bill.</b> That is the opposite of the "
             "usual claim, and it is measured rather than asserted.",
    "procurement": "Three instruments, reported side by side and never "
                   "averaged. <b>The disagreement between them is the "
                   "result</b>, and the obvious headline is withdrawn before "
                   "it is made.",
}

# Documents about the work rather than about the bridge. They are research and
# they are linked from every page - but they are grouped apart in the nav and
# placed last on the index, because someone arriving here is looking for the
# noise problem, not for what it cost to study it.
BEHIND_THE_SCENES = {"usage", "procurement"}

# (path, kind, title, what it demonstrates, what to look at first)
ARTIFACTS = [
    ("visual-review/acoustic-demo.html", "Audio", "Acoustic demonstration",
     "Web Audio synthesis pinned to the MTA's own measurements. Six receptors, "
     "single pass-by or continuous running at the measured headway, A-weighted "
     "meters, CEQR threshold marks and a running energy average.",
     "Start at the Brooklyn Bridge Park dog run, play one pass-by, then switch "
     "to continuous at 20x speed and watch the running average settle onto "
     "87.50 - then read why that convergence is a closed loop and not evidence."),
    ("visual-review/model-3d.html", "Bridge", "Navigable 3D model",
     "Both bridges, four zoom tiers from the whole crossing down to a single "
     "rail fastener, with anchored callouts, click-to-inspect components and a "
     "live scale bar that reads in inches at the finest tier.",
     "Turn every provenance filter off. The viewport goes completely empty and "
     "the display says so. That is the state of public knowledge."),
    ("visual-review/section-problem.html", "Bridge",
     "Provenance-tagged section",
     "The 2D cross-section of the Manhattan Bridge track zone, every component "
     "colour-coded and dash-coded by how well it is actually known, with the "
     "source rubric attached to the drawing.",
     "Turn off the DOCUMENTED filter and watch most of the drawing disappear."),
    ("visual-review/frequency-dashboard.html", "Data",
     "Frequency and exposure dashboard",
     "Traversals by hour, route and direction across day, evening and night; "
     "pedestrian arrivals, departures, walkway flow and residents; and a "
     "four-cohort presence model that publishes its own non-identifiability.",
     "Drag the coincidence window from 1 s to 29 s. The answer does not move - "
     "which is a finding about the feed, not about the railway."),
    ("visual-review/noise-canyon.html", "Bridge", "The noise canyon",
     "A five-slide picture essay drawn entirely from open data: the structure "
     "photographed, 76 surveyed buildings extruded around the alignment, a true "
     "section cut across the corridor, the ordinary walk in from the York "
     "Street F platform, and every point along it anyone has ever measured.",
     "The last slide. Four narrow bands of measured evidence against 1,482 m "
     "of walk - 23% - and the shaded field is not quiet, it is unmeasured."),
    ("visual-review/agent-model.html", "Agents", "Agentic population model",
     "Groups - not individuals - enter DUMBO at persona-specific gateways, "
     "follow scenario itineraries, contend for capacity and accumulate a noise "
     "dose along their actual path. Deterministic, seeded, fully event-logged. "
     "A fifth rung models who is standing in that dose - reduced sound "
     "tolerance, autistic listeners with hyperacusis, over-65s, carried "
     "infants, people with a history of cancer, and dogs - and changes "
     "nobody's decibels by doing so. Three selectable arrival processes let "
     "the same population walk in as a flat trickle, at random, or in slugs "
     "off a train.",
     "The first panel: the same itinerary started ninety seconds apart gets a "
     "different dose. Then the arrival card, where multiplying peak bunching "
     "by 4.2 times moves the mean dose by 0.001 dB - and the reason it does "
     "not move is the interesting part. Then the rejected-propagation panel, "
     "which is a negative result and the most important thing on the page. "
     "Then, at the "
     "susceptibility rung, the card that refuses to compute the one number "
     "that would settle the argument, and names the single measurement that "
     "would unblock it."),
    ("pedestrian-site-visits/media.html", "Field", "Field media, first capture",
     "Two days of phone video, stills, by-product audio and stopwatch laps "
     "under the bridge: level traces, a threshold sweep, the stopwatch laps, "
     "and where each capture stood against every point anyone has ever "
     "measured - with the operator's stated purpose for each capture carried "
     "on the page, because a measurement can only be read for the purpose it "
     "was taken for.",
     "The withdrawal card, which quotes this page's own strongest claim from "
     "the day before and kills it - the audio and the stopwatch are "
     "independent samples 62.4 minutes apart. Then the echo-chamber frames, "
     "which are what the video was actually for."),
    ("usage/usage-dashboard.html", "Meta", "Usage and cost dashboard",
     "What this investigation cost to produce, from the tool's own per-request "
     "log: every model call priced by channel, time measured four ways that "
     "disagree by an order of magnitude, and an energy bracket that spans a "
     "factor of twenty-four because nothing here is a measured joule.",
     "The two bars under the ledger: what an agent reads is most of the tokens "
     "and half the money; what it writes is under one per cent of the tokens "
     "and a fifth of it. Then the process note at the foot - the first "
     "conclusion this dashboard reached about itself was that the data did not "
     "exist, and that was wrong."),
    ("procurement/procurement-dashboard.html", "Meta",
     "Procurement comparison dashboard",
     "What this same deliverable would have cost to buy, from three "
     "instruments that are never averaged: dollars actually obligated on 56 "
     "federal noise-study contracts, a bottom-up build at GSA awarded ceiling "
     "rates verified cent-for-cent against a vendor's own card, and the "
     "metered inference ledger.",
     "The first card, which withdraws the headline before it is made. Then "
     "the discipline populations near the foot: 12,825 project managers "
     "against seven acoustical engineers on the same schedule - and the "
     "project manager costs more per hour."),
]

# Above-the-fold statements on the index page.
#
# TO ADD A CARD:    append one tuple (big, unit, line, href_or_None)
# TO REMOVE A CARD: delete the tuple
# TO REORDER:       move it. Order here is order on screen.
#
# `big` may contain {q}, {methods} or {words}, substituted from the repository
# at build time, so a card can quote a live count without anyone maintaining it.
#
# Keep every one of these traceable to something on the site. A large number
# with no destination is a poster, not a research index.
HERO_CARDS = [
    ("98.9", "dB(A) average maximum",
     "measured by the MTA in Brooklyn Bridge Park, at the dog run",
     "read/idea-concept.html"),
    ("67", "trains an hour, overhead",
     "at the weekday peak, one crossing every 54 seconds",
     "visual-review/frequency-dashboard.html"),
    ("4,055", "noise complaints since 2020",
     "within 500 m of that measurement, and not one can be about the train",
     "read/community-evidence-audit.html"),
    ("17.3", "dB above the fit",
     "the dog run sits this far over ideal line-source spreading, so the "
     "three-point agreement that looked like a result was a coincidence",
     "visual-review/agent-model.html"),
    ("23%", "of the walk measured",
     "four bands of instrument data along 1,482 m from the F train to the water",
     "visual-review/noise-canyon.html"),
    ("{q}", "questions nobody had asked",
     "an open, unfinished investigation that works by finding the question the "
     "record skipped, then writing it so it can be proved wrong",
     "research.html#method"),
]

SCRIPTS = [
    ("data-collection/bridge_schedule.py",
     "Counts scheduled Manhattan Bridge traversals from the MTA GTFS static "
     "feed, by hour, route and direction."),
    ("data-collection/bridge_realtime.py",
     "Polls GTFS-realtime for actual traversals. Built and verified; the "
     "week-long run has not been done."),
    ("data-collection/build_dashboard_data.py",
     "Assembles the frequency dashboard's dataset, including the coincidence "
     "analysis that exposed the feed's 30-second quantisation."),
    ("data-collection/build_pedestrian_data.py",
     "Derives arrival rate, departure rate, walkway flow and resident count "
     "from four public datasets. Disproved this repository's own claim about "
     "which hour is worst."),
    ("data-collection/build_cohort_model.py",
     "Fits four population cohorts to the observed departure curve and reports "
     "the range across every parameter set that fits equally well - which is "
     "how the non-identifiability result was found."),
    ("data-collection/fetch_geodata.py",
     "Fetches NYC building footprints with surveyed roof heights and the "
     "OpenStreetMap street, park, water and footway network for the corridor. "
     "The reproducibility path for every line in the noise-canyon drawings."),
    ("build_carousel.py",
     "Draws the noise-canyon slides from that geodata and emits the page. "
     "Slides are declared in visual-review/carousel.json, and the build "
     "refuses to run if any of them lacks a source or a caveat."),
    ("make_hero.py",
     "Composites the hero band on this page from a public-domain HAER "
     "photograph and a render taken from this repository's own 3D model."),
]

DATASETS = [
    ("data-collection/dashboard-data.json",
     "Traversal counts by hour, route, direction and period."),
    ("data-collection/pedestrian-data.json",
     "Turnstile entries, origin-destination arrivals, walkway counts, residents."),
    ("data-collection/cohort-data.json",
     "The admissible cohort parameter family and the presence ranges it implies."),
]

# Work that is finished, shown with a marker on the index.
#
# The second field is EITHER a method number in the README register - in which
# case build_index reads the marker out of the register and refuses to build if
# the register disagrees - OR the literal "done" / "partial" for work that is
# not a numbered method. Nothing here types its own completeness for a method:
# a green tick this page asserts and the register denies is exactly the drift
# the programme exists to avoid.
#
# "partial" means THE WORK WAS DONE AND THE RESULT WAS NOT OBTAINED. It draws a
# different marker, because a full tick beside "the week has not been run"
# would overstate it.
DONE = [
    ("Method 38 - the first captured field material", 38,
     "One afternoon, a phone already owned",
     "Two days of video, stills, by-product audio and stopwatch laps under "
     "the bridge - <b>the first material in this repository that was captured "
     "rather than retrieved</b>. It delivered <b>the first photographic record "
     "of the echo chamber</b> the repository had until then only modelled from "
     "surveyed footprints, the geometry of every capture, and a rate that "
     "agrees with the timetable inside an interval wide enough to say so "
     "plainly. <b>It also produced this repository's fastest withdrawal</b>: "
     "v1.0 used an audio duty cycle to refute a reading of the stopwatch, and "
     "v1.1 withdrew that one day later, because the two are independent "
     "samples 62.4 minutes apart. Every number in the withdrawn claim was "
     "computed correctly - what was wrong was joining two datasets that were "
     "never joined in the field, which no check here can catch."),
    ("Method 33 - the cost of the study itself", 33,
     "One SQLite read, free",
     "A per-request ledger of what producing this repository consumed, priced "
     "by billing channel from the tool's own log. <b>It opens by withdrawing "
     "its own first conclusion</b> - that no such data existed - which had been "
     "reached from the wrong file and was three minutes from being published as "
     "the finding. It reports <b>no measured energy at all</b>, because none "
     "reaches a client."),
    ("Method 32 - the corridor geometry", 32,
     "Two open datasets, no key, about a minute",
     "The canyon under the bridge, drawn from 960 surveyed building footprints "
     "and 2,826 OpenStreetMap ways rather than sketched or traced off a "
     "proprietary basemap. It produced an independent check on the bridge "
     "alignment - <b>2.3&deg; off the bearing this repository had digitised by "
     "eye</b> - and established that the one object in the frame nobody has "
     "surveyed is the bridge itself."),
    ("Method 29 - the cohort survival model", 29,
     "About six minutes of arithmetic",
     "Fits four population cohorts to the observed departure curve. "
     "<b>It reports its own failure</b>: the sweep found many parameter sets "
     "that fit equally well and imply materially different exposure, so the "
     "model establishes that dwell time cannot be inferred from arrival and "
     "departure counts alone. That is why Method 28 sits at the top of the "
     "list below."),
    ("Method 30 - the agentic population model", 30,
     "Built, not run as a measurement",
     "Personas, family groups, itineraries, ingress and egress points, and "
     "dose accumulated along a path. Built as a <b>mechanism demonstration and "
     "labelled as one on its own face</b>, because every itinerary in it is "
     "invented. Its most useful output was a negative result: the propagation "
     "model over the four MTA points could not be fitted. A fifth rung now "
     "models <b>who is standing in the dose</b> and applies <b>no decibel "
     "penalty to any of them</b> - a per-class adjustment would be a "
     "fabricated exposure-response function wearing the costume of a "
     "measurement."),
    ("The acoustic demonstration", "done",
     "Synthesised, and labelled synthetic in the interface",
     "A train approaching, passing and departing at the measured decibel "
     "difference against each receptor's own background, then running "
     "continuously at the real headway. <b>It is synthesis, not a "
     "recording</b>, and the page says so before it says anything else."),
    ("The community evidence audit", "done",
     "Searching, and finding nothing",
     "Reddit, Freesound, the NYU SONYC corpus, NYC Open Data, local press and "
     "petitions, searched for crowd-sourced recordings. <b>None exist</b> - "
     "and the audit found the structural reason: three separate instruments "
     "for recording city noise and no rail category in any of them."),
    ("Method 27 - count the denominator", 27,
     "Four API pulls, about a minute",
     "Arrival rate, walkway flow and resident count from four public datasets, "
     "two of which agree to within 1.77% by different methods. It "
     "<b>disproved this repository's own claim</b> that 08:00 is the worst "
     "hour; the real peak is 14:00. Marked partial because it produces "
     "&lambda; and not W - the arrival rate exists, the dwell time does not."),
    ("Method 26 - the traversal census tooling", 26,
     "Written and verified against the live feed",
     "The poller is built and correct. <b>The week-long run has not been "
     "done</b>, so this is a mark on the code and not on the result - which is "
     "why the census still appears in the queue below."),
    ("The field capture protocol", "partial",
     "Written, and now partly attempted",
     "A complete protocol for a consumer phone targeting the four things the "
     "MTA's five-number table discarded. <b>One session has now been run "
     "against it</b> and scored honestly: C1 not satisfied, C2 partly and not "
     "usefully, C3 partly, C4 and C5 not attempted. The gap between what the "
     "protocol asked for and what a first outing produced is itself the "
     "useful part."),
    ("Method 37 - price the same deliverable against the market", 37,
     "Two free federal APIs, no key",
     "What this would have cost to buy, from three instruments reported side "
     "by side and <b>never averaged</b>: 56 federal noise-study awards, a "
     "bottom-up build at GSA awarded ceiling rates verified cent-for-cent "
     "against a vendor's own card, and the metered inference ledger. "
     "<b>Its result is the disagreement between them</b>, not a number - and "
     "it withdraws the obvious headline before making it, because the "
     "numerator would be measured and the denominator invented."),
]

# The work queue. Ordering is a judgement and is stated as one; the STATUS of
# each method is parsed from the register rather than typed here.
TODO = [
    ("blocking", "Method 28 - measure dwell time",
     "A few hours with a clicker, repeated over several sessions",
     "Presence is L = &lambda;W. Method 27 produced &lambda;. Without W there is "
     "no absolute exposure figure, and the cohort model proved that no amount of "
     "further arithmetic will substitute for measuring it. <b>This is the single "
     "blocking unknown for any design-build case.</b> <b>Method 42 rides along "
     "with it at no extra cost</b> &mdash; the same observer, at the same "
     "cordon, tallying prams, dogs, mobility aids and apparent age band. "
     "<b>Record individual crossings, not only a total.</b> The arrival-process "
     "result in the agent model turns on the <i>bottom</i> of the dwell "
     "distribution rather than its mean, and a running tally throws that away."),
    ("cheap", "Method 42 - count the corridor by attribute, not just by head",
     "The same session as Method 28, one extra clicker",
     "Every susceptibility share in the agent model is a <b>national "
     "prevalence applied flat to a corridor nobody has ever counted by any "
     "attribute at all</b>, and each is rated 1/5 on whether it applies here. "
     "A flat rate is knowably wrong at a place whose purpose selects for a "
     "class, and this corridor is full of them: a dog run, a carousel, a lawn, "
     "and the residential blocks at Farragut Houses. <b>The honest half of the "
     "method is what it cannot do:</b> an age band, a pram and a lead are "
     "observable; hyperacusis, autism and a cancer history are not. It must "
     "publish which shares it moved and which it left national, or it will "
     "read as having verified all of them."),
    ("cheap", "Method 44 - the crowding half, and only if the whole of it is run",
     "The feeder headways are one constant and a minute; the rest is a study",
     "Three arrival processes were compared in the agent model at a fixed "
     "population, and <b>multiplying peak bunching by 4.2 times moved the mean "
     "dose by 0.001 dB</b> &mdash; never more than 0.037 dB on any seed &mdash; "
     "because dwell dominates headway. Contention is the one quantity that does "
     "respond, up about 12%. So this method has been <b>demoted by a result "
     "rather than by a judgement</b>, and it is listed here mostly to say so. "
     "<code>bridge_schedule.py</code> already computes the feeder headways if "
     "one constant is changed, and running that alone would produce a real "
     "number that reaches nothing. <b>The part that matters is behavioural</b>: "
     "whether a full bench sends someone toward the bridge or away from it."),
    ("cheap", "Method 31 - the decay transect",
     "One afternoon, free if a sound level meter is borrowed",
     "Walk outward from the structure with a meter and establish where the "
     "affected zone ends. Nobody has ever determined that boundary, yet it sizes "
     "the denominator for every exposure figure here. Three possible outcomes "
     "and all three are informative, including the one that corrects this "
     "repository."),
    ("cheap", "Method 21 - the taxonomy query",
     "A database query",
     "Confirm across the full 311 and SONYC taxonomies that no rail category "
     "exists anywhere in either. The finding is already evidenced; this closes "
     "the last route by which it could be wrong."),
    ("cheap", "Method 34 - pin one cohort from outside the curve",
     "One download of a free federal dataset",
     "The cohort model is degenerate by construction, because <b>a departure "
     "curve carries no labels</b>: at 14:00 the fitted worker count ranges "
     "3,629-5,490 and visitors 1,460-2,313 across 9,248 parameter sets that fit "
     "equally well. No better fitting narrows that. <b>One exogenous number "
     "does</b> - LEHD LODES gives jobs by census block, which pins workers and "
     "leaves visitors as a residual rather than a guess."),
    ("cheap", "Q42 - preemption or merely unregulated?",
     "One competent lawyer, one day",
     "Is elevated rapid transit federally <i>preempted</i> from local noise "
     "regulation, or simply <i>unregulated</i>? These have opposite consequences "
     "for every remedy in the programme. <b>The highest-value open question "
     "here.</b>"),
    ("cheap", "Method 26 - the traversal census",
     "Leave a script running for a week, unattended",
     "The tooling is built and verified. It is now the only route to the "
     "coincidence distribution, since the schedule feed was shown to be "
     "quantised to 30 s and unable to answer it."),
    ("field", "Methods 39, 40 and 41 - the instrumented session",
     "One afternoon plus one quiet hour, with gear already owned",
     "Three questions that need no calibration, because all three are ratios "
     "or timings and an unknown microphone sensitivity cancels out of both. "
     "<b>Direction and speed</b> from two timecode-synchronised recorders "
     "separated 50&ndash;80 m along the track axis, read off the order of the "
     "two level peaks. <b>The decay tail</b> &mdash; the operator's "
     "&ldquo;noise time on clock versus floor time&rdquo; &mdash; which no "
     "instrument here has ever measured, because automatic gain control "
     "pushes gain up as a sound fades and so flattens exactly the thing "
     "being measured. <b>Simultaneous crossings</b>, which the published "
     "schedule cannot answer at all: every departure in the feed falls on an "
     "exact :00 or :30 second, so the window in which two trains merge "
     "acoustically is empty by construction. The session card is "
     "<a href=\"pedestrian-site-visits/FIELD-KIT.md\">FIELD-KIT.md</a>."),
    ("field", "Extend the walk: York Street to Fulton Ferry along the water",
     "One afternoon on foot, the phone already owned",
     "The drawn walk currently stops at the water's edge. <b>That is not the "
     "walk people take.</b> They come up from the York Street F platform, go "
     "straight down to the water, turn, and follow the shoreline past Jane's "
     "Carousel to Fulton Ferry Landing &mdash; passing under the bridge, out "
     "from under it, and back into its shadow. Extending the corridor drawing "
     "and the capture route along that full line puts the receptor path where "
     "the population actually is, and it crosses the one geometry this "
     "programme keeps asserting and has never walked end to end: <b>where the "
     "canyon stops.</b> Method 31's decay transect and this share a route."),
    ("field", "Captures C1 to C5 - the phone protocol",
     "A Galaxy S23+, public ground, no permission and no funding",
     "The only proposal in the programme that requires nothing the programme "
     "does not already have. <b>One outing has been made</b> and it satisfied "
     "none of C1, C4 or C5 and only part of C2 and C3. <b>C2, the temporal "
     "envelope, remains the highest-value item</b>: it is the one measurement "
     "that could establish that this repository's own derived result is wrong, "
     "and the first attempt showed why it needs a windscreen and a capture "
     "path with the compressor disabled. A shielded and metered session is "
     "planned; Q56 should be answered before it is taken, not after."),
    ("cheap", "Q56 - is any duty cycle computable from consumer capture?",
     "An afternoon on a bench, no equipment beyond the phone",
     "Every duty figure computed from the field audio passed through "
     "automatic gain control, and <b>the interaction has a sign</b>: a "
     "compressor shrinks excursions above a clip's own median, so any such "
     "figure is biased low by an unknown amount. Play a signal of known duty "
     "cycle through a speaker, record it on the same handset, and the known "
     "input gives the answer. <b>This should be run before the next capture, "
     "not after</b> - a shielded, metered microphone still feeds the same "
     "compressor unless <code>AudioSource.UNPROCESSED</code> is explicitly "
     "enabled, so this test decides whether the next session needs its "
     "capture path changed to be worth taking."),
    ("cheap", "Method 43 - what licenses comparing dB HL to dB(A)?",
     "One afternoon at a desk, but strictly blocked on capture C1",
     "Loudness discomfort centres near <b>100 dB HL</b> for normal-hearing "
     "listeners and hyperacusis is commonly marked at <b>90 dB HL or below</b>; "
     "the MTA measured <b>98.90 dB(A)</b> peaks at the dog run. Those look "
     "comparable and <b>they are not the same units</b> - one is per-frequency, "
     "pure-tone and headphone-presented, the other broadband, free-field and "
     "weighted by a single fixed curve. Bridging them needs the third-octave "
     "spectrum of the actual sound, which does not exist for either bridge. "
     "<b>That is the value of the question:</b> it turns an open-ended plea "
     "for more evidence into one named missing measurement. It will not give "
     "a clean verdict even then - the defensible output is a bracket with its "
     "assumptions named, and a bracket that straddles the measured peak would "
     "be as informative as either clean result."),
    ("review", "Red-team the three newest results",
     "Reading and arithmetic",
     "Issues <a href=\"" + ISSUES + "26\">#26</a> (is the cohort model's "
     "non-identifiability a finding or an artefact of an arbitrary threshold?), "
     "<a href=\"" + ISSUES + "27\">#27</a> (does a model whose every input is "
     "invented belong in a repository built on quoted loci?) and "
     "<a href=\"" + ISSUES + "28\">#28</a> (<b>was the propagation model "
     "genuinely unfittable, or merely digitised badly?</b>)."),
    ("review", "Read the five counter-citations",
     "Library access",
     "Five works surfaced during red-teaming that bear directly on Q1 to Q8 and "
     "were <b>not read in full</b>. They are listed in section 14 of the concept "
     "document. Anyone taking this forward should start there, not here."),
    ("gate", "Methods 0 and 1 - the structural and acoustic prerequisites",
     "A records request and an engineer; then a two-season field campaign",
     "The load rating at the track zone gates roughly half the option space, and "
     "source apportionment is the programme's stated prerequisite - nothing "
     "downstream is non-arbitrary without it. Expensive, unavoidable, and the "
     "reason nothing here is recommended for procurement."),
]

CONVENTIONS = [
    ("Every number carries its locus",
     "Not a citation - the actual quoted sentence the number came from. If a "
     "claim has no locus, it is an inference and is labelled as one."),
    ("Sources are rated 1 to 5 and marked VERIFIED, SNIPPET or UNVERIFIED",
     "VERIFIED means the full text was read. SNIPPET means only an abstract or "
     "search result was seen. Most over-claiming in this programme has come from "
     "treating a SNIPPET as if it were VERIFIED."),
    ("Errors are quoted in place, not deleted",
     "When something here turns out to be wrong, the original wording is left "
     "visible as a blockquote and followed by the words <i>that is withdrawn</i>. "
     "A research record that hides its own corrections is not a research record."),
    ("Every document ends by attacking itself",
     "A section titled <i>where this document is likely to be wrong</i>, written "
     "by the authors, naming the specific claim they would attack first."),
    ("Synthetic is labelled synthetic, in the interface",
     "The 3D model contains zero measured elements. The audio is synthesised, "
     "not recorded. The agent model's itineraries are invented. Each says so on "
     "its own face rather than in a footnote somewhere else."),
]

# ---------------------------------------------------------------------------
# Reading the repository
# ---------------------------------------------------------------------------


WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven",
         "eight", "nine", "ten", "eleven", "twelve"]


def spell(n):
    """Prose uses words for small numbers; tables keep the numerals."""
    return WORDS[n] if 0 <= n < len(WORDS) else "{:,}".format(n)


def read(path):
    with io.open(os.path.join(ROOT, path), encoding="utf-8") as fh:
        return fh.read()


def size_kb(path):
    try:
        return int(round(os.path.getsize(os.path.join(ROOT, path)) / 1024.0))
    except OSError:
        return 0


def gh_slug(value, separator="-"):
    """Reproduce GitHub's heading-anchor algorithm so existing #links survive."""
    value = re.sub(r"[^\w\- ]", "", value.strip().lower(), flags=re.UNICODE)
    return value.replace(" ", separator)


def parse_methods(readme):
    """Pull the method register out of the README and classify each status."""
    rows = []
    for line in readme.split("\n"):
        s = line.strip()
        if not (s.startswith("|") and s.endswith("|")):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) != 5:
            continue
        num = re.sub(r"[*\s]", "", cells[0])
        if not num.isdigit():
            continue
        plain = re.sub(r"[*_`]", "", cells[4]).strip().lower()
        if plain.startswith("partially executed"):
            cls = "partial"
        elif plain.startswith("executed") or plain.startswith("built as"):
            cls = "executed"
        elif plain.startswith("tooling built"):
            cls = "tooling"
        elif plain.startswith("not started"):
            cls = "not-started"
        else:
            cls = "other"
        rows.append({
            "n": int(num),
            "name": re.sub(r"[*_`]", "", cells[1]).split(" - ")[0].strip(),
            "doc": cells[2],
            "cost": re.sub(r"[*_`]", "", cells[3]).strip(),
            "status": re.sub(r"[*_`]", "", cells[4]).strip(),
            "cls": cls,
        })
    rows.sort(key=lambda r: r["n"])
    return rows


def collect_stats():
    st = {}
    texts = {p: read(p) for p, _, _, _, _ in DOCS}
    st["words"] = {p: len(t.split()) for p, t in texts.items()}
    st["total_words"] = sum(st["words"].values())
    st["methods"] = parse_methods(texts["README.md"])
    st["n_methods"] = len(st["methods"])
    st["n_exec"] = sum(1 for m in st["methods"] if m["cls"] == "executed")
    st["n_partial"] = sum(1 for m in st["methods"] if m["cls"] == "partial")
    st["n_tooling"] = sum(1 for m in st["methods"] if m["cls"] == "tooling")
    st["n_open"] = st["n_methods"] - st["n_exec"] - st["n_partial"]

    qmax = 0
    for t in texts.values():
        for m in re.finditer(r"\bQ(\d{1,3})\b", t):
            qmax = max(qmax, int(m.group(1)))
    st["max_q"] = qmax

    # Explicit withdrawal markers, counted rather than estimated.
    st["withdrawals"] = sum(
        len(re.findall(r"(?:that|this|which) (?:is|are) withdrawn", t, re.I))
        for t in texts.values())

    try:
        st["sha"] = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], cwd=ROOT).decode().strip()
        st["date"] = subprocess.check_output(
            ["git", "log", "-1", "--format=%cs"], cwd=ROOT).decode().strip()
    except Exception:
        st["sha"] = "unknown"
        st["date"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return st


# ---------------------------------------------------------------------------
# Page furniture
# ---------------------------------------------------------------------------

THEME_JS = """<script>
  (() => {
    const param = new URLSearchParams(window.location.search).get("scoutTheme");
    const theme =
      param || (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    document.documentElement.setAttribute("data-theme", theme);
  })();
</script>"""

# A suspension bridge, inlined so that no page ever requests /favicon.ico.
FAVICON = (
    '<link rel="icon" href="data:image/svg+xml,'
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'"
    "%3E%3Crect width='32' height='32' rx='7' fill='%23b11f4b'/"
    "%3E%3Cpath d='M3 22h26' stroke='%23fff' stroke-width='2.4' "
    "stroke-linecap='round'/%3E%3Cpath d='M9 8v14M23 8v14' stroke='%23fff' "
    "stroke-width='2' stroke-linecap='round'/%3E%3Cpath "
    "d='M3 14L9 8Q16 17 23 8L29 14' stroke='%23fff' stroke-width='2' "
    "fill='none' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E\">")

CSS = """
:root {
  color-scheme: light;
  --cp-bg: #f7f4ef;
  --cp-bg-elevated: #fcfbf8;
  --cp-surface: #ffffff;
  --cp-surface-soft: #f5f5f5;
  --cp-border: #dedede;
  --cp-border-strong: #919191;
  --cp-text: #242424;
  --cp-text-muted: #5c5c5c;
  --cp-text-soft: #6f6f6f;
  --cp-accent: #b11f4b;
  --cp-accent-hover: #9a1a41;
  --cp-accent-soft: rgba(177, 31, 75, 0.08);
  --cp-accent-fg: #ffffff;
  --cp-success: #16a34a;
  --cp-danger: #dc2626;
  --cp-warning: #f59e0b;
  --cp-link: #0078d4;
  --cp-shadow: 0 18px 48px rgba(0, 0, 0, 0.12);
  --cp-overlay: rgba(255, 255, 255, 0.8);
  --cp-panel: rgba(255, 255, 255, 0.86);
  --cp-panel-strong: rgba(255, 255, 255, 0.96);
  --cp-sheen: rgba(255, 255, 255, 0.55);
  --cp-highlight: rgba(177, 31, 75, 0.12);
}
html[data-theme="dark"] {
  color-scheme: dark;
  --cp-bg: #3d3b3a;
  --cp-bg-elevated: #343231;
  --cp-surface: #292929;
  --cp-surface-soft: #2e2e2e;
  --cp-border: #474747;
  --cp-border-strong: #5f5f5f;
  --cp-text: #dedede;
  --cp-text-muted: #919191;
  --cp-text-soft: #b0b0b0;
  --cp-accent: #fd8ea1;
  --cp-accent-hover: #fb7b91;
  --cp-accent-soft: rgba(253, 142, 161, 0.14);
  --cp-accent-fg: #1a1a1a;
  --cp-success: #4ade80;
  --cp-danger: #f87171;
  --cp-warning: #fbbf24;
  --cp-link: #4da6ff;
  --cp-shadow: 0 18px 48px rgba(0, 0, 0, 0.32);
  --cp-overlay: rgba(41, 41, 41, 0.88);
  --cp-panel: rgba(41, 41, 41, 0.72);
  --cp-panel-strong: rgba(41, 41, 41, 0.96);
  --cp-sheen: rgba(255, 255, 255, 0.04);
  --cp-highlight: rgba(253, 142, 161, 0.12);
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; scroll-padding-top: 72px; }
body {
  margin: 0;
  background: var(--cp-bg);
  color: var(--cp-text);
  font-family: "Segoe UI", Aptos, Calibri, -apple-system, BlinkMacSystemFont, sans-serif;
  font-size: 16px;
  line-height: 1.62;
  -webkit-font-smoothing: antialiased;
}
a { color: var(--cp-link); text-decoration: none; }
a:hover { text-decoration: underline; }
code, kbd, pre {
  font-family: Consolas, "Courier New", Courier, monospace;
  font-size: 0.9em;
}
code {
  background: var(--cp-surface-soft);
  border: 1px solid var(--cp-border);
  border-radius: 4px;
  padding: 0.1em 0.36em;
}
/* A code span inside a link must still read as a link. */
a code { color: var(--cp-link); border-color: var(--cp-link); }
pre {
  background: var(--cp-surface-soft);
  border: 1px solid var(--cp-border);
  border-radius: 0.625rem;
  padding: 14px 16px;
  overflow-x: auto;
  line-height: 1.5;
}
pre code { background: none; border: 0; padding: 0; }

/* ---- top bar ---- */
/* mh- prefixed to match the block ensure_masthead() injects into the
   hand-written artifacts. One definition, one set of names, no collisions. */
.mh-bar {
  position: sticky; top: 0; z-index: 50; display: block;
  background: var(--cp-panel-strong);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--cp-border);
}
.mh-bar .mh-in {
  max-width: 1180px; margin: 0 auto; padding: 10px 22px;
  display: flex; align-items: center; gap: 14px; flex-wrap: wrap;
}
.mh-bar .mh-home {
  font-weight: 700; color: var(--cp-text); font-size: 0.95rem;
  display: inline-flex; align-items: center; gap: 9px; white-space: nowrap;
}
.mh-bar .mh-home .mh-mark { display: block; flex: none; border-radius: 6px;
  width: 26px; height: 26px; min-width: 26px; max-width: 26px; }
.mh-bar .mh-home:hover { color: var(--cp-accent); text-decoration: none; }
@media (max-width: 560px) { .mh-bar .mh-home .mh-wm { display: none; } }
.mh-bar .mh-nav { display: flex; gap: 4px; flex-wrap: wrap; margin-left: auto;
  align-items: center; }
.mh-bar .mh-nav a {
  color: var(--cp-text-muted); font-size: 0.82rem; padding: 4px 9px;
  display: inline-block; border-radius: 999px; white-space: nowrap;
}
.mh-bar .mh-nav a:hover { background: var(--cp-accent-soft); color: var(--cp-accent); text-decoration: none; }
.mh-bar .mh-nav a.on { background: var(--cp-accent); color: var(--cp-accent-fg); }
/* Divides the investigation from the work about the work. Decorative, so it
   is aria-hidden in the markup and carries no text. */
.mh-bar .mh-nav .mh-sep { width: 1px; height: 17px; flex: none; margin: 0 7px;
  background: var(--cp-border-strong); border-radius: 1px; }

.wrap { max-width: 1180px; margin: 0 auto; padding: 30px 22px 90px; }

h1 { font-size: 2.15rem; line-height: 1.18; margin: 0 0 10px; letter-spacing: -0.01em; }
h2 { font-size: 1.42rem; margin: 0 0 14px; letter-spacing: -0.005em; }
h3 { font-size: 1.08rem; margin: 26px 0 8px; }
p { margin: 0 0 14px; }
.lede { font-size: 1.06rem; color: var(--cp-text-muted); }
.sub { color: var(--cp-text-muted); font-size: 1.02rem; margin: 0 0 4px; }

.card {
  background: var(--cp-surface);
  border: 1px solid var(--cp-border);
  border-radius: 16px;
  padding: 26px 28px;
  margin: 0 0 22px;
  box-shadow: 0 0 2px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.14);
}
.hero { background: var(--cp-bg-elevated); }

/* -- above the fold ------------------------------------------------------ */
/* The hero image is grayscale by construction so the theme, not the JPEG,
   decides what colour it is. */
.hb {
  position: relative; border-radius: 16px; overflow: hidden;
  border: 1px solid var(--cp-border); margin: 0 0 22px;
  background: #101010; isolation: isolate;
}
.hb .pic {
  position: absolute; inset: 0; width: 100%; height: 100%;
  object-fit: cover; object-position: 62% 46%; z-index: 0;
  opacity: 0.95;
}
.hb .tint {
  position: absolute; inset: 0; z-index: 1; pointer-events: none;
  background:
    linear-gradient(90deg, rgba(16,16,16,0.94) 0%, rgba(16,16,16,0.86) 34%,
                    rgba(16,16,16,0.42) 62%, rgba(16,16,16,0.20) 100%),
    linear-gradient(0deg, var(--cp-highlight), var(--cp-highlight));
}
.hb .hin { position: relative; z-index: 2; padding: 44px 40px 30px; color: #f2efea; }
.hb .kicker {
  font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.14em;
  color: var(--cp-accent); font-weight: 700; margin: 0 0 10px;
}
html[data-theme="light"] .hb .kicker { color: #fd8ea1; }
.hb h1 { font-size: 2.5rem; margin: 0 0 10px; letter-spacing: -0.02em; color: #fff; }
.hb .sub { font-size: 1.06rem; margin: 0 0 6px; max-width: 44rem; color: #e6e1da; }
.hb .sub a { color: #ffd0da; }
.hb .lede { font-size: 0.95rem; margin: 0; max-width: 44rem; color: #bdb7b0; }
.hb .cred {
  position: relative; z-index: 2; margin: 22px 0 0; padding-top: 14px;
  border-top: 1px solid rgba(255,255,255,0.14);
  font-size: 0.7rem; color: rgba(255,255,255,0.52); line-height: 1.5;
}
.hb .cred a { color: rgba(255,255,255,0.74); }

/* the statement carousel */
.wc { position: relative; z-index: 2; margin: 26px 0 34px; min-height: 148px; }
.wc .wcslide {
  position: absolute; inset: 0; opacity: 0; transition: opacity .5s ease;
  pointer-events: none; display: block; color: inherit;
}
.wc .wcslide.on { opacity: 1; pointer-events: auto; }
.wc .wcslide:hover { text-decoration: none; }
.wc .n {
  font-size: clamp(3rem, 8.5vw, 5.4rem); font-weight: 700; line-height: 0.94;
  letter-spacing: -0.035em; color: #fff; display: block;
}
.wc .u {
  font-size: 0.96rem; font-weight: 700; letter-spacing: 0.04em;
  text-transform: uppercase; color: var(--cp-accent); margin: 8px 0 6px;
}
html[data-theme="light"] .wc .u { color: #ff9bad; }
.wc .l { font-size: 0.98rem; color: #ded8d1; max-width: 40rem; }
.wc .wcslide:hover .n { color: #ffd0da; }
.wcnav { position: relative; z-index: 2; display: flex; align-items: center; gap: 8px; }
.wcnav button {
  width: 30px; height: 6px; border-radius: 3px; border: 0; cursor: pointer;
  background: rgba(255,255,255,0.26); padding: 0;
}
.wcnav button[aria-current="true"] { background: var(--cp-accent); }
.wcnav button:focus-visible { outline: 2px solid #fff; outline-offset: 3px; }
.wcnav .pp {
  width: auto; height: auto; border-radius: 0.625rem; padding: 4px 10px;
  font: inherit; font-size: 0.74rem; color: #ded8d1;
  background: rgba(255,255,255,0.12); margin-left: 8px;
}
@media (prefers-reduced-motion: reduce) {
  .wc .wcslide { transition: none; }
}
@media (max-width: 760px) {
  .hb .hin { padding: 28px 20px 22px; }
  .hb h1 { font-size: 1.8rem; }
  .hb .cred { position: static; max-width: none; text-align: left; }
  .wc { min-height: 190px; }
}

.statrow { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-top: 20px; }
.s {
  background: var(--cp-surface-soft); border: 1px solid var(--cp-border);
  border-radius: 0.625rem; padding: 14px 16px;
  font-size: 0.78rem; color: var(--cp-text-muted);
}
.s .k { font-size: 0.74rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px; }
.s .big { font-size: 1.9rem; font-weight: 700; color: var(--cp-accent); line-height: 1.1; }

.tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(268px, 1fr)); gap: 14px; }
.tile {
  display: block; background: var(--cp-surface-soft);
  border: 1px solid var(--cp-border); border-radius: 0.625rem;
  padding: 16px 18px; color: var(--cp-text); transition: border-color .15s, transform .15s;
}
.tile:hover { border-color: var(--cp-accent); text-decoration: none; transform: translateY(-2px); }
.tile .t { font-weight: 700; margin-bottom: 6px; color: var(--cp-accent); }
.tile .d { font-size: 0.87rem; color: var(--cp-text-muted); }
.mgrid { display: grid; grid-template-columns: repeat(auto-fit, minmax(232px, 1fr));
         gap: 14px; margin-top: 18px; }
.m { border: 1px solid var(--cp-border); border-radius: 10px; padding: 14px 16px;
     background: var(--cp-surface-soft); }
.m .mn { font-size: 2.1rem; font-weight: 800; line-height: 1; color: var(--cp-accent);
         letter-spacing: -0.02em; }
.m .mt { font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.06em;
         color: var(--cp-text-muted); margin: 6px 0 8px; }
.m p { font-size: 0.88rem; margin: 0; }
.tile .look {
  font-size: 0.82rem; margin-top: 10px; padding-top: 10px;
  border-top: 1px dashed var(--cp-border); color: var(--cp-text-soft);
}
.tile .look b { color: var(--cp-text); }

.badge {
  display: inline-block; font-size: 0.68rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.06em;
  padding: 2px 8px; border-radius: 999px; vertical-align: middle;
  border: 1px solid var(--cp-border-strong); color: var(--cp-text-muted);
}
.badge.ok { border-color: var(--cp-success); color: var(--cp-success); }
.badge.no { border-color: var(--cp-danger); color: var(--cp-danger); }
.badge.warn { border-color: var(--cp-warning); color: var(--cp-warning); }
.badge.acc { border-color: var(--cp-accent); color: var(--cp-accent); }

.note {
  border-left: 3px solid var(--cp-accent);
  background: var(--cp-accent-soft);
  border-radius: 0 0.625rem 0.625rem 0;
  padding: 13px 17px; margin: 16px 0; font-size: 0.92rem;
}
.note.bad { border-left-color: var(--cp-danger); background: rgba(220,38,38,0.07); }
.note.good { border-left-color: var(--cp-success); background: rgba(22,163,74,0.07); }
.note.warn { border-left-color: var(--cp-warning); background: rgba(245,158,11,0.09); }

.tw { overflow-x: auto; margin: 16px 0; }
table { border-collapse: collapse; width: 100%; font-size: 0.88rem; }
th, td {
  border: 1px solid var(--cp-border); padding: 8px 11px;
  text-align: left; vertical-align: top;
}
th { background: var(--cp-surface-soft); font-weight: 700; }
tbody tr:nth-child(even) td { background: var(--cp-surface-soft); }

ul, ol { margin: 0 0 14px; padding-left: 22px; }
li { margin-bottom: 7px; }

blockquote {
  margin: 16px 0; padding: 10px 18px;
  border-left: 3px solid var(--cp-border-strong);
  background: var(--cp-surface-soft);
  border-radius: 0 0.625rem 0.625rem 0;
  color: var(--cp-text-muted);
}

hr { border: 0; border-top: 1px solid var(--cp-border); margin: 26px 0; }

.foot {
  color: var(--cp-text-soft); font-size: 0.83rem;
  border-top: 1px solid var(--cp-border); padding-top: 18px; margin-top: 30px;
}

/* ---- work queue ---- */
.q { border-top: 1px solid var(--cp-border); padding: 15px 0; display: grid;
     grid-template-columns: 132px 1fr; gap: 18px; }
.q:first-of-type { border-top: 0; }
.q .lab { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.06em;
          font-weight: 700; padding-top: 3px; display: flex;
          align-items: flex-start; gap: 8px; line-height: 1.35; }
.q .h { font-weight: 700; margin-bottom: 2px; }
.q .cost { font-size: 0.8rem; color: var(--cp-text-soft); margin-bottom: 7px;
           font-family: Consolas, "Courier New", monospace; }
.q .why { font-size: 0.9rem; color: var(--cp-text-muted); }
.lab.blocking { color: var(--cp-danger); }
.lab.cheap { color: var(--cp-success); }
.lab.field { color: var(--cp-accent); }
.lab.review { color: var(--cp-warning); }
.lab.gate { color: var(--cp-text-muted); }
.lab.done { color: var(--cp-success); }

/* A tick and an empty box, so done and not-done are distinguishable without
   relying on colour alone. Both are drawn, not typed, so neither depends on
   an emoji font being present. */
.mk { display: inline-block; width: 17px; height: 17px; border-radius: 4px;
      position: relative; flex: 0 0 17px; margin-top: 1px; }
.mk.on { background: var(--cp-success); }
.mk.on::after { content: ""; position: absolute; left: 5px; top: 1.5px;
                width: 4px; height: 9px; border: solid #fff;
                border-width: 0 2px 2px 0; transform: rotate(42deg); }
/* Indeterminate: the work was done, the result was not obtained. A full tick
   next to "the week has not been run" would overstate it. */
.mk.half { border: 2px solid var(--cp-success); }
.mk.half::after { content: ""; position: absolute; left: 2.5px; top: 5.5px;
                  width: 8px; height: 2px; background: var(--cp-success); }
.mk.off { border: 2px solid var(--cp-border-strong); }
.q .h { display: block; }
.qdone { margin-bottom: 6px; }
.qdone .h { color: var(--cp-text); }
.qdone .why { color: var(--cp-text-soft); }
.donehead { display: flex; align-items: baseline; justify-content: space-between;
            gap: 14px; flex-wrap: wrap; margin: 26px 0 4px; }
.donehead h3 { margin: 0; }
.donehead .cnt { font-size: 0.82rem; color: var(--cp-text-muted);
                 font-family: Consolas, "Courier New", monospace; }
.legend { display: flex; flex-wrap: wrap; gap: 10px 22px; margin: 14px 0 2px;
          font-size: 0.84rem; color: var(--cp-text-muted); }
.legend > span { display: flex; align-items: flex-start; gap: 8px; }

/* ---- rendered document pages ---- */
.doclayout { display: grid; grid-template-columns: 250px 1fr; gap: 34px; align-items: start; }
.toc { position: sticky; top: 76px; max-height: calc(100vh - 100px); overflow-y: auto;
       font-size: 0.84rem; padding-right: 6px; }
.toc .h { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.07em;
          color: var(--cp-text-soft); font-weight: 700; margin-bottom: 8px; }
.toc a { display: block; padding: 3px 0 3px 9px; color: var(--cp-text-muted);
         border-left: 2px solid var(--cp-border); line-height: 1.35; }
.toc a:hover { color: var(--cp-accent); border-left-color: var(--cp-accent); text-decoration: none; }
.toc a.l3 { padding-left: 20px; font-size: 0.95em; color: var(--cp-text-soft); }
.doc { min-width: 0; }
.doc h1 { font-size: 1.95rem; margin-top: 0; }
.doc h2 { font-size: 1.38rem; margin: 34px 0 12px; padding-bottom: 6px;
          border-bottom: 1px solid var(--cp-border); }
.doc h3 { font-size: 1.1rem; margin: 26px 0 8px; }
.doc h4 { font-size: 0.98rem; margin: 20px 0 6px; color: var(--cp-text-muted); }
.doc img { max-width: 100%; }

@media (max-width: 980px) {
  .statrow { grid-template-columns: repeat(2, 1fr); }
  .doclayout { grid-template-columns: 1fr; }
  .toc { position: static; max-height: none; margin-bottom: 26px; }
  .q { grid-template-columns: 1fr; gap: 4px; }
  .wrap { padding: 22px 16px 70px; }
  .card { padding: 20px 18px; }
}
@media (max-width: 560px) {
  .statrow { grid-template-columns: 1fr; }
}
"""


HERO_JS = """<script>
(function () {
  var wc = document.getElementById("wc");
  var nav = document.getElementById("wcnav");
  if (!wc || !nav) return;
  var slides = [].slice.call(wc.querySelectorAll(".wcslide"));
  var dots = [].slice.call(nav.querySelectorAll("button[data-i]"));
  var pp = document.getElementById("wcpp");
  var i = 0, timer = null;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function show(n) {
    i = (n + slides.length) % slides.length;
    slides.forEach(function (s, k) { s.classList.toggle("on", k === i); });
    dots.forEach(function (d, k) {
      d.setAttribute("aria-current", k === i ? "true" : "false");
    });
  }
  function stop() {
    if (timer) { clearInterval(timer); timer = null; }
    pp.textContent = "Play";
    pp.setAttribute("aria-label", "Resume the rotating statements");
  }
  function start() {
    if (timer || reduce) return;
    timer = setInterval(function () { show(i + 1); }, 5200);
    pp.textContent = "Pause";
    pp.setAttribute("aria-label", "Pause the rotating statements");
  }
  dots.forEach(function (d) {
    d.addEventListener("click", function () {
      show(parseInt(d.dataset.i, 10)); stop();
    });
  });
  pp.addEventListener("click", function () { timer ? stop() : start(); });
  // Rotating text that keeps moving while someone is reading it is hostile,
  // so hovering, focusing or leaving the tab all halt it.
  wc.addEventListener("mouseenter", stop);
  wc.addEventListener("focusin", stop);
  document.addEventListener("visibilitychange", function () {
    if (document.hidden) stop();
  });
  if (reduce) { stop(); pp.textContent = "Next"; pp.addEventListener(
    "click", function () { show(i + 1); }); } else { start(); }
})();
</script>"""


# The same suspension bridge as the favicon, drawn at nav size. Inline rather
# than a file so that a hand-written artifact patched with the masthead stays
# self-contained and works from a file:// URL with no asset alongside it.
LOGO = (
    '<svg class="mh-mark" viewBox="0 0 32 32" width="26" height="26" '
    'aria-hidden="true" focusable="false">'
    '<rect width="32" height="32" rx="7" fill="var(--cp-accent)"/>'
    '<path d="M3 22h26" stroke="var(--cp-accent-fg)" stroke-width="2.4" '
    'stroke-linecap="round"/>'
    '<path d="M9 8v14M23 8v14" stroke="var(--cp-accent-fg)" stroke-width="2" '
    'stroke-linecap="round"/>'
    '<path d="M3 14L9 8Q16 17 23 8L29 14" stroke="var(--cp-accent-fg)" '
    'stroke-width="2" fill="none" stroke-linecap="round" '
    'stroke-linejoin="round"/></svg>')


def bar(active, depth):
    """The masthead, identical on every page of the site.

    `active` is "home", "demos", or "research".
    `depth` is 1 for anything in a subdirectory.

    THREE ITEMS, DELIBERATELY. This nav previously carried twelve: the README,
    seven numbered documents, the demos, and two meta documents behind a rule.
    That is a correct table of contents and a bad menu. A reader who has never
    heard of this problem cannot tell from "3. Comparator" whether it is worth
    a click, so twelve pills read as a wall and the whole thing gets skipped.

    So the documents are no longer in the header. They are on research.html,
    one click away, each with a line saying what it FOUND rather than what it
    is numbered. The header now answers only the three questions a newcomer
    actually has: what is this, can I see it, and where is the evidence.

    The same string is emitted for generated pages and injected into
    hand-written ones by ensure_masthead(), so there is exactly one definition
    of what the header is. Every class carries an mh- prefix because the
    artifacts own their own stylesheets and at least one of them already
    used .bar for something else entirely.
    """
    up = "../" if depth else ""

    def link(href, label, on):
        return '<a href="%s"%s>%s</a>' % (href, ' class="on"' if on else "",
                                          label)

    # Demos is an anchor on the landing page rather than a page of its own:
    # the demonstrations are seven separate files, a pill cannot point at
    # seven things, and putting them on the opening page is the point.
    items = [
        link("%sindex.html" % up, "Overview", active == "home"),
        link("%sindex.html#demos" % up, "Demos", active == "demos"),
        link("%sresearch.html" % up, "Research", active == "research"),
    ]
    home = ' aria-current="page"' if active == "home" else ""
    return (
        '<div class="mh-bar"><div class="mh-in">'
        '<a class="mh-home" href="%sindex.html"%s>%s'
        '<span class="mh-wm">Silencing the Span</span></a>'
        '<nav class="mh-nav">%s</nav></div></div>'
        % (up, home, LOGO, "".join(items)))



def shell(title, desc, body, active, depth):
    return (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n"
        "<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        "<title>" + title + "</title>\n"
        "<meta name=\"description\" content=\"" + desc + "\">\n"
        + FAVICON + "\n" + THEME_JS + "\n<style>" + CSS + "</style>\n</head>\n<body>\n"
        + bar(active, depth) + "\n<div class=\"wrap\">\n" + body
        + "\n</div>\n</body>\n</html>\n")


# ---------------------------------------------------------------------------
# Rendering the documents
# ---------------------------------------------------------------------------

SRC_TO_SLUG = {}
for _p, _s, _t, _l, _d in DOCS:
    SRC_TO_SLUG[os.path.normpath(_p).replace("\\", "/").lower()] = _s

CODE_EXT = (".py", ".json", ".txt", ".csv", ".yml", ".cfg")


def rewrite_href(href, src_dir):
    """Repoint a link written for the repository at the rendered site."""
    if not href or href.startswith(("http://", "https://", "mailto:", "#")):
        return href
    target, _, frag = href.partition("#")
    frag = ("#" + frag) if frag else ""
    if not target:
        return href
    norm = os.path.normpath(os.path.join(src_dir, target)).replace("\\", "/")
    low = norm.lower()
    if low.endswith(".md"):
        slug = SRC_TO_SLUG.get(low)
        return (slug + ".html" + frag) if slug else (BLOB + norm)
    if low.endswith(CODE_EXT) or os.path.basename(norm) == "LICENSE":
        return BLOB + norm
    if low.endswith(".html"):
        return "../" + norm + frag
    return "../" + norm + frag


def mark_register(html):
    """Put a tick or an empty box on each row of the rendered method register.

    The register in README.md is the authoritative status source and is parsed
    by parse_methods(), so it is NOT edited to carry a glyph - a tick typed
    into the markdown could drift from the status text beside it. The marker is
    derived here from the same status cell the parser reads, using the same
    row test (five cells, first one a bare number), so the two cannot disagree.
    """
    ROW = re.compile(r"<tr>\s*(<td.*?</td>)\s*</tr>", re.S)
    CELL = re.compile(r"<td[^>]*>(.*?)</td>", re.S)

    def strip(s):
        return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()

    def one(m):
        cells = CELL.findall(m.group(1))
        if len(cells) != 5 or not strip(cells[0]).isdigit():
            return m.group(0)
        status = strip(cells[4]).lower()
        if status.startswith(("executed", "built as")):
            mk = '<span class="mk on" title="Executed"></span> '
        elif status.startswith(("partially executed", "tooling built")):
            mk = ('<span class="mk half" title="Partial - the work was done, '
                  'the result was not obtained"></span> ')
        else:
            mk = '<span class="mk off" title="Not started"></span> '
        row = m.group(0)
        # Only the LAST cell is touched, so the method number and name are
        # returned exactly as the markdown wrote them.
        head, sep, tail = row.rpartition("<td")
        inner = tail.split(">", 1)
        return head + sep + inner[0] + ">" + mk + inner[1]

    return ROW.sub(one, html)


def render_doc(src, slug, title, stats):
    md_text = read(src)
    src_dir = os.path.dirname(src).replace("\\", "/")

    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "sane_lists", "toc", "attr_list"],
        extension_configs={"toc": {"slugify": gh_slug, "toc_depth": "2-3"}})
    html = md.convert(md_text)

    html = re.sub(r'href="([^"]*)"',
                  lambda m: 'href="%s"' % rewrite_href(m.group(1), src_dir),
                  html)
    html = re.sub(r"(<table\b)", r'<div class="tw">\1', html)
    html = html.replace("</table>", "</table></div>")

    if src == "README.md":
        html = mark_register(html)

    toc = ['<div class="h">On this page</div>']
    for tok in md.toc_tokens:
        toc.append('<a href="#%s">%s</a>' % (tok["id"], tok["name"]))
        for sub in tok.get("children", []):
            toc.append('<a class="l3" href="#%s">%s</a>'
                       % (sub["id"], sub["name"]))

    words = stats["words"][src]
    body = (
        '<div class="doclayout">\n'
        '<aside class="toc">' + "".join(toc) + '</aside>\n'
        '<main class="doc">\n'
        '<div class="note">'
        '<b>Rendered copy.</b> The authoritative version of this document is '
        '<a href="' + BLOB + src.replace("\\", "/") + '"><code>'
        + src.replace("\\", "/") + '</code></a> in the repository. '
        'This page is regenerated from it by '
        '<a href="' + BLOB + 'build_pages.py"><code>build_pages.py</code></a> '
        '&mdash; roughly ' + "{:,}".format(words) + ' words. '
        'Not peer-reviewed. No option in this document is recommended for '
        'procurement.</div>\n'
        + html +
        '\n<p class="foot">'
        '<a href="../research.html">&larr; All research</a> '
        '&middot; <a href="../index.html">Overview</a> '
        '&middot; <a href="' + BLOB + src.replace("\\", "/") + '">Source on '
        'GitHub</a> &middot; Built from <code>' + stats["sha"] + '</code> on '
        + stats["date"] + '.</p>\n'
        '</main>\n</div>\n')

    return shell("%s &mdash; Silencing the Span" % title,
                 "Rendered copy of %s from the Manhattan Bridge rail-noise "
                 "research repository." % src.replace("\\", "/"),
                 body, "research", 1)


# ---------------------------------------------------------------------------
# The two organising pages
#
# The site has one landing page and one research hub, and every card below is
# written as a SECTION FUNCTION returning a list of HTML strings so that a
# section can be moved from one page to the other without a word of it
# changing. That constraint is the whole point of the split: the information
# architecture was wrong, the writing was not, and a reorganisation that
# rewrites as it moves cannot be checked against what it replaced.
#
#   index.html      the opening page, and an executive summary. Hero, the
#                   headline numbers, the three ways in, the interactive
#                   demonstrations, and what has actually been found. A reader
#                   who has never heard of this problem should be able to stop
#                   here and know what it is.
#
#   research.html   everything underneath: the eleven documents with their
#                   highlights, where the investigation stands, the work queue,
#                   the scripts, the method, the conventions, and the work
#                   about the work. One nav item, because a newcomer counting
#                   twelve of them reads a wall, not a menu.
# ---------------------------------------------------------------------------

def _ctx(stats):
    """Everything more than one section needs, computed once."""
    return {
        "m_exec": [m for m in stats["methods"] if m["cls"] == "executed"],
        "m_part": [m for m in stats["methods"] if m["cls"] == "partial"],
        "m_tool": [m for m in stats["methods"] if m["cls"] == "tooling"],
        "by_num": {m["n"]: m for m in stats["methods"]},
        # The two "Meta" dashboards are about the work rather than about the
        # bridge. Listing them beside the demonstrations is what made the demos
        # and the usage page look like the same thing.
        "demos": [a for a in ARTIFACTS if a[1] != "Meta"],
        "metas": [a for a in ARTIFACTS if a[1] == "Meta"],
    }


def sec_hero(stats, c):
    o = []
    A = o.append

    # -- hero --------------------------------------------------------------
    A('<div class="hb">')
    A('<img class="pic" src="assets/hero-composite.jpg" alt="" '
      'srcset="assets/hero-composite-1200.jpg 1200w, '
      'assets/hero-composite.jpg 2400w" sizes="100vw" '
      'width="2400" height="1000" fetchpriority="high">')
    A('<div class="tint"></div>')
    A('<div class="hin">')
    A('<p class="kicker">Ethical Tech CoLab &middot; open research programme</p>')
    A('<h1>Silencing the Span</h1>')
    A('<p class="sub">Rail noise from the NYC Subway crossing the Manhattan '
      'Bridge into DUMBO, Brooklyn &mdash; measured by the operator, '
      'uncomplainable to the city, and unstudied where people actually are.</p>')

    A('<div class="wc" id="wc" aria-live="polite">')
    live = {"q": stats["max_q"], "methods": stats["n_methods"],
            "words": "{:,}".format(stats["total_words"])}
    cards = [(str(big).format(**live) if "{" in str(big) else big, u, l, h)
             for big, u, l, h in HERO_CARDS]
    for i, (big, unit, line, href) in enumerate(cards):
        tag = "a" if href else "div"
        attr = ' href="%s"' % href if href else ""
        A('<%s class="wcslide%s"%s data-i="%d">'
          '<span class="n">%s</span><div class="u">%s</div>'
          '<div class="l">%s</div></%s>'
          % (tag, " on" if i == 0 else "", attr, i, big, unit, line, tag))
    A("</div>")
    A('<div class="wcnav" id="wcnav">')
    for i, (big, _u, _l, _h) in enumerate(cards):
        A('<button type="button" data-i="%d" aria-current="%s" '
          'aria-label="Statement %d of %d: %s"></button>'
          % (i, "true" if i == 0 else "false", i + 1, len(cards), big))
    A('<button type="button" class="pp" id="wcpp" aria-label="Pause the '
      'rotating statements">Pause</button>')
    A("</div>")

    A('<p class="lede" style="margin-top:26px">This is the short version: what '
      'the problem is, artifacts you can hear and navigate for yourself, and '
      'what has actually been established. <a href="research.html">The '
      'research</a> holds the evidence underneath it &mdash; every document, '
      'the open questions, the work still to be done, and the claims this '
      'programme has had to withdraw. Both pages are regenerated from the '
      'repository, so the counts on them cannot drift away from the work.</p>')
    A('<p class="cred">Photograph: Historic American Engineering Record '
      'NY-127-7, Jack E. Boucher, National Park Service, via '
      '<a href="https://www.loc.gov/item/ny0980/">Library of Congress</a> '
      '&mdash; no known restrictions on images made by the U.S. Government. '
      'Overlaid wireframe rendered from this repository\'s own '
      '<a href="visual-review/model-3d.html">3D model</a>, so it is inferred '
      'geometry and not a survey. Composited by '
      '<a href="' + BLOB + 'make_hero.py"><code>make_hero.py</code></a>.</p>')
    A("</div>")
    A("</div>")

    A('<div class="card hero">')
    A('<div class="statrow">'
      '<div class="s"><div class="k">MTA-measured peak, Brooklyn Bridge Park</div>'
      '<div class="big">98.9</div>dB(A) average maximum</div>'
      '<div class="s"><div class="k">Weekday crossings, busiest hour</div>'
      '<div class="big">67</div>a train every 54 seconds</div>'
      '<div class="s"><div class="k">People living in the affected corridor</div>'
      '<div class="big">15.8k</div>to 21.4k, from tax lots</div>'
      '<div class="s"><div class="k">Rail noise complaints NYC 311 can accept</div>'
      '<div class="big">0</div>there is no category</div>'
      '</div>')
    A('<p style="margin-top:18px">The first two are the MTA\'s own figures and '
      'are the most reliable numbers here. The third is derived from public '
      'tax-lot data. <strong>The fourth is the finding this programme did not '
      'expect to make.</strong></p>')
    A('<div class="note bad" style="margin-top:16px"><strong>Read this before '
      'anything below it.</strong> <b>Nobody from this programme has stood in '
      'Brooklyn Bridge Park with an instrument.</b> Every level quoted here was '
      'measured by someone else and published; every level <i>modelled</i> here '
      'is synthetic. <a href="research.html#status">Where the investigation '
      'stands</a> sets out how little of the specified work has actually been '
      'done.</div>')
    A('</div>')
    return o


def sec_start(stats, c):
    o = []
    A = o.append

    # -- start here --------------------------------------------------------
    A('<div class="card" id="start">')
    A('<h2>Start here</h2>')
    A('<p class="lede">Three different readers want three different things.</p>')
    A('<div class="tiles">')
    A('<a class="tile" href="visual-review/acoustic-demo.html">'
      '<div class="t">I want to hear it &rarr;</div>'
      '<div class="d">The acoustic demonstration. A train approaching, passing '
      'and departing at the correct decibel difference against each receptor\'s '
      'measured background &mdash; then running continuously at the real '
      'headway.</div>'
      '<div class="look">Start with <b>Brooklyn Bridge Park dog run</b>, one '
      'pass-by, then switch to continuous at 20&times; speed.</div></a>')
    A('<a class="tile" href="read/readme.html">'
      '<div class="t">I want the argument &rarr;</div>'
      '<div class="d">The repository README. Headline findings, the full '
      'document index, the method register with its honest status column, and a '
      'section called &ldquo;what has not been done&rdquo; that is longer than '
      'most projects\' results sections.</div>'
      '<div class="look">Read <b>Three headline findings</b>, then <b>What has '
      'not been done</b>.</div></a>')
    A('<a class="tile" href="visual-review/frequency-dashboard.html">'
      '<div class="t">I want the data &rarr;</div>'
      '<div class="d">The frequency and exposure dashboard. Every crossing by '
      'hour, route and direction; how many people are underneath; how long they '
      'stay; and three of this programme\'s own withdrawn claims, printed on '
      'the page.</div>'
      '<div class="look">Drag the coincidence window from 1&nbsp;s to '
      '29&nbsp;s. <b>The answer does not move.</b> That is a finding about the '
      'feed, not the railway.</div></a>')
    A('</div></div>')
    return o


def sec_demos(stats, c):
    o = []
    A = o.append
    demos = c["demos"]

    # -- demonstrations ----------------------------------------------------
    A('<div class="card" id="demos">')
    A('<h2>Interactive demonstrations</h2>')
    A('<p>Each is a <strong>single self-contained HTML file</strong>: no build '
      'step, no server, no network access, no dependencies, no tracking. Open '
      'it here, or download it and double-click. Each applies the same '
      'provenance discipline to a different medium.</p>')
    A('<div class="tiles">')
    for path, kind, title, what, look in demos:
        A('<a class="tile" href="%s">'
          '<div class="t">%s <span class="badge acc">%s</span></div>'
          '<div class="d">%s</div>'
          '<div class="look">%s</div></a>'
          % (path, title, kind, what, look))
    A('</div>')
    A('<div class="note"><strong>A warning that applies to all %s.</strong> The '
      '3D model contains <strong>zero measured elements</strong>. The audio is '
      '<strong>synthesised, not recorded</strong>. The agent model\'s '
      'itineraries are <strong>invented</strong>. These are instruments for '
      'reasoning about a problem, not evidence about it &mdash; and each says '
      'so in its own interface rather than in a footnote somewhere else.</div>'
      % spell(len(demos)))
    A('</div>')
    return o


def sec_status(stats, c):
    o = []
    A = o.append
    m_exec, m_part, m_tool = c["m_exec"], c["m_part"], c["m_tool"]

    # -- status board ------------------------------------------------------
    # First thing on the research page, and deliberately not on the front one.
    # A reader who has just been shown five working artifacts is the reader
    # most likely to over-estimate how much of this programme has been done,
    # so this is the correction, and it is the first thing they meet when they
    # come looking for the evidence behind those artifacts.
    A('<div class="card" id="status">')
    A('<h2>Where the investigation stands</h2>')
    A('<p class="lede">%s research documents, %s interactive artifacts, %s '
      'runnable scripts and roughly %s words &mdash; against %s specified '
      'methods of which <strong>%s have been executed and %s partially</strong>. '
      'The gap between those two halves of the sentence is the honest summary '
      'of this programme, and it is the reason this section leads the research '
      'rather than the front page: <b>the artifacts are the most finished '
      'thing here and the least load-bearing.</b></p>'
      % (spell(len(DOCS) - 1).capitalize(), spell(len(ARTIFACTS)),
         spell(len(SCRIPTS)), "{:,}".format(stats["total_words"]),
         spell(stats["n_methods"]), spell(stats["n_exec"]),
         spell(stats["n_partial"])))

    A('<div class="tw"><table><thead><tr>'
      '<th>State</th><th>Count</th><th>What it means</th></tr></thead><tbody>')
    A('<tr><td><span class="badge ok">Executed</span></td><td><b>%d</b> of %d '
      'methods</td><td>%s. <b>Every one of them changed something</b>, and two '
      'contradicted claims this repository had already published.</td></tr>'
      % (stats["n_exec"] + stats["n_partial"], stats["n_methods"],
         ", ".join("Method %d" % m["n"]
                   for m in sorted(m_exec + m_part, key=lambda x: x["n"]))))
    A('<tr><td><span class="badge warn">Tooling built</span></td><td><b>%d</b></td>'
      '<td>%s &mdash; the code is written and verified against the live feed, '
      'but the run has not been done.</td></tr>'
      % (len(m_tool), ", ".join("Method %d" % m["n"] for m in m_tool) or "none"))
    A('<tr><td><span class="badge no">Not started</span></td><td><b>%d</b></td>'
      '<td>Proposals. Several of the cheapest are also the most load-bearing, '
      'and their being undone is why so many claims here are hedged.</td></tr>'
      % (stats["n_methods"] - stats["n_exec"] - stats["n_partial"] - len(m_tool)))
    A('<tr><td><span class="badge acc">Withdrawn</span></td><td><b>%d</b> '
      'explicit retractions</td><td>Claims this programme published and then '
      'disproved. They are <b>left visible in the text</b> rather than deleted, '
      'which is the point.</td></tr>' % stats["withdrawals"])
    A('<tr><td><span class="badge">Open questions</span></td><td><b>Q1&ndash;Q%d</b></td>'
      '<td>Numbered, attributed to a document, and none of them rhetorical. '
      'Q42 is the highest-value one and a lawyer could settle it in a day.</td></tr>'
      % stats["max_q"])
    A('</tbody></table></div>')

    A('<div class="note bad"><strong>The one thing to carry away from '
      'everything above.</strong> <b>Nobody from this programme has stood in '
      'Brooklyn Bridge Park with an instrument.</b> Every acoustic level quoted '
      'here was measured by someone else and published; every acoustic level '
      '<i>modelled</i> here is synthetic. No option in any document is '
      'recommended for procurement, and none of it is peer-reviewed.</div>')
    A('</div>')
    return o


def sec_findings(stats, c):
    o = []
    A = o.append

    # -- findings ----------------------------------------------------------
    A('<div class="card" id="findings">')
    A('<h2>What has actually been found</h2>')

    A('<h3>1. The problem is documented, and then abandoned</h3>')
    A('<p>The MTA measured the noise, in DUMBO, at named addresses, and '
      'published the levels. The levels are high. Nothing followed. The '
      'measurement exists and the response does not, and the gap between those '
      'two facts is where this programme lives.</p>')

    A('<h3>2. Three instruments for recording city noise, and no rail category '
      'in any of them</h3>')
    A('<p>NYC 311 has a complaint descriptor for ice cream trucks and one for '
      '&ldquo;other animals&rdquo;. It has none for trains. Neither does SONYC, '
      'NYU\'s 150-million-clip urban sound corpus, whose authors state in print '
      'that they built their taxonomy from the NYC noise code &mdash; which is '
      'where the absence originates.</p>')
    A('<div class="note bad">Within 500&nbsp;m of the park where the MTA '
      'measured <strong>87.50 dB(A)</strong>, residents filed <strong>4,055'
      '</strong> noise complaints since 2020 and <strong>not one of them can be '
      'about the train.</strong> That same circle produced 117 complaints about '
      'ice cream trucks and 95 about barking dogs. <em>The dogs at the dog run '
      'are complainable. The trains over it are not.</em></div>')
    A('<p>This is a mechanism rather than a motive, which makes it testable, and '
      'it yields the first remedy in the programme that a resident could act on '
      'this month: amending a taxonomy is a far smaller ask than solving the '
      'noise.</p>')

    A('<h3>3. Exposure peaks in the early afternoon &mdash; and this programme '
      'got that wrong twice first</h3>')
    A('<p>Exposure is people multiplied by events. Optimising on attendance '
      'alone pointed to the weekend afternoon. Optimising on train rate alone '
      'pointed to the weekday morning. <strong>Both were published here and both '
      'are withdrawn.</strong> Train rate is nearly flat from 07:00 to 19:00 '
      'while the number of people underneath changes by a factor of four, so the '
      'product peaks between the two: <strong>14:00 on a weekday</strong>, 13:00 '
      'Saturday, 15:00 Sunday.</p>')

    A('<h3>4. A population\'s composition cannot be recovered from its departure '
      'curve</h3>')
    A('<p>A four-cohort model pins <em>total</em> non-resident presence to about '
      '&plusmn;10%. The <em>split</em> between workers and visitors inside that '
      'total swings by more than half again across thousands of parameter sets '
      'that fit the data equally well. <strong>A departure curve carries no job '
      'titles</strong> &mdash; someone present for eight hours looks identical '
      'whether they came to work or came for the day. On a Saturday the model is '
      'explicitly degenerate and says so in its own output.</p>')

    A('<h3>5. Distance does not order the measurements, and a propagation model '
      'was withdrawn before publication</h3>')
    A('<div class="note bad">The three near-bridge sites agree with ideal '
      'line-source spreading to <strong>0.15 dB</strong>, which looks like a '
      'result and is not one. Jittering the digitised positions by '
      '&plusmn;10&nbsp;m &mdash; well inside the error of reading a point off a '
      'scanned figure &mdash; moves the fitted decay exponent anywhere from '
      '<strong>0.7 to 22.3</strong>, and the dog run sits <strong>17.3 dB '
      'above</strong> the fit. The agreement is coincidence.</div>')
    A('<p>The model was therefore <strong>retracted before it was published '
      'rather than after</strong> &mdash; the first time in this programme that '
      'has happened in that order. It is also under review in its own right, at '
      '<a href="%s28">issue #28</a>, because <b>a negative result asserted from '
      'four points is as vulnerable to over-claiming as a positive one.</b></p>'
      % ISSUES)

    A('<h3>6. Twenty-one years of measurement without mitigation, and a blank '
      'cell in a statute helps explain it</h3>')
    A('<p>The levels have been on the record for two decades. The legal '
      'mechanism joining that record to the absence of any remedy is rated '
      '<b>2/5 and written as a question, not a finding</b> &mdash; and the '
      'document that proposes it names that joint as the first place to attack '
      'it, because the finding is elegant and arrived unexpectedly, which is '
      'exactly the condition under which this programme has previously '
      'over-claimed.</p>')
    A('</div>')
    return o


def sec_todo(stats, c):
    o = []
    A = o.append
    by_num = c["by_num"]

    # -- work: done, then to be done ---------------------------------------
    A('<div class="card" id="todo">')
    A('<h2>Work: done, and to be done</h2>')
    A('<p class="lede">A mark here means the work was finished, <b>not that '
      'the question it was meant to answer is settled</b> &mdash; in three '
      'cases below the finished work is what established that the question is '
      'harder than it looked. The ordering of the open queue is a judgement; '
      'the state of every numbered method is <b>read out of the register</b> '
      'rather than asserted here, and this page will not build if the two '
      'disagree.</p>')
    A('<div class="legend">'
      '<span><span class="mk on"></span>Done</span>'
      '<span><span class="mk half"></span>The work was done, the result was '
      'not obtained</span>'
      '<span><span class="mk off"></span>Not started</span>'
      '</div>')

    A('<div class="donehead"><h3>Done</h3>'
      '<span class="cnt">%d of %d items on this page</span></div>'
      % (len(DONE), len(DONE) + len(TODO)))
    for head, meth, cost, why in DONE:
        if isinstance(meth, int):
            # The marker is READ OUT OF THE REGISTER, not typed here. A tick on
            # this page that the register denies is exactly the drift the whole
            # programme is built to prevent, so a mismatch is a hard failure.
            row = by_num.get(meth)
            if row is None:
                sys.exit("DONE claims Method %d, which is not in the register."
                         % meth)
            if row["cls"] == "executed":
                state = "on"
            elif row["cls"] in ("partial", "tooling"):
                state = "half"
            else:
                sys.exit("DONE lists Method %d as finished, but the register "
                         "says %r. Fix one of them." % (meth, row["status"]))
        elif meth in ("done", "partial"):
            state = "on" if meth == "done" else "half"
        else:
            sys.exit("DONE entry %r has an unusable second field %r."
                     % (head, meth))
        A('<div class="q qdone"><div class="lab done">'
          '<span class="mk %s"></span><span>%s</span></div><div>'
          '<div class="h">%s</div><div class="cost">%s</div>'
          '<div class="why">%s</div></div></div>'
          % (state, "Done" if state == "on" else "Partial", head, cost, why))

    A('<div class="donehead"><h3>To be done</h3>'
      '<span class="cnt">%d of %d items on this page</span></div>'
      % (len(TODO), len(DONE) + len(TODO)))
    labels = {"blocking": "Blocking", "cheap": "Cheap &amp; high value",
              "field": "Fieldwork", "review": "Needs review", "gate": "Gating"}
    for kind, head, cost, why in TODO:
        A('<div class="q"><div class="lab %s">'
          '<span class="mk off"></span><span>%s</span></div><div>'
          '<div class="h">%s</div><div class="cost">%s</div>'
          '<div class="why">%s</div></div></div>' %
          (kind, labels[kind], head, cost, why))

    A('<div class="note"><strong>The count above is of items on this '
      'page, and is not the state of the programme.</strong> The register '
      'holds %d methods, of which <b>%d have been executed or partially '
      'executed</b>. Anything that reads as encouraging progress here should '
      'be read against that ratio.</div>'
      % (stats["n_methods"], stats["n_exec"] + stats["n_partial"]))
    A('<div class="note good"><strong>The cheapest useful contribution is a '
      'recording.</strong> If you have ever recorded a train crossing the '
      'Manhattan Bridge from Brooklyn Bridge Park, DUMBO or the Williamsburg '
      'Bridge walkway, that file is more useful to this programme than anything '
      'currently in it. The bar is far lower than people assume: <b>spectral '
      'shape and event timing survive an uncalibrated phone.</b></div>')
    A('</div>')
    return o


def sec_documents(stats, c):
    o = []
    A = o.append

    # -- documents ---------------------------------------------------------
    A('<div class="card" id="documents">')
    A('<h2>The research documents</h2>')
    A('<p>Rendered here for reading. The markdown files in the repository '
      'remain authoritative, and each rendered page links back to its '
      'source.</p>')
    A('<div class="tw"><table><thead><tr><th>Document</th><th>What it asks</th>'
      '<th style="white-space:nowrap">Words</th></tr></thead><tbody>')
    for src, slug, title, _label, desc in DOCS:
        A('<tr><td style="white-space:nowrap"><a href="read/%s.html"><b>%s</b></a>'
          '<br><code style="font-size:0.78em">%s</code></td>'
          '<td>%s</td><td>%s</td></tr>'
          % (slug, title, src.replace("\\", "/"), desc,
             "{:,}".format(stats["words"][src])))
    A('</tbody></table></div>')
    A('</div>')
    return o


def sec_code(stats, c):
    o = []
    A = o.append

    # -- data and code -----------------------------------------------------
    A('<div class="card" id="code">')
    A('<h2>Data and code</h2>')
    A('<p>Every script runs against live public feeds and can be re-run from '
      'scratch by anyone. The schedule figures they produce are rated 5/5 '
      '&mdash; read directly from the MTA\'s own published feed.</p>')
    A('<div class="tw"><table><thead><tr><th>Script</th><th>What it does</th>'
      '<th style="white-space:nowrap">Size</th></tr></thead><tbody>')
    for path, desc in SCRIPTS:
        A('<tr><td style="white-space:nowrap"><a href="%s%s"><code>%s</code></a></td>'
          '<td>%s</td><td>%d&nbsp;KB</td></tr>'
          % (BLOB, path, os.path.basename(path), desc, size_kb(path)))
    for path, desc in DATASETS:
        A('<tr><td style="white-space:nowrap"><a href="%s%s"><code>%s</code></a></td>'
          '<td>%s</td><td>%d&nbsp;KB</td></tr>'
          % (BLOB, path, os.path.basename(path), desc, size_kb(path)))
    A('</tbody></table></div>')
    A('<div class="note warn"><strong>The trap that took three attempts to '
      'find.</strong> The MTA\'s turnstile feed publishes <code>entries</code> '
      'at a station, which sounds like people arriving in the neighbourhood and '
      'is the exact opposite: an entry is somebody going <em>down into</em> the '
      'system and <em>leaving</em>. Reading it the natural way inverts the daily '
      'curve, and it will look entirely plausible while doing so. That directional '
      'trap and three others are documented in '
      '<a href="read/data-collection.html">the data-collection notes</a>.</div>')
    A('</div>')
    return o


def sec_method(stats, c):
    o = []
    A = o.append

    # -- method ------------------------------------------------------------
    A('<div class="card" id="method">')
    A('<h2>How this investigation works</h2>')
    A('<p class="lede">This is an <strong>open, unfinished investigation</strong>, '
      'not a report. It is published while it is still wrong in places, because '
      'the method depends on that being visible.</p>')

    A('<p>The programme applies the methodology from '
      '<a href="https://github.com/Ethical-Tech-CoLab/ai-research-question-assistant">'
      '<code>ai-research-question-assistant</code></a> &mdash; '
      '<i>AI-Powered Assistance in Formulating Research Questions</i> '
      '(Rhodes et al.), &sect;8. Its central move is that '
      '<strong>gap identification and contradiction detection come before '
      'question formulation.</strong> You do not start from what you want to '
      'prove. You start by reading what the record already contains, finding '
      'where it stops, and writing the question it never asked.</p>')

    A('<div class="mgrid">')
    A('<div class="m"><div class="mn">%d</div>'
      '<div class="mt">questions derived this way</div>'
      '<p>Numbered Q1 to Q%d and carried across every document, so a question '
      'raised in one place can be answered or killed in another.</p></div>'
      % (stats["max_q"], stats["max_q"]))
    A('<div class="m"><div class="mn">%d</div>'
      '<div class="mt">methods specified to answer them</div>'
      '<p>Each with a cost, a named question and an honest status. '
      '<strong>%d have been executed.</strong> The register does not hide the '
      'ratio.</p></div>' % (stats["n_methods"], stats["n_exec"]))
    A('<div class="m"><div class="mn">%d</div>'
      '<div class="mt">explicit retractions</div>'
      '<p>Every one was published here, disproved here, and left standing in '
      'the text with the correction beneath it. <strong>That count going up is '
      'the method working, not failing.</strong></p></div>'
      % stats["withdrawals"])
    A('</div>')

    A('<h3 style="margin-top:22px">Hypotheses, not positions</h3>')
    A('<p>Every question here is written so that it can come back <em>no</em>. '
      'That is a deliberate constraint and it has cost this programme several '
      'of its more attractive claims &mdash; the three-site propagation fit, '
      'the peak-hour argument, and the assumption that the tool kept no record '
      'of its own cost. Each was a reasonable reading of real data. Each turned '
      'out to be wrong, and each is still on the page, because '
      '<strong>a research record that only shows its surviving claims is not '
      'showing its method.</strong></p>')
    A('<p>What follows from that is the uncomfortable part: '
      '<b>nothing here is a finding until someone has stood under the bridge '
      'with an instrument.</b> The questions are sharp. The evidence behind '
      'them is second-hand, and every page says so where it applies. '
      '<a href="#status">Where the investigation stands</a> gives the honest '
      'ratio, and <a href="#todo">what to do next</a> lists the work that '
      'would settle it.</p>')
    A('</div>')
    return o


def sec_conventions(stats, c):
    o = []
    A = o.append

    # -- conventions -------------------------------------------------------
    A('<div class="card" id="conventions">')
    A('<h2>How to read anything in here</h2>')
    A('<p class="lede">Five conventions apply across every document and every '
      'artifact. They exist because this programme has failed adversarial '
      'review repeatedly, and always the same way: <strong>over-claiming from '
      'abstract-level reading.</strong></p>')
    A('<ol>')
    for head, body_txt in CONVENTIONS:
        A('<li><strong>%s.</strong> %s</li>' % (head, body_txt))
    A('</ol>')
    A('</div>')
    return o


def sec_behind(stats, c):
    o = []
    A = o.append
    metas = c["metas"]

    # -- behind the scenes -------------------------------------------------
    # Placed here deliberately, near the foot. This is real research and it is
    # linked from every page in the header, but a reader arriving at this site
    # came for the bridge. Putting the cost of the study above the study
    # inverts that, and previously these two dashboards sat in the demos
    # section, where they read as if they were part of the investigation's
    # findings rather than an account of how it was made.
    A('<div class="card" id="behind">')
    A('<h2>Behind the scenes</h2>')
    A('<p class="lede">Two pieces of work <strong>about</strong> this '
      'investigation rather than about the bridge: what it cost to produce, '
      'measured from the tool\'s own per-request log, and what the same '
      'deliverable would have cost to buy from a consultancy. Both are held '
      'to the same evidence standard as everything else here, and both '
      'withdraw a headline claim on their own front page.</p>')
    A('<div class="tiles">')
    for src, slug, title, _label, desc in DOCS:
        if slug not in BEHIND_THE_SCENES:
            continue
        A('<a class="tile" href="read/%s.html">'
          '<div class="t">%s <span class="badge acc">Document</span></div>'
          '<div class="d">%s</div></a>' % (slug, title, desc))
    for path, kind, title, what, look in metas:
        A('<a class="tile" href="%s">'
          '<div class="t">%s <span class="badge acc">%s</span></div>'
          '<div class="d">%s</div>'
          '<div class="look">%s</div></a>'
          % (path, title, kind, what, look))
    A('</div>')
    A('<div class="note">Why this is published at all: the cost of producing '
      'research with these tools is <strong>routinely asserted and almost '
      'never measured</strong>. Both pages exist so that the assertion here '
      'can be checked, including the parts that come out unflattering '
      '&mdash; the human direction time alone costs about '
      '<strong>eight and a half times</strong> the entire metered inference '
      'bill, which is the opposite of the usual claim.</div>')
    A('</div>')
    return o


def sec_help(stats, c):
    o = []
    A = o.append

    # -- help --------------------------------------------------------------
    A('<div class="card" id="help">')
    A('<h2>How to help</h2>')
    A('<p>This is a working research repository, not a publication. Corrections '
      'are more valuable than agreement.</p>')
    A('<ul>'
      '<li><strong>Post a recording.</strong> See '
      '<a href="read/field-capture-protocol.html">the field capture protocol</a> '
      'for what makes one usable.</li>'
      '<li><strong>Falsify a &ldquo;not found&rdquo; claim.</strong> Five have '
      'already failed. The prior on others failing is not low.</li>'
      '<li><strong>Execute any method.</strong> Several cost an email, a form, '
      'or an afternoon.</li>'
      '<li><strong>Challenge the arithmetic.</strong> The event-duration '
      'derivation, the cohort identifiability result and the propagation '
      'rejection are each either right or wrong, and none has been reviewed by '
      'anyone. Issues <a href="' + ISSUES + '26">#26</a>, '
      '<a href="' + ISSUES + '27">#27</a> and '
      '<a href="' + ISSUES + '28">#28</a> exist specifically to attack them.</li>'
      '<li><strong>Reclassify a component\'s provenance.</strong> Anyone with '
      'structural knowledge of riveted lattice trusses will find '
      'misclassifications in the 3D model, and finding them is the point of '
      'publishing the classification.</li>'
      '</ul>')
    A('<div class="note good"><strong>One standing condition.</strong> The '
      'people who live under this bridge have been asking for help since 2008. '
      'Any contact with them must offer something before it asks for anything, '
      'must not represent this programme as more established than it is, and '
      'must make clear that its central artifacts are <strong>synthetic</strong>. '
      'Over-claiming to a community in that position would be a different and '
      'worse kind of error than the ones already made here.</div>')
    A('</div>')
    return o


def sec_foot(stats, c):
    o = []
    A = o.append
    A('<p class="foot"><strong>Silencing the Span: Defining the Manhattan Bridge '
      'Rail-Noise Problem in DUMBO for a Design-Build Intervention.</strong> '
      'Ethical Tech CoLab. Research content released under '
      '<a href="' + BLOB + 'LICENSE">CC BY 4.0</a>. Not peer-reviewed. '
      'No option in any document is recommended for procurement.<br><br>'
      'This page was generated by <a href="' + BLOB + 'build_pages.py">'
      '<code>build_pages.py</code></a> from commit <code>' + stats["sha"]
      + '</code> on ' + stats["date"] + '. '
      '<a href="https://github.com/' + REPO + '">Repository</a> &middot; '
      '<a href="' + ISSUES + '">Open issues</a></p>')
    return o


# ---------------------------------------------------------------------------
# The two pages, assembled from those sections
# ---------------------------------------------------------------------------

def sec_research_head(stats, c):
    """The hub's own opening: what is here, and one highlight per document.

    Every highlight below is a statement already published elsewhere on this
    site - in the README's headline findings, in a document's own abstract, or
    in the register. Nothing here is a new claim. A hub that summarises by
    paraphrasing is a hub that can drift away from what it indexes, so these
    are quotations of the programme's own conclusions and are checked against
    the documents when either changes.
    """
    o = []
    A = o.append

    # A document with no highlight is a document nobody asked "what did it
    # find?" about. Fail rather than render a blank tile.
    missing = [s for _p, s, _t, _l, _d in DOCS if s not in HIGHLIGHTS]
    if missing:
        sys.exit("HIGHLIGHTS has no entry for: %s" % ", ".join(missing))
    live = {"methods": stats["n_methods"],
            "done": stats["n_exec"] + stats["n_partial"],
            "q": stats["max_q"], "withdrawals": stats["withdrawals"]}
    hi = {k: (v.format(**live) if "{" in v else v)
          for k, v in HIGHLIGHTS.items()}

    A('<div class="card" id="research-top">')
    A('<h2>The research</h2>')
    A('<p class="lede">%s documents and roughly %s words, in the order they '
      'were written. Each asks one question, answers as much of it as the '
      'evidence allows, and ends with a section on where it is most likely to '
      'be wrong. <strong>They are meant to be read out of order</strong> '
      '&mdash; start with whichever question is yours.</p>'
      % (spell(len(DOCS)).capitalize(),
         "{:,}".format(stats["total_words"])))

    A('<div class="statrow">'
      '<div class="s"><div class="k">Documents</div>'
      '<div class="big">%d</div>each one question</div>'
      '<div class="s"><div class="k">Methods specified</div>'
      '<div class="big">%d</div>%d executed or partly</div>'
      '<div class="s"><div class="k">Questions derived</div>'
      '<div class="big">%d</div>Q1 to Q%d, none rhetorical</div>'
      '<div class="s"><div class="k">Claims withdrawn</div>'
      '<div class="big">%d</div>left standing in the text</div>'
      '</div>'
      % (len(DOCS), stats["n_methods"], stats["n_exec"] + stats["n_partial"],
         stats["max_q"], stats["max_q"], stats["withdrawals"]))

    A('<h3 style="margin-top:26px">The investigation</h3>')
    A('<div class="tiles">')
    for src, slug, title, _label, desc in DOCS:
        if slug in BEHIND_THE_SCENES:
            continue
        A('<a class="tile" href="read/%s.html">'
          '<div class="t">%s <span class="badge acc">%s words</span></div>'
          '<div class="d">%s</div>'
          '<div class="look">%s</div></a>'
          % (slug, title, "{:,}".format(stats["words"][src]), desc,
             hi[slug]))
    A('</div>')

    A('<h3 style="margin-top:26px">The work about the work</h3>')
    A('<p>Two documents that study this investigation rather than the bridge: '
      'what it cost to produce, measured from the tool\'s own per-request log, '
      'and what the same deliverable would have cost to buy. Both are held to '
      'the same evidence standard as everything else here, and both withdraw '
      'a headline claim on their own front page.</p>')
    A('<div class="tiles">')
    for src, slug, title, _label, desc in DOCS:
        if slug not in BEHIND_THE_SCENES:
            continue
        A('<a class="tile" href="read/%s.html">'
          '<div class="t">%s <span class="badge acc">%s words</span></div>'
          '<div class="d">%s</div>'
          '<div class="look">%s</div></a>'
          % (slug, title, "{:,}".format(stats["words"][src]), desc,
             hi[slug]))
    A('</div>')

    A('<div class="note">Looking for the interactive pieces instead? They are '
      'on the <a href="index.html#demos">front page</a>, where a reader who '
      'has never heard of this problem will find them first. This page is the '
      'evidence underneath them.</div>')
    A('</div>')
    return o


def sec_handoff(stats, c):
    """The one card on the landing page that exists only because of the split.

    Everything above it on the index is the argument. This is the door to the
    evidence, and it is written as a door: named documents, honest word count,
    and no pretence that reading them is a small undertaking.
    """
    o = []
    A = o.append
    A('<div class="card" id="research">')
    A('<h2>The research behind all of it</h2>')
    A('<p class="lede">Everything above is a summary. <strong>%s documents, '
      'roughly %s words</strong>, every quantitative claim carrying a quoted '
      'source and a rating, and every error left standing in the text with the '
      'correction beneath it.</p>'
      % (spell(len(DOCS)).capitalize(), "{:,}".format(stats["total_words"])))
    A('<div class="tiles">')
    A('<a class="tile" href="research.html">'
      '<div class="t">Read the research &rarr;</div>'
      '<div class="d">One page indexing all %s documents with what each asks '
      'and what it found, plus where the investigation stands, the work queue, '
      'the runnable scripts, the method it follows, and the two pieces of work '
      'about the work itself.</div>'
      '<div class="look">If you read one thing, read <b>where the '
      'investigation stands</b> &mdash; %d of %d specified methods have '
      'actually been executed.</div></a>'
      % (spell(len(DOCS)), stats["n_exec"] + stats["n_partial"],
         stats["n_methods"]))
    A('<a class="tile" href="research.html#status">'
      '<div class="t">What is still wrong with it &rarr;</div>'
      '<div class="d">%d claims published on this site and then disproved on '
      'it. They are not deleted. Each is quoted where it was made, with the '
      'withdrawal underneath, because a research record that shows only its '
      'surviving claims is not showing its method.</div>'
      '<div class="look">Q1&ndash;Q%d are numbered, attributed, and none of '
      'them rhetorical.</div></a>'
      % (stats["withdrawals"], stats["max_q"]))
    A('</div>')
    A('</div>')
    return o


def build_index(stats):
    c = _ctx(stats)
    o = []
    for fn in (sec_hero, sec_start, sec_demos, sec_findings, sec_handoff,
               sec_foot):
        o.extend(fn(stats, c))
    o.append(HERO_JS)

    return shell(
        "Silencing the Span &mdash; Manhattan Bridge rail noise in DUMBO",
        "Open research on rail noise from the NYC Subway crossing the Manhattan "
        "Bridge into DUMBO, Brooklyn. What the problem is, interactive "
        "demonstrations you can hear and navigate, and what has been found.",
        "\n".join(o), "home", 0)


def build_research(stats):
    c = _ctx(stats)
    o = []
    for fn in (sec_research_head, sec_status, sec_todo, sec_documents,
               sec_code, sec_method, sec_conventions, sec_behind, sec_help,
               sec_foot):
        o.extend(fn(stats, c))

    return shell(
        "The research &mdash; Silencing the Span",
        "Every document, dataset, script and open question behind the "
        "Manhattan Bridge rail-noise investigation, with where it stands and "
        "what it still gets wrong.",
        "\n".join(o), "research", 0)


# ---------------------------------------------------------------------------

def write(rel, text):
    path = os.path.join(ROOT, rel)
    d = os.path.dirname(path)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print("  wrote %-42s %6d bytes" % (rel, len(text.encode("utf-8"))))


def ensure_favicon(rel):
    """The artifacts are hand-written and stay that way, except for this.

    Without an icon link every page silently requests /favicon.ico and takes
    a 404 on it, which shows up as a console error and makes a clean page look
    unclean. One line, inserted once, idempotent.
    """
    path = os.path.join(ROOT, rel)
    with io.open(path, encoding="utf-8") as fh:
        text = fh.read()
    if 'rel="icon"' in text:
        return False
    m = re.search(r'<meta name="viewport"[^>]*>', text)
    anchor = m.group(0) if m else "<head>"
    if anchor not in text:
        return False
    text = text.replace(anchor, anchor + "\n" + FAVICON, 1)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print("  patched favicon into %s" % rel)
    return True


MASTHEAD_CSS = """
/* Site masthead, injected by build_pages.py. Do not edit by hand.
   Every class is mh- prefixed. An artifact is free to own .bar, .in, .home,
   .mark or .nav for its own purposes, and one of them already does: the usage
   dashboard uses .bar for its horizontal bar-chart rows, which turned an
   un-prefixed masthead into a stacked column covering the page. */
.mh-bar { position: sticky; top: 0; z-index: 200; display: block;
  background: var(--cp-panel-strong); backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--cp-border); }
.mh-bar .mh-in { max-width: 1180px; margin: 0 auto; padding: 10px 22px;
  display: flex; align-items: center; gap: 14px; flex-wrap: wrap; }
.mh-bar .mh-home { font-weight: 700; color: var(--cp-text); font-size: 0.95rem;
  text-decoration: none; display: inline-flex; align-items: center; gap: 9px;
  white-space: nowrap; }
.mh-bar .mh-home .mh-mark { display: block; flex: none; border-radius: 6px;
  width: 26px; height: 26px; min-width: 26px; max-width: 26px; }
.mh-bar .mh-home:hover { color: var(--cp-accent); text-decoration: none; }
.mh-bar .mh-nav { display: flex; gap: 4px; flex-wrap: wrap; margin-left: auto;
  align-items: center; }
.mh-bar .mh-nav a { color: var(--cp-text-muted); font-size: 0.82rem;
  padding: 4px 9px; display: inline-block; font-weight: 400;
  border-radius: 999px; white-space: nowrap; text-decoration: none; border: 0; }
.mh-bar .mh-nav a:hover { background: var(--cp-accent-soft);
  color: var(--cp-accent); text-decoration: none; }
.mh-bar .mh-nav a.on { background: var(--cp-accent); color: var(--cp-accent-fg); }
.mh-bar .mh-nav .mh-sep { width: 1px; height: 17px; flex: none; margin: 0 7px;
  background: var(--cp-border-strong); border-radius: 1px; }
@media (max-width: 560px) { .mh-bar .mh-home .mh-wm { display: none; } }
"""

MAST_OPEN = "<!--MASTHEAD-->"
MAST_CLOSE = "<!--/MASTHEAD-->"


def artifact_nav_state(rel):
    """Which nav pill should light up when standing on a hand-written page.

    Not every hand-written page is a demonstration. The usage and procurement
    dashboards belong to their own documents, and marking them "demos" told a
    reader standing on the AI usage dashboard that they were looking at the
    interactive demos - which is how the meta pages came to appear to have
    taken the demos' place in the header.

    Derived from the artifact's own directory, so adding a dashboard under an
    existing document picks up the right state without another edit here.
    """
    d = os.path.dirname(rel).replace("\\", "/").split("/")[0]
    for _src, slug, _t, _l, _desc in DOCS:
        if slug in BEHIND_THE_SCENES and d == slug:
            return "research"
    return "demos"


def ensure_masthead(rel):
    """Put the same header on a hand-written artifact page.

    The artifacts are hand-written and stay that way, but navigation is not a
    per-page decision: a reader who lands on a demonstration from a search
    result needs the same way back that every other page offers. Before this,
    of seven artifacts three carried a hand-rolled bar with a different nav,
    one had a breadcrumb, one had a link at the very bottom, and two offered
    no way back to the site at all.

    Delimited by markers and rewritten in place on every run, so the header
    tracks DOCS rather than drifting. Any pre-existing hand-rolled bar is
    replaced, once, and its stylesheet rules are left alone - they are
    overridden by the block inserted here, which is emitted last.
    """
    path = os.path.join(ROOT, rel)
    with io.open(path, encoding="utf-8") as fh:
        text = fh.read()
    before = text

    html = MAST_OPEN + bar(artifact_nav_state(rel), 1) + MAST_CLOSE
    css = MAST_OPEN + "<style>" + MASTHEAD_CSS + "</style>" + MAST_CLOSE

    # A page assembled by copying another page's <head> arrives carrying the
    # CSS block and no bar. The idempotent branch below would then rewrite the
    # stylesheet, change nothing, and report success on a page that has no
    # header at all. Presence of a marker is not presence of a masthead:
    # check for each block by what it contains.
    has_css = re.search(re.escape(MAST_OPEN) + r"\s*<style>", text) is not None
    has_bar = re.search(re.escape(MAST_OPEN) + r'\s*<div class="mh-bar"',
                        text) is not None

    if has_css and has_bar:
        # Idempotent path: replace what a previous run inserted.
        text = re.sub(re.escape(MAST_OPEN) + r".*?" + re.escape(MAST_CLOSE),
                      lambda m: css if "<style>" in m.group(0) else html,
                      text, flags=re.S)
    else:
        # Retire any hand-rolled bar so two headers cannot stack, and any
        # half-present block, so the insert below cannot duplicate one.
        text = re.sub(re.escape(MAST_OPEN) + r".*?" + re.escape(MAST_CLOSE),
                      "", text, flags=re.S)
        text = re.sub(r'<div class="(?:mh-)?bar"><div class="(?:mh-)?in">.*?</div></div>',
                      "", text, count=1, flags=re.S)
        m = re.search(r"</head>", text)
        if not m:
            print("  SKIP masthead, no </head> in %s" % rel)
            return False
        text = text[:m.start()] + css + "\n" + text[m.start():]
        m = re.search(r"<body[^>]*>", text)
        if not m:
            print("  SKIP masthead, no <body> in %s" % rel)
            return False
        text = text[:m.end()] + "\n" + html + text[m.end():]

    # Nothing may leave this function with a stylesheet and no header.
    if text.count(MAST_OPEN) != 2 or '<div class="mh-bar"' not in text:
        raise SystemExit("masthead did not land correctly in %s "
                         "(%d marker blocks, bar present: %s)"
                         % (rel, text.count(MAST_OPEN),
                            '<div class="mh-bar"' in text))

    if text == before:
        return False
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print("  masthead -> %s" % rel)
    return True


def main():
    print("Reading repository...")
    stats = collect_stats()
    print("  %d methods: %d executed, %d partial, %d tooling-built"
          % (stats["n_methods"], stats["n_exec"], stats["n_partial"],
             stats["n_tooling"]))
    print("  questions run to Q%d" % stats["max_q"])
    print("  %d explicit withdrawal statements" % stats["withdrawals"])
    print("  %s words across %d documents"
          % ("{:,}".format(stats["total_words"]), len(DOCS)))
    print("  built from %s (%s)" % (stats["sha"], stats["date"]))

    print("Writing pages...")
    write(".nojekyll", "")
    write("index.html", build_index(stats))
    write("research.html", build_research(stats))
    for src, slug, title, _label, _desc in DOCS:
        write("read/%s.html" % slug, render_doc(src, slug, title, stats))

    missing = [p for p, _, _, _, _ in ARTIFACTS
               if not os.path.exists(os.path.join(ROOT, p))]
    if missing:
        print("WARNING: artifacts referenced but not present: %s" % missing)
        return 1
    for path, _, _, _, _ in ARTIFACTS:
        ensure_favicon(path)
        ensure_masthead(path)
    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
