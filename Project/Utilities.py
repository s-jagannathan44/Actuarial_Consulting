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
# split_csv splits a dataframe into multiple parts and then writes them to file
# rollup_policies rolls up the policy data as per the columns provided
import numpy as np
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
    col_list = ["NOL Flag", "RSD New", "UniqueKey"]
    # This line does a pivot table like summation based on the specified columns
    df = df.groupby(col_list).sum()
    df.to_csv("Output\\PaidClaimGrouping.csv")


def process_outstanding_claims():
    df = pd.read_csv("Output\\Data\\Project\\Claims_Outstanding.csv")
    df = df[df["OS AS ON"] == "01-03-2022"]
    df["UniqueKey"] = df["Policy No"] + df["UWYear"]
    df.drop(columns="Product code", axis=1, inplace=True)
    col_list = ["NOL Flag", "RSD New", "UniqueKey"]
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
                "Zone", "UniqueKey", "UY New"]
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
    dataFrame4 = pd.merge(dataFrame2, dataFrame3, on='UniqueKey', how="outer")

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
    # This is right outer join and includes all keys from table on right .
    # To get keys from both tables  use the full outer join [how = outer]
    dataFrame3 = pd.merge(dataFrame2, dataFrame1, on='Key', how="right")

    print(dataFrame3)


def split_csv():
    df = pd.DataFrame(
        {
            "Key": ["1", "2", "3", "4", "5", "6"],
            "Col2": [10, 30, 40, 50, 20, 60],
            "Col3": [2, 5, 7, 9, 1, 3]
        },
    )
    df_split = np.array_split(df, 3)
    for i in range(0, 3):
        df_split[i].to_csv(str(i) + ".csv")


def rollup_policies(freq):
    col_list = ["UY New", "LT_ANNUAL Flag", "CC_desc", "Body Type", "Vehicle Make", "V AGE BAND",
                "Registration States", "Zone", "Channel", "Cluster", "Vehicle Registration Region"]

    full_list = col_list + ['Gross Cost'] + ['Exposure']

    freq = freq[full_list]
    df_freq = freq[col_list]

    df_freq = df_freq.iloc[df_freq.drop_duplicates().index]
    df_freq = df_freq.reset_index(drop=True)
    df_freq['GroupID'] = df_freq.index + 1

    df_freq = pd.merge(freq, df_freq, how='left')
    df_freq['GroupID'] = df_freq['GroupID'].fillna(method='ffill')
    df_freq.set_index("GroupID", inplace=True, drop=True)
    df_freq.to_csv("Output\\pivot.csv")

    freq = pd.read_csv("Output\\pivot.csv")
    freq = freq.groupby(col_list).sum()
    return freq


def combine_state(filename):
    df = pd.read_csv(filename, encoding='windows-1252')
    Major_States = ["Tamil Nadu", "Madhya Pradesh", "Kerala", "Karnataka", "Rajasthan", "Odisha", "West Bengal",
                    "Maharashtra", "Chattisgarh", "Telangana", "Uttar Pradesh", "Gujarat", "Andhra Pradesh",
                    "Bihar", "Haryana", "Delhi"]
    list_states = df["Registration States"].unique()
    OtherStates = []

    for State in list_states:
        if Major_States.count(State) == 0:
            OtherStates.append(State)
    for State in OtherStates:
        for index in range(len(df)):
            if index < len(df):
                if df["Registration States"].iloc[index] == State:
                    df["Registration States"].iloc[index] = df["Zone"].iloc[index]
    df.to_csv("Output\\State.csv")


# UW Year Code
# df = pd.read_csv("Output\\Death.csv")
# index = 0
# for index in range(len(df)):
#     if index < len(df) - 1:
#         if df["UY_Newer"].iloc[index] != "2012-18":
#             df["UY_Newer"].iloc[index] = df["UY New"].iloc[index]
#
# df.to_csv("Output\\Death_Modified.csv")
#


# for i in range(0, 10):
#     df_ = combine_make("D:\\MachineLearning_Files\\Project\\Split_Files\\" + str(i) + ".csv")
#     df_ = group_policies(df_)
#     df_ = sum_columns(df_)
#     df_.to_csv("D:\\MachineLearning_Files\\Project\\Split_Files\\FinalPolicy_" + str(i) + ".csv")
#     print(i)

# for i in range(0, 10):
#     policy = pd.read_csv("D:\\MachineLearning_Files\\Project\\Split_Files\\FinalPolicy_" + str(i) + ".csv")
#     claims = combine_claim_files()
#     dataFrame4 = pd.merge(claims, policy, on='UniqueKey', how="right")
#     dataFrame4.set_index("UniqueKey", inplace=True, drop=True)
#     dataFrame4.to_csv("D:\\MachineLearning_Files\\Project\\Split_Files\\DataFile_" + str(i) + ".csv")
#     print(i)

# for i in range(0, 10):
#     policy = pd.read_csv("D:\\MachineLearning_Files\\Project\\Split_Files\\DataFile_" + str(i) + ".csv")
#     rollup_policies(policy).to_csv("D:\\MachineLearning_Files\\Project\\Split_Files\\Rollup_" + str(i) + ".csv")

# dfs = []
# for i in range(0, 10):
#     policy = pd.read_csv("D:\\MachineLearning_Files\\Project\\Split_Files\\Rollup_" + str(i) + ".csv")
#     dfs.append(policy)
#     print(i)
#
# result = pd.concat(dfs)
# result.to_csv("Output\\frames.csv")


#
# dfs = []
# for i in range(0, 10):
#     policy = pd.read_csv("D:\\MachineLearning_Files\\Project\\Split_Files\\DataFile_" + str(i) + ".csv")
#     dfs.append(policy)
#     print(i)
#
# result = pd.concat(dfs)
# result.to_csv("Output\\frames.csv")

# Code for conditional merging

# master = pd.read_csv("Output\\InjuryMaster.csv")
#
# unroll = pd.read_csv("Output\\Injury_Unroll.csv")
# index = 0
# for index in range(len(master)):
#     if index < len(master) - 1:
#         UY = master["UY_Newer"].iloc[index]
#         Age = master["Age_New"].iloc[index]
#         Flag = master["LT_ANNUAL Flag"].iloc[index]
#         Body_Type = master["Body Type"].iloc[index]
#         CC = master["CC_New"].iloc[index]
#         Make = master["Vehicle Make"].iloc[index]
#         State = master["Registration States"].iloc[index]
#         Zone = master["Zone"].iloc[index]
#         cost = unroll.loc[
#             (unroll['UY New'] == UY) & (unroll['LT_ANNUAL Flag'] == Flag) & (unroll['V AGE NEW'] == Age) &
#             (unroll['Body Type'] == Body_Type) & (unroll['CC_desc'] == CC) &
#             (unroll['State_New'].str.contains(State)) & (unroll['Make_New'].str.contains(Make)) &
#             (unroll['Zone_New'].str.contains(Zone)), 'Output']
#         cost = np.average(cost)
#         if cost is not np.nan:
#             master["Predicted"].iloc[index] = np.average(cost)
#         else:
#             master["Predicted"].iloc[index] = 0
# master.to_csv("Output\\unrolled.csv")
