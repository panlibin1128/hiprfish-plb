# AGENTS.md - hiprfish-plb
Guide for coding agents working in this repository.
Use these commands and conventions unless newer local rules override them.

## 1) Current Repository Facts
- Language: Python + Cython.
- Orchestration: Snakemake.
- Top-level packaging metadata: not present (`pyproject.toml` missing).
- Tests: minimal pytest suite present under `tests/`.
- Lint/type config: not present.

## 2) Cursor / Copilot Rules Status
Checked and not found:
- `.cursor/rules/`
- `.cursorrules`
- `.github/copilot-instructions.md`
If any are added later, treat them as higher-priority policy.

## 3) Read These Files First
- `README.md`
- `probe-design/hiprfish-probe-design-consensus/Snakefile`
- `probe-design/hiprfish-probe-design-molecule/Snakefile`
- `image-analysis/*/Snakefile`
- `image-analysis/*/setup.py`
- `probe-design/*/hiprfish_config*.json`
- `image-analysis/*/hiprfish_config_imaging.json`

## 4) Environment Setup (From README)
```bash
conda create -n hiprfish python=3.8
conda activate hiprfish
conda install pandas
conda install -c bioconda primer3 -y
conda install -c anaconda joblib -y
conda install -c anaconda biopython -y
pip install snakemake ete3 SetCoverPy tables openpyxl matplotlib
python -m pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose
```
External dependencies also required:
- `usearch`
- NCBI `blast+`
- local NCBI 16S database path in config JSON

## 5) Build Commands
No unified build exists.
Build Cython in each relevant image-analysis submodule:
```bash
cd image-analysis/hiprfish-image-analysis-ecoli
python3 setup.py build_ext --inplace
```
Repeat for each module containing `setup.py` + `neighbor*.pyx`.

## 6) Pipeline Run Commands
Run from the relevant subproject directory:
```bash
snakemake --configfile hiprfish_config.json -j <N>
```
Dry-run first:
```bash
snakemake -n --configfile hiprfish_config.json -j <N>
```
Repo-root explicit invocation example:
```bash
snakemake --snakefile "probe-design/hiprfish-probe-design-molecule/Snakefile" --configfile "probe-design/hiprfish-probe-design-molecule/hiprfish_config_multispecies.json" -j <N>
```

## 6.1) Smoke Checks (Contract Baseline)

Run these before and after refactor edits that may affect workflow contracts:

```bash
python3 scripts/smoke/check_env.py --repo-root .
python3 scripts/smoke/check_config.py --config "probe-design/hiprfish-probe-design-consensus/hiprfish_config_example.json" --workflow probe_consensus
python3 scripts/smoke/check_config.py --config "probe-design/hiprfish-probe-design-molecule/hiprfish_config_multispecies.json" --workflow probe_molecule
python3 scripts/smoke/check_config.py --config "image-analysis/hiprfish-image-analysis-ecoli/hiprfish_config_imaging.json" --workflow image_ecoli
python3 scripts/smoke/check_config.py --config "image-analysis/hiprfish-image-analysis-microbiome-gut/hiprfish_config_imaging.json" --workflow image_microbiome_gut
python3 scripts/smoke/check_outputs.py --workflow probe_molecule --mode patterns
python3 scripts/smoke/check_outputs.py --workflow probe_consensus --mode patterns
python3 scripts/smoke/check_outputs.py --workflow image_ecoli --mode patterns
python3 scripts/smoke/check_outputs.py --workflow image_microbiome_gut --mode patterns
```

## 7) Single Script Run Commands
Most scripts are standalone CLIs with `argparse`.
Generic pattern:
```bash
python3 path/to/script.py <positional_args> [--flags]
```
Use the exact script call patterns found in the matching `Snakefile` `shell:` blocks.

## 8) Test Commands (Including Single Test)
Current state:
- Minimal pytest unit tests exist for config/path/CLI compatibility layers.
Recommended commands:

```bash
pytest -q
pytest tests/test_config.py::test_require_profile_passes_for_minimum_probe_molecule -q
```

Single-test pattern:

```bash
pytest tests/path/test_file.py::test_case_name -q
```
For workflow-sensitive changes, also validate by:
1. `snakemake -n` on impacted workflow.
2. Running touched script on small representative input.
3. Verifying expected output files/markers exist.

## 9) Lint / Format / Type Commands
No project-standard lint/format/type commands are currently defined.
Agent rules:
- Do not claim lint/type pass unless tooling is added.
- If you add tooling, document exact commands in this file.

## 10) Code Style Guidelines (Observed + Practical)

### Imports
- Keep imports at file top.
- Common imports: `numpy`, `pandas`, `skimage`, `dask`, `Bio.*`.
- In legacy files, avoid import-only refactor churn.

### Formatting
- Legacy style often uses `name = value` spacing.
- `.format(...)` strings are common; `%` formatting appears too.
- Large `########` separators are common in scripts.
- Keep local style when touching old files.

### Naming
- Use `snake_case` for functions, variables, files.
- Preserve established scientific abbreviations (`mch`, `bot`, `tpn`) where used.

### Typing
- Python code is mostly untyped.
- Cython files include typed signatures.
- Do not enforce broad typing retrofits in unrelated edits.

### CLI Structure
- Keep `argparse` pattern.
- Keep `main()` + `if __name__ == '__main__': main()`.
- Preserve existing CLI flag names for compatibility.

### Error Handling
- Existing code has limited explicit exception handling.
- Prefer explicit failure with context to silent swallowing.
- Do not add `except Exception: pass`.

## 11) Workflow Contract Rules
- Workflow dependencies are file-path and filename sensitive.
- Many steps rely on `*_complete.txt` markers.
- CSV/HDF output names are consumed downstream.
Agent rule: do not rename outputs without updating all dependent rules.

## 12) Recommended Agent Execution Loop
1. Identify impacted Snakefile + scripts.
2. Apply smallest safe change.
3. Run `snakemake -n` on impacted workflow.
4. Run touched script with minimal input.
5. Confirm output naming contract still matches downstream usage.
6. Report verified and unverified parts explicitly.
For Cython edits:
1. rebuild with `python3 setup.py build_ext --inplace`.
2. verify module import succeeds in that module directory.

## 13) Avoid By Default
- Full-repo style rewrites.
- Workflow engine migration.
- Output path/schema changes without migration plan.
- Claiming test success when no tests exist.

## 14) Evidence Basis
This guide is derived from repository inspection of:
- `README.md`
- workflow `Snakefile`s in `probe-design/` and `image-analysis/`
- `image-analysis/*/setup.py`
- representative standalone scripts
- absence checks for Cursor/Copilot rule files

## 15) Verification Reporting Format

When reporting validation in PRs or agent updates, include:

- `Verified`: commands actually executed and their status.
- `Unverified`: checks not run (and why), explicitly listed.

Do not claim contract/test/build success without executed evidence.
