import pytest

from envconfig import ConfigError, Var, load


def test_defaults_and_conversion():
    cfg = load(
        {"PORT": Var(int, 80), "DEBUG": Var(bool, False), "HOSTS": Var(list, []), "RATIO": Var(float, 0.5)},
        {"PORT": "9000", "DEBUG": "Yes", "HOSTS": "a, b,,c"},
    )
    assert cfg == {"PORT": 9000, "DEBUG": True, "HOSTS": ["a", "b", "c"], "RATIO": 0.5}


def test_bool_variants():
    for raw, expected in [("1", True), ("off", False), ("TRUE", True), ("", False)]:
        assert load({"X": Var(bool)}, {"X": raw})["X"] is expected


def test_reports_all_problems_together():
    with pytest.raises(ConfigError) as info:
        load({"A": Var(str), "B": Var(int, 1), "C": Var(bool, False)}, {"B": "x", "C": "maybe"})
    assert len(info.value.problems) == 3
    assert any(p.startswith("A is required") for p in info.value.problems)


def test_falls_back_to_os_environ(monkeypatch):
    monkeypatch.setenv("ENVCONFIG_TEST_PORT", "1234")
    assert load({"ENVCONFIG_TEST_PORT": Var(int)})["ENVCONFIG_TEST_PORT"] == 1234


def test_default_may_be_none():
    assert load({"X": Var(str, None)}, {})["X"] is None
