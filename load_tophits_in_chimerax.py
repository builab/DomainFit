#!/usr/bin/env python
# # -*- coding: utf-8 -*-

"""
@Authors Huy Bui
"""
# Usage
# Operate from the main folder
# Load the top hits in ChimeraX

import sys,os,subprocess,shutil
import pandas as pd

def print_usage ():
	print("usage: load_tophits_in_chimerax.py density solutions_dir number_of_top_hit minsize")
	print("eg: load_tophits_in_chimerax.py density.mrc solutions_dir 5 60")
	sys.exit()
	
def filter_csv(fitcsv, minsize):
	''' This function is similar but not identical to visualize_solutions.py'''
	if os.path.exists(fitcsv):
		df = pd.read_csv(fitcsv, header = 0)
	else:
		print("WARNING: {:s} does not exist. Check again!".format(fitcsv))
		exit(0)
		
	df = df.loc[df['NoRes'] > minsize]	
	df_sub = df['Domain'].reset_index(drop=True).reset_index().copy()
	#print(df_sub)
	# Make index = 0 -> rank 1
	return df_sub


if __name__ == "__main__":
	if len(sys.argv) < 5:
		print(sys.argv)
		print_usage()

	density = sys.argv[1]
	sol_dir = sys.argv[2]
	noTophits = int(sys.argv[3])
	minsize = int(sys.argv[4])
	outfile = 'load_tophits.cxc'
	
	default_macos_chimera_path = "/Applications/ChimeraX-1.5.app/Contents/MacOS/ChimeraX"
	
	print("Generate a script to load {:d} top hits from {:s} with a minumum size of {:d} amino acids".format(noTophits, sol_dir, minsize))
	f = open(outfile, 'wt')
	f.write(f'open {density}\n')
	f.write(f'volume #1 transparency .5\n')
	
	fitcsv = sol_dir + '/fit_logs_revised.csv'
	df = filter_csv(fitcsv, minsize)
	
	for index, row in df.iterrows():
		if index < noTophits:
			#print(index)
			f.write("open {:s}/{:s}_bestfit.pdb\n".format(sol_dir,row['Domain']))
		else:
			break
	
	f.close()
	print(f"{outfile} written!")
	
	# Check operating system
	useMacOs = 0
	print("Platform: " + sys.platform)

	if sys.platform == 'darwin': #MacOS
		useMacOs = 1
		print ("No capability to generate picture on MacOS!!!")
		
	chimerax_path = "chimerax"
	if useMacOs == 1:
		chimerax_path = default_macos_chimera_path
	
	# Check if ChimeraX path is correct	
	if os.path.exists(chimerax_path) == 0 and shutil.which(chimerax_path) is None:
		print(f"The file '{chimerax_path}' does not exist.")
		print("Modify the script for the path of ChimeraX version from 1.5 and above.")
		print(f"Or just open the {outfile} with ChimeraX")
		exit(0)
	
	cmd = f'{chimerax_path} --cmd \"runscript {outfile}"'
	print(cmd)
	status = subprocess.call(cmd,shell=True)
	if status != 0:
		print(f"Error in {cmd}. Try to open the cxc file manually")
	