from __future__ import annotations

import argparse
from typing import Sequence


def build_common_parser(prog: str = "hiprfish-compat") -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog=prog)
    parser.add_argument("-n_workers", "--n-workers", dest="n_workers", type=int, default=1)
    parser.add_argument("-t", "--target-rank", dest="target_rank", default=None)
    parser.add_argument("-tmin", "--min-tm", dest="min_tm", type=float, default=None)
    parser.add_argument("-tmax", "--max-tm", dest="max_tm", type=float, default=None)
    parser.add_argument("-m", "--mch", dest="mch", type=float, default=None)
    parser.add_argument("-gc", "--gc", dest="gc", type=float, default=None)
    parser.add_argument("-bot", "--bot", dest="bot", type=float, default=None)
    parser.add_argument("-bt", "--bitscore-threshold", dest="bt", type=float, default=None)
    return parser


def parse_common_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = build_common_parser()
    return parser.parse_args(list(argv))
