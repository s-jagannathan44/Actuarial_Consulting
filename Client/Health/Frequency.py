import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.linear_model import PoissonRegressor


def build_model():
    global df_train, df_test

    interaction = make_pipeline(
        OneHotEncoder(),
        PolynomialFeatures(degree=3, interaction_only=True, include_bias=False)
    )

    column_trans = ColumnTransformer(
        [
            ('interaction', interaction,
             "Mem_Age_New Mem_Gender_New Product_Name_New Renewal_Count_New Zone_New Sum_Insured_New "
             "Revised_Individual_Floater_New".split()),
        ],
    )

    print(df_test.shape, df_train.shape)
    poisson_glm = Pipeline(
        [
            ("transform", column_trans),
            ("regressor", PoissonRegressor(alpha=1e-12, max_iter=5000)),
        ]
    )
    poisson_glm.fit(
        df_model, df_train["Frequency"], regressor__sample_weight=df_train["LIVES_EXPOSED"]
    )
    joblib.dump(poisson_glm, "Poisson.sav")
    return poisson_glm


def make_pivots(dataframe, columns):
    df2 = pd.pivot_table(dataframe, values="Claim_Count  LIVES_EXPOSED".split(), columns=columns,
                         aggfunc="sum").T
    df2["Actual"] = df2["Claim_Count"] / df2["LIVES_EXPOSED"]
    # df2["Error"] = (df2["Actual"] - df2["Predicted"]) / df2["Actual"]
    # df2['Error'] = df2['Error'].map('{:.2%}'.format)
    df2.to_csv("Output\\" + columns + ".csv")


def make_multi(dataframe, columns):
    df2 = pd.pivot_table(dataframe, values="Claim_Count Pred_Count LIVES_EXPOSED".split(), columns=columns,
                         aggfunc="sum").T
    df2["Actual"] = df2["Claim_Count"] / df2["LIVES_EXPOSED"]
    df2["Predicted"] = df2["Pred_Count"] / df2["LIVES_EXPOSED"]
    df2["Error"] = (df2["Actual"] - df2["Predicted"]) / df2["Actual"]
    df2['%ageError'] = df2['Error'].map('{:.2%}'.format)
    df2["Error"] = df2["Error"].abs()
    below_ten = df2[df2["Error"] <= 0.1]["LIVES_EXPOSED"].sum()
    total = df2["LIVES_EXPOSED"].sum()
    print('{:.2%}'.format(below_ten / total))
    df2.to_csv("Output\\multi.csv")
    # 1 feature and constant
    p = 1 + 1
    aic_value = aic(df2["Actual"], df_test, df2["Predicted"], p)
    print('{:.2%}'.format(aic_value))


def execute_model(poisson_model, dataframe):
    y_pred = poisson_model.predict(dataframe)
    dataframe["Pred"] = y_pred
    dataframe["Pred_Count"] = dataframe["Pred"] * dataframe["LIVES_EXPOSED"]
    make_multi(dataframe, "Mem_Age_New Mem_Gender_New Product_Name_New Renewal_Count_New Revised_Individual_Floater_New"
                          " Zone_New Sum_Insured_New".split())


def multiplier(year):
    if year == "FY23":
        return 1.07
    elif year == "FY22":
        return 1.016
    else:
        return 1.0


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


df = pd.read_csv("CSV\\FrequencyModelFile.csv", usecols="Mem_Age_New Mem_Gender_New LIVES_EXPOSED "
                                                        "Claim_Count Financial_Year Renewal_Count_New Zone_New "
                                                        "Revised_Individual_Floater_New Product_Name_New "
                                                        "Channel_type_New Sum_Insured_New "
                 .split())
for col in df.columns:
    if "Unnamed" in col:
        df.drop(col, axis=1, inplace=True)

df = df[df["LIVES_EXPOSED"] >= 1]
df = df[~ df["Product_Name_New"].isin("SURPLUS-FLOATER "
                                      "SURPLUS-INDI Micro Insurance Individual".split())]

df = df[df["Financial_Year"].isin([0, 1, 2])]
df["Frequency"] = df["Claim_Count"] / df["LIVES_EXPOSED"]
df = df[df["Frequency"] <= 1]
df["Frequency"].fillna(0, inplace=True)
df["Mem_Age_New"].fillna("0.0", inplace=True)

df_train, df_test = train_test_split(df, test_size=0.2, random_state=0)
df_model = df_train[['Mem_Age_New', "Mem_Gender_New", "Product_Name_New", "Renewal_Count_New",
                     "Revised_Individual_Floater_New", "Zone_New", "Sum_Insured_New"]]

glm = build_model()
execute_model(glm, df_test)

def othering(dataframe):
    make_pivots(dataframe, "Product_Name_New")
    make_pivots(dataframe, "Zone_New")
    make_pivots(dataframe, "Mem_Age_New")
    make_pivots(dataframe, "Renewal_Count_New")
    make_pivots(dataframe, "Channel_type_New")
    make_pivots(dataframe, "Sum_Insured_New")
    make_pivots(dataframe, "Revised_Individual_Floater_New")


def find_separation():
    df_ = pd.read_csv("CSV\\FrequencyModelFile.csv")

    df_ = df_[df_["Financial_Year"].isin([0, 1, 2])]
    othering(df_)

find_separation()

