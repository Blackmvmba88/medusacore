"""Adapter to integrate ethical judgments into blast radius scoring."""

from typing import Dict, List, Any

from .ethical_governance import assess_ethical_impact


def compute_ethics_penalty(judgments: List[Dict], policy: Dict = None) -> float:
    """Compute a penalty (0-100) from ethical judgments.

    Default mapping: penalty = max_violation_level * 100 + 2 * len(judgments)
    Policy can adjust `penalty_scale`.
    Clamped to [0, 100].
    """
    if not judgments:
        return 0.0

    max_v = max(j.get("violation_level", 0.0) for j in judgments)
    base = max_v * 100.0 + 2.0 * len(judgments)
    scale = 1.0
    if policy and isinstance(policy, dict):
        scale = float(policy.get("penalty_scale", 1.0))
    penalty = base * scale
    if penalty > 100.0:
        penalty = 100.0
    return penalty


def decide_operational_action(judgments: List[Dict], policy: Dict = None) -> str:
    """Decide operational disposition: ALLOW, REVIEW, BLOCK based on policy thresholds."""
    if not policy:
        policy = {}
    block_thr = float(policy.get("block_threshold", 0.85))
    review_thr = float(policy.get("review_threshold", 0.6))
    review_count = int(policy.get("review_count", 1))

    if not judgments:
        return "ALLOW"

    max_v = max(j.get("violation_level", 0.0) for j in judgments)
    if any(j.get("violation_level", 0.0) >= block_thr for j in judgments):
        return "BLOCK"
    if max_v >= review_thr or len(judgments) >= review_count:
        return "REVIEW"
    return "ALLOW"

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
    report: Dict[str, Any], judgments: List[Dict], policy: Dict = None, policy_hash: str = None
) -> Dict[str, Any]:
    """Apply ethics penalty to an existing blast radius report object.

    Modifies and returns the report dict. Policy optional to drive decisions.
    """
    blast = report.setdefault("blast_radius", {})
    original_score = float(blast.get("score", 0.0))

    penalty = compute_ethics_penalty(judgments, policy)
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

    # Compute operational decision
    operational = decide_operational_action(judgments, policy)
    ethical["operational_decision"] = operational

    # Map operational decision to human oversight flag
    ethical["human_oversight_required"] = operational in ("REVIEW", "BLOCK")
    ethical["judgments"] = judgments
    if policy_hash:
        # Record policy hash for traceability
        report.setdefault("meta", {})["policy_hash"] = policy_hash
        ethical["policy_hash"] = policy_hash

    return report


def apply_ethics_to_scoring(
    report: Dict[str, Any], capabilities: Dict[str, List], context: Dict[str, Any], policy: Dict = None, policy_hash: str = None
) -> Dict[str, Any]:
    """End-to-end convenience: run ethical assessment and apply to report.

    Optional `policy` (dict) and `policy_hash` allow deterministic decisioning and traceability.
    """
    # Ensure context carries policy_hash and target_sha256 for deterministic IDs/audit
    if policy_hash:
        context = dict(context)
        context.setdefault("policy_hash", policy_hash)

    assessment = assess_ethical_impact(capabilities, context)
    judgments = assessment.get("ethical_impact", {}).get("judgments", [])
    # judgments are dicts already via to_dict()
    return apply_ethics_to_report(report, judgments, policy=policy, policy_hash=policy_hash)
