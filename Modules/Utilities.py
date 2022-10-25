import numpy as np
import pandas as pd
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.optimizers import SGD
from matplotlib import pyplot as plt
from scikeras.wrappers import KerasRegressor
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import KBinsDiscretizer, MinMaxScaler, OrdinalEncoder
from keras import Sequential
from keras.layers import Dense, Dropout
from tensorflow import keras


def fetch_data(filename, length):
    df = pd.read_csv(filename)
    print(df.shape)
    df.dropna(how="all", axis=1)

    # X is list of input features
    data = df.iloc[:, 0:length]
    # Y is label of what we want to predict
    target = df.iloc[:, length:]

    return data, target


def create_model(length, X, y, metrics):
    # Define the model
    model = Sequential([
        Dense(2, activation='sigmoid', input_shape=(length,)),
        Dense(14, activation='relu'),
        Dense(1, activation='sigmoid'),
    ])
    checkpoint = ModelCheckpoint(filepath="Output\\Checkpoint.h5", monitor="poisson", verbose=1,
                                 save_best_only=True, mode="min")
    early_stopping = EarlyStopping(monitor="poisson", min_delta=0.00001, patience=5)
    model.compile(optimizer=SGD(learning_rate=0.01, momentum=0.1), loss="poisson", metrics=metrics)
    model.fit(X, y, epochs=1000, batch_size=1000, callbacks=[checkpoint, early_stopping])
    return model


def plot_scatter(columns, levels):
    features = pd.read_csv("Output\\X_test.csv")
    actual = pd.read_csv("Output\\y_test.csv")
    predicted = pd.read_csv("Output\\y_pred.csv")

    features['Actual'] = actual
    features['Predicted'] = predicted

    df_freq = features.drop(['Actual', 'Predicted'], axis=1)
    df_freq = df_freq.iloc[df_freq.drop_duplicates().index]
    df_freq = df_freq.reset_index(drop=True)
    df_freq['GroupID'] = df_freq.index + 1
    df_freq = pd.merge(features, df_freq, how='left')
    df_freq['GroupID'] = df_freq['GroupID'].fillna(method='ffill')
    df_freq.set_index("GroupID", inplace=True, drop=True)

    df3 = df_freq.set_index(columns).groupby(level=levels).sum()

    df3.to_csv("Output\\pivot.csv")
    x = df3["Actual"]
    y = df3["Predicted"]
    plt.scatter(x, y)
    plt.show()


def create_classifier_model(length, X, y, metrics):
    model = Sequential(
        [
            keras.layers.Dense(
                256, activation="relu", input_shape=(length,)
            ),
            Dense(256, activation="relu"),
            Dropout(0.3),
            Dense(256, activation="relu"),
            Dropout(0.3),
            Dense(1, activation="sigmoid"),
        ]
    )
    model.compile(
        optimizer=keras.optimizers.Adam(1e-2), loss="binary_crossentropy", metrics=metrics
    )
    weight_for_0 = 1.0
    weight_for_1 = 1.0
    class_weight = {0: weight_for_0, 1: weight_for_1}
    model.fit(
        X,
        y,
        batch_size=2048,
        epochs=30,
        verbose=2,
        class_weight=class_weight,
    )
    return model


def create_severity_model(length, X, y, metrics):
    # Define the model
    model = Sequential([
        Dense(26, activation='relu', input_shape=(length,)),
        Dense(52, activation='relu'),
        Dense(1),
    ])
    model.compile(optimizer=SGD(learning_rate=0.01, momentum=0.1), loss="mean_absolute_error", metrics=metrics, )
    early_stopping = EarlyStopping(monitor="mean_absolute_error", min_delta=0.01, patience=5)
    checkpoint = ModelCheckpoint(filepath="Output\\Severity.h5", monitor="mean_absolute_error", verbose=1,
                                 save_best_only=True, mode="min")
    sev_regressor = KerasRegressor(model=model,
                                   callbacks=[early_stopping, checkpoint],
                                   batch_size=32,
                                   epochs=100,
                                   verbose=2
                                   )
    sev_regressor.fit(X, y)
    return sev_regressor


