#!/usr/bin/python
# # -*- coding: utf-8 -*-

"""
@Authors Jerry Gao & Huy Bui
TODO May offer more option to filter
TODO Make the filter a common library and then reuse & rewrite some of the other programs
"""

import sys,os
import pandas as pd

def print_usage ():
	print("usage: python filter_solution_list.py solutions_list minsize")
	print("\tsolutions_list the revised csv file")
	print("\tminsize minium size in amino acids")
	print("eg: python filter_solution_list.py solutions_density1/fit_logs_revised.csv 100")
	sys.exit()
	
def filter_csv(fitcsv, minsize):
	''' This function is similar load_tophits_in_chimerax.py. Can we merge it or make a common one to share'''
	if os.path.exists(fitcsv):
		df = pd.read_csv(fitcsv, header = 0)
	else:
		print("WARNING: {:s} does not exist. Check again!".format(fitcsv))
		exit(0)
		
	df = df.loc[df['NoRes'] > minsize]	
	df_sub = df.reset_index(drop=True).copy()
	#print(df_sub)
	# Make index = 0 -> rank 1
	return df_sub

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print_usage()

	fitcsv = sys.argv[1]
	minsize = int(sys.argv[2])
	
	print("Filtering {:s} with a minumum size of {:d} amino acids".format(fitcsv, minsize))	
	df = filter_csv(fitcsv, minsize)
	print(df)
	out_csv = fitcsv.replace('.csv', '_min{:d}.csv'.format(minsize))
	df.to_csv(out_csv, index=False)
	print("{:s} written!".format(out_csv))
	