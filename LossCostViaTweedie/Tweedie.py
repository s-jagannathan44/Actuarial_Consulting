# import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import TweedieRegressor


def build_model():
    global df_train, df_test
    linear_model_preprocessor = ColumnTransformer(
        [
            ("binned_numeric", KBinsDiscretizer(n_bins=10), ["VehicleValue"]),
            ("passthrough_numeric", "passthrough", ["Exposure"]),
            (
                "onehot_categorical",
                OneHotEncoder(),
                ["GenderMainDriver", "MaritalMainDriver", "Make", "Use", "PaymentMethod", "PaymentFrequency"],
            ),
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
        df_train, df_train["Loss_Cost"], regressor__sample_weight=df_train["Exposure"]
    )
    #  joblib.dump(tweedie_glm, "Tweedie.sav")
    return tweedie_glm


def execute_model(tweedie_model, dataframe):
    y_pred = tweedie_model.predict(dataframe)
    np.savetxt("Output\\output.csv", y_pred, delimiter=',')
    dataframe.to_csv("Output\\df_test.csv")


df = pd.read_csv("Output\\Policies.csv")
for col in df.columns:
    if "Unnamed" in col:
        df.drop(col, axis=1, inplace=True)

df.set_index("PolicyReference", inplace=True, drop=True)
df["Loss_Cost"] = df["Claim"]
df_train, df_test = train_test_split(df, test_size=0.33, random_state=0)
glm = build_model()
execute_model(glm, df_test)
