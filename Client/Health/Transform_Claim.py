import pandas as pd
import duckdb as db


def verify():
    sum_22 = paid_22["PAID_AMT"].sum()
    sum_23 = paid_23["PAID_AMT"].sum()
    sum_os = os_23["PAID_AMT"].sum()
    sum_full = claims["PAID_AMT"].sum()
    diff = sum_full - (sum_os + sum_23 + sum_22)

    print(sum_22)
    print(sum_23)
    print(sum_os)
    print(sum_full)
    print(diff)


paid_23 = pd.read_csv("C:\\SHAI\\Revised 11-12-23\\FY 23_Paid.csv")
paid_22 = pd.read_csv("C:\\SHAI\\Revised 11-12-23\\FY22_Paid.csv")
os_23 = pd.read_csv("C:\\SHAI\\Revised 11-12-23\\FY23_OS.csv")

os_23.rename(columns={'PROVISION_AMT': 'PAID_AMT'}, inplace=True)
claims = pd.concat([paid_22, paid_23, os_23], axis=0)

claims.rename(columns={'POLICY_NUM': "Policy_number", "MEMBER_ID_CARD_NUM": "Mem_ID"}, inplace=True)
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
icd_master = pd.read_csv("C:\\SHAI\\Revised 11-12-23\\ICD_Ver10cm 2019 V1.csv")

claim_master = db.sql("""select consolidated_claim.*, icd_master.ICD_category from consolidated_claim join 
                        icd_master on icd_master.icd_code =  consolidated_claim.icd_code """).df()
q1 = """ select Policy_number, Mem_ID, icd_category, count(claim_num) as claim_count,sum(Aggregate) as Aggregate  
        from claim_master group by Policy_number, Mem_ID, icd_category"""

claim_count = db.execute(q1).df()
print(claim_count["Aggregate"].sum())
claim_count.to_csv("CSV\\Claims_Master.csv")
