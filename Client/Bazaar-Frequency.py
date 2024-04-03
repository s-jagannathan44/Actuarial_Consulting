import joblib
import numpy as np
import pandas as pd
from statsmodels.genmod.families import Poisson
import statsmodels.formula.api as smf


def build_model():
    df = pd.read_csv("Bazaar\\Output\\4WheeleerFrequencies.csv")
    df["Frequency"] = df["Claim_Count"] / df["LIVES_EXPOSED"]
    result = smf.glm(
        formula='Frequency ~  State_new + cubiccapacity_New + Insurer_new + plancategory_new + roundage_new  + make_model_new + fuel_new',
        data=df, family=Poisson(), var_weights=df["LIVES_EXPOSED"]).fit()
    joblib.dump(result, "Bazaar\\Output\\4Wheeleer.sav")
    return df


df = pd.read_csv("Bazaar\\Output\\OutofTime.csv")  # build_model()
result2 = joblib.load("Bazaar\\Output\\4Wheeleer.sav")
print("-----------Summary-----------")
print(result2.summary2())
print("-----------GLM simple form relativity-----------")
print(np.exp(result2.params))
print("-----------predict-----------")
y_pred = result2.predict(df)
df["Pred"] = y_pred
df["Pred_Count"] = df["Pred"] * df["LIVES_EXPOSED"]
df.to_csv("Bazaar\\Output\\new_4wheeler.csv")
