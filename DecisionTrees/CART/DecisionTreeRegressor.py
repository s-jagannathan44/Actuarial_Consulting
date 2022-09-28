import joblib
import numpy as np
import pandas as pd
from sklearn import tree
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error, make_scorer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


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


def return_best_tree(tree_, X_train_val, y_train_val, y_test_val):
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
    }
    mae_scorer = make_scorer(mean_absolute_error, greater_is_better=False)
    tree_reg = GridSearchCV(tree_, param_grid, scoring=mae_scorer, cv=5, refit=True, verbose=3, n_jobs=-1)
    tree_reg.fit(X_train_val, y_train_val)
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


def write_output(X_val, actual_val, pred_val):
    one_hot = transformer.named_transformers_['onehot_categorical'].inverse_transform(X_val[:, ord_col_size:])
    ordinal = transformer.named_transformers_['ordinal'].inverse_transform(X_val[:, :ord_col_size])
    one_frame = pd.DataFrame(one_hot, columns=["MaritalMainDriver", "DrivingRestriction", "Make"])
    ordinal_frame = pd.DataFrame(ordinal, columns=["GenderMainDriver", "VehFuel1"])

    # axis 0 is vertical and axis 1 is horizontal
    output = pd.concat([one_frame, ordinal_frame], axis=1)
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
            ("ordinal", OrdinalEncoder(), ["GenderMainDriver", "VehFuel1"]),
            ("onehot_categorical", OneHotEncoder(), ["MaritalMainDriver", "DrivingRestriction", "Make"],),
        ],
        remainder='drop'
    )
    X_ = transformer_.fit_transform(X_)
    return df_, X_, y_, transformer_


def build_tree(X_val, y_val, y_test_val, alpha):
    dt_ = DecisionTreeRegressor(random_state=42, criterion='absolute_error', ccp_alpha=alpha)
    dt_.fit(X_val, y_val)
    # We will export the tree here
    dt_ = return_best_tree(dt_, X_val, y_val, y_test_val)
    tree.export_graphviz(dt_, out_file="Output\\tree.img", filled=True, rounded=True, feature_names=get_columns())
    joblib.dump(dt_, "SeverityRegressionTree.sav")
    return dt_


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
df, X, y, transformer = read_analyze_transform("Output\\Sev_4.csv")
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=40)
X_train = X_train.toarray()
X = X.toarray()
build_tree(X_train, y_train, y_test, 0.0)

model = joblib.load("SeverityRegressionTree.sav")
y_pred = predict_tree(X, y, model)
write_output(X, y,  y_pred)

# alpha_ = calculate_alpha(X_train, y_train, dt)
# dt_pruned = build_tree(X_train, y_train, alpha_)
# y_pred_pruned = predict_tree(X_test, y_test, dt_pruned)
# write_output(X_test, y_test,  y_pred_pruned)
# plot_feature_importance()
# plt.show()
"""
Why R2 of 0?

From SKLEARN

"A constant model that always predicts the expected value of y, 
disregarding the input features, would get a R^2 score of 0.0."
 Try out Permutation Importance
"""
