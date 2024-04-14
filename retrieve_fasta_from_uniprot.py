#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 00:33:50 2020
Last updated Jul 26, 2020

Script to retrieve separate FASTA file from a list of uniprot ID

@author: Huy Bui
"""
import urllib, argparse, time, urllib.request

""" Retrieve the fasta sequence from uniprot ID and write to an output file """
def retrieveFasta(pID, outfile):
	print('Retrieving ' + pID)
	response = urllib.request.urlopen("http://www.uniprot.org/uniprot/" + pID + ".fasta").read()
	content = response.decode('utf-8')
	outhandle = open(outfile, 'w')
	outhandle.write(content)
	outhandle.close()
	
if __name__=='__main__':
	parser = argparse.ArgumentParser(description='Retrieve sequence of Uniprot ID')
	parser.add_argument('--id', help='Input of ID list',required=False)
	parser.add_argument('--ilist', help='Input of ID list',required=False)
	parser.add_argument('--odir', help='Output directory location',required=True)

	args = parser.parse_args()
	
	if args.id is None and args.ilist is None:
		   parser.error("Require either --id or --ilist")

	if args.id is not None and args.ilist is not None:
		   parser.error("Use either --id or --ilist")
		   
	outdir = args.odir

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
			out = outdir + '/' + line + '.fasta'
			retrieveFasta(line, out)
		time.sleep(5)
		
	if useList == 1:
		list.close()
