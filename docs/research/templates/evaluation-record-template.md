# Evaluation / performance record title

> **Boundary note:** this is a bounded evaluation or performance record for V2 research and
> validation planning. It can support evidence gathering, but it is not runtime authority or
> promotion authority by itself.

## Status

- status: proposed | active | closed | superseded
- opened: YYYY-MM-DD
- working branch: `<branch-name>`
- lifecycle lane: research | validate
- evaluation type: quality | performance | security | regression | retrieval-lens | other

## Evaluation question

What bounded claim, behavior, or assumption is being evaluated?

## Candidate under review

- candidate surface: `path-or-name`
- intended change or behavior: short summary

## Baseline or comparison

- baseline surface: `path-or-name`
- comparison rule: what counts as same, better, worse, or unknown

## Source surfaces and fixtures

- `path/or/url` ÔÇö why it matters
- fixture or dataset boundary: local fixture | repo-tracked output | redacted sample | none

## Artifact layout

- input artifact:
- output artifact:
- summary artifact:
- failure artifact:
- storage boundary:

## Quality signals

- correctness signal
- reproducibility signal
- failure signal

## Performance signals

- latency / runtime budget, if relevant
- token / cost budget, if relevant
- memory / file-size budget, if relevant
- not applicable, if this is not a performance evaluation

## Summary table

| Signal | Baseline | Candidate | Result | Notes |
| ------ | -------- | --------- | ------ | ----- |
|        |          |           |        |       |

## Failure table

| Failure mode | Trigger | Observed? | Impact | Follow-up |
| ------------ | ------- | --------- | ------ | --------- |
|              |         | yes/no    |        |           |

## Security and data boundary

- secrets required: yes/no; name placeholders only, never values
- allowed data: public repo data | local fixtures | redacted outputs | other
- forbidden data: secrets, live private account data, non-redacted logs, or other sensitive payloads

## Method

How should the evaluation be run or inspected?

## Result summary

What happened, including pass/fail/unknown state?

## Interpretation

What does the result mean for the research or validation question?

## Validation evidence

- command, artifact, or review surface: result
- not validated yet, if still research-only

## Promotion decision

- no promotion: why
- candidate for validation: required next evidence
- candidate for promotion: target admitted authority or verification surface

## Linked log entry

- `docs/research/log.md` ÔÇö `## [YYYY-MM-DD] kind | title`

## Current status

Short current-state summary and next step.
