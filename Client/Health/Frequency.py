
import pandas as pd
from sklearn.model_selection import train_test_split
import statsmodels.discrete.count_model as dcm
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder


df = pd.read_csv("CSV\\forecast.csv")
# df = df.loc[:, ['Zone', 'Mem_Age_New', "Claim_Count", "LIVES_EXPOSED", "EARNED_PREMIUM"]]
df["Claim_Count"] = df["Claim_Count"].fillna(0)
df["LIVES_EXPOSED"] = df["LIVES_EXPOSED"].clip(lower=1)
df2 = df[df["Frequency"] < 1]
df2 = df2[df2["Frequency"]>0]
print(df2["EARNED_PREMIUM"].sum() / df["EARNED_PREMIUM"].sum())

linear_model_preprocessor = ColumnTransformer(
        [
            ("passthrough1", "passthrough", ["Frequency"]),
            (
                "onehot_categorical",
                OrdinalEncoder(),
                ["Financial_Year"]
            ),
        ],
        remainder='drop'
    )

y= linear_model_preprocessor.fit_transform(df2)
df3 = pd.DataFrame(y,columns=["Frequency","Financial_Year"])

x_train, x_test, y_train, y_test = train_test_split(df3,df3["Frequency"], test_size=0.2, random_state=25)


out = dcm.ZeroInflatedPoisson.from_formula(formula="Frequency ~ Financial_Year",data=x_train)


result = out.fit_regularized(maxiter=100)

print("-----------Summary-----------")
summary = result.summary2()
print(summary)
with open('All_Var.txt', 'w') as fh:
    fh.write(summary.as_text())

print("-----------predict-----------")
test = pd.read_csv("input.csv.csv")

y_pred = result.predict(test)
print(y_pred)