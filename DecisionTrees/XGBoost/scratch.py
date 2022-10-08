import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error, make_scorer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
import xgboost as xgb
from sklearn.model_selection import train_test_split, GridSearchCV
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


def return_best_tree(regressor, X_train_val, y_train_val,  X_test_val, y_test_val, exposure):
    # get the mean baseline because this is a regression problem
    # with regression, the baseline can be as simple as the mean.
    mean_baseline = y_test_val.mean()
    y_pred_base = [mean_baseline] * len(y_test_val)

    mae_base = mean_absolute_error(y_test_val, y_pred_base)
    print(f'Mean Baseline: {mean_baseline:.1f} ')
    print(f'Baseline mean absolute error: {mae_base}')
    # print(f'r2 score: {r2_base}')
    # defining parameter range
    param_grid = {
        'max_depth': [3, 4, 5, 6],
        'learning_rate': [0.01, 0.1, 0.3],
        'n_estimators': [100, 300, 500]
    }
    param_dict = {'sample_weight': exposure, 'eval_set': [(X_test_val, y_test_val)], 'verbose': True}
    mae_scorer = make_scorer(mean_absolute_error, greater_is_better=False)
    xgb_reg = GridSearchCV(regressor, param_grid, scoring=mae_scorer, cv=3, refit=True, verbose=3, n_jobs=-1)
    xgb_reg.fit(X_train_val, y_train_val, **param_dict)
    # print best parameter after tuning
    print(xgb_reg.best_params_)
    return xgb_reg.best_estimator_


def plot_feature_importance(tree_):
    importance = tree_.feature_importances_
    print(importance)
    columns = get_columns()
    combo = pd.Series(importance, columns)
    figure(figsize=(16, 4))
    combo.sort_values().plot.barh(color='red')
    plt.title('Visualization of decision tree model feature importance')


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


def write_output(X_val, actual_val, pred_val, exposure):
    one_hot = transformer.named_transformers_['onehot_categorical'].inverse_transform(X_val[:, ord_col_size:])
    ordinal = transformer.named_transformers_['ordinal'].inverse_transform(X_val[:, :ord_col_size])
    one_frame = pd.DataFrame(one_hot, columns=["MaritalMainDriver", "DrivingRestriction", "Make"])
    ordinal_frame = pd.DataFrame(ordinal, columns=["GenderMainDriver", "VehFuel1"])

    # axis 0 is vertical and axis 1 is horizontal
    output = pd.concat([one_frame, ordinal_frame], axis=1)
    output["Exposure"] = exposure
    frame = pd.DataFrame(output.copy(), columns=df.columns)
    frame["Claim"] = actual_val.to_list()
    frame['Predicted'] = pred_val
    frame.to_csv("Output\\Output.csv")


def read_analyze_transform(filename):
    df_ = pd.read_csv(filename)
    for c in df_.drop('Claim', axis=1).columns:
        csv_file_name = "Output\\Columns\\" + c + ".csv"
        insight = df_[c].value_counts()
        insight.to_csv(csv_file_name)
    X_ = df_.drop('Claim', axis=1)
    y_ = df_["Claim"]

    transformer_ = ColumnTransformer(
        [
            ("passthrough_numeric", "passthrough", ["Exposure"]),
            ("ordinal", OrdinalEncoder(), ["GenderMainDriver", "VehFuel1"]),
            ("onehot_categorical", OneHotEncoder(), ["MaritalMainDriver", "DrivingRestriction", "Make"],),
        ],
        remainder='drop'
    )
    X_ = transformer_.fit_transform(X_)
    return df_, X_, y_, transformer_


def build_tree(X_train_val, y_train_val, X_test_val, y_test_val):
    rgr = xgb.XGBRegressor(objective='reg:gamma', seed=42, early_stopping_rounds=10, eval_metric='mae')
    flat_arr = X_train_val[:, :1]
    exposure = np.reshape(flat_arr, np.shape(X_train_val)[0])
    X_test_val = X_test_val[:, 1:]
    # We will export the tree here
    rgr = return_best_tree(rgr, X_train_val, y_train_val, X_test_val,  y_test_val, exposure)
    # tree.export_graphviz(dt_, out_file="Output\\tree.img", filled=True, rounded=True, feature_names=get_columns())
    return rgr


def predict_tree(X_val, y_val, tree_):
    # We will predict the output  here
    y_pred_dt_ = tree_.predict(X_val)
    np.savetxt("Output\\y_pred.csv", y_pred_dt_, delimiter=",")
    # print('r2 score', tree_.score(X_val, y_val))
    print('predicted mean', y_pred_dt_.mean())
    mae_model = mean_absolute_error(y_val, y_pred_dt_)
    print(f'Model mean absolute error: {mae_model}')
    return y_pred_dt_


# -------------------- CODE STARTS HERE ---------------------------------------
ord_col_size = ohe_col_size = 0
df, X, y, transformer = read_analyze_transform("Output\\Sev_3.csv")
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=40)
X_train = X_train.toarray()
X = X.toarray()
model = build_tree(X_train, y_train, X_test, y_test)

# remove exposure from feature set
X_train = X_train[:, 1:]
exposure_arr = X[:, :1]
test_exposure = np.reshape(exposure_arr, np.shape(X)[0])
X = X[:, 1:]

# model = joblib.load("SeverityRegressionTree.sav")
# y_pred = predict_tree(X, y, model)
# write_output(X, y, y_pred, test_exposure)
