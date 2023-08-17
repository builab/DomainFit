#!/usr/bin/python
# # -*- coding: utf-8 -*-

"""
@Authors Max Tong & HB
@Require ChimeraX
2023/06/13 Accomodate both pdb & cif
Right now, the script assumes .domains always exist, if not make the .domains = entire molecule?
"""

import sys,os,time
from shutil import which
from datetime import datetime
script_dir=os.path.dirname(os.path.realpath(__file__))
import subprocess, multiprocessing
import pandas as pd

def execute(cmd):
	print(f'start {cmd}', datetime.now())
	return subprocess.call(cmd,shell=True)

def print_usage ():
	print("usage: python save_domain_all_using_domain_info.py inputDirPDB inputDirDomainInfo outputDir minLength maxLength noProcessor")
	sys.exit()
#print(len(sys.argv))

if __name__ == "__main__":

	if len(sys.argv) < 2 :
		print_usage()
	else:
		logs=[]
		input_dir1 = sys.argv[1] # PDB
		input_dir2 = sys.argv[2] # Domain info
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
	
	# Check operating system
	useMacOs = 0
	print("Platform: " + sys.platform)
	
	os.makedirs(output_dir, exist_ok=True)
	
	if sys.platform == 'darwin': #MacOS
		useMacOs = 1
		print ("No capability to generate picture on MacOS!!!")
	
	chimerax_path = "chimerax"
	if useMacOs == 1:
		chimerax_path = "/Applications/ChimeraX-1.5.app/Contents/MacOS/ChimeraX"
		
	if os.path.exists(chimerax_path) == 0 and which(chimerax_path) is None:
		print(f"The file '{chimerax_path}' does not exist.")
		print("Modify the script for the path of ChimeraX version from 1.5 and above.")
		exit(0)
	
	print('Saving chains between ' + min_length + ' and ' + max_length + ' aa')

	log_file = output_dir + '/domain_logs.txt'
	log = open(log_file, "w")
	log.write("#{}\n".format(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
	log.write("\nUniprotId,Domain,NoResidues\n")
	log.close()


	list = os.listdir(input_dir1)
	cmds=[]
	for cif in os.listdir(input_dir1):
		if cif.endswith((".cif", ".pdb")) & os.path.exists(os.path.join(input_dir2, f"{cif[:-4]}.domains")):
			# Add them to the command list
			uniprotID = cif[:-4]
			cmds.append(f'{chimerax_path} --nogui --offscreen --cmd \"runscript {script_dir}/save_domain_single_from_info.py {input_dir1}/{cif} {input_dir2}/{uniprotID}.domains {output_dir} {min_length} {max_length}" --exit')



	with multiprocessing.Pool(processes=threads) as pool:
		results = pool.map(execute, cmds)
