from __future__ import annotations

import importlib

cli_mod = importlib.import_module("hiprfish_plb.cli_compat")
parse_common_args = cli_mod.parse_common_args


def test_cli_supports_legacy_n_workers_flag() -> None:
    args = parse_common_args(["-n_workers", "8"])
    assert args.n_workers == 8


def test_cli_supports_new_n_workers_alias() -> None:
    args = parse_common_args(["--n-workers", "6"])
    assert args.n_workers == 6


def test_cli_parses_probe_selection_flags() -> None:
    args = parse_common_args(["-t", "species", "-tmin", "50", "-tmax", "70", "-m", "14", "-gc", "0.5", "-bot", "0.8", "-bt", "100"])
    assert args.target_rank == "species"
    assert args.min_tm == 50
    assert args.max_tm == 70
    assert args.mch == 14
    assert args.gc == 0.5
    assert args.bot == 0.8
    assert args.bt == 100
