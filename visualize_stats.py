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
	print("\tnumber_of_tophits Number of hit included in pdf generation (default = 0)")
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
	if len(sys.argv) < 2:
		print_usage()

	fitcsv = sys.argv[1]
	if len(sys.argv) == 3:
		noTophits = int(sys.argv[2])
	else:
		noTophits = 0
	
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
	
	fig, axs = plt.subplots(2)
	fig.suptitle('Fitting of all domains')
	fig.set_figwidth(10)
	fig.set_figheight(11)
	axs[0].plot(df['Corr_about_mean'].to_numpy(), -np.log10(df['Pvalue'].to_numpy()), marker='o', linestyle="", markerfacecolor="white", linewidth=4)
	axs[0].set(ylabel="-log(pvalue)", xlabel = "Normalized correlation coefficient")
	axs[0].grid(False)
	
	axs[1].plot(df['Corr_about_mean'].to_numpy(), -np.log10(df['BH_adjusted_Pvalue'].to_numpy()), marker='o', linestyle="", markerfacecolor="white", linewidth=4)
	axs[1].set(ylabel="-log(BH_adjusted_pvalue)", xlabel = "Normalized correlation coefficient")
	axs[1].grid(False)	
	
	
	plt.savefig(outEps, format='eps')
	plt.show()
