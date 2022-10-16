import math
from matplotlib import pyplot
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import GroupShuffleSplit, GridSearchCV
from xgboost import XGBRegressor, plot_importance
import Modules.Utilities as Ut
import pandas as pd


def describe():
    df = pd.read_csv("Output\\FMTPL.csv")
    temp = df.drop(['IDpol', 'Exposure', 'ClaimNb', 'Claim'], axis=1)
    df_freq = temp.iloc[temp.drop_duplicates().index]
    df_freq = df_freq.reset_index(drop=True)
    df_freq['GroupID'] = df_freq.index + 1
    df_freq.to_csv("Output\\Unique.csv")
    df_freq = pd.merge(df, df_freq, how='left')
    df_freq['GroupID'] = df_freq['GroupID'].fillna(method='ffill')
    print(df_freq['GroupID'].max())
    df_freq.to_csv("Output\\Grouped.csv")

    df_freq = df_freq[df_freq["Claim"] > 0]
    df_freq = df_freq.drop('IDpol', axis=1)
    for c in df_freq.columns:
        csv_file_name = "Output\\Columns\\" + c + ".csv"
        insight = df[c].value_counts()
        insight.to_csv(csv_file_name)
    df_freq.describe(percentiles=[0.25, 0.5, 0.75, 0.85, 0.9, 0.98, 1]).to_csv("Output\\Columns\\desc.csv")
    df_freq.corr().to_csv("Output\\Columns\\corr.csv")


def read_transform():
    df = pd.read_csv("Output\\Grouped.csv")
    df['VehAge'] = df['VehAge'].apply(lambda x: 20 if x > 20 else x)
    df['DrivAge'] = df['DrivAge'].apply(lambda x: 90 if x > 90 else x)
    df['BonusMalus'] = df['BonusMalus'].apply(lambda x: 150 if x > 150 else int(x))
    df['Density'] = df['Density'].apply(lambda x: round(math.log(x), 2))
    df['Exposure'] = df['Exposure'].apply(lambda x: 1 if x > 1 else x)
    df_freq_ml = Ut.motor_third_party_transform(df)
    df_freq_ml = df_freq_ml[df_freq_ml["Claim"] > 0]

    df_freq_ml["Target"] = df_freq_ml['Claim'] / df_freq_ml['ClaimNb']
    splitter = GroupShuffleSplit(test_size=0.2, n_splits=2, random_state=999)
    split = splitter.split(df_freq_ml, groups=df_freq_ml['GroupID'])
    train_ind, test_ind = next(split)
    df_freq_ml = df_freq_ml.drop(['ClaimNb', 'Exposure', 'GroupID', 'Claim'], axis=1)
    train = df_freq_ml.iloc[train_ind]
    test = df_freq_ml.iloc[test_ind]
    df_freq_ml.to_csv("Output\\normalised.csv")
    return train.drop("Target", axis=1), train["Target"], test.drop("Target", axis=1), test["Target"]


def predict(X_val, y_val, estimator):
    # We will predict the output  here
    y_pred_ = estimator.predict(X_val)

    mean_baseline = y_val.mean()
    y_pred_base = [mean_baseline] * len(y_val)
    mae_base = mean_absolute_error(y_val, y_pred_base)
    print(f'Mean Baseline: {mean_baseline:.1f} ')
    print(f'Baseline mean absolute error: {mae_base}')

    print('predicted mean', y_pred_.mean())
    mae_model = mean_absolute_error(y_val, y_pred_)
    print(f'Model mean absolute error: {mae_model}')
    return y_pred_


def write_output(actual_val, pred_val):
    frame = pd.DataFrame(columns=["Actual", "Predicted", "Error", '%ageError', 'Below5%'])
    frame["Actual"] = actual_val.to_list()
    frame['Predicted'] = pred_val
    frame["Error"] = abs(frame["Actual"] - frame["Predicted"])
    frame["%ageError"] = frame["Error"] / frame["Actual"]
    frame["Below5%"] = frame[frame["%ageError"] < 0.05].shape[0] / frame.shape[0]
    print((frame[frame["%ageError"] < 0.05].shape[0] / frame.shape[0]) * 100)
    frame.to_csv("Output\\Output.csv")


def gridsearch(rgr):
    param_grid = \
        {
          'gamma': [0.8]
        }
    model = GridSearchCV(rgr, param_grid, cv=10, scoring="neg_mean_absolute_error", refit=True, verbose=3, n_jobs=-1)
    model.fit(X_train, y_train)
    print(model.best_params_)
    return model.best_estimator_


X_train, y_train, X_test, y_test = read_transform()
estimator_ = XGBRegressor(objective='reg:gamma', seed=42, eval_metric='mae', max_depth=6,
                          gamma=0.8, learning_rate=0.15, n_estimators=300, colsample_bytree=0.9)
estimator_.fit(X_train, y_train)
# estimator_ = gridsearch(estimator_)
plot_importance(estimator_)
y_pred = predict(X_test, y_test, estimator_)
write_output(y_test, y_pred)
pyplot.show()
