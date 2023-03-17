#!/usr/bin/python

from chimerax.core.commands import run
import os.path
import sys,os

input_dir = sys.argv[1]
output_dir = sys.argv[2]
modelFile = sys.argv[3]

inputModel = os.path.join(input_dir, modelFile) 
model = run(session, 'open %s' % inputModel)[0]

# outputDir = '/Users/kbui2/Desktop/tip_CP'
modelName = os.path.basename(inputModel)

print(range(model.num_chains))
for chainNo in range(model.num_chains):
	print('Saving chain ' + model.chains[chainNo].chain_id)
	run(session, 'select /%s' % model.chains[chainNo].chain_id)
	outputPdb = output_dir + '/' + modelName.replace('_domains.pdb', '_domain') + str(chainNo) + '.pdb'
	run(session, 'save %s selectedOnly true models #%d' % (outputPdb, 1))
	
# runscript save_domain_single.py /storage2/Thibault/Max/test_parsing/output /storage2/Thibault/Max/test_parsing Q22DM0_processed.pdb
