import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import KBinsDiscretizer, OrdinalEncoder
from tensorflow import keras


def my_loss(y_true, y_pred):
    actual = float(y_true)
    predicted = float(y_pred)
    loss = actual - predicted
    return loss


def load_predict(filename):
    my_model = keras.models.load_model(filename, custom_objects={"my_loss": my_loss})
    my_model.compile(optimizer='adam',
                     loss='binary_crossentropy')
    return float(np.sum(my_model.predict(X)))


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


df = pd.read_csv("Output\\Input30k.csv")
impute_missing_values("AgeYoungestAdditionalDriver")
impute_missing_values("GenderYoungestAdditionalDriver")
X = df.iloc[:, :39]
y = df.iloc[:, 39:]
X = transform().fit_transform(X)
actual_value = float(np.sum(y))

normal = load_predict("Output\\Normal_All.h5")
print("Normal prediction:", normal)
print("Normal Error:", (abs(normal-actual_value)/actual_value) * 100)

checkpoint = load_predict("Output\\Checkpoint_All.h5")
print("Model prediction:", checkpoint)
print("Model Error:", (abs(checkpoint-actual_value)/actual_value) * 100)

callback = load_predict("Output\\Callback_All.h5")
print("Callback  prediction:", callback)
print("Callback Error:", (abs(callback-actual_value)/actual_value) * 100)
