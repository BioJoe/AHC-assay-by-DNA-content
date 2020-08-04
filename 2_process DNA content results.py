#load python included modules
import ntpath
import tkinter as tk
from tkinter import filedialog
#load additional python modules
import numpy as np
import pandas as pd

#required for the dialog box
root = tk.Tk()
root.withdraw()

#ask for a file
file_path = filedialog.askopenfilename(
    title = "Select the compiled DNA content results file")

#open file
df_cells = pd.read_excel(file_path, index_col=None)
dirName = ntpath.dirname(file_path)

#get a list with all the genotypes in the dataframe
gt_ls = df_cells.genotype.unique()

#calcute internal standard deviation for each cyst
for gt in gt_ls:
    cyst_ls = df_cells.loc[
        df_cells['genotype'] == gt].CystNumber.unique()
    for cyst in cyst_ls:
        cyst_stdev = df_cells.loc[
            (df_cells['genotype'] == gt)
            & (df_cells['CystNumber'] == cyst),
            'norm signal'].std(axis=0)
        df_cells.loc[
            (df_cells['genotype'] == gt)
            & (df_cells['CystNumber'] == cyst),
            'cyst_stdev'] = cyst_stdev

    #calcute mean standard deviation each genotype
    mean_cyst_stdev = df_cells.loc[
        df_cells['genotype'] == gt].drop_duplicates(
        subset ="CystNumber", keep = "first",
        inplace = False)["cyst_stdev"].mean(axis=0)
    df_cells.loc[
        (df_cells['genotype'] == gt),
        'mean_cyst_stdev'] = mean_cyst_stdev

save_path = filedialog.asksaveasfilename(
    title='Save compiled results as ...', defaultextension = '.xlsx',
    initialdir = dirName, initialfile = "compiled DNA content results")
df_cells.to_excel(save_path, index=False)
print('done')
