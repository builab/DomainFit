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

def print_usage ():
    print("usage: python save_domain_all.py inputDir outputDir minLength maxLength")
    sys.exit()
#print(len(sys.argv))

if len(sys.argv) < 2 :
    print_usage()
else:
    logs=[]
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    
if len(sys.argv) < 3:
	min_length = '50'
else:
	min_length = sys.argv[3]

if len(sys.argv) < 4:
	max_length = '1000'
else:
	max_length = sys.argv[4]
	
print('Saving chains between ' + min_length + ' and ' + max_length + ' aa')

log_file = output_dir + '/domain_logs.txt'
log = open(log_file, "w")
log.write("#{}\n".format(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
log.write("\nUniprotId,Domain,NoResidues\n")
log.close()


list = os.listdir(input_dir)
cmds=[]
for pdb in os.listdir(input_dir):
    if pdb.endswith("domains.pdb"):
        # Add them to the command list
        cmds.append(f'chimerax --nogui --offscreen --cmd \"runscript {script_dir}/save_domain_single.py {input_dir}/{pdb} {output_dir} {min_length} {max_length}" --exit')

print(cmds)

# Execute command list
# Execute command list
#os.chdir(output_dir)
def execute(cmd):
    print(f'start {cmd}', datetime.now())
    return subprocess.call(cmd,shell=True)
#os.chdir(script_dir)

count = multiprocessing.cpu_count()
with multiprocessing.Pool(processes=count) as pool:
    results = pool.map(execute, cmds)
