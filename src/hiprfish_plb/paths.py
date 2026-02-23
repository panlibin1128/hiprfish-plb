from __future__ import annotations

from pathlib import Path


def ensure_parent(path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    return target


def format_contract_path(template: str, **values: str) -> str:
    try:
        return template.format(**values)
    except KeyError as exc:
        missing = exc.args[0]
        raise ValueError(f"missing template value `{missing}`") from exc


def is_marker_filename(name: str) -> bool:
    return name.endswith("_complete.txt")
