#!/usr/bin/python
# # -*- coding: utf-8 -*-

"""
@Authors Max Tong & HB
@Require phenix 1.20
@v0.1 Update with option
"""
import sys,os,time
from datetime import datetime
script_dir=os.path.dirname(os.path.realpath(__file__))
import subprocess

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

print(f'Process_predicted_model options: {options}')

list = os.listdir(input_dir)
cmds=[]
for pdb in os.listdir(input_dir):
    if pdb.endswith(".pdb"):
        # Add them to the command list
        out_pdb = pdb.replace('.pdb', '_domains')
        cmds.append(f'phenix.process_predicted_model {input_dir}/{pdb} processed_model_prefix={output_dir}/{out_pdb} {options}')

# Execute command list
#os.chdir(output_dir)
for cmd in cmds:
        print(f'start {cmd}', datetime.now())
        status = subprocess.call(cmd,shell=True)
#os.chdir(script_dir)
