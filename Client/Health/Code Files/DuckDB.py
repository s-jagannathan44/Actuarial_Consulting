import pandas as pd
import duckdb as db
# df = pd.read_csv("thousand.csv")
db.default_connection.execute("SET GLOBAL pandas_analyze_sample=100000")
df = pd.read_csv("C:\\SHAI\Revised 11-12-23\FY23 Exposure Mapped_Final.csv")
df = df.head(5000000)
df2 = pd.read_csv("C:\\SHAI\Revised 11-12-23\FY23 OS.csv")
print("read complete")
df["I1"] = 2
df["I2"] = 3
df["I3"] = 5
df["I4"] = 7
df["I5"] = 9
df["I6"] = 11
df.rename(columns={"Mem ID 2": "Member_ID_2", "Mem ID 3": "Member_ID_3","Mem ID 5": "Member_ID_5",
                   "Mem ID 7": "Member_ID_7","Mem ID 9": "Member_ID_9", "Mem ID 10": "Member_ID_10"}, inplace=True)

print("rename complete")
q1 = """create table T1 as select df2.PROVISION_AMT as Income, df2.MEMBER_ID_CARD_NUM as Id,        
        case when df.Member_ID_2 = Id then 2 when df.Member_ID_3 = Id then 3  
        when df.Member_ID_5 = Id then 5 when df.Member_ID_7 = Id then 7
        when df.Member_ID_9 = Id then 9 when df.Member_ID_10 = Id then 10 
        else 0 end as Index  from df2
        right outer join df on df.Member_ID_2 = df2.MEMBER_ID_CARD_NUM
        or df.Member_ID_3 = df2.MEMBER_ID_CARD_NUM or df.Member_ID_5 = df2.MEMBER_ID_CARD_NUM 
        or df.Member_ID_7 = df2.MEMBER_ID_CARD_NUM or df.Member_ID_9 = df2.MEMBER_ID_CARD_NUM
        or df.Member_ID_10 = df2.MEMBER_ID_CARD_NUM """

db.execute(q1)
print("execute complete")

q2 = """update T1 set I1=case when Index = 2 Then Income else 0 end """
q3 = """update T1 set I2=case when Index = 3 Then Income else 0 end """
q5 = """update T1 set I3=case when Index = 5 Then Income else 0 end """
q7 = """update T1 set I4=case when Index = 7 Then Income else 0 end """
q9 = """update T1 set I5=case when Index = 9 Then Income else 0 end """
q11 = """update T1 set I5=case when Index = 10 Then Income else 0 end """

db.execute(q2)
db.execute(q3)
db.execute(q5)
db.execute(q7)
db.execute(q9)
db.execute(q11)
print("update complete")
df6 = db.sql("select * from T1").df()
df6.head(500000).to_csv("db6.csv")

# print(df3)
# flag = True
# flagfor3 = True
# for index, row in df3.iterrows():
#     name2 = row["Mem_ID_2"]
#     name3 = row["Mem_ID_3"]
#     name5 = row["Mem_ID_5"]
#     name7 = row["Mem_ID_7"]
#
#     if name2 is not None and name3 is None and name5 is None and name7 is None:
#         Income = df3.loc[index, "Income"]
#         df3.loc[index, "Income1"] = Income
#     if name2 is not None and name3 is None and name5 is not None and name7 is None and flag:
#         flag = False
#         Income1 = df3.loc[index, "Income"]
#         Income3 = df3.loc[index + 2, "Income"]
#         df3.loc[index, "Income1"] = Income1
#         df3.loc[index, "Income3"] = Income3
#     if name2 is None and name3 is not None and name5 is None and name7 is None:
#         Income = df3.loc[index, "Income"]
#         df3.loc[index, "Income2"] = Income
#     if name2 is None and name3 is None and name5 is None and name7 is not None:
#         Income = df3.loc[index, "Income"]
#         df3.loc[index, "Income4"] = Income
#     if name2 is not None and name3 is not None and name5 is not None and name7 is not None and flagfor3:
#         flagfor3 = False
#         Income1 = df3.loc[index, "Income"]
#         Income2 = df3.loc[index + 1, "Income"]
#         Income3 = df3.loc[index+2, "Income"]
#         Income4 = df3.loc[index + 3, "Income"]
#         df3.loc[index, "Income1"] = Income1
#         df3.loc[index, "Income2"] = Income2
#         df3.loc[index, "Income3"] = Income3
#         df3.loc[index, "Income4"] = Income4
#
# df3.drop(columns="Income", inplace=True)
# # df4 = df3.drop(df3[(df3.Income1.isna()) & (df3.Income2.isna()) & df3.Income3.isna() & df3.Income4.isna()].index)
# df3.to_csv("duckDB.csv")