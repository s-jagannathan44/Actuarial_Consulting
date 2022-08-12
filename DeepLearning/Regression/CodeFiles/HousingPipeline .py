import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from scikeras.wrappers import KerasRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.compose import ColumnTransformer


def fetch_california_housing():
    cal_housing = np.loadtxt("california_housing_train.csv", delimiter=",")
    target, data = cal_housing[:, 8], cal_housing[:, 0:8]
    return data, target


X, Y = fetch_california_housing()


print(Y.shape)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size=0.8, random_state=123)

print(X_train.shape, X_test.shape, Y_train.shape, Y_test.shape, X_train.shape[1])
neural_regressor = Sequential(
    [
        Dense(26, activation="relu", input_shape=(10,)),
        Dense(52, activation="relu"),
        Dense(1)
    ]
)

# print(neural_regressor.summary())

scikeras_regressor = KerasRegressor(model=neural_regressor,
                                    optimizer="adam",
                                    loss="mean_squared_error",
                                    batch_size=32,
                                    epochs=100,
                                    verbose=0
                                    )

linear_model_preprocessor = ColumnTransformer(
    [
        ("binned_numeric", KBinsDiscretizer(n_bins=10), [4])
    ],
    remainder='drop'
    # remainder='passthrough'
)

ml_pipeline = Pipeline([("preprocessor", linear_model_preprocessor), ("Model", scikeras_regressor)])

ml_pipeline.fit(X_train, Y_train)

y_pred = ml_pipeline.predict(X_test)
np.savetxt("output.csv", y_pred, delimiter=',')
np.savetxt("Y_test.csv", Y_test, delimiter=',')
np.savetxt("X_test.csv", X_test, delimiter=',')
