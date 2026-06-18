from __future__ import annotations

import argparse
import copy
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from core.backtest.engine import BacktestEngine
from core.decision.candidate_builder import build_candidate_packet, metric_snapshot_from_mapping
from core.optimizer.scoring import score_backtest

REPO_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_SEED_PATH = REPO_ROOT / "config" / "runtime.seed.json"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "results" / "evaluation" / "candidate_search"

# --- Research <-> authority boundary guard ---------------------------------------------
# A candidate SEARCH is research, not authority. It must never self-issue the promotion
# override/signoff that would let its output read as an approval. With both flags False,
# ready_for_promotion is structurally unforceable here (apply_promotion requires a real
# override + signoff), so a candidate-search artifact can only *propose*, never *approve*.
RESEARCH_PROMOTION_OVERRIDE = False
RESEARCH_PROMOTION_SIGNOFF = False
RESEARCH_AUTHORITY_STATUS = "research_only"


def research_authority_stamp() -> dict[str, Any]:
    """Non-authoritative marker stamped onto every candidate-search artifact.

    Makes the research<->authority boundary explicit in the output so a later reader (human
    or agent) cannot mistake candidate-search output for promotion / champion / signoff
    authority. Research proposes; it does not approve.
    """
    return {
        "status": RESEARCH_AUTHORITY_STATUS,
        "non_authoritative": True,
        "requires_human_signoff": True,
        "note": (
            "candidate_search is a research artifact: it may propose a candidate but cannot "
            "approve promotion. ready_for_promotion stays False here because a research search "
            "does not issue the promotion override/signoff that authority requires."
        ),
    }


def build_research_run_payload(
    *,
    run_at: str,
    symbol: str,
    timeframe: str,
    incumbent_payload: dict[str, Any],
    best_eval: dict[str, Any],
    evaluations: list[dict[str, Any]],
) -> dict[str, Any]:
    """Assemble the candidate-search artifact, stamped non-authoritative."""
    return {
        "authority": research_authority_stamp(),
        "run_at": run_at,
        "symbol": symbol,
        "timeframe": timeframe,
        "incumbent": {k: v for k, v in incumbent_payload.items() if not k.startswith("_")},
        "best_candidate": best_eval,
        "evaluations": evaluations,
    }


@dataclass(frozen=True)
class CandidateSpec:
    label: str
    entry_conf_overall: float
    exit_conf_threshold: float
    max_hold_bars: int


def _load_runtime_seed_cfg() -> dict[str, Any]:
    payload = json.loads(RUNTIME_SEED_PATH.read_text(encoding="utf-8"))
    cfg = payload.get("cfg")
    if not isinstance(cfg, dict):
        raise ValueError("config/runtime.seed.json must contain top-level 'cfg' object")
    return cfg


def _score_to_metric_payload(
    result: dict[str, Any], *, strategy_family: str = "ri"
) -> dict[str, Any]:
    scored = score_backtest(result, score_version="v2")
    metrics = dict(scored.get("metrics") or {})

    backtest_info = result.get("backtest_info") or {}
    start_raw = str(backtest_info.get("start_date") or "")
    end_raw = str(backtest_info.get("end_date") or "")
    start_ts = datetime.fromisoformat(start_raw.replace("Z", "+00:00"))
    end_ts = datetime.fromisoformat(end_raw.replace("Z", "+00:00"))
    days = max(1.0, (end_ts - start_ts).total_seconds() / 86400.0)
    years = max(1.0 / 365.0, days / 365.0)

    num_trades = float(metrics.get("num_trades", 0.0) or 0.0)
    trades_per_year = num_trades / years

    sharpe = float(metrics.get("sharpe_ratio", 0.0) or 0.0)
    # Stability proxy for decision-gates: clamp Sharpe-based signal to [0,1]
    stability = max(0.0, min(1.0, (sharpe + 1.0) / 2.0))

    return {
        "strategy_family": strategy_family,
        "profit_factor": float(metrics.get("profit_factor", 0.0) or 0.0),
        "max_drawdown": float(metrics.get("max_drawdown", 0.0) or 0.0),
        "trades_per_year": float(trades_per_year),
        "stability": float(stability),
        "winrate": float(metrics.get("win_rate", 0.0) or 0.0),
        "metadata": {
            "score_version": "v2",
            "sharpe_ratio": f"{sharpe:.6f}",
            "start": start_raw,
            "end": end_raw,
            "years": f"{years:.6f}",
        },
        "_scored": scored,
    }


