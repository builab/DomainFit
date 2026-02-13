#!/usr/bin/env python3
"""
Compile fit_logs_revised.csv from all *_pvalues.csv files in a directory.

Usage:
    python generate_fit_logs_revised.py <pvalues_dir> <output_dir>

Arguments:
    pvalues_dir  Directory containing *_pvalues.csv files
    output_dir   Directory where fit_logs_revised.csv will be written
"""

import sys
import os
import csv
import glob
import pandas as pd
from tqdm import tqdm


# ---------------------------------------------------------------------------
# Column index constants (0-based) within each *_pvalues.csv
# These match the indices used in fit_domains_in_chimerax.py
# ---------------------------------------------------------------------------
COL_P_VAL_BEST_FIT   =  0   # first column — the best-fit p-value string from R
COL_CORR_ABOUT_MEAN  = 26
COL_PVALUE           = 38
COL_ETA0             = 39
COL_BH_ADJ_PVALUE    = 41   # used to select the best row per file


def domain_name_from_path(filepath: str) -> str:
    """
    Derive a domain name from the pvalues CSV filename.
    Strips the '_pvalues.csv' suffix so that e.g.
    'domain_ABC_pvalues.csv' -> 'domain_ABC'.
    """
    basename = os.path.basename(filepath)
    for suffix in ("_pvalues.csv", "_pvalue.csv"):
        if basename.lower().endswith(suffix):
            return basename[: -len(suffix)]
    # Fallback: just strip the extension
    return os.path.splitext(basename)[0]


def process_pvalues_file(filepath: str) -> dict | None:
    """
    Read a *_pvalues.csv file and return a result row dict,
    selecting the row with the lowest BH_adjusted_Pvalue.
    Returns None if the file cannot be parsed.
    """
    try:
        p_df = pd.read_csv(filepath, sep=r'\s*,\s*', engine='python').dropna()

        if p_df.empty:
            print(f"  [WARN] Empty after dropna: {filepath}")
            return None

        # Guard against files that don't have enough columns
        required_cols = max(COL_P_VAL_BEST_FIT, COL_CORR_ABOUT_MEAN,
                            COL_PVALUE, COL_ETA0, COL_BH_ADJ_PVALUE)
        if p_df.shape[1] <= required_cols:
            print(f"  [WARN] Too few columns ({p_df.shape[1]}) in: {filepath}")
            return None

        # Pick the row with the best (lowest) BH-adjusted p-value
        best_idx = p_df.iloc[:, COL_BH_ADJ_PVALUE].astype(float).idxmin()
        best_row = p_df.loc[best_idx]

        # Clean the R-output p-value string (may carry stray quotes)
        p_val_raw = str(best_row.iloc[COL_P_VAL_BEST_FIT]).replace('"', '').replace("'", "")

        return {
            "Domain":             domain_name_from_path(filepath),
            "P_val_best_fit":     p_val_raw,
            "Corr_about_mean":    best_row.iloc[COL_CORR_ABOUT_MEAN],
            "Eta0":               best_row.iloc[COL_ETA0],
            "Pvalue":             best_row.iloc[COL_PVALUE],
            "BH_adjusted_Pvalue": best_row.iloc[COL_BH_ADJ_PVALUE],
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

    # Collect all *_pvalues.csv files (case-insensitive on the suffix)
    pattern = os.path.join(pvalues_dir, "*_pvalues.csv")
    pval_files = sorted(glob.glob(pattern))

    if not pval_files:
        print(f"No *_pvalues.csv files found in: {pvalues_dir}")
        sys.exit(1)

    print(f"Found {len(pval_files)} *_pvalues.csv files. Compiling...")

    all_rows = []
    skipped  = 0

    for fpath in tqdm(pval_files, desc="Processing"):
        row = process_pvalues_file(fpath)
        if row:
            all_rows.append(row)
        else:
            skipped += 1

    print(f"\nParsed:  {len(all_rows)} files")
    print(f"Skipped: {skipped} files")

    if not all_rows:
        print("No valid data to write. Exiting.")
        sys.exit(1)

    df = pd.DataFrame(all_rows)

    # Sort by best BH_adjusted_Pvalue first, then highest Corr_about_mean
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