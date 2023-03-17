#!/usr/bin/python
# # -*- coding: utf-8 -*-

"""
@Authors Max Tong & HB
"""

# Python open a map
print("WARNING: Only work with Chimerax 1.5 and up")

import sys,os,time
import os.path

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
		best_fit = [f]
		
from chimerax.map_fit.search import save_fits
print ('Writing %s' % outFit)
save_fits(session, best_fit, outFit)
run(session, 'save %s/%s.png width 1500 super 3' % (output_dir, model_basename))

# runscript /storage2/Thibault/Max/ProteinAnalysis/fit_in_chimerax.py /storage2/Thibault/Max/test_parsing /storage2/Thibault/Max/test_parsing C1C2_MAP_only_erase.mrc Q22DM0.pdb