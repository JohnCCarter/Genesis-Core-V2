# Agent-/verktygs- & ekosysteminventering — Genesis-Core-V2

Last update: 2026-06-08
Status: evaluation / reference (non-authorizing)
Scope: agent-/AI-arbetsflöde (komplement till Issue #1 "Tooling & Ecosystem Review")
Grounding branch: `candidate-results-review` (@ `2b5e5e3`)

> Detta är ett **evaluerings-/referensdokument**. Det är subordinerat högre-ordningens
> governance-/authority-källor (`AGENTS.md`, `.github/copilot-instructions.md`,
> `docs/SKELETON_SCOPE.md`, `docs/governance_mode.md`). Det **auktoriserar inte** någon adoption,
> dependency-ändring, runtime-/promotion-/authority-ändring eller aktivering av deferred/dormant
> surfaces. Varje rekommendation som ska genomföras kräver en separat, scope-bunden slice.

> **Recovery note (2026-06-08):** Denna fil återställdes i `main` från den historiska PR #2-diffen
> under en bounded docs-recovery slice, tillsammans med den bredare repo-trackade research-wikin
> under `docs/research/**`.

---

## Syfte

Genesis-Core-V2 är en avsiktligt smal, RI-first, evidence-first, local-first **skeleton-repo** som
ska göra _research snabb, validering hård och promotion sällsynt_. Innan repot växer dokumenterar
denna inventering vilka externa agent-/ekosystem-patterns som är värda att skriva om **repo-native** —
utan att importera tredjeparts-skills/agent-regler rakt av, utan att vidga authority/runtime, och utan
att aktivera deferred surfaces.

> **Relation till Issue #1:** Repot har en öppen issue `#1 "Tooling & Ecosystem Review for Genesis V2"`
> (labels: enhancement/governance/tooling) som täcker _bibliotek/dependency_-vinkeln (uv, ruff, pydantic,
> pandera, DuckDB, gitleaks, …). Detta dokument är **komplementärt** och fokuserar på den vinkel Issue #1
> _inte_ täcker: **agent-/AI-arbetsflöde** (skills, subagents, orchestration, prompt/context engineering,
> MCP tool-use, evals för agentbeteende, observability/replay, research→validate→promotion-gates som
> agent-guardrails). Där de överlappar (CI/PR-automation, ADR, security, agentic guardrails) markeras det.

---

## 1. Repo-grounding summary (Observed)

**Identitet & doktrin (Observed — `AGENTS.md`, `.github/copilot-instructions.md`, `docs/SKELETON_SCOPE.md`):**

- Lifecycle: **Research → Validate → Promote**. "Research is cheap, Validation is expensive, Promotion is rare."
- **RI är enda aktiva strategy family** på runtime-, config-authority-, champion-default- och promotion-ytor.
  **Legacy = historisk/audit/replay-referens**, aldrig authority/default/fallback.
- Två spår: **Track A** (skeleton completeness — där vi är) och **Track B** (authority migration — deferred).
- **Default-defer:** allt som inte explicit admitted i seed behandlas som deferred.
- `Genesis-Core` (V1) = generator/seed-källa + historisk referens, överskrider inte admitted V2-authority.

**Admitted surfaces (Observed — README/SKELETON_SCOPE/seed_manifest):**

- Runtime kernel + `src/core/pipeline.py`; lokal-only API shell (`account/config/info/models/paper/public/status/strategy/ui`).
- Strategy authority helpers: `family_registry`, `family_admission`, `run_intent`, `authority_mode_resolver`.
- Config/runtime authority **verification-only**: `config/authority.py`, `config/schema.py`, `api/config.py`,
  repo-tracked `config/runtime.seed.json` (aktiv fallback); lokal `config/runtime.json` **exkluderad**.
- Verifierad champion-subset: `tBTCUSD_1h.json` (baseline-carried), `tBTCUSD_3h.json` (artifact-backed). Övriga champions deferred.
- Backtest compare/diff: `src/core/utils/diffing/results_diff.py`, `tools/compare_backtest_results.py`.
- Bitfinex REST read-spine (G1/G2) bunden via `core.server`; övrig `core.io.bitfinex.*` = **dormant package surface**.
- Dormant optimizer-paket (`core.optimizer.*`) + `config/optimizer/**` korpus = **import/test-completeness only**.
- Constrained remote MCP-semantik (`mcp_server/remote_server.py`) = **verification-only** (auth/safe-mode/confirm-token/transport-alias).
- Lokal MCP stdio shell (`mcp_server/*.py`, `scripts/mcp/mcp_stdio.py`, `.vscode/mcp.json`).

**Deferred/exkluderat (Observed):** live/private transport-rebinding, optimizer execution roots
(`scripts/run/run_backtest.py`, `scripts/optimize/**`, preflight/validate-CLIs), `config/runtime.json`,
candidate/test/backup champions, remote MCP launchers/deployment/tunnel/proxy, bred dokmigrering.

**Governance-/verifieringsmaskineri (Observed):**

- `docs/governance_mode.md` = SSOT: lägen **STRICT / RESEARCH / SANDBOX**, deterministisk A→B→C→D-resolution,
  fail-closed till STRICT, obligatorisk "Mode:"-banner, strict-only surfaces (champions, freeze-guard, family-/runtime-/comparison-ytor).
- CI (`.github/workflows/ci.yml`): pre-commit → `pytest -q` → `scripts/smoke/smoke_suite.py`, `permissions: contents: read`.
- `champion-freeze-guard.yml`: blockerar `config/strategy/champions/`-ändringar under freeze-fönster (2026-06-01→12-31), läser policy ur `seed_manifest.json`.
- `pull_request_template.md`: Governance Packet (Category/Mode/Risk/Path/Lifecycle/Scope IN-OUT) + PRE/POST-gates + Skill Usage + Evidence.
- Governance-tester: `test_v2_seed_boundaries.py`, `test_dead_code_tripwires.py`, `test_no_legacy_feature_imports.py`
  (AST-guard: ingen importerar `core.strategy.features`), `test_authority_mode_resolver.py`, `test_mcp_remote_authorization.py`,
  `test_pipeline_fast_hash_guard.py`, `test_pyproject_console_scripts.py`, `test_import_smoke_backtest_optuna.py`.
- `seed_manifest.json` = maskinläsbar inventering (admitted/copied/generated/blocked_imports/verification-surfaces).

**Candidate-branch-specifika nyheter (Observed — diff vs working branch):**

- **Deterministisk premortem-motor** `src/core/decision/premortem.py` (+`tests/test_premortem_system.py`): fail-closed,
  reason-codes PM-000…PM-007, severity-vägd risk_score, beslut PROCEED/MITIGATE/BLOCK, bunden till `MetricSnapshot`/run-intent/phase/signoff/override.
- **`index.md`-konvention** i subsystem-mappar (`decision/`, `config/`, `strategy/`, `api/`, `io/bitfinex/`, `optimizer/`):
  Purpose/Scope IN-OUT/Inputs/Outputs/Invariants/Must Not/Related tests/Governance boundaries/Lifecycle role.
- **`docs/subsystem-index-and-premortem-convention.md`** + **`docs/repository-layout-policy.md`** (zon-modell, parts/component/helper-regler, anti-patterns).
- `compare_backtest_results.py` har **RI P1 OFF-parity**-läge: deterministisk decision-row-jämförelse → maskinläsbart evidence-artifact (`parity_verdict`, mismatch-counts).

**Ekosystem-läge (Observed):** Inga öppna PRs. En öppen issue (#1). Branches på remote:
`main`, `candidate-results-review`, `feature/champion-results-review`, `copilot/cursorfib-context-review-overlay-64ac`.

---

## 2. Scan-fullständighet & evidensregler

- **Grundad på:** `candidate-results-review`-trädet via `git show` (495 filer i trädet; ~30 nyckelfiler lästa i sin helhet,
  hela `src/core`- och `tests`-trädet listat, alla governance-/doc-/CI-filer lästa).
- **Ofullständigt (markerat):** Inte varje modul i `src/core/**` är läst (t.ex. full `optimizer/runner*`, `intelligence/**`,
  `backtest/htf_*`), testerna är inte körda, hela `seed_manifest.json` (114 KB) är inte läst. Externa verktygs egenskaper
  bygger på allmän kunskap (cutoff jan-2026), **inte** på körd verifiering här → märkta **Inferred**.
- **Evidensregler i detta dokument:** Påståenden om repot = **Observed** (med filhänvisning). Slutsatser/extrapolation = **Inferred**.
  Sådant som kräver körning/beslut = **Unverified**. Sammanfattat i §10.

---

## 3. Kategori-för-kategori findings

> Format per kategori: **(1)** problem för V2 · **(2)** V2:s specifika behov · **(3)** etablerade verktyg/repos ·
> **(4)** patterns att kopiera · **(5)** importera ALDRIG rakt av · **(6)** repo-native form · **(7)** högst ROI först ·
> **(8)** risker · **(9)** verifieringskrav före adoption · **(10)** skjut upp.

### 3.1 Skills

1. Ad-hoc agent-arbete missar repots gates (Mode-banner, packet, lifecycle); kunskap bor i prompts, inte i repo.
2. Repo-native, körbara skills som kodar V2:s arbetsflöden: _governance-mode-resolve_, _candidate-results-review_, _premortem-run_, _seed-boundary-check_, _evidence-packet_.
3. Claude Code skills (`SKILL.md` + frontmatter), `.github/copilot-instructions.md` (finns), Cursor rules, Anthropic Agent Skills-format.
4. Progressive disclosure (kort frontmatter → detalj on-demand); skill = tunn orchestrator över _befintliga_ scripts (`scripts/smoke/*`, `tools/compare_backtest_results.py`).
5. Tredjeparts trading-/"alpha"-skills; generiska "do everything"-skills; skills som wrappar nätverk/secrets.
6. `.claude/skills/<name>/SKILL.md` som anropar repo-scripts read-only; varje skill deklarerar Mode/Lifecycle/Scope IN-OUT och pekar på verifieringskommando. Speglar `index.md`-konventionen.
7. **`candidate-results-review` skill** (störst ROI — det är grenens kärna): driver `compare_backtest_results.py` + `results_diff` + `premortem` → strukturerad review-output.
8. Skill blir "shadow authority" som kringgår tester/governance; drift mot prompt-only regler utan CI-bevis.
9. Skill får bara anropa redan-admitted scripts; en governance-test som verifierar att skills inte refererar deferred surfaces; körs i SANDBOX/RESEARCH först.
10. Auto-genererande/självmodifierande skills; skills som muterar config/champion.

### 3.2 Subagents

1. En monolitisk agent blandar snabb research med hård validering → riskerar promotion-drift.
2. Roll-separerade subagents speglande lifecycle: **Researcher** (lättvikt, read-mostly), **Validator** (hård, kör tester/smoke), **Reviewer/Promotion-gate** (read-only, premortem+diff).
3. Claude Code subagents (`.claude/agents/*.md` med `tools:`-allowlist), Explore/Plan-mönster, role-prompts.
4. Least-privilege per roll (Researcher saknar write till champions/runtime); reviewer = read-only; tydlig hand-off-artefakt mellan roller.
5. Subagents med bred `tools: *` på authority-ytor; subagent som både validerar och promotar (separation of duties bryts).
6. `.claude/agents/{researcher,validator,promotion-reviewer}.md`, var och en med Mode/Scope och verktygs-allowlist som matchar strict-only-listan i `governance_mode.md`.
7. **Promotion-reviewer subagent** (read-only) som kör premortem + results-diff och vägrar besluta utan evidence — direkt nytta på denna gren.
8. Roll-glidning (validator börjar "fixa"); kontext-läckage mellan roller; falsk trygghet.
9. Verktygs-allowlist testas; reviewer bevisat oförmögen att skriva champions/runtime; körs mot fixtures innan riktiga artefakter.
10. Auto-promoterande agent; multi-agent "swarm"-orchestration (för tidigt).

### 3.3 Agent orchestration

1. Flerstegs slices (research→validate→review) körs manuellt och oreproducerbart.
2. Deterministisk, evidence-bärande pipeline mellan stegen; varje steg lämnar en artefakt nästa konsumerar.
3. LangGraph, CrewAI, Claude Agent SDK, OpenAI Swarm — _som mönsterkälla_.
4. **State-machine = lifecycle** (Research→Validate→Promote är redan en graf); fail-closed transitions; artefakt-passing (jfr P1-parity-artifact).
5. Tunga ramverk (LangGraph/CrewAI) som runtime-dependency; nätverks-orchestration; dynamisk verktygs-syntes.
6. Lättviktig orchestrator i `tools/` eller skill som sekvenserar befintliga scripts och stoppar vid första BLOCK (premortem) — ingen ny tung dependency.
7. **Lifecycle-runner skill** som kedjar smoke → diff → premortem och kräver grön PRE-gate innan nästa steg.
8. Över-engineering; orchestrator blir ny authority-yta; icke-determinism.
9. Determinism-replay (samma input → samma beslut); pipeline-invariant-test (jfr `test_pipeline_fast_hash_guard.py`).
10. Distribuerad/parallell multi-agent execution; scheduling.

### 3.4 Prompt engineering

1. Agent-regler lever i flera filer (`AGENTS.md`, copilot-instructions, governance_mode) — risk för drift och motsägelser.
2. En tydlig auktoritetsordning + obligatorisk Mode-banner redan kodad; behåll _deterministisk_ tolkning.
3. Anthropic prompt-guider, "constitution"-mönster, few-shot reason-code-exempel.
4. **Hierarki "specifik vinner"** (redan dokumenterad), explicit fail-closed default, goda/dåliga exempel (premortem-doc har redan good/bad-listor → kopiera mönstret till fler ytor).
5. Generiska "best practice"-systemprompts; prompt-injection-känsliga mönster (instruktioner från extern data).
6. En kort, kanonisk `CLAUDE.md` på rot som _pekar_ (inte duplicerar) till SSOT-dokumenten + Mode-banner-regeln; håll varje doc DRY.
7. **Rot-`CLAUDE.md`** som länkar auktoritetsordningen (Issue #1 efterfrågar AI-instruktionsfiler) — låg risk, hög styrning.
8. Duplicering → divergens; promptregler som inte backas av CI (prompt säger en sak, test en annan).
9. Konsistenskontroll: prompt-regler får inte motsäga `governance_mode.md`; helst ett test som kollar att banner-formatet är intakt.
10. Avancerad meta-prompting/auto-optimering av prompts.

### 3.5 Context engineering

1. Agenter måste snabbt förstå "var hör detta hemma + vad får jag inte röra" utan att läsa hela repot.
2. Lokala, scannbara kontextkartor per subsystem; tydlig admitted-vs-deferred-signal.
3. `index.md`-konventionen (finns!), repository-layout-policy (finns!), context-map-mönster, "llms.txt".
4. **Behåll/utöka `index.md`-konventionen** (Purpose/Scope IN-OUT/Invariants/Must Not/Related tests) — detta är redan best-in-class context engineering, repo-native.
5. Auto-genererade "context dumps" som blir inaktuella; index.md som växer till andra-README/shadow authority (uttryckligen förbjudet i konventionen).
6. Rulla ut `index.md` till de återstående major-subsystemen som konventionen listar; håll dem korta; lägg ev. en `seed_manifest`-härledd "admitted/deferred"-rad överst.
7. **Slutför `index.md`-utrullning** till listade kandidatmappar (billigt, direkt agent-ROI).
8. Index.md-drift (inaktuella boundaries); överproduktion i små leaf-mappar (förbjudet).
9. Konventionens "must not"-regler hålls; ev. test som kollar att index.md har required sections i major-mappar.
10. Auto-generering av context från kod; embeddings/RAG-index över repot.

### 3.6 MCP / tool-use

1. Local-only MCP får inte vidgas till remote/live utan verifierad admission; tool-use måste vara safe-by-default.
2. Behåll stdio-first lokal MCP; remote MCP förblir verification-only (auth required, safe-mode, confirm-token).
3. Anthropic MCP-spec, FastMCP, MCP server-mönster (finns redan: `mcp_server/*`).
4. **Auth-required-by-default + confirm-token** (redan i `remote_server.py` + `test_mcp_remote_authorization.py`); safe/git transport-alias-konfig; least-privilege tools.
5. Operationella remote-launchers/tunnel/proxy (deferred); MCP-tools som muterar champions/runtime; unauth-by-default.
6. Håll MCP-tool-ytan = read/verification; varje ny tool deklareras i `seed_manifest` och täcks av en authorization-test.
7. **Ingen ny adoption nu** — högst ROI är att _dokumentera_ MCP-boundary i en `mcp/index.md` (verification-only) så agenter inte vidgar den.
8. Oavsiktlig widening av local-only→remote; prompt-injection via tool-output; secret-läckage.
9. `test_mcp_remote_authorization.py` grön; ingen ny route bunden i `core.server`; admission verifierad mot seed.
10. Remote deployment, tunnel/proxy, live transport — Track B.

### 3.7 Planning / persistent working memory

1. Slices spänner över sessioner; beslut/evidens tappas mellan körningar (remote ephemeral container).
2. Deterministisk, repo-tracked "memory" = artefakter (inte fri text): manifests, parity-artifacts, premortem-reports.
3. Claude Code plan-files, scratchpad/TODO-mönster, "agent memory" (mem0 m.fl. — _endast mönster_).
4. **Strukturerad evidens-artefakt som minne** (P1-parity-artifact + premortem `to_dict()` är redan maskinläsbara) — checka in i `results/` (en output-zon i layout-policy).
5. Fri-text long-term memory som blir hidden state/authority; externa memory-tjänster (nätverk/secret).
6. En `results/evaluation/`-konvention (artefakten skrivs redan dit av compare-toolet) + ev. enkel JSON "run-ledger"; ingen DB-dependency.
7. **Formalisera evidence-artefakt-konventionen** (var de bor, schema-version) — billigt, stärker reproducerbarhet.
8. Hidden state som påverkar beslut icke-deterministiskt; artefakt-drift.
9. Artefakt-schema deterministiskt & versionerat; regressions-/golden-test på artefakt-form.
10. Externa memory-stores, vektor-minne.

### 3.8 Runtime/config authority workflows

1. Runtime/config authority måste vara verification-only; oavsiktlig widening är hög risk.
2. Behåll `ConfigAuthority`-precedens (runtime.json > seed) men håll `runtime.json` exkluderad; RI som enda aktiva family.
3. (Repo-native; inga externa.) Mönster: config-precedence, schema-validation (pydantic/jsonschema från Issue #1).
4. **Deterministisk authority-mode-resolver + schema-validering** (finns); fail-closed; seed-fallback.
5. Externa config-managers som tar över authority; runtime-override i seed.
6. Inga ändringar; ev. `config/index.md` (finns) som låser boundaries; pydantic _endast_ som internt kontrakt om Issue #1 godkänner.
7. **Ingen ändring** — högst ROI = säkra att authority-ytor förblir verification-only via befintliga tester.
8. Widening utan scope; schema-drift; precedens-buggar.
9. `test_config_authority_semantics.py` + `test_stateful_authority_payloads.py` gröna; ingen ny authoritativ payload.
10. All authority-migration (Track B).

### 3.9 Strategy admission / family authority

1. Måste garantera RI-first och att Legacy aldrig blir authority/default/fallback.
2. Behåll `family_registry`/`family_admission`/`run_intent`; håll legacy-feature-import-guarden.
3. (Repo-native.) Mönster: capability/admission registries, AST import-guards, import-linter (Issue #1).
4. **AST-tripwire** `test_no_legacy_feature_imports.py` + **run_intent fail-closed** (`validate_run_intent_name`) — utmärkta admission-guards att replikera.
5. Tredjeparts strategi-bibliotek som "family"; legacy som fallback.
6. Inga ändringar; ev. **import-linter** (repo-native kontrakt) för att CI-blockera felaktiga lager-importer — men först efter Issue #1-godkännande.
7. **Ingen ändring nu**; dokumentera family-authority i `strategy/index.md` (finns).
8. Smyg-admission av legacy/tredjepart; family-drift.
9. Family-/admission-tester gröna; import-guard utan offenders.
10. Nya families/promotion-authority.

### 3.10 Candidate-results review tooling _(grenens kärna)_

1. Kandidat-vs-incumbent-jämförelser görs annars subjektivt/icke-reproducerbart → osäker promotion.
2. Deterministisk metric-diff + regression-detektion + decision-row-parity + fail-closed premortem, allt maskinläsbart.
3. `results_diff.py`, `tools/compare_backtest_results.py` (strict/report + RI P1 OFF-parity), `premortem.py` — **finns redan**.
4. **Strict non-regression-gate**, **deterministisk row-key-normalisering**, **parity-artifact**, **premortem reason-codes** — alla värda att standardisera som review-flöde.
5. Externa backtest-jämförare (vectorbt/quantstats) som _source of truth_ (Issue #1 säger uttryckligen sandbox/reference-only).
6. **`candidate-results-review` skill/subagent** (§3.1/3.2) som kedjar diff → parity → premortem → strukturerad review-rapport + ev. PR-kommentar.
7. **HÖGST ROI ÖVERLAG:** wrappa befintliga verktyg i ett review-flöde (skill) — ingen ny kärnkod, direkt nytta för grenens syfte.
8. Falsk precision om metrics saknas (premortem fail-closar — bra); review blir "rubber stamp"; extern jämförare smyger in som authority.
9. `test_compare_backtest_results.py`, `test_results_diff.py`, `test_premortem_system.py` gröna; review producerar evidence-artefakt; körs på fixtures.
10. Integration mot live results-corpora (deferred); auto-promotion på grön review.

### 3.11 Evals / regression testing för agentbeteende

1. Agent-output (reviews, premortem, mode-resolution) kan drifta tyst.
2. Golden/snapshot-tester på _deterministiska_ agent-artefakter; reason-code-stabilitet.
3. pytest-regressions/approvaltests/syrupy, Hypothesis (Issue #1), Anthropic eval-mönster.
4. **Determinism-replay** (samma input→samma report), **reason-code-kontrakt** (PM-000…), **golden-master** på artefakt-JSON.
5. LLM-as-judge-evals som blir authority; icke-deterministiska evals i gates.
6. pytest golden-tester över premortem/diff/parity-artefakter (de är redan `to_dict()`/JSON); ev. Hypothesis på validators/run-intent.
7. **Golden-tester på review-/premortem-artefakter** — billigt, fångar drift, passar deterministisk doktrin.
8. Brittle snapshots; flakiga evals; eval som mäter fel sak.
9. Snapshots stabila över körningar; deterministisk seed; inga nätverksberoenden i eval.
10. LLM-judge-baserade beteende-evals (gated later).

### 3.12 Observability / tracing / replay

1. Svårt att granska _varför_ en agent/beslutsmotor gav ett utfall i efterhand.
2. Strukturerad, maskinläsbar, deterministisk logg/trace + replay från artefakt.
3. structlog/OpenTelemetry (Issue #1 — soon/later), `core/observability/metrics.py` (finns).
4. **Strukturerade reason-codes + evidence-artefakter = inbyggd replay** (premortem/parity är redan deterministiskt återskapbara).
5. Tung tracing-stack (OTel/Prometheus) som runtime-dependency nu; loggning av secrets (jfr `logging_redaction.py`).
6. structlog _om_ Issue #1 godkänner; annars stdlib + redaction; replay = återkör verktyg på sparad input-artefakt.
7. **Replay via artefakter** (redan möjligt) — dokumentera mönstret; structlog = "soon".
8. Secret-läckage i loggar; trace-overhead; icke-determinism i loggning.
9. `logging_redaction`-täckning; replay reproducerar identiskt beslut; ingen secret i artefakt.
10. OTel/Prometheus/distributed tracing (service-fas).

### 3.13 Research → Validate → Promotion gates

1. Utan hårda gates riskerar lovande-men-osäkra kandidater promotion.
2. Fail-closed gates: research lätt, validate hård, promotion kräver evidence+signoff+override+rätt run-intent.
3. `premortem.py` (PM-006 governance, PM-007 run-intent/phase), `governance_mode.md`, freeze-guard — **finns**.
4. **Premortem-decision (BLOCK på CRITICAL)**, **freeze-guard CI**, **run-intent↔phase-matchning**, **PR Governance Packet** — komplett gate-mönster värt att hålla intakt.
5. Externa "approval bots" som beslutar utan evidence; auto-merge på champions.
6. Inga ändringar; ev. binda premortem-output i CI som icke-blockande rapport först, blockande efter verifiering.
7. **Wire premortem som CI-rapport** (report-mode) på review-PRs — synliggör gate utan att ändra authority.
8. Gate-bypass; falsk PASS; gate blir byråkrati utan proportion (governance_mode varnar för detta).
9. Premortem BLOCK:ar korrekt på saknad evidens (testat); freeze-guard aktiv; proportionalitet per Mode.
10. Auto-promotion; promotion-authority till agenter.

### 3.14 Security (skills, tools, MCP, prompt injection, repo-miljö)

1. Agent-miljö + MCP + extern data (PR-kommentarer, CI-loggar) = prompt-injection- och secret-exfiltrerings-yta.
2. Least-privilege tools, auth-required MCP, secret-scanning, redaction, fail-closed.
3. gitleaks/pip-audit/bandit (Issue #1), `logging_redaction.py`, `crypto.py`, `nonce_manager.py`, `.env.example` (finns).
4. **Auth-required-by-default MCP**, **CI `permissions: contents: read`**, **redaction-helper**, **freeze-guard** — solid security-baslinje.
5. Verktyg som exekverar instruktioner från extern data; MCP unauth; secrets i repo/loggar; auto-fix på injicerade kommandon.
6. Behandla all extern data (PR/issue/CI-text) som untrusted; secret-scan i pre-commit+CI (Issue #1); skills/tools får ej röra secrets.
7. **gitleaks i pre-commit+CI** (om Issue #1 godkänner) — hög security-ROI, låg risk.
8. Prompt-injection → scope-drift/exfiltrering; supply-chain via nya deps; falskt negativ secret-scan.
9. Auth-tester gröna; redaction täcker secret-fält; ingen ny dep utan pip-audit/scoped issue.
10. SLSA/provenance, tung supply-chain (Issue #1: later).

### 3.15 GitHub / CI / PR-review automation

1. Manuell review skalar dåligt och missar governance-konsistens.
2. CI som speglar lokala gates; PR-packet enforced; ev. automatiserad review-kommentar bunden till evidence.
3. CI (finns), PR-template (finns), CODEOWNERS/issue-templates/reusable workflows (Issue #1), GitHub MCP.
4. **CI = lokala gates** (pre-commit→pytest→smoke), **freeze-guard**, **Governance Packet PR-template** — kopierings-värda mönster (redan på plats).
5. Auto-merge på champions/strict-only; review-bot som godkänner utan evidence; bred CI-permission.
6. Lägg ev. **issue-templates** (Research/Validate/Promotion/Tooling) speglande PR-packet; CODEOWNERS på strict-only paths; review-skill postar _findings_, beslutar inte.
7. **Issue-templates + CODEOWNERS på strict-only surfaces** — billig governance-hävstång (Issue #1 efterfrågar).
8. Över-automation; bot beslutar; CI-flakiness blockerar legitim research.
9. CI grön & deterministisk; CODEOWNERS täcker champions/freeze-guard/family/runtime; templates obligatoriska fält.
10. Auto-merge, auto-promotion-bots.

### 3.16 Documentation / context maps / ADR / glossary workflows

1. Arkitektur-/scope-beslut riskerar tappas → drift och åter-debatt.
2. Lättviktig ADR-traceability + glossary för V2-termer (admitted/deferred/dormant/run-intent/family/champion).
3. ADR-templates/adr-tools, mkdocs (Issue #1: later), `index.md`/layout-policy (finns).
4. **`index.md` + layout-policy som levande konvention**; ADR-mönster (kort, numrerat, immutabelt beslut).
5. Tung docs-site nu; ADR som blir governance-SSOT (layout-policy förbjuder att blanda governance i layout-docs).
6. `docs/adr/NNNN-*.md` lättviktsmall + en `docs/glossary.md`; håll subordinerat till governance-SSOT (auktoritetsordning finns).
7. **Lightweight ADR-mall + glossary** — billigt, fångar beslutshistorik (Issue #1: Adopt Now).
8. ADR-drift/övergivande; glossary divergerar från kod; docs-site-overhead.
9. ADR refererar evidens/PR; glossary-termer matchar kod (run_intent-värden etc.).
10. mkdocs-material/docs-site (Issue #1: later).

### 3.17 Test/smoke/validation automation

1. Slices måste bevisas gröna deterministiskt före commit/merge.
2. Snabb, körbar, fixture-backad smoke + full pytest + determinism/parity, lokalt = CI.
3. pytest (finns), nox (Issue #1: soon), `scripts/smoke/*`, `scripts/validate/pytest_suite.py`, bootstrap-smoke (finns).
4. **Fixture-backad smoke-suite**, **lokal=CI-paritet**, **console-script-verifiering**, **determinism-/hash-guards** — exemplariskt; behåll.
5. Smoke som rör nätverk/live; icke-deterministiska tester i gate.
6. Inga ändringar; ev. **nox**-sessions (lint/test/smoke/validate) som EN ingång lokalt+CI (Issue #1) efter godkännande.
7. **Ingen ändring nödvändig**; nox = "soon" som reproducerbarhets-hävstång.
8. Flakighet; smoke-täckning luckor; CI-lokal-divergens.
9. `pytest -q` + `smoke_suite.py` gröna; console-script-test grön; deterministisk seed.
10. Tung orchestration av tester (Prefect/Dagster).

### 3.18 Results comparison / diff tooling

1. Resultat-jämförelser måste vara apples-to-apples och regressions-säkra.
2. Comparability-check + metric-delta + regression-flagga + row-parity, tmp-isolerat, utan execution-roots.
3. `results_diff.py` (`check_backtest_comparability`, `diff_metrics`, regression-thresholds), `compare_backtest_results.py` — **finns**.
4. **Comparability-guard före diff**, **regression-thresholds**, **None-säker float-coercion**, **canonical JSON row-key** — robusta mönster.
5. Externa diff-/analytics-bibliotek som authority; jämförelse mot icke-comparable runs.
6. Inga ändringar; ev. exponera diff via review-skill (§3.10); håll tmp-isolering.
7. **Återanvänd i review-skill** (täcks av §3.10) — ingen ny kärnkod.
8. Icke-comparable jämförelser ger falska slutsatser; metric-namn-drift.
9. `test_results_diff.py` grön; comparability-check körs först; tmp-path-isolerat.
10. Integration mot stora results-corpora (deferred).

---

## 4. Verktyg/patterns att kopiera **som idé** (repo-native, ej rakt av)

1. **Skill/subagent-pattern** (Claude Code/Anthropic Agent Skills): progressive disclosure, tools-allowlist → skriv om som `.claude/skills` + `.claude/agents` som _bara_ wrappar admitted scripts.
2. **import-linter** (lager-boundary-kontrakt) → repo-native CI-regel som speglar strict-only-lager.
3. **ADR-mall + glossary** → lättvikts `docs/adr/` + `docs/glossary.md`, subordinerat governance-SSOT.
4. **Issue-templates + CODEOWNERS** → spegla befintlig PR Governance Packet; routa strict-only paths.
5. **gitleaks/pip-audit** (security) → pre-commit+CI, fail-closed (via Issue #1).
6. **nox** → en ingång för lint/test/smoke/validate, lokalt=CI (via Issue #1).
7. **Golden/snapshot-evals (pytest-regressions/syrupy)** → deterministiska agent-/premortem-artefakt-tester.
8. **Hypothesis** → property-tester på validators/run-intent/diff (via Issue #1).
9. **structlog** → strukturerad audit-logg med redaction (via Issue #1, "soon").

## 5. Verktyg/patterns att **undvika** (eller hårt gata)

- **Tunga orchestration-ramverk** (LangGraph/CrewAI/Prefect/Dagster) som runtime-dependency — för tidigt; lifecycle är redan en graf.
- **Externa backtest-motorer som source of truth** (vectorbt/backtesting.py/bt) — endast sandbox/reference (Issue #1).
- **Optuna-driven tuning** utöver redan dormant paket — överfittnings-/drift-risk (Issue #1: gated later); aktivera inte execution-roots.
- **LLM-as-judge i blockande gates** — bryter determinism/fail-closed-doktrin.
- **Externa memory-/RAG-tjänster** — hidden state + nätverk/secret-yta.
- **Tredjeparts-skills/agent-regler rakt av** — uttryckligen förbjudet; extrahera mönster, skriv repo-native.
- **Tung docs-site / MLflow / DVC / lakeFS / OTel / Prometheus nu** — skala-beroende (Issue #1: later).

## 6. Rekommenderad Genesis V2-native struktur (förslag — ej byggt)

```
CLAUDE.md                      # tunn: auktoritetsordning + Mode-banner-regel, länkar SSOT (dupblicerar ej)
.claude/
  skills/
    governance-mode/SKILL.md         # resolverar/visar Mode (A→B→C→D), read-only
    candidate-results-review/SKILL.md# diff → parity → premortem → review-artefakt (kärnan)
    premortem-run/SKILL.md           # kör premortem på MetricSnapshot-par
    seed-boundary-check/SKILL.md     # verifierar admitted/deferred mot seed_manifest
  agents/
    researcher.md             # lättvikt, read-mostly, ingen write på strict-only
    validator.md              # kör pytest/smoke/determinism, ingen promotion
    promotion-reviewer.md     # read-only, premortem+diff, beslutar ej promotion
docs/
  adr/0001-record-architecture-decisions.md   # lättvikts-ADR-mall
  glossary.md                                  # admitted/deferred/dormant/run-intent/family/champion
src/core/<subsystem>/index.md  # slutför utrullning till listade major-mappar
```

Varje skill/agent/index.md deklarerar **Mode · Lifecycle · Scope IN/OUT · Verifieringskommando**, speglar
`governance_mode.md` strict-only-listan, och anropar **endast admitted** scripts read-only.

## 7. Prioriterad implementation roadmap (om approvad — separata scoped slices)

> Varje rad = egen scope-bunden slice med PRE/POST-gates. Inget byggs utan explicit order per slice.

**Fas 0 — Noll-risk dokument/kontext (RESEARCH):**

1. Slutför **`index.md`-utrullning** till konventionens kandidatmappar. _(billigast, agent-ROI)_
2. **Rot-`CLAUDE.md`** som länkar auktoritetsordning + Mode-banner. _(prompt-konsolidering)_
3. **ADR-mall + `glossary.md`**. _(beslutshistorik)_

**Fas 1 — Review-flödet (grenens syfte) (RESEARCH→VALIDATE):** 4. **`candidate-results-review` skill** som wrappar `compare_backtest_results.py`+`results_diff`+`premortem` → review-artefakt. _(HÖGST ROI)_ 5. **`promotion-reviewer` subagent** (read-only) + tools-allowlist-test. 6. **Golden-tester** på premortem/diff/parity-artefakter.

**Fas 2 — Governance/CI-hävstänger (kräver Issue #1-godkännande för deps):** 7. **Issue-templates + CODEOWNERS** på strict-only paths. 8. **gitleaks** i pre-commit+CI; **nox**-sessions (lokalt=CI). 9. **Premortem som icke-blockande CI-rapport** på review-PRs → blockande efter verifiering.

**Senare/gated:** import-linter, Hypothesis, structlog, pip-audit (per Issue #1-kategorier).

## 8. Riskregister

| #   | Risk                                                                  | Sannolikhet | Påverkan | Mitigering                                                                                     |
| --- | --------------------------------------------------------------------- | ----------- | -------- | ---------------------------------------------------------------------------------------------- |
| R1  | Skill/subagent blir "shadow authority" som kringgår tester/governance | Med         | Hög      | Skills anropar endast admitted scripts read-only; governance-test mot deferred refs            |
| R2  | Oavsiktlig widening av local-only API/MCP→remote/live                 | Låg         | Kritisk  | Behåll auth-required + verification-only; ingen ny route i `core.server`; seed-admission krävs |
| R3  | Aktivering av dormant optimizer/transport utan beslut                 | Låg         | Kritisk  | Håll import/test-only; ingen execution-root; freeze/scope-regler                               |
| R4  | Prompt-injection via extern data (PR/CI/issue) → scope-drift          | Med         | Hög      | Behandla extern data untrusted; least-privilege tools; bekräfta vid tvetydighet                |
| R5  | Ny dependency → supply-chain/maintenance-skuld                        | Med         | Med      | All adoption via separat Issue #1-slice; pip-audit; minsta admissibla                          |
| R6  | Doc/index-drift (inaktuella boundaries)                               | Med         | Med      | Required sections-test; håll DRY/länka SSOT                                                    |
| R7  | Extern backtest-jämförare smyger in som authority                     | Låg         | Hög      | Sandbox/reference-only; review-artefakt = enda evidens                                         |
| R8  | Gate-byråkrati bryter proportionalitet (research blir långsam)        | Med         | Med      | Respektera Mode-proportionalitet (governance_mode.md)                                          |
| R9  | Icke-determinism i evals/LLM-judge                                    | Med         | Hög      | Endast deterministiska gates; LLM-judge gated/icke-blockande                                   |
| R10 | Scan-ofullständighet → felaktig rekommendation                        | Med         | Med      | §10 separerar Observed/Inferred/Unverified; verifiera före adoption                            |

## 9. Verification checklist (före varje adoption/slice)

- [ ] Slicen har explicit **Scope IN/OUT** + **Mode** + **Lifecycle stage** (PR Governance Packet).
- [ ] **Ingen** runtime-/promotion-/authority-ändring utan explicit scope.
- [ ] **Ingen** widening av local-only API/MCP utan verifierad admission i `seed_manifest.json`.
- [ ] **Ingen** aktivering av dormant/deferred paket.
- [ ] `pre-commit run --all-files`, `pytest -q`, `scripts/smoke/smoke_suite.py` **gröna**.
- [ ] Relevanta governance-tester gröna (`test_v2_seed_boundaries`, `test_no_legacy_feature_imports`, `test_authority_mode_resolver`, `test_mcp_remote_authorization`, `test_premortem_system`).
- [ ] Determinism-replay + pipeline-invariant där runtime/comparison berörs.
- [ ] Skills/agents/index.md rör **endast admitted surfaces** read-only.
- [ ] Ny dependency: separat scoped issue + pip-audit + minsta admissibla version.
- [ ] Evidence-artefakt producerad och versionerad.
- [ ] RI-first respekterat; Legacy ej authority/default/fallback.

## 10. Observed / Inferred / Unverified

**Observed (lästa filer på `candidate-results-review`):**

- Doktrin/governance: `AGENTS.md`, `.github/copilot-instructions.md`, `docs/SKELETON_SCOPE.md`, `docs/governance_mode.md`, `docs/repository-layout-policy.md`, `docs/subsystem-index-and-premortem-convention.md`, `README.md`.
- Kod/tooling: `src/core/decision/premortem.py`, `decision/index.md`, `tools/compare_backtest_results.py`, `src/core/utils/diffing/results_diff.py`, `src/core/strategy/run_intent.py`.
- CI/PR: `.github/workflows/ci.yml`, `champion-freeze-guard.yml`, `.github/pull_request_template.md`.
- Tester (delvis): `test_v2_seed_boundaries.py`, `test_dead_code_tripwires.py`, `test_no_legacy_feature_imports.py`, `test_mcp_remote_authorization.py`.
- Struktur: hela `src/core`- och `tests`-trädet listat; `mcp_server/`, `scripts/`, `tools/`, `docs/` listade; `seed_manifest.json` (head).
- Ekosystem: 0 öppna PRs; Issue #1 "Tooling & Ecosystem Review" (full text läst).

**Inferred (rimlig slutsats, ej körd verifiering här):**

- Externa verktygs egenskaper/ROI (uv, ruff, nox, gitleaks, import-linter, Hypothesis, structlog, pytest-regressions, vectorbt m.fl.) bygger på allmän kunskap (cutoff jan-2026).
- Att skills/subagents kan wrappa befintliga scripts utan authority-widening (kräver implementation+test för bevis).
- Att premortem/diff/parity-artefakter går att golden-testa deterministiskt (formen är JSON/`to_dict()`, men ej testat här).

**Unverified (kräver körning/beslut):**

- Att `pytest -q`/smoke faktiskt är grönt på `candidate-results-review` _nu_ (ej kört).
- Exakt innehåll i icke-lästa moduler (`optimizer/runner*`, `intelligence/**`, `backtest/htf_*`, full `seed_manifest.json`).
- Vilka externa deps Issue #1 slutligen godkänner (öppen, ej beslutad).

---

### Scan-status: **delvis fullständig** — grundad på branchens nyckel-/governance-filer och fullständig trädlistning; enskilda implementationsmoduler och testkörning är ej uttömda (se §2 och §10).
