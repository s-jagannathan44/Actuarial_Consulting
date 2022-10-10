import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from Modules import Utilities as Ut
from xgboost import XGBRegressor

passthrough_list = ["AnalysisPeriod", "NumberOfDrivers", "VoluntaryExcess", "NumberOfPastClaims",
                    "NumberOfPastConvictions", "ClaimLastYr"]
ordinal_list = ["GenderMainDriver", "GenderYoungestDriver", "MaritalMainDriver",
                "Make", "Use", "PaymentMethod", "PaymentFrequency", "BonusMalusProtection",
                "GenderYoungestAdditionalDriver", "VehFuel1"]
to_bin_list = [['AgeMainDriver', 4, 'uniform'], ['AgeYoungestDriver', 4, 'uniform'],
               ['AgeYoungestAdditionalDriver', 2, 'uniform'], ['VehicleAge', 2, 'uniform'],
               ['VehicleValue', 10, 'uniform'], ['VehicleMileage', 4, 'uniform'],
               ['BonusMalusYears', 4, 'quantile'], ['PolicyTenure', 3, 'quantile']]


def get_columns():
    global ord_col_size, ohe_col_size
    encoder = transformer.named_transformers_['onehot_categorical']
    columns = encoder.get_feature_names_out()
    ohe_col_size = columns.size
    encoder = transformer.named_transformers_['ordinal']
    ord_columns = encoder.get_feature_names_out()
    columns = np.append(columns, ord_columns)
    ord_col_size = ord_columns.size
    return columns


def predict(X_val, y_val, estimator):
    # We will predict the output  here
    y_pred_ = estimator.predict(X_val)
    print('Actual mean', y_val.mean())
    print('predicted mean', y_pred_.mean())
    mae_model = mean_absolute_error(y_val, y_pred_)
    print(f'Model mean absolute error: {mae_model}')
    return y_pred_


# -------------------- CODE STARTS HERE ---------------------------------------
ord_col_size = ohe_col_size = 0
sev = pd.read_csv('Output\\Policies.csv')

sev = sev[sev["Claim"] > 0]
X = sev.drop("Claim", axis=1)
y = sev["Claim"]

X = Ut.impute_missing_values(X, "AgeYoungestAdditionalDriver")
X = Ut.impute_missing_values(X, "GenderYoungestAdditionalDriver")

transformer = Ut.transform(passthrough_list, to_bin_list, ordinal_list)
X = transformer.fit_transform(X)


rgr = XGBRegressor(objective='reg:gamma', seed=42, eval_metric='mae', max_depth=5,
                   learning_rate=0.1, n_estimators=300)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=40)
# rgr.fit(X_train, y_train)
# rgr.save_model('Output\\model.json')
rgr.load_model('Output\\model.json')
y_pred = predict(X, y, rgr)
np.savetxt("Output\\y_pred.csv", y_pred, delimiter=",")
