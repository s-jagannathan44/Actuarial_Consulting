import numpy as np
import pandas as pd
import joblib
from sklearn.linear_model import GammaRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline, make_pipeline


def build_model():
    global df_train, df_test

    interaction = make_pipeline(
        OneHotEncoder(),
        PolynomialFeatures(degree=3, interaction_only=True, include_bias=False)
    )

    column_trans = ColumnTransformer(
        [
            ('interaction', interaction, "Financial_Year Mem_Age_New Mem_Gender_New Product_Name_New Renewal_Count_New "
                                         "Zone_New Sum_Insured_New Revised_Individual_Floater_New".split()

             ),
        ],
    )

    print(df_test.shape, df_train.shape)
    gamma_glm = Pipeline(
        [
            ("transform", column_trans),
            ("regressor", GammaRegressor(alpha=1e-12, max_iter=5000)),
        ]
    )
    gamma_glm.fit(
        df_model, df_train["Severity"], regressor__sample_weight=df_train["claim_count"]
    )
    joblib.dump(gamma_glm, "Severity.sav")
    return gamma_glm


def make_multi(dataframe, columns):
    df2 = pd.pivot_table(dataframe, values="Aggregate Pred_Amount claim_count".split(), columns=columns,
                         aggfunc="sum").T
    df2["Actual"] = df2["Aggregate"] / df2["claim_count"]
    df2["Predicted"] = df2["Pred_Amount"] / df2["claim_count"]
    df2["Error"] = (df2["Actual"] - df2["Predicted"]) / df2["Actual"]
    df2['%ageError'] = df2['Error'].map('{:.2%}'.format)
    df2["Error"] = df2["Error"].abs()
    below_ten = df2[df2["Error"] <= 0.1]["claim_count"].sum()
    total = df2["claim_count"].sum()
    print('{:.2%}'.format(below_ten / total))
    df2.to_csv("SeverityOutput\\multi.csv")
    # 1 feature and constant
    p = 1 + 1
    aic_value = aic(df2["Actual"], df_test, df2["Predicted"], p)
    print('{:.2}'.format(aic_value))


def execute_model(gamma_model, dataframe):
    y_pred = gamma_model.predict(dataframe)
    dataframe["Pred"] = y_pred
    dataframe["Pred_Amount"] = dataframe["Pred"] * dataframe["claim_count"]
    make_multi(dataframe, "Mem_Age_New Mem_Gender_New Product_Name_New Renewal_Count_New Financial_Year "
                          "Revised_Individual_Floater_New"
                          " Zone_New Sum_Insured_New".split())


def make_pivots(dataframe, columns):
    df2 = pd.pivot_table(dataframe, values="claim_count  Aggregate".split(), columns=columns,
                         aggfunc="sum").T
    df2["Actual"] = df2["Aggregate"] / df2["claim_count"]
    # df2["Error"] = (df2["Actual"] - df2["Predicted"]) / df2["Actual"]
    # df2['Error'] = df2['Error'].map('{:.2%}'.format)
    df2.to_csv("SeverityOutput\\" + columns + ".csv")


def multiplier(year):
    if year == 5:
        return 1.07
    elif year == 4:
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


df = pd.read_csv("CSV\\ClaimsFile.csv")
df = df[df["Financial_Year"].isin([3, 4, 5])]
df = df[~ df["Product_Name_New"].isin("Star Hospital Cash Insurance Policy".split())]

df["Severity"] = df["Aggregate"] / df["claim_count"]
df = df[df["Severity"] > 0]
df_train, df_test = train_test_split(df, test_size=0.2, random_state=0)

df_train.to_csv("SeverityOutput\\Eighty.csv")
df_test.to_csv("SeverityOutput\\Twenty.csv")
df_model = df_train[['Mem_Age_New', "Mem_Gender_New", "Product_Name_New", "Renewal_Count_New",
                     "Revised_Individual_Floater_New", "Zone_New", "Sum_Insured_New", "Financial_Year"]]

model = build_model()


execute_model(model, df_test)


def othering(dataframe):
    make_pivots(dataframe, "Product_Name_New")
    make_pivots(dataframe, "Zone_New")
    make_pivots(dataframe, "Mem_Age_New")
    make_pivots(dataframe, "Renewal_Count_New")
    make_pivots(dataframe, "Channel_type_New")
    make_pivots(dataframe, "Sum_Insured_New")
    make_pivots(dataframe, "Revised_Individual_Floater_New")
    make_pivots(dataframe, "Financial_Year")


def find_separation():
    df_ = pd.read_csv("CSV\\ClaimsModelFile.csv")

    df_ = df_[df_["Financial_Year"].isin([3, 4])]
    othering(df_)
