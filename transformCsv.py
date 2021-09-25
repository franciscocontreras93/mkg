import os
import glob
import pandas as pd

path = r"C:\ISMAEL\entregas"
excel_files = glob.glob(
    'C:/ISMAEL/entregas/*.xlsx')  # assume the path
for excel in excel_files:
    out = excel.split('.')[0]+'.csv'
    # if only the first sheet is needed.
    df = pd.read_excel(excel, sheet_name=0, engine="openpyxl")
    df.to_csv(out)
    os.remove(excel)
