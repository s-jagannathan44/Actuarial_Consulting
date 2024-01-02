import pandas as pd
# import duckdb as db


def rename_columns():
    df = pd.read_csv("C:\\SHAI\\Revised 11-12-23\\FY23 Exposure Mapped_Final (1).csv",
                     usecols=['Policy number', 'Policy Start Date', 'Policy End Date', 'Product Name', 'Plan type',
                              'Policy Period', 'Office Name', 'Zone', 'Channel type', 'Channel Vertical',
                              'Ported Customer',
                              'Previous Company Name', 'Inception Date', 'Renewal Count', 'NOP_RCD', 'NOR_RCD',
                              'GWP_RCD',
                              'EARNED_PREMIUM', 'POLICIES_EXPOSED', 'LIVES_EXPOSED', 'Revised Individual/Floater',
                              'POLICY_VERSION_CODE', 'Sum Insured'])
    df.rename(columns={'Policy number': "Policy_number", 'Policy Start Date': "Policy_Start_Date",
                       'Policy End Date': 'Policy_End-Date',
                       'Product Name': 'Product_name', 'Plan type': 'Plan_type', 'Policy Period': 'Policy_Period',
                       'Office Name': 'Office_Name',
                       'Channel type': 'Channel_type', 'Channel Vertical': 'Channel_Vertical',
                       'Ported Customer': 'Ported_Customer',
                       'Previous Company Name': 'Previous_Company_Name', 'Inception Date': 'Inception_Date',
                       'Renewal Count': 'Renewal_Count',
                       'Revised Individual/Floater': 'Revised_Individual_Floater', 'Sum Insured': 'Sum_Insured'},
              inplace=True)
    df.to_csv("CSV\\Policy23.csv")


rename_columns()

# premium = pd.read_csv("CSV\\output.csv")
# print(db.sql("""select sum(EARNED_PREMIUM) ,sum(PROVISION_AMT) from premium """).df())

# member = pd.read_csv("CSV\\df3.csv")
# policy = pd.read_csv("CSV\\Policy.csv")
#
# q1 = """select sum(EARNED_PREMIUM) as EARNED_PREMIUM ,sum(PAID_AMT) as PAID_AMT, Zone,Mem_Gender,
#         policy.Sum_Insured, member.Mem_Age from policy
#         inner join member on
#         policy.Policy_number = member.Policy_number
#         where member.Mem_ID !=''
#         group by policy.Zone , member.Mem_Gender , policy.Sum_Insured, member.Mem_Age
#  """
#
#
# output = db.execute(q1).df()
# output.to_csv("CSV\\output.csv")
# print(db.sql("""select sum(EARNED_PREMIUM) ,sum(PROVISION_AMT) from output """).df())
