#!/usr/bin/python
# # -*- coding: utf-8 -*-

"""
@Authors Max Tong & HB
@Require phenix 1.20
"""
import sys,os,time
from datetime import datetime
script_dir=os.path.dirname(os.path.realpath(__file__))
import subprocess

def print_usage ():
    print("usage: python process_predicted_model_all.py <inputDir> <outputDir> options")
    sys.exit()

if len(sys.argv) > 3 or len(sys.argv) < 2 :
    print_usage()
else:
    logs=[]
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    # options = sys.argv[3]

list = os.listdir(input_dir)
cmds=[]
for pdb in os.listdir(input_dir):
    if pdb.endswith(".pdb"):
        # Add them to the command list
        out_pdb = pdb.replace('.pdb', '_domains')
        cmds.append(f'phenix.process_predicted_model {input_dir}/{pdb} processed_model_prefix={output_dir}/{out_pdb} split_model_by_compact_regions=True')

# Execute command list
#os.chdir(output_dir)
for cmd in cmds:
        print(f'start {cmd}', datetime.now())
        status = subprocess.call(cmd,shell=True)
#os.chdir(script_dir)
