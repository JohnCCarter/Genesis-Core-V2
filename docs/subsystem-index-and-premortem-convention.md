# Subsystem Index + Premortem Convention

Last update: 2026-06-02
Status: active

## Purpose

This document defines two practical repository conventions for `Genesis-Core-V2`:

1. `index.md` files for major subsystem folders
2. deterministic premortem reflection rules for Validate -> Promote flows

The goal is to improve placement accuracy, reduce architectural drift, and make the repository
more navigable for both humans and AI agents.

This is a practical operating convention. It must not override higher-order governance or authority
documents such as `AGENTS.md`, `.github/copilot-instructions.md`, `docs/SKELETON_SCOPE.md`, or
`docs/governance_mode.md`.

## Why this exists

`Genesis-Core-V2` is intentionally narrower than `Genesis-Core` and is designed to preserve clear
boundaries between:

- Research
- Validate
- Premortem reflection
- Promote

When subsystem boundaries are unclear, work drifts into the wrong folder, authority surfaces widen
accidentally, and agents start inventing local structure. The `index.md` convention makes local
responsibility explicit. The premortem convention keeps risk reflection deterministic and fail-closed.

## Lifecycle framing

Every subsystem and every premortem surface should preserve this lifecycle order:

- Research creates hypotheses.
- Validate produces evidence.
- Premortem reflects on verified failure modes.
- Promote consumes validated evidence and explicit signoff.

Premortem is a **post-validation synthesis layer**.

Premortem does **not**:

- create new evidence
- replace validation
- authorize promotion on its own
- speculate freely

## `index.md` convention

Add `index.md` only to **major subsystem folders**, not every small folder.

Good candidates include folders that:

- own a clear domain responsibility
- are likely entrypoints for future work
- contain multiple modules with non-trivial boundaries
- benefit from explicit governance/authority framing

Do **not** add `index.md` to every tiny helper folder, transient staging folder, or low-signal leaf.

### Required sections

Each subsystem `index.md` should define:

- Purpose
- Scope IN
- Scope OUT
- Inputs
- Outputs
- Invariants
- Must Not
- Related tests
- Governance boundaries
- Lifecycle role / authority level

### Authoring rules

Each `index.md` should be:

- short enough to scan quickly
- specific to the local subsystem
- explicit about boundaries and non-goals
- framed using current repository reality, not hoped-for future shape

### What `index.md` must not become

An `index.md` must not become:

- a second README for the whole repository
- speculative architecture prose
- a dumping ground for migration dreams
- a shadow authority source that overrides tests or governance docs

## Premortem reflection convention

Premortem in V2 must be:

- deterministic
- evidence-based
- fail-closed
- bound to explicit evidence surfaces

Premortem claims may only be emitted when they can be tied to one or more of:

- metric completeness
- incumbent completeness
- threshold comparisons
- trade density
- run-intent
- lifecycle phase
- governance signoff / override
- deterministic evidence surfaces already present in the repository

### Good premortem reflection

- Candidate metrics are incomplete.
- Incumbent baseline is incomplete.
- Trade density is too thin.
- PF margin is fragile.
- Drawdown buffer is too small.
- Stability is weaker than incumbent.
- Governance signoff or override is missing.
- Run-intent does not match promotion phase.

### Bad premortem reflection

- Strategy feels risky.
- Market may change.
- Edge might disappear.
- AI believes promotion is unsafe without evidence.

### Hard rule

If a premortem claim cannot be tied to a metric, run-intent, threshold, signoff, or deterministic
evidence surface, it does not belong in V2 premortem.

## Structured-first rule

Premortem should be expressed as structured deterministic output first, with human-readable markdown
or narrative explanation only as a secondary rendering.

The structured source should remain the contract-bearing surface.

## Recommended rollout policy

Start with major subsystem folders only. Current V2 candidates include:

- `src/core/decision/`
- `src/core/config/`
- `src/core/strategy/`
- `src/core/api/`
- `src/core/io/bitfinex/`
- `src/core/optimizer/`

Expand further only when a folder proves large enough and boundary clarity materially improves.
