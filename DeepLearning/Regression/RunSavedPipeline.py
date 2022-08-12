import joblib
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from scikeras.wrappers import KerasRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from tensorflow import keras


def fetch_severity():
    df = pd.read_csv("Policies.csv")
    print(df.shape)
    df.set_index("PolicyReference", inplace=True, drop=True)
    df.dropna(how="all", axis=1)

    # X is list of input features
    data = df.iloc[:, 0:40]
    # Y is label of what we want to predict
    target = df.iloc[:, 40:]

    return data, target


def build_model():
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size=0.67, random_state=123)
    print(X_train.shape, X_test.shape, Y_train.shape, Y_test.shape)

    neural_regressor = Sequential(
        [
            Dense(26, activation="relu", input_shape=(65,)),
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

    linear_model_preprocessor2 = ColumnTransformer(
        [
            ("binned_numeric", KBinsDiscretizer(n_bins=10), ["VehicleValue"]),
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

    save_pipeline(scikeras_regressor, ml_pipeline)
    return ml_pipeline


def save_pipeline(scikeras_regressor, ml_pipeline):
    # Save the Keras model first:
    scikeras_regressor.model.save("keras_regressor")
    # This hack allows us to save the sklearn pipeline:
    ml_pipeline.named_steps['Model'].model = None
    # Finally, save the pipeline:
    joblib.dump(ml_pipeline, 'sklearn_pipeline.pkl')


def execute_model():
    # Load the pipeline first:
    saved_pipeline = joblib.load('sklearn_pipeline.pkl')
    # Then, load the Keras model:
    saved_pipeline.named_steps['Model'].model = keras.models.load_model("keras_regressor")
    y_pred = saved_pipeline.predict(X)
    np.savetxt("output.csv", y_pred, delimiter=',')
    np.savetxt("Y_test.csv", Y, delimiter=',')


X, Y = fetch_severity()
# build_model()
execute_model()
