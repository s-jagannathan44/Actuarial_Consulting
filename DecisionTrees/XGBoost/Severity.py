import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split, GridSearchCV
from Modules import Utilities as Ut
from xgboost import XGBRegressor

passthrough_list = ["AnalysisPeriod", "NumberOfDrivers", "VoluntaryExcess", "NumberOfPastClaims",
                    "NumberOfPastConvictions", "ClaimLastYr"]
ordinal_list = ["GenderMainDriver", "GenderYoungestDriver", "MaritalMainDriver",
                "Use", "PaymentMethod",  "BonusMalusProtection",
                "GenderYoungestAdditionalDriver", "VehFuel1"]
to_bin_list = [['AgeMainDriver', 4, 'uniform'], ['AgeYoungestDriver', 4, 'uniform'],
               ['AgeYoungestAdditionalDriver', 2, 'uniform'], ['VehicleAge', 2, 'uniform'],
               ['VehicleValue', 10, 'uniform'], ['VehicleMileage', 4, 'uniform'],
               ['BonusMalusYears', 4, 'quantile'], ['PolicyTenure', 3, 'quantile']]


def return_best_model(estimator):
    # get the mean baseline because this is a regression problem
    # with regression, the baseline can be as simple as the mean.
    mean_baseline = y_test.mean()
    y_pred_base = [mean_baseline] * len(y_test)

    mae_base = mean_absolute_error(y_test, y_pred_base)
    print(f'Mean Baseline: {mean_baseline:.1f} ')
    print(f'Baseline mean absolute error: {mae_base}')
    # print(f'r2 score: {r2_base}')
    # defining parameter range
    param_grid = {
        'max_depth': [2, 3, 4, 5, 6, 7, 8],
        'learning_rate': [0.1, 0.2, 0.3, 0.4, 0.5],
        'n_estimators': [100, 200, 300, 500],
        'early_stopping_rounds': [10],
        'eval_metric': ['mae']
    }
    param_dict = {'eval_set': [(X_val, y_val)], 'verbose': True}
    xgb_reg = GridSearchCV(estimator, param_grid, cv=5, refit=True, verbose=3, n_jobs=-1)
    xgb_reg.fit(X_train, y_train, **param_dict)
    # print best parameter after tuning
    print(xgb_reg.best_params_, xgb_reg.best_score_)
    return xgb_reg.best_estimator_


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


def predict(X_value, y_value, estimator):
    # We will predict the output  here
    y_pred_ = estimator.predict(X_value)
    print('Actual mean', y_value.mean())
    print('predicted mean', y_pred_.mean())
    mae_model = mean_absolute_error(y_value, y_pred_)
    print(f'Model mean absolute error: {mae_model}')
    return y_pred_


# -------------------- CODE STARTS HERE ---------------------------------------
ord_col_size = ohe_col_size = 0
sev = pd.read_csv('Output\\Severity.csv')

sev = sev[sev["Actual"] > 0]
X = sev.drop("Actual", axis=1)
y = sev["Actual"]

transformer = Ut.transform(passthrough_list, to_bin_list, ordinal_list)
X = transformer.fit_transform(X)

rgr = XGBRegressor(objective='reg:gamma', seed=42)

X_train, X_test_val, y_train, y_test_val = train_test_split(X, y, test_size=0.30, random_state=40)
X_test, X_val, y_test, y_val = train_test_split(X_test_val, y_test_val, test_size=0.33, random_state=40)

model = return_best_model(rgr)
# rgr.save_model('Output\\model.json')
# rgr.load_model('Output\\model.json')
y_pred = predict(X_test, y_test, model)
Output = pd.DataFrame(columns=['Actual_XGB', 'Predicted_XGB'])
Output["Actual_XGB"] = y_test
Output["Predicted_XGB"] = y_pred
Output.to_csv("Output\\Output.csv")
