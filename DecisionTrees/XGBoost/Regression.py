import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder
from xgboost import XGBRegressor

df = pd.read_csv("Output\\Sev_3.csv")
X = df.drop('Claim', axis=1)
y = df["Claim"]
transformer_ = ColumnTransformer(
    [
        ("ordinal", OrdinalEncoder(), ["GenderMainDriver", "VehFuel1"]),
        ("onehot_categorical", OneHotEncoder(), ["MaritalMainDriver", "DrivingRestriction", "Make"],),
    ],
    remainder='drop'
)

X = transformer_.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=40)
X_train = X_train.toarray()

rgr = XGBRegressor(objective='reg:gamma', seed=42, eval_metric='mae', max_depth=5,
                   learning_rate=0.1, n_estimators=300)
rgr.fit(X_train, y_train)
y_pred = rgr.predict(X_test)
np.savetxt("Output\\y_pred.csv", y_pred, delimiter=",")
np.savetxt("Output\\y_test.csv", y_test, delimiter=",")
print(mean_absolute_error(y_test, y_pred))
