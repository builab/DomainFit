#!/usr/bin/python
# # -*- coding: utf-8 -*-

"""
@Authors Max Tong & HB
@Require ChimeraX 1.5 with proper excecutable
"""
# Usage
# python fit_all_domain_in_chimerax pdb_dir output_dir input_map map_level resolution search numProc

# TODO
# Add also cif option
# Write a file for the best fit correlation for each domain as a summary

import sys,os,time
from datetime import datetime
script_dir=os.path.dirname(os.path.realpath(__file__))
import subprocess, multiprocessing

def print_usage ():
    print("usage: python fit_all_domain_in_chimerax.py inputDir outputDir inputMap mapLevel resolution searchNo noProcessor")
    print("eg: python fit_all_domain_in_chimerax.py single_domains solutions ref.mrc 0.0394 5 200 10")
    sys.exit()
    
def execute(cmd):
    print(f'start {cmd}', datetime.now())
    return subprocess.call(cmd,shell=True)

if len(sys.argv) < 7 :
    print_usage()

pdb_dir = sys.argv[1]
output_dir = sys.argv[2]
input_map = sys.argv[3]
map_level = sys.argv[4]
resolution = sys.argv[5]
search = sys.argv[6]

if len(sys.argv) == 7:
	threads = 10; # Default 10 threads
else:
	threads = sys.argv[7]
	
# Initiate a log file
log_file = output_dir + '/fit_logs.txt'
log = open(log_file, "w")
# log.write("#{}\n".format(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
log.write("\nDomain, NoRes, Best_Corr, Second_Best_Corr, Diff, Worst_Corr, Range, P_val_best_fit, Corr_mean, Pvalue\n")
# log.write("\n")
log.close()

list = os.listdir(pdb_dir)
cmds=[]
for pdb in os.listdir(pdb_dir):
    if pdb.endswith((".pdb", ".cif")):
        # Add them to the command list
        cmds.append(f'chimerax --nogui --offscreen --cmd \"runscript {script_dir}/fit_in_chimerax.py {pdb_dir}/{pdb} {output_dir} {input_map} {map_level} {resolution} {search}" --exit')

with multiprocessing.Pool(processes=threads) as pool:
    results = pool.map(execute, cmds)

# Find best domain based on largest change in fit correlation between first and second hit
import pandas as pd
df = pd.read_csv(log_file, sep='\s*,\s*')
df.info()
df.dropna()
print(df)
for col in df.columns:
    print(col)
df.sort_values(['Corr_mean', 'Diff'], ascending=[False, False], inplace=True)
# df.sort_values(by = "Diff", inplace=True, ascending=False)

print(df)
df.to_csv(output_dir + '/fit_logs_revised.csv', index=False)


