#!/usr/bin/python
# # -*- coding: utf-8 -*-

"""
@Authors Max Tong & HB
@Require phenix 1.20
@v0.1 Update with option
@v0.2 Update with multiprocessing and phenix lddt option
"""
import sys,os,time
from datetime import datetime
script_dir=os.path.dirname(os.path.realpath(__file__))
import subprocess, multiprocessing

def print_usage ():
    print("usage: python process_predicted_model_all.py <inputDir> <outputDir> options")
    print("eg: python process_predicted_model_all.py input domains maximum_rmsd=.8 maximum_domains=8")
    sys.exit()

# Default option seems to work very well
default_options = "maximum_rmsd=.8 maximum_domains=8"

if len(sys.argv) < 3 :
    print_usage()

if len(sys.argv) == 3:
	options = default_options
else:
    logs=[]
    options = ' '.join(sys.argv[3:])  

input_dir = sys.argv[1]
output_dir = sys.argv[2]

input_pdbs = f"{input_dir}/PDBs"
list = os.listdir(input_pdbs)
cmds=[]
for pdb in os.listdir(input_pdbs):
    if pdb.endswith(".pdb"):
        # Add them to the command list
        out_pdb = pdb.replace('.pdb', '_domains')

        #### Can use PAE .json files in the future for better fitting
        # pae = pdb.replace('.pdb', '.json')
        cmds.append(f'phenix.process_predicted_model {input_dir}/PDBs/{pdb} processed_model_prefix={output_dir}/{out_pdb} split_model_by_compact_regions=True b_value_field_is=lddt {options}')

# Execute command list

def execute(cmd):
    print(f'start {cmd}', datetime.now())
    return subprocess.call(cmd,shell=True)
#os.chdir(script_dir)

count = multiprocessing.cpu_count()
with multiprocessing.Pool(processes=count) as pool:
    results = pool.map(execute, cmds)
#os.chdir(script_dir)

