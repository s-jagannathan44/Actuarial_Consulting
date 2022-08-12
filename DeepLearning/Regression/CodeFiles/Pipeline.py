import pandas as pd
# from keras.wrappers.scikit_learn import KerasRegressor
from scikeras.wrappers import KerasRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from keras.models import Sequential
from keras.layers import Dense


# create a function that returns a model, taking as parameters things you
# want to verify using cross-validation and model selection
def create_model():
    model = Sequential([
        Dense(32, activation='relu', kernel_initializer='he_normal', input_shape=(6,)),
        Dense(32, activation='relu', kernel_initializer='he_normal'),
        Dense(1),  # output layer with one node uses the default or linear activation function (no activation function).
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model


def build_model():
    linear_model_preprocessor = ColumnTransformer(
        [
           ("binned_numeric", KBinsDiscretizer(n_bins=10), ["VehicleValue"]),
            (
                "onehot_categorical",
                OneHotEncoder(),
                ["MaritalMainDriver", "GenderMainDriver"]
                #   ["GenderMainDriver", "MaritalMainDriver", "Make", "Use", "PaymentMethod", "PaymentFrequency"],
            ),
        ],
        remainder='drop'
        # remainder='passthrough'
    )

    pipeline = Pipeline(
        [
            ("preprocessor", linear_model_preprocessor),
            ("regressor", KerasRegressor(model=create_model, verbose=0)),
        ]
    )

    pipeline.fit(X_train, y_train,
                 regressor__batch_size=32, regressor__epochs=100,
                 regressor__validation_data=(X_test, y_test))

    return pipeline


df = pd.read_csv("onehot.csv")

# X is list of input features
X = df.iloc[:, 0:3]
# Y is label of what we want to predict
Y = df.iloc[:, 3:]
print(df.shape, X.shape, Y.shape)
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33)
pipe_line = build_model()
