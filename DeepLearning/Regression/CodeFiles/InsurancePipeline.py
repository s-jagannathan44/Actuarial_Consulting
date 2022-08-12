import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from scikeras.wrappers import KerasRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import KBinsDiscretizer, FunctionTransformer, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from tensorflow import keras


def fetch_severity():
    df = pd.read_csv("insurance.csv")
    print(df.shape)
    df.set_index("PolicyReference", inplace=True, drop=True)
    df.loc[(df["Claim"] == 0) & (df["Claim Count"] >= 1), "Claim Count"] = 0
    # Note: filter out policies with zero claims
    df = df[df["Claim Count"] >= 1]
    df.dropna(how="all", axis=1)

    # X is list of input features
    data = df.iloc[:, 0:42]
    # Y is label of what we want to predict
    target = df.iloc[:, 42:]

    return data, target


def build_model():
    neural_regressor = Sequential(
        [
            Dense(26, activation="relu", input_shape=(67,)),
            Dense(52, activation="relu"),
            Dense(1)
        ]
    )

    scikeras_regressor = KerasRegressor(model=neural_regressor,
                                        optimizer="adam",
                                        loss="mean_squared_error",
                                        batch_size=32,
                                        epochs=100,
                                        verbose=0
                                        )
    log_scale_transformer2 = make_pipeline(
        FunctionTransformer(np.log, validate=False), StandardScaler()
    )
    linear_model_preprocessor2 = ColumnTransformer(
        [
            ("binned_numeric", KBinsDiscretizer(n_bins=10), ["VehicleValue"]),
            ("passthrough_numeric", "passthrough", ["Claim Count"]),
            ("log_scaled_numeric", log_scale_transformer2, ["Claim"]),
            (
                "onehot_categorical",
                OneHotEncoder(),
                ["GenderMainDriver", "MaritalMainDriver", "Make", "Use", "PaymentMethod", "PaymentFrequency"],
            ),
        ],
        remainder='drop'
        # remainder='passthrough'
    )

    ml_pipeline = Pipeline([("preprocessor", linear_model_preprocessor2), ("Model", scikeras_regressor)])
    ml_pipeline.fit(X_train, Y_train)
    scikeras_regressor.model.save("keras_regressor")
    return ml_pipeline


X, Y = fetch_severity()

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size=0.67, random_state=123)

print(X_train.shape, X_test.shape, Y_train.shape, Y_test.shape)

X_train.to_csv("X.csv")
Y_train.to_csv("Y.csv")

pipeline = build_model()


y_pred = pipeline.predict(X_test)
np.savetxt("output.csv", y_pred, delimiter=',')
np.savetxt("Y_test.csv", Y_test, delimiter=',')

