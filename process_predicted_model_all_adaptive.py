#!/usr/bin/python
# # -*- coding: utf-8 -*-

"""
@Authors Max Tong & HB
@Require phenix 1.20
@v0.2 Update with multiprocessing and phenix lddt option
@v0.3 Run biopython for sequence length & adaptive option (maximum_domains=protein_length/100)
"""
from Bio.PDB import *

import sys,os,time
from datetime import datetime
script_dir=os.path.dirname(os.path.realpath(__file__))
import subprocess, multiprocessing

def print_usage ():
    print("usage: python process_predicted_model_all.py <inputDir> <outputDir> <noProc> options")
    print("eg: python process_predicted_model_all.py input domains 10 maximum_rmsd=.8 maximum_domains=8")
    sys.exit()
    
def execute(cmd):
    print(f'start {cmd}', datetime.now())
    return subprocess.call(cmd,shell=True)
    
# Default option seems to work very well
default_options = "maximum_rmsd=.8 maximum_domains=8"

if len(sys.argv) < 4 :
    print_usage()

if len(sys.argv) == 4 : 
    options = default_options
else:
    logs=[]
    options = ' '.join(sys.argv[4 : ])  

    
input_dir = sys.argv[1]
output_dir = sys.argv[2]
threads = int(sys.argv[3])

print(f'Process_predicted_model options: {options}')

cmds=[]
for pdb in os.listdir(input_dir):
	# PDB file
    if pdb.endswith(".pdb"):
    	# Adaptive option for maximum_domains
		parser = PDBParser()
		structure = parser.get_structure("PHA-L", "1FAT.pdb")
        # Add them to the command list
        out_pdb = pdb.replace('.pdb', '_domains')
        cmds.append(f'phenix.process_predicted_model {input_dir}/{pdb} processed_model_prefix={output_dir}/{out_pdb} {options}')
    # CIF file
    if pdb.endswith(".cif"):
    	parser = MMCIFParser()
        
# Execute command list
count = threads
with multiprocessing.Pool(processes=count) as pool:
    results = pool.map(execute, cmds)
