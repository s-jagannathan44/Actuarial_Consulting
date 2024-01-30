import pandas as pd
import statsmodels.formula.api as smf
from sklearn.model_selection import train_test_split
from statsmodels.genmod.families import Gamma, links
import joblib

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


def predict_model():
    model = joblib.load("claims.sav")
    print("-----------predict-----------")
    test_input = pd.read_csv("text.csv")
    y_pred = model.predict(test_input)
    test["Pred"] = y_pred
    test.to_csv("text_out.csv")


df = pd.read_csv("CSV\\ClaimsModelFile.csv")
df["Financial_Year"] = df["Financial_Year"].apply(lambda x: transform_fy(x))

train, test = train_test_split(df, test_size=0.2, random_state=25)

link = links.log()
result = smf.glm(formula="Aggregate ~  Mem_Age_New + Renewal_Count_New + Product_Name_New +Zone + Financial_Year"
                         "+ Mem_Gender_New + Sum_Insured_New +  Channel_type_New + Revised_Individual_Floater_New",
                 data=train, family=Gamma(link=link),
                 exposure=train["claim_count"]).fit()
joblib.dump(result, "claims.sav")

print("-----------Summary-----------")
# print(result.summary2())

print("-----------predict-----------")
y_pred = result.predict(test)
test["Pred"] = y_pred
test.to_csv("output.csv")
