#!/usr/bin/env python3
# # -*- coding: utf-8 -*-

"""
@Authors Max Tong & Huy Bui
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
cmd = f'Rscript {script_dir}/pval_from_solutions.R {outlist} correlation_about_mean'
print(f'start {cmd}', datetime.now())
status = subprocess.call(cmd, shell=True)
# We don't extract P-values here anymore because pandas is broken in ChimeraX
print(f'end {cmd}', datetime.now()) 

# Extract the unique temp log path passed as the 7th argument
# We use -1 to get the last argument passed, which is our temp log path
temp_log_path = sys.argv[-1] 

try:
    with open(temp_log_path, "w") as log:
        # Find the path to the P-value CSV created by the Rscript
        pval_file = os.path.join(output_dir, model_basename + '_pvalues.csv')
        
        # Write basic metrics + the path to the P-value file
        log.write('%s,%d,%0.4f,%0.4f,%0.4f,%0.4f,%0.4f,%s\n' % (
            model_basename, 
            model.chains[0].num_existing_residues, 
            best_corr, 
            second_best_corr, 
            difference, 
            worst_best_corr, 
            range,
            pval_file
        ))
    print(f"Worker finished: {model_basename}")
except Exception as e:
    print(f"Worker failed to write log: {e}")