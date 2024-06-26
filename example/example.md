# DomainFit example

## Goal: Find the identity of the domain beloging to [density2.mrc](density2.mrc)


## Step 1: Download the AlphaFold model from AFDB 

Fetching AlphaFold PDBs from a list of UniprotID. The [`list_proteins.csv`](list_proteins.csv) is a shortened list with 164 proteins. The output will be all the PDB models downloaded from AFDB in the pdb_files directory

	getAlphaFoldPDBs.py --ilist list_proteins.csv --odir pdb_files
	
If there are missing proteins, they will be recorded in `missingAF.log` file. The missing proteins tend to be big proteins > 100kD. In this case, there are 4 missing proteins. You can predict them using ColabFold or AlphaFold. 

Note: For the sake of the example, just ignore it and skip to Step 2. Otherwise, continue to Step 1b to predict all the missing proteins.

> I7M688  
I7LWA5  
I7LU47  
Q230X9

## Step 1b: Predict the missing proteins using Colabfold
If you predict these proteins using Colabfold notebook, download all the result files and move in Colabfold_output (no subfolders).
Otherwise, using localcolabfold [https://github.com/YoshitakaMo/localcolabfold], it is easy to run colabfold in batch

First, download all the fasta files listed in the `missingAF.log` file and then predict all the fasta files in batch.
  
	mkdir fasta colabfold_pred
	retrieve_fasta_from_uniprot.py --ilist missingAF.log --odir fasta
	colabfold_batch fasta colabfold_pred

Now, copy and rename all the rank_001 pdb files (top rank out of 5 predictions from ColabFold) to the downloaded AlphaFold folder

	copy_colabfold_predictions.py colabfold_pred pdb_files


## Step 2: Automatically divide the PDBs into domains
Note: Phenix must be sourced if it is not in the path
This step segments the PDB in `pdb_files` directory automatically into domains and writes the domain info (.domains) in the `domains` directory with the DPAM format.

	process_predicted_models_adaptive.py pdb_files domains 10 split_model_by_compact_regions=True

In this case, using 10 processors speeds up the calculation a lot.
Example of a domain info file: `Q238X3.domains`

> D1	10-21  
D2	32-157  
D3	183-223


## Step 3: Saving domain-separated PDBs to using domain info files from the previous step.

We will save one PDB for each domain in `single_domains` directory. In this step, we also filter all domains < 40 amino acids & > 1000 amino acids (the upper range is for the case the domain segmentation fails) using 10 processors.

	save_domains_from_info.py pdb_files domains single_domains 40 1000 10

This process writes out 344 PDB files of single domains in `single_domain` directory.

## Step 4: fit_domains_in_chimerax.py
Fitting all domains from `single_domains` folder in the `density2.mrc` using ChimeraX: Take each domain and fit it into the density automatically using ChimeraX built-in function *fitmap* in no screen mode. The script writes best fitted position of PDB for each domain in `solutions` folder. The script also generates a non-sorted csv file and sorted csv file (`solutions/fit_logs.csv` and `solutions/fit_logs_revised.csv`) to document all hits and their respective values (number of residues, correlation, overlap, correlation about mean, p-value etc.). You need to determine the map level from ChimeraX (here 0.886) and the resolution of the search (here 4 Å). We use 10 processors here but if your machine has more, use more since ChimeraX will be run in no screen mode and require small memory for the small density.

	fit_domains_in_chimerax.py single_domains solutions density2.mrc 0.886 4 200 10

Alternatively, if you want to see how the complete AlphaFold2 models fit into the density, you can run this script for all PDBs in `pdb_files` directory. You might got lucky if the tertiary structure of the AlphaFold2 model is good. With this, you need to use more initial search placement (400-800) and also use a bigger segmented density. Since here it is only a demonstration, just run the command below to see if you found the protein.

	fit_domains_in_chimerax.py pdb_files_ solutions_complete density2.mrc 0.886 4 400 10
	

## Step 5: Analysing results

### Visualize the p-value & correlations
You can look at the `solutions/fit_logs_revised.csv` in Excel for details. For a quick visualization of the overall fitting

	visualize_fit_stats.py solutions/fit_logs_revised.csv
	
	
A graph of -log10(pvalue) and -log10(BenjaminiHochberg_adjusted_pvalue) vs. Normalized correlation coefficient should show up. The graph is also saved as `solutions/summaryplot.eps`. In this case, the top 2 hits (right top corner) are clearly distinct from other solutions. So, they are likely paralogs.


![summaryplot](https://github.com/builab/DomainFit/blob/main/example/summaryplot.png?raw=true)


### Visualize the top hits in ChimeraX
Generate a .cxc file to load the top hits for visualization in ChimeraX. Here, we choose to load only the top 5 hits with the minimum size of 80 amino acids. Size filtering is helpful in filtering small domains fitting wrongly with good correlations.

	load_tophits_in_chimerax.py density2.mrc solutions 2 80

ChimeraX is supposed to open from the terminal. If it is not, open the `load_tophits.cxc` using ChimeraX manually. The domains are sorted by rank in ChimeraX, #2 = rank 1, #3 = rank 2, etc. As you can clearly see, the top 2 hits are paralogs (PACRG paralogs)


![summaryplot](https://github.com/builab/DomainFit/blob/main/example/tophits.png?raw=true)


### Filter the solution list file size
Generate a new .csv file with a minimum size in amino acids filtering. Filter all domains < 100 amino acids. The output .csv will contain NO domain with a size < 100 amino acids. A new solution list file `solutions_example/fit_logs_revised_min80.csv` is created in this case.

	filter_solution_list.py solutions/fit_log_revised.csv 80
	
	
## Step 6: Clean up results
Once you are done analyzing and found your data, you can clean up the data. The script reads `fit_log_revised.csv` file in the provided directory and only keeps the top X (10 in this case) hits.

	clean_up_solutions.py solutions 10
