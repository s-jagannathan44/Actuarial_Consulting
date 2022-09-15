import numpy as np
import pandas as pd
from keras.metrics import Poisson
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from tensorflow.python.keras.models import load_model

import Modules.Utilities as Ut


def build_predict():
    my_model = Ut.create_model(X_train.shape[1], X_train, y_train, [Poisson(name="poisson")])

    y_pred = my_model.predict(X_test)
    actual = np.sum(y_test)
    predicted = np.sum(y_pred)
    error = 1 - (predicted / actual)
    print("error", float(error) * 100)
    return y_pred


def predict():
    my_model = load_model("Output\\Freq.h5")
    my_model.compile(optimizer='sgd', loss="poisson")
    y_pred = my_model.predict(X)
    actual = np.sum(y)
    predicted = np.sum(y_pred)
    error = 1 - (predicted / actual)
    print("error", float(error) * 100)
    return y_pred


df = pd.read_csv("Output\\Input_4.csv")
X = df.drop("Claim", axis=1)
y = df["Claim"]

transformer = ColumnTransformer(
    [
        (
            "onehot_categorical",
            OrdinalEncoder(),
            ["GenderMainDriver", "MaritalMainDriver", "DrivingRestriction", "Make", "VehFuel1"],
        ),
    ],
    remainder='drop'
)

X = transformer.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=40)
y_pred_ = build_predict()

# y_pred_ = predict()

X_test = transformer.named_transformers_['onehot_categorical'].inverse_transform(X_test)
frame = pd.DataFrame(X_test, columns=["Gender", "MaritalMainDriver", "DrivingRestriction", "Make", "VehFuel1"])

frame.to_csv("Output\\X_test.csv")
np.savetxt("Output\\y_test.csv", y_test, delimiter=",")
np.savetxt("Output\\y_pred.csv", y_pred_, delimiter=",")

columns_ = ['Gender', 'MaritalMainDriver', 'DrivingRestriction', "Make", 'VehFuel1']
levels_ = [0, 1, 2, 3, 4]
Ut.plot_scatter(columns_, levels_)
