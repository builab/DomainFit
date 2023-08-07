#!/usr/bin/python
# # -*- coding: utf-8 -*-

"""
@Authors ChatGPT
"""

import os
import requests
from Bio import SeqIO

# Path to the fasta file containing Uniprot IDs
fasta_file_path = "test.fasta"

# Directory to save downloaded PDB files
pdb_directory = "pdb_files"
os.makedirs(pdb_directory, exist_ok=True)

# AlphaFold API endpoint
alphafold_api_url = "https://alphafold.ebi.ac.uk/queries"

def fetch_pdb_by_uniprot(uniprot_id):
    payload = {
        "input": {
            "seq": {
                "sequence": "",
                "accession": uniprot_id
            }
        }
    }

    response = requests.post(alphafold_api_url, json=payload)
    response_data = response.json()

    if "model" in response_data:
        pdb_data = response_data["model"]["prody_pdb"]
        return pdb_data
    else:
        return None

# Parse the fasta file and fetch PDB files
for record in SeqIO.parse(fasta_file_path, "fasta"):
    uniprot_id = record.id
    print(uniprot_id)
    pdb_data = fetch_pdb_by_uniprot(uniprot_id)

    if pdb_data:
        pdb_file_path = os.path.join(pdb_directory, f"{uniprot_id}.pdb")

        with open(pdb_file_path, "w") as pdb_file:
            pdb_file.write(pdb_data)

        print(f"Downloaded PDB for {uniprot_id} to {pdb_file_path}")
    else:
        print(f"No PDB data available for {uniprot_id}")

print("All PDB files downloaded successfully.")
