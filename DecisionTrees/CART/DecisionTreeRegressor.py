import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error, make_scorer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from Modules import Utilities as Ut

passthrough_list = ["AnalysisPeriod", "NumberOfDrivers", "VoluntaryExcess", "NumberOfPastClaims",
                    "NumberOfPastConvictions", "ClaimLastYr"]
ordinal_list = ["GenderMainDriver", "GenderYoungestDriver", "MaritalMainDriver",
                "Make", "Use", "PaymentMethod", "PaymentFrequency", "BonusMalusProtection",
                "GenderYoungestAdditionalDriver", "VehFuel1"]
to_bin_list = [['AgeMainDriver', 4, 'uniform'], ['AgeYoungestDriver', 4, 'uniform'],
               ['AgeYoungestAdditionalDriver', 2, 'uniform'], ['VehicleAge', 2, 'uniform'],
               ['VehicleValue', 10, 'uniform'], ['VehicleMileage', 4, 'uniform'],
               ['BonusMalusYears', 4, 'quantile'], ['PolicyTenure', 3, 'quantile']]


def calculate_alpha(X_val, y_val, tree_):
    # We will calculate cost complexity here
    path = tree_.cost_complexity_pruning_path(X_val, y_val)  # determine values for alpha
    ccp_alphas = path.ccp_alphas  # extract different values of alpha
    ccp_alphas = ccp_alphas[:-1]  # exclude maximum value for alpha
    # create scoring function for MAE to be used with cross_val_score instead of R2
    mae__scorer = make_scorer(mean_absolute_error, greater_is_better=False)
    # create an array to store the results of each fold during cross validation
    alpha_loop_values = []
    for ccp_alpha in ccp_alphas:
        if ccp_alpha > 0:
            clf_dt = DecisionTreeRegressor(random_state=0, ccp_alpha=ccp_alpha, criterion='absolute_error')
            scores = cross_val_score(clf_dt, X_val, y_val, cv=10, scoring=mae__scorer)
            alpha_loop_values.append([ccp_alpha, np.mean(scores), np.std(scores)])
    # now we can draw a graph of the means and standard deviations of the scores for each candidate value of alpha
    alpha_results = pd.DataFrame(alpha_loop_values, columns=['alpha', "mean_error", 'std'])
    alpha_results.plot(x='alpha', y='mean_error', yerr='std', marker='o', linestyle='--')
    # return max error value because they are stored with negative sign
    frame = alpha_results[alpha_results["mean_error"] == alpha_results["mean_error"].max()].head(1)
    return frame["alpha"].iloc[0]


def return_best_tree(tree_, X_train_val, y_train_val, y_test_val, exposure):
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
        'min_samples_leaf': [100, 20, 1],
        'min_weight_fraction_leaf': [0.15, 0.25, 0.45]
    }
    param_dict = {'sample_weight': exposure}
    mae_scorer = make_scorer(mean_absolute_error, greater_is_better=False)
    tree_reg = GridSearchCV(tree_, param_grid, scoring=mae_scorer, cv=10, refit=True, verbose=3, n_jobs=-1)
    tree_reg.fit(X_train_val, y_train_val, **param_dict)
    # print best parameter after tuning
    print(tree_reg.best_params_)
    return tree_reg.best_estimator_


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
    frame = pd.DataFrame(output.copy(), columns=sev.columns)
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


def build_tree(X_val, y_val, alpha):
    dt_ = DecisionTreeRegressor(random_state=42, criterion='absolute_error', ccp_alpha=alpha)
    dt_.fit(X_val, y_val)
    joblib.dump(dt_, "SeverityRegressionTree.sav")
    return dt_


def predict_tree(X_val, y_val, tree_):
    # We will predict the output  here
    y_pred_dt_ = tree_.predict(X_val)
    np.savetxt("Output\\y_pred.csv", y_pred_dt_, delimiter=",")
    print('Actual mean', y_val.mean())
    print('predicted mean', y_pred_dt_.mean())
    mae_model = mean_absolute_error(y_val, y_pred_dt_)
    print(f'Model mean absolute error: {mae_model}')
    return y_pred_dt_


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
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=40)

# build_tree(X_train, y_train, 0.0)

model = joblib.load("SeverityRegressionTree.sav")
y_pred = predict_tree(X, y, model)
