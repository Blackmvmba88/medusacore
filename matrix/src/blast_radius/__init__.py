"""blast_radius package initialiser."""

from .ethical_governance import (
    assess_ethical_impact,
    global_ethics,
    EthicalJudgment,
    EthicalPrinciple,
)
from .ethics_adapter import (
    compute_ethics_penalty,
    apply_ethics_to_report,
    apply_ethics_to_scoring,
)

__all__ = [
    "assess_ethical_impact",
    "global_ethics",
    "EthicalJudgment",
    "EthicalPrinciple",
    "compute_ethics_penalty",
    "apply_ethics_to_report",
    "apply_ethics_to_scoring",
]
