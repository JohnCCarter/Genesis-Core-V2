# Research wiki operations

> **Boundary note:** this page defines the working loop for the V2 research wiki.
> It governs how humans and agents ingest, query, and lint `docs/research/**`, but it does not act
> as runtime or promotion authority.

## Purpose

Turn the Karpathy-style LLM-wiki pattern into an explicit local workflow for `Genesis-Core-V2`.
This page defines how new knowledge enters the wiki, how answers get filed back, and how the wiki
is kept healthy as it grows.

## Agent discipline

When working against `docs/research/**`:

- read `map.md` first
- read raw source surfaces directly before summarizing them
- treat raw sources as immutable from the perspective of wiki maintenance
- file durable answers back into the wiki instead of leaving them stranded in chat history
- promote load-bearing conclusions into admitted authority or verification surfaces separately

## Ingest

Use ingest when a new source, seam, or bounded question needs to enter the wiki.

Typical loop:

1. Identify the raw source surface.
2. Read the raw source directly.
3. Create or update a bounded topic page.
4. Link the relevant source surfaces explicitly.
5. Update `map.md` if a new durable page or state change was introduced.
6. Append a dated entry to `log.md`.

Good outputs:

- a new topic page
- a tightened existing topic page
- a new source-family note in `sources/index.md`

## Query

Use query when a human or agent asks a bounded question and the answer should survive beyond the
current session.

Typical loop:

1. Read `map.md` first.
2. Open the relevant topic pages, query pages, and raw source surfaces.
3. Answer with explicit source paths or links.
4. If the answer has future reuse value, file it back into `queries/**`.
5. If the answer changes durable topic understanding, update the relevant topic page too.
6. Append a dated entry to `log.md` when the wiki itself changed.

Good outputs:

- a filed-back query answer
- a clarified topic page
- a promoted conclusion in a stronger authority surface when required

## Lint

Use lint when the question is not about a business seam, but about the health of the wiki itself.

Typical loop:

1. Choose the scope: one page, one surface family, or the full wiki.
2. Run `scripts/audit/research_wiki_lint.py` for structural checks (required paths/markers) and
   referential integrity (unregistered dated pages, dangling registry references). Referential
   findings are warn-only and do not gate the structural `ok`.
3. Look for contradictions, stale claims, orphan pages, missing links, and unclear ownership. This
   stays agent judgment — the script does referential integrity, not semantic consistency.
4. Record substantive passes or findings in `lint/**`.
5. Append a dated `lint` entry to `log.md` if the pass matters to future sessions.

Good outputs:

- a recorded lint pass
- a fixed stale or contradictory page
- a clearer registry, template, or page state

## When to write to the wiki

Write to the wiki when the result is:

- likely to matter in a later session
- tied to specific source surfaces
- bounded enough to stay understandable
- derivative rather than authority-bearing

Do not write to the wiki when the result is only transient terminal noise or when the conclusion
must land directly in an authority-bearing file instead.

## Must not

- mutate source-of-truth payloads by documentation alone
- let chat transcripts become the primary memory system
- treat filed query answers as authority by themselves
- skip source links when making a durable claim
