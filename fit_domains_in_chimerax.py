#!/usr/bin/env python3
# # -*- coding: utf-8 -*-

"""
@Authors Max Tong & Huy Bui
"""

import sys, os, time
from shutil import which
from datetime import datetime
import subprocess, multiprocessing
from tqdm import tqdm
import pandas as pd


script_dir = os.path.dirname(os.path.realpath(__file__))

def print_usage():
    print("usage: fit_domains_in_chimerax.py inputDir outputDir inputMap mapLevel resolution searchNo noProcessor")
    print("eg: fit_domains_in_chimerax.py single_domains solutions ref.mrc 0.0394 5 200 10")
    sys.exit()
    
def execute(cmd):
    # Redirecting stdout and stderr to DEVNULL keeps the tqdm bar from being broken by logs
    return subprocess.call(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == "__main__":
    if len(sys.argv) < 7:
        print_usage()

    pdb_dir = sys.argv[1]
    output_dir = sys.argv[2]
    input_map = sys.argv[3]
    map_level = sys.argv[4]
    resolution = sys.argv[5]
    search = sys.argv[6]

    threads = int(sys.argv[7]) if len(sys.argv) > 7 else 10
    
    # Platform Setup
    useMacOs = 1 if sys.platform == 'darwin' else 0
    chimerax_path = "/Applications/ChimeraX-1.10.1.app/Contents/MacOS/ChimeraX" if useMacOs == 1 else "chimerax"
    
    if os.path.exists(chimerax_path) == 0 and which(chimerax_path) is None:
        print(f"Error: ChimeraX not found at {chimerax_path}")
        exit(0)
    
    os.makedirs(output_dir, exist_ok=True)

    # Initialize Log
    log_file = os.path.join(output_dir, 'fit_logs.txt')
    with open(log_file, "w") as log:
        log.write("\nDomain, NoRes, Best_Corr, Second_Best_Corr, Diff, Worst_Corr, Range, P_val_best_fit, Corr_about_mean, Eta0, Pvalue, BH_adjusted_Pvalue\n")

    # Build the list of commands based on PDB/CIF files
    cmds = []
    for pdb in os.listdir(pdb_dir):
        if pdb.endswith((".pdb", ".cif")):
            cmds.append(f'{chimerax_path} --nogui --offscreen --cmd \"runscript {script_dir}/fit_in_chimerax.py {pdb_dir}/{pdb} {output_dir} {input_map} {map_level} {resolution} {search}" --exit')

    # --- Multiprocessing with tqdm Progress Bar ---
    print(f"Processing {len(cmds)} domains across {threads} threads...")
    
    with multiprocessing.Pool(processes=threads) as pool:
        # pool.imap_unordered yields results as soon as they finish
        # list() is used to consume the iterator so the pool finishes
        list(tqdm(
            pool.imap_unordered(execute, cmds), 
            total=len(cmds), 
            desc="Fitting Domains", 
            unit="pdb"
        ))

    # Data Analysis
    try:
        df = pd.read_csv(log_file, sep='\s*,\s*', engine='python')
        df.dropna(inplace=True)
        df.sort_values(['BH_adjusted_Pvalue', 'Corr_about_mean'], ascending=[True, False], inplace=True)
        df.to_csv(os.path.join(output_dir, 'fit_logs_revised.csv'), index=False)
        print(f"\nSuccess! Revised log created in {output_dir}")
    except Exception as e:
        print(f"\nNote: Could not process pandas summary (likely no data written to log yet): {e}")