# Black-box experiments

> **Boundary note:** this page governs bounded black-box experiments for `docs/research/**`.
> These records help explain research and validation work, but they are not authority by themselves.

## Purpose

Give V2 a clean home for experiment records that make parameter, evaluation, result, and log
explicit.

Evaluation/performance records also live here until a narrower index is admitted. They should make
candidate, baseline, quality/performance/security signals, result, interpretation, and promotion
decision explicit.

## Minimum experiment record

Every experiment record should name:

- the parameter or question under test
- the evaluation surface
- the baseline or comparison point
- the result summary
- the linked `docs/research/log.md` entry

For eval/perf/security records, also name:

- the candidate under review
- quality and performance signals
- security and data boundary
- the promotion decision or reason for no promotion

## Good fits

- threshold checks
- sensitivity passes
- fixture-backed comparisons
- bounded validation probes
- quality/performance/security records for research tools, hosted-model helpers, or retrieval-lens probes

## Current registry

No admitted black-box experiment records are tracked yet.

## Next use

When the first experiment is added, start from `../templates/experiment-template.md`. When the
record is primarily evidence-oriented, start from `../templates/evaluation-record-template.md`.
Keep the scope narrow and record the result before promoting any durable conclusion elsewhere.
