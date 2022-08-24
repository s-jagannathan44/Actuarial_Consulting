import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from sklearn.preprocessing import KBinsDiscretizer, OrdinalEncoder
from keras.callbacks import CSVLogger, ModelCheckpoint


def my_loss(y_true, y_pred):
    actual = float(y_true)
    predicted = float(y_pred)
    loss = actual - predicted
    return abs(loss)


def create_model():
    # Define the model
    model = Sequential([
        Dense(500, activation='relu', input_shape=(24,)),
        Dense(100, activation='relu'),
        Dense(50, activation='relu'),
        Dense(1, activation="sigmoid"),
    ])

    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=my_loss)
    csv_logger = CSVLogger('Output\\training1.log')
    checkpoint = ModelCheckpoint(filepath="Output\\Checkpoint_All.h5", monitor="my_loss", verbose=1,
                                 save_best_only=True, mode="min")
    model.fit(X_train, y_train, epochs=200, batch_size=100,
              callbacks=[checkpoint, csv_logger])
    model.save("Output\\Normal_All.h5")
    return model


def impute_missing_values(column_name):
    imp_mean = SimpleImputer(missing_values=-1, strategy='most_frequent')
    df.loc[df[column_name].isnull(), column_name] = -1
    column_values = np.asarray(df[column_name]).reshape(-1, 1)
    df[column_name] = imp_mean.fit_transform(column_values)


def transform():
    return ColumnTransformer(
        [
            ("passthrough_1", "passthrough", ["AnalysisPeriod"]),
            ("passthrough_8", "passthrough", ["NumberOfDrivers"]),
            ("passthrough_14", "passthrough", ["VoluntaryExcess"]),
            ("passthrough_17", "passthrough", ["NumberOfPastClaims"]),
            ("passthrough_18", "passthrough", ["NumberOfPastConvictions"]),
            ("passthrough_24", "passthrough", ["ClaimLastYr"]),
            ("binned_2", KBinsDiscretizer(n_bins=4, encode='ordinal', strategy='quantile'), ["AgeMainDriver"]),
            ("binned_3", KBinsDiscretizer(n_bins=4, encode='ordinal', strategy='quantile'), ["AgeYoungestDriver"]),
            ("binned_4", KBinsDiscretizer(n_bins=2, encode='ordinal', strategy='quantile'),
             ["AgeYoungestAdditionalDriver"]),
            ("binned_9", KBinsDiscretizer(n_bins=2, encode='ordinal', strategy='quantile'), ["VehicleAge"]),
            ("binned_11", KBinsDiscretizer(n_bins=10, encode='ordinal', strategy='quantile'), ["VehicleValue"]),
            ("binned_13", KBinsDiscretizer(n_bins=4, encode='ordinal', strategy='quantile'), ["VehicleMileage"]),
            ("binned_15", KBinsDiscretizer(n_bins=4, encode='ordinal', strategy='quantile'), ["BonusMalusYears"]),
            ("binned_19", KBinsDiscretizer(n_bins=3, encode='ordinal', strategy='quantile'), ["PolicyTenure"]),
            (
                "onehot_categorical",
                OrdinalEncoder(),
                ["GenderMainDriver", "GenderYoungestDriver",  "MaritalMainDriver",
                 "Make", "Use", "PaymentMethod", "PaymentFrequency", "BonusMalusProtection",
                 "GenderYoungestAdditionalDriver", "VehFuel1"],
            ),
        ],
        remainder='drop'
    )


df = pd.read_csv("Output\\Input.csv")
impute_missing_values("AgeYoungestAdditionalDriver")
impute_missing_values("GenderYoungestAdditionalDriver")
X = df.iloc[:, :39]
y = df.iloc[:, 39:]


predictors = ["AnalysisPeriod", "NumberOfDrivers", "VoluntaryExcess", "NumberOfPastClaims",
              "NumberOfPastConvictions", "ClaimLastYr",
              "AgeMainDriver", "AgeYoungestDriver", "AgeYoungestAdditionalDriver",
              "VehicleAge", "VehicleValue", "VehicleMileage", "BonusMalusYears", "PolicyTenure",
              "GenderMainDriver", "GenderYoungestDriver", "MaritalMainDriver",
              "Make", "Use", "PaymentMethod", "PaymentFrequency", "BonusMalusProtection",
              "GenderYoungestAdditionalDriver", "VehFuel1"]
X = transform().fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=40)

df = pd.DataFrame(X_test, columns=predictors)

#df.to_csv("Output\\X_test.csv")

y_pred_ = np.sum(create_model().predict(X_test))
print(y_pred_)
