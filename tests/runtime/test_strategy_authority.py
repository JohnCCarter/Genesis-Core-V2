from __future__ import annotations

import pytest

from core.config.authority_mode_resolver import (
    AUTHORITY_MODE_SOURCE_ALIAS,
    AUTHORITY_MODE_SOURCE_ALIAS_INVALID_FALLBACK,
    AUTHORITY_MODE_SOURCE_CANONICAL,
    AUTHORITY_MODE_SOURCE_CANONICAL_INVALID_FALLBACK,
    AUTHORITY_MODE_SOURCE_DEFAULT,
    resolve_authority_mode_with_source_permissive,
)
from core.strategy.family_admission import (
    StrategyFamilyAdmissionError,
    validate_optimizer_family_admission,
    validate_strategy_family_admission,
)
from core.strategy.family_registry import (
    STRATEGY_FAMILY_LEGACY,
    STRATEGY_FAMILY_RI,
    StrategyFamilyValidationError,
    inject_strategy_family,
    resolve_strategy_family,
    validate_cross_family_promotion,
)
from core.strategy.run_intent import RunIntentValidationError


def _canonical_ri_config(*, strategy_family: str | None = None) -> dict[str, object]:
    payload: dict[str, object] = {
        "thresholds": {
            "entry_conf_overall": 0.25,
            "regime_proba": {"balanced": 0.36},
            "signal_adaptation": {
                "atr_period": 14,
                "zones": {
                    "low": {"entry_conf_overall": 0.16, "regime_proba": 0.33},
                    "mid": {"entry_conf_overall": 0.40, "regime_proba": 0.51},
                    "high": {"entry_conf_overall": 0.32, "regime_proba": 0.57},
                },
            },
        },
        "gates": {"hysteresis_steps": 3, "cooldown_bars": 2},
        "multi_timeframe": {"regime_intelligence": {"authority_mode": "regime_module"}},
    }
    if strategy_family is not None:
        payload["strategy_family"] = strategy_family
    return payload


def _ri_research_config() -> dict[str, object]:
    return {
        "strategy_family": "ri",
        "thresholds": {
            "entry_conf_overall": 0.28,
            "regime_proba": {"balanced": 0.36},
            "signal_adaptation": {
                "atr_period": 14,
                "zones": {
                    "low": {"entry_conf_overall": 0.14, "regime_proba": 0.32},
                    "mid": {"entry_conf_overall": 0.42, "regime_proba": 0.52},
                    "high": {"entry_conf_overall": 0.34, "regime_proba": 0.58},
                },
            },
        },
        "gates": {"hysteresis_steps": 2, "cooldown_bars": 1},
        "multi_timeframe": {"regime_intelligence": {"authority_mode": "regime_module"}},
    }


def _ri_optimizer_research_config(
    *, run_intent: str | None = "research_slice"
) -> dict[str, object]:
    runs: dict[str, object] = {}
    if run_intent is not None:
        runs["run_intent"] = run_intent
    return {
        "strategy_family": "ri",
        "meta": {"runs": runs},
        "parameters": {
            "multi_timeframe.regime_intelligence.authority_mode": {
                "type": "fixed",
                "value": "regime_module",
            },
            "thresholds.signal_adaptation.atr_period": {"type": "fixed", "value": 14},
            "gates.hysteresis_steps": {"type": "int", "low": 2, "high": 4, "step": 1},
            "gates.cooldown_bars": {"type": "int", "low": 1, "high": 3, "step": 1},
            "thresholds.entry_conf_overall": {"type": "fixed", "value": 0.28},
            "thresholds.regime_proba.balanced": {"type": "fixed", "value": 0.36},
            "thresholds.signal_adaptation.zones.low.entry_conf_overall": {
                "type": "fixed",
                "value": 0.14,
            },
            "thresholds.signal_adaptation.zones.low.regime_proba": {
                "type": "fixed",
                "value": 0.32,
            },
            "thresholds.signal_adaptation.zones.mid.entry_conf_overall": {
                "type": "fixed",
                "value": 0.42,
            },
            "thresholds.signal_adaptation.zones.mid.regime_proba": {
                "type": "fixed",
                "value": 0.52,
            },
            "thresholds.signal_adaptation.zones.high.entry_conf_overall": {
                "type": "fixed",
                "value": 0.34,
            },
            "thresholds.signal_adaptation.zones.high.regime_proba": {
                "type": "fixed",
                "value": 0.58,
            },
        },
    }


@pytest.mark.parametrize(
    ("cfg", "expected"),
    [
        ({}, ("regime_module", AUTHORITY_MODE_SOURCE_DEFAULT)),
        (
            {"regime_unified": {"authority_mode": "regime_module"}},
            ("regime_module", AUTHORITY_MODE_SOURCE_ALIAS),
        ),
        (
            {
                "multi_timeframe": {"regime_intelligence": {"authority_mode": " legacy "}},
                "regime_unified": {"authority_mode": "regime_module"},
            },
            ("legacy", AUTHORITY_MODE_SOURCE_CANONICAL),
        ),
        (
            {
                "multi_timeframe": {"regime_intelligence": {"authority_mode": "invalid_mode"}},
                "regime_unified": {"authority_mode": "regime_module"},
            },
            ("regime_module", AUTHORITY_MODE_SOURCE_CANONICAL_INVALID_FALLBACK),
        ),
        (
            {"regime_unified": {"authority_mode": "invalid_mode"}},
            ("regime_module", AUTHORITY_MODE_SOURCE_ALIAS_INVALID_FALLBACK),
        ),
    ],
    ids=[
        "default_regime_module",
        "alias_regime_module",
        "canonical_legacy_wins",
        "canonical_invalid_falls_back_to_regime_module",
        "alias_invalid_falls_back_to_regime_module",
    ],
)
def test_strategy_authority_resolver_contract(
    cfg: dict[str, object], expected: tuple[str, str]
) -> None:
    assert resolve_authority_mode_with_source_permissive(cfg) == expected


def test_strategy_family_registry_contract() -> None:
    cfg = _canonical_ri_config(strategy_family="ri")

    assert resolve_strategy_family(cfg) == STRATEGY_FAMILY_RI
    assert (
        inject_strategy_family({"thresholds": {"entry_conf_overall": 0.6}})["strategy_family"]
        == STRATEGY_FAMILY_LEGACY
    )

    with pytest.raises(StrategyFamilyValidationError, match="cross_family_promotion"):
        validate_cross_family_promotion("legacy", "ri")

    validate_cross_family_promotion(
        "legacy",
        "ri",
        explicit_override=True,
        governance_signoff=True,
    )


def test_strategy_family_admission_contract() -> None:
    family, run_intent = validate_strategy_family_admission(
        _ri_research_config(),
        run_intent="research_slice",
    )
    assert family == "ri"
    assert run_intent == "research_slice"

    with pytest.raises(StrategyFamilyAdmissionError, match="champion_freeze"):
        validate_strategy_family_admission(
            _ri_research_config(),
            run_intent="champion_freeze",
        )

    with pytest.raises(StrategyFamilyAdmissionError, match="champion_freeze"):
        validate_optimizer_family_admission(
            _ri_optimizer_research_config(run_intent="champion_freeze")
        )

    with pytest.raises(RunIntentValidationError, match="invalid_run_intent"):
        validate_optimizer_family_admission(_ri_optimizer_research_config(run_intent="mystery"))
