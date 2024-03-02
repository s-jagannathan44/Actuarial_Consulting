import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import PoissonRegressor


def build_model():
    global df_train, df_test
    linear_model_preprocessor = ColumnTransformer(
        [
            (
                "onehot_categorical",
                OneHotEncoder(drop=["Male", "Married"]),
                ["GenderMainDriver", "MaritalMainDriver"],
            ),
        ],
        remainder='drop'
        # remainder ='passthrough'
    )
    print(df_test.shape, df_train.shape)
    tweedie_glm = Pipeline(
        [
            ("preprocessor", linear_model_preprocessor),
            ("regressor", PoissonRegressor(alpha=1e-12, max_iter=300)),
        ]
    )
    tweedie_glm.fit(
        df_train, df_train["Claim Count"], regressor__sample_weight=df_train["Exposure"]
    )
    joblib.dump(tweedie_glm, "Tweedie.sav")
    return tweedie_glm, linear_model_preprocessor


def execute_model(tweedie_model, dataframe):
    y_pred = tweedie_model.predict(dataframe)
    np.savetxt("Output\\output.csv", y_pred, delimiter=',')
    dataframe.to_csv("Output\\df_test.csv")


# df = pd.read_csv("Output\\Policies.csv", usecols=["GenderMainDriver", "MaritalMainDriver",
#                                                   "Claim Count", "Exposure"])
# for col in df.columns:
#     if "Unnamed" in col:
#         df.drop(col, axis=1, inplace=True)
# # df.head(1).to_csv("sample.csv")
# # df.set_index("PolicyReference", inplace=True, drop=True)
# # df["Loss_Cost"] = df["Claim"]
# df_train, df_test = train_test_split(df, test_size=0.33, random_state=0)
# glm, trans = build_model()
tweedie_mode = joblib.load("Tweedie.sav")
dataframe_ = pd.read_csv("sample.csv", usecols=["GenderMainDriver", "MaritalMainDriver"])
ct = tweedie_mode[0]
tf = ct.fit_transform(dataframe_)
cf = tweedie_mode[1].coef_
i = tweedie_mode[1].intercept_
mat = tf.dot(cf) + i
print(np.exp(mat))
print(tweedie_mode.predict(dataframe_))
