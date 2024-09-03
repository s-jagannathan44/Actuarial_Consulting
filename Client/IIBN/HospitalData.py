import pandas as pd
import glob
import duckdb as db


def merge_member_files():
    path = "C:\\Users\\jvpra\\OneDrive\\Desktop\\Narayana\\Hospital_Data/*.csv"
    df = pd.DataFrame()
    files = glob.glob(path)
    for file_name in files:
        frame = pd.read_csv(file_name)
        frame["file_name"] = file_name[:-3]
        frame["key"] = frame["patient_mrn"] + "_" +  frame["invoice_number"]
        df = pd.concat([df, frame], axis=0)
    df = df[~df.patient_type.isin(["INTERNATIONAL", "STAFF"])]
    df.to_csv("Output\\merged_hospitalisation_file.csv")
    return df


# df3 = merge_member_files()
df3 = pd.read_csv("Output\\merged_hospitalisation_file.csv")
q3 = """select sum(gross_amount),
            patient_mrn,invoice_number, admitted_for,admission_date,patient_gender,patient_age,
            correspondence_address_pincode, tariff_class, ordering_department_name
            from df3
            group by patient_mrn,invoice_number, admitted_for,admission_date,patient_gender,patient_age,
            correspondence_address_pincode, tariff_class, ordering_department_name
     """

output = db.execute(q3).df()
output["Key"] = output["patient_mrn"] + "_" +  output["invoice_number"]
output.to_csv("Output\\MemberSummary_v2.csv")
