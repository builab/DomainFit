#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2023
Modified 2024/06 to compatible with Mac like getAlphaFoldPDBs.py

Retrieve PAE file from a list of UniprotID
Note: Not working on Mac because of wget


@author: Max Tong, McGill University
"""

import argparse
import os
import urllib.error
import urllib.request
import time

BASE_URL = "https://alphafold.ebi.ac.uk/files/AF-{}-F1-predicted_aligned_error_v4.json"


def retrieve_af_file(uniprot_id, outdir, ignore_existing):
    print('Retrieving', uniprot_id, '.json')

    outfile = os.path.join(outdir, f"{uniprot_id}.json")
    
    if os.path.exists(outfile) and ignore_existing:
        print(f'Skipping {uniprot_id} due to existing file')
        return 1
    
    try:
        response = urllib.request.urlopen(BASE_URL.format(uniprot_id)).read().decode('utf-8')
    except urllib.error.HTTPError as e:
        print('Error:', uniprot_id)
        return 0
    
    with open(outfile, 'w') as outhandle:
        outhandle.write(response)
    
    return 1


def main():
    parser = argparse.ArgumentParser(description='Retrieve sequences of UniProt IDs')
    parser.add_argument('--id', help='Input UniProt ID', required=False)
    parser.add_argument('--ilist', help='Input ID list', required=False)
    parser.add_argument('--odir', help='Output directory location', required=True)
    parser.add_argument('--ignore_existing', help='Ignore existing file (1/0)', required=False, default='0')
    args = parser.parse_args()
    
    if not args.id and not args.ilist:
        parser.error("Require either --id or --ilist")
    
    if args.id and args.ilist:
        parser.error("Use either --id or --ilist")
    
    outdir = args.odir
    os.makedirs(outdir, exist_ok=True)
    
    ignore_existing = int(args.ignore_existing)
    
    use_list = args.ilist is not None
    input_list = open(args.ilist, 'r') if use_list else [args.id]
    
    missing = []
    
    with open('missingAFjson.log', 'w') as log:
        for uniprot_id in input_list:
            uniprot_id = uniprot_id.strip()
            if uniprot_id:
                res = retrieve_af_file(uniprot_id, outdir, ignore_existing)
                if res == 0:
                    missing.append(uniprot_id)
                    
    if use_list:
        input_list.close()
    
    print("\nThere are {} missing AlphaFold json written in missingAFjson.log".format(len(missing)))
    
    with open('missingAFjson.log', 'a') as log:
        log.write("\n".join(missing))
    
if __name__ == '__main__':
    main()
