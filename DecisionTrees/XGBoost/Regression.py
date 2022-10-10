import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder
from xgboost import XGBRegressor

ordinal_columns = ["TP Pool / Non TP Pool", "FY", "Loss Type"]
ohe_columns = ["Segment 1", "Make", "Product Type 1",  "RTO State - RTO State"]


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


def transform():
    ordinal_tuple = ("ordinal", OrdinalEncoder(), ordinal_columns)
    # transformer_ = ColumnTransformer([ordinal_tuple, ohe_tuple], remainder='drop')
    transformer_ = ColumnTransformer([ordinal_tuple, ("onehot_categorical", OneHotEncoder(sparse=False),
                                                      ohe_columns)], remainder='drop')
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
    frame.to_csv("Output\\Output.csv")


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
df = pd.read_csv("Output\\Commercial - Cleaned.csv")
df.drop(df[(df['TOTAL_OURSHARE'] < 1000)].index, inplace=True)
df.drop(df[(df['TOTAL_OURSHARE'] > 2000000)].index, inplace=True)

transformer = transform()

X = df.drop('TOTAL_OURSHARE', axis=1)
y = df["TOTAL_OURSHARE"]
X = transformer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=40)
rgr = XGBRegressor(objective='reg:gamma',  seed=42, eval_metric='mae', max_depth=5,
                   learning_rate=0.1, n_estimators=300)
rgr.fit(X_train, y_train)
y_pred = predict(X_test, y_test, rgr)
get_columns()
write_output(X_test, y_test, y_pred)
