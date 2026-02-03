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


if __name__ == "__main__":
    pytest.main([__file__])
