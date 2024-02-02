import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import TweedieRegressor


def build_model():
    global df_train, df_test
    linear_model_preprocessor = ColumnTransformer(
        [
            (
                "onehot_categorical",
                OneHotEncoder(),
                ["Mem_Age_New", "Mem_Gender_New", "Zone", "Renewal_Count_New", "Sum_Insured_New",
                 "Channel_type_New", "Product_Name_New", "Revised_Individual_Floater_New"],
            ),
            ('ordinal_categorical', OrdinalEncoder(), ["Financial_Year"])

        ],
        remainder='drop'
        # remainder ='passthrough'
    )
    print(df_test.shape, df_train.shape)
    tweedie_glm = Pipeline(
        [
            ("preprocessor", linear_model_preprocessor),
            ("regressor", TweedieRegressor(power=1.9, alpha=1e-12, max_iter=300)),
        ]
    )
    tweedie_glm.fit(
        df_train, df_train["Loss_Cost"], regressor__sample_weight=df_train["LIVES_EXPOSED"]
    )
    joblib.dump(tweedie_glm, "Tweedie.sav")
    return tweedie_glm


def pivot_age(dataframe):
    df2 = pd.pivot_table(dataframe, values="Loss_Cost Pred LIVES_EXPOSED".split(), columns="Mem_Age_New", aggfunc="sum")
    df2 = df2.transpose()
    df2["Actual_Total"] = df2["Loss_Cost"].sum()
    df2["Predicted_Total"] = df2["Pred"].sum()
    df["Error"] = (df2["Loss_Cost"] - df2['Pred']) / df2["Loss_Cost"]
    df2.to_csv("Output\\Age.csv")


def pivot_gender(dataframe):
    df2 = pd.pivot_table(dataframe, values="Loss_Cost Pred LIVES_EXPOSED".split(), columns="Mem_Gender_New",
                         aggfunc="sum")
    df2 = df2.transpose()
    df2["Actual_Total"] = df2["Loss_Cost"].sum()
    df2["Predicted_Total"] = df2["Pred"].sum()
    df["Error"] = (df2["Loss_Cost"] - df2['Pred']) / df2["Loss_Cost"]
    df2.to_csv("Output\\Gender.csv")


def pivot_renewal_count(dataframe):
    df2 = pd.pivot_table(dataframe, values="Loss_Cost Pred LIVES_EXPOSED".split(), columns="Renewal_Count_New",
                         aggfunc="sum")
    df2 = df2.transpose()
    df2["Actual_Total"] = df2["Loss_Cost"].sum()
    df2["Predicted_Total"] = df2["Pred"].sum()
    df["Error"] = (df2["Loss_Cost"] - df2['Pred']) / df2["Loss_Cost"]
    df2.to_csv("Output\\RC.csv")


def execute_model(tweedie_model, dataframe):
    dataframe.to_csv("Output\\text.csv")
    y_pred = tweedie_model.predict(dataframe)
    dataframe["Pred"] = y_pred
    dataframe.to_csv("Output\\text_out.csv")
    pivot_age(dataframe)
    pivot_gender(dataframe)
    pivot_renewal_count(dataframe)


df = pd.read_csv("OOS.csv")
df = df[df['LIVES_EXPOSED'] >= 1]
# df["LIVES_EXPOSED"].fillna(0, inplace=True)
for col in df.columns:
    if "Unnamed" in col:
        df.drop(col, axis=1, inplace=True)

df["Loss_Cost"] = df["PAID_AMT"] / df["LIVES_EXPOSED"]
df["Loss_Cost"].fillna(0, inplace=True)
df_train, df_test = train_test_split(df, test_size=0.2, random_state=0)
glm = build_model()
execute_model(glm, df_test)
