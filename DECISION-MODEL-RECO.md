# Decision-model recommendation: qualify research evidence

Date: 2026-10-11. Public-source proposal; no acoustic or legal conclusion added.
Reviewed [README](https://github.com/Ethical-Tech-CoLab/manhattan-bridge-noise-dumbo/blob/8f773706699643382299444db2245b20e6697119/README.md).
This is a document-level assessment, not a replication of the research.

## Recommendation

Use bounded decisions to help prioritize source passages relevant to a named
open question, or flag whether a cited passage establishes a claim at the
stated place, time and measurement definition. Output supports / contradicts /
not established / insufficient evidence with exact source references.

Preserve the distinction between a problem definition and an engineered
mitigation design. Source-system omissions must not be converted into evidence
that an event never occurred. A model cannot infer an absent rail category's
unrecorded measurements.

## Keep deterministic

Decibel arithmetic, acoustic propagation, denominators, timestamps, source
counts and legal-text quotation remain in code or accountable expert review.
Do not use Jev to invent noise measurements, calibrate rejected models or
decide statutory compliance. Preserve negative results and exposed errors.

## Trial and gate

Compare human/lexical review and a local classifier with Jev's
[citation pattern](https://docs.typesafe.ai/cookbooks/citation_check.md),
Microsoft-Decision-1 and Sage on public sources. Split by source/claim family.
Include different acoustic metrics, unmatched periods, unmeasured scenarios
and absence-of-category cases. Measure false support, missing-evidence recall,
calibration and reviewer cost.

Derived annotations only, no changed quantitative or legal findings.
Adoption requires useful review gain without false reassurance. Exact
proprietary models are not locally downloadable; no cost or energy saving has
been measured for this project.
