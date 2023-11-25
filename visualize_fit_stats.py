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
	print("usage: visualize_fit_stats.py solutions_list minsize")
	print("\tsolutions_list the revised csv file")
	print("\tminsize mininum size to use to filter (default = 0)")
	print("eg: visualize_fit_stats.py solutions_density1/fit_logs_revised.csv 100")
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
		minsize = int(sys.argv[2])
	else:
		minsize = 0
	
	# Generate plot
	print(f"Plotting result for {fitcsv}")
	if os.path.exists(fitcsv):
		df = pd.read_csv(fitcsv, header = 0)
	else:
		print(f"WARNING: {fitcsv} does not exist. Check again!")
		exit(0)
		
	soldir = os.path.dirname(fitcsv)

	outEps = os.path.join(soldir, "summaryplot.eps")	
	print(f"Plotting R statistics for {fitcsv} from minimum size of {minsize} amino acid.\nOutput to {outEps}")
	
	fig, axs = plt.subplots(2)
	fig.suptitle(f'Fitting of all domains using a size filter of {minsize} aa')
	fig.set_figwidth(10)
	fig.set_figheight(11)
	#axs[0].plot(df.loc[df['NoRes'] >= minsize, 'Corr_about_mean'].to_numpy(), -np.log10(df.loc[df['NoRes'] >= minsize, 'Pvalue'].to_numpy()), marker='o', linestyle="", markerfacecolor=(0.121,0.466,0.705,0.2), linewidth=4, mec='#1F77B4')
	axs[0].plot(df.loc[df['NoRes'] < minsize, 'Corr_about_mean'].to_numpy(), -np.log10(df.loc[df['NoRes'] < minsize, 'Pvalue'].to_numpy()), marker='o', linestyle="", markerfacecolor='white', linewidth=4, mec=(0.121,0.466,0.705,0.5))
	axs[0].plot(df.loc[df['NoRes'] >= minsize, 'Corr_about_mean'].to_numpy(), -np.log10(df.loc[df['NoRes'] >= minsize, 'Pvalue'].to_numpy()), marker='o', linestyle="", markerfacecolor='white', linewidth=4, mec='#1F77DA')
	axs[0].set(ylabel="-log10(pvalue)", xlabel = "Normalized correlation coefficient")
	axs[0].grid(False)
	axs[1].plot(df.loc[df['NoRes'] < minsize, 'Corr_about_mean'].to_numpy(), -np.log10(df.loc[df['NoRes'] < minsize, 'BH_adjusted_Pvalue'].to_numpy()), marker='o', linestyle="", markerfacecolor='white', linewidth=4, mec=(0.121,0.466,0.705,0.5))
	axs[1].plot(df.loc[df['NoRes'] >= minsize, 'Corr_about_mean'].to_numpy(), -np.log10(df.loc[df['NoRes'] >= minsize, 'BH_adjusted_Pvalue'].to_numpy()), marker='o', linestyle="", markerfacecolor='white', linewidth=4, mec='#1F77B4')
	axs[1].set(ylabel="-log10(BH_adjusted_pvalue)", xlabel = "Normalized correlation coefficient")
	axs[1].grid(False)	
	
	
	plt.savefig(outEps, format='eps')
	plt.show()
