import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from sklearn.model_selection import train_test_split
import statsmodels.discrete.count_model as dcm
import duckdb as db

df = pd.read_csv("CSV\\FrequencyModelFile.csv")
# df = df.loc[:, ['Zone', 'Mem_Age_New', "Claim_Count", "LIVES_EXPOSED", "EARNED_PREMIUM"]]
df["Claim_Count"] = df["Claim_Count"].fillna(0)
df["LIVES_EXPOSED"] = df["LIVES_EXPOSED"].clip(lower=1)
df["frequency"] = df["Claim_Count"] / df["LIVES_EXPOSED"]
df2 = df[df["frequency"] < 1]
df2 = df2[df2["frequency"]>0]
print(df2["EARNED_PREMIUM"].sum() / df["EARNED_PREMIUM"].sum())

x_train, x_test, y_train, y_test = train_test_split(df2,df2["frequency"], test_size=0.2, random_state=25)


out = dcm.ZeroInflatedPoisson.from_formula(formula="frequency ~ Mem_Age_New + Renewal_Count_New + Mem_Gender_New + "
                                                   "Sum_Insured_New + Channel_type_New + Product_Name_New + "
                                                   "Revised_Individual_Floater_New",data=x_train)


result = out.fit_regularized(maxiter=100)

print("-----------Summary-----------")
summary = result.summary2()
print(summary)
with open('All_Var.txt', 'w') as fh:
    fh.write(summary.as_text())

print("-----------predict-----------")
y_pred = result.predict(x_test)
x_test["Pred"] = y_pred
x_test.to_csv("df_test.csv")
