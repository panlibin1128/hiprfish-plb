#!/usr/bin/env python3

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def _load_support(repo_root: Path):
    sys.path.insert(0, str(repo_root / "src"))
    import hiprfish_plb.cython_support as cython_support

    return cython_support


def _run(command: str, cwd: Path) -> int:
    completed = subprocess.run(command, shell=True, cwd=str(cwd), check=False)
    return completed.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Cython rebuild/import smoke checks")
    parser.add_argument("--repo-root", default=".", help="Repository root")
    parser.add_argument("--execute", action="store_true", help="Execute build/import commands")
    parser.add_argument("--module", default=None, help="Only run one module directory name")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    support = _load_support(repo_root)
    modules = support.discover_cython_modules(repo_root)
    if args.module:
        modules = [m for m in modules if m.name == args.module]

    if not modules:
        print("[FAIL] no cython modules found")
        return 2

    print(f"[INFO] found {len(modules)} cython module(s)")
    failures = 0
    for module in modules:
        build_cmd, import_cmd = support.build_commands(module)
        print(f"[MODULE] {module.name}")
        print(f"  dir: {module.module_dir}")
        print(f"  build: {build_cmd}")
        print(f"  import: {import_cmd}")

        if not args.execute:
            continue

        build_rc = _run(build_cmd, module.module_dir)
        if build_rc != 0:
            print(f"  [FAIL] build rc={build_rc}")
            failures += 1
            continue

        import_rc = _run(import_cmd, module.module_dir)
        if import_rc != 0:
            print(f"  [FAIL] import rc={import_rc}")
            failures += 1
        else:
            print("  [OK] build and import")

    if failures:
        print(f"[FAIL] failures: {failures}")
        return 3
    print("[OK] cython smoke check complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
