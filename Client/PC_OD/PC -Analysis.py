import pandas as pd
import math

# import duckdb as db

count = 0


def set_financial_year(year_p):
    global count
    try:
        year = year_p.to_period('Q-MAR').qyear
        quarter = year_p.to_period('Q-MAR').quarter
        retval = str(year) + "_Q" + str(quarter)
        print(retval)
        return retval
        # return year_p.to_period('Q-MAR').quarter
    except AttributeError:
        count = count + 1
        print("error occurred in set_financial_year")
        return ""


def apply_multiplier(quarter):
    if quarter in ["2023_Q1", "2023_Q2", "2023_Q3", "2023_Q4"]:
        return 1.001
    elif quarter == "2024_Q1":
        return 1.002
    elif quarter == "2024_Q2":
        return 1.003
    elif quarter == "2024_Q3":
        return 1.009
    elif quarter == "2024_Q4":
        return 1.112


df = pd.read_csv("CSV\\policy_claims_analysis.csv")
df = df[df["Accident_Year"].isin([2023, 2024])]
df['Loss Date'] = pd.to_datetime(df['Loss Date'], format="mixed", dayfirst=True)
df["Accident_Quarter"] = df["Loss Date"].apply(lambda x: set_financial_year(x))
df['registration_rto_code'] = df['registration_rto_code'].str.replace('DL01', 'DL1')
df['registration_rto_code'] = df['registration_rto_code'].str.replace('RJ01', 'RJ1')
df["PAID_AMT"] = df["total_paid"] * df["Accident_Quarter"].apply(lambda x: apply_multiplier(x))
df.to_csv("CSV\\Ultimate.csv")
