#!/usr/bin/python

# Python open a map

import sys,os,time
from datetime import datetime
script_dir=os.path.dirname(os.path.realpath(__file__))
import subprocess

pdb_dir = sys.argv[1]
output_dir = sys.argv[2]
input_map = sys.argv[3]
resolution = sys.argv[4]
search = sys.argv[5]

list = os.listdir(pdb_dir)
cmds=[]
for pdb in os.listdir(pdb_dir):
    if pdb.endswith(".pdb"):
        # Add them to the command list
        cmds.append(f'chimerax-daily --nogui --offscreen --cmd \"runscript {script_dir}/fit_in_chimerax.py {pdb_dir}/{pdb} {output_dir} {input_map} {resolution} {search}" --exit')

# Execute command list
#os.chdir(output_dir)
for cmd in cmds:
        print(f'start {cmd}', datetime.now())
        status = subprocess.call(cmd,shell=True)
#os.chdir(script_dir)

