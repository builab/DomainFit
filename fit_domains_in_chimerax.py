#!/usr/bin/env python3
import sys, os, time, subprocess, multiprocessing
import pandas as pd
from tqdm import tqdm

def execute(cmd):
    """Executes the ChimeraX command and returns results."""
    process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return process.returncode, process.stderr

if __name__ == "__main__":
    if len(sys.argv) < 7:
        print("Usage: fit_domains_in_chimerax.py inputDir outputDir inputMap mapLevel resolution searchNo noProcessor")
        sys.exit()

    pdb_dir, output_dir, input_map, map_level, resolution, search = sys.argv[1:7]
    threads = int(sys.argv[7]) if len(sys.argv) > 7 else 10
    script_dir = os.path.dirname(os.path.realpath(__file__))
    chimerax_path = "/Applications/ChimeraX-1.10.1.app/Contents/MacOS/ChimeraX" if sys.platform == 'darwin' else "chimerax"
    
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    temp_logs_dir = os.path.join(output_dir, "temp_logs")
    os.makedirs(temp_logs_dir, exist_ok=True)

    # 1. Build Commands
    cmds = []
    files = [f for f in os.listdir(pdb_dir) if f.endswith((".pdb", ".cif"))]
    for pdb in files:
        temp_log = os.path.join(temp_logs_dir, f"{pdb}.log")
        cmds.append(f'{chimerax_path} --nogui --offscreen --cmd "runscript {script_dir}/fit_in_chimerax.py {pdb_dir}/{pdb} {output_dir} {input_map} {map_level} {resolution} {search} {temp_log}" --exit')

    # 2. Run Pool with tqdm
    print(f"Starting fitting for {len(cmds)} files using {threads} threads...")
    with multiprocessing.Pool(processes=threads) as pool:
        for res_code, res_err in tqdm(pool.imap_unordered(execute, cmds), total=len(cmds), desc="Fitting Progress"):
            if res_code != 0:
                # If a worker fails, print the error to help with troubleshooting
                print(f"\nWorker Error detected for a file:\n{res_err}")

    # 3. Merge and Data Aggregation
    all_rows = []
    print("\nCompiling logs and cleaning formatting...")
    
    for log_name in os.listdir(temp_logs_dir):
        part_path = os.path.join(temp_logs_dir, log_name)
        with open(part_path, "r") as f_in:
            raw_data = f_in.read().strip()
            if not raw_data:
                continue
            
            parts = raw_data.split(',')
            if len(parts) < 8:
                continue
            
            pval_csv = parts[7]
            if os.path.exists(pval_csv):
                try:
                    p_df = pd.read_csv(pval_csv, sep='\s*,\s*', engine='python').dropna()

                    # Select the row with the best (lowest) BH_adjusted_Pvalue
                    # Column index 41 = BH_adjusted_Pvalue
                    best_idx = p_df.iloc[:, 41].astype(float).idxmin()
                    best_row = p_df.loc[best_idx]

                    # CLEANING: Strip extra quotes from the R output if they exist
                    p_val_raw = str(best_row.iloc[0]).replace('"', '').replace("'", "")
                    
                    row = {
                        "Domain": parts[0],
                        "NoRes": int(parts[1]),
                        "Best_Corr": float(parts[2]),
                        "Second_Best_Corr": float(parts[3]),
                        "Diff": float(parts[4]),
                        "Worst_Corr": float(parts[5]),
                        "Range": float(parts[6]),
                        "P_val_best_fit": p_val_raw,  # Cleaned value
                        "Corr_about_mean": best_row.iloc[26],
                        "Eta0": best_row.iloc[39],
                        "Pvalue": best_row.iloc[38],
                        "BH_adjusted_Pvalue": best_row.iloc[41]
                    }
                    all_rows.append(row)
                except Exception as e:
                    print(f"Data error for {parts[0]}: {e}")
        
        os.remove(part_path)

    if os.path.exists(temp_logs_dir):
        os.rmdir(temp_logs_dir)

    # 4. Save Final Output Files
    if all_rows:
        df = pd.DataFrame(all_rows)
        
        # Define common CSV settings to prevent double-quoting
        import csv
        csv_settings = {
            "index": False,
            "quoting": csv.QUOTE_MINIMAL # Only quote if strictly necessary
        }

        # Save raw fit_logs.txt
        log_file = os.path.join(output_dir, 'fit_logs.txt')
        df.to_csv(log_file, **csv_settings)
        
        # Save sorted fit_logs_revised.csv
        df.sort_values(['BH_adjusted_Pvalue', 'Corr_about_mean'], ascending=[True, False], inplace=True)
        revised_file = os.path.join(output_dir, 'fit_logs_revised.csv')
        df.to_csv(revised_file, **csv_settings)
        
        print(f"\nProcessing complete! Cleaned records saved to {revised_file}")