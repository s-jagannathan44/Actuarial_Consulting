import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from sklearn.preprocessing import KBinsDiscretizer, OrdinalEncoder


def my_loss(y_true, y_pred):
    return y_pred


def create_model():
    # Define the model
    model = Sequential([
        Dense(500, activation='relu', input_shape=(7,)),
        Dense(100, activation='relu'),
        Dense(50, activation='relu'),
        Dense(1, activation="sigmoid"),
    ])

    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=my_loss)
    model.fit(X_train, y_train, epochs=200, batch_size=100)
    return model


df = pd.read_csv("Input.csv")
X = df.iloc[:, :39]
y = df.iloc[:, 39:]

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
print(np.sum(y))
X = transformer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=40)
print(np.sum(y_test))
print(create_model().evaluate(X_test, y_test))
