import pandas as pd
import glob
import duckdb as db


def merge_opd_files():
    path = "C:\\Data\\Narayana\\OPD_DATA\\All_Files/*.csv"
    df = pd.DataFrame()
    files = glob.glob(path)
    for file_name in files:
        frame = pd.read_csv(file_name)
        frame["file_name"] = file_name[:-3]
        df = pd.concat([df, frame], axis=0)
    df = df[~df.patient_type.isin(["VIP", "STAFF"])]
    df.to_csv("Output\\merged_OPD_file.csv")
    return df


# df3 = merge_opd_files()
df3 = pd.read_csv("Output\\merged_OPD_file.csv")
q3 = """select sum(gross_amount),
            patient_mrn,invoice_number, patient_gender,patient_age,
            correspondence_address_pincode, ordering_department_name, plan_name,item_group
            from df3 
            group by patient_mrn,invoice_number, patient_gender,patient_age,
            correspondence_address_pincode, ordering_department_name, plan_name,item_group
     """

output = db.execute(q3).df()
output.to_csv("Output\\OPDMemberSummary.csv")
