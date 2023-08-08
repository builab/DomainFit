# chimerax_domain_fit
Script to autofit domains in Chimerax

Goal: Provided a database of proteins and an isolated electron density, find the protein that best fits the electron density geometrically

## Installation

    $ git clone https://github.com/builab/chimerax_domain_fit.git

### Software and Package Requirements
1. **Phenix** v1.20.1 or higher
        phenix.process_predicted_model
2. **Chimerax** v1.4 or higher
        chimerax.fitmap
3. **Python** 3 or higher
4. **Rscript** 3.6.3 or higher  
        fdrtool
        psych
## Workflow

Master Script:
- chimerax_domain_fit.py

Subordinate Scripts:
- getPDBs.py
- process_predicted_model_all.py
- save_domain_all_from_info.py
    - save_domain_single_from_info.py
- fit_all_domains_in_chimerax.py
    - fit_in_chimerax.py
    - pval_from_solutions.R
    
Other utility scripts:
- getPAEs.py
- plot_domain_histogram.py
- clean_up_solutions.py
- write_domain_info.py

### getPDBs.py
Fetching AlphaFold PDBs from a list of Uniprot ID

> Input: A list of Uniprot ID (1 per line) in text format (.txt or .csv)
> Output: A download directory containing pdbs downloading from alphafold.ebi.ac.uk

	python getPDBs.py --ilist list_proteins.csv --odir pdb_files --ignore_existing

### process_predicted_model_all.py
Generating domain pdbs: Parse automatically using phenix.process_predicted_model, can use default parameters or options.

> Input: Alphafold pdbs
> Output: Domain-parsed pdbs (*domains.pdb) and domain information files (*.domains)

	python process_predicted_model_all.py pdb_files domains nocpu

### save_domain_all_from_info.py
Saving domain-separated pdbs using info from previous step: Parse through domain info and save domains into individual pdbs. Additional screenshots are taken of each domain.

> Input: Domain-parsed pdbs
> Output: Domain-separated pdbs + pngs

	python save_domain_all_from_info.py pdb_files domains single_domains minResidueNo maxResidueNo nocpu


### fit_all_domains_in_chimerax.py
Fitting using ChimeraX: Take each domain and fit it into the density automatically using ChimeraX built in function fitmap. Output pdb saves the fit orientation. Additional screenshots are taken of each domain fitted into the density. A csv file is generated to document all hits and their respective values (correlation, overlay, overlap, etc.). Default map level is set to 0.034 and a map resolution of 5 Å

> Input: Domain-separated pdbs + protein density
> Output: Solutions with Best-hit pdbs + pngs + csvs

	python save_domain_all_from_info.py pdb_files domains single_domains minResidueNo maxResidueNo nocpu


Picking the highest hit: Best fits are further filtered to determine the top hits in terms of correlation_mean (Corr_mean), p-value (PValue), and difference between best hit and the second hit (Diff). Final csv is sorted by Diff and Corr_mean. All values are to 4 decimals (subject to change as p-values are often much longer).
> Input: csvs
> Output: fit_logs_revised.csv

	python fit_all_domain_in_chimerax.py inputDir outputDir inputMap mapLevel resolution searchNo noProcessor


# Script Name: chimerax_domain_fit.py


# Usage: 
    python chimerax_domain_fit.py <input_dir> <proteinDensity> <minThreshold> <maxThreshold> <search> <threads>


Inputs:
- **\<input_dir>** -- Input directory with all alphafold pdbs
- **\<proteinDensity>** -- The intended protein density that is used for fit-mapping in chimera
- **\<minThreshold>** -- The minimum number of protein residues per domain
- **\<maxThreshold>** -- The maximum number of protein residues per domain
- **\<search>** -- The number of fits per domain
- **\<threads>** -- The number of multiprocessors used for parallel batch processing

Outputs:
- **\<PDBs>** -- Directory containing all input Alphafold pdbs
- **\<processed>** -- Directory containing all domain-processed pdbs
- **\<single_domains>** -- Directory containing all individual domain pdbs
    - PNGs of each domain
    - Text file that logs all domains and their residue number
- **\<solutions>** -- Directory containing:
    - Domain pdbs of best fit
    - csv files of all hits per domain
    - csv files containing p-values per domain
    - final overall fit_log_revised.csv to summarize best overall fits across all domains

Note:
If all domains have been parsed through once, it isn’t necessary to re-generate PDB domains. Refer to chimerax_domain_fit.py documentation to see how to skip process_predicted_model_all.py and save_domain_all.py

## Additional Scripts

#### clean_up_solutions.py
Clean up the solution after having a look at it

> Input: Best-hit pdbs + pngs + csvs
> Output: Clean up solution folder keeping only top hits


### plot_domain_histogram.py
Visualizing domain features: Generates histograms based on the number of residues per domain

> Input: **\<processed>** directory
> Output: histogram

### getPAEs.py
Fetching AlphaFold predicted alignment error from a list of Uniprot ID. Not used now but might be useful for other methods of domain parsing.

> Input: A list of Uniprot ID (1 per line) in text format (.txt or .csv)
> Output: A download directory containing PAEs downloading from alphafold.ebi.ac.uk

### write_domain_information.py
Writing domain information (should be done also during process_predicted_model_all.py)

> Input: **\<processed>** directory
> Output: domain information files (*.domains) using ECOD format 