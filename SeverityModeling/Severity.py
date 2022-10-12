import numpy as np
import pandas as pd
import joblib
from sklearn.linear_model import GammaRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


def build_model():
    linear_model_preprocessor = ColumnTransformer(
        [
            ("onehot_categorical", OneHotEncoder(),
             ["Segment 1", "Make", "Product Type 1",  "RTO State - RTO State"],),
            ("ordinal", OrdinalEncoder(),
             ["TP Pool / Non TP Pool", "FY", "Loss Type"],
             ),
        ],
        remainder='drop'
    )

    gamma_glm = Pipeline(
        [
            ("preprocessor", linear_model_preprocessor),
            ("regressor", GammaRegressor(alpha=1e-12, max_iter=300)),
        ]
    )
    gamma_glm.fit(df_train, df_train["Actual"], regressor__sample_weight=df_train["Exposure"])
    joblib.dump(gamma_glm, "SeverityModel.sav")
    return gamma_glm


def execute_model(gamma_model, dataframe):
    y_pred = gamma_model.predict(dataframe)
    np.savetxt("Output\\output.csv", y_pred, delimiter=',')
    dataframe.to_csv("Output\\df_test.csv")


df = pd.read_csv("Output\\Commercial - WeightedInput.csv")
df.dropna(how="all", axis=1)
df_train, df_test = train_test_split(df, test_size=0.25, random_state=0)
# model = joblib.load("SeverityModel.sav")
# execute_model(model, df)
model = build_model()
execute_model(model, df_test)
