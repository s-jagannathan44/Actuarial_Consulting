import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import GammaRegressor
import joblib


def build_model():
    global df_train, df_test
    linear_model_preprocessor = ColumnTransformer(
        [
            ("binned_numeric", KBinsDiscretizer(n_bins=3, strategy='uniform'), ["V AGE NEW"]),
            (
                "onehot_categorical",
                OneHotEncoder(),
                ["LT_ANNUAL Flag", "UY New", "CC_Make", "Zone_State", "Body Type"]
            ),
        ],
        remainder='drop'
    )
    print(df_test.shape, df_train.shape)
    gamma_glm = Pipeline(
        [
            ("preprocessor", linear_model_preprocessor),
            # ("regressor", TweedieRegressor(power=1.9, alpha=1e-12, max_iter=300)),
            ("regressor", GammaRegressor(alpha=1e-12, max_iter=300)),
        ]
    )
    gamma_glm.fit(
        df_train, df_train["Gross Cost"])
    joblib.dump(gamma_glm, "GammaModel.sav")
    return gamma_glm


def execute_model(gamma_model, dataframe):
    y_pred = gamma_model.predict(dataframe)
    dataframe["Output"] = y_pred
    dataframe.to_csv("Output\\df_test.csv")


df = pd.read_csv("Output\\Injury_Final.csv")
for col in df.columns:
    if "Unnamed" in col:
        df.drop(col, axis=1, inplace=True)
df_train = df
df_test = df

# glm = build_model()
glm = joblib.load("Output\\GammaModel.sav")
execute_model(glm, df_test)


# UW Year Code
# df = pd.read_csv("Output\\Death.csv")
# index = 0
# for index in range(len(df)):
#     if index < len(df) - 1:
#         if df["UY_Newer"].iloc[index] != "2012-18":
#             df["UY_Newer"].iloc[index] = df["UY New"].iloc[index]
#
# df.to_csv("Output\\Death_Modified.csv")
#
