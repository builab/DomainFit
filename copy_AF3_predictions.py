#!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# Author: HB &  ChatGPT
# Script to copy/rename rank_000 prediction from AF3 to a new directory for running DomainFit
# The file name pattern must be fold_i7mh00_model_3_rank_001.cif, will be renamed to i7mh00.cif

import os
import shutil
import sys

def copy_files(source_dir, dest_dir):
    # Iterate over all files in the source directory
    for filename in os.listdir(source_dir):
        if "rank_001" in filename and filename.endswith(".cif"):
            # Extract the prefix dynamically
            prefix = filename.split("_")[1]
            new_filename = prefix.upper() + '.cif'
            source_file = os.path.join(source_dir, filename)
            dest_file = os.path.join(dest_dir, new_filename)
            # Copy the file to the destination directory
            shutil.copy(source_file, dest_file)
            print(f"Copied {source_file} to {dest_file}")


if __name__ == "__main__":
    print("| copy_AF3_predictions.py |\nCopy and rename AF3 rank 1 prediction to another folder")
    print("Must run rank_AF3_models.py before!\n File pattern fold_uniprotID_model_x_rank_001.cif")

    print("Starting\n")
    # Check if the number of arguments is correct
    if len(sys.argv) != 3:
        print("Usage: copy_colabfold_predictions.py source_directory destination_directory")
        sys.exit(1)

    # Get source and destination directories from command line arguments
    source_directory = sys.argv[1]
    destination_directory = sys.argv[2]

    # Call the function to copy files
    copy_files(source_directory, destination_directory)

    print("\nDone!\n")