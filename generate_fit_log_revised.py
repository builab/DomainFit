#!/usr/bin/env python3
"""
Compile fit_logs_revised.csv from all *_pvalues.csv files, joining NoRes
from fit_logs.txt, then sorting by BH_adjusted_Pvalue (asc) and
Corr_about_mean (desc).

Usage:
    python compile_fit_logs.py <pvalues_dir> <output_dir>

Arguments:
    pvalues_dir  Directory containing *_pvalues.csv files
    output_dir   Directory containing fit_logs.txt; revised CSV written here too
"""

import sys
import os
import csv
import glob
import pandas as pd
from tqdm import tqdm


def domain_name_from_path(filepath):
    """Strip _pvalues.csv suffix to get domain name."""
    basename = os.path.basename(filepath)
    for suffix in ("_pvalues.csv", "_pvalue.csv"):
        if basename.lower().endswith(suffix):
            return basename[: -len(suffix)]
    return os.path.splitext(basename)[0]


def clean_val(val):
    """Strip whitespace and stray quotes, then cast to float."""
    return float(str(val).strip().strip('"').strip("'"))


def process_pvalues_file(filepath):
    """
    Read a *_pvalues.csv and return the best-row dict
    (lowest BH_adjusted_pvalues), using named columns.
    """
    try:
        p_df = pd.read_csv(filepath, sep=r'\s*,\s*', engine='python').dropna()

        if p_df.empty:
            print(f"  [WARN] Empty after dropna: {filepath}")
            return None

        # Normalise column names: strip whitespace AND quotes (R output quirk)
        p_df.columns = [c.strip().strip('"').strip("'") for c in p_df.columns]

        required = {"correlation", "correlation_about_mean", "eta0", "pvalues", "bh_adjusted_pvalues"}
        actual   = {c.lower() for c in p_df.columns}
        missing  = required - actual
        if missing:
            print(f"  [WARN] Missing columns {missing} in: {filepath}")
            return None

        # Build lowercase -> original name map for safe access
        col_map = {c.lower(): c for c in p_df.columns}

        # Select the row with the best (lowest) BH_adjusted_pvalues
        bh_col   = col_map["bh_adjusted_pvalues"]
        best_idx = p_df[bh_col].apply(clean_val).idxmin()
        best_row = p_df.loc[best_idx]

        return {
            "Domain":             domain_name_from_path(filepath),
            "Best_Corr":          clean_val(best_row[col_map["correlation"]]),
            "Corr_about_mean":    clean_val(best_row[col_map["correlation_about_mean"]]),
            "Eta0":               clean_val(best_row[col_map["eta0"]]),
            "Pvalue":             clean_val(best_row[col_map["pvalues"]]),
            "BH_adjusted_Pvalue": clean_val(best_row[bh_col]),
        }

    except Exception as exc:
        print(f"  [ERROR] Could not parse {filepath}: {exc}")
        return None


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    pvalues_dir = os.path.abspath(sys.argv[1])
    output_dir  = os.path.abspath(sys.argv[2])

    if not os.path.isdir(pvalues_dir):
        print(f"Error: pvalues_dir does not exist: {pvalues_dir}")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    # --- Load NoRes lookup from fit_logs.txt ---
    log_file = os.path.join(output_dir, 'fit_logs.txt')
    if not os.path.isfile(log_file):
        print(f"Error: fit_logs.txt not found in: {output_dir}")
        sys.exit(1)

    logs_df   = pd.read_csv(log_file, usecols=["Domain", "NoRes"])
    nores_map = dict(zip(logs_df["Domain"], logs_df["NoRes"]))
    print(f"Loaded NoRes for {len(nores_map)} domains from fit_logs.txt")

    # --- Process all *_pvalues.csv files ---
    pval_files = sorted(glob.glob(os.path.join(pvalues_dir, "*_pvalues.csv")))
    if not pval_files:
        print(f"No *_pvalues.csv files found in: {pvalues_dir}")
        sys.exit(1)

    print(f"Found {len(pval_files)} *_pvalues.csv files. Compiling...")

    all_rows = []
    skipped  = 0

    for fpath in tqdm(pval_files, desc="Processing"):
        row = process_pvalues_file(fpath)
        if row is None:
            skipped += 1
            continue

        # Join NoRes from fit_logs.txt; warn if not found
        domain = row["Domain"]
        if domain not in nores_map:
            print(f"  [WARN] Domain '{domain}' not found in fit_logs.txt — NoRes set to NA")
        row["NoRes"] = nores_map.get(domain, pd.NA)

        all_rows.append(row)

    print(f"\nParsed:  {len(all_rows)} files")
    print(f"Skipped: {skipped} files")

    if not all_rows:
        print("No valid data to write. Exiting.")
        sys.exit(1)

    # --- Assemble, sort and save ---
    df = pd.DataFrame(all_rows, columns=[
        "Domain", "NoRes", "Best_Corr", "Corr_about_mean",
        "Eta0", "Pvalue", "BH_adjusted_Pvalue"
    ])

    df.sort_values(
        ['BH_adjusted_Pvalue', 'Corr_about_mean'],
        ascending=[True, False],
        inplace=True
    )

    revised_file = os.path.join(output_dir, 'fit_logs_revised.csv')
    df.to_csv(revised_file, index=False, quoting=csv.QUOTE_MINIMAL)
    print(f"\nSaved {len(df)} records → {revised_file}")


if __name__ == "__main__":
    main()