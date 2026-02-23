# Workflow Contracts Baseline

This document captures non-negotiable workflow contracts in `hiprfish-plb`.
It is the baseline guardrail for modular refactors.

## Purpose

- Preserve existing Snakemake behavior while refactoring internals.
- Explicitly document file naming/path contracts, marker contracts, and schema assumptions.
- Provide smoke-check entrypoints to detect contract drift early.

## Hard Contract Invariants

These are treated as compatibility contracts unless a migration plan is provided.

- Output naming/path patterns produced by Snakefile rules.
- Marker files used as pipeline checkpoints (for example `*_complete.txt`).
- CSV/HDF data contracts consumed by downstream scripts.
- CLI argument contracts from Snakefile `shell:` invocations.

## Workflows Covered (Step 1 baseline)

Primary scope for this baseline:

1. `probe-design/hiprfish-probe-design-molecule/Snakefile`
2. `probe-design/hiprfish-probe-design-consensus/Snakefile`
3. `image-analysis/hiprfish-image-analysis-ecoli/Snakefile`
4. `image-analysis/hiprfish-image-analysis-microbiome-gut/Snakefile`

Additional mapped workflows (secondary baseline):

- `image-analysis/hiprfish-image-analysis-microbiome-oral/Snakefile`
- `image-analysis/hiprfish-image-analysis-synthetic-community/Snakefile`
- `image-analysis/hiprfish-image-analysis-ecoli-snr/Snakefile`
- `image-analysis/hiprfish-image-analysis-ecoli-spatiospectral-deconvolution/Snakefile`
- `image-analysis/hiprfish-image-analysis-airy/Snakefile`

## Global Contract Notes

- Snakefiles invoke scripts via `config[__default__][SCRIPTS_PATH]`; script path key is required.
- Most workflows are path-sensitive and rely on strict naming templates.
- Several workflows use marker-style files to gate downstream rules.
- Several downstream scripts assume fixed column names (for example `cell_barcode`) and fixed dtypes.

## Contract Registry

### A. Probe Design - Molecule

Reference: `probe-design/hiprfish-probe-design-molecule/Snakefile:221`

Rule chain:

- initialize -> design -> combine -> write -> evaluate_primary -> evaluate_secondary
- select -> add_spacers -> collect_selected_probe_information -> generate_full_probes
- combine_full_length_sequences -> collect_probe_coverage_results

Key outputs and markers:

- `{sample}/log/probe_design_initialization_complete.txt`
- `{sample}/log/probe_design_complete.txt`
- `{sample}/probes_summary/probes_summary.h5`
- `{sample}/probes/probes_write_complete.txt`
- `{sample}/log/{design_level}_probe_evaluation_primary_complete.txt`
- `simulation/{design_id}/probe_evaluation_secondary_complete.txt`
- `simulation/{design_id}/{design_id}_probe_selection_complete.txt`
- `simulation/{design_id}/{design_id}_probe_spacer_addition_complete.txt`
- `simulation/{design_id}/taxon_best_probes_filtered.csv`
- `simulation/{design_id}/taxon_best_probes_summary.csv`
- `simulation/{design_id}/{design_id}_full_length_probes_sequences.txt`
- `simulation/{design_id}/{design_id}_full_length_blocking_probes_sequences.txt`
- `simulation/{design_id}/{design_id}_full_length_helper_probes_sequences.txt`
- `simulation/{design_id}/{design_id}_complex_oligo_pool.txt`

CLI contract examples from Snakefile shell blocks:

- `hiprfish_design_probes.py {primer3_dir} {primer3_exec_dir} -n_workers {n_workers}`
- `hiprfish_select_probes.py {design_level_evaluation_dir} {design_id} {design_dir} -n_workers ...`
- `hiprfish_generate_full_probes.py {design_dir} {utilities_dir} {evaluation_dir} ...`

Schema-sensitive assumptions:

- `probes_summary.h5` key layout is consumed by `hiprfish_write_probes.py`.
- Probe-selection CSV and summary CSV are consumed downstream by full-probe generation and result collection.

### B. Probe Design - Consensus

Reference: `probe-design/hiprfish-probe-design-consensus/Snakefile:279`

Rule chain:

- design_probes -> blast_probes -> evaluate_taxon_probes -> select_taxon_probes
- add_spacers -> collect_selected_probe_information -> generate_full_probes
- combine_full_length_sequences -> collect_probe_coverage_results

Key outputs and markers:

