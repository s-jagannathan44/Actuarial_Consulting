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
        formula='Loss_Cost ~ cc_large + Make_large + body_type_large + Zone_large + Insurer_large',
        data=df_, family=Tweedie(var_power=1.9), var_weights=df_["LIVES_EXPOSED"]).fit()
    joblib.dump(result, "Bazaar\\TW\\CSV\\Files\\Output\\2WheelerLarge.sav")
    return df_


df = pd.read_csv("Bazaar\\TW\\CSV\\Files\\Output\\2WheelerFullFile.csv")  # build_model()  #
result2 = joblib.load("Bazaar\\TW\\CSV\\Files\\Output\\2WheelerLarge.sav")
print("-----------Summary-----------")
print(result2.summary2())
print("-----------GLM simple form relativity-----------")
print(np.exp(result2.params))
print("-----------predict-----------")
y_pred = result2.predict(df)
df["Pred_large"] = y_pred
df["Pred_Cost_large"] = df["Pred_large"] * df["LIVES_EXPOSED"]
df.to_csv("Bazaar\\TW\\CSV\\Files\\Output\\2WheelerOutputFull.csv")

# make_pivots(df, "Accident_Year_new")

# make_pivots(df, "Zone")
# make_pivots(df, "Insurer")
# make_pivots(df, "plan_category")
# # make_pivots(df, "Accident_Year")
# make_pivots(df, "body_type")
# make_pivots(df, "ccnew")
# make_pivots(df, "Make")
