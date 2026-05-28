# Copilot Instructions — Genesis-Core-V2

This repository is a skeleton-first, local-only V2 seed.
Read `AGENTS.md` and `docs/SKELETON_SCOPE.md` before widening scope.

## Default behavior

- Prefer the smallest admissible slice.
- Prioritize V2 skeleton completeness before content migration.
- Keep `Genesis-Core` as the source of truth for authority-bearing behavior until a slice is admitted.
- Prefer generator-driven changes in `Genesis-Core` over manual drift in this repo.
- Keep the local-only API shell runnable and tested.
- Keep the local MCP stdio shell local-first and safe by default.
- Prefer fixture-backed smoke tests before moving wider runtime content.

## Out of scope by default

- exchange, paper, UI, and private runtime edges
- remote MCP server and remote MCP config surfaces
- runtime state and champion authority payloads
- freeze-sensitive and governance-sensitive authority surfaces
- unverified content migration for its own sake