def impute_missing_values(dataframe, column_name):
    imp_mean = SimpleImputer(missing_values=-1, strategy='most_frequent')
    dataframe.loc[dataframe[column_name].isnull(), column_name] = -1
    column_values = np.asarray(dataframe[column_name]).reshape(-1, 1)
    dataframe[column_name] = imp_mean.fit_transform(column_values)
    return dataframe


def transform(pass_list, bin_list, categorical_list):
    counter = 0
    index = 0
    my_list = list()
    passthrough = "passthrough"

    for p in pass_list:
        counter = counter + 1
        name = passthrough + str(counter)
        my_tuple = (name, MinMaxScaler(), [p])
        my_list.insert(index, my_tuple)
        index = index + 1
    counter = 0
    for b in bin_list:
        counter = counter + 1
        name = "binned_" + str(counter)
        my_tuple = (name, KBinsDiscretizer(n_bins=b[1], encode='ordinal', strategy=b[2]), [b[0]])
        my_list.insert(index, my_tuple)
        index = index + 1

    my_tuple = ("onehot_categorical", OrdinalEncoder(), categorical_list)
    my_list.insert(index, my_tuple)
    ct = ColumnTransformer(my_list, remainder="drop")
    return ct


def load_predict(my_model, data):
    y_pred = my_model.predict(data)
    np.savetxt("Output\\y_pred.csv", y_pred, delimiter=",")
    return y_pred


def motor_third_party_transform(freq):
    freq = freq.drop(['VehBrand', 'Region'], axis=1)
    columns = ["ClaimNb", "Exposure", "Area", "VehPower", "VehAge", "DrivAge", "BonusMalus",
               "VehGas", "Density", 'Claim', 'GroupID']

    freq['VehGas'] = freq['VehGas'].apply(lambda x: 0.5 if x == "'Regular'" else -0.5)
    area_pipe = Pipeline([
        ('encoder', OrdinalEncoder()),
        ('Scaler', MinMaxScaler())
    ])

    preprocessor = ColumnTransformer(
        [("area", area_pipe, ["Area"])], remainder='passthrough')

    ct = ColumnTransformer(
        [("Scaler", MinMaxScaler(), ["VehPower", "VehAge", "DrivAge", "BonusMalus", "Density"]), ],
        remainder='passthrough'
    )
    preprocessor.fit(freq)
    area_transform = pd.DataFrame(preprocessor.transform(freq), columns=columns)
    ct.fit(area_transform)

    temp = ct.transform(area_transform)
    full_columns = ["VehPower", "VehAge", "DrivAge", "BonusMalus", "Density", "Area", "ClaimNb", "Exposure",
                    "VehGas", "Claim", "GroupID"]
    return pd.DataFrame(temp, columns=full_columns)


def motor_third_party_severity_transform(freq):
    freq = freq.drop(['IDpol', 'VehBrand', 'Region'], axis=1)
    columns = ["Area", "ClaimNb", "Exposure", "VehPower", "VehAge", "DrivAge", "BonusMalus",
               "VehGas", "Density", "Claim", 'GroupID']

    freq['VehGas'] = freq['VehGas'].apply(lambda x: 0.5 if x == "'Regular'" else -0.5)
    area_pipe = Pipeline([
        ('encoder', OrdinalEncoder()),
        ('Scaler', MinMaxScaler())
    ])

    preprocessor = ColumnTransformer(
        [("area", area_pipe, ["Area"])], remainder='passthrough')

    ct = ColumnTransformer(
        [("Scaler", MinMaxScaler(), ["VehPower", "VehAge", "DrivAge", "BonusMalus", "Density"]), ],
        remainder='passthrough'
    )
    preprocessor.fit(freq)
    area_transform = pd.DataFrame(preprocessor.transform(freq), columns=columns)
    ct.fit(area_transform)

    temp = ct.transform(area_transform)
    full_columns = ["VehPower", "VehAge", "DrivAge", "BonusMalus", "Density", "Area", "ClaimNb", "Exposure",
                    "VehGas", "Claim", "GroupID"]
    return pd.DataFrame(temp, columns=full_columns)


def fetch_xy(dataframe, length):
    print(dataframe.shape)
    dataframe.dropna(how="all", axis=1)

    # X is list of input features
    data = dataframe.iloc[:, 0:length]
    # Y is label of what we want to predict
    target = dataframe.iloc[:, length:]

    return data, target
