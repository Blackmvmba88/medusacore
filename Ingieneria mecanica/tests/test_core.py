from core.genesis import PrimordialSeed, HermeticCore
import pytest


def test_axiom_zero_has_statement():
    assert "statement" in PrimordialSeed.AXIOM_ZERO
    assert "meta_instruction" in PrimordialSeed.AXIOM_ZERO


def test_derive_principles_contains_recursion():
    core = HermeticCore()
    assert "recursion" in core.principles


def test_evolve_principle_adds_variant_and_log():
    core = HermeticCore()
    entry = core.evolve_principle(
        "recursion", "variant 42", "unit test", {"evidence": "ok"}
    )
    assert core.evolution_log[-1] == entry
    assert any(k.startswith("recursion_v") for k in core.principles.keys())
    # ensure the mutation text is present in the principles values
    assert any("variant 42" in v for v in core.principles.values())


def test_evolve_missing_principle_raises():
    core = HermeticCore()
    with pytest.raises(KeyError):
        core.evolve_principle("nope", "v", "test", {})
