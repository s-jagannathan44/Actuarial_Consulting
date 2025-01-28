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


# def merge_ncb():
#     path = "CSV/NCB/ncb*.csv"
#     df = pd.DataFrame()
#     files = glob.glob(path)
#     for file_name in files:
#         frame = pd.read_csv(file_name)
#         df = pd.concat([df, frame], axis=0)
#     df.to_csv("CSV\\NCB\\NCB_file.csv")
#
#
# def merge_booking():
#     path = "CSV/NCB/t*.csv"
#     df = pd.DataFrame()
#     files = glob.glob(path)
#     for file_name in files:
#         frame = pd.read_csv(file_name)
#         df = pd.concat([df, frame], axis=0)
#     df.to_csv("CSV\\NCB\\t_booking_file.csv")
#

# ncb = pd.read_csv("CSV\\NCB\\NCB_file.csv")
# booking = pd.read_csv("CSV\\NCB\\t_booking_file.csv")
# ncb.drop(["lead_id", "bookingdate", "Unnamed: 0"], axis=1, inplace=True)
# booking.drop(["lead_id", "bookingdate", "Unnamed: 0"], axis=1, inplace=True)
# ncb.rename(columns={"policy_no": "Policy_Number"}, inplace=True)
# booking.rename(columns={"policy_no": "Policy_Number"}, inplace=True)
# df_final = ncb.merge(booking, on=["Policy_Number"], how="left")
# df_final.to_csv("CSV\\Consolidated_fixed.csv")

# pol = pd.read_csv("CSV\\Ultimate.csv")
# fixed = pd.read_csv("CSV\\Consolidated_fixed.csv")
# pol.drop(["Unnamed: 0.1", "Unnamed: 0"], axis=1, inplace=True)
# fixed.drop(["Unnamed: 0"], axis=1, inplace=True)
# df_final = pol.merge(fixed, on=["Policy_Number"], how="left")
# df_final.to_csv("CSV\\Ultimate_fixed.csv")
