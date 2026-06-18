"""Research<->authority boundary guard for the candidate-search artifact.

`scripts/audit/find_new_champion_candidate.py` is legitimate research infra: it searches a
grid for a better champion candidate and writes a JSON artifact under
`results/evaluation/candidate_search/`. The guard proven here is narrow: that artifact may
*propose* a candidate, but it may never read as promotion / champion / signoff *authority*.

Invariant: ``candidate_search artifact != promotion evidence`` — research proposes; it does
not approve.
"""

from __future__ import annotations

import importlib.util
import inspect
import sys
from pathlib import Path

from core.decision.candidate_builder import build_candidate_packet, metric_snapshot_from_mapping

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "scripts" / "audit" / "find_new_champion_candidate.py"


def _load_search_module():
    spec = importlib.util.spec_from_file_location("find_new_champion_candidate", SCRIPT_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    # Register before exec so the module's dataclasses can resolve string annotations
    # (PEP 563 / `from __future__ import annotations`) via sys.modules[cls.__module__].
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _snapshot(*, pf: float, dd: float, tpy: float, stability: float):
    return metric_snapshot_from_mapping(
        {
            "strategy_family": "ri",
            "profit_factor": pf,
            "max_drawdown": dd,
            "trades_per_year": tpy,
            "stability": stability,
            "winrate": 0.55,
            "metadata": {"source": "guard-test"},
        }
    )


def test_research_promotion_flags_are_not_forced() -> None:
    """Regression guard: the search must not self-issue promotion override/signoff."""
    mod = _load_search_module()
    assert mod.RESEARCH_PROMOTION_OVERRIDE is False
    assert mod.RESEARCH_PROMOTION_SIGNOFF is False


def test_research_flags_cannot_force_ready_for_promotion_even_for_strong_candidate() -> None:
    """Forced flags cannot make ready_for_promotion true via the research path.

    A clearly-superior candidate is an objective *proposal* (comparison may say PROMOTE), but
    the research path holds ready_for_promotion False because it issues no override/signoff.
    """
    mod = _load_search_module()
    incumbent = _snapshot(pf=1.20, dd=0.12, tpy=85.0, stability=0.80)
    candidate = _snapshot(pf=1.45, dd=0.08, tpy=120.0, stability=0.95)

    packet = build_candidate_packet(
        incumbent,
        candidate,
        promotion_override_flag=mod.RESEARCH_PROMOTION_OVERRIDE,
        promotion_signoff_flag=mod.RESEARCH_PROMOTION_SIGNOFF,
    )

    assert packet.ready_for_promotion is False


def test_candidate_search_artifact_is_stamped_non_authoritative() -> None:
    mod = _load_search_module()
    stamp = mod.research_authority_stamp()
    assert stamp["status"] == "research_only"
    assert stamp["non_authoritative"] is True
    assert stamp["requires_human_signoff"] is True
    assert "propose" in str(stamp["note"]).lower()


def test_research_run_payload_is_stamped_and_still_useful() -> None:
    mod = _load_search_module()
    best_eval = {
        "spec": {"label": "grid_a"},
        "metrics": {"profit_factor": 1.45},
        "score": 0.91,
        "hard_failures": [],
        "candidate_packet": {
            "ready_for_promotion": False,
            "comparison": {"decision": "promote"},
        },
    }
    payload = mod.build_research_run_payload(
        run_at="20260618T000000Z",
        symbol="tBTCUSD",
        timeframe="1h",
        incumbent_payload={"profit_factor": 1.20, "_scored": {"hidden": True}},
        best_eval=best_eval,
        evaluations=[best_eval],
    )

    # Stamped non-authoritative ...
    assert payload["authority"]["status"] == "research_only"
    assert payload["authority"]["requires_human_signoff"] is True
    # ... still a useful research artifact (the proposal is preserved) ...
    assert payload["best_candidate"] is best_eval
    assert payload["evaluations"] == [best_eval]
    assert payload["incumbent"] == {"profit_factor": 1.20}  # private _scored field stripped
    # ... and its best candidate is not presentable as approved.
    assert payload["best_candidate"]["candidate_packet"]["ready_for_promotion"] is False


def test_research_path_is_results_scoped_and_seed_read_only() -> None:
    """Proxy for 'research path does not mutate champion/config/runtime authority'.

    The search writes only under results/evaluation/candidate_search/ and reads the
    repo-tracked seed read-only — it never targets config/runtime.json or champions/.
    """
    mod = _load_search_module()
    assert "/results/evaluation/candidate_search" in mod.DEFAULT_OUTPUT_DIR.as_posix()
    assert mod.RUNTIME_SEED_PATH.name == "runtime.seed.json"


def test_main_write_path_is_stamped_and_not_self_authorized() -> None:
    """The stamp cannot be silently bypassed and the search must not self-issue authority.

    main() runs a real backtest (too heavy to call here), so assert at the source level that
    its single artifact write routes through the stamping helper, and that no output surface —
    including the opt-in --trace gate — attributes governance-kernel authority to the search.
    """
    mod = _load_search_module()
    main_src = inspect.getsource(mod.main)
    assert "build_research_run_payload(" in main_src  # artifact is always stamped
    assert "write_text" in main_src
    assert "governance-kernel" not in main_src  # third surface (trace gate) de-authorized
