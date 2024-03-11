import pandas as pd
import glob


def convert_files():
    path = "TW/*.xlsx"
    files = glob.glob(path)
    for file_name in files:
        print(file_name)
        excelFile = pd.read_excel(file_name)
        excelFile.to_csv(file_name + ".csv")


convert_files()
