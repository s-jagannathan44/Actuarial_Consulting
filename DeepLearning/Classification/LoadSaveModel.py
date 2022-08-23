import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
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
    y_pred = my_model.predict(X)
    np.savetxt("Output\\y_pred.csv", y_pred, delimiter=",")
    return float(np.sum(y_pred))


def transform(data):
    transformer = ColumnTransformer(
        [
            ("binned_numeric", KBinsDiscretizer(n_bins=10, encode='ordinal', strategy='quantile'), ["VehicleValue"]),
            (
                "onehot_categorical",
                OrdinalEncoder(),
                ["GenderMainDriver", "MaritalMainDriver", "Make", "Use", "PaymentMethod", "PaymentFrequency"],
            ),
        ],
        remainder='drop'
    )
    return transformer.fit_transform(data)


df = pd.read_csv("Output\\Insurance.csv")
X = df.iloc[:, :39]
y = df.iloc[:, 39:]
X = transform(X)
actual_value = float(np.sum(y))

callback = load_predict("Output\\Callback.h5")
print("Callback  prediction:", callback)
print("Callback Error:", (abs(callback-actual_value)/actual_value) * 100)
