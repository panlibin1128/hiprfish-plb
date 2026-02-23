"""
Collect HiPRFISH probe design results
Hao Shi 2017
"""

import argparse
import importlib
import os
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

workflow_io = importlib.import_module("hiprfish_plb.workflow_io")
read_probe_selection_tables = workflow_io.read_probe_selection_tables
require_columns = workflow_io.require_columns
resolve_design_context = workflow_io.resolve_design_context

###############################################################################################################
# HiPR-FISH : collect probe design results
###############################################################################################################

def collect_taxon_best_probes(design_directory, sim_input_filename, taxon_best_probes_filtered_filename, output_probes_summary_filename, bot):
    simulation_directory, design_id = os.path.split(design_directory)
    sim_tab = pd.read_csv(sim_input_filename)
    resolve_design_context(sim_tab, design_id)
    best_probes_df = read_probe_selection_tables(design_directory)
    require_columns(best_probes_df, ["blast_on_target_rate", "target_taxon"], "probe selections")
    best_probes_filtered = best_probes_df[best_probes_df['blast_on_target_rate'] > bot]
    best_probes_filtered_summary = pd.Series(best_probes_filtered["target_taxon"]).value_counts()
    best_probes_filtered.to_csv(taxon_best_probes_filtered_filename, index = False)
    best_probes_filtered_summary.to_csv(output_probes_summary_filename)
    return

###############################################################################################################
# main function
###############################################################################################################

def main():
    parser = argparse.ArgumentParser('Collect summary statistics of HiPRFISH probes for a complex microbial community')

    # data directory
    parser.add_argument('design_directory', type = str, help = 'Directory of the data files')

    # input simulation table
    parser.add_argument('sim_input_filename', type = str, help = 'Input csv table containing simulation information')

    # output simulation results table
    parser.add_argument('taxon_best_probes_filtered_filename', type = str, help = 'Output csv table containing simulation results')

    # output simulation results table
    parser.add_argument('output_probes_summary_filename', type = str, help = 'Output csv table containing simulation results')

    parser.add_argument('bot', type = float, help = 'Output csv table containing simulation results')

    args = parser.parse_args()

    collect_taxon_best_probes(args.design_directory, args.sim_input_filename, args.taxon_best_probes_filtered_filename, args.output_probes_summary_filename, args.bot)

if __name__ == '__main__':
    main()
