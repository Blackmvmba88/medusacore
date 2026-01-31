from core.genesis import HermeticCore
from hydras.red import RedTeamHydra


def test_evolve_principle_stores_malicious_evidence():
    core = HermeticCore()
    malicious_evidence = {
        "cmd": "rm -rf / --no-preserve-root",
        "payload": "<script>alert('xss')</script>",
        "nested": {"a": [1, 2, {"b": "c"}]},
    }
    entry = core.evolve_principle("recursion", "variant-malicious", "adversarial", malicious_evidence)
    # Evidence must be stored as-is and not executed; test checks equality
    assert entry["evidence"] == malicious_evidence
    assert core.evolution_log[-1]["evidence"] == malicious_evidence


def test_red_probe_handles_malicious_input_gracefully():
    r = RedTeamHydra()
    # Simulate different attack-like states
    inputs = ["DROP TABLE users;", {"payload": "' OR '1'='1"}, 12345, None]
    for inp in inputs:
        rep = r.probe({"state": inp})
        assert isinstance(rep, dict)
        assert "finding" in rep
