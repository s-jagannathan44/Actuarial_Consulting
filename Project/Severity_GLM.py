import numpy as np
import pandas as pd
import joblib
from sklearn.linear_model import GammaRegressor
from sklearn.model_selection import train_test_split
from Modules import Utilities as Ut
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


def build_model():
    linear_model_preprocessor = ColumnTransformer(
        [
            ("passthrough_17", "passthrough", ["NumberOfPastClaims"]),
            ("passthrough_18", "passthrough", ["NumberOfPastConvictions"]),
            ("passthrough_24", "passthrough", ["ClaimLastYr"]),
            ("binned_2", KBinsDiscretizer(n_bins=4, encode='ordinal', strategy='quantile'), ["AgeMainDriver"]),
            ("binned_3", KBinsDiscretizer(n_bins=4, encode='ordinal', strategy='quantile'), ["AgeYoungestDriver"]),
            ("binned_4", KBinsDiscretizer(n_bins=2, encode='ordinal', strategy='quantile'),
             ["AgeYoungestAdditionalDriver"]),
            ("binned_9", KBinsDiscretizer(n_bins=2, encode='ordinal', strategy='quantile'), ["VehicleAge"]),
            ("binned_11", KBinsDiscretizer(n_bins=10, encode='ordinal', strategy='quantile'), ["VehicleValue"]),
            ("binned_13", KBinsDiscretizer(n_bins=4, encode='ordinal', strategy='quantile'), ["VehicleMileage"]),
            ("binned_15", KBinsDiscretizer(n_bins=4, encode='ordinal', strategy='quantile'), ["BonusMalusYears"]),
            ("binned_19", KBinsDiscretizer(n_bins=3, encode='ordinal', strategy='quantile'), ["PolicyTenure"]),
            ("onehot_categorical", OneHotEncoder(),
             ["MaritalMainDriver", "Make", "Use", "PaymentMethod", "PaymentFrequency"],),
            ("ordinal", OrdinalEncoder(),
             ["GenderMainDriver", "GenderYoungestDriver", "BonusMalusProtection",
              "GenderYoungestAdditionalDriver", "VehFuel1"],
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
    gamma_glm.fit(df_train, df_train["Sev_Act"])
    joblib.dump(gamma_glm, "Output\\SeverityModel.sav")
    return gamma_glm


def execute_model(gamma_model, dataframe):
    y_pred = gamma_model.predict(dataframe)
    np.savetxt("Output\\output.csv", y_pred, delimiter=',')
    dataframe.to_csv("Output\\df_test.csv")


df = pd.read_csv("Output\\Policies.csv")
df = Ut.impute_missing_values(df, "AgeYoungestAdditionalDriver")
df = Ut.impute_missing_values(df, "GenderYoungestAdditionalDriver")

df.set_index("PolicyReference", inplace=True, drop=True)
#  Note: filter out claims with zero amount, as the severity model
# requires strictly positive target values.
df.loc[(df["Claim"] == 0) & (df["Claim Count"] >= 1), "Claim Count"] = 0
# Note: filter out policies with zero claims
df = df[df["Claim Count"] >= 1]
df["Sev_Act"] = df["Claim"]
df.dropna(how="all", axis=1)
df_train, df_test = train_test_split(df, test_size=0.20, random_state=0)
model = build_model()
execute_model(model, df_test)
