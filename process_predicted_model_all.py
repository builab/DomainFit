#!/usr/bin/python
# # -*- coding: utf-8 -*-

"""
@Authors Max Tong & HB
@Require phenix 1.20
@v0.2 Update with multiprocessing and phenix lddt option
"""
import sys,os,time,platform
import Bio
import os.path,re
from Bio.PDB import PDBParser
from Bio.PDB import PDBIO
from datetime import datetime
import subprocess, multiprocessing

script_dir=os.path.dirname(os.path.realpath(__file__))


def print_usage ():
	print("usage: python process_predicted_model_all.py <inputDir> <outputDir> <noProc> options")
	print("eg: python process_predicted_model_all.py input domains 10 maximum_rmsd=.8 maximum_domains=8")
	sys.exit()
	
def execute(cmd):
	print(f'start {cmd}', datetime.now())
	return subprocess.call(cmd,shell=True)
	
def write_domains(input_pdb, output):
	parser=PDBParser(QUIET=True)
	protein = parser.get_structure('Y', input_pdb)
	log = open(output, "w")
	
	chain_id = 1
	for chain in protein[0]:
		#print ("Chain " + str(chain))
		# Print first & last residues
		first = last = next(chain.get_residues(), None)
		for last in chain.get_residues():
			pass
		#log.write("D{:s}\t{:d}-{:d}\n".format(chain.get_id(), first.get_id()[1], last.get_id()[1]))	
		log.write("D{:d}\t{:d}-{:d}\n".format(chain_id, first.get_id()[1], last.get_id()[1]))
		chain_id += 1	
	
	log.close()	

if __name__ == "__main__":
	# Default option seems to work very well
	default_options = "maximum_rmsd=.8 maximum_domains=8"

	if len(sys.argv) < 4 :
  		print_usage()

	if len(sys.argv) == 4 : 
   		options = default_options
	else:
		logs=[]
		options = ' '.join(sys.argv[4 : ])  

	
	input_dir = sys.argv[1]
	output_dir = sys.argv[2]
	threads = int(sys.argv[3])

	os.makedirs(output_dir, exist_ok=True)


	print(f'Process_predicted_model options: {options}')

	cmds=[]
	for pdb in os.listdir(input_dir):
		if pdb.endswith(".pdb"):
			ext = ".pdb"
		elif pdb.endswith(".cif"):
			ext = ".cif"
		else:
			continue
			
		# Add them to the command list
		out_pdb = re.sub("{}$".format(ext), '_domains', pdb)			
		cmds.append(f'phenix.process_predicted_model {input_dir}/{pdb} processed_model_prefix={output_dir}/{out_pdb} {options}')
		
	# Execute command list
	count = threads
	with multiprocessing.Pool(processes=count) as pool:
		results = pool.map(execute, cmds)

	# Writing info
	for pdb in os.listdir(output_dir):
		if pdb.endswith("domains.pdb"):  
			print("Writing info for " + pdb)
			protein_basename = os.path.basename(pdb).replace('_domains.pdb','')
			write_domains(os.path.join(output_dir, pdb), os.path.join(output_dir, f"{protein_basename}.domains"))