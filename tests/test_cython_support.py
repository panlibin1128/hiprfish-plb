from __future__ import annotations

import importlib
from pathlib import Path


def test_discover_cython_modules_finds_setup_dirs(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    module_dir = root / "image-analysis" / "mod-a"
    module_dir.mkdir(parents=True)
    (module_dir / "setup.py").write_text("setup()", encoding="utf-8")
    (module_dir / "neighbor2d.pyx").write_text("", encoding="utf-8")

    cython_support = importlib.import_module("hiprfish_plb.cython_support")
    modules = cython_support.discover_cython_modules(root)

    assert len(modules) == 1
    assert modules[0].name == "mod-a"
    assert modules[0].setup_path == module_dir / "setup.py"
    assert modules[0].pyx_files == [module_dir / "neighbor2d.pyx"]


def test_discover_cython_modules_ignores_hidden_dirs(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    good_dir = root / "image-analysis" / "mod-a"
    good_dir.mkdir(parents=True)
    (good_dir / "setup.py").write_text("setup()", encoding="utf-8")
    (good_dir / "neighbor2d.pyx").write_text("", encoding="utf-8")

    hidden_dir = root / ".venv" / "x"
    hidden_dir.mkdir(parents=True)
    (hidden_dir / "setup.py").write_text("setup()", encoding="utf-8")
    (hidden_dir / "neighbor2d.pyx").write_text("", encoding="utf-8")

    cython_support = importlib.import_module("hiprfish_plb.cython_support")
    modules = cython_support.discover_cython_modules(root)
    names = [m.name for m in modules]
    assert names == ["mod-a"]


def test_build_commands_contains_build_and_import() -> None:
    cython_support = importlib.import_module("hiprfish_plb.cython_support")
    module = cython_support.CythonModuleInfo(
        name="demo",
        module_dir=Path("/tmp/demo"),
        setup_path=Path("/tmp/demo/setup.py"),
        pyx_files=[Path("/tmp/demo/neighbor2d.pyx")],
    )
    build_cmd, import_cmd = cython_support.build_commands(module)
    assert "python3 setup.py build_ext --inplace" in build_cmd
    assert "import neighbor2d" in import_cmd
