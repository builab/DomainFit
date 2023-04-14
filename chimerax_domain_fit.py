#!/usr/bin/python
# # -*- coding: utf-8 -*-

"""
@Authors Max Tong & HB
@Require ChimeraX 1.5 with proper excecutable
"""
# Usage
# python chimerax_domain_fit.py input_dir proteinDensity minThreshold maxThreshold search threads
# python fit_all_domain_in_chimerax pdb_dir output_dir input_map map_level resolution search

# TODO
# Write a file for the best fit correlation for each domain as a summary

import sys,os,time
import glob
from datetime import datetime
import subprocess
script_dir=os.path.dirname(os.path.realpath(__file__))


# Syntax
def print_usage ():
    print("usage: chimerax_domain_fit.py <input_dir> <proteinDensity> <minThreshold> <maxThreshold> <search> <threads>" )

# Ensures that there are 5 arguments
if len(sys.argv) < 5:
    print_usage()
else:
    input_dir = sys.argv[1]
    # Check if the input directory exists
    if not os.path.isdir(input_dir):
        print("Invalid directory")
        sys.exit()
    density = sys.argv[2]
    # Check if the density (.mrc) exists
    if not os.path.isfile(density) and '.mrc' == density[-4:]:
        print("Invalid protein density. Please ensure that the protein density is a .mrc file")
        sys.exit()

    #Intialize Folder Paths "Processed", "Single Domains", and "Solutions"
    PDBs = f"{input_dir}/PDBs"
    processed = f"{input_dir}/processed"
    single_domains = f"{input_dir}/single_domains"
    solutions = f"{input_dir}/solutions"

    #Check if there are valid PDBs in the input directory
    globPath = glob.glob(PDBs)
    if len(globPath) < 1:
        print("Please put valid pdbs in the input directory")
        sys.exit()
    logs=[]
    minT = sys.argv[3]
    maxT = sys.argv[4]
    search = sys.argv[5]
    # threads = sys.argv[6]

    if input_dir[0] != '/':
        input_dir = os.getcwd() + '/' + input_dir
    
    # Make sure all folders are properly created

    if not os.path.exists(PDBs):
        os.system('mkdir ' + PDBs)
    if not os.path.exists(processed):
        os.system('mkdir ' + processed)
    if not os.path.exists(single_domains):
        os.system('mkdir ' + single_domains)
    if not os.path.exists(solutions):
        os.system('mkdir ' + solutions)

    print('start input processing', datetime.now())
    cmds=[]

    ####################### RUN THESE SCRIPTS ONLY IF DOMAIN PARSING IS NECESSARY ############################
    cmds.append(f'python {script_dir}/process_predicted_model_all.py {input_dir} {processed}')
    cmds.append(f'python {script_dir}/save_domain_all.py {processed} {single_domains} {minT} {maxT}')

    ###################### CHIMERAX FITMAP ######################
    cmds.append(f'python {script_dir}/fit_all_domain_in_chimerax.py {single_domains} {solutions} {density} 0.034 5 {search}')
    step=1
    for cmd in cmds:
        print(f'start {cmd}', datetime.now())
        status = subprocess.call(cmd,shell=True)
        if status != 0:
            print(f"Error in {cmd}.Exiting...")
        else:
            logs.append(str(step))
            step = step + 1
        print(f'end {cmd}', datetime.now()) 
    print(f'Domain fitting for {density} done')
