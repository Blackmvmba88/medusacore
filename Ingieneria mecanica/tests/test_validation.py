from core.genesis import HermeticCore


def test_principles_non_empty_strings():
    core = HermeticCore()
    for k, v in core.principles.items():
        assert isinstance(k, str)
        assert isinstance(v, str)
        assert v.strip() != ""


def test_evolve_preserves_original_and_adds_version():
    core = HermeticCore()
    original = core.principles.get("recursion")
    entry = core.evolve_principle("recursion", "variant-validated", "unit-test", {"evidence": "ok"})
    # original key must still exist and be unchanged
    assert core.principles["recursion"] == original
    # new version key should appear
    assert any(k.startswith("recursion_v") for k in core.principles.keys())
    # evolution log reference should match returned entry
    assert core.evolution_log[-1] == entry
