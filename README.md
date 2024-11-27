# DomainFit v1.2
Script to autofit domains in Chimerax

Goal: Provided a database of proteins and an isolated electron density, and find the protein that best fits the electron density geometrically

The program works for Linux and MacOS. For MacOS, a bit more modification is needed.

Update: 2024/06/15 It seems like parsing using PAE is a lot better. From AFDB, you can download the json in the same folder as the PDB. With ColabFold prediction, use the copy_colabfold_predictions.py. With AF3, it is a bit tricky. You can use the rank_AF3_models.py and copy_AF3_predictions.py but it is not as straight forward to use.

### Software and Package Requirements
1. **Phenix** v1.21 or higher (https://phenix-online.org/)
   
        phenix.process_predicted_model
   
2. **Chimerax** v1.5 or higher (https://www.cgl.ucsf.edu/chimera/)
   
        chimerax.fitmap

3. **Python** 3.10 or higher (Tested with the following)
	
        BioPython
        pandas (should be ok with both panda 1.0 and 2.0), numpy=2.0

6. **Rscript** 3.6.3 or higher  (https://cran.r-project.org/)

        fdrtool
        psych

## Installation

It is probably easier to use conda environment to avoid conflict with numpy version (1 & 2)

	conda create -n DomainFit python=3.10
	conda activate DomainFit

DomainFit Python Script

    git clone https://github.com/builab/DomainFit.git
    cd DomainFit
    chmod +x install.sh
    ./install.sh

For MacOSX, you have to modify the "chimerax_path" variable to your ChimeraX's binary file. e.g. /Applications/ChimeraX-1.5.app/Contents/MacOS/ChimeraX in "save_domains_from_info.py" and "fit_domains_in_chimerax.py" and "load_tophits_in_chimerax.py"
For Linux, install Biopython and numpy using pip

     pip install numpy==2.1
     pip install biopython==1.84
     pip install pandas==2.2.3
     pip install matplotlib


For MacOS and some Linux, you have to install pandas inside ChimeraX
Inside MacOS, open the terminal and type:

    /Applications/ChimeraX-1.7.1.app/Contents/bin/python3.11 -m pip install pandas

In Linux, look for the installed ChimeraX folder and open the terminal and type:

    /usr/lib/ucsf-chimerax/bin/python3.11  -m pip install pandas==2.2.3


R with fdrtool & psych

     Download R from https://cran.r-project.org/ and install
     Start R in a terminal
     $R
     >>install.packages('fdrtool', repos='http://cran.us.r-project.org')
     >>install.packages('psych', repos='http://cran.us.r-project.org')
     >> quit()
     Save workspace image? [y/n/c]: n



Before usage

    source DOMAIN_FIT_DIR/source_env.sh
   
## Workflow

Scripts:
- getAlphaFoldPDBs.py
- process_predicted_models.py
- process_predicted_models_using_pae.py
- save_domains_from_info.py
    - save_domain_single_from_info.py
- fit_domains_in_chimerax.py
    - fit_in_chimerax.py
    - pval_from_solutions.R
    
Other utility scripts:
- getAlphaFoldPAEs.py
- retrieve_fasta_from_uniprot.py
- copy_colabfold_predictions.py
- plot_domain_histogram.py
- filter_solution_list.py
- clean_up_solutions.py
- write_domain_info.py
- load_tophits_in_chimerax.py
- generate_Rplot.py

NOTE: Try out the [example](example/example.md) to test the workflow and correct installation.

### 1. Fetching AlphaFold PDBs 
Downloading from AFDB from a list of UniprotID

> Input: A list of UniprotIDs (1 per line) in text format (.txt or .csv)

> Output: A download directory containing pdbs downloading from alphafold.ebi.ac.uk

> Note: The list_proteins.csv must be free of special characters otherwise the program will complain about Unicode utf-8 error. The best way to prepare the file is to copy from a list to a text editor such as gedit.

	getAlphaFoldPDBs.py --ilist list_proteins.csv --odir pdb_files

 missingAF.log file will tell you which proteins do not have AlphaFold structure available.
 
 
 If you also want to get the PAE files for domain parsing using PAE graph later
 
 	getAlphaFoldPAEs.py --ilist list_proteins.csv --odir pdb_files


### 2. Parsing AlphaFold predicted models into domains
Generating domain pdbs: Parse automatically using phenix.process_predicted_model, can use default parameters or options.

> Input: AlphaFold predicted pdbs

> Output: Domain-parsed pdbs (*domains.pdb) and domain information files (*.domains)

> Note: Unfortunately, there are many *_remainder.seq file produced in the main folder. They will be deleted by the script at the end

	process_predicted_models.py pdb_files domains nocpu
	

Alternatively, you can also generate domains using PAE file (https://github.com/tristanic/pae_to_domains). Change the pae_graph_resolution from 1 to 5 for more domains.

	process_predicted_models_using_pae.py pdb_files domains nocpu pae_graph_resolution=1



### 3. Save each domain into single PDB file
Saving domain-separated pdbs using info from the previous step: Parse through domain info and save domains into individual pdbs. Additional screenshots are taken of each domain.

> Input: Domain-parsed pdbs, domain_info files folder

> Output: Domain-separated pdbs + pngs

	save_domains_from_info.py pdb_files domains single_domains minResidueNo maxResidueNo nocpu


### 4. Fit all domains into ChimeraX
Fitting using ChimeraX: Take each domain and fit it into the density automatically using ChimeraX built in function fitmap. Output pdb saves the fit orientation. Additional screenshots are taken of each domain fitted into the density. A CSV file is generated to document all hits and their respective values (correlation, overlay, overlap, etc.). The default map level is set to 0.034 and a map resolution of 5 Å. Make sure to change this value to the corresponding value for your density.

> Input: Domain-separated pdbs + protein density

> Output: Solutions with Best-hit pdbs + pngs + csvs

	fit_domains_in_chimerax.py inputDir outputDir inputMap mapLevel resolution searchNo noProcessor
 

## Additional Scripts


### clean_up_solutions.py
Clean up the solution after having a look at it

> Input: Best-hit pdbs + pngs + csvs

> Output: Clean up the solution folder keeping only top hits

	clean_up_solutions.py solution_dir numberTopHitsRetained


### plot_domain_histogram.py
Visualizing domain features: Generates histograms based on the number of residues per domain

> Input: **\<processed>** directory

> Output: histogram

	plot_domain_histogram.py domain_info_dir


### load_tophits_in_chimerax.py
Generate a .cxc file to load the top hits for visualization in ChimeraX.

> Input: density + solution_dir

> Output: .cxc file to open in ChimeraX

	load_tophits_in_chimerax.py density solutions_dir number_of_top_hit minsize


### filter_solution_list.py
Generate a new .csv file with a minimum size filtering

> Input: solution_dir/fit_log_revised.csv file

> Output: filtered csv file

	filter_solution_list.py solutions_list minsize
	
	
### visualize_fit_stats.py
Generate a new .eps plot of the fitting statistics from one fitting list with size filtering

> Input: solution_dir/fit_log_revised.csv file, minimum size in amino acids (default = 0)

> Output: solutions_dir/summaryplot.eps

	visualize_fit_stats.py solutions_list minsize


 ### visualize_solutions.py
 Generate a visual of top solutions from many searches

 > Input: solution directories of many densities, a .txt file containing the list of those directories

 > Output: eps file showing

	visualize_solutions.py solutions_csv_list cutoff_rank min_size outputPlot


### getAlphaFoldPAEs.py
Fetching AlphaFold predicted alignment error from a list of Uniprot IDs. Not used now but might be useful for other methods of domain parsing.

> Input: A list of Uniprot ID (1 per line) in text format (.txt or .csv)

> Output: A download directory containing PAEs downloading from alphafold.ebi.ac.uk

	getAlphaFoldPAEs.py --ilist list_proteins.csv --odir pdb_files --ignore_existing

### generate_Rplot.py
Generate PDF for the R-plot to see the statistical calculation for top hit domains.

> Input: solution_dir/fit_log_revised.csv file, number of top hits to plot.

> Output: A PDF file for each domain in the solution folder

 	generate_Rplot.py solution_dir/fit_log_revised.csv 10

## Citation
If you use DomainFit for your work, please cite the following preprint:
	
	Gao, J., Tong, M., Lee, C., Gaertig, J., Legal., T., Bui, K.H., (2024) DomainFit: Identification of Protein Domains in cryo-EM maps at Intermediate Resolution using AlphaFold2-predicted Models. Structure. Doi: https://doi.org/10.1016/j.str.2024.04.017

 
