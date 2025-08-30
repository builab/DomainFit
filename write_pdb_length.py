#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Require ChimeraX, Inside ChimeraX run:
runscript write_pdb_length.py input_dir minAA maxAA
Example: runscript write_pdb_length.py /path/to/pdbs 30 500
If you run without the GUI, then type this
chimerax --nogui --offscreen --cmd "runscript write_pdb_length.py /path/to/pdbs 30 500" --exit 

"""
from chimerax.core.commands import run
import os.path
import sys, os
import pandas as pd
import glob

# Get command line arguments
if len(sys.argv) != 4:
    print("Usage: runscript write_pdb_length.py input_dir minAA maxAA")
    print("Example: runscript write_pdb_length.py /path/to/pdbs 30 500")
    sys.exit(1)

input_dir = sys.argv[1]
minAA = int(sys.argv[2])
maxAA = int(sys.argv[3])

# Check if input directory exists
if not os.path.exists(input_dir):
    print(f"Error: Input directory '{input_dir}' does not exist.")
    sys.exit(1)

# Initialize lists to store results
pdb_files = []
num_residues = []

# Find all PDB files in the input directory
pdb_pattern = os.path.join(input_dir, "*.pdb")
pdb_file_list = glob.glob(pdb_pattern)

if not pdb_file_list:
    print(f"No PDB files found in directory: {input_dir}")
    sys.exit(1)

print(f"Found {len(pdb_file_list)} PDB files to process...")
print(f"Filtering for proteins with {minAA}-{maxAA} residues...")

# Process each PDB file
for pdb_file in pdb_file_list:
    try:
        print(f"Processing: {os.path.basename(pdb_file)}")
        
        # Open the PDB file in ChimeraX
        model = run(session, 'open %s' % pdb_file)[0]
        
        # Get the number of residues
        residue_count = model.num_residues
        
        # Store the results
        pdb_files.append(os.path.basename(pdb_file))
        num_residues.append(residue_count)
        
        # Close the model to free memory
        run(session, 'close #%s' % model.id_string)
        
        print(f"  - Residues: {residue_count}")
        
    except Exception as e:
        print(f"Error processing {pdb_file}: {str(e)}")
        # Still add the file to the list with 0 residues or None
        pdb_files.append(os.path.basename(pdb_file))
        num_residues.append(0)

# Create DataFrame with the results
df = pd.DataFrame({
    'pdb_file': pdb_files,
    'num_residues': num_residues
})

# Write to CSV file in current directory
output_csv = 'pdb_residue_counts.csv'
df.to_csv(output_csv, index=False)

# Filter proteins within the specified range
print(f"\nFiltering data...")
print(f"Total files before filtering: {len(df)}")
print(f"Range: {minAA} to {maxAA} residues")

# Debug: show some examples
print("\nSample data:")
for i, row in df.head().iterrows():
    print(f"  {row['pdb_file']}: {row['num_residues']} residues")

filtered_df = df[(df['num_residues'] >= minAA) & (df['num_residues'] <= maxAA)].copy()

print(f"Files after filtering: {len(filtered_df)}")

# Create a simple list file with filtered PDB names
filtered_list_file = f'pdb_list_{minAA}_{maxAA}AA.txt'
with open(filtered_list_file, 'w') as f:
    for pdb_file in filtered_df['pdb_file']:
        f.write(f"{pdb_file}\n")

# Also create a CSV with only filtered results
filtered_csv = f'pdb_filtered_{minAA}_{maxAA}AA.csv'
filtered_df.to_csv(filtered_csv, index=False)

print(f"\nResults written to: {output_csv}")
print(f"Filtered CSV written to: {filtered_csv}")
print(f"Filtered list written to: {filtered_list_file}")
print(f"Processed {len(pdb_files)} files total.")
print(f"Found {len(filtered_df)} files with {minAA}-{maxAA} residues.")

# Display summary statistics
print(f"\nSummary:")
print(f"  - Total files processed: {len(pdb_files)}")
print(f"  - Files in range ({minAA}-{maxAA} AA): {len(filtered_df)}")
print(f"  - Average residues (all): {df['num_residues'].mean():.1f}")
print(f"  - Average residues (filtered): {filtered_df['num_residues'].mean():.1f}" if len(filtered_df) > 0 else "  - No files in specified range")
print(f"  - Min residues: {df['num_residues'].min()}")
print(f"  - Max residues: {df['num_residues'].max()}")