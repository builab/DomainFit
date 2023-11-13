#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2023

Retrieve PAE file from a list of UniprotID
Note: Not working on Mac because of wget


@author: Max Tong, McGill University
"""
import wget
import sys,os,time
from datetime import datetime
script_dir=os.path.dirname(os.path.realpath(__file__))
import subprocess
import csv

def print_usage ():
    print("usage: getAlphaFoldPAEs.py <inputFile> <outputDir>")
    sys.exit()

if not len(sys.argv) == 2 :
    print_usage()
else:
    input_file = sys.argv[1]
    output_dir = sys.argv[2]

with open(input_file, 'r') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        if type(row) is list:
            row = row[0]
        url = f"https://alphafold.ebi.ac.uk/files/AF-{row}-F1-predicted_aligned_error_v4.json"
        filename = wget.download(url, out=output_dir)
        os.rename(filename, f"{output_dir}/{row}.json")