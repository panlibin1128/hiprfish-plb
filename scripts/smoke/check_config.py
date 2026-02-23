#!/usr/bin/env python3
"""Validate minimal workflow config contracts for hiprfish-plb.

Pure stdlib by design.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


WORKFLOW_KEYS = {
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
        "images": ["image_list_table", "image_type"],
        "background": ["bkg_spec_filename"],
    },
    "image_microbiome_gut": {
        "__default__": ["SCRIPTS_PATH", "DATA_DIR", "PROBE_DESIGN_DIR"],
        "images": ["image_list_table"],
    },
}


def _validate(config: dict[str, object], workflow: str) -> list[str]:
    issues: list[str] = []
    expected = WORKFLOW_KEYS[workflow]
    for section, keys in expected.items():
        section_value = config.get(section)
        if not isinstance(section_value, dict):
            issues.append(f"missing section `{section}`")
            continue
        section_dict: dict[str, object] = section_value
        for key in keys:
            if key not in section_dict:
                issues.append(f"missing key `{section}.{key}`")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate config key contracts")
    parser.add_argument("--config", required=True, help="Path to config JSON")
    parser.add_argument(
        "--workflow",
        required=True,
        choices=sorted(WORKFLOW_KEYS),
        help="Workflow contract profile",
    )
    args = parser.parse_args()

    config_path = Path(args.config).resolve()
    if not config_path.exists():
        print(f"[FAIL] config not found: {config_path}")
        return 2

    try:
        raw = config_path.read_text(encoding="utf-8")
        config = json.loads(raw)
    except json.JSONDecodeError as exc:
        raw = config_path.read_text(encoding="utf-8")
        sanitized = re.sub(r",\s*([}\]])", r"\1", raw)
        try:
            config = json.loads(sanitized)
            print(f"[WARN] parsed {config_path} with trailing-comma fallback")
        except json.JSONDecodeError:
            print(f"[FAIL] invalid JSON: {config_path}: {exc}")
            return 3

    issues = _validate(config, args.workflow)
    if issues:
        print(f"[FAIL] workflow={args.workflow} config={config_path}")
        for issue in issues:
            print(f" - {issue}")
        return 4

    print(f"[OK] workflow={args.workflow} config={config_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
