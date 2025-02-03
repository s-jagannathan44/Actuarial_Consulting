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


def extract_8cos():
    # Step 3  Separate out 8 companies  which have paid and OS til Q1 2025 hence need no multiplier from  theft and total loss
    df_8cos = theft_tl[theft_tl["supplier_name"].isin(
        ["Bajaj Allianz General Insurance Company Ltd", "Cholamandalam MS General Insurance Company Ltd",
         "National Insurance Company Ltd", "Reliance General Insurance Company Ltd",
         "Shriram General Insurance Company Ltd", "The New India Assurance Co. Ltd.",
         "The Oriental Insurance Company Ltd", "United India Insurance Company Ltd"])]
    df_8cos["Ultimate_PAID"] = df_8cos["total_paid"] * df_8cos["Accident_Quarter"].apply(
        lambda x: apply_theft_tl_multiplier(x))
    df_8cos.to_csv("CSV\\FixedMultiplier\\theft_total_loss_8cos.csv")
    # Step 4  Separate out 8 companies   which have paid and OS til Q1 2025 hence need no multiplier from large
    df_8cos = large[large["supplier_name"].isin(
        ["Bajaj Allianz General Insurance Company Ltd", "Cholamandalam MS General Insurance Company Ltd",
         "National Insurance Company Ltd", "Reliance General Insurance Company Ltd",
         "Shriram General Insurance Company Ltd", "The New India Assurance Co. Ltd.",
         "The Oriental Insurance Company Ltd", "United India Insurance Company Ltd"])]
    df_8cos["Ultimate_PAID"] = df_8cos["total_paid"] * df_8cos["Accident_Quarter"].apply(
        lambda x: apply_large_multiplier(x))
    df_8cos.to_csv("CSV\\FixedMultiplier\\large_8cos.csv")
    # Step 5  Separate out 8 companies   which have paid and OS til Q1 2025 hence need no multiplier  from non-large
    df_8cos = df[df["supplier_name"].isin(
        ["Bajaj Allianz General Insurance Company Ltd", "Cholamandalam MS General Insurance Company Ltd",
         "National Insurance Company Ltd", "Reliance General Insurance Company Ltd",
         "Shriram General Insurance Company Ltd", "The New India Assurance Co. Ltd.",
         "The Oriental Insurance Company Ltd", "United India Insurance Company Ltd"])]
    df_8cos["Ultimate_PAID"] = df_8cos["total_paid"] * df_8cos["Accident_Quarter"].apply(
        lambda x: apply_non_large_multiplier(x))
    df_8cos.to_csv("CSV\\FixedMultiplier\\non_large_8cos.csv")


def extract_6cos():
    # Step 6 Separate out 6 companies which have paid till Q1 2025 hence need 3 different multipliers for each quarter
    # Step 6.1
    df_6cos = theft_tl[theft_tl["supplier_name"].isin(
        ["Future Generali", "Liberty General Insurance Co. Ltd", "Magma HDI General Insurance",
         "Royal Sundaram Alliance Insurance Company Ltd", "Zuno General Insurance", "Zurich Kotak General Insurance"])]
    df_6cos["Ultimate_PAID"] = df_6cos["total_paid"] * df_6cos["Accident_Quarter"].apply(
        lambda x: apply_theft_tl_multiplier(x))
    df_6cos.to_csv("CSV\\FixedMultiplier\\theft_total_loss_6cos.csv")
    # Step 6.2
    df_6cos = large[large["supplier_name"].isin(
        ["Future Generali", "Liberty General Insurance Co. Ltd", "Magma HDI General Insurance",
         "Royal Sundaram Alliance Insurance Company Ltd", "Zuno General Insurance", "Zurich Kotak General Insurance"])]
    df_6cos["Ultimate_PAID"] = df_6cos["total_paid"] * df_6cos["Accident_Quarter"].apply(
        lambda x: apply_large_multiplier(x))
    df_6cos.to_csv("CSV\\FixedMultiplier\\large_6cos.csv")
    # Step 6.3
    df_6cos = non_large[non_large["supplier_name"].isin(
        ["Future Generali", "Liberty General Insurance Co. Ltd", "Magma HDI General Insurance",
         "Royal Sundaram Alliance Insurance Company Ltd", "Zuno General Insurance", "Zurich Kotak General Insurance"])]
    df_6cos["Ultimate_PAID"] = df_6cos["total_paid"] * df_6cos["Accident_Quarter"].apply(
        lambda x: apply_non_large_multiplier(x))
    df_6cos.to_csv("CSV\\FixedMultiplier\\non_large_6cos.csv")


df = pd.read_csv("CSV\\Ultimate_fixed.csv")
df["IDV_Ratio"] = df["incurred"] / df["sum_insured"]
df["is_non_large"] = df["IDV_Ratio"].apply(lambda x: "Y" if x <= 0.4 else "N")

# Step 1 remove 3 problematic companies
df = df[~ df["supplier_name"].str.contains("Iffco Tokio General Insurance Company Ltd", na=False)]
df = df[~ df["supplier_name"].str.contains("Raheja QBE General Insurance Company", na=False)]
df = df[~ df["supplier_name"].str.contains("SBI General Insurance Company Ltd", na=False)]

# Step 2 Split  file into Non-large, large , theft and total loss
theft_tl, large, non_large = split_into_3(df)
extract_8cos()
extract_6cos()
