import numpy as np
import pandas as pd
# from matplotlib import pyplot as plt
from numpy import sort
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import GridSearchCV  # train_test_split
from Modules import Utilities as Ut
from xgboost import XGBRegressor

passthrough_list = ["Exposure"]
scaler_list = []
ordinal_list = ["LT_ANNUAL Flag", "CC_desc", "Body Type", "Vehicle Make", "V AGE BAND",
                "Registration States", "UY New", "Zone"]
# ordinal_list = ["LT_ANNUAL Flag", "UY New", "CC_Make", "Zone_State", "Body Type"]
# to_bin_list = [['V AGE NEW', 3, 'uniform']]
to_bin_list = []


def data_analysis():
    for c in sev.columns:
        csv_file_name = "Output\\Columns\\" + c.replace("/", "_") + ".csv"
        insight = sev[c].value_counts()
        insight.to_csv(csv_file_name)
    sev.describe(percentiles=[0.25, 0.5, 0.75, 0.85, 0.9, 0.98, 1]).to_csv("Output\\Columns\\desc.csv")


def select_features():
    thresholds = sort(rgr.feature_importances_)
    for thresh in thresholds:
        # select features using threshold
        selection = SelectFromModel(rgr, threshold=thresh, prefit=True)
        select_X_train = selection.transform(X_train)
        # train model
        selection_model = XGBRegressor(objective='reg:tweedie', seed=42, tweedie_variance_power=1.5,
                                       n_estimators=300, subsample=None)
        param_dict = {'sample_weight': exposure, 'verbose': True}
        selection_model.fit(select_X_train, y_train, **param_dict)
        # eval model
        select_X_test = selection.transform(X_test)
        predictions = selection_model.predict(select_X_test)
        print("Thresh=%.3f, n=%d, Accuracy: " % (thresh, select_X_train.shape[1]))
        predict_output(y_test, predictions)


def predict_output(actual_val, pred_val):
    actual = np.sum(actual_val)
    predicted = np.sum(pred_val)
    error = 1 - (predicted / actual)
    print("error", round(float(error) * 100, ndigits=2))


def get_columns():
    columns = {}
    for encoder in transformer.named_transformers_:
        if type(transformer.named_transformers_[encoder]) != str:
            item = [(encoder, transformer.named_transformers_[encoder].get_feature_names_out().size)]
            columns.update(item)
    return columns


def write_output(X_value, actual_val, pred_val):
    frame_list = []
    res = []
    length = 0
    index = 0
    for item in column_dict:
        encoder = transformer.named_transformers_[item]
        size = column_dict[item]
        length = length + size
        if length == size:
            col = encoder.inverse_transform(X_value[:, :length])
        else:
            col = encoder.inverse_transform(X_value[:, index:length])
        frame = pd.DataFrame(col, columns=encoder.get_feature_names_out())
        frame_list.append(frame)
        index = length

    for frame in frame_list:
        res.append(frame)

    # axis 0 is rows and axis 1 is columns
    frame = pd.concat(res, axis=1)
    frame["Actual"] = actual_val.to_list()
    frame['Predicted'] = pred_val
    frame["Exposure"] = test_exposure
    frame.to_csv("Output\\Output.csv")


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
        # 'learning_rate': [0.01, 0.05, 0.1, 0.2],
        # 'n_estimators': [100, 300, 500],
        #  'colsample_bytree': [0.8, 0.9, 1]
    }
    param_dict = {'eval_set': [(X_val, y_val)], 'verbose': True, 'sample_weight': exposure}
    xgb_reg = GridSearchCV(estimator, param_grid,
                           cv=5, refit=True, verbose=3, n_jobs=-1)
    xgb_reg.fit(X_train, y_train, **param_dict)
    # print best parameter after tuning
    print(xgb_reg.best_params_, xgb_reg.best_score_)
    return xgb_reg.best_estimator_


def predict(X_value, y_value, estimator):
    # We will predict the output  here
    y_pred_ = estimator.predict(X_value)
    print('Actual mean', y_value.mean())
    print('predicted mean', y_pred_.mean())
    mae_model = mean_absolute_error(y_value, y_pred_)
    print(f'Model mean absolute error: {mae_model}')
    return y_pred_


# -------------------- CODE STARTS HERE ---------------------------------------
# print(get_scorer_names())
sev = pd.read_csv('Output\\Injury_Correct.csv')
X = sev.drop("Loss Cost", axis=1)
y = sev["Loss Cost"]

transformer = Ut.transform(scaler_list, to_bin_list, ordinal_list, passthrough_list)
X = transformer.fit_transform(X)

# tweedie_variance_power=1.5, n_estimators=300, subsample=None
rgr = XGBRegressor(objective='reg:tweedie', seed=42, tweedie_variance_power=1.5, n_estimators=300, subsample=None)
# remove this line
X_train, X_test_val, y_train, y_test_val, X_val, y_val, exposure = X, X, X, X, X, X, X
X_test = X
y_test = y

# B----
# X_train, X_test_val, y_train, y_test_val = train_test_split(X, y, test_size=0.30, random_state=40)
# X_test, X_val, y_test, y_val = train_test_split(X_test_val, y_test_val, test_size=0.33, random_state=40)
# flat_arr = X_train[:, :1]
# exposure = np.reshape(flat_arr, np.shape(X_train)[0])
# X_train = X_train[:, 1:]
#  E---

test_exposure = np.reshape(X_test[:, :1], np.shape(X_test)[0])
X_test = X_test[:, 1:]

# B----
# X_val = X_val[:, 1:]
# params_dict = {'sample_weight': exposure, 'verbose': True}
# rgr.fit(X_train, y_train, **params_dict)
#  E---

# rgr.save_model('Output\\tweedie.json')
# rgr = return_best_model(rgr)
rgr.load_model('Output\\tweedie.json')
y_pred = predict(X_test, y_test, rgr)
column_dict = get_columns()
predict_output(y_test, y_pred)
write_output(X_test, y_test, y_pred)

# (pd.Series(rgr.feature_importances_, index=["LT_ANNUAL Flag", "CC_desc", "Body Type", "Vehicle Make", "V AGE BAND",
#                                             "Registration States", "UY New", "Zone", "Channel", "Cluster",
#                                             "Vehicle Registration Region"])
#  .nlargest(11)
#  .plot(kind='barh'))
# select_features()
# plt.show()
