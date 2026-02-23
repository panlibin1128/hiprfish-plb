from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CythonModuleInfo:
    name: str
    module_dir: Path
    setup_path: Path
    pyx_files: list[Path]


def discover_cython_modules(repo_root: str | Path) -> list[CythonModuleInfo]:
    root = Path(repo_root)
    modules: list[CythonModuleInfo] = []
    for setup_path in sorted(root.glob("**/setup.py")):
        if any(part.startswith(".") for part in setup_path.parts):
            continue
        module_dir = setup_path.parent
        pyx_files = sorted(module_dir.glob("*.pyx"))
        if not pyx_files:
            continue
        modules.append(
            CythonModuleInfo(
                name=module_dir.name,
                module_dir=module_dir,
                setup_path=setup_path,
                pyx_files=pyx_files,
            )
        )
    return modules


def build_commands(module: CythonModuleInfo) -> tuple[str, str]:
    pyx_stem = module.pyx_files[0].stem
    build_cmd = "python3 setup.py build_ext --inplace"
    import_cmd = f"python3 -c \"import {pyx_stem}; print('OK')\""
    return build_cmd, import_cmd
