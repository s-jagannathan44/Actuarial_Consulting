import pandas as pd


# import glob


def set_financial_year(year_p):
    try:
        year = year_p.to_period('Q-MAR').qyear
        quarter = year_p.to_period('Q-MAR').quarter
        retval = str(year) + "_Q" + str(quarter)
        print(retval)
        return retval
        # return year_p.to_period('Q-MAR').quarter
    except AttributeError:
        print("error occurred in set_financial_year")
        return ""


def apply_non_large_multiplier(quarter):
    if quarter in ["2023_Q1"]:
        return 1.000
    elif quarter == "2023_Q2":
        return 1.000
    elif quarter == "2023_Q3":
        return 1.000
    elif quarter == "2023_Q4":
        return 1.0002
    elif quarter == "2024_Q1":
        return 1.0006
    elif quarter == "2024_Q2":
        return 1.0001
    elif quarter == "2024_Q3":
        return 1.0020
    elif quarter == "2024_Q4":
        return 1.0214


def apply_large_multiplier(quarter):
    if quarter in ["2023_Q1"]:
        return 1.000
    elif quarter == "2023_Q2":
        return 1.0115
    elif quarter == "2023_Q3":
        return 1.0023
    elif quarter == "2023_Q4":
        return 1.0294
    elif quarter == "2024_Q1":
        return 1.0483
    elif quarter == "2024_Q2":
        return 1.0248
    elif quarter == "2024_Q3":
        return 1.0228
    elif quarter == "2024_Q4":
        return 1.1337


def apply_theft_tl_multiplier(quarter):
    if quarter in ["2023_Q1"]:
        return 1.00
    elif quarter == "2023_Q2":
        return 1.000
    elif quarter == "2023_Q3":
        return 1.00
    elif quarter == "2023_Q4":
        return 1.00
    elif quarter == "2024_Q1":
        return 1.00
    elif quarter == "2024_Q2":
        return 1.00
    elif quarter == "2024_Q3":
        return 1.0353
    elif quarter == "2024_Q4":
        return 1.3999


def split_into_3(frame):
    theft_tl_ = frame[frame["cause_of_loss"].isin(
        ["Theft of entire vehicle", "Theft", "Theft of Entire Vehicle", "THEFT-VEHICLE", "Theft - Vehicle",
         "Theft of Vehicle", "Total Loss"])]
    non_theft = frame[~ frame["cause_of_loss"].str.contains("Theft of entire vehicle", na=False)]
    non_theft = non_theft[~ non_theft["cause_of_loss"].str.contains("Theft", na=False)]
    non_theft = non_theft[~ non_theft["cause_of_loss"].str.contains("Theft of Entire Vehicle", na=False)]
    non_theft = non_theft[~ non_theft["cause_of_loss"].str.contains("THEFT-VEHICLE", na=False)]
    non_theft = non_theft[~ non_theft["cause_of_loss"].str.contains("Theft - Vehicle", na=False)]
    non_theft = non_theft[~ non_theft["cause_of_loss"].str.contains("Theft of Vehicle", na=False)]
    non_theft = non_theft[~ non_theft["cause_of_loss"].str.contains("Total Loss", na=False)]
    large_ = non_theft[non_theft["is_non_large"] == 'N']
    non_large_ = non_theft[non_theft["is_non_large"] == 'Y']
    return theft_tl_, large_, non_large_


def check_cause_of_loss(x):
    if "Theft of entire vehicle" in x or "Theft" in x or "Theft of Entire Vehicle" in x or "THEFT-VEHICLE" in x \
            or "Theft - Vehicle" in x or "Theft of Vehicle" in x or "Total Loss" in x:
        return 1
    else:
        return 0


