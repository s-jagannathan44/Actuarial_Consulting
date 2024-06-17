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
    df2["Error"] = (df2["Predicted"] - df2["Actual"]) / df2["Actual"]
    df2["Error"] = df2["Error"].abs()
    df2['%ageError'] = df2['Error'].map('{:.2%}'.format)
    below_ten = df2[df2["Error"] <= 0.1]["LIVES_EXPOSED"].sum()
    total = df2["LIVES_EXPOSED"].sum()
    print('{:.2%}'.format(below_ten / total))
    df2.to_csv("Bazaar\\TW\\CSV\\Files\\Output\\multi.csv")


def make_pivots(dataframe, columns):
    df2 = pd.pivot_table(dataframe, values="PAID_AMT  Pred_Cost LIVES_EXPOSED".split(), columns=columns,
                         aggfunc="sum").T
    df2["Actual"] = df2["PAID_AMT"] / df2["LIVES_EXPOSED"]
    df2["Predicted"] = df2["Pred_Cost"] / df2["LIVES_EXPOSED"]
    df2["Error"] = (df2["Predicted"] - df2["Actual"]) / df2["Actual"]
    df2['%ageError'] = df2['Error'].map('{:.2%}'.format)
    df2.to_csv("Bazaar\\TW\\CSV\\Files\\Output\\" + columns + ".csv")


def build_model():
    df_ = pd.read_csv("Bazaar\\TW\\CSV\\Files\\Output\\2WheelerNewLargeFiles.csv")
    df_["Loss_Cost"] = df_["PAID_AMT"] / df_["LIVES_EXPOSED"]
    result = smf.glm(
        formula='Loss_Cost ~  cc_new +  body_type_new  + Zone_new + Make_new',
        data=df_, family=Tweedie(var_power=1.9), var_weights=df_["LIVES_EXPOSED"]).fit()
    joblib.dump(result, "Bazaar\\TW\\CSV\\Files\\Output\\2WheeleerLarge.sav")
    return df_


df =  pd.read_csv("Bazaar\\TW\\CSV\\Files\\Output\\2WheelerNewLargeFile.csv") # build_model() #
result2 = joblib.load("Bazaar\\TW\\CSV\\Files\\Output\\2WheeleerLarge.sav")
print("-----------Summary-----------")
print(result2.summary2())
print("-----------GLM simple form relativity-----------")
print(np.exp(result2.params))
print("-----------predict-----------")
y_pred = result2.predict(df)
df["Pred"] = y_pred
df["Pred_Cost"] = df["Pred"] * df["LIVES_EXPOSED"]
df.to_csv("Bazaar\\TW\\CSV\\Files\\Output\\2wheelerOutputLarge.csv")


make_pivots(df, "Zone")
make_pivots(df, "body_type")
make_pivots(df, "ccnew")
make_pivots(df, "Make")