- `{sample}/{target_rank}/s_{similarity}/primer3/{taxon}_consensus.int`
- `{sample}/{target_rank}/s_{similarity}/primer3/{taxon}.probe.blast.complete.txt`
- `{sample}/{target_rank}/s_{similarity}/blast/{taxon}.probe.evaluation.complete.txt`
- `simulation/{design_id}/{taxon}_probe_selection.csv`
- `simulation/{design_id}/{taxon}_probe_selection_sa.csv`
- `simulation/{design_id}/taxon_best_probes.csv`
- `simulation/{design_id}/taxon_best_probes_filtered.csv`
- `simulation/{design_id}/taxon_best_probes_summary.csv`
- `simulation/{design_id}/{design_id}_complex_oligo_pool.txt`
- final `{simulation_table}_results.csv`

Schema-sensitive assumptions:

- Taxon best probe CSVs are merged with cluster lookup and consumed by follow-up summarization.
- Full-length sequence TXT files are consumed by final coverage summarization.

### C. Image Analysis - E.coli

Reference: `image-analysis/hiprfish-image-analysis-ecoli/Snakefile:72`

Rule chain:

- measure_reference_image -> classify_images -> collect_measurement_results

Key outputs:

- `{folder}/{sample}_avgint.csv`
- `{folder}/{sample}_avgint_norm.csv`
- `{folder}/{sample}_seg.npy`
- `{folder}/{sample}_seg.png`
- `{folder}/{sample}_avgint_ids_replicate_29.csv`
- final `{input_image_list}_results.csv`

CLI contract examples:

- `hiprfish_imaging_spectral_image_measurement.py -i ... -c ... -cf ...`
- `hiprfish_imaging_image_classification.py {input_spectrum} -rf ... -b ... -bs ...`

Schema-sensitive assumptions:

- Collector script consumes per-image avgint outputs and image list table.
- Replicate suffix in output naming is embedded in workflow (`replicate_29`).

### D. Image Analysis - Microbiome Gut

Reference: `image-analysis/hiprfish-image-analysis-microbiome-gut/Snakefile:140`

Rule chain:

- measure_image -> classify_spectra -> spatial_analysis

Key outputs:

- `{folder}/{sample}_avgint.csv`
- `{folder}/{sample}_cell_information_consensus.csv`
- `{folder}/{sample}_identification.pdf`

Derived contracts used by spatial scripts:

- `{sample}_cell_information_consensus_filtered.csv`
- `{sample}_adjacency_matrix.csv`
- `{sample}_adjacency_matrix_filtered.csv`
- `{sample}_identification.npy`

Schema-sensitive assumptions:

- `cell_barcode` is expected as string in multiple scripts.
- Spatial analysis expects matched segmentation and adjacency artifacts in same stem namespace.

## Baseline Validation Commands

Dry-run workflow validation (non-destructive):

```bash
snakemake -n --snakefile "probe-design/hiprfish-probe-design-consensus/Snakefile" --configfile "probe-design/hiprfish-probe-design-consensus/hiprfish_config_example.json" -j 1
snakemake -n --snakefile "probe-design/hiprfish-probe-design-molecule/Snakefile" --configfile "probe-design/hiprfish-probe-design-molecule/hiprfish_config_multispecies.json" -j 1
snakemake -n --snakefile "image-analysis/hiprfish-image-analysis-ecoli/Snakefile" --configfile "image-analysis/hiprfish-image-analysis-ecoli/hiprfish_config_imaging.json" -j 1
snakemake -n --snakefile "image-analysis/hiprfish-image-analysis-microbiome-gut/Snakefile" --configfile "image-analysis/hiprfish-image-analysis-microbiome-gut/hiprfish_config_imaging.json" -j 1
```

Smoke checks (added in Commit 1):

```bash
python3 scripts/smoke/check_env.py --repo-root .
python3 scripts/smoke/check_config.py --config "probe-design/hiprfish-probe-design-consensus/hiprfish_config_example.json" --workflow probe_consensus
python3 scripts/smoke/check_config.py --config "probe-design/hiprfish-probe-design-molecule/hiprfish_config_multispecies.json" --workflow probe_molecule
python3 scripts/smoke/check_outputs.py --workflow probe_molecule --mode patterns
python3 scripts/smoke/check_outputs.py --workflow probe_consensus --mode patterns
python3 scripts/smoke/check_outputs.py --workflow image_ecoli --mode patterns
python3 scripts/smoke/check_outputs.py --workflow image_microbiome_gut --mode patterns
python3 scripts/smoke/check_cython.py --repo-root .
```

Cython rebuild/import smoke (executed mode):

```bash
python3 scripts/smoke/check_cython.py --repo-root . --execute --module hiprfish-image-analysis-ecoli
```

## Change Control Rules for Refactor Commits

- Any output-path rename or marker rename requires:
  - explicit migration note,
  - downstream consumer update,
  - dedicated commit.
- Any schema change requires:
  - before/after schema note,
  - compatibility strategy (adapter or migration).
- Default assumption: no output naming/path/schema/marker changes.
