#!/usr/bin/env python3
"""Output contract smoke checker for hiprfish-plb workflows.

Modes:
- patterns: print expected naming contracts (no filesystem dependency)
- exists: verify at least one file exists per pattern under --data-dir
"""

from __future__ import annotations

import argparse
import glob
from pathlib import Path


PATTERNS = {
    "probe_molecule": [
        "{data_dir}/*/log/probe_design_initialization_complete.txt",
        "{data_dir}/*/log/probe_design_complete.txt",
        "{data_dir}/*/probes_summary/probes_summary.h5",
        "{data_dir}/*/probes/probes_write_complete.txt",
        "{data_dir}/simulation/*/probe_evaluation_secondary_complete.txt",
        "{data_dir}/simulation/*/*_probe_selection_complete.txt",
        "{data_dir}/simulation/*/*_probe_spacer_addition_complete.txt",
        "{data_dir}/simulation/*/taxon_best_probes_filtered.csv",
        "{data_dir}/simulation/*/*_full_length_probes_sequences.txt",
    ],
    "probe_consensus": [
        "{data_dir}/*/*/s_*/primer3/*_consensus.int",
        "{data_dir}/*/*/s_*/primer3/*.probe.blast.complete.txt",
        "{data_dir}/*/*/s_*/blast/*.probe.evaluation.complete.txt",
        "{data_dir}/simulation/*/*_probe_selection.csv",
        "{data_dir}/simulation/*/*_probe_selection_sa.csv",
        "{data_dir}/simulation/*/taxon_best_probes.csv",
        "{data_dir}/simulation/*/*_complex_oligo_pool.txt",
    ],
    "image_ecoli": [
        "{data_dir}/*/*_avgint.csv",
        "{data_dir}/*/*_avgint_norm.csv",
        "{data_dir}/*/*_seg.npy",
        "{data_dir}/*/*_seg.png",
        "{data_dir}/*/*_avgint_ids_replicate_29.csv",
    ],
    "image_microbiome_gut": [
        "{data_dir}/*/*_avgint.csv",
        "{data_dir}/*/*_cell_information_consensus.csv",
        "{data_dir}/*/*_cell_information_consensus_filtered.csv",
        "{data_dir}/*/*_adjacency_matrix.csv",
        "{data_dir}/*/*_identification.pdf",
    ],
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Check workflow output contracts")
    parser.add_argument(
        "--workflow",
        required=True,
        choices=sorted(PATTERNS),
        help="Workflow output contract profile",
    )
    parser.add_argument(
        "--mode",
        default="patterns",
        choices=["patterns", "exists"],
        help="patterns prints expected paths, exists validates filesystem",
    )
    parser.add_argument(
        "--data-dir",
        default=".",
        help="Base data directory used to resolve wildcard patterns",
    )
    args = parser.parse_args()

    data_dir = str(Path(args.data_dir).resolve())
    patterns = [p.format(data_dir=data_dir) for p in PATTERNS[args.workflow]]

    print(f"[INFO] workflow={args.workflow}")
    print(f"[INFO] mode={args.mode}")

    if args.mode == "patterns":
        for p in patterns:
            print(f"[PATTERN] {p}")
        print("[OK] printed output contract patterns")
        return 0

    failures = 0
    for p in patterns:
        matches = glob.glob(p)
        if matches:
            print(f"[OK] {p} -> {len(matches)} match(es)")
        else:
            print(f"[MISS] {p}")
            failures += 1

    if failures:
        print(f"[FAIL] missing patterns: {failures}")
        return 5
    print("[OK] all patterns matched at least one file")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
