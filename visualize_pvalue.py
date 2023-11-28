#!/usr/bin/env python3
# # -*- coding: utf-8 -*-

"""
Plot radar plot for P-value and corr_about_mean
Need to merge with visualize_solutions
@Authors Jerry Gao, Huy Bui 
"""
# Usage
# python visualize_pvalue.py solutions_csv_list min_size

import sys,os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def print_usage ():
	print("usage: visualize_pvalue.py solutions_csv_list column minsize")
	print("solutions_csv_list: a text file having path to the fit_logs_revised.csv of each solution")
	print("column: column label (pvalue, corr_about_mean, bh_adjusted_pvalue)")
	print("minsize (optional, default 40): minimum amino acid size")
	print("eg: visualize_pvalue.py solutions_csv_list.txt corr_about_mean 50")
	sys.exit()

''' Get protein ranking for this list'''
def process_csv(fitcsv, minsize, column):
	if os.path.exists(fitcsv):
		df = pd.read_csv(fitcsv, header = 0)
	else:
		print("WARNING: {:s} does not exist. Check again!".format(fitcsv))
		exit(0)
		
	df['Protein'] = df['Domain'].replace('_D[0-9]+','', regex=True)
	df = df.loc[df['NoRes'] > minsize]	
	df.drop_duplicates(subset='Protein', inplace=True)
	
	if column.lower() == 'pvalue':
		df['Value'] = -np.log10(df['Pvalue']) #Taking the -log10(Pvalue)
	elif column.lower() == 'corr_about_mean':
		df['Value'] = df['Corr_about_mean'] 
	elif column.lower() == 'bh_adjusted_pvalue':
		df['Value'] = -np.log10(df['BH_adjusted_Pvalue']) #Taking the -log10(BH_adjusted_Pvalue)
	else:
		print('Not recorganized column!')
		return None		

	
	df_sub = df[['Protein', 'Value']].reset_index(drop=True).reset_index().copy()
	df_sub = df_sub.reindex(columns={'Protein': 'Protein', 'Value': 'Value'})
	#print(df_sub)
	return df_sub
	

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print_usage()

	csvlist = sys.argv[1]
	column = 'Pvalue'
	minsize = 40
		
	if len(sys.argv) > 2:
		column = sys.argv[2]
		
	if len(sys.argv) == 4:
		minsize = sys.argv[3]
		
	with open(csvlist) as f:
		sol_list = f.read().splitlines()
		

	if column.lower() == 'pvalue':
		ptitle = f'-log10(Pvalue) for top hit from each solution with size filter of {minsize} amino acid'
	elif column.lower() == 'corr_about_mean':
		ptitle = f'Normalized correlation coefficient for top hit from each solution with size filter of {minsize} amino acid'
	elif column.lower() == 'bh_adjusted_pvalue':
		ptitle = f'-log10(BH_adjusted_Pvalue) for top hit from each solution with size filter of {minsize} amino acid'
	else:
		print('Not recorganized column!')
		exit(0)	

	values = []
	for fitcsv in sol_list:
		if fitcsv.isspace() == True:
			continue
		df_fit = process_csv(fitcsv, minsize, column)
		values.append(df_fit['Value'].iloc[0])  
	
	values += values[:1]	
	
	
	categories = list(range(1, len(values)))
	print(categories)
	N = len(categories)
	angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
	#print(angles)
	angles += angles[:1]
	print(values)
	print(angles)

	fig, ax = plt.subplots(figsize=(10, 6), subplot_kw=dict(polar=True))
	ax.set_theta_offset(np.pi / 2)
	ax.set_theta_direction(-1)


	ax.plot(angles, values, marker='o', markerfacecolor="white", linewidth=4)

	ax.set_xticks(angles[:-1])
	ax.set_xticklabels(categories)
	ax.tick_params(axis='y', labelsize=11)
	ax.set_rlabel_position(0)
	ax.set_ylim(0, max(values)) #y axis range
	#ax.text(-0.05, ax.get_rmax() - 7, '-log10(Pvalue)', horizontalalignment='center', verticalalignment='center', rotation=90)
	plt.xlabel('Density Number')		
	plt.title(ptitle)
	plt.show()