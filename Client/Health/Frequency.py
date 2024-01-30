import pandas as pd
from sklearn.model_selection import train_test_split
import statsmodels.discrete.count_model as dcm
import joblib
import numpy

def transform_fy(year):
    if year == "FY18":
        return 1
    elif year == "FY19":
        return 2
    elif year == "FY20":
        return 3
    elif year == "FY21":
        return 4
    elif year == "FY22":
        return 5
    elif year == "FY23":
        return 6


def fit_zip():
    result = out.fit_regularized(maxiter=100)
    joblib.dump(result, "result.sav")
    print("-----------Summary-----------")
    summary = result.summary2()
    print(summary)
    with open('All_Var.txt', 'w') as fh:
        fh.write(summary.as_text())


def forecast_model():
    model = joblib.load("result.sav")
    print("-----------predict-----------")
    test = pd.read_csv("text.csv")
    y_pred = model.predict(test)
    test["Pred"] = y_pred
    test.to_csv("text_forecast.csv")


def predict_model():
    model = joblib.load("result.sav")
    print("-----------predict-----------")
    test.to_csv("OOS.csv")
    y_pred = model.predict(test)
    test["Pred"] = y_pred
    test.to_csv("text_out.csv")


df = pd.read_csv("CSV\\FrequencyModelFile.csv")
# df = df.loc[:, ['Zone', 'Mem_Age_New', "Claim_Count", "LIVES_EXPOSED", "EARNED_PREMIUM"]]
df["Claim_Count"] = df["Claim_Count"].fillna(0)
df["LIVES_EXPOSED"] = df["LIVES_EXPOSED"].clip(lower=1)
df["Frequency"] = df["Claim_Count"] / df["LIVES_EXPOSED"]
df["Financial_Year"] = df["Financial_Year"].apply(lambda x: transform_fy(x))
train, test = train_test_split(df, test_size=0.2, random_state=25)

out = dcm.ZeroInflatedPoisson.from_formula(formula="Frequency ~ Mem_Age_New + Renewal_Count_New + Mem_Gender_New + Zone"
                                                   "+ Sum_Insured_New + Channel_type_New + Product_Name_New +"
                                                   "Revised_Individual_Floater_New + Financial_Year", data=train)

fit_zip()
predict_model()
