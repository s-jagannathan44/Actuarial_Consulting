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
    # df2["Error"] = df2["Error"].abs()
    df2['%ageError'] = df2['Error'].map('{:.2%}'.format)
    df2.to_csv("Bazaar\\Output\\" + columns + ".csv")


def build_model():
    df_ = pd.read_csv("Bazaar\\Output\\4WheelerFiles.csv")
    df_["Loss_Cost"] = df_["PAID_AMT"] / df_["LIVES_EXPOSED"]
    result = smf.glm(
        formula='Loss_Cost ~ Accident_Year_new + cc_new + Zone_new + Insurer_new + makename_new + fuel_new +'
                'plancategory_new + roundage_new',
        data=df_, family=Tweedie(var_power=1.9), var_weights=df_["LIVES_EXPOSED"]).fit()
    joblib.dump(result, "Bazaar\\Output\\4Wheeleer.sav")
    return df_


df =   pd.read_csv("Bazaar\\Output\\4WheelerPPT2024File.csv")  # build_model()  #
result2 = joblib.load("Bazaar\\Output\\4Wheeleer.sav")
print("-----------Summary-----------")
print(result2.summary2())
print("-----------GLM simple form relativity-----------")
print(np.exp(result2.params))
print("-----------predict-----------")
y_pred = result2.predict(df)
df["Pred"] = y_pred
df["Pred_Cost"] = df["Pred"] * df["LIVES_EXPOSED"]
df.to_csv("Bazaar\\Output\\new_4wheeler2024.csv")
# make_pivots(df, "Accident_Year_new")
# make_pivots(df, "Zone_new")4
# make_pivots(df, "cc_new")
# make_pivots(df, "Insurer_new")
# make_pivots(df, "makename_new")

# make_multi(df, "Accident_Year_new Zone_new cc_new Insurer_new makename_new ".split())

# make_pivots(df, "Accident_Year")
# make_pivots(df, "Zone_1")
# make_pivots(df, "cubiccapacity_New")
# make_pivots(df, "Insurer")
# make_pivots(df, "makename")
# make_pivots(df, "newplancategory")
# make_pivots(df, "fuel")
# make_pivots(df, "roundage")
