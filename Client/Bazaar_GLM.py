import joblib
import numpy as np
import pandas as pd
from statsmodels.genmod.families import Tweedie
import statsmodels.formula.api as smf


def build_model():
    df.rename(columns={"Policy number": "Policy_number"}, inplace=True)
    result = smf.glm(
        formula='Loss_Cost ~ Zone_1 + cubiccapacity_New + Insurer_new + plancategory_new + roundage_new  + makename_new + fuel_new',
        data=df, family=Tweedie(var_power=1.9), var_weights=df["LIVES_EXPOSED"]).fit()
    joblib.dump(result, "Bazaar\\Output\\4Wheeleer.sav")
    return result


df = pd.read_csv("Bazaar\\Output\\4WheelerTestFile.csv")
df["Loss_Cost"] = df["PAID_AMT"] / df["LIVES_EXPOSED"]
result2 = joblib.load("Bazaar\\Output\\4Wheeleer.sav")
print("-----------Summary-----------")
print(result2.summary2())
print("-----------GLM simple form relativity-----------")
print(np.exp(result2.params))
print("-----------predict-----------")
y_pred = result2.predict(df)
df["Pred"] = y_pred
df["Pred_Cost"] = df["Pred"] * df["LIVES_EXPOSED"]
df.to_csv("Bazaar\\Output\\text_out.csv")
