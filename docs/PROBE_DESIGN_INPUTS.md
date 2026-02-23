# Probe Design Inputs (Consensus + Molecule)

This guide explains what files you must prepare before running probe-design workflows.
It is a practical checklist aligned with current Snakefiles and script contracts.

## 1) Choose Workflow

- Consensus workflow:
  - `probe-design/hiprfish-probe-design-consensus/Snakefile`
- Molecule workflow:
  - `probe-design/hiprfish-probe-design-molecule/Snakefile`

Both consume a config JSON and a simulation table CSV.

## 2) Config JSON Requirements

### 2.1 Consensus config

Reference file:

- `probe-design/hiprfish-probe-design-consensus/hiprfish_config_example.json`

Required keys:

- `__default__.SCRIPTS_PATH`
- `__default__.DATA_DIR`
- `blast.16s_db`
- `primer3.primer3_exec_dir`
- `primer3.primer3_config_dir`
- `usearch.usearch_dir`
- `simulations.simulation_table`

### 2.2 Molecule config

Reference file:

- `probe-design/hiprfish-probe-design-molecule/hiprfish_config_multispecies.json`

Required keys:

- `__default__.SCRIPTS_PATH`
- `__default__.DATA_DIR`
- `__default__.N_WORKERS`
- `blast.16s_db`
- `primer3.primer3_exec_dir`
- `simulations.simulation_table`
- `plotting.theme_color`

## 3) simulation_table CSV Requirements

Template reference:

- `probe-design/example/simulation_table_example.csv`

Recommended required columns (safe for both workflows):

- `DESIGN_ID`
- `SAMPLE`
- `TARGET_RANK`
- `SIMILARITY`
- `MAX_CONTINUOUS_HOMOLOGY`
- `MIN_TM`
- `MAX_TM`
- `GC`
- `INCLUDE_START`
- `INCLUDE_END`
- `PROBE_SELECTION_METHOD`
- `PRIMERSET`
- `OTU`
- `TPN`
- `FREQLL`
- `BOT`
- `BITSCORE_THRESH`
- `BARCODESELECTION`
- `BPLC`
- `HELPER_PROBE_REPEAT`
- `SOD`
- `DNACONC`
- `MT_CUTOFF`
- `OT_GC_CUTOFF`
- `THEMECOLOR`

Notes:

- `DESIGN_ID` must be unique per row.
- `SAMPLE` must match your fasta file basename.
- Keep numeric fields as numeric values (no text suffixes).

## 4) Required Input FASTA Layout

For each `SAMPLE` in simulation table:

- Place file at:
  - `DATA_DIR/<SAMPLE>/input/<SAMPLE>.fasta`

Example:

- `DATA_DIR/test_sample/input/test_sample.fasta`

This path is hardcoded by helper functions in both Snakefiles.

## 5) External Tool Inputs

You also need these external resources available in config paths:

- NCBI 16S BLAST database (`blast.16s_db`)
- primer3 executable (`primer3_exec_dir`)
- primer3 config dir (consensus workflow)
- usearch executable (consensus workflow)

## 6) Output Contract (Do Not Rename)

The workflows depend on stable naming and markers. Do not rename these casually:

- `*_probe_evaluation_complete.txt`
- `taxon_best_probes.csv`
- `taxon_best_probes_filtered.csv`
- `taxon_best_probes_summary.csv`
- `*_complex_oligo_pool.txt`
- `<simulation_table>_results.csv`

See also:

- `docs/WORKFLOW_CONTRACTS.md`

## 7) Dry-Run Commands

Run these first to validate wiring before full execution.

Consensus:

```bash
snakemake -n --snakefile "probe-design/hiprfish-probe-design-consensus/Snakefile" --configfile "probe-design/hiprfish-probe-design-consensus/hiprfish_config_example.json" -j 1
```

Molecule:

```bash
snakemake -n --snakefile "probe-design/hiprfish-probe-design-molecule/Snakefile" --configfile "probe-design/hiprfish-probe-design-molecule/hiprfish_config_multispecies.json" -j 1
```

## 8) Quick Preflight Checklist

- Config JSON exists and absolute paths are valid.
- `simulation_table` path in config exists.
- All required columns exist in simulation table.
- Every `SAMPLE` has `DATA_DIR/SAMPLE/input/SAMPLE.fasta`.
- BLAST/primer3/usearch binaries are available.
- Dry-run (`snakemake -n`) succeeds.
