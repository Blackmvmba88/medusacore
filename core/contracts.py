"""Formal contracts for MedusaCore experiments and promotions.

This module turns the project philosophy into explicit, testable data contracts.
It intentionally contains no autonomous side effects.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import hashlib
import json
from typing import Any, Dict, Iterable, Tuple


class Verdict(str, Enum):
    """Result of evaluating a candidate mutation."""

    ACCEPT = "accept"
    REJECT = "reject"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class ResourceBudget:
    """Declared resource envelope for one experiment.

    These values are policy inputs. Enforcing OS-level isolation is a separate
    concern and must not be implied by this data structure alone.
    """

    wall_seconds: float = 5.0
    cpu_seconds: float = 2.0
    memory_mb: int = 256
    max_iterations: int = 1
    max_output_bytes: int = 1_000_000
    network_allowed: bool = False

    def __post_init__(self) -> None:
        numeric = {
            "wall_seconds": self.wall_seconds,
            "cpu_seconds": self.cpu_seconds,
            "memory_mb": self.memory_mb,
            "max_iterations": self.max_iterations,
            "max_output_bytes": self.max_output_bytes,
        }
        invalid = [name for name, value in numeric.items() if value <= 0]
        if invalid:
            raise ValueError(f"Budget values must be > 0: {', '.join(invalid)}")


@dataclass(frozen=True)
class RuntimeEnvelope:
    """Policy boundary separating immutable kernel from mutable organism."""

    allowed_mutation_kinds: Tuple[str, ...] = (
        "parameter",
        "strategy",
        "workflow",
        "agent",
    )
    immutable_targets: Tuple[str, ...] = (
        "core/contracts.py",
        "core/governance.py",
    )
    budget: ResourceBudget = field(default_factory=ResourceBudget)
    require_evidence: bool = True


@dataclass(frozen=True)
class Measurement:
    """Measured outcome of a baseline or candidate execution."""

    operation: str
    duration_seconds: float
    success: bool
    metrics: Dict[str, float] = field(default_factory=dict)
    output_hash: str = ""
    errors: Tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.duration_seconds < 0:
            raise ValueError("duration_seconds cannot be negative")


@dataclass(frozen=True)
class InvariantResult:
    """One invariant check and its evidence-facing explanation."""

    name: str
    passed: bool
    detail: str = ""


@dataclass(frozen=True)
class EvaluationResult:
    """Decision produced by comparing a candidate with a baseline."""

    verdict: Verdict
    objective_metric: str
    objective_delta: float | None
    invariants: Tuple[InvariantResult, ...]
    reason: str


@dataclass(frozen=True)
class MutationProposal:
    """A candidate change MedusaCore may experiment with."""

    candidate_id: str
    target: str
    kind: str
    payload_hash: str


def stable_hash(payload: Any) -> str:
    """Return a deterministic SHA-256 hash for JSON-compatible evidence."""

    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=str,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def hash_lines(lines: Iterable[str]) -> str:
    """Hash a sequence while preserving item boundaries deterministically."""

    return stable_hash(list(lines))
