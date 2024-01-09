import pandas as pd
import duckdb as db


def write_to_file():
    df1.to_csv("CSV\\1.csv")
    df2.to_csv("CSV\\2.csv")
    df3.to_csv("CSV\\3.csv")
    df4.to_csv("CSV\\4.csv")
    df5.to_csv("CSV\\5.csv")
    df6.to_csv("CSV\\6.csv")


df = pd.read_csv("C:\\SHAI\\Revised 11-12-23\\FY23 Exposure Mapped_Final (1).csv", usecols=['Member ID 1', 'Member ID 2', 'Member ID 3', 'Member ID 4', 'Member ID 5', 'Member ID 6', 'Member Age 1', 'Member Age 2', 'Member Age 3', 'Member Age 4', 'Member Age 5', 'Member Age 6', 'Member Gender 1', 'Member Gender 2', 'Member Gender 3', 'Member Gender 4', 'Member Gender 5', 'Member Gender 6', 'Policy number' ])
#df = df.filter(['Member ID 1', 'Member ID 2', 'Member ID 3', 'Member ID 4', 'Member ID 5', 'Member ID 6', 'Member Age 1', 'Member Age 2', 'Member Age 3', 'Member Age 4', 'Member Age 5', 'Member Age 6', 'Member Gender 1', 'Member Gender 2', 'Member Gender 3', 'Member Gender 4', 'Member Gender 5', 'Member Gender 6', 'Policy number' ])

print("read complete")
df1 = pd.DataFrame(columns=["Policy_number", "Mem_ID", "Mem_Age", "Mem_Gender"])
df2 = pd.DataFrame(columns=["Policy_number", "Mem_ID", "Mem_Age", "Mem_Gender"])
df3 = pd.DataFrame(columns=["Policy_number", "Mem_ID", "Mem_Age", "Mem_Gender"])
df4 = pd.DataFrame(columns=["Policy_number", "Mem_ID", "Mem_Age", "Mem_Gender"])
df5 = pd.DataFrame(columns=["Policy_number", "Mem_ID", "Mem_Age", "Mem_Gender"])
df6 = pd.DataFrame(columns=["Policy_number", "Mem_ID", "Mem_Age", "Mem_Gender"])

df1[["Policy_number", "Mem_ID", "Mem_Age", "Mem_Gender"]] = df[
    ["Policy number", "Member ID 1", "Member Age 1", "Member Gender 1"]]
df2[["Policy_number", "Mem_ID", "Mem_Age", "Mem_Gender"]] = df[
    ["Policy number", "Member ID 2", "Member Age 2", "Member Gender 2"]]
df3[["Policy_number", "Mem_ID", "Mem_Age", "Mem_Gender"]] = df[
    ["Policy number", "Member ID 3", "Member Age 3", "Member Gender 3"]]
df4[["Policy_number", "Mem_ID", "Mem_Age", "Mem_Gender"]] = df[
    ["Policy number", "Member ID 4", "Member Age 4", "Member Gender 4"]]
df5[["Policy_number", "Mem_ID", "Mem_Age", "Mem_Gender"]] = df[
    ["Policy number", "Member ID 5", "Member Age 5", "Member Gender 5"]]
df6[["Policy_number", "Mem_ID", "Mem_Age", "Mem_Gender"]] = df[
    ["Policy number", "Member ID 6", "Member Age 6", "Member Gender 6"]]
print("assign complete")


# write_to_file()

df8 = pd.concat([df1, df2, df3, df4, df5, df6], axis=0)
print("append complete")
df8.rename(columns={"Policy number": "Policy_number"}, inplace=True)
df9 = db.sql("select * from df8 where Mem_ID is not null").df()
df9.to_csv("CSV\\Member_23.csv")


def merge_claim():
    df7 = pd.read_csv("C:\\SHAI\\Revised 11-12-23\\FY 23_Paid.csv")
    df7 = df7.filter(['POLICY_NUM', 'MEMBER_ID_CARD_NUM', 'PAID_AMT'])
    print("execute started")
    q1 = """select df8.Mem_ID, df8.Mem_Age, df8.Mem_Gender, df8.Policy_number, df7.PAID_AMT from df7
 right outer join df8 on df8.Policy_number = df7.POLICY_NUM and df8.Mem_ID = df7.MEMBER_ID_CARD_NUM"""
    df9 = db.execute(q1).df()
    df9.to_csv("CSV\\Member22.csv")





