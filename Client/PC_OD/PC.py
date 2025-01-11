import pandas as pd
import glob

count = 0


def merge_files():
    path = "Booking/*.csv"
    df = pd.DataFrame()
    files = glob.glob(path)
    for file_name in files:
        frame = pd.read_csv(file_name)
        df = pd.concat([df, frame], axis=0)
    df.to_csv("base_file.csv")


def merge_claims():
    path = "Claims/*.csv"
    df = pd.DataFrame()
    files = glob.glob(path)
    for file_name in files:
        frame = pd.read_csv(file_name)
        new_frame = pd.DataFrame(
            columns=["Claim_Reference", "Policy_Number", "Insurer_Name", "product_type", "Loss Date",
                     "Report Date", "Claim Closed Date", "kind_of_loss", "cause_of_loss",
                     "registration_no", "total_paid", "total_os", "status", "file_date", "incurred"])
        print(file_name)
        if "claim_number" in frame.columns:
            new_frame["Claim_Reference"] = frame["claim_number"]
        if "policy_num" in frame.columns:
            new_frame["Policy_Number"] = frame["policy_num"]
        if "insurer_name" in frame.columns:
            new_frame["Insurer_Name"] = frame["insurer_name"]
        if "producttype" in frame.columns:
            new_frame["product_type"] = frame["producttype"]
        else:
            new_frame["product_type"] = frame["product_type"]
        if "loss_date" in frame.columns:
            new_frame["Loss Date"] = frame["loss_date"]
        if "intimation_date" in frame.columns:
            new_frame["Report Date"] = frame["intimation_date"]
        if "claim_close_date" in frame.columns:
            new_frame["Claim Closed Date"] = frame["claim_close_date"]
        if "kind_of_loss" in frame.columns:
            new_frame["kind_of_loss"] = frame["kind_of_loss"]
        if "cause_of_loss" in frame.columns:
            new_frame["cause_of_loss"] = frame["cause_of_loss"]
        if "registration_no" in frame.columns:
            new_frame["registration_no"] = frame["registration_no"]
        if "total_paid" in frame.columns:
            new_frame["total_paid"] = frame["total_paid"]
        if "total_os" in frame.columns:
            new_frame["total_os"] = frame["total_os"]
        if "status" in frame.columns:
            new_frame["status"] = frame["status"]
        if "file_date" in frame.columns:
            new_frame["file_date"] = frame["file_date"]
        if "incurred" in frame.columns:
            new_frame["incurred"] = frame["incurred"]
        elif "Incurred" in frame.columns:
            new_frame["incurred"] = frame["Incurred"]
        else:
            new_frame["incurred"] = frame["total_incurred"]

        df = pd.concat([df, new_frame], axis=0)
    df = df[~ df["product_type"].str.contains("TWO WHEELER", na=False)]
    df = df[~ df["kind_of_loss"].str.contains("TP", na=False)]
    df = df[~ df["kind_of_loss"].str.contains("Tp", na=False)]
    df.to_csv("claims_file.csv")


def set_financial_year(year_p):
    global count
    try:
        return year_p.to_period('Q-MAR').qyear
    except AttributeError:
        count = count + 1
        print("error occurred in set_financial_year")
        return ""


def transform_claim():
    claims = pd.read_csv("claims_file.csv")
    claims['Loss Date'] = pd.to_datetime(claims['Loss Date'], format="mixed", dayfirst=True)
    claims['Report Date'] = pd.to_datetime(claims['Report Date'], format="mixed", dayfirst=True)
    claims['Claim Closed Date'] = pd.to_datetime(claims['Claim Closed Date'], format="mixed", dayfirst=True)
    claims["Loss_FY"] = claims["Loss Date"].apply(lambda x: set_financial_year(x))
    claims["Reported_FY"] = claims["Report Date"].apply(lambda x: set_financial_year(x))
    claims["Paid_FY"] = claims["Claim Closed Date"].apply(lambda x: set_financial_year(x))
    return claims


# merge_claims()
transform_claim().to_csv("claims_file_v2.csv")
# Code to read all column headers dump them to a file  we can Identify files where headers are spelt differently
# path = "Claims/*.csv"
# df = pd.DataFrame()
# files = glob.glob(path)
# for file_name in files:
#     frame = pd.read_csv(file_name)
#     frame.dtypes.to_csv("Columns\\" + file_name[7:-4] + ".csv")
#
# path = "Columns/*.csv"
# df = pd.DataFrame()
# files = glob.glob(path)
# for file_name in files:
#     client_name = file_name[8:-4]
#     frame = pd.read_csv(file_name)
#     frame["Policy_Client_Name"] = client_name
#
#     df = pd.concat([df, frame], axis=0)
#     df.to_csv("cols.csv")
