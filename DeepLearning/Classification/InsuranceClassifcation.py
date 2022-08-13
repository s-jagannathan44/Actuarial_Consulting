import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from tensorflow import keras
from sklearn import preprocessing


def create_model():
    # Define the model
    model = Sequential([
        Dense(500, activation='relu', input_shape=(len(predictors),)),
        Dense(100, activation='relu'),
        Dense(50, activation='relu'),
        Dense(1, activation="sigmoid"),
    ])

    # Compile the model
    metrics = [
        keras.metrics.FalseNegatives(name="fn"),
        keras.metrics.FalsePositives(name="fp"),
        keras.metrics.TrueNegatives(name="tn"),
        keras.metrics.TruePositives(name="tp"),
    ]

    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=metrics)

    model.fit(X_train, y_train, epochs=30, verbose=0)
    return model


def create_mapping(dataframe_values):
    counter = 0
    _dictionary = {}
    for v in dataframe_values:
        item = [(v, counter)]
        _dictionary.update(item)
        counter = counter + 1
    return _dictionary


def map_categorical_values():
    df.Make = df.Make.map(MakeValues)
    df.GenderMainDriver = df.GenderMainDriver.map(GenderValues)
    df.MaritalMainDriver = df.MaritalMainDriver.map(MaritalValues)
    df.VehicleValue = df.VehicleValue.map(VehicleValues)
    df.Use = df.Use.map(Uses)
    df.PaymentMethod = df.PaymentMethod.map(PaymentMethods)
    df.PaymentFrequency = df.PaymentFrequency.map(PaymentFrequencies)


def invert_mapping():
    df.Make = df.Make.map(invertMake)
    df.GenderMainDriver = df.GenderMainDriver.map(invertGender)
    df.MaritalMainDriver = df.MaritalMainDriver.map(invertMaritalMainDriver)
    df.VehicleValue = df.VehicleValue.map(invertVehicleValue)
    df.Use = df.Use.map(invertUse)
    df.PaymentMethod = df.PaymentMethod.map(invertPaymentMethod)
    df.PaymentFrequency = df.PaymentFrequency.map(invertPaymentFrequency)


def create_output_dataframe():
    global df
    my_input = X_test[:, numeric_column_count:numeric_column_count + len(categorical_columns)]
    Make = my_input[:, 0]
    Gender = my_input[:, 1]
    MaritalMainDriver = my_input[:, 2]
    VehicleValue = my_input[:, 3]
    Use = my_input[:, 4]
    PaymentMethod = my_input[:, 5]
    PaymentFrequency = my_input[:, 6]
    df = pd.DataFrame({"Make": Make, "GenderMainDriver": Gender, "MaritalMainDriver": MaritalMainDriver,
                       "VehicleValue": VehicleValue, "Use": Use, "PaymentMethod": PaymentMethod,
                       "PaymentFrequency": PaymentFrequency})


# Step 1 read the CSV file
# Step 2 scale the values
# Step 3 Map   the values
# Step 4 define , compile and fit  the model
# Step 5 predict the output and write to file
# Step 6 unscale the values and write to file
# Step 7 unmap the values and write to file

#  Step 1
df = pd.read_csv("Insurance.csv")
#  Step 2 ------------------ begin ----------------------------------
target_column = ['Freq_Act']
categorical_columns = ['Make', 'GenderMainDriver', 'MaritalMainDriver', 'VehicleValue', 'Use', 'PaymentMethod',
                       'PaymentFrequency']

predictors = list(set(list(df.columns)) - set(target_column) - set(categorical_columns))
numerical_predictors = list()
for column in predictors:
    numerical_predictors.append(column)

min_max_scaler = preprocessing.MinMaxScaler()

df[predictors] = X_scale = min_max_scaler.fit_transform(df[predictors])

for column in categorical_columns:
    predictors.append(column)
# ------------------ end ----------------------------------


# Step 3 ------------------ begin ----------------------------------
MakeValues = create_mapping(df.Make.unique())
GenderValues = create_mapping(df.GenderMainDriver.unique())
MaritalValues = create_mapping(df.MaritalMainDriver.unique())
VehicleValues = create_mapping(df.VehicleValue.unique())
Uses = create_mapping(df.Use.unique())
PaymentMethods = create_mapping(df.PaymentMethod.unique())
PaymentFrequencies = create_mapping(df.PaymentFrequency.unique())
map_categorical_values()
X = df[predictors].values
y = df[target_column].values
# ------------------ end ----------------------------------

# Step 4
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=40)
insurance_model = create_model()
# Step 5
y_pred = insurance_model.predict(X_test)
np.savetxt("y_test.csv", y_test, delimiter=",")
np.savetxt("y_pred.csv", y_pred, delimiter=",")

# Step 6 ------------------begin--------------------------------
numeric_column_count = X_test.shape[1] - len(categorical_columns)
my_numerical_input = X_test[:, 0:numeric_column_count]
my_numerical_input = min_max_scaler.inverse_transform(my_numerical_input)
numerical_df = pd.DataFrame(my_numerical_input, columns=numerical_predictors)
numerical_df.to_csv("output.csv")
# ------------------end--------------------------------------


# Step 7 ------------------begin--------------------------------
invertGender = {v: k for k, v in GenderValues.items()}
invertMake = {v: k for k, v in MakeValues.items()}
invertMaritalMainDriver = {v: k for k, v in MaritalValues.items()}
invertVehicleValue = {v: k for k, v in VehicleValues.items()}
invertUse = {v: k for k, v in Uses.items()}
invertPaymentMethod = {v: k for k, v in PaymentMethods.items()}
invertPaymentFrequency = {v: k for k, v in PaymentFrequencies.items()}

create_output_dataframe()
invert_mapping()
df.to_csv("Categorical.csv")
# ------------------end--------------------------------------
