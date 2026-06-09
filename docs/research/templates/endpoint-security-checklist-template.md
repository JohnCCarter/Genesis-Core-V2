# Endpoint security checklist title

> **Boundary note:** this checklist is for bounded endpoint, external-service, MCP, or agent-tool
> reviews. It documents safety posture and required evidence, but it does not authorize runtime,
> deployment, live trading, or promotion behavior by itself.

## Status

- status: proposed | active | closed | superseded
- opened: YYYY-MM-DD
- working branch: `<branch-name>`
- capability or endpoint: `<name>`
- lifecycle lane: research | validate

## Trust boundary

- local-only | hosted API | MCP | exchange endpoint | browser/tooling | other
- trusted surfaces:
- untrusted surfaces:
- human confirmation required: yes/no and why

## Endpoint trust confirmation

- endpoint owner:
- endpoint documentation:
- allowed hostnames:
- confirmed by:
- confirmation date:

## Intended use

What is this endpoint or capability allowed to support?

## Scope OUT

- runtime authority unless separately admitted
- promotion authority by checklist alone
- secrets in prompts, logs, docs, screenshots, or committed files
- live/private trading operations unless a separate validated slice explicitly admits them
- deployment, tunnel, proxy, or remote ops guidance unless explicitly in scope

## Endpoint inventory

| Endpoint or tool | Purpose | Auth mode | Required? | Notes |
| ---------------- | ------- | --------- | --------- | ----- |
| `<name>`         |         |           | yes/no    |       |

## Auth and secret handling

- secret names only:
- storage surface:
- rotation or revocation note:
- redaction expectation:

## No secrets in prompts

- prompt may include:
- prompt must not include: API keys, tokens, private account data, non-redacted logs, or secrets
- redaction check:

## Data classification

- allowed inputs:
- forbidden inputs:
- allowed outputs:
- retention expectation:

## Egress and endpoint controls

- deny-by-default assumption: yes/no
- allowed hostnames or paths:
- blocked hostnames or paths:
- method restrictions:
- timeout / rate-limit expectation:

## Path/method scoped external calls

| Host | Path scope | Methods | Purpose | Confirmation required? |
| ---- | ---------- | ------- | ------- | ---------------------- |
|      |            |         |         | yes/no                 |

## Prompt and tool boundary

- tool calls allowed:
- tool calls forbidden:
- prompt content restrictions:
- user confirmation triggers:

## Logging and observability

- logs allowed:
- logs forbidden:
- redaction checks:
- artifact storage boundary:

## Failure modes

- auth failure:
- timeout or cold start:
- malformed response:
- unsafe output:
- fallback behavior:

## Validation evidence

- command, test, review, or manual check: result
- not validated yet, if still research-only

## Promotion gates

Before this endpoint or capability becomes load-bearing, evidence must be promoted into admitted
authority or verification surfaces such as `README.md`, `docs/SKELETON_SCOPE.md`,
`seed_manifest.json`, focused tests, or runtime/config contracts when explicitly in scope.

## Linked log entry

- `docs/research/log.md` ÔÇö `## [YYYY-MM-DD] kind | title`

## Current status

Short current-state summary and next step.
