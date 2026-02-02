"""Unit tests for core seed primitives."""
import pytest
from core.seed import PrimordialSeed, HermeticCore, GenesisCommand, run_genesis_dry_run


def test_axiom_zero_exists():
    """Test that AXIOM_ZERO exists and has required fields."""
    assert isinstance(PrimordialSeed.AXIOM_ZERO, dict)
    assert "statement" in PrimordialSeed.AXIOM_ZERO
    assert "essence" in PrimordialSeed.AXIOM_ZERO
    assert "meta_instruction" in PrimordialSeed.AXIOM_ZERO


def test_primordial_seed_initialize():
    """Test PrimordialSeed initialization."""
    seed = PrimordialSeed.initialize()
    assert seed == PrimordialSeed.AXIOM_ZERO
    assert "OBSERVA" in seed["statement"]


def test_primordial_seed_get_essence():
    """Test getting the essence of AXIOM_ZERO."""
    essence = PrimordialSeed.get_essence()
    assert "PERCEPCIÓN" in essence
    assert "ACCIÓN" in essence
    assert "MEDICIÓN" in essence
    assert "INTEGRACIÓN" in essence


def test_hermetic_core_initialization():
    """Test HermeticCore initializes with principles."""
    core = HermeticCore()
    assert len(core.principles) > 0
    assert isinstance(core.principles, dict)
    assert len(core.evolution_log) == 0


def test_derive_principles_has_keys():
    """Test that derived principles contain expected keys."""
    core = HermeticCore()
    keys = set(core.principles.keys())
    expected = {
        "recursion", 
        "resistance_oracle", 
        "temporal_topology", 
        "holographic_memory",
        "paradox_navigation",
        "leverage_points",
        "omnidirectional_awareness"
    }
    assert expected.issubset(keys)


def test_get_principle():
    """Test retrieving a specific principle."""
    core = HermeticCore()
    recursion = core.get_principle("recursion")
    assert recursion != ""
    assert "entidad" in recursion.lower() or "función" in recursion.lower()
    
    # Test non-existent principle
    assert core.get_principle("nonexistent") == ""


def test_list_principles():
    """Test listing all principles."""
    core = HermeticCore()
    principles = core.list_principles()
    assert isinstance(principles, list)
    assert len(principles) >= 7
    assert "recursion" in principles


def test_evolve_principle_versioning():
    """Test that evolving a principle creates a new version."""
    core = HermeticCore()
    prev_count = len(core.evolution_log)
    
    entry = core.evolve_principle(
        principle_name="recursion",
        new_variant="recursion_vX: experimental variant",
        conditions="unit-test",
        evidence={"ok": True, "test_id": "test_001"},
    )
    
    # Check evolution log
    assert len(core.evolution_log) == prev_count + 1
    assert entry["trigger"] == "unit-test"
    assert entry["principle"] == "recursion"
    assert entry["mutation"] == "recursion_vX: experimental variant"
    
    # Check new versioned key was created
    assert any(k.startswith("recursion_v") for k in core.principles.keys())
    
    # Original principle should still exist
    assert "recursion" in core.principles


def test_evolve_nonexistent_principle_raises():
    """Test that evolving a non-existent principle raises KeyError."""
    core = HermeticCore()
    with pytest.raises(KeyError):
        core.evolve_principle("nonexistent", "v1", "cond", {})


def test_multiple_evolutions():
    """Test multiple evolutions of the same principle."""
    core = HermeticCore()
    
    # First evolution
    core.evolve_principle("recursion", "variant_1", "test_1", {})
    assert "recursion_v1" in core.principles
    
    # Second evolution
    core.evolve_principle("recursion", "variant_2", "test_2", {})
    assert "recursion_v2" in core.principles
    
    # Both versions should exist along with original
    assert "recursion" in core.principles
    assert len(core.evolution_log) == 2


def test_genesis_command_summary():
    """Test GenesisCommand summary."""
    summary = GenesisCommand.summary()
    assert "MEDUSA-HYDRA" in summary
    assert "CONÓCETE A TI MISMO" in summary
    assert "RESTRICCIÓN" in summary


def test_run_genesis_dry_run():
    """Test the genesis dry-run function."""
    result = run_genesis_dry_run()
    
    assert "axiom_zero" in result
    assert "first_breath" in result
    assert "initial_principles" in result
    assert "principle_count" in result
    
    assert result["axiom_zero"] == PrimordialSeed.AXIOM_ZERO
    assert result["principle_count"] >= 7
    assert isinstance(result["initial_principles"], list)


def test_spacetime_coords():
    """Test that spacetime coordinates are generated correctly."""
    core = HermeticCore()
    coords = core._get_spacetime_coords()
    
    assert "timestamp" in coords
    assert "id" in coords
    assert coords["timestamp"].endswith("Z")
    assert len(coords["id"]) == 36  # UUID format
