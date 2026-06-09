# Capability card title

> **Boundary note:** this page describes a bounded V2 capability for research or validation planning.
> It is not runtime authority, promotion authority, or permission to widen scope by itself.

## Status

- status: proposed | active | validated | superseded | retired
- opened: YYYY-MM-DD
- working branch: `<branch-name>`
- lifecycle lane: research | validate | promote
- capability type: agent skill | helper script | endpoint | workflow | checklist | other
- version: `<version-or-date>`
- provenance: source pattern, source repo, or local origin

## Purpose

What capability is being described, and why should V2 keep it legible?

## Owner and compatibility

- owner: `<person-or-role>`
- maintainer: `<person-or-role>`
- compatible lanes: research | validate | promote
- compatible surfaces:
- incompatible surfaces:

## Trigger / when to use

Use this capability when:

- condition 1
- condition 2

Do not use it when:

- condition 1
- condition 2

## Scope IN

- bounded action or decision this capability may support
- files, folders, or repo surfaces it may inspect or update
- expected human/agent workflow role

## Scope OUT

- runtime authority not explicitly admitted elsewhere
- promotion authority by documentation alone
- external service activation or dependency installation unless separately approved
- private/live trading, secrets handling, or deployment claims unless covered by a separate contract

## Source surfaces

- `path/or/url` ÔÇö why it matters

## Dependencies and external endpoints

- dependency or endpoint: purpose, auth mode, and whether it is required or optional
- none, if the capability is local/docs-only

## Secret and data boundary

- secrets required: yes/no; name placeholders only, never values
- allowed data: public repo data | local fixtures | redacted outputs | other
- forbidden data: secrets, live private account data, non-redacted logs, or other sensitive payloads

## Allowed tools or operations

- read-only search/inspection
- bounded file edits under named paths
- focused tests or lint commands
- other allowed operation

## Expected output

- concrete artifact, page, test result, checklist, or decision record

## Version and provenance

- version:
- derived from:
- compatibility note:
- review cadence:

## Known risks

- risk 1
- risk 2

## Mitigations and controls

- control 1
- control 2

## Limitations

- limitation 1
- limitation 2

## Scan / review / evidence state

- scan result: pass | fail | unknown
- review result: accepted-for-research | needs-work | blocked
- evidence marker:
- evidence pipeline record: `docs/research/templates/evidence-pipeline-template.md` or concrete page

## Validation evidence

- command or evidence surface: result
- not validated yet, if still research-only

## Promotion path

If this capability becomes load-bearing, promote the stable contract into the appropriate admitted
surface, such as `README.md`, `docs/SKELETON_SCOPE.md`, `seed_manifest.json`, focused tests, or
runtime/config authority files when explicitly in scope.

## Linked log entry

- `docs/research/log.md` ÔÇö `## [YYYY-MM-DD] kind | title`

## Current status

Short current-state summary and next step.
