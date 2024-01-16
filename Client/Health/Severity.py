import pandas as pd
import duckdb as db
import statsmodels.formula.api as smf
import statsmodels.genmod.families.links
from sklearn.model_selection import train_test_split
from statsmodels.genmod.families import Gamma, links


def create_file():
    policy = pd.read_csv("CSV\\Policy_Merged.csv")
    member = pd.read_csv("CSV\\Member_Merged.csv")
    claim = pd.read_csv("CSV\\Claims_Merged.csv")
    q1 = """select claim.*, Zone,Renewal_Count,
            Sum_Insured, Product_Name,Plan_type,  
            Channel_type, Revised_Individual_Floater from claim inner join policy on claim.Policy_number = policy.policy_number and 
            claim.Financial_Year = policy.Financial_Year  where claim.Mem_ID !='' """
    policy_claim = db.execute(q1).df()
    policy_claim.to_csv("CSV\\Sev.csv")
    q2 = """select policy_claim.*,  member.Mem_Age, Mem_Gender from policy_claim join member on 
policy_claim.Policy_number = member.policy_number and 
            policy_claim.Mem_Id = member.Mem_Id  and policy_claim.Financial_Year = member.Financial_Year   """
    member_claim = db.execute(q2).df()
    member_claim.to_csv("CSV\\PolicyMemberClaim.csv")



df = pd.read_csv("CSV\\PolicyMemberClaim.csv")
train,test= train_test_split(df, test_size=0.2,  random_state=25)

link = links.log()
result=smf.glm(formula = "Aggregate ~  Mem_Age + ICD_category + Financial_Year ", data=train, family =Gamma(link=link),
               exposure = train["claim_count"]).fit()

print("-----------Summary-----------")
print(result.summary2())


print("-----------predict-----------")
y_pred = result.predict(test)
test["Pred"] = y_pred
test.to_csv("output.csv")




