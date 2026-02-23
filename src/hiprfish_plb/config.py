from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


class ConfigContractError(ValueError):
    pass


PROFILE_KEYS: dict[str, dict[str, list[str]]] = {
    "probe_consensus": {
        "__default__": ["SCRIPTS_PATH", "DATA_DIR"],
        "blast": ["16s_db"],
        "primer3": ["primer3_exec_dir", "primer3_config_dir"],
        "usearch": ["usearch_dir"],
        "simulations": ["simulation_table"],
    },
    "probe_molecule": {
        "__default__": ["SCRIPTS_PATH", "DATA_DIR", "N_WORKERS"],
        "blast": ["16s_db"],
        "primer3": ["primer3_exec_dir"],
        "simulations": ["simulation_table"],
    },
    "image_ecoli": {
        "__default__": ["SCRIPTS_PATH", "DATA_DIR"],
        "images": ["image_list_table"],
    },
    "image_microbiome_gut": {
        "__default__": ["SCRIPTS_PATH", "DATA_DIR", "PROBE_DESIGN_DIR"],
        "images": ["image_list_table"],
    },
}


def load_config_json(path: str | Path) -> dict[str, Any]:
    config_path = Path(path)
    raw = config_path.read_text(encoding="utf-8")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        sanitized = re.sub(r",\s*([}\]])", r"\1", raw)
        return json.loads(sanitized)


def validate_profile(config: dict[str, Any], profile: str) -> list[str]:
    if profile not in PROFILE_KEYS:
        return [f"unknown profile `{profile}`"]
    missing: list[str] = []
    for section, keys in PROFILE_KEYS[profile].items():
        section_obj = config.get(section)
        if not isinstance(section_obj, dict):
            missing.append(f"missing section `{section}`")
            continue
        for key in keys:
            if key not in section_obj:
                missing.append(f"missing key `{section}.{key}`")
    return missing


def require_profile(config: dict[str, Any], profile: str) -> None:
    missing = validate_profile(config, profile)
    if missing:
        raise ConfigContractError("; ".join(missing))
