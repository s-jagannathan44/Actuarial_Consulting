import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import statsmodels.api as sm
from sklearn.base import BaseEstimator, RegressorMixin


class SMWrapper(BaseEstimator, RegressorMixin):
    """ A universal sklearn-style wrapper for statsmodels regressors """
    def __init__(self, model_class, fit_intercept=True):
        self.results_ = None
        self.model_ = None
        self.model_class = model_class
        self.fit_intercept = fit_intercept

    def fit(self, X, y):
        if self.fit_intercept:
            X = sm.add_constant(X)
        link = sm.families.links.log()
        self.model_ = sm.GLM(y, X, family=sm.families.Gamma(link))
        self.results_ = self.model_.fit()
        return self

    def predict(self, X):
        if self.fit_intercept:
            X = sm.add_constant(X)
        return self.results_.predict(X)

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
    poisson_glm = Pipeline(
        [
            ("preprocessor", linear_model_preprocessor),
            ("regressor", SMWrapper(sm.families.Gaussian)),
        ]
    )
    poisson_glm.fit(
        df_train, df_train["Gross Cost"])
    return poisson_glm


def execute_model(poisson_model, dataframe):
    y_pred = poisson_model.predict(dataframe)
    dataframe["Predicted"] = y_pred
    dataframe.to_csv("Output\\df_test.csv")


df = pd.read_csv("Output\\Injury.csv")
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

df_train = df
df_test = df
poisson = build_model()
# drop multiple columns from DataFrame
# df.drop(df.columns[[0, 1]], axis=1, inplace=True)
execute_model(poisson, df_test)
# poisson = joblib.load("Frequency.sav")
# execute_model(poisson, df)
