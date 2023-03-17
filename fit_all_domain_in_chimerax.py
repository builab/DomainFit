#!/usr/bin/python
# # -*- coding: utf-8 -*-

"""
@Authors Max Tong & HB
@Require ChimeraX 1.5 with proper excecutable
"""
# Usage
# python fit_all_domain_in_chimerax pdb_dir output_dir input_map map_level resolution search

# TODO
# Write a file for the best fit correlation for each domain as a summary

import sys,os,time
from datetime import datetime
script_dir=os.path.dirname(os.path.realpath(__file__))
import subprocess

pdb_dir = sys.argv[1]
output_dir = sys.argv[2]
input_map = sys.argv[3]
map_level = sys.argv[4]
resolution = sys.argv[5]
search = sys.argv[6]

# Initiate a log file
log_file = open(r"fit_logs.txt", "w")
log_file.write(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
log_file.write("\n")
log_file.close()

list = os.listdir(pdb_dir)
cmds=[]
for pdb in os.listdir(pdb_dir):
    if pdb.endswith(".pdb"):
        # Add them to the command list
        cmds.append(f'ChimeraX --nogui --offscreen --cmd \"runscript {script_dir}/fit_in_chimerax.py {pdb_dir}/{pdb} {output_dir} {input_map} {map_level} {resolution} {search}" --exit')

# Execute command list
#os.chdir(output_dir)
for cmd in cmds:
        print(f'start {cmd}', datetime.now())
        status = subprocess.call(cmd,shell=True)
#os.chdir(script_dir)

