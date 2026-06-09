# Karpathy agent discipline

> **Boundary note:** this is a durable query-answer record.
> It captures one reusable explanation, but it does not act as runtime or promotion authority.

Date: 2026-06-04
Working branch: `feature/champion-results-review`
Knowledge product links: `../index.md` ┬À `../map.md` ┬À `../log.md`

## Question

What does Karpathy-style `llm-wiki` imply about agent discipline for V2?

## Why this answer should persist

This answer drove a structural product decision: V2 should encode agent discipline in files,
workflow, and durable markdown artifacts rather than leave it implicit in chat behavior.

## Consulted surfaces

- `../index.md`
- `../map.md`
- `../operations.md`
- `https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f`
- `https://gist.github.com/karpathy/fb64880bf1f99d58d6c759c966616922`

## Answer summary

Karpathy-style agent discipline is schema-driven. The agent should operate inside a clear
raw-sources ÔåÆ wiki ÔåÆ schema split, follow an ingest/query/lint loop, and file durable answers back
into the wiki instead of treating the chat transcript as the memory system.

## Durable takeaways

- discipline lives in the schema and workflow, not in improvised chat behavior alone
- `map.md` should be the first file an agent reads when answering against the wiki
- raw sources remain primary and should be cited directly
- durable answers belong in the wiki, not only in ephemeral conversation history
- linting the wiki is part of maintenance, not an afterthought

## Linked log entry

`docs/research/log.md` ÔåÆ `question | file back karpathy agent discipline answer`

## Current status

Closed ÔÇö the answer has been captured and translated into repo-native wiki structure.
