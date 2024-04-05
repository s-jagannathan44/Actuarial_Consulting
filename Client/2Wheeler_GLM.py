import joblib
import numpy as np
import pandas as pd
from statsmodels.genmod.families import Tweedie
import statsmodels.formula.api as smf


def make_multi(dataframe, columns):
    df2 = pd.pivot_table(dataframe, values="PAID_AMT Pred_Cost LIVES_EXPOSED".split(), columns=columns,
                         aggfunc="sum").T
    df2["Actual"] = df2["PAID_AMT"] / df2["LIVES_EXPOSED"]
    df2["Predicted"] = df2["Pred_Cost"] / df2["LIVES_EXPOSED"]
    df2["Error"] = (df2["Actual"] - df2["Predicted"]) / df2["Actual"]
    df2["Error"] = df2["Error"].abs()
    df2['%ageError'] = df2['Error'].map('{:.2%}'.format)
    below_ten = df2[df2["Error"] <= 0.1]["LIVES_EXPOSED"].sum()
    total = df2["LIVES_EXPOSED"].sum()
    print('{:.2%}'.format(below_ten / total))
    df2.to_csv("Bazaar\\Output\\multi.csv")


def make_pivots(dataframe, columns):
    df2 = pd.pivot_table(dataframe, values="PAID_AMT  Pred_Cost LIVES_EXPOSED".split(), columns=columns,
                         aggfunc="sum").T
    df2["Actual"] = df2["PAID_AMT"] / df2["LIVES_EXPOSED"]
    df2["Predicted"] = df2["Pred_Cost"] / df2["LIVES_EXPOSED"]
    df2["Error"] = (df2["Actual"] - df2["Predicted"]) / df2["Actual"]
    df2["Error"] = df2["Error"].abs()
    df2['%ageError'] = df2['Error'].map('{:.2%}'.format)
    df2.to_csv("Bazaar\\Output\\" + columns + ".csv")


def build_model():
    df = pd.read_csv("Bazaar\\Output\\2WheeleerFiles.csv")
    df["Loss_Cost"] = df["PAID_AMT"] / df["LIVES_EXPOSED"]
    result = smf.glm(
        formula='Loss_Cost ~ Zone_new + CC_Make_new + body_type + plancategory_new + Age_new',
        data=df, family=Tweedie(var_power=1.9), var_weights=df["LIVES_EXPOSED"]).fit()
    joblib.dump(result, "Bazaar\\Output\\2Wheeleer.sav")
    return df


df =  build_model()  # pd.read_csv("Bazaar\\Output\\4WheelerTestFile.csv")
result2 = joblib.load("Bazaar\\Output\\2Wheeleer.sav")
print("-----------Summary-----------")
print(result2.summary2())
print("-----------GLM simple form relativity-----------")
print(np.exp(result2.params))
print("-----------predict-----------")
y_pred = result2.predict(df)
df["Pred"] = y_pred
df["Pred_Cost"] = df["Pred"] * df["LIVES_EXPOSED"]
df.to_csv("Bazaar\\Output\\2wheeler.csv")
# make_pivots(df, "Accident_Year_new")
make_pivots(df, "Zone_new")
make_pivots(df, "body_type")
make_pivots(df, "plancategory_new")
make_pivots(df, "Age_new")
make_pivots(df, "CC_Make_new")


