import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder, KBinsDiscretizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import PoissonRegressor


# %%
# The remaining columns can be used to predict the Freq_Act of claim events.
# Those columns are very heterogeneous with a mix of categorical and numeric
# variables with different scales, possibly very unevenly distributed.
#
# In order to fit linear models with those predictors it is therefore
# necessary to perform standard feature transformations as follows:

def build_model():
    linear_model_preprocessor = ColumnTransformer(
        [
            ("passthrough_1", "passthrough", ["AnalysisPeriod"]),
            (
                "onehot_categorical",
                OrdinalEncoder(),
                ["GenderMainDriver", "GenderYoungestDriver",
                 "Use", "PaymentMethod", "BonusMalusProtection"],
            ),
            ("binned_2", KBinsDiscretizer(n_bins=4, encode='ordinal', strategy='quantile'), ["AgeMainDriver"]),
            ("binned_9", KBinsDiscretizer(n_bins=2, encode='ordinal', strategy='quantile'), ["VehicleAge"]),
            ("binned_15", KBinsDiscretizer(n_bins=4, encode='ordinal', strategy='quantile'), ["BonusMalusYears"]),
            ("binned_19", KBinsDiscretizer(n_bins=3, encode='ordinal', strategy='quantile'), ["PolicyTenure"]),
        ],
        remainder='drop'
    )
    poisson_glm = Pipeline(
        [
            ("preprocessor", linear_model_preprocessor),
            ("regressor", PoissonRegressor(alpha=1e-12, max_iter=300)),
        ]
    )
    poisson_glm.fit(
        df_train, df_train["Claim Count"])
    joblib.dump(poisson_glm, "Frequency.sav")
    return poisson_glm


def execute_model(poisson_model, dataframe):
    y_pred = poisson_model.predict(dataframe)
    np.savetxt("CSV\\output.csv", y_pred, delimiter=',')
    dataframe.to_csv("CSV\\df_test.csv")


df = pd.read_csv("CSV\\Frequency.csv")
for col in df.columns:
    if "Unnamed" in col:
        df.drop(col, axis=1, inplace=True)
print(df.shape)

# %%
# The number of claims (``ClaimNb``) is a positive integer that can be modeled
# as a Poisson distribution. It is then assumed to be the number of discrete
# events occurring with a constant rate in a given time interval (``Exposure``,
# in units of years).
#
# Here we want to model the Freq_Act ``y = ClaimNb / Exposure`` conditionally
# on ``X`` via a (scaled) Poisson distribution, and use ``Exposure`` as
# ``sample_weight``.

df_train, df_test = train_test_split(df, test_size=0.30, random_state=0)
poisson = build_model()
# drop multiple columns from DataFrame
# df.drop(df.columns[[0, 1]], axis=1, inplace=True)
execute_model(poisson, df_test)
# poisson = joblib.load("Frequency.sav")
# execute_model(poisson, df)
