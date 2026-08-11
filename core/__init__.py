"""MedusaCore - Core package for hermetic seed and bounded optimization.

The package keeps AXIOM_ZERO and HermeticCore as the conceptual genesis layer,
while contracts, governance, evaluation, and evidence provide the testable
boundary for bounded experimentation.
"""
from .seed import PrimordialSeed, HermeticCore, GenesisCommand
from .optimizer import Optimizer, PerformanceMonitor
from .contracts import (
    EvaluationResult,
    InvariantResult,
    Measurement,
    MutationProposal,
    ResourceBudget,
    RuntimeEnvelope,
    Verdict,
    stable_hash,
)
from .evaluator import Evaluator, ObjectiveSpec
from .evidence import EvidenceBundle
from .governance import GateDecision, MutationGate

__all__ = [
    "PrimordialSeed",
    "HermeticCore",
    "GenesisCommand",
    "Optimizer",
    "PerformanceMonitor",
    "EvaluationResult",
    "InvariantResult",
    "Measurement",
    "MutationProposal",
    "ResourceBudget",
    "RuntimeEnvelope",
    "Verdict",
    "stable_hash",
    "Evaluator",
    "ObjectiveSpec",
    "EvidenceBundle",
    "GateDecision",
    "MutationGate",
]
__version__ = "0.2.0-dev"
