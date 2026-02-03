"""Adapter to integrate ethical judgments into blast radius scoring."""

from typing import Dict, List, Any

from .ethical_governance import assess_ethical_impact


def compute_ethics_penalty(judgments: List[Dict]) -> float:
    """Compute a penalty (0-100) from ethical judgments.

    Simple mapping: penalty = max_violation_level * 100 + 2 * len(judgments)
    Clamped to [0, 100].
    """
    if not judgments:
        return 0.0

    max_v = max(j.get("violation_level", 0.0) for j in judgments)
    penalty = max_v * 100.0 + 2.0 * len(judgments)
    if penalty > 100.0:
        penalty = 100.0
    return penalty


def classification_from_score(score: float) -> str:
    if score <= 10:
        return "MINIMAL"
    if score <= 30:
        return "LOW"
    if score <= 60:
        return "MODERATE"
    if score <= 85:
        return "HIGH"
    return "CRITICAL"


def apply_ethics_to_report(
    report: Dict[str, Any], judgments: List[Dict]
) -> Dict[str, Any]:
    """Apply ethics penalty to an existing blast radius report object.

    Modifies and returns the report dict.
    """
    blast = report.setdefault("blast_radius", {})
    original_score = float(blast.get("score", 0.0))

    penalty = compute_ethics_penalty(judgments)
    final_score = original_score + penalty
    if final_score > 100.0:
        final_score = 100.0

    # Save original score for audit
    blast["original_score"] = original_score
    blast["score"] = final_score
    blast["classification"] = classification_from_score(final_score)

    # Attach ethical metadata
    ethical = report.setdefault("ethical_governance", {})
    ethical["ethical_penalty"] = penalty
    ethical["human_oversight_required"] = any(
        (j.get("violation_level", 0.0) >= 0.85) for j in judgments
    )
    ethical["judgments"] = judgments

    return report


def apply_ethics_to_scoring(
    report: Dict[str, Any], capabilities: Dict[str, List], context: Dict[str, Any]
) -> Dict[str, Any]:
    """End-to-end convenience: run ethical assessment and apply to report."""
    assessment = assess_ethical_impact(capabilities, context)
    judgments = assessment.get("ethical_impact", {}).get("judgments", [])
    # judgments are dicts already via to_dict()
    return apply_ethics_to_report(report, judgments)
