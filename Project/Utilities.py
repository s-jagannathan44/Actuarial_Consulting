# This file contains Utility functions which perform the following functions
# extract_policies does a data dump of specific policies
# process_paid_claims sums up the paid claims file till FY 22-23
# process_outstanding_claims extracts the outstanding claims as on 1 Mar 2022
# sum_columns horizontally sums up columns in the policy file
# group_policies vertically sums up rows in the policy file
# combine_make combines makes with different spellings into one .
# process_policies creates a final policy file
# create_csv combines policies and claims files to create a final csv file
# combine_claim_files combines the outstanding and paid claim files and passes the Gross claim amount
# per policy to create_csv to be included in the final csv file
# merge_dataframes has sample code for merging 2 data frames with different columns into 1 via a UniqueKey

import pandas as pd


def extract_policies():
    df = pd.read_csv("Output\\2W_Policy.csv", encoding='windows-1252')

    PolicyNos = ["P0017300002/4102/103012", "P0019200005/4113/101756", "P0019400039/4112/100314",
                 "P0020100004/4113/117071", "P0021200014/4113/132491"]
    Grouped = pd.DataFrame(columns=df.columns)
    for PolicyNo in PolicyNos:
        rows = df[df["Policy No"] == PolicyNo]
        Grouped = Grouped.append(rows)

    Grouped.to_csv("Output\\Row.csv")


def process_paid_claims():
    df = pd.read_csv("Output\\Data\\Project\\PaidClaims.csv")
    df["UniqueKey"] = df["Policy No"] + df["UWYear"]
    df = df[df["Paid FY"] != "2022-23"]
    df.drop(columns="Product Code", axis=1, inplace=True)
    col_list = ["Policy No",  "Type", "NOL Flag", "RSD New", "UniqueKey"]
    # This line does a pivot table like summation based on the specified columns
    df = df.groupby(col_list).sum()
    df.to_csv("Output\\PaidClaimGrouping.csv")


def process_outstanding_claims():
    df = pd.read_csv("Output\\Data\\Project\\Claims_Outstanding.csv")
    df = df[df["OS AS ON"] == "01-03-2022"]
    df["UniqueKey"] = df["Policy No"] + df["UWYear"]
    df.drop(columns="Product code", axis=1, inplace=True)
    col_list = ["Policy No", "Type", "NOL Flag", "RSD New", "UniqueKey"]
    # This line does a pivot table like summation based on the specified columns
    df = df.groupby(col_list).sum()

    df.to_csv("Output\\OutstandingClaimGrouping.csv")


def sum_columns(df):
    GEP_List = ["GEP 1213", "GEP 1314", "GEP 1415", "GEP 1516", "GEP 1617", "GEP 1718", "GEP 1819", "GEP 1920",
                "GEP 2021", "GEP 2122"]
    NEP_List = ["NEP 1213", "NEP 1314", "NEP 1415", "NEP 1516", "NEP 1617", "NEP 1718", "NEP 1819", "NEP 1920",
                "NEP 2021", "NEP 2122"]
    Exposure_List = ["EXPO 1213", "EXPO 1314", "EXPO 1415", "EXPO 1516", "EXPO 1617", "EXPO 1718", "EXPO 1819",
                     "EXPO 1920", "EXPO 2021", "EXPO 2122"]
    col_to_drop = GEP_List + NEP_List + Exposure_List + \
                  ["GEP 2223", "NEP 2223", "EXPO 2223"]

    # ----------  df = pd.read_csv("Output\\VerticalAddition.csv")
    # Below lines do a horizontal addition of columns specified in the list
    df['NEP'] = df[NEP_List].sum(axis=1)
    df["Exposure"] = df[Exposure_List].sum(axis=1)
    df["GEP"] = df[GEP_List].sum(axis=1)
    df.drop(columns=col_to_drop, axis=1, inplace=True)

    for col in df.columns:
        if "Unnamed" in col:
            df.drop(col, axis=1, inplace=True)
    return df
    # df.to_csv("Output\\Sum.csv")


