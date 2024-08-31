import pandas as pd
import glob


def merge_member_files():
    path = "C:\\Users\\jvpra\\Desktop\\IIB-Narayana\\Nararayana_member_data/*.dat"
    df = pd.DataFrame()
    files = glob.glob(path)
    for file_name in files:
        frame = pd.read_csv(file_name, encoding="UTF-16LE", delimiter="~~", engine="python")
        frame["file_name"] = file_name[-11:-3]
        df = pd.concat([df, frame], axis=0)
    # df.to_csv("Output\\base_member_file.csv")


def merge_policy_files():
    path = "C:\\Users\\jvpra\\Desktop\\IIB-Narayana\\Narayana_Policy_Dataset/*.dat"
    df = pd.DataFrame()
    files = glob.glob(path)
    for file_name in files:
        frame = pd.read_csv(file_name, delimiter="\t")
        frame["file_name"] = file_name[-11:-3]
        df = pd.concat([df, frame], axis=0)
    # df.to_csv("Output\\base_policy_file.csv")


def merge_claim_files():
    path = "C:\\Users\\jvpra\\Desktop\\IIB-Narayana\\Narayana Bespoke_Claims_Dataset/*.csv"
    df = pd.DataFrame()
    files = glob.glob(path)
    for file_name in files:
        frame = pd.read_csv(file_name)
        frame["file_name"] = file_name[-11:-3]
        df = pd.concat([df, frame], axis=0)
    # df.to_csv("Output\\base_claim_file.csv")


# merge_policy_files()
merge_member_files()
# merge_claim_files()
