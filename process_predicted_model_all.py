#!/usr/bin/python
# # -*- coding: utf-8 -*-

"""
@Authors Max Tong & HB
@Require phenix 1.20
@v0.2 Update with multiprocessing and phenix lddt option
"""
import sys,os,time,platform
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
    if pdb.endswith(".pdb"):
        # Add them to the command list
        out_pdb = pdb.replace('.pdb', '_domains')
        cmds.append(f'phenix.process_predicted_model {input_dir}/{pdb} processed_model_prefix={output_dir}/{out_pdb} {options}')
        
# Execute command list
count = threads
with multiprocessing.Pool(processes=count) as pool:
    results = pool.map(execute, cmds)
