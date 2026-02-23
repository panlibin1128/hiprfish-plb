from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


def require_columns(df: pd.DataFrame, columns: list[str], context: str) -> None:
    missing = [col for col in columns if col not in df.columns]
    if missing:
        missing_text = ", ".join(missing)
        raise KeyError(f"{context} missing columns: {missing_text}")


def resolve_design_context(sim_tab: pd.DataFrame, design_id: str) -> dict[str, Any]:
    require_columns(sim_tab, ["DESIGN_ID", "SAMPLE", "TARGET_RANK"], "simulation table")
    matched = sim_tab[sim_tab.DESIGN_ID == design_id]
    if matched.shape[0] == 0:
        raise KeyError(f"design id not found: {design_id}")
    row = matched.iloc[0]
    context: dict[str, Any] = {
        "sample": row["SAMPLE"],
        "target_rank": row["TARGET_RANK"],
    }
    if "SIMILARITY" in matched.columns:
        context["similarity"] = row["SIMILARITY"]
    return context


def read_probe_selection_tables(design_directory: str | Path) -> pd.DataFrame:
    root = Path(design_directory)
    files = sorted(root.glob("*_probe_selection.csv"))
    if not files:
        raise FileNotFoundError(f"no probe selection files under {root}")
    tables: list[pd.DataFrame] = []
    for filename in files:
        df = pd.read_csv(filename)
        require_columns(df, ["quality"], f"probe selection file {filename}")
        tables.append(df.sort_values(by=["quality"], ascending=True))
    return pd.concat(tables).sort_values(by=["quality"], ascending=True)


def load_image_table(path: str | Path) -> pd.DataFrame:
    image_tab = pd.read_csv(path)
    require_columns(image_tab, ["SAMPLE", "IMAGES"], "image table")
    return image_tab


def load_required_csv(path: str | Path, context: str) -> pd.DataFrame:
    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(f"{context} file not found: {csv_path}")
    return pd.read_csv(csv_path)
