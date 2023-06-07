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
3. **Python** 2.7 or higher
4. **Rscript** 3.6.3 or higher  
        fdrtool
        psych
## Workflow

Master Script:
- chimerax_domain_fit.py

Subordinate Scripts:
- Process_predicted_model_all.py
- Save_domain_all.py
    - Save_domain_single.py
- Fit_all_domain_in_chimerax.py
    - Fit_in_chimerax.py

### process_predicted_model_all.py
Generating domain pdbs: Parse automatically using phenix.process_predicted_model, need to tweak LDDT threshold, or domain size if you know about the size of the density.

> Input: Alphafold pdbs
> Output: Domain-parsed pdbs 

### save_domain_all.py
Saving domain-separated pdbs: Parse through domains and save domains into individual pdbs. Additional screenshots are taken of each domain.

> Input: Domain-parsed pdbs
> Output: Domain-separated pdbs + pngs

### fit_all_domain_in_chimerax.py
Fitting using ChimeraX: Take each domain and fit it into the density automatically using ChimeraX built in function fitmap. Output pdb saves the fit orientation. Additional screenshots are taken of each domain fitted into the density. A csv file is generated to document all hits and their respective values (correlation, overlay, overlap, etc.). Default map level is set to 0.034 and a map resolution of 5 Å

> Input: Domain-separated pdbs + protein density
> Output: Best-hit pdbs + pngs + csvs


Picking the highest hit: Best fits are further filtered to determine the top hits in terms of correlation_mean (Corr_mean), p-value (PValue), and difference between best hit and the second hit (Diff). Final csv is sorted by Diff and Corr_mean. All values are to 4 decimals (subject to change as p-values are often much longer).
> Input: csvs
> Output: fit_logs_revised.csv

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

### getPDBs.py
Installing Alphafold pdbs: UI for installing Alphafold pdbs provided a .csv or .xlsx file with a list of protein Accession Numbers (Uniprot)

Provided columns of mass spectrometry RMSD values, has an additional option to prune the list

> Input: list of Accession Numbers and output directory
> Output: Alphafold pdbs 

### visaulize_noRes.py
Visualizing domain features: Generates histograms based on the number of residues per domain

> Input: **\<processed>** directory

> Output: histogram
