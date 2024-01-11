import datetime

import pandas as pd
import duckdb as db


def verify():
    sum_21 = paid_21["PAID_AMT"].sum()
    sum_22 = paid_22["PAID_AMT"].sum()
    sum_23 = paid_23["PAID_AMT"].sum()
    sum_os = os_23["PAID_AMT"].sum()
    sum_full = claims["PAID_AMT"].sum()
    diff = sum_full - (sum_os + sum_23 + sum_22 + sum_21)

    print(sum_21)
    print(sum_22)
    print(sum_23)
    print(sum_os)
    print(sum_full)
    print(diff)


def set_financial_year(admission_dt):
    if (admission_dt > datetime.datetime(2020, 3, 31)) & (admission_dt < datetime.datetime(2021, 4, 1)):
        return "FY21"
    elif (admission_dt > datetime.datetime(2021, 3, 31)) & (admission_dt < datetime.datetime(2022, 4, 1)):
        return "FY22"
    elif (admission_dt > datetime.datetime(2022, 3, 31)) & (admission_dt < datetime.datetime(2023, 4, 1)):
        return "FY23"


paid_23 = pd.read_csv("C:\\SHAI\\Revised 11-12-23\\FY23 Paid_Final.csv")
paid_22 = pd.read_csv("C:\\SHAI\\Revised 11-12-23\\FY22 Paid_Final.csv")
paid_21 = pd.read_csv("C:\\SHAI\\Revised 11-12-23\\FY21 Paid_Final.csv")
os_23 = pd.read_csv("C:\\SHAI\\Revised 11-12-23\\FY23_OS.csv")

os_23.rename(columns={'PROVISION_AMT': 'PAID_AMT'}, inplace=True)
claims = pd.concat([paid_23, paid_22, paid_21, os_23], axis=0)
claims['ADMISSION_DT'] = pd.to_datetime(claims['ADMISSION_DT'], format="mixed", dayfirst=True)
claims["Financial_Year"] = claims["ADMISSION_DT"].apply(lambda x: set_financial_year(x))

claims = db.query("""select * from claims where PROD_TYPE != 'Group' """).df()

claims.rename(columns={'POLICY_NUM': "Policy_number", "MEMBER_ID_CARD_NUM": "Mem_ID"}, inplace=True)
claims["Policy_number"] = claims["Financial_Year"] + claims["Policy_number"]
claims["Mem_ID"] = claims["Financial_Year"]+claims["Mem_ID"]


q1 = """SELECT claims.*,filter.Aggregate
FROM claims
JOIN
    (SELECT CLAIM_NUM, sum(PAID_AMT) as Aggregate
    FROM claims
    GROUP BY CLAIM_NUM
    ) filter
    ON claims.CLAIM_NUM = filter.CLAIM_NUM """

consolidated_claim = db.execute(q1).df()

consolidated_claim.drop_duplicates(subset="CLAIM_NUM", inplace=True)
print(consolidated_claim["Aggregate"].sum())
consolidated_claim.to_csv("console.csv")
icd_master = pd.read_csv("C:\\SHAI\\Revised 11-12-23\\ICD_Ver10cm 2019 V1.csv")

claim_master = db.sql("""select consolidated_claim.*, icd_master.ICD_category from consolidated_claim left join 
                        icd_master on icd_master.icd_code =  consolidated_claim.icd_code """).df()

q1 = """ select Policy_number, Mem_ID, icd_category, Financial_Year, count(claim_num) as claim_count,sum(Aggregate) as Aggregate

        from claim_master group by Policy_number, Mem_ID, icd_category,Financial_Year"""
claim_count = db.execute(q1).df()

# claim_final = db.sql("""select claim_count.*, claim_master.Quarter from claim_count left join
#                         claim_master on claim_master.Policy_number =  claim_count.Policy_number and
#                         claim_master.Mem_Id =  claim_count.Mem_Id""").df()


print(claim_count["Aggregate"].sum())
for col in claim_count.columns:
    if "Unnamed" in col:
        claim_count.drop(col, axis=1, inplace=True)

claim_count.to_csv("CSV\\Claims_Merged.csv")

