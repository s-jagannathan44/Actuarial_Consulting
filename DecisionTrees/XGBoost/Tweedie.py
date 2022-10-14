import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder
from xgboost import XGBRegressor

ordinal_columns = ["GenderMainDriver"]
ohe_columns = ["MaritalMainDriver", "Make", "Use", "PaymentMethod", "PaymentFrequency"]


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


def get_transformer():
    ordinal_tuple = ("ordinal", OrdinalEncoder(), ordinal_columns)
    transformer_ = ColumnTransformer(
        [("passthrough_numeric", "passthrough", ["Exposure"]), ordinal_tuple,
         ("onehot_categorical", OneHotEncoder(sparse=False), ohe_columns)],
        remainder='drop')
    return transformer_


def write_output(X_val, actual_val, pred_val):
    one_hot = transformer.named_transformers_['onehot_categorical'].inverse_transform(X_val[:, ord_col_size:])
    ordinal = transformer.named_transformers_['ordinal'].inverse_transform(X_val[:, :ord_col_size])
    one_frame = pd.DataFrame(one_hot, columns=ohe_columns)
    ordinal_frame = pd.DataFrame(ordinal, columns=ordinal_columns)

    # axis 0 is vertical and axis 1 is horizontal
    frame = pd.concat([one_frame, ordinal_frame], axis=1)
    frame["Actual"] = actual_val.to_list()
    frame['Predicted'] = pred_val
    frame["Exposure"] = test_exposure
    frame["Error"] = abs(frame["Actual"] - frame["Predicted"])
    frame.to_csv("Output\\Output.csv")


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


# -------------------- CODE STARTS HERE ---------------------------------------
ord_col_size = ohe_col_size = 0
df = pd.read_csv("Output\\WeightedPolicy.csv")

transformer = get_transformer()

X = df.drop('Actual', axis=1)
y = df["Actual"]
X = transformer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=40)
''' 
'learning_rate': 0.01,'gamma':1.5,'max_depth': 2, 'subsample':0.6, 'reg_alpha': 0,'reg_lambda':1,'min_child_weight':5, 
'n_estimators':2000,'tweedie_variance_power':1.6}
'''

rgr = XGBRegressor(objective='reg:tweedie', seed=42, eval_metric='tweedie-nloglik@1.2', max_depth=5,
                   learning_rate=0.1, n_estimators=300, tweedie_variance_power=1.9)

flat_arr = X_train[:, :1]
exposure = np.reshape(flat_arr, np.shape(X_train)[0])
X_train = X_train[:, 1:]
test_exposure = np.reshape(X_test[:, :1], np.shape(X_test)[0])
X_test = X_test[:, 1:]
param_dict = {'sample_weight': exposure, 'verbose': True}

rgr.fit(X_train, y_train, **param_dict)
y_pred = predict(X_test, y_test, rgr)
get_columns()
write_output(X_test, y_test, y_pred)

df = pd.read_csv("Output\\Output.csv")
df = df[df["Actual"] > 0]
df["%ageError"] = df["Error"] / df["Actual"]
df["Below%% "] = df[df["%ageError"] < 0.05].shape[0] / df.shape[0]
df.to_csv("Output\\WithError.csv")
print(df[df["%ageError"] < 0.05].shape[0] / df.shape[0])
