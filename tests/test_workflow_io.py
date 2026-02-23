from __future__ import annotations

import importlib
from pathlib import Path

import pandas as pd


def test_require_columns_raises_for_missing_columns() -> None:
    workflow_io = importlib.import_module("hiprfish_plb.workflow_io")
    df = pd.DataFrame({"a": [1], "b": [2]})
    raised = False
    try:
        workflow_io.require_columns(df, ["a", "c"], "sample")
    except KeyError:
        raised = True
    assert raised


def test_resolve_design_context_reads_expected_fields() -> None:
    workflow_io = importlib.import_module("hiprfish_plb.workflow_io")
    sim = pd.DataFrame(
        {
            "DESIGN_ID": ["D1"],
            "SAMPLE": ["S1"],
            "TARGET_RANK": ["species"],
            "SIMILARITY": [97],
        }
    )
    ctx = workflow_io.resolve_design_context(sim, "D1")
    assert ctx["sample"] == "S1"
    assert ctx["target_rank"] == "species"
    assert ctx["similarity"] == 97


def test_read_probe_selection_tables_concatenates_csvs(tmp_path: Path) -> None:
    workflow_io = importlib.import_module("hiprfish_plb.workflow_io")
    first = tmp_path / "111_probe_selection.csv"
    second = tmp_path / "222_probe_selection.csv"
    pd.DataFrame({"quality": [0.2], "blast_on_target_rate": [0.9], "target_taxon": ["A"]}).to_csv(first, index=False)
    pd.DataFrame({"quality": [0.1], "blast_on_target_rate": [0.8], "target_taxon": ["B"]}).to_csv(second, index=False)
    combined = workflow_io.read_probe_selection_tables(tmp_path)
    assert combined.shape[0] == 2
    assert list(combined["quality"].values) == [0.1, 0.2]
