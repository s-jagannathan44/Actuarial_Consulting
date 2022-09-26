"""
============================
Gradient Boosting regression
============================

This example demonstrates Gradient Boosting to produce a predictive
model from an ensemble of weak predictive models. Gradient boosting can be used
for regression and classification problems. Here, we will train a model to
tackle a diabetes regression task. We will obtain the results from
:class:`~sklearn.ensemble.GradientBoostingRegressor` with least squares loss
and 500 regression trees of depth 4.

Note: For larger datasets (n_samples >= 10000), please refer to
:class:`~sklearn.ensemble.HistGradientBoostingRegressor`.

"""
import joblib
# Author: Peter  <peter.prettenhofer@gmail.com>
#         Maria  <https://github.com/maikia>
#         Katrina Ni <https://github.com/nilichen>
#
# License: BSD 3 clause

import matplotlib.pyplot as plt
import numpy as np
from sklearn import ensemble
from sklearn.compose import ColumnTransformer
import pandas as pd
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder


# %%
# Load the data
# -------------------------------------
#
# First we need to load the data.

def read_analyze_transform(filename):
    df_ = pd.read_csv(filename)
    for c in df_.drop('Claim', axis=1).columns:
        csv_file_name = "Output\\Columns\\" + c + ".csv"
        insight = df_[c].value_counts()
        insight.to_csv(csv_file_name)
    X_ = df_.drop('Claim', axis=1)
    y_ = df_["Claim"]
    transformer_ = ColumnTransformer(
        [("onehot_categorical", OneHotEncoder(), ["MaritalMainDriver", "DrivingRestriction", "Make"],),
         ("ordinal", OrdinalEncoder(), ["GenderMainDriver", "VehFuel1"],),
         ],
        remainder='drop'
    )
    X_ = transformer_.fit_transform(X_)
    return df_, X_, y_, transformer_


df, X, y, transformer = read_analyze_transform("Output\\Sev_2.csv")
# %%
# Data preprocessing
# -------------------------------------
#
# Next, we will split our dataset to use 90% for training and leave the rest
# for testing. We will also set the regression model parameters. You can play
# with these parameters to see how the results change.
#
# `n_estimators` : the number of boosting stages that will be performed.
# Later, we will plot deviance against boosting iterations.
#
# `max_depth` : limits the number of nodes in the tree.
# The best value depends on the interaction of the input variables.
#
# `min_samples_split` : the minimum number of samples required to split an
# internal node.
#
# `learning_rate` : how much the contribution of each tree will shrink.
#
# `loss` : loss function to optimize. The least squares function is  used in
# this case however, there are many other options (see
# :class:`~sklearn.ensemble.GradientBoostingRegressor` ).

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=40)
params = {
    "n_estimators": 500,
    "max_depth": 4,
    "min_samples_split": 5,
    "learning_rate": 0.01,
    "loss": "absolute_error",
}

# %%
# Fit regression model
# --------------------
#
# Now we will initiate the gradient boosting regressors and fit it with our
# training data. Let's also look and the mean squared error on the test data.

# reg = ensemble.GradientBoostingRegressor(**params)
# reg.fit(X_train, y_train)
# joblib.dump(reg, "SeverityBoostedTree.sav")
reg = joblib.load("SeverityBoostedTree.sav")
y_pred = reg.predict(X)
np.savetxt("Output\\y_pred.csv", y_pred, delimiter=",")
mse = mean_absolute_error(y, y_pred)
print("The mean absolute  error (MAE) on test set: {:.4f}".format(mse))

# %%
# Plot training deviance
# ----------------------
#
# Finally, we will visualize the results. To do that we will first compute the
# test set deviance and then plot it against boosting iterations.

test_score = np.zeros((params["n_estimators"],), dtype=np.float64)
for i, y_pred in enumerate(reg.staged_predict(X_test)):
    test_score[i] = reg.loss_(y_test, y_pred)

fig = plt.figure(figsize=(6, 6))
plt.subplot(1, 1, 1)
plt.title("Deviance")
plt.plot(
    np.arange(params["n_estimators"]) + 1,
    reg.train_score_,
    "b-",
    label="Training Set Deviance",
)
plt.plot(
    np.arange(params["n_estimators"]) + 1, test_score, "r-", label="Test Set Deviance"
)
plt.legend(loc="upper right")
plt.xlabel("Boosting Iterations")
plt.ylabel("Deviance")
fig.tight_layout()
plt.show()
