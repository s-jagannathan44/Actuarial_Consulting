import numpy as np
import pandas as pd
from keras.metrics import AUC
from matplotlib import pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from sklearn.preprocessing import OrdinalEncoder
from keras.callbacks import ModelCheckpoint, EarlyStopping
from Modules import Utilities as Ut


def plot_curve(epoch, his, list_of_metrics):
    """Plot a curve of one or more classification metrics vs. epoch."""
    # list_of_metrics should be one of the names shown in:
    # https://www.tensorflow.org/tutorials/structured_data/imbalanced_data#define_the_model_and_metrics

    plt.figure()
    plt.xlabel("Epoch")
    plt.ylabel("Value")
    for m in list_of_metrics:
        print(m)
        x = his['auc']
        plt.plot(epoch[1:], x[1:], label='AUC')
    plt.legend()
    plt.show()


def create_model():
    # Define the model
    model = Sequential([
        Dense(5, activation='relu', input_shape=(X_train.shape[1],)),
        Dense(10, activation='relu'),
        Dense(5, activation='relu'),
        Dense(1, activation="sigmoid"),
    ])
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=AUC(name='auc'))
    checkpoint = ModelCheckpoint(filepath="Output\\Checkpoint.h5", monitor="auc", verbose=1,
                                 save_best_only=True, mode="max")
    early_stopping = EarlyStopping(monitor="auc", min_delta=0.001, patience=5)
    history = model.fit(X_train, y_train, epochs=30, batch_size=500,
                        callbacks=[checkpoint, early_stopping])
    # The list of epochs is stored separately from the rest of history.
    epochs = history.epoch
    # Isolate the classification metric for each epoch.
    hist = pd.DataFrame(history.history)
    metric_list = ['auc']
    plot_curve(epochs, hist, metric_list)

    return model


df = pd.read_csv("Output\\Input_5.csv")
X = df.drop("Claim", axis=1)
y = df["Claim"]

transformer = ColumnTransformer(
    [
        (
            "onehot_categorical",
            OrdinalEncoder(),
            ["GenderMainDriver", "MaritalMainDriver",  "DrivingRestriction", "Make", "VehFuel1"],
        ),
    ],
    remainder='drop'
)

X = transformer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=40)

y_pred_ = create_model().predict(X_test)


X_test = transformer.named_transformers_['onehot_categorical'].inverse_transform(X_test)
frame = pd.DataFrame(X_test, columns=["GenderMainDriver", "MaritalMainDriver",  "DrivingRestriction",
                                      "Make", "VehFuel1"])

frame.to_csv("Output\\X_test.csv")
np.savetxt("Output\\y_test.csv", y_test, delimiter=",")
np.savetxt("Output\\y_pred.csv", y_pred_, delimiter=",")

columns_ = ["GenderMainDriver", "MaritalMainDriver",  "DrivingRestriction", "Make", "VehFuel1"]
levels_ = [0, 1, 2, 3, 4]
Ut.plot_scatter(columns_, levels_)
