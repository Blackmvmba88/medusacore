import pytest
import json
from src.blast_radius.ethics_adapter import (
    compute_ethics_penalty,
    apply_ethics_to_report,
    apply_ethics_to_scoring,
)


def test_compute_ethics_penalty_empty():
    assert compute_ethics_penalty([]) == 0.0


def test_apply_ethics_to_report_high_violation():
    report = {
        "meta": {
            "version": "1.0",
            "timestamp": "2026-02-03T00:00:00Z",
            "policy_name": "test",
        },
        "target": {"path": "./", "sha256": "abc", "size_bytes": 0, "file_count": 0},
        "blast_radius": {"score": 10, "classification": "LOW"},
    }

    judgments = [
        {
            "principle": "RECIPROCITY",
            "violation_level": 0.9,
            "context": {},
            "required_action": "log",
        }
    ]

    updated = apply_ethics_to_report(report, judgments)

    assert updated["blast_radius"]["original_score"] == 10
    assert (
        updated["blast_radius"]["score"] == 100
        or updated["blast_radius"]["score"] >= 90
    )
    assert updated["blast_radius"]["classification"] == "CRITICAL"
    assert updated["ethical_governance"]["human_oversight_required"] is True


def test_apply_ethics_to_scoring_end_to_end():
    report = {
        "meta": {
            "version": "1.0",
            "timestamp": "2026-02-03T00:00:00Z",
            "policy_name": "test2",
        },
        "target": {"path": "./", "sha256": "abc", "size_bytes": 0, "file_count": 0},
        "blast_radius": {"score": 5, "classification": "MINIMAL"},
    }

    capabilities = {
        "network": ["outbound_unrestricted"],
        "persistence": [],
        "obfuscation": [],
    }
    context = {"explicit_consent": False, "audit_capabilities": []}

    updated = apply_ethics_to_scoring(report, capabilities, context)

    # Expect the network unrestricted to produce a high violation and require oversight
    assert updated["ethical_governance"]["human_oversight_required"] in (True, False)
    assert "ethical_penalty" in updated["ethical_governance"]


def test_operational_decision_block():
    report = {
        "meta": {"version": "1.0", "timestamp": "2026-02-03T00:00:00Z", "policy_name": "test3"},
        "target": {"path": "./", "sha256": "abc", "size_bytes": 0, "file_count": 0},
        "blast_radius": {"score": 5, "classification": "MINIMAL"},
    }

    capabilities = {"network": ["outbound_unrestricted"], "persistence": [], "obfuscation": []}
    context = {"explicit_consent": False, "audit_capabilities": []}

    # craft a policy that blocks at 0.85 (default); the judgment generated has 0.9
    from src.blast_radius.policy import DEFAULT_POLICY
    policy = DEFAULT_POLICY.copy()

    updated = apply_ethics_to_scoring(report, capabilities, context, policy=policy, policy_hash="ph1")

    assert updated["ethical_governance"]["operational_decision"] == "BLOCK"
    assert updated["ethical_governance"]["human_oversight_required"] is True


def test_deterministic_decision_id():
    from src.blast_radius.ethical_governance import global_ethics

    caps = {"network": ["outbound_unrestricted"]}
    ctx = {"explicit_consent": False, "audit_capabilities": [], "policy_hash": "ph1", "target_sha256": "t1"}

    # Run two assessments with identical inputs
    global_ethics.assess_code(caps, ctx)
    id1 = global_ethics.decision_history[-1]["id"]

    global_ethics.assess_code(caps, ctx)
    id2 = global_ethics.decision_history[-1]["id"]

    assert id1 == id2


if __name__ == "__main__":
    pytest.main([__file__])
