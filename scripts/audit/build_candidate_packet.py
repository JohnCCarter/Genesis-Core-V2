"""Build deterministic candidate packet for V2 champion evaluation.

This script composes comparison, premortem, and promotion checks into a
single JSON packet from incumbent/candidate metric payloads.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from core.decision.candidate_builder import (
    build_candidate_packet,
    metric_snapshot_from_mapping,
)


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _extract_metric_source(payload: dict[str, Any]) -> dict[str, Any]:
    if all(
        key in payload for key in ("profit_factor", "max_drawdown", "trades_per_year", "stability")
    ):
        return payload
    metrics = payload.get("metrics")
    if isinstance(metrics, dict):
        source = dict(metrics)
        if "strategy_family" not in source and "strategy_family" in payload:
            source["strategy_family"] = payload["strategy_family"]
        if "metadata" not in source and "metadata" in payload:
            source["metadata"] = payload["metadata"]
        return source
    raise ValueError("Payload must contain metrics either at top-level or under 'metrics'.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build V2 candidate decision packet")
    parser.add_argument("--incumbent", required=True, help="Path to incumbent metrics JSON")
    parser.add_argument("--candidate", required=True, help="Path to candidate metrics JSON")
    parser.add_argument("--output", help="Optional output path for packet JSON")
    parser.add_argument(
        "--validate-run-intent",
        default="candidate",
        help="Run intent for validate-phase premortem (default: candidate)",
    )
    parser.add_argument(
        "--promotion-run-intent",
        default="promotion_compare",
        help="Run intent for promote-phase premortem (default: promotion_compare)",
    )
    parser.add_argument(
        "--promotion-override",
        action="store_true",
        help="Set promotion override flag",
    )
    parser.add_argument(
        "--promotion-signoff",
        action="store_true",
        help="Set promotion signoff flag",
    )
    parser.add_argument(
        "--promotion-margin",
        type=float,
        default=0.05,
        help="PF promotion margin (default: 0.05)",
    )
    parser.add_argument(
        "--minimum-trade-threshold",
        type=float,
        default=51.0,
        help="Minimum trades/year threshold (default: 51.0)",
    )
    parser.add_argument(
        "--fail-if-not-ready",
        action="store_true",
        help="Exit with code 2 when ready_for_promotion=false",
    )

    args = parser.parse_args()

    incumbent_payload = _load_json(Path(args.incumbent).resolve())
    candidate_payload = _load_json(Path(args.candidate).resolve())

    incumbent_metrics = metric_snapshot_from_mapping(_extract_metric_source(incumbent_payload))
    candidate_metrics = metric_snapshot_from_mapping(_extract_metric_source(candidate_payload))

    packet = build_candidate_packet(
        incumbent_metrics,
        candidate_metrics,
        validate_run_intent=args.validate_run_intent,
        promotion_run_intent=args.promotion_run_intent,
        promotion_override_flag=bool(args.promotion_override),
        promotion_signoff_flag=bool(args.promotion_signoff),
        promotion_margin=float(args.promotion_margin),
        minimum_trade_threshold=float(args.minimum_trade_threshold),
    )

    payload = packet.to_dict()
    print(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True))

    if args.output:
        output_path = Path(args.output).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    if args.fail_if_not_ready and not packet.ready_for_promotion:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
