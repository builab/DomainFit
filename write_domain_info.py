#!/usr/bin/python
# # -*- coding: utf-8 -*-

"""
@Authors Max Tong & HB
@Require ChimeraX
Eliminate domain smaller than a minLength or larger than a maxLength
save
"""
from chimerax.core.commands import run
import os.path
import sys,os

input_pdb = sys.argv[1]
output_dir = sys.argv[2]

if len(sys.argv) < 3:
	min_length = 50
else:
	min_length = int(sys.argv[3])

if len(sys.argv) < 4:
	max_length = 1000
else:
	max_length = int(sys.argv[4])

model = run(session, 'open %s' % input_pdb)[0]

model_basename = os.path.basename(input_pdb).replace('_domains.pdb','')

print('Saving chains between ' + str(min_length) + ' and ' + str(max_length) + ' aa')

log_file = output_dir + '/domain_logs.txt'
log = open(log_file, "a")

# Check operating system
useMacOs = 0
if sys.platform == 'darwin': #MacOS
	useMacOs = 1
	
for chainNo in range(model.num_chains):
	noResidues = int(model.chains[chainNo].num_residues)
	print('Chain ' + model.chains[chainNo].chain_id + ' has ' + str(model.chains[chainNo].num_residues))
	log.write('%s,%s,%d\n' % (model_basename, model.chains[chainNo].chain_id, noResidues))
	if noResidues < min_length or noResidues > max_length:
		print('--> Skip due to length')
		continue		
	print('Saving chain ' + model.chains[chainNo].chain_id)
	run(session, 'select /%s' % model.chains[chainNo].chain_id)
	output_pdb = output_dir + '/' + model_basename +  '_domain' + str(chainNo) + '.pdb'
	run(session, 'save %s selectedOnly true models #%d' % (output_pdb, 1))
	if useMacOs == 0 : #MacOS
		output_png = output_dir + '/' + model_basename +  '_domain' + str(chainNo) + '.png'
		run(session, 'save %s width 1000 super 3' % output_png)
	

# runscript save_domain_single.py /storage2/Thibault/Max/test_parsing Q22DM0_processed.pdb
#/storage2/Thibault/Max/test_parsing/output 50 1000

log.close()
