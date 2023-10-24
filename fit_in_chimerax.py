#!/usr/bin/python
# # -*- coding: utf-8 -*-

"""
@Authors Max Tong & HB
# Better use re.sub for replace .pdb or .cif
"""

# Python open a map
print("WARNING: Only work with Chimerax 1.5 and up")

import sys,os,time
import os.path
import inspect
from datetime import datetime
import subprocess
script_dir=os.path.dirname(os.path.realpath(__file__))


input_model = sys.argv[1]
output_dir = sys.argv[2]
input_map = sys.argv[3]
map_level = float(sys.argv[4])
resolution = float(sys.argv[5])
search = int(sys.argv[6])


# This load to ChimeraX (still required interface)
from chimerax.core.commands import run
map = run(session, 'open %s' % input_map)[0]

# Set threshold
run(session, 'volume #1 level %0.4f transparency 0.5 step 1' % map_level)

model = run(session, 'open %s' % input_model)[0]

model_basename = os.path.basename(input_model)
model_basename = model_basename.replace('.pdb', '').replace('.cif', '')

print('Reading ' + input_model)

outlist = output_dir + '/' + model_basename + '.csv'

print(outlist)

from chimerax.map_fit.fitcmd import fitmap
fits = fitmap(session, model, map, resolution=resolution, search=search, placement='sr', log_fits=outlist)

# logFits=outlist
#print(fits)

# Save the best fit of each molecule
max_corr = 0
best_fit = []
outFit = output_dir + '/' + model_basename +  '_bestfit.pdb'


for f in fits:
	if f.correlation() > max_corr:
		max_corr = f.correlation()
		#print(inspect.getmembers(f))
		best_fit = [f]	

# Determine best fits
# Error to catch here to avoid empty solutions
try:
	print("cur best: ", fits[0].correlation())
	print("second best: ", fits[1].correlation())
	print("worst best: ", fits[len(fits)-1].correlation())
except IndexError:
	print(f'Something wrong with {input_model}')
	exit(0)

best_corr = fits[0].correlation()
second_best_corr = fits[1].correlation()
worst_best_corr = fits[len(fits)-1].correlation()
difference = best_corr - second_best_corr
range = best_corr-worst_best_corr


# Save session fits into csv
from chimerax.map_fit.search import save_fits
print ('Writing %s with correlation of %0.3f' % (outFit, max_corr))
save_fits(session, best_fit, outFit)

# Check operating system
useMacOs = 0
if sys.platform == 'darwin': #MacOS
	useMacOs = 1

if useMacOs == 0 :
	run(session, 'save %s/%s.png width 1500 super 3' % (output_dir, model_basename))

# Generate p_values

cmd = f'Rscript {script_dir}/pval_from_solutions.R {outlist}'

print(f'start {cmd}', datetime.now())
status = subprocess.call(cmd,shell=True)
if status != 0:
	print(f"Error in {cmd}.Exiting...")
print(f'end {cmd}', datetime.now()) 

# Extract p_values
import pandas as pd

pval_file = output_dir + '/' + model_basename +  '_pvalues.csv'

df = pd.read_csv(pval_file, sep='\s*,\s*')
# df.info()
df.dropna()
# print(df)
fit_no = df.loc[:, df.columns[0]][0]
corr_mean = df.loc[:, df.columns[26]][0]
pvalue = df.loc[:, df.columns[38]][0]
eta0 = df.loc[:, df.columns[39]][0]
# print(df.loc[:, df.columns[0]])

# Log best results into log_file
log_file = output_dir + '/fit_logs.txt'
log = open(log_file, "a")
log.write('%s,%d,%0.4f,%0.4f,%0.4f,%0.4f,%0.4f,%s,%0.4f,%0.4f\n' % (model_basename, model.chains[0].num_existing_residues, best_corr, second_best_corr, difference, worst_best_corr, range, fit_no, corr_mean, eta0, pvalue))
log.close()

# runscript /storage2/Thibault/Max/ProteinAnalysis/fit_in_chimerax.py /storage2/Thibault/Max/test_parsing /storage2/Thibault/Max/test_parsing C1C2_MAP_only_erase.mrc Q22DM0.pdb
