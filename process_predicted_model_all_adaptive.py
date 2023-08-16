#!/usr/bin/python
# # -*- coding: utf-8 -*-

"""
@Authors Max Tong & HB
@Require phenix 1.20
@v0.2 In this version, you have no flexibility in choosing option. the maximum_domains = no_of_AA/100
assuming ~100AA per domain
TO DO: remove *.remainder_seq in source PDB folder
"""
import sys,os,time,platform,math
import Bio
import os.path,re
from Bio.PDB import PDBParser
from Bio.PDB import PDBIO
from datetime import datetime
import subprocess, multiprocessing

script_dir=os.path.dirname(os.path.realpath(__file__))


def print_usage ():
	print("usage: python process_predicted_model_all_adaptive.py <inputDir> <outputDir> <noProc> options")
	print("eg: python process_predicted_model_all_adaptive.py input domains 10 maximum_rmsd=.8")
	sys.exit()
	
def execute(cmd):
	print(f'start {cmd}', datetime.now())
	return subprocess.call(cmd,shell=True)

""" Write domain info"""	
def write_domains(input_pdb, output):
	parser=PDBParser(QUIET=True)
	protein = parser.get_structure('Y', input_pdb)
	log = open(output, "w")

	for chain in protein[0]:
		#print ("Chain " + str(chain))
		# Print first & last residues
		first = last = next(chain.get_residues(), None)
		for last in chain.get_residues():
			pass
		log.write("D{:s}\t{:d}-{:d}\n".format(chain.get_id(), first.get_id()[1], last.get_id()[1]))	
	
	log.close()	
	
""" Retrieve protein sequence length"""
def get_PDB_len(input_pdb):
	parser=PDBParser(QUIET=True)
	protein = parser.get_structure('Y', input_pdb)	
	for last in protein[0].get_residues():
		pass
	return last.get_id()[1]


if __name__ == "__main__":
	# Default option seems to work very well
	# Adaptive doesn't seem to do much
	default_options = "split_model_by_compact_regions = True"

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
		
		# Adaptive adjust maximum_domains
		no_residues = get_PDB_len(os.path.join(input_dir, pdb))
		no_domains = math.ceil(no_residues/100)
		print(f'{pdb} has {no_residues} residues')
		
		if "maximum_domains" not in options:
			adaptive_options = options + " maximum_domains=" + '{:d}'.format(no_domains)
			print(f'Running with adaptive option of {no_domains}')
		else:
			adaptive_options = options
			
		# Add them to the command list
		out_pdb = re.sub("{}$".format(ext), '_domains', pdb)			
		cmds.append(f'phenix.process_predicted_model {input_dir}/{pdb} processed_model_prefix={output_dir}/{out_pdb} {adaptive_options}')
	
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