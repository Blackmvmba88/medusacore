from hydras.red import RedTeamHydra
from hydras.blue import BlueTeamHydra
from hydras.forensics import ForensicsHydra


def test_red_probe():
    r = RedTeamHydra()
    rep = r.probe({"state": "ok"})
    assert rep["finding"] == "simulated_probe"


def test_blue_assess_ok():
    b = BlueTeamHydra()
    rep = b.assess({"candidate": "x"})
    assert rep["assessment"] == "ok"


def test_forensics_capture():
    f = ForensicsHydra()
    rep = f.capture("wip/genesis", {"log": "value"})
    assert rep["branch"] == "wip/genesis"
    assert "artifacts" in rep
