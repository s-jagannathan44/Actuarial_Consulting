import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import KBinsDiscretizer, OrdinalEncoder
from keras import Sequential
from keras.layers import Dense
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


def create_model(length, dep, independent):
    # Define the model
    model = Sequential([
        Dense(500, activation='relu', input_shape=(length,)),
        Dense(100, activation='relu'),
        Dense(50, activation='relu'),
        Dense(1, activation="sigmoid"),
    ])

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(dep, independent, epochs=200, batch_size=100)
    return model


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
        my_tuple = (name, passthrough, [p])
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


def load_predict(filename, data):
    my_model = keras.models.load_model(filename)
    my_model.compile(optimizer='adam',
                     loss='mean_squared_error')
    y_pred = my_model.predict(data)
    np.savetxt("y_pred.csv", y_pred, delimiter=",")


passthrough_list = []
ordinal_list = ["GenderMainDriver", "MaritalMainDriver", "Make", "Use"]
to_bin_list = [['VehicleValue', 10, 'uniform']]

X, y = fetch_data("Input30k.csv", 5)

X = transform(passthrough_list, to_bin_list, ordinal_list).fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=40)

# create_model(5, X_train, y_train).save("My_Model.h5")
load_predict("My_Model.h5", X)


