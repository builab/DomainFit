#!/usr/bin/python
# # -*- coding: utf-8 -*-

"""
@Authors Jerry Gao & Huy Bui
"""
# Usage
# Operate from the main folder
# Load the top hits in ChimeraX

import sys,os
import pandas as pd

def print_usage ():
	print("usage: python load_tophits_in_chimerax.py density solutions_dir number_of_top_hit minsize")
	print("eg: python load_tophits_in_chimerax.py density.mrc solutions_dir 5 60")
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
		print_usage()

	density = sys.argv[1]
	sol_dir = sys.argv[2]
	noTophits = int(sys.argv[3])
	minsize = int(sys.argv[4])
	
	print("Generate a script to load {:d} top hits from {:s} with a minumum size of {:d} amino acids".format(noTophits, sol_dir, minsize))
	f = open('load_tophits.cxc', 'wt')
	f.write(f'open {density}\n')
	
	fitcsv = sol_dir + '/fit_logs_revised.csv'
	df = filter_csv(fitcsv, minsize)
	
	for index, row in df.iterrows():
		if index < noTophits:
			#print(index)
			f.write("open {:s}/{:s}_bestfit.pdb\n".format(sol_dir,row['Domain']))
		else:
			break
	
	f.close()
	print("load_tophits.cxc written!")
	