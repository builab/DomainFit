#!/usr/bin/env python3
# # -*- coding: utf-8 -*-

"""
@Authors Jerry Gao & Huy Bui
Script to visualize the stats
Top X to generate R stats
Generate the plot for the summarize of the fitting (for publication)
"""

import sys,os, subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
script_dir=os.path.dirname(os.path.realpath(__file__))


def print_usage ():
	print("usage: visualize_stats.py solutions_list number_of_tophits")
	print("\tsolutions_list the revised csv file")
	print("\tnumber_of_tophits Number of hit included in pdf generation")
	print("eg: visualize_stats.py solutions_density1/fit_logs_revised.csv 100")
	sys.exit()
	
def generate_Rpdf (outlist, model_basename):
	''' Use R to generate the stat '''
	print(f"Generating R stats for {outlist}")
	cmd = f"Rscript {script_dir}/pval_from_solutions.R {outlist} correlation_about_mean {model_basename}"
	status = subprocess.call(cmd, shell=True)
	if status != 0:
		print(f"Error in {cmd}. Exiting...")	
	return status
	
if __name__ == "__main__":
	if len(sys.argv) < 3:
		print_usage()

	fitcsv = sys.argv[1]
	noTophits = int(sys.argv[2])
	
	
	# Generate plot
	print(f"Plotting result for {fitcsv}")
	if os.path.exists(fitcsv):
		df = pd.read_csv(fitcsv, header = 0)
	else:
		print(f"WARNING: {fitcsv} does not exist. Check again!")
		exit(0)
	
	
	soldir = os.path.dirname(fitcsv)

	for index, row in df.iterrows():
		if index < noTophits:
			domain_name = row['Domain']
			generate_Rpdf(os.path.join(soldir, f"{domain_name}.csv"), os.path.join(soldir, f"{domain_name}"))
		else:
			break	

	outEps = os.path.join(soldir, "summaryplot.eps")	
	print(f"Plotting R statistics for {fitcsv} from {noTophits} top hits.\nOutput to {outEps}")
	plt.figure(figsize=(10, 6))
	plt.plot(df['Corr_mean'].to_numpy(), -np.log10(df['Pvalue'].to_numpy()), marker='o', linestyle="", markerfacecolor="white", linewidth=4)
	plt.ylabel('-log(pvalue)')
	plt.xlabel('Normalized correlation coefficient')
	plt.title(f'Fitting of all domains')
	plt.grid(False)
	plt.savefig(outEps, format='eps')
	plt.show()