def _run_backtest(
    symbol: str, timeframe: str, cfg: dict[str, Any], trace_writer=None
) -> dict[str, Any]:
    runtime_cfg = copy.deepcopy(cfg)
    runtime_cfg.setdefault("meta", {})
    runtime_cfg["meta"]["skip_champion_merge"] = True

    engine = BacktestEngine(symbol=symbol, timeframe=timeframe, warmup_bars=120, fast_window=False)
    if not engine.load_data():
        raise RuntimeError(f"Unable to load data for {symbol} {timeframe}")

    result = engine.run(
        policy={"symbol": symbol, "timeframe": timeframe},
        configs=runtime_cfg,
        verbose=False,
    )
    if result.get("error") is not None:
        raise RuntimeError(f"Backtest error for {symbol} {timeframe}: {result.get('error')}")

    if trace_writer is not None:
        from core.trace import record_backtest_run

        record_backtest_run(result, writer=trace_writer, symbol=symbol, timeframe=timeframe)

    return result


def _candidate_grid() -> list[CandidateSpec]:
    return [
        CandidateSpec("grid_a", 0.22, 0.38, 16),
        CandidateSpec("grid_b", 0.24, 0.40, 18),
        CandidateSpec("grid_c", 0.26, 0.42, 20),
        CandidateSpec("grid_d", 0.28, 0.44, 24),
        CandidateSpec("grid_e", 0.30, 0.46, 28),
    ]


