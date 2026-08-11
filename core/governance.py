"""Governance gates for MedusaCore experiments and promotions."""
from __future__ import annotations

from dataclasses import dataclass

from .contracts import EvaluationResult, MutationProposal, RuntimeEnvelope, Verdict


@dataclass(frozen=True)
class GateDecision:
    allowed: bool
    reason: str


class MutationGate:
    """Pure policy checks; performs no mutation itself."""

    @staticmethod
    def _matches_target(target: str, protected: str) -> bool:
        normalized_target = target.strip("/")
        normalized_protected = protected.strip("/")
        return (
            normalized_target == normalized_protected
            or normalized_target.startswith(normalized_protected + "/")
        )

    def authorize_experiment(
        self,
        proposal: MutationProposal,
        envelope: RuntimeEnvelope,
    ) -> GateDecision:
        if proposal.kind not in envelope.allowed_mutation_kinds:
            return GateDecision(
                False,
                f"mutation kind '{proposal.kind}' is outside the runtime envelope",
            )

        for protected in envelope.immutable_targets:
            if self._matches_target(proposal.target, protected):
                return GateDecision(
                    False,
                    f"target '{proposal.target}' belongs to the immutable kernel",
                )

        if not proposal.candidate_id.strip():
            return GateDecision(False, "candidate_id is required")
        if not proposal.payload_hash.strip():
            return GateDecision(False, "payload_hash is required")

        return GateDecision(True, "candidate is authorized for bounded experimentation")

    def authorize_promotion(
        self,
        evaluation: EvaluationResult,
        *,
        evidence_hash: str | None,
        envelope: RuntimeEnvelope,
    ) -> GateDecision:
        if evaluation.verdict is not Verdict.ACCEPT:
            return GateDecision(
                False,
                f"promotion requires ACCEPT, got {evaluation.verdict.value}",
            )

        if envelope.require_evidence and not evidence_hash:
            return GateDecision(False, "promotion requires an evidence hash")

        return GateDecision(True, "candidate satisfies promotion policy")
