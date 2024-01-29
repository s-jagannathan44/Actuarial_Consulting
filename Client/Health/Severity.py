import pandas as pd
import statsmodels.formula.api as smf
from sklearn.model_selection import train_test_split
from statsmodels.genmod.families import Gamma, links

df = pd.read_csv("CSV\\PolicyMemberClaim.csv")
train, test = train_test_split(df, test_size=0.2, random_state=25)

link = links.log()
result = smf.glm(formula="Aggregate ~  Mem_Age + ICD_category + Financial_Year ", data=train, family=Gamma(link=link),
                 exposure=train["claim_count"]).fit()

print("-----------Summary-----------")
print(result.summary2())

print("-----------predict-----------")
y_pred = result.predict(test)
test["Pred"] = y_pred
test.to_csv("output.csv")
