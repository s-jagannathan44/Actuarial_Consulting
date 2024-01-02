import pandas as pd
import duckdb as ps
# df = pd.read_csv("thousand.csv")
ps.default_connection.execute("SET GLOBAL pandas_analyze_sample=100000")
df = pd.read_csv("C:\\SHAI\Revised 11-12-23\FY23 Exposure Mapped_Final.csv")
print(df['EARNED_PREMIUM'].sum())

# df.head(1000).to_csv("thousand.csv")
# q1 = """SELECT  SUM(EARNED_PREMIUM) FROM df where Mem Age 2 is not null OR
# Mem Age 3 is not null OR Mem Age 4 is not null OR Mem Age 5 is not null OR Mem Age 6 is not null OR Mem Age 7 is not null OR Mem Age 8 is not null OR Mem Age 9 is not null OR Mem Age 10 is not null
# """
# df.rename(columns={"Policy number": "Policy_number", "Plan type": "Plan_type", "Product Name": "Product_Name", "Channel Vertical": "Channel_Vertical", "Revised Individual/Floater" : "Revised_Individual/Floater"}, inplace=True)
df.rename(columns={"Policy number": "Policy_number",}, inplace=True)
df.rename(columns={"Mem ID 2": "Mem_ID_2", "Mem ID 3": "Mem_ID_3", "Mem ID 5": "Mem_ID_5", "Mem ID 7": "Mem_ID_7", "Mem ID 9": "Mem_ID_9", "Mem ID 10": "Mem_ID_10"}, inplace=True)

q2 = """ SELECT Policy_number, COUNT(Mem_ID_2)+COUNT(Mem_ID_3)+COUNT(Mem_ID_5)+COUNT(Mem_ID_7)+COUNT(Mem_ID_9)+COUNT(Mem_ID_10) Member_count
FROM df  GROUP BY Policy_number
"""
df2 = ps.query(q2).df()
df3 = pd.merge(df, df2, on="Policy_number")
df3.to_csv("M3.csv")
#
# q1= """ SELECT SUM(EARNED_PREMIUM) as EP, Zone, Plan_type, Product_Name,
# FROM df
# GROUP BY Zone, Plan_type, Product_Name
# """
#
# ps.query(q2).df().to_csv("duck.csv")
#


