#!/usr/bin/python
# # -*- coding: utf-8 -*-

"""
@Authors Max Tong & HB
Reads all the *.domains in the domain_info_dir and plot histogram of domain residues number
"""

from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
import os, sys
import subprocess
script_dir=os.path.dirname(os.path.realpath(__file__))


# Syntax
def print_usage ():
    print("usage: plot_domain_histogram.py domain_info_dir" )

# Ensures that there are 1 arguments
if len(sys.argv) < 1:
    print_usage()
else:
    domain_info_dir = sys.argv[1]

# d is the array contains the number of residues per domain
d = []

# Read all the domain info file & calculate number of residues
for file in os.listdir(domain_info_dir):
	if file.endswith(".domains"):
		df = pd.read_csv(domain_info_dir + '/' + file, sep="\t", header=None)
		domain_names = df[0]
		domain_ranges = df[1]
		for chainNo in range(len(domain_names)):
			noResidues = 0
			if ',' in domain_ranges[chainNo]:
				ranges = [x for x in domain_ranges[chainNo].split(',') if x.strip()]
				for x in ranges:
					r = [int(x) for x in x.split('-') if x.strip()]
					noResidues += r[1] - r[0]
			else:
				ranges = [int(x) for x in domain_ranges[chainNo].split('-') if x.strip()]
				noResidues = ranges[1] - ranges[0]
			print(file + " Chain " + str(chainNo) + " noRes " + str(noResidues))
			d.append(noResidues)
		


# Visualization part
(mu, sigma) = norm.fit(d)

#print(mu)
#print(sigma)
#print(d)

# An "interface" to matplotlib.axes.Axes.hist() method
n, bins, patches = plt.hist(x=d, bins=range(min(d), max(d) + 5, 5), color='#0504aa',
                            alpha=0.7, rwidth=0.85)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Number of residues')
plt.ylabel('Number of Domains')
plt.title('Histogram of domain size')
# plt.text(23, 45, r'$\mu=15, b=3$')
maxfreq = n.max()
# Set a clean upper y-axis limit.
y = norm.pdf( bins, mu, sigma)
y = y*n.sum()*10
# plt.plot(bins, y, 'r--', linewidth=2)
plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)

plt.show()