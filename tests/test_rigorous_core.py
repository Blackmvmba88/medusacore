"""Tests for MedusaCore's bounded-experimentation contracts."""
import pytest

from core.contracts import (
    InvariantResult,
    Measurement,
    MutationProposal,
    ResourceBudget,
    RuntimeEnvelope,
    Verdict,
    stable_hash,
)
from core.evaluator import Evaluator, ObjectiveSpec
from core.evidence import EvidenceBundle
from core.governance import MutationGate


def test_budget_rejects_non_positive_values():
    with pytest.raises(ValueError):
        ResourceBudget(wall_seconds=0)


def test_stable_hash_is_order_independent_for_mapping_keys():
    assert stable_hash({"b": 2, "a": 1}) == stable_hash({"a": 1, "b": 2})


def test_immutable_kernel_target_is_denied():
    proposal = MutationProposal(
        candidate_id="candidate-1",
        target="core/contracts.py",
        kind="strategy",
        payload_hash="abc",
    )
    decision = MutationGate().authorize_experiment(proposal, RuntimeEnvelope())
    assert decision.allowed is False
    assert "immutable kernel" in decision.reason


def test_mutable_strategy_is_allowed_for_experiment():
    proposal = MutationProposal(
        candidate_id="candidate-2",
        target="strategies/router.py",
        kind="strategy",
        payload_hash="abc",
    )
    decision = MutationGate().authorize_experiment(proposal, RuntimeEnvelope())
    assert decision.allowed is True


def test_candidate_is_accepted_only_when_objective_improves_and_invariants_hold():
    baseline = Measurement("route", 1.0, True, metrics={"score": 0.70})
    candidate = Measurement("route", 1.0, True, metrics={"score": 0.82})

    def safe(measurement: Measurement) -> InvariantResult:
        return InvariantResult("safety", passed=measurement.success)

    result = Evaluator().evaluate(
        baseline,
        candidate,
        ObjectiveSpec("score", direction="maximize", min_improvement=0.05),
        invariants=[safe],
    )
    assert result.verdict is Verdict.ACCEPT
    assert result.objective_delta == pytest.approx(0.12)


def test_candidate_is_rejected_when_an_invariant_fails():
    baseline = Measurement("route", 1.0, True, metrics={"score": 0.70})
    candidate = Measurement("route", 1.0, True, metrics={"score": 0.99})

    def unsafe(_: Measurement) -> InvariantResult:
        return InvariantResult("safety", passed=False, detail="guardrail regression")

    result = Evaluator().evaluate(
        baseline,
        candidate,
        ObjectiveSpec("score"),
        invariants=[unsafe],
    )
    assert result.verdict is Verdict.REJECT
    assert "safety" in result.reason


def test_missing_metric_is_unknown_not_accept():
    baseline = Measurement("route", 1.0, True, metrics={"score": 0.70})
    candidate = Measurement("route", 1.0, True, metrics={})
    result = Evaluator().evaluate(baseline, candidate, ObjectiveSpec("score"))
    assert result.verdict is Verdict.UNKNOWN


def test_promotion_requires_accept_and_evidence():
    baseline = Measurement("route", 1.0, True, metrics={"score": 0.70})
    candidate = Measurement("route", 1.0, True, metrics={"score": 0.80})
    evaluation = Evaluator().evaluate(
        baseline,
        candidate,
        ObjectiveSpec("score", min_improvement=0.05),
    )
    proposal = MutationProposal("candidate-3", "strategies/router.py", "strategy", "abc")
    bundle = EvidenceBundle.create(
        proposal=proposal,
        baseline=baseline,
        candidate=candidate,
        evaluation=evaluation,
        seed=42,
    )

    gate = MutationGate()
    denied = gate.authorize_promotion(
        evaluation,
        evidence_hash=None,
        envelope=RuntimeEnvelope(require_evidence=True),
    )
    allowed = gate.authorize_promotion(
        evaluation,
        evidence_hash=bundle.evidence_hash(),
        envelope=RuntimeEnvelope(require_evidence=True),
    )

    assert denied.allowed is False
    assert allowed.allowed is True
