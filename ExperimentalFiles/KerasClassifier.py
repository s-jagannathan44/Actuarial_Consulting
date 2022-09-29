import numpy as np
import pandas as pd
from scikeras.wrappers import KerasClassifier
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from sklearn.preprocessing import KBinsDiscretizer, OrdinalEncoder


def create_model():
    # Define the model
    model = Sequential([
        Dense(500, activation='relu', input_shape=(7,)),
        Dense(100, activation='relu'),
        Dense(50, activation='relu'),
        Dense(1, activation="sigmoid"),
    ])

    model.compile(optimizer='adam',
                  loss='binary_crossentropy')
    return model


df = pd.read_csv("Base_File.csv")
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

X = transformer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=40)
estimator = KerasClassifier(model=create_model, batch_size=100, epochs=200, verbose=0)
# np.savetxt("train.csv", X_train, delimiter=",")
estimator.fit(X_train, y_train)
print(sum(estimator.predict(X_test)))
print(np.sum(y_test))
