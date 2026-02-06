from core.genesis import run_genesis_dry_run, GenesisCommand


def test_dry_run_returns_first_breath_and_principles():
    out = run_genesis_dry_run()
    assert "first_breath" in out
    assert isinstance(out["initial_principles"], list)
    assert len(out["initial_principles"]) > 0


def test_genesis_command_contains_mandate():
    assert "MEDUSA-HYDRA" in GenesisCommand.summary()
