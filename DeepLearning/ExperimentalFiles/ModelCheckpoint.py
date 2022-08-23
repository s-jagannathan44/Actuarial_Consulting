import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from sklearn.preprocessing import KBinsDiscretizer, OrdinalEncoder
from keras.callbacks import CSVLogger, ModelCheckpoint


def my_loss(y_true, y_pred):
    actual = float(y_true)
    predicted = float(y_pred)
    loss = actual - predicted
    return abs(loss)


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
    csv_logger = CSVLogger('training.log')
    checkpoint = ModelCheckpoint(filepath="Output\\Checkpoint.h5", monitor="my_loss", verbose=1,
                                 save_best_only=True, mode="min")
    model.fit(X_train, y_train, epochs=200, batch_size=100,
              callbacks=[checkpoint, csv_logger])
    return model


df = pd.read_csv("Output\\Input.csv")
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

y_pred_ = np.sum(create_model().predict(X_test))
print(y_pred_)
