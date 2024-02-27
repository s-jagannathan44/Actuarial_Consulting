import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.linear_model import TweedieRegressor


def build_model(power, iter_):
    global df_train, df_test

    interaction = make_pipeline(
        OneHotEncoder(),
        PolynomialFeatures(degree=3, interaction_only=True, include_bias=False)
    )

    column_trans = ColumnTransformer(
        [
            ("passthrough1", "passthrough", ["Financial_Year"]),
            ('interaction', interaction,
             "Mem_Age_New Mem_Gender_New Revised_Product_Name_New Renewal_Count_New Zone_New Sum_Insured_New "
             .split()),
        ],
    )

    print(df_test.shape, df_train.shape)
    tweedie_glm = Pipeline(
        [
            ("transform", column_trans),
            ("regressor", TweedieRegressor(power=power, alpha=1e-12, max_iter=iter_)),
        ]
    )
    tweedie_glm.fit(
        df_model, df_train["Loss_Cost"], regressor__sample_weight=df_train["LIVES_EXPOSED"]
    )
    joblib.dump(tweedie_glm, "Tweedie.sav")
    return tweedie_glm, column_trans


def make_pivots(dataframe, columns):
    df2 = pd.pivot_table(dataframe, values="PAID_AMT  LIVES_EXPOSED".split(), columns=columns,
                         aggfunc="sum").T
    df2["Actual"] = df2["PAID_AMT"] / df2["LIVES_EXPOSED"]
    df2.to_csv("Output\\" + columns + ".csv")


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
    df2.to_csv("Output\\multi.csv")
    # 1 feature and constant
    p = 1 + 1
    aic_value = aic(df2["Actual"], df_test, df2["Predicted"], p)
    print('{:.2%}'.format(aic_value))


def execute_model(tweedie_model, dataframe):
    y_pred = tweedie_model.predict(dataframe)
    dataframe["Pred"] = y_pred
    dataframe["Pred_Cost"] = dataframe["Pred"] * dataframe["LIVES_EXPOSED"]
    dataframe.to_csv("Output\\text_out.csv")
    make_multi(dataframe, "Mem_Age_New Mem_Gender_New Revised_Product_Name_New Renewal_Count_New  Financial_Year "
                          "Zone_New Sum_Insured_New".split())


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


df = pd.read_csv("CSV\\TweedieModelFile.csv", usecols="Mem_Age_New Mem_Gender_New LIVES_EXPOSED "
                                                      "PAID_AMT Financial_Year Renewal_Count_New Zone_New "
                                                      "Revised_Product_Name_New Channel_type_New Sum_Insured_New "
                 .split())
for col in df.columns:
    if "Unnamed" in col:
        df.drop(col, axis=1, inplace=True)

df = df[df["LIVES_EXPOSED"] >= 1]
df = df[~ df["Revised_Product_Name_New"].isin("SURPLUS-FLOATERFLOATER SURPLUS-FLOATERMED-PLT-046 "
                                              "SURPLUS-INDINDIVIDUAL Corona Kavach PolicyFLOATER "
                                              "Corona Kavach PolicyINDIVIDUAL"
                                              " Star Hospital Cash Insurance PolicyFLOATER ".split())]
df = df[df["Financial_Year"].isin([0, 1, 2, 4, 5])]
df["Loss_Cost"] = df["PAID_AMT"] / df["LIVES_EXPOSED"]
df["Loss_Cost"].fillna(0, inplace=True)
df["Mem_Age_New"].fillna("0.0", inplace=True)
df["Pred_Cost"] = df["Loss_Cost"]

df_train, df_test = train_test_split(df, test_size=0.2, random_state=0)
df_model = df_train[['Mem_Age_New', "Mem_Gender_New", "Revised_Product_Name_New", "Financial_Year", "Renewal_Count_New",
                     "Zone_New", "Sum_Insured_New"]]

powers = [1.7]
iterations = [5000]
for p_ in powers:
    for i in iterations:
        print(p_, i)
        glm, transformer = build_model(p_, i)
        execute_model(glm, df_test)


def othering(dataframe):
    make_pivots(dataframe, "Revised_Product_Name_New")
    make_pivots(dataframe, "Zone_New")
    make_pivots(dataframe, "Mem_Age_New")
    # make_pivots(dataframe, "Mem_Gender_New")
    make_pivots(dataframe, "Renewal_Count_New")
    # make_pivots(dataframe, "Channel_type_New")
    make_pivots(dataframe, "Sum_Insured_New")
    make_pivots(dataframe, "Financial_Year")


def find_separation():
    df_ = pd.read_csv("CSV\\TweedieModelFile.csv", usecols="Mem_Age_New Mem_Gender_New LIVES_EXPOSED "
                                                           "PAID_AMT Financial_Year Renewal_Count_New Zone_New "
                                                           "Revised_Product_Name_New Channel_type_New "
                                                           "Sum_Insured_New ".split())

    othering(df_)
