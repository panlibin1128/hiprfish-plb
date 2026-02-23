from __future__ import annotations

import importlib
from pathlib import Path

paths_mod = importlib.import_module("hiprfish_plb.paths")
ensure_parent = paths_mod.ensure_parent
format_contract_path = paths_mod.format_contract_path
is_marker_filename = paths_mod.is_marker_filename


def test_ensure_parent_creates_directory(tmp_path: Path) -> None:
    target = tmp_path / "a" / "b" / "result.csv"
    ensure_parent(target)
    assert target.parent.exists()


def test_format_contract_path_formats_values() -> None:
    path = format_contract_path("{data_dir}/simulation/{design_id}/out.csv", data_dir="/d", design_id="D1")
    assert path == "/d/simulation/D1/out.csv"


def test_format_contract_path_raises_on_missing_value() -> None:
    raised = False
    try:
        format_contract_path("{a}/{b}", a="x")
    except ValueError:
        raised = True
    assert raised


def test_is_marker_filename() -> None:
    assert is_marker_filename("probe_design_complete.txt")
    assert not is_marker_filename("taxon_best_probes.csv")
