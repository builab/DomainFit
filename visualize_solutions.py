#!/usr/bin/env python3
# # -*- coding: utf-8 -*-

"""
@Authors Huy Bui 
"""
# Usage
# python visualize_solutions.py solutions_csv_list cutoff_rank outputPlot
# output a graph is optional

import sys,os
import pandas as pd
import matplotlib.pyplot as plt

def print_usage ():
	print("usage: visualize_solutions.py solutions_csv_list cutoff_rank min_size outputPlot")
	print("solutions_csv_list: a text file having path to the fit_logs_revised.csv of each solution")
	print("cutoff_rank: maximum rank display (3)")	
	print("min_size (optional, default 40): amino acid size")
	print("outputPlot (optional) output plot in eps format")
	print("eg: visualize_solutions.py solutions_csv_list.txt 10 min_size plot.eps")
	sys.exit()

''' Get protein ranking for this list'''
def process_csv(fitcsv, minsize):
	if os.path.exists(fitcsv):
		df = pd.read_csv(fitcsv, header = 0)
	else:
		print("WARNING: {:s} does not exist. Check again!".format(fitcsv))
		exit(0)
		
	df['Protein'] = df['Domain'].replace('_D[0-9]+','', regex=True)
	df = df.loc[df['NoRes'] > minsize]	
	df.drop_duplicates(subset='Protein', inplace=True)
	df_sub = df['Protein'].reset_index(drop=True).reset_index().copy()
	print(df_sub)
	# Make index = 0 -> rank 1
	df_sub['index'] = df_sub['index'] + 1
	df_sub = df_sub.reindex(columns={'Protein': 'Protein', 'index': 'index'})
	return df_sub
	

if __name__ == "__main__":

	if len(sys.argv) < 2:
		print_usage()

	doPlot = 0
	csvlist = sys.argv[1]
	cutoff = int(sys.argv[2])
	minsize = 40
	
	if len(sys.argv) > 3:
		minsize = int(sys.argv[3])
		
	if len(sys.argv) == 5:
		doPlot = 1
		outEps = sys.argv[4]
	
	with open(csvlist) as f:
		sol_list = f.read().splitlines()
		
	#print(sol_list)
	count = 1
	df_rank = pd.DataFrame()
	for fitcsv in sol_list:
		df_fit = process_csv(fitcsv, minsize)
		new_col = f'rank{count}'
		df_fit.rename(columns={'index': new_col}, inplace=True)
		#print(df_fit)
		if df_rank.empty:
			df_rank = df_fit
		else:
			df_rank = df_rank.merge(df_fit, on='Protein', how='inner')
		count = count + 1
		
	# Filtering 
	print(f'Filtering protein with cutoff rank of {cutoff}')
	protList = list()
	for i in range(count-1):
		new_col = f'rank{i+1}'
		protList.extend(df_rank.loc[df_rank[new_col] < cutoff, 'Protein'].tolist())
	protList = set(protList)
	
	# Need to replace either .txt or .csv to .csv	
	outcsv = 'rank_' + csvlist.replace('.txt', '.csv')
	print(f'Write ranking output file {outcsv}')
	df_rank = df_rank[df_rank['Protein'].isin(protList)]
	df_rank.to_csv(outcsv, index=False)
	
	
	# Plotting
	if doPlot < 1:
		exit()
	print('Plotting protein hits!')
	# Reset rank > 10 to 20
	for i in range(count-1):
		new_col = f'rank{i+1}'
		df_rank.loc[df_rank[new_col] > cutoff, new_col] = cutoff*2	
	
	#print(df_rank)
	plt.figure(figsize=(10, 6))
	for index, row in df_rank.iterrows():
		# Highlight one with rank 1
		if 1 in set(row):
			plt.plot(range(1, len(row)), row[1:], marker='o', markerfacecolor="white", linewidth=4, label=row['Protein'])
		else:
			plt.plot(range(1, len(row)), row[1:], marker='o', markerfacecolor="white", linewidth=2, label=row['Protein'], alpha=0.4)

	
	plt.xlabel('Density Number')
	plt.ylabel('Rank')
	plt.gca().invert_yaxis()
	plt.title(f'Rank Values for Proteins with cutoff rank={cutoff} and MinSize = {minsize}')
	plt.xticks(range(1, len(row)))
	plt.legend()
	plt.grid(False)
	plt.savefig(outEps, format='eps')
	plt.show()
