#!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# 2024/06/04

"""
@Script Script to rank AF3 cif files and also extract PAE from the AF json to the new rank PAE json
@Authors Huy Bui & ChatGPT
"""

import os,sys,shutil
import json
import numpy as np

def extract_pae_from_json(file_path, pae_json):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            pae_data = data['pae']       
            #pae_data = np.round(pae_data)
            max_predicted_aligned_error = np.max(pae_data)
            #print(len(pae_data))
            #print(max_predicted_aligned_error)    
            json_data = {
                    "predicted_aligned_error": pae_data,
                    "max_predicted_aligned_error": max_predicted_aligned_error
            }
            json_object = json.dumps([json_data])
            with open(pae_json, "w") as outfile:
                outfile.write(json_object)
        return 1
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

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
        print(f"Rank {rank}")
        rank = rank + 1
        file_basename = file_path.replace('.cif','')
        new_file_path = f"{file_basename}_rank_{rank:03d}.cif"
        shutil.copy(file_path, new_file_path)
        print(f"File {file_path} copied to {new_file_path} with value {value}")
        # json file
        json_basename = file_basename.replace('_model_','_full_data_')
        json_path = f"{json_basename}.json"
        new_pae_json = f"{file_basename}_rank_{rank:03d}.json"
        extract_pae_from_json(json_path, new_pae_json)
        print(f"PAE from {json_path} to {new_pae_json} with value {value}")
        

        
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python rank_AF3_models.py <directory_path>")
        sys.exit(1)
    
    directory_path = sys.argv[1]
    process_files(directory_path)

