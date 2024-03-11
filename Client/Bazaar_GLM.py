import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from statsmodels.genmod.families import Tweedie
import statsmodels.formula.api as smf


def llf_(y, x, pr):
    # return maximized log likelihood
    nobs = float(x.shape[0])
    nobs2 = nobs / 2.0
    nobs = float(nobs)
    resid = y - pr
    ssr = np.sum(resid ** 2)
    llf = -nobs2 * np.log(2 * np.pi) - nobs2 * np.log(ssr / nobs) - nobs2
    return llf


def aic(y, X_, pr, p):
    # return aic metric
    llf = llf_(y, X_, pr)
    return -2 * llf + 2 * p


def make_multi(dataframe, columns):
    df2 = pd.pivot_table(dataframe, values="PAID_AMT Pred_Cost LIVES_EXPOSED".split(), columns=columns,
                         aggfunc="sum").T
    df2["Actual"] = df2["PAID_AMT"] / df2["LIVES_EXPOSED"]
    df2["Predicted"] = df2["Pred_Cost"] / df2["LIVES_EXPOSED"]
    df2["Error"] = (df2["Actual"] - df2["Predicted"]) / df2["Actual"]
    df2['%ageError'] = df2['Error'].map('{:.2%}'.format)
    df2["Error"] = df2["Error"].abs()
    below_ten = df2[df2["Error"] <= 0.1]["LIVES_EXPOSED"].sum()
    total = df2["LIVES_EXPOSED"].sum()
    print('{:.2%}'.format(below_ten / total))
    df2.to_csv("Bazaar\\Output\\text_out.csv")
    # 1 feature and constant
    p = 1 + 1
    aic_value = aic(df2["Actual"], test, df2["Predicted"], p)
    print(round(aic_value, 2))


df = pd.read_csv("Bazaar\\Output\\4WheeleerFile.csv")
df["Loss_Cost"] = df["PAID_AMT"] / df["LIVES_EXPOSED"]
train, test = train_test_split(df, test_size=0.2, random_state=25)

result = smf.glm(formula="Loss_Cost ~ Zone_1 + cubiccapacity_New + Insurer_new + plancategory_new + roundage_new "
                         "+ makename_new + fuel_new",
                 data=train, family=Tweedie(var_power=1.9), var_weights=train["LIVES_EXPOSED"]).fit()

print("-----------Summary-----------")
print(result.summary2())

print("-----------predict-----------")
y_pred = result.predict(test)
test["Pred"] = y_pred
test["Pred_Cost"] = test["Pred"] * test["LIVES_EXPOSED"]
make_multi(test, "Zone_1 cubiccapacity_New Insurer_new plancategory_new  roundage_new "
                 "makename_new fuel_new".split())
# test.to_csv("Bazaar\\Output\\text_out.csv")
