import pandas as pd
import duckdb as db

claim = pd.read_csv("CSV\\Claims_Master.csv")
claim.rename(columns={'POLICY_NUM': "Policy_number", "MEMBER_ID_CARD_NUM": "Mem_ID"}, inplace=True)
q1 = """select Policy_number, Mem_ID, icd_category, count(claim_num) as claim_count,sum(Aggregate) as Aggregate  
        from claim group by Policy_number, Mem_ID, icd_category"""

member_count_claim = db.sql(""" select Policy_number, Mem_ID, count(Mem_ID) as count 
                   from claim group by Policy_number , Mem_ID""").df()

df2 = db.execute(q1).df()
df1 = df2.merge(member_count_claim, on=["Policy_number", "Mem_ID"])
df1.to_csv("df1.csv")
print(df1["Aggregate"].sum())

member = pd.read_csv("CSV\\Member_Paid.csv")
policy = pd.read_csv("CSV\\Policy.csv")

member_count = db.sql(""" select Policy_number, count(Mem_ID) as count  from member group by Policy_number """).df()
q2 = """select policy.Policy_number, EARNED_PREMIUM/count  as Normalized_Earned_Premium,  
        POLICIES_EXPOSED/count as Normalized_POLICIES_EXPOSED , LIVES_EXPOSED/count as Normalized_LIVES_EXPOSED,
        from policy join member_count 
        on policy.Policy_number =member_count.Policy_number"""
nep = db.execute(q2).df()
norm_policy = policy.merge(nep, on="Policy_number")


q3 = """select norm_policy.Policy_number, Mem_ID, Normalized_Earned_Premium as EARNED_PREMIUM,
           Normalized_POLICIES_EXPOSED as POLICIES_EXPOSED, Normalized_LIVES_EXPOSED as LIVES_EXPOSED,
            Zone,Mem_Gender,
            norm_policy.Sum_Insured, member.Mem_Age, Product_Name,Plan_type, Policy_Period, Office_Name, 
            Channel_type, Channel_Vertical, Ported_Customer, Previous_Company_Name, Revised_Individual_Floater 
            from norm_policy
            inner join member on
            norm_policy.Policy_number = member.Policy_number
            where member.Mem_ID !=''                        
     """
policy_member = db.execute(q3).df()
policy_member.to_csv("pm.csv")

claim_member = policy_member.merge(df1, on=["Policy_number", "Mem_ID"], how="outer")
claim_member.to_csv("dp.csv")

