#!/usr/bin/env python
# # -*- coding: utf-8 -*-

"""
@Authors Huy Bui
Last mod: 2024/11/21
This is only used when somehow the last step of fit_domains_in_chimerax.py does
not work and no fit_log_revised.csv generated.
"""

import pandas as pd
import sys


def print_usage ():
	print("usage: generate_fit_log_revised.py log_file output_dir ")
	print("eg: generate_fit_log_revised.py solutions/fit_logs.txt solutions/")
	sys.exit()
	

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print(sys.argv)
		print_usage()

	log_file = sys.argv[1]
	output_dir = sys.argv[2]
	


	df = pd.read_csv(log_file, sep='\s*,\s*', engine='python')
	df.info()
	df.dropna()
	print(df)

	df.sort_values(['BH_adjusted_Pvalue', 'Corr_about_mean'], ascending=[True, False], inplace=True)

	df.to_csv(output_dir + '/fit_logs_revised.csv', index=False)
