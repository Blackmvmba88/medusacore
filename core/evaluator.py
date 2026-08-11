"""Deterministic candidate evaluator for MedusaCore."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence

from .contracts import EvaluationResult, InvariantResult, Measurement, Verdict

Invariant = Callable[[Measurement], InvariantResult]


@dataclass(frozen=True)
class ObjectiveSpec:
    """One measurable objective used to compare baseline and candidate."""

    metric: str
    direction: str = "maximize"
    min_improvement: float = 0.0

    def __post_init__(self) -> None:
        if self.direction not in {"maximize", "minimize"}:
            raise ValueError("direction must be 'maximize' or 'minimize'")
        if self.min_improvement < 0:
            raise ValueError("min_improvement cannot be negative")


class Evaluator:
    """Compare a candidate against a baseline under explicit invariants."""

    def evaluate(
        self,
        baseline: Measurement,
        candidate: Measurement,
        objective: ObjectiveSpec,
        invariants: Sequence[Invariant] = (),
    ) -> EvaluationResult:
        invariant_results = []

        for invariant in invariants:
            try:
                result = invariant(candidate)
            except Exception as exc:
                return EvaluationResult(
                    verdict=Verdict.UNKNOWN,
                    objective_metric=objective.metric,
                    objective_delta=None,
                    invariants=tuple(invariant_results),
                    reason=f"invariant evaluation failed: {exc}",
                )
            invariant_results.append(result)

        if not candidate.success:
            return EvaluationResult(
                verdict=Verdict.REJECT,
                objective_metric=objective.metric,
                objective_delta=None,
                invariants=tuple(invariant_results),
                reason="candidate execution failed",
            )

        failed = [item.name for item in invariant_results if not item.passed]
        if failed:
            return EvaluationResult(
                verdict=Verdict.REJECT,
                objective_metric=objective.metric,
                objective_delta=None,
                invariants=tuple(invariant_results),
                reason=f"candidate violated invariants: {', '.join(failed)}",
            )

        if objective.metric not in baseline.metrics or objective.metric not in candidate.metrics:
            return EvaluationResult(
                verdict=Verdict.UNKNOWN,
                objective_metric=objective.metric,
                objective_delta=None,
                invariants=tuple(invariant_results),
                reason=f"objective metric '{objective.metric}' is missing",
            )

        baseline_value = baseline.metrics[objective.metric]
        candidate_value = candidate.metrics[objective.metric]
        if objective.direction == "maximize":
            delta = candidate_value - baseline_value
        else:
            delta = baseline_value - candidate_value

        if delta >= objective.min_improvement:
            verdict = Verdict.ACCEPT
            reason = (
                f"objective improved by {delta:.6g}; "
                f"required >= {objective.min_improvement:.6g}"
            )
        else:
            verdict = Verdict.REJECT
            reason = (
                f"objective improvement {delta:.6g} is below required "
                f"{objective.min_improvement:.6g}"
            )

        return EvaluationResult(
            verdict=verdict,
            objective_metric=objective.metric,
            objective_delta=delta,
            invariants=tuple(invariant_results),
            reason=reason,
        )
