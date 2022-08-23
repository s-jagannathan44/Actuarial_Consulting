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
    return float(np.sum(my_model.predict(X)))


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


df = pd.read_csv("Output\\Input.csv")
X = df.iloc[:, :39]
y = df.iloc[:, 39:]
X = transform(X)
actual_value = float(np.sum(y))

normal = load_predict("ModelFiles\\Normal.h5")
print("Normal prediction:", normal)
print("Normal Error:", (abs(normal-actual_value)/actual_value) * 100)

checkpoint = load_predict("ModelFiles\\Checkpoint.h5")
print("Model prediction:", checkpoint)
print("Model Error:", (abs(checkpoint-actual_value)/actual_value) * 100)

callback = load_predict("ModelFiles\\Callback.h5")
print("Callback  prediction:", callback)
print("Callback Error:", (abs(callback-actual_value)/actual_value) * 100)
