#!/usr/bin/env python3
"""Lightweight environment smoke checks for hiprfish-plb.

Pure stdlib by design.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


def _check_path(path: Path, label: str) -> tuple[bool, str]:
    ok = path.exists()
    status = "OK" if ok else "MISSING"
    return ok, f"[{status}] {label}: {path}"


def _check_command(cmd: str) -> tuple[bool, str]:
    resolved = shutil.which(cmd)
    ok = resolved is not None
    status = "OK" if ok else "MISSING"
    where = resolved if resolved else "<not found in PATH>"
    return ok, f"[{status}] command `{cmd}` -> {where}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Check runtime prerequisites")
    parser.add_argument("--repo-root", default=".", help="Path to repository root")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return non-zero if optional external tools are missing",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    print(f"[INFO] repo root: {repo_root}")
    print(f"[INFO] python: {sys.version.split()[0]}")

    required_paths = [
        repo_root / "README.md",
        repo_root / "probe-design",
        repo_root / "image-analysis",
        repo_root / "docs" / "WORKFLOW_CONTRACTS.md",
    ]

    required_cmds = ["python3"]
    recommended_cmds = ["snakemake", "blastn", "primer3_core", "usearch"]

    hard_failures = 0
    soft_failures = 0

    print("[INFO] required paths")
    for path in required_paths:
        ok, msg = _check_path(path, "path")
        print(msg)
        if not ok:
            hard_failures += 1

    print("[INFO] required commands")
    for cmd in required_cmds:
        ok, msg = _check_command(cmd)
        print(msg)
        if not ok:
            hard_failures += 1

    print("[INFO] recommended external commands")
    for cmd in recommended_cmds:
        ok, msg = _check_command(cmd)
        print(msg)
        if not ok:
            soft_failures += 1

    if hard_failures > 0:
        print(f"[FAIL] hard failures: {hard_failures}")
        return 2

    if args.strict and soft_failures > 0:
        print(f"[FAIL] missing recommended commands in strict mode: {soft_failures}")
        return 3

    if soft_failures > 0:
        print(f"[WARN] missing recommended commands: {soft_failures}")
    else:
        print("[OK] all recommended commands available")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
