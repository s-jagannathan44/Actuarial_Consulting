import pandas as pd
import glob
import duckdb as db


def merge_opd_files():
    path = "C:\\Data\\Narayana\\OPD_DATA\\All_Files/*.csv"
    df = pd.DataFrame()
    files = glob.glob(path)
    for file_name in files:
        frame = pd.read_csv(file_name)
        frame["file_name"] = file_name[36:40]
        df = pd.concat([df, frame], axis=0)
    df = df[~df.patient_type.isin(["VIP", "STAFF"])]
    df["Age_New"] = df["patient_age"].apply(lambda x: group_Age(x))
    df.to_csv("Output\\merged_OPD_file.csv")
    return df


def group_Age(x):
    if 0 <= x <= 4:
        return "0 to 4"
    elif 5 <= x <= 9:
        return "5 to 9"
    elif 10 <= x <= 14:
        return "10 to 14"
    elif 15 <= x <= 19:
        return "15 to 19"
    if 20 <= x <= 24:
        return "20 to 24"
    elif 25 <= x <= 29:
        return "25 to 29"
    elif 30 <= x <= 34:
        return "30 to 34"
    elif 35 <= x <= 39:
        return "35 to 39"
    if 40 <= x <= 44:
        return "40 to 44"
    elif 45 <= x <= 49:
        return "45 to 49"
    elif 50 <= x <= 54:
        return "50 to 54"
    elif 55 <= x <= 59:
        return "55 to 59"
    if 60 <= x <= 64:
        return "60 to 64"
    elif 65 <= x <= 69:
        return "65 to 69"
    elif 70 <= x <= 79:
        return "70 to 79"
    elif 80 <= x <= 89:
        return "80 to 89"
    elif 90 <= x <= 99:
        return "90 to 99"
    else:
        return "Above 100"


df3 = merge_opd_files()
# df3 = pd.read_csv("Output\\merged_OPD_file.csv")

# q3 = """select sum(gross_amount),
#             patient_mrn,invoice_number, patient_gender,patient_age,
#             correspondence_address_pincode, ordering_department_name, plan_name,item_group
#             from df3
#             group by patient_mrn,invoice_number, patient_gender,patient_age,
#             correspondence_address_pincode, ordering_department_name, plan_name,item_group
#      """
#
# output = db.execute(q3).df()
# output.to_csv("Output\\OPDMemberSummary.csv")
