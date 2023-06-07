#!/usr/bin/python
# # -*- coding: utf-8 -*-

"""
@Authors Max Tong & HB
@Require ChimeraX
TODO Write out summary for no of AA
"""

import sys,os,time
from datetime import datetime
script_dir=os.path.dirname(os.path.realpath(__file__))
import subprocess, multiprocessing
import pandas as pd

def execute(cmd):
    print(f'start {cmd}', datetime.now())
    return subprocess.call(cmd,shell=True)

def print_usage ():
    print("usage: python save_domain_all_cif_human.py inputDir1 inputDir2 outputDir minLength maxLength noProcessor")
    sys.exit()
#print(len(sys.argv))

if len(sys.argv) < 2 :
    print_usage()
else:
    logs=[]
    input_dir1 = sys.argv[1]
    input_dir2 = sys.argv[2]
    output_dir = sys.argv[3]
    
threads = 10

if len(sys.argv) < 4:
	min_length = '50'
else:
	min_length = sys.argv[4]

if len(sys.argv) < 5:
	max_length = '1000'
else:
	max_length = sys.argv[5]
	
if len(sys.argv) == 7:
	threads = int(sys.argv[6])
	
print('Saving chains between ' + min_length + ' and ' + max_length + ' aa')

log_file = output_dir + '/domain_logs.txt'
log = open(log_file, "w")
log.write("#{}\n".format(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
log.write("\nUniprotId,Domain,NoResidues\n")
log.close()


list = os.listdir(input_dir1)
cmds=[]
for cif in os.listdir(input_dir1):
    if cif.endswith(".cif"):
        # Add them to the command list
        uniprotID = cif[:-4]
        cmds.append(f'chimerax --nogui --offscreen --cmd \"runscript {script_dir}/save_domain_single_cif_human.py {input_dir1}/{cif} {input_dir2}/{uniprotID}.domains {output_dir} {min_length} {max_length}" --exit')


with multiprocessing.Pool(processes=threads) as pool:
    results = pool.map(execute, cmds)
