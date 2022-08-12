import numpy as np
import pandas as pd
import joblib
from sklearn.linear_model import GammaRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder
from sklearn.preprocessing import StandardScaler, KBinsDiscretizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


def build_model():
    linear_model_preprocessor = ColumnTransformer(
        [
            ("binned_numeric", KBinsDiscretizer(n_bins=10), ["VehicleValue"]),
            ("passthrough_numeric", "passthrough", ["Claim Count"]),
            (
                "onehot_categorical",
                OneHotEncoder(),
                ["GenderMainDriver", "MaritalMainDriver", "Make", "Use", "PaymentMethod", "PaymentFrequency"],
            ),
        ],
        remainder='drop'
        # remainder ='passthrough'
    )
    gamma_glm = Pipeline(
        [
            ("preprocessor", linear_model_preprocessor),
            ("regressor", GammaRegressor(alpha=1e-12, max_iter=300)),
        ]
    )
    gamma_glm.fit(df_train, df_train["Sev_Act"], regressor__sample_weight=df_train["Claim Count"])
    joblib.dump(gamma_glm, "SeverityModel.sav")
    return gamma_glm


def execute_model(gamma_model, dataframe):
    y_pred = gamma_model.predict(dataframe)
    np.savetxt("output.csv", y_pred, delimiter=',')
    dataframe.to_csv("df_test.csv")


df = pd.read_csv("Policies.csv")
df.set_index("PolicyReference", inplace=True, drop=True)
#  Note: filter out claims with zero amount, as the severity model
# requires strictly positive target values.
df.loc[(df["Claim"] == 0) & (df["Claim Count"] >= 1), "Claim Count"] = 0
# Note: filter out policies with zero claims
df = df[df["Claim Count"] >= 1]

# Correct for unreasonable observations (that might be data error)
# and a few exceptionally large claim amounts
'''
df["Claim Count"] = df["Claim Count"].clip(upper=4)
df["Exposure"] = df["Exposure"].clip(upper=1)
df["ClaimA"] = df["Claim"].clip(upper=200000)
'''
df["Sev_Act"] = df["Claim"] / df["Claim Count"]
df.dropna(how="all", axis=1)
df_train, df_test = train_test_split(df, test_size=0.33, random_state=0)
model = joblib.load("SeverityModel.sav")
execute_model(model,df)
# model = build_model()
# execute_model(model, df_test)
