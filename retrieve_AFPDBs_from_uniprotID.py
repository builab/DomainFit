#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 00:33:50 2020
Last updated Jul 26, 2020

Script to retrieve separate AF file from a list of uniprot ID

@author: kbui2
"""
import urllib, argparse, time, urllib.request
import os

""" Retrieve the fasta sequence from uniprot ID and write to an output file """
def retrievePDB(pID, outfile):
	print('Retrieving ' + pID)
	try:
		response = urllib.request.urlopen("https://alphafold.ebi.ac.uk/files/AF-" + pID + "-F1-model_v4.pdb").read()
	except urllib.error.HTTPError as e:
		print('Error: ' + pID)
		return
				
	content = response.decode('utf-8')
	outhandle = open(outfile, 'w')
	outhandle.write(content)
	outhandle.close()
	
if __name__=='__main__':
	parser = argparse.ArgumentParser(description='Retrieve sequence of Uniprot ID')
	parser.add_argument('--id', help='Input of ID list',required=False)
	parser.add_argument('--ilist', help='Input of ID list',required=False)
	parser.add_argument('--odir', help='Output directory location',required=True)
	parser.add_argument('--ignore_existing', help='Ignore existing file (1/0)',required=False,default='0')
	
	args = parser.parse_args()
	
	if args.id is None and args.ilist is None:
		   parser.error("Require either --id or --ilist")

	if args.id is not None and args.ilist is not None:
		   parser.error("Use either --id or --ilist")
		   
	outdir = args.odir
	ignore_existing = int(args.ignore_existing)

	useList = 1
	if args.id is None:
		useList = 1
		list = open(args.ilist, 'r')
	else:
		useList = 0
		list = {args.id}
		
	
	
	for line in list:
		line = line.strip()
		if line:
			out = outdir + '/' + line + '.pdb'
			if os.path.exists(out) and ignore_existing == 1:
				print('Skip ' +line + ' due to existing file')
				continue
				
			retrievePDB(line, out)
		time.sleep(2)
		
	if useList == 1:
		list.close()