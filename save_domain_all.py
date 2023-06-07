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

def execute(cmd):
    print(f'start {cmd}', datetime.now())
    return subprocess.call(cmd,shell=True)

def print_usage ():
    print("usage: python save_domain_all.py inputDir outputDir minLength maxLength noProcessor")
    sys.exit()
#print(len(sys.argv))


if __name__ == "__main__":
    if len(sys.argv) < 2 :
        print_usage()
    else:
        logs=[]
        input_dir = sys.argv[1]
        output_dir = sys.argv[2]
    
    # Check operating system
    useMacOs = 0
    print("Platform: " + sys.platform)

    if sys.platform == 'darwin': #MacOS
        useMacOs = 1
        print ("No capability to generate picture on MacOS!!!")
    
    threads = 1

    if len(sys.argv) < 3:
        min_length = '50'
    else:
        min_length = sys.argv[3]

    if len(sys.argv) < 4:
        max_length = '1000'
    else:
        max_length = sys.argv[4]
    
    if len(sys.argv) == 6:
        threads = sys.argv[5]
    
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
            if useMacOs == 1:
                cmds.append(f'/Applications/ChimeraX-1.5.app/Contents/MacOS/ChimeraX --nogui --offscreen --cmd \"runscript {script_dir}/save_domain_single.py {input_dir}/{pdb} {output_dir} {min_length} {max_length}" --exit')
            else:
                cmds.append(f'chimerax --nogui --offscreen --cmd \"runscript {script_dir}/save_domain_single.py {input_dir}/{pdb} {output_dir} {min_length} {max_length}" --exit')

    #print(cmds)

    with multiprocessing.Pool(processes=threads) as pool:
        results = pool.map(execute, cmds)
