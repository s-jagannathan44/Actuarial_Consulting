import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import GammaRegressor


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
    return gamma_glm


def execute_model(gamma_model, dataframe):
    y_pred = gamma_model.predict(dataframe)
    dataframe["Output"] = y_pred
    dataframe.to_csv("Output\\df_test.csv")


df = pd.read_csv("Output\\Injury_NewApproach.csv")
for col in df.columns:
    if "Unnamed" in col:
        df.drop(col, axis=1, inplace=True)
df_train = df
df_test = df

glm = build_model()
execute_model(glm, df_test)

# Major_States = ["Tamil Nadu", "Madhya Pradesh", "Kerala", "Karnataka", "Rajasthan", "Odisha", "West Bengal",
#                 "Maharashtra", "Chattisgarh", "Telangana", "Uttar Pradesh", "Gujarat", "Andhra Pradesh",
#                 "Bihar", "Haryana", "Delhi"]
# list_states = df["Registration States"].unique()
# OtherStates = []

# for State in list_states:
#     if Major_States.count(State) == 0:
#         OtherStates.append(State)
# for State in OtherStates:
#     for index in range(len(df)):
#         if index < len(df):
#             if df["Registration States"].iloc[index] == State:
#                 df["Registration States"].iloc[index] = df["Zone"].iloc[index]
# df.to_csv("Output\\State.csv")
#
# df = pd.read_csv("Output\\Death.csv")
# index = 0
# for index in range(len(df)):
#     if index < len(df) - 1:
#         if df["UY_Newer"].iloc[index] != "2012-17":
#             df["UY_Newer"].iloc[index] = df["UY New"].iloc[index]
#
# df.to_csv("Output\\Death_Modified.csv")
#
