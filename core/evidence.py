"""Evidence primitives for reproducible MedusaCore decisions."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Dict

from .contracts import EvaluationResult, Measurement, MutationProposal, stable_hash


@dataclass(frozen=True)
class EvidenceBundle:
    """Minimal immutable evidence required to explain a promotion decision."""

    proposal: MutationProposal
    baseline: Measurement
    candidate: Measurement
    evaluation: EvaluationResult
    seed: int
    created_at: str

    @classmethod
    def create(
        cls,
        *,
        proposal: MutationProposal,
        baseline: Measurement,
        candidate: Measurement,
        evaluation: EvaluationResult,
        seed: int,
    ) -> "EvidenceBundle":
        return cls(
            proposal=proposal,
            baseline=baseline,
            candidate=candidate,
            evaluation=evaluation,
            seed=seed,
            created_at=datetime.now(timezone.utc).isoformat(),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def evidence_hash(self) -> str:
        return stable_hash(self.to_dict())