def _extract_candidate_cfg(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    for key in ("merged_config", "cfg", "parameters"):
        candidate = payload.get(key)
        if isinstance(candidate, dict):
            return candidate
    raise ValueError(
        f"Candidate artifact {path} must contain one of: merged_config, cfg, parameters"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Find a new champion candidate from runtime-seed grid"
    )
    parser.add_argument("--symbol", default="tBTCUSD")
    parser.add_argument("--timeframe", default="1h")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument(
        "--candidate-config",
        help="Optional path to candidate artifact/config JSON (merged_config/cfg/parameters)",
    )
    parser.add_argument(
        "--trace",
        action="store_true",
        help="Emit an agent-readable run-trace under results/trace/ (opt-in, side-effect-free)",
    )
    args = parser.parse_args()

    output_dir = Path(args.output).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    trace_writer = None
    if args.trace:
        try:
            from core.trace import TraceWriter, new_run_id, resolve_actor_from_env

            trace_writer = TraceWriter(
                run_id=new_run_id(),
                actor=resolve_actor_from_env(),
                intent="candidate_search",
                symbol=args.symbol,
                timeframe=args.timeframe,
            )
        except Exception:  # fail-open: tracing must never block the search
            trace_writer = None

    seed_cfg = _load_runtime_seed_cfg()

    incumbent_result = _run_backtest(
        args.symbol, args.timeframe, seed_cfg, trace_writer=trace_writer
    )
    incumbent_payload = _score_to_metric_payload(incumbent_result)
    incumbent_snapshot = metric_snapshot_from_mapping(incumbent_payload)

    evaluations: list[dict[str, Any]] = []
    best_eval: dict[str, Any] | None = None

    for spec in _candidate_grid():
        candidate_cfg = copy.deepcopy(seed_cfg)
        candidate_cfg.setdefault("thresholds", {})
        candidate_cfg.setdefault("exit", {})
        candidate_cfg["thresholds"]["entry_conf_overall"] = spec.entry_conf_overall
        candidate_cfg["exit"]["exit_conf_threshold"] = spec.exit_conf_threshold
        candidate_cfg["exit"]["max_hold_bars"] = spec.max_hold_bars

        candidate_result = _run_backtest(
            args.symbol, args.timeframe, candidate_cfg, trace_writer=trace_writer
        )
        candidate_payload = _score_to_metric_payload(candidate_result)
        candidate_snapshot = metric_snapshot_from_mapping(candidate_payload)
        candidate_scored = candidate_payload.get("_scored") or {}

        packet = build_candidate_packet(
            incumbent_snapshot,
            candidate_snapshot,
            validate_run_intent="candidate",
            promotion_run_intent="promotion_compare",
            promotion_override_flag=RESEARCH_PROMOTION_OVERRIDE,
            promotion_signoff_flag=RESEARCH_PROMOTION_SIGNOFF,
        )

        if trace_writer is not None:
            from core.trace import record_candidate_build

            record_candidate_build(
                packet,
                incumbent=incumbent_snapshot,
                candidate=candidate_snapshot,
                writer=trace_writer,
            )

        eval_item = {
            "spec": {
                "label": spec.label,
                "entry_conf_overall": spec.entry_conf_overall,
                "exit_conf_threshold": spec.exit_conf_threshold,
                "max_hold_bars": spec.max_hold_bars,
            },
            "metrics": {k: v for k, v in candidate_payload.items() if not k.startswith("_")},
            "score": float(candidate_scored.get("score") or 0.0),
            "hard_failures": list(candidate_scored.get("hard_failures") or []),
            "candidate_packet": packet.to_dict(),
        }
        evaluations.append(eval_item)

        if best_eval is None:
            best_eval = eval_item
            continue

        if eval_item["score"] > best_eval["score"]:
            best_eval = eval_item

    if args.candidate_config:
        artifact_path = Path(args.candidate_config).resolve()
        artifact_cfg = _extract_candidate_cfg(artifact_path)
        candidate_cfg = copy.deepcopy(seed_cfg)
        # Candidate artifact values override seed baseline deterministically.
        for top_key, top_value in artifact_cfg.items():
            if isinstance(top_value, dict) and isinstance(candidate_cfg.get(top_key), dict):
                nested = dict(candidate_cfg[top_key])
                nested.update(top_value)
                candidate_cfg[top_key] = nested
            else:
                candidate_cfg[top_key] = top_value

        candidate_result = _run_backtest(
            args.symbol, args.timeframe, candidate_cfg, trace_writer=trace_writer
        )
        candidate_payload = _score_to_metric_payload(candidate_result)
        candidate_snapshot = metric_snapshot_from_mapping(candidate_payload)
        candidate_scored = candidate_payload.get("_scored") or {}
        packet = build_candidate_packet(
            incumbent_snapshot,
            candidate_snapshot,
            validate_run_intent="candidate",
            promotion_run_intent="promotion_compare",
            promotion_override_flag=RESEARCH_PROMOTION_OVERRIDE,
            promotion_signoff_flag=RESEARCH_PROMOTION_SIGNOFF,
        )

        if trace_writer is not None:
            from core.trace import record_candidate_build

            record_candidate_build(
                packet,
                incumbent=incumbent_snapshot,
                candidate=candidate_snapshot,
                writer=trace_writer,
            )

        eval_item = {
            "spec": {
                "label": "artifact_candidate",
                "artifact_path": str(artifact_path),
            },
            "metrics": {k: v for k, v in candidate_payload.items() if not k.startswith("_")},
            "score": float(candidate_scored.get("score") or 0.0),
            "hard_failures": list(candidate_scored.get("hard_failures") or []),
            "candidate_packet": packet.to_dict(),
        }
        evaluations.append(eval_item)
        if best_eval is None or eval_item["score"] > best_eval["score"]:
            best_eval = eval_item

    if best_eval is None:
        raise RuntimeError("No candidate evaluations were produced")

    if trace_writer is not None:
        try:
            ready = bool(best_eval["candidate_packet"]["ready_for_promotion"])
            status = "PASS" if ready else "WAIT"
            trace_writer.record_gate(
                stage="promotion_readiness",
                status=status,
                criteria_snapshot={
                    "best_spec": best_eval["spec"],
                    "ready_for_promotion": ready,
                    "authority_status": RESEARCH_AUTHORITY_STATUS,
                    "requires_human_signoff": True,
                },
                # Honest provenance: this gate is issued by the research search, not the
                # governance kernel. A candidate_search run must not self-attribute authority.
                issued_by="candidate-search",
            )
            trace_writer.close(outcome=status)
        except Exception:  # fail-open: tracing must never block the search
            pass

    now = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    run_payload = build_research_run_payload(
        run_at=now,
        symbol=args.symbol,
        timeframe=args.timeframe,
        incumbent_payload=incumbent_payload,
        best_eval=best_eval,
        evaluations=evaluations,
    )

    out_file = output_dir / f"candidate_search_{args.symbol}_{args.timeframe}_{now}.json"
    out_file.write_text(
        json.dumps(run_payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "authority_status": RESEARCH_AUTHORITY_STATUS,
                "best_score": best_eval["score"],
                "best_spec": best_eval["spec"],
                "output": str(out_file),
                "ready_for_promotion": best_eval["candidate_packet"]["ready_for_promotion"],
                "requires_human_signoff": True,
            },
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
