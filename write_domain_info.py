#!/usr/bin/python
# # -*- coding: utf-8 -*-

"""
@Authors Max Tong & HB
@Require ChimeraX
Script to write domain informations from output of process_predicted_model_all.py
IMPORTANT: This script does not output empty file for the one is not parsed
"""
import Bio
import os.path
import sys,os
from Bio.PDB import PDBParser
from Bio.PDB import PDBIO
   

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
	
def print_usage ():
	print("Usage: python write_domain_info.py inputDir outputDir")
	sys.exit()

if __name__ == "__main__":
	if len(sys.argv) < 2 :
		print_usage()
        
	input_dir = sys.argv[1]
	output_dir = sys.argv[2]
	
	try:
		os.makedirs(output_dir, exist_ok = True)
	except OSError as error:
		print("Output dir exists")


	for pdb in os.listdir(input_dir):
		if pdb.endswith("domains.pdb"):  
			print("Processing " + pdb)
			protein_basename = os.path.basename(pdb).replace('_domains.pdb','')
			output = output_dir + '/' + protein_basename + '.domains'
			write_domains(input_dir + "/" + pdb, output)
    

