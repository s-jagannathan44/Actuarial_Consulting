import pandas as pd
# from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
# from sklearn.preprocessing import KBinsDiscretizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
# from sklearn.linear_model import TweedieRegressor
from sklearn.linear_model import GammaRegressor


def build_model():
    global df_train, df_test
    linear_model_preprocessor = ColumnTransformer(
        [
            # ("binned_numeric", KBinsDiscretizer(n_bins=3, strategy='uniform'), ["V AGE BAND"]),
            ("passthrough_numeric", "passthrough", ["CC_desc"]),
            ("passthrough_numeric1", "passthrough", ["Body Type"]),
            (
                "onehot_categorical",
                OneHotEncoder(),
                ["LT_ANNUAL Flag", "UY_Newer", "Vehicle Make"]
            ),
        ],
        remainder='drop'
    )
    print(df_test.shape, df_train.shape)
    tweedie_glm = Pipeline(
        [
            ("preprocessor", linear_model_preprocessor),
            # ("regressor", TweedieRegressor(power=1.9, alpha=1e-12, max_iter=300)),
            ("regressor", GammaRegressor(alpha=1e-12, max_iter=300)),
        ]
    )
    tweedie_glm.fit(
        df_train, df_train["Gross Cost"])
    return tweedie_glm


def execute_model(tweedie_model, dataframe):
    y_pred = tweedie_model.predict(dataframe)
    dataframe["Output"] = y_pred
    dataframe.to_csv("Output\\df_test.csv")


df = pd.read_csv("Output\\Injury.csv")

for col in df.columns:
    if "Unnamed" in col:
        df.drop(col, axis=1, inplace=True)
df_train = df
df_test = df
# df_train, df_test = train_test_split(df, test_size=0.33, random_state=0)
glm = build_model()
execute_model(glm, df_test)

# index = 0
# for index in range(len(df)):
#     if index < len(df) - 1:
#         if df["UY_Newer"].iloc[index] != "2012-17":
#             df["UY_Newer"].iloc[index] = df["UY New"].iloc[index]
#
# df.to_csv("Output.csv")
#
