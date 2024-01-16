import pandas as pd
import statsmodels.formula.api as smf
from sklearn.model_selection import train_test_split
from statsmodels.genmod.families import Poisson, links
import duckdb as db

df = pd.read_csv("CSV\\SummaryExposed_Merged(1).csv")
df["Claim_Count"] = df["Claim_Count"].fillna(0)
df["LIVES_EXPOSED"] = df[df["LIVES_EXPOSED"] >1]["LIVES_EXPOSED"]
df["frequency"] = df["Claim_Count"] / df["LIVES_EXPOSED"]
df2 = df[df["frequency"] <1 ]
df2.to_csv("basefile.csv")

print(df["EARNED_PREMIUM"].sum()/df2["EARNED_PREMIUM"].sum())

train, test = train_test_split(df2, test_size=0.2, random_state=25)

# result=smf.poisson(formula = "Claim_Count ~  Mem_Age", data=train,
#                    exposure=train["LIVES_EXPOSED"]).fit()

link = links.log()
train["LIVES_EXPOSED"] = train["LIVES_EXPOSED"].apply(lambda x: 1 if x <= 0 else x)
result = smf.glm(formula="frequency ~ Mem_Age",
                 data=train, family=Poisson(link=link), exposure=train["LIVES_EXPOSED"]).fit()

print("-----------Summary-----------")
print(result.summary2())

print("-----------predict-----------")
y_pred = result.predict(test)
test["Pred"] = y_pred
test.to_csv("freq.csv")