# df = pd.read_csv("CSV\\Ultimate_fixed.csv")
# df["IDV_Ratio"] = df["incurred"] / df["sum_insured"]
# df["is_non_large"] = df["IDV_Ratio"].apply(lambda x: "Y" if x <= 0.4 else "N")
#
# # Step 1 remove 3 problematic companies
# df = df[~ df["supplier_name"].str.contains("Iffco Tokio General Insurance Company Ltd", na=False)]
# df = df[~ df["supplier_name"].str.contains("Raheja QBE General Insurance Company", na=False)]
# df = df[~ df["supplier_name"].str.contains("SBI General Insurance Company Ltd", na=False)]
#
# # Step 2 Split  file into Non-large, large , theft and total loss
# theft_tl, large, non_large = split_into_3(df)
#
# # Step 3 apply multipliers
#
# theft_tl["Ultimate_PAID"] = theft_tl["total_paid"] * theft_tl["Accident_Quarter"].apply(
#     lambda x: apply_theft_tl_multiplier(x))
# theft_tl.to_csv("CSV\\FixedMultiplier\\theft_total_loss.csv")
#
# large["Ultimate_PAID"] = large["total_paid"] * large["Accident_Quarter"].apply(
#     lambda x: apply_large_multiplier(x))
# large.to_csv("CSV\\FixedMultiplier\\large.csv")
#
# non_large["Ultimate_PAID"] = non_large["total_paid"] * non_large["Accident_Quarter"].apply(
#     lambda x: apply_non_large_multiplier(x))
# non_large.to_csv("CSV\\FixedMultiplier\\non_large.csv")

# df1 = pd.read_csv("CSV\\FixedMultiplier\\non_large.csv")
# df2 = pd.read_csv("CSV\\FixedMultiplier\\large.csv")
# df3 = pd.read_csv("CSV\\FixedMultiplier\\theft_total_loss.csv")
# df = pd.concat([df1, df2, df3], axis=0)
# df.to_csv("CSV\\FixedMultiplier\\Combined_file.csv")
# df = pd.read_csv("CSV\\FixedMultiplier\\Combined_new_file.csv")
# # df["cause_of_loss"] = df["cause_of_loss"].fillna("NA")
# # df["is_theft_total_loss"] = df["cause_of_loss"].apply(lambda x: check_cause_of_loss(x))
# # df["is_large_loss_non_theft"] = df["IDV_Ratio"].apply(lambda x: 0 if x <= 0.4 else 1) - df["is_theft_total_loss"]
# # df["is_large_loss_non_theft"] = df["is_large_loss_non_theft"].apply(lambda x: 0 if x < 0 else x)
# # df["non_theft_non_large"] = df["IDV_Ratio"].apply(lambda x: 1 if x <= 0.4 else 0) - df["is_theft_total_loss"]
# # df["non_theft_non_large"] = df["non_theft_non_large"].apply(lambda x: 0 if x < 0 else x)
# # df["ultimate_paid_non_large"] = df["Ultimate_PAID"] * df["non_theft_non_large"]
# # df["sum_insured_in_hundreds"] = df["sum_insured"]/1000
# df["large_theft_total_loss"] = df["is_large_loss_non_theft"] + df["is_theft_total_loss"]
# df["large_theft_total_loss"] = df["large_theft_total_loss"].apply(lambda x: 1 if x > 1 else x)
#
# df["ultimate_paid_large_ttl"] = df["Ultimate_PAID"] * df["large_theft_total_loss"]
#
# df.to_csv("CSV\\FixedMultiplier\\Combined_ttl_file.csv")

df = pd.read_csv("CSV\\FixedMultiplier\\Combined_final_file.csv")
missing = pd.read_csv("CSV\\base_file.csv", usecols=["policy_no", "previous_insurer_type"])
missing.rename(columns={"policy_no": "Policy_Number"}, inplace=True)
df.drop(["Unnamed: 0", "Unnamed: 0.1", "Unnamed: 0.2", "Unnamed: 0.3", "Unnamed: 0.4",  "Unnamed: 0.5"], axis=1, inplace=True)
df_final = df.merge(missing, on=["Policy_Number"], how="left")
df_final.to_csv("Output\\Combined_final_file.csv")


