import pandas as pd
import duckdb as db


def summaries():
    q3 = """select sum(Normalized_Earned_Premium) as EARNED_PREMIUM,sum(Aggregate) as PAID_AMT,sum(claim_count) as CC, 
           sum(Normalized_POLICIES_EXPOSED) as POLICIES_EXPOSED, sum(Normalized_LIVES_EXPOSED) as LIVES_EXPOSED,
            icd_category,Zone,Mem_Gender,
            norm_policy.Sum_Insured, member_claim.Mem_Age, Product_Name,Plan_type, Policy_Period, Office_Name, 
            Channel_type, Channel_Vertical, Ported_Customer, Previous_Company_Name, Revised_Individual_Floater 
            from norm_policy
            inner join member_claim on
            norm_policy.Policy_number = member_claim.Policy_number
            where member_claim.Mem_ID !=''
            group by norm_policy.Zone , member_claim.Mem_Gender , norm_policy.Sum_Insured, member_claim.Mem_Age, 
            Product_Name,Plan_type, Policy_Period, Office_Name, Channel_type, Channel_Vertical, Ported_Customer, 
            Previous_Company_Name, Revised_Individual_Floater,icd_category            
     """

    output = db.execute(q3).df()
    output.to_csv("CSV\\SummaryExposed_23.csv")


def verify():
    print(claim["Aggregate"].sum())
    print(policy["EARNED_PREMIUM"].sum())


claim = pd.read_csv("CSV\\Claims_Master.csv")
claim.rename(columns={'POLICY_NUM': "Policy_number", "MEMBER_ID_CARD_NUM": "Mem_ID"}, inplace=True)
policy = pd.read_csv("CSV\\Policy23.csv")
member = pd.read_csv("CSV\\Member_23.csv")

member_claim = member.merge(claim, on=["Policy_number", "Mem_ID"], how="left")

member_count = db.sql(""" select Policy_number, count(Mem_ID) as count  from member_claim group by Policy_number """).df()

q2 = """select policy.Policy_number, EARNED_PREMIUM/count  as Normalized_Earned_Premium,  
        POLICIES_EXPOSED/count as Normalized_POLICIES_EXPOSED , LIVES_EXPOSED/count as Normalized_LIVES_EXPOSED,
        from policy join member_count 
        on policy.Policy_number =member_count.Policy_number"""
nep = db.execute(q2).df()
norm_policy = policy.merge(nep, on="Policy_number")

summaries()
