#!/usr/bin/env python3
# # -*- coding: utf-8 -*-

"""
@Authors Max Tong & Huy Bui
@Require ChimeraX
Note: if the .domains not exist, save the entire file
"""
from chimerax.core.commands import run
import os.path
import sys,os
import pandas as pd

input_cif = sys.argv[1]
input_domain = sys.argv[2]
output_dir = sys.argv[3]

if len(sys.argv) < 4:
	min_length = 50
else:
	min_length = int(sys.argv[4])

if len(sys.argv) < 5:
	max_length = 1000
else:
	max_length = int(sys.argv[5])

model = run(session, 'open %s' % input_cif)[0]

if input_cif.endswith('cif'):
	model_basename = os.path.basename(input_cif).replace('.cif','')
else:
	model_basename = os.path.basename(input_cif).replace('.pdb','')

print('Saving chains between ' + str(min_length) + ' and ' + str(max_length) + ' aa')

# Check operating system
useMacOs = 0
if sys.platform == 'darwin': #MacOS
	useMacOs = 1
	
log_file = output_dir + '/domain_logs.txt'
log = open(log_file, "a")


df = pd.read_csv(f"{input_domain}", sep="\t", header=None)

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


	log.write('%s,%s,%d\n' % (model_basename, domain_names[chainNo], noResidues))

	if noResidues < min_length or noResidues > max_length:
		print('--> Skip due to length')
		continue
	print('Saving chain ' + domain_names[chainNo])
	run(session, f"sel #1:{domain_ranges[chainNo]}")
	output = output_dir + '/' + model_basename +  '_' + domain_names[chainNo] + '.pdb'
	run(session, 'save %s selectedOnly true models #%d' % (output, 1))
	
	if useMacOs == 0 : #MacOS
		output_png = output_dir + '/' + model_basename +  '_' + domain_names[chainNo] + '.png'
		run(session, 'save %s width 1000 super 3' % output_png)

log.close()
