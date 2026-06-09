# Raw source layer

> **Boundary note:** this page describes the raw-source layer for `docs/research/**`.
> Raw sources are read, cited, and linked; they are not rewritten as part of routine wiki
> maintenance.

## Purpose

Make the source-of-truth layer explicit so humans and agents know what the research wiki is allowed
to summarize, connect, and depend on.

## Current source families

Current raw source families include:

- repo contract surfaces such as `README.md`, `AGENTS.md`, and `docs/SKELETON_SCOPE.md`
- machine-readable repo contracts such as `seed_manifest.json`
- code and tests under `src/**` and `tests/**`
- tracked configs and evidence payloads under `config/**`
- diagnostics and evidence artifacts already present in the repository
- explicitly linked external references when a bounded research page needs them

## Raw-source rule

- read raw sources directly before summarizing them
- prefer links and file paths over copied payloads
- keep source citations explicit in topic and query pages
- do not silently replace a source surface with wiki prose
- if a conclusion becomes load-bearing, promote it into the admitted authority or verification file

## Current source emphasis

For the current research product, the most common raw-source seams are:

- repo contracts and scope docs
- runtime loader and authority behavior
- governance tests
- tracked evidence payloads and diagnostics

## External references

External sources are allowed when they are clearly linked, bounded, and treated as derivative input.
They do not become V2 authority merely by being cited here.

## Next use

When a new source family becomes important for repeated research work, record it here and keep the
rule simple: raw sources stay primary; the wiki stays derivative.
