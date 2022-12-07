import numpy as np
import pandas as pd
from keras import Model, Input
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from Modules import Utilities as Ut

ordinal_list = ["NAME_CONTRACT_TYPE", "CODE_GENDER", "FLAG_OWN_CAR", "FLAG_OWN_REALTY", "NAME_INCOME_TYPE",
                "NAME_EDUCATION_TYPE", "OCCUPATION_TYPE", "NAME_FAMILY_STATUS", "NAME_HOUSING_TYPE",
                "REGION_RATING_CLIENT"]
scaler_list = ["AMT_INCOME_TOTAL", "AMT_CREDIT", "CNT_CHILDREN", "REGION_POPULATION_RELATIVE",
               "DAYS_BIRTH", "DAYS_EMPLOYED"]
to_bin_list = [['AMT_INCOME_TOTAL', 4, 'uniform'],
               ['AMT_CREDIT', 4, 'uniform']]


def data_analysis():
    df = pd.read_csv('Output\\application_data.csv')
    for c in df.columns:
        csv_file_name = "Output\\Columns\\" + c.replace("/", "_") + ".csv"
        insight = df[c].value_counts()
        insight.to_csv(csv_file_name)
    df.describe(percentiles=[0.25, 0.5, 0.75, 0.85, 0.9, 0.98, 1]).to_csv("Output\\Columns\\desc.csv")


def data_modification():
    df = pd.read_csv('Output\\Credit.csv')
    df = df.replace({'NAME_FAMILY_STATUS': {'Civil marriage': 'Single / not married'}})
    df = df.replace({'NAME_INCOME_TYPE': {'State servant': 'Pensioner'}})
    df = df.replace({'NAME_HOUSING_TYPE': {'Co-op apartment': 'House / apartment'}})
    df = df.replace({'OCCUPATION_TYPE': {'IT staff': 'Core staff', 'HR staff': 'Core staff',
                                         'Managers': 'Core staff',
                                         'High skill tech staff': 'Core staff'
                                         }})
    df = df.replace({'OCCUPATION_TYPE': {'Cooking staff': 'Laborers', 'Security staff': 'Laborers'}})
    df = df.replace({'OCCUPATION_TYPE': {'Waiters/barmen staff': 'Drivers'}})
    df = df.replace({'OCCUPATION_TYPE': {'Medicine staff': 'Private service staff',
                                         'Secretaries': 'Private service staff'}})
    df = df.replace({'OCCUPATION_TYPE': {'Cleaning staff': 'Sales staff', }})

    df["AMT_INCOME_TOTAL"] = df["AMT_INCOME_TOTAL"].clip(upper=420000)
    df["AMT_INCOME_TOTAL"] = df["AMT_INCOME_TOTAL"].clip(lower=55000)
    df["AMT_CREDIT"] = df["AMT_CREDIT"].clip(upper=2000000)
    df["AMT_CREDIT"] = df["AMT_CREDIT"].clip(lower=100000)
    df["AMT_ANNUITY"] = df["AMT_ANNUITY"].clip(lower=65000)
    df["AMT_ANNUITY"] = df["AMT_ANNUITY"].clip(upper=6500)
    df["CNT_CHILDREN"] = df["CNT_CHILDREN"].clip(upper=2)
    df["REGION_POPULATION_RELATIVE"] = df["REGION_POPULATION_RELATIVE"].clip(lower=.002)

    return df  # df[df["TARGET"] == 0]


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
    frame.to_csv("Output\\Output.csv")


df_ = data_modification()
df_ = Ut.impute_missing_values(df_, "OCCUPATION_TYPE")
# df_.to_csv("Output\\Df.csv")
# how does one get a 378 - 96 split for occupation type
X = df_.drop('TARGET', axis=1)
y = df_["TARGET"]
transformer = Ut.transform([], to_bin_list, ["CODE_GENDER", "NAME_EDUCATION_TYPE", "OCCUPATION_TYPE"])
X = transformer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=X[:, 2:4], random_state=25)

X_train_normal = X_train[y_train == 0]
X_train_fraud = X_train[y_train == 1]

input_layer = Input(shape=(5, ))
encoded = Dense(3, activation='tanh')(input_layer)
decoded = Dense(5, activation='sigmoid')(encoded)

# This is a functional, not sequential neural network
estimator_ = Model(input_layer, decoded)
estimator_.compile(optimizer='adam', loss="mae", metrics="mae")
estimator_.fit(X_train_normal, X_train_normal, epochs=100, batch_size=1000)

# estimator_ = gridsearch(estimator_)
test_predictions = estimator_.predict(X_test)
mae = np.mean(np.abs(X_test - test_predictions), axis=1)
error_df = pd.DataFrame({'reconstruction_error': mae,
                        'true_class': y_test})
error_df.groupby('true_class').describe()
y_pred = [(lambda er: 1 if er >= 1.1 else 0)(er) for er in mae]
column_dict = get_columns()
write_output(X_test, y_test, y_pred)
