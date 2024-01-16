import pandas as pd
import duckdb as db


def summaries():
    q3 = """select sum(Normalized_Earned_Premium) as EARNED_PREMIUM ,sum(PAID_AMT) as PAID_AMT,
           sum(Normalized_POLICIES_EXPOSED) as POLICIES_EXPOSED, sum(Normalized_LIVES_EXPOSED) as LIVES_EXPOSED,
            Zone,Mem_Gender,
            norm_policy.Sum_Insured, member.Mem_Age, Product_Name,Plan_type, Policy_Period, Office_Name, 
            Channel_type, Channel_Vertical, Ported_Customer, Previous_Company_Name, Revised_Individual_Floater 
            from norm_policy
            inner join member on
            norm_policy.Policy_number = member.Policy_number
            where member.Mem_ID !=''
            group by norm_policy.Zone , member.Mem_Gender , norm_policy.Sum_Insured, member.Mem_Age, 
            Product_Name,Plan_type, Policy_Period, Office_Name, Channel_type, Channel_Vertical, Ported_Customer, 
            Previous_Company_Name, Revised_Individual_Floater            
     """

    output = db.execute(q3).df()
    output.to_csv("CSV\\SummaryExposed_21.csv")


member = pd.read_csv("CSV\\Member21.csv")
policy = pd.read_csv("CSV\\Policy21.csv")

member_count = db.sql(""" select Policy_number, count(Mem_ID) as count  from member group by Policy_number """).df()
# q1 = """select policy.Policy_number, EARNED_PREMIUM, count , EARNED_PREMIUM/count  from policy join member_count
#         on policy.Policy_number =member_count.Policy_number"""
# ep = db.execute(q1).df().to_csv("csv\\ep.csv")
q2 = """select policy.Policy_number, EARNED_PREMIUM/count  as Normalized_Earned_Premium,  
        POLICIES_EXPOSED/count as Normalized_POLICIES_EXPOSED , LIVES_EXPOSED/count as Normalized_LIVES_EXPOSED,
        from policy join member_count 
        on policy.Policy_number =member_count.Policy_number"""
nep = db.execute(q2).df()
norm_policy = policy.merge(nep, on="Policy_number")
# norm_policy.to_csv("csv\\norm_policy.csv")
summaries()


# db.execute(q1).df().to_csv("membercount.csv")
# print(db.sql("""select count(Mem_ID), count(distinct Mem_ID)  from member"""))
# db.sql("""select  Mem_ID, count(Mem_ID) from member group by Mem_ID having count(Mem_ID) >1  """).to_csv("CSV\\duplicates.csv")
