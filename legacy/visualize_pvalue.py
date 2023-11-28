#!/usr/bin/env python3
# # -*- coding: utf-8 -*-

"""
@Authors Jerry Gao, Huy Bui 
"""
# Usage
# python visualize_pvalue.py solutions_csv_list cutoff_rank min_size outputPlot plotMode
# output a graph is optional

# python visualize_pvalue.py solutions_csv_list.txt 5 40 plot.eps
# python visualize_pvalue.py solutions_csv_list.txt 5 60 plot.eps scatter

import sys,os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def print_usage ():
    print("usage: visualize_solutions.py solutions_csv_list cutoff_rank min_size outputPlot")
    print("solutions_csv_list: a text file having path to the fit_logs_revised.csv of each solution")
    print("cutoff_rank: maximum rank display (3)")	
    print("min_size (optional, default 40): amino acid size")
    print("outputPlot (optional) output plot in eps format")
    print("plotMode (optional, default radar) chart style of outputPlot")
    print("eg: visualize_pvalue_correlation.py solutions_csv_list.txt 5 40 plot.eps radar")
    sys.exit()

''' Get protein ranking for this list'''
def process_csv(fitcsv, minsize):
    if os.path.exists(fitcsv):
        df = pd.read_csv(fitcsv, header = 0)
    else:
        print("WARNING: {:s} does not exist. Check again!".format(fitcsv))
        exit(0)
        
    df['Protein'] = df['Domain'].replace('_D[0-9]+','', regex=True)
    df = df.loc[df['NoRes'] > minsize]	
    df.drop_duplicates(subset='Protein', inplace=True)

    df['-log(Pvalue)'] = -np.log10(df['Pvalue']) #Taking the -log(Pvalue)

    df_sub = df[['Protein', '-log(Pvalue)']].reset_index(drop=True).reset_index().copy()
    # print(df_sub)
    # Make index = 0 -> rank 1
    # df_sub['index'] = df_sub['index'] + 1
    df_sub = df_sub.reindex(columns={'Protein': 'Protein', '-log(Pvalue)': '-log(Pvalue)'})
    print(df_sub)
    return df_sub
    

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print_usage()

    csvlist = sys.argv[1]
    cutoff = 1
    minsize = 40
    plotmode = None
        
    if len(sys.argv) > 2:
        cutoff = int(sys.argv[2])
        minsize = int(sys.argv[3])
        
    if len(sys.argv) == 5:
        outEps = sys.argv[4]
        plotmode = 'radar'

    if len(sys.argv) == 6:
        plotmode = sys.argv[5]

    with open(csvlist) as f:
        sol_list = f.read().splitlines()
        
    #print(sol_list)
    count = 1
    df_rank = pd.DataFrame()
    for fitcsv in sol_list:
        df_fit = process_csv(fitcsv, minsize)
        new_col = f'rank{count}'
        df_fit.rename(columns={'-log(Pvalue)': new_col}, inplace=True)
        print(df_fit)
        if df_rank.empty:
            df_rank = df_fit
        else:
            df_rank = df_rank.merge(df_fit, on='Protein', how='inner')
        count = count + 1
        
    # Filtering 
    print(f'Filtering protein with cutoff rank of {cutoff}')
    protList = list()
    for i in range(count-1):
        new_col = f'rank{i+1}'
        cutoff_value = df_rank[new_col].nlargest(cutoff).iloc[-1]
        protList.extend(df_rank.loc[df_rank[new_col] >= cutoff_value, 'Protein'].tolist())
    protList = set(protList)
    
    # Need to replace either .txt or .csv to .csv	
    outcsv = 'rank_' + csvlist.replace('.txt', '.csv')
    print(f'Write ranking output file {outcsv}')
    df_rank = df_rank[df_rank['Protein'].isin(protList)]
    df_rank.to_csv(outcsv, index=False)
    

    # Plotting
    if not plotmode:
        exit()
    print(f'Plotting protein hits as {plotmode} chart!')
    # Reset pvalue < cutoff to 0
    for i in range(count-1):
        new_col = f'rank{i+1}'
        cutoff_value = df_rank[new_col].nlargest(cutoff).iloc[-1]
        # print (f'Cutoff for {new_col}: top {cutoff} at value {cutoff_value}.')
        df_rank.loc[df_rank[new_col] < cutoff_value, new_col] = 0

    if plotmode == 'radar':
        categories = list(range(1, len(df_rank.columns)))
        N = len(categories)
        angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(10, 6), subplot_kw=dict(polar=True))
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)

        for index, row in df_rank.iterrows():
            values = row[1:].tolist()
            values += values[:1]

            # Highlight one with rank 1
            if 1 in set(row):
                ax.plot(angles, values, marker='o', markerfacecolor="white", linewidth=4, label=row['Protein'])
            else:
                ax.plot(angles, values, marker='o', markerfacecolor="white", linewidth=2, label=row['Protein'], alpha=0.4)


        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        ax.tick_params(axis='y', labelsize=11)
        ax.set_rlabel_position(0)
        ax.set_ylim(0, 16) #y axis range
        ax.text(-0.05, ax.get_rmax() - 7, '-log(Pvalue)', horizontalalignment='center', verticalalignment='center', rotation=90)
        plt.xlabel('Density Number')
        
        plt.title(f'-log(Pvalues) for Proteins with cutoff rank={cutoff} and MinSize = {minsize}')
        plt.legend(loc='right')
        plt.show()

    #Generate a scatter/line plot instead
    elif plotmode == 'scatter':
        #print(df_rank)
        plt.figure(figsize=(10, 6))
        for index, row in df_rank.iterrows():
            # Highlight one with rank 1
            if 1 in set(row):
                plt.plot(range(1, len(row)), row[1:], marker='o', markerfacecolor="white", linewidth=4, label=row['Protein'])
            else:
                plt.plot(range(1, len(row)), row[1:], marker='o', markerfacecolor="white", linewidth=2, label=row['Protein'], alpha=0.4)

        plt.rcParams['svg.fonttype'] = 'none' #Change this to 'path' if necessary
        plt.xlabel('Density Number')
        plt.ylabel('-log(Pvalue)')
        plt.title(f'-log(Pvalues) for Proteins with cutoff rank={cutoff} and MinSize = {minsize}')
        plt.xticks(range(1, len(row)))
        plt.legend()
        plt.grid(False)
        plt.show()