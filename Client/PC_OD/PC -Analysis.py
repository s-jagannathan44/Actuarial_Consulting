import pandas as pd


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
    if quarter in ["2023_Q1"]:
        return 0.996
    elif quarter == "2023_Q2":
        return 1.0002
    elif quarter == "2023_Q3":
        return 1.0033
    elif quarter == "2023_Q4":
        return 1.0018
    elif quarter == "2024_Q1":
        return 1.0071
    elif quarter == "2024_Q2":
        return 1.0084
    elif quarter == "2024_Q3":
        return 1.0479
    elif quarter == "2024_Q4":
        return 1.1965


df = pd.read_csv("CSV\\policy_claims_analysis.csv")
df = df[df["Accident_Year"].isin([2023, 2024])]
df['Loss Date'] = pd.to_datetime(df['Loss Date'], format="mixed", dayfirst=True)
df['registration_rto_code'] = df['registration_rto_code'].str.replace('DL01', 'DL1')
df['registration_rto_code'] = df['registration_rto_code'].str.replace('RJ01', 'RJ1')
df["Accident_Quarter"] = df["Loss Date"].apply(lambda x: set_financial_year(x))
df["Ultimate_PAID"] = df["total_paid"] * df["Accident_Quarter"].apply(lambda x: apply_multiplier(x))
df.to_csv("CSV\\Ultimate.csv")

# df['Report Date'] = pd.to_datetime(df['Report Date'], format="mixed", dayfirst=True)
# df['Claim Closed Date'] = pd.to_datetime(df['Claim Closed Date'], format="mixed", dayfirst=True)
# df["Reported_Quarter"] = df["Report Date"].apply(lambda x: set_financial_year(x))
# df["Paid_Quarter"] = df["Claim Closed Date"].apply(lambda x: set_financial_year(x))