def group_policies(df):
    col_list = ["LT_ANNUAL Flag", "Policy No", "CC_desc", "Body Type", "Vehicle Make", "Channel", "RSD New",
                "RED New", "V AGE BAND", "Vehicle Registration Region", "Registration States", "Cluster",
                "Zone", "UniqueKey"]
    # ------------------- df = pd.read_csv("Output\\Make.csv")
    # This line does a pivot table like summation based on the specified columns
    df = df.groupby(col_list).sum()
    return df
    # df.to_csv("Output\\VerticalAddition.csv")


def combine_make():
    df = pd.read_csv("Output\\Data\\Project\\Project.csv")
    df["UniqueKey"] = df["Policy No"] + df["UY New"]
    Major_manufacturer = ["HERO", "BAJAJ", "HONDA", "TVS", "YAMAHA", "ROYALENFIELD", "SUZUKI"]
    list_makes = df["Vehicle Make"].unique()
    OtherMakes = []

    # Below loop takes all makes not in list of major manufacturers and labels them Other
    for Make in list_makes:
        if Major_manufacturer.count(Make) == 0:
            OtherMakes.append(Make)

    for Make in Major_manufacturer:
        df.loc[df['Vehicle Make'].str.startswith(Make, na=False), 'Vehicle Make'] = Make

    for Make in OtherMakes:
        df.loc[df['Vehicle Make'].str.startswith(Make, na=False), 'Vehicle Make'] = "OTHER"
    return df
    #  df.to_csv("Output\\Make.csv")


def process_policies():
    df = combine_make()
    df = group_policies(df)
    df = sum_columns(df)
    df.to_csv("Output\\FinalPolicy.csv")


def create_csv():
    policy = pd.read_csv("Output\\FinalPolicy.csv")
    claims = combine_claim_files()
    dataFrame4 = pd.merge(claims, policy, on='UniqueKey', how="right")
    dataFrame4.to_csv("Output\\Combined.csv")


def combine_claim_files():
    dataFrame2 = pd.read_csv("Output\\PaidClaimGrouping.csv")
    dataFrame2 = dataFrame2[dataFrame2["NOL Flag_Paid"] == "Injury"]
    dataFrame3 = pd.read_csv("Output\\OutstandingClaimGrouping.csv")
    dataFrame3 = dataFrame3[dataFrame3["NOL Flag_OS"] == "Injury"]
    dataFrame4 = pd.merge(dataFrame2, dataFrame3, on='UniqueKey', how="right")

    Gross_List = ["Gross Paid", "Gross  OS"]
    col_to_drop = ["Gross Paid", "Gross Loss Paid", "Gross Expense Paid", "Net Paid", "Unique Claim Count_Paid",
                   "NOL Flag_OS", "Gross  OS", "Gross Loss OS", "Gross Expense OS", "Net OS", "Unique Claim Count_OS"]
    # Below lines do a horizontal addition of columns specified in the list
    dataFrame4['Gross Cost'] = dataFrame4[Gross_List].sum(axis=1)
    dataFrame4.drop(columns=col_to_drop, axis=1, inplace=True)
    dataFrame4.set_index("UniqueKey", inplace=True, drop=True)
    return dataFrame4
    # dataFrame4.to_csv("Output\\CombinedClaims.csv")


def merge_dataframes():
    # Create DataFrame1
    dataFrame1 = pd.DataFrame(
        {
            "Key": ["1", "2", "3", "4"],
            "Col2": [10, 30, 40, 50],
            "Col3": [2, 5, 7, 9]
        },
    )

    print(dataFrame1)

    # Create DataFrame2
    dataFrame2 = pd.DataFrame(
        {
            "Col1": [100],
            "Col7": [200],
            "Key": ["1"]
        },
    )

    print(dataFrame2)

    dataFrame3 = pd.merge(dataFrame2, dataFrame1, on='Key', how="right")

    print(dataFrame3)
