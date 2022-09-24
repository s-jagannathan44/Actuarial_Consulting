import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error, r2_score, make_scorer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.model_selection import train_test_split, cross_val_score
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


def calculate_alpha():
    global dt
    # We will calculate cost complexity here
    path = dt.cost_complexity_pruning_path(X_train, y_train)  # determine values for alpha
    ccp_alphas = path.ccp_alphas  # extract different values of alpha
    ccp_alphas = ccp_alphas[:-1]  # exclude maximum value for alpha
    clf_dts = []  # create an array to put decision trees into
    # now create one decision tree per value of alpha and store it in the array
    # ccp = cost complexity pruning
    for ccp_alpha in ccp_alphas:
        clf_dt = DecisionTreeRegressor(random_state=0, ccp_alpha=ccp_alpha, criterion='absolute_error')
        clf_dt.fit(X_train, y_train)
        clf_dts.append(clf_dt)
    train_maes = []
    test_maes = []
    for dt in clf_dts:
        tree_predictions = dt.predict(X_test)
        test_maes.append(mean_absolute_error(y_test, tree_predictions))
    for dt in clf_dts:
        tree_predictions = dt.predict(X_train)
        train_maes.append(mean_absolute_error(y_train, tree_predictions))
    fig, ax = plt.subplots()
    ax.set_xlabel("alpha")
    ax.set_ylabel("Mean Absolute Error")
    ax.set_title("MAE vs alpha for training and test sets")
    ax.plot(ccp_alphas, train_maes, marker='o', label='train', drawstyle="steps-post")
    ax.plot(ccp_alphas, test_maes, marker='*', label='test', drawstyle="steps-post")
    ax.legend()
    mae_scorer = make_scorer(mean_absolute_error, greater_is_better=False)
    # create an array to store the results of each fold during cross validation
    alpha_loop_values = []
    for ccp_alpha in ccp_alphas:
        clf_dt = DecisionTreeRegressor(random_state=0, ccp_alpha=ccp_alpha, criterion='absolute_error')
        scores = cross_val_score(clf_dt, X_train, y_train, cv=10, scoring=mae_scorer)
        alpha_loop_values.append([ccp_alpha, np.mean(scores), np.std(scores)])
    # now we can draw a graph of the means and standard deviations of the scores for each candidate value of alpha
    alpha_results = pd.DataFrame(alpha_loop_values, columns=['alpha', "mean_error", 'std'])
    alpha_results.plot(x='alpha', y='mean_error', yerr='std', marker='o', linestyle='--')
    dt = DecisionTreeRegressor(random_state=42, criterion='absolute_error', ccp_alpha=.30876)
    dt.fit(X_train, y_train)
    # We will plot the tree here
    plt.figure(figsize=(15, 7.5))
    plot_tree(dt, filled=True, rounded=True, feature_names=get_columns())
    plt.show()


def plot_feature_importance():
    importance = dt.feature_importances_
    print(importance)
    columns = get_columns()
    combo = pd.Series(importance, columns)
    figure(figsize=(16, 4))
    combo.sort_values().plot.barh(color='red')
    plt.title('Visualization of decision tree model feature importance')
    plt.show()


def get_columns():
    encoder = transformer.named_transformers_['onehot_categorical']
    columns = encoder.get_feature_names_out()
    encoder = transformer.named_transformers_['ordinal']
    ord_columns = encoder.get_feature_names_out()
    columns = np.append(columns, ord_columns)
    return columns


def write_output():
    one_hot = transformer.named_transformers_['onehot_categorical'].inverse_transform(X_test[:, :4])
    ordinal = transformer.named_transformers_['ordinal'].inverse_transform(X_test[:, 4:])
    one_frame = pd.DataFrame(one_hot, columns=["MaritalMainDriver"])
    ordinal_frame = pd.DataFrame(ordinal, columns=["GenderMainDriver"])

    # axis 0 is vertical and axis 1 is horizontal
    output = pd.concat([one_frame, ordinal_frame], axis=1)

    frame = pd.DataFrame(output.copy(), columns=df.columns)
    frame["Claim"] = y_test.to_list()
    frame['Predicted'] = y_pred_dt
    frame.to_csv("Output\\Output.csv")


#  Part 1 read study and transform the file
df = pd.read_csv("Output\\Sev_1.csv")

for c in df.columns:
    print(df[c].name, df[c].unique())
X = df.drop('Claim', axis=1)

y = df["Claim"]
print(X["GenderMainDriver"].value_counts())

transformer = ColumnTransformer(
    [("onehot_categorical", OneHotEncoder(), ["MaritalMainDriver"],),
     ("ordinal", OrdinalEncoder(), ["GenderMainDriver"],),
     ],
    remainder='drop'
)

X = transformer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=40)

dt = DecisionTreeRegressor(random_state=42, criterion='absolute_error')
dt.fit(X_train, y_train)

# We will plot the tree here
plt.figure(figsize=(15, 7.5))
plot_tree(dt, filled=True, rounded=True, feature_names=get_columns())


calculate_alpha()


y_pred_dt = dt.predict(X_test)
print('r2 score', dt.score(X_test, y_test))
print('predicted mean', y_pred_dt.mean())

# get the mean baseline because this is a regression problem
# with regression, the baseline can be as simple as the mean.

mean_baseline = y_test.mean()

y_pred_base = [mean_baseline] * len(y_test)
mae_base = mean_absolute_error(y_test, y_pred_base)
mae_model = mean_absolute_error(y_test, y_pred_dt)
r2_base = r2_score(y_test, y_pred_base)

print(f'Mean Baseline: {mean_baseline:.1f} ')
print(f'Baseline mean absolute error: {mae_base}')
print(f'Model mean absolute error: {mae_model}')
print(f'r2 score: {r2_base}')

"""
Why R2 of 0?

From SKLEARN

"A constant model that always predicts the expected value of y, 
disregarding the input features, would get a R^2 score of 0.0."

"""


# plot_feature_importance()
# write_output()
# Try out Permutation Importance
