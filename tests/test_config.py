from __future__ import annotations

import importlib
from pathlib import Path

config_mod = importlib.import_module("hiprfish_plb.config")
ConfigContractError = config_mod.ConfigContractError
load_config_json = config_mod.load_config_json
require_profile = config_mod.require_profile
validate_profile = config_mod.validate_profile


def test_load_config_supports_trailing_comma(tmp_path: Path) -> None:
    config_file = tmp_path / "config.json"
    config_file.write_text('{"__default__": {"SCRIPTS_PATH": "x",},}', encoding="utf-8")
    config = load_config_json(config_file)
    assert config["__default__"]["SCRIPTS_PATH"] == "x"


def test_validate_profile_reports_missing_keys() -> None:
    config = {"__default__": {"SCRIPTS_PATH": "a"}, "simulations": {"simulation_table": "x.csv"}}
    missing = validate_profile(config, "probe_molecule")
    assert "missing key `__default__.DATA_DIR`" in missing
    assert "missing section `blast`" in missing


def test_require_profile_raises_on_missing() -> None:
    config = {"__default__": {"SCRIPTS_PATH": "a", "DATA_DIR": "b"}}
    raised = False
    try:
        require_profile(config, "image_ecoli")
    except ConfigContractError:
        raised = True
    assert raised


def test_require_profile_passes_for_minimum_probe_molecule() -> None:
    config = {
        "__default__": {"SCRIPTS_PATH": "a", "DATA_DIR": "b", "N_WORKERS": 1},
        "blast": {"16s_db": "db"},
        "primer3": {"primer3_exec_dir": "primer3"},
        "simulations": {"simulation_table": "sim.csv"},
    }
    require_profile(config, "probe_molecule")
