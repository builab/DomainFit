#!/usr/bin/python
# # -*- coding: utf-8 -*-

"""
@Authors Max Tong & HB
@Require ChimeraX 1.5 with proper excecutable
"""
# Usage
# python getPDBs.py <outputDir> <minThreshold> <maxThreshold> <options>

# Output
# Saved pdbs in the given <outputDir>
# csv file with all proteins that were not found in the alphafold database

# Function
# Creates a UI for the user to select the given .xlsx file that can be used to determine which desired columns to be worked with.
# NOTE: .xlsx files must be saved as EXCEL WORKBOOKS to be compatible with the code. Otherwise, an error will be thrown.
# Load columns --> Loads all columns in the selected sheet. The first column of the file should be the accession numbers and the following should be the RMSD values used for Abundance threshold pruning
# Submit columns --> Submits all of the selected columns to be used in processing the list

# TODO: Give an option as to whether to prune the list based on Abundance Thresholds or Not
# TODO: Make a generalize solution (csv )

from tkinter import messagebox
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import wget
import csv
import sys,os,time
from datetime import datetime
script_dir=os.path.dirname(os.path.realpath(__file__))

def print_usage ():
    print("usage: python getPDBs.py <outputDir> <minThreshold> <maxThreshold> options")
    sys.exit()

if len(sys.argv) < 2 :
    print(len(sys.argv))
    print_usage()
else:
    output_dir = sys.argv[1]
    lowerAbundanceThreshold = sys.argv[2]
    upperAbundanceThreshold = sys.argv[3]
    options = sys.argv[4]

class ColumnSelectorUI:
    def __init__(self, master):
        self.master = master
        self.file_path = ''
        self.sheet_names = []
        self.column_names = []
        self.selected_columns = []


        # Create UI elements
        self.title_label = tk.Label(master, text="Select columns to work with:")
        self.title_label.pack()

        self.column_listbox = tk.Listbox(master, selectmode=tk.MULTIPLE)
        self.column_listbox.pack()

        self.load_button = tk.Button(master, text="Load Columns", command=self.load_columns)
        self.load_button.pack()

        self.submit_button = tk.Button(master, text="Submit Columns", command=self.submit_selection)
        self.submit_button.pack()

        # Add options for file type
        self.file_type_label = tk.Label(master, text="Select file type:")
        self.file_type_label.pack()

        self.file_type_optionmenu_var = tk.StringVar(master)
        self.file_type_optionmenu_var.set(".xlsx")
        self.file_type_optionmenu = tk.OptionMenu(master, self.file_type_optionmenu_var, ".csv", ".xlsx")
        self.file_type_optionmenu.pack()

        # Add options for sheets
        self.sheet_label = tk.Label(master, text="Select sheet:")
        self.sheet_label.pack()

        self.sheet_optionmenu_var = tk.StringVar(master)
        self.sheet_optionmenu = tk.OptionMenu(master, self.sheet_optionmenu_var, "")
        self.sheet_optionmenu.pack()

        # Set up event listener for file type change
        self.file_type_optionmenu_var.trace("w", self.file_type_changed)

    def file_type_changed(self, *args):
        if self.file_type_optionmenu_var.get() == ".xlsx":
            # Ask user to select an xlsx file
            self.file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
            # Get sheet names from xlsx file
            self.sheet_names = pd.ExcelFile(self.file_path).sheet_names
            
        elif self.file_type_optionmenu_var.get() == ".csv":
            # Ask user to select a csv file
            self.file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
            # Get sheet names from csv file
            self.sheet_names = pd.read_csv(self.file_path, nrows=0).columns.tolist()

        # Update sheet optionmenu
        self.sheet_optionmenu.destroy()
        try:
            self.sheet_optionmenu = tk.OptionMenu(self.master, self.sheet_optionmenu_var, *self.sheet_names)
        except Exception as e:
            self.sheet_name = None
        self.sheet_optionmenu.pack()

    def load_columns(self):
        # Clear listbox
        self.column_listbox.delete(0, tk.END)

        # Load column names from file
        if self.file_type_optionmenu_var.get() == ".xlsx":
            sheet_name = self.sheet_optionmenu_var.get()
            self.sheet_name = sheet_name
            df = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
            self.column_names = list(df.columns)
        elif self.file_type_optionmenu_var.get() == ".csv":
            df = pd.read_csv(self.file_path)
            self.column_names = list(df.columns)

        # Add column names to listbox
        for column_name in self.column_names:
            self.column_listbox.insert(tk.END, column_name)
    def submit_selection(self):

        # Get selected columns
        selected_indices = self.column_listbox.curselection()
        self.selected_columns = [self.column_listbox.get(idx) for idx in selected_indices]

        if len(self.selected_columns) < 1:
            messagebox.showerror("Error", "No columns selected")
            return
        
        # Show selected columns
        selected_columns = list(selected_indices)
        df = pd.ExcelFile(self.file_path).parse(sheet_name=self.sheet_name, usecols=selected_columns, skiprows=3)
        
        df['mean'] = df.iloc[:, 1:len(selected_columns)].mean(axis = 1)
        x = df['mean'] > float(lowerAbundanceThreshold)
        df = df[x]
        x = df['mean'] < float(upperAbundanceThreshold)
        df = df[x] 

        # Find curated list of protein accession names
        pdbs = df.iloc[:,0].apply(lambda x: x.split()[0])

        notFound = []

        # Search in Alphafold if they exist and download said pdbs
        for pdb in pdbs:
            if type(pdb) is list:
                row = pdb[0]
            url = f"https://alphafold.ebi.ac.uk/files/AF-{pdb}-F1-model_v4.pdb"
            try:
                filename = wget.download(url, out=output_dir)
                os.rename(filename, f"{output_dir}/{pdb}.pdb")
            except Exception as e:
                # print(f"Alphafold protein {pdb} not found")
                notFound.append(pdb)
        
        

        with open(f"{output_dir}/Proteins_Not_Found.csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for pdb in notFound:
                writer.writerow([pdb])
        
        messagebox.showinfo("Complete", f"All pdbs have been downloaded to {output_dir}")


        # Reset UI
        self.column_listbox.selection_clear(0, tk.END)
        self.selected_columns = []

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Get PDBs From AlphaFold")
    root.geometry("400x300")
    # frame = tk.Frame(root)
    # frame.pack(fill='both', expand=True)
    # frame.pack_propagate(0)
    app = ColumnSelectorUI(root)
    root.mainloop()
