#!/usr/bin/env python3
# # -*- coding: utf-8 -*-

"""
@Authors Jerry Gao & Huy Bui
Script to visualize the stats
Top X to generate pdf_pvalue
Generate Z-score of correlation_about_mean
Not yet done
"""

import sys,os
import pandas as pd

def print_usage ():
	print("usage: visualize_stats.py solutions_list number_of_tophits")
	print("\tsolutions_list the revised csv file")
	print("\tnumber_of_tophits Number of hit included in pdf generation")
	print("eg: visualize_stats.py solutions_density1/fit_logs_revised.csv 100")
	sys.exit()
	
if __name__ == "__main__":
	if len(sys.argv) < 3:
		print_usage()

	fitcsv = sys.argv[1]
	nohits = int(sys.argv[2])
	
	print("Plotting R statistics for {:s} from {:d} top hits".format(fitcsv, nohits))
		
	