"""Unit tests for core genesis primitives."""
import pytest
from core.genesis import PrimordialSeed, HermeticCore


def test_axiom_zero_exists():
    assert isinstance(PrimordialSeed.AXIOM_ZERO, dict)
    assert "statement" in PrimordialSeed.AXIOM_ZERO


def test_derive_principles_has_keys():
    core = HermeticCore()
    keys = set(core.principles.keys())
    expected = {"recursion", "resistance_oracle", "temporal_topology", "holographic_memory"}
    assert expected.issubset(keys)


def test_evolve_principle_versioning():
    core = HermeticCore()
    prev_count = len(core.evolution_log)
    entry = core.evolve_principle(
        principle_name="recursion",
        new_variant="recursion_vX: experimental",
        conditions="unit-test",
        evidence={"ok": True},
    )
    assert len(core.evolution_log) == prev_count + 1
    # new key created
    assert any(k.startswith("recursion_v") for k in core.principles.keys())
    assert entry["trigger"] == "unit-test"


def test_evolve_nonexistent_principle_raises():
    core = HermeticCore()
    with pytest.raises(KeyError):
        core.evolve_principle("nonexistent", "v1", "cond", {})
