#!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# 2024/06/04

"""
@Script Script to rank AF3 cif files
@Authors Huy Bui & ChatGPT
"""


import os,sys,shutil

# Script to read pLDDT value
# Base on this line
# _ma_qa_metric_global.metric_value 41.08
def read_plddt_from_af3_cif(file_path):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if "_ma_qa_metric_global.metric_value" in line:
                    try:
                        value = float(line.split()[-1])
                        return value
                    except ValueError:
                        print(f"Error: Unable to convert value to float in line: {line.strip()}")
                        return None
        print("Error: The line with '_ma_qa_metric_global.metric_value' was not found.")
        return None
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
        
        
def process_files(directory_path):
    # List all .cif files in the directory
    file_paths = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith('.cif')]
    
    # Read values from the files
    file_values = [(file_path, read_plddt_from_af3_cif(file_path)) for file_path in file_paths]
    
    # Remove files with None values
    file_values = [fv for fv in file_values if fv[1] is not None]
    
    # Sort files by their values in descending order
    file_values.sort(key=lambda x: x[1], reverse=True)
    
    # Rename the files based on their rank
    for rank, (file_path, value) in enumerate(file_values):
        file_basename = file_path.replace('.cif','')
        new_file_path = f"{file_basename}_rank_{rank+1:03d}.cif"
        shutil.copy(file_path, new_file_path)
        print(f"File {file_path} copied to {new_file_path} with value {value}")
        # json file
        shutil.copy(file_path, new_file_path)
        print(f"File {file_path} copied to {new_file_path} with value {value}")

        
        
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python rank_AF3_models.py <directory_path>")
        sys.exit(1)
    
    directory_path = sys.argv[1]
    process_files(directory_path)

