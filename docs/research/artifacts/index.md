# Atomic runnable artifacts

> **Boundary note:** this page governs atomic runnable artifacts for `docs/research/**`.
> These artifacts are bounded clarity surfaces, not runtime-authority surfaces.

## Purpose

Give V2 a home for very small artifacts that show one idea, seam, or mechanism end-to-end.
The goal is clarity, not framework-building.

## What qualifies

An atomic artifact should usually satisfy all of the following:

- one bounded question
- one minimal artifact
- self-explanatory inputs and outputs
- runnable or inspectable without hidden context
- easy to delete, keep, or supersede

## Placement rules

- If the artifact is primarily documentation, record it here and link to the relevant source surfaces.
- If the artifact genuinely needs code, prefer a bounded admitted script surface such as `scripts/audit/`.
- Do not move experimental research code into `src/core/**` just to make it feel more official.

## Minimum artifact record

- bounded question
- source surfaces
- how to run or inspect
- expected output or signal
- short result summary
- linked `docs/research/log.md` entry

## Current inventory

No admitted atomic runnable artifacts are tracked yet.

## Next use

When the first artifact is added, record it with `../templates/artifact-template.md` and append a
short dated entry to `../log.md`.
