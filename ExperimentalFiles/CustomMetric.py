import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from sklearn.preprocessing import KBinsDiscretizer, OrdinalEncoder
from keras.callbacks import Callback, CSVLogger


def my_loss(y_true, y_pred):
    actual = float(y_true)
    predicted = float(y_pred)
    loss = actual - predicted
    return loss


class EarlyStoppingAtMinLoss(Callback):
    """Stop training when the loss is at its min, i.e. the loss stops decreasing.

  Arguments:
      patience: Number of epochs to wait after min has been hit. After this
      number of no improvement, training stops.
  """

    def __init__(self, patience=0):
        super(EarlyStoppingAtMinLoss, self).__init__()
        self.wait = None
        self.patience = patience
        self.best = None
        self.stopped_epoch = None
        # best_weights to store the weights at which the minimum loss occurs.
        self.best_weights = None

    def on_train_begin(self, logs=None):
        # The number of epoch it has waited when loss is no longer minimum.
        self.wait = 0
        # The epoch the training stops at.
        self.stopped_epoch = 0
        # Initialize the best as infinity.
        self.best = np.Inf

    def on_epoch_end(self, epoch, logs=None):
        current = abs(logs.get("my_loss"))
        loss_percentage = (current / actual_chance) * 100
        if np.less(current, self.best):
            self.best = current
            self.wait = 0
            # Record the best weights if current results is better (less).
            self.best_weights = self.model.get_weights()
        else:
            self.wait += 1
            # if self.wait >= self.patience or abs(loss_percentage) < 1:
            if abs(loss_percentage) < 1:
                value = logs.get("my_loss") + actual_chance
                pred = value * total_count
                self.stopped_epoch = epoch
                self.model.stop_training = True
                print("Restoring model weights from the end of the best epoch.")
                print(pred, float(current), loss_percentage)
                self.model.set_weights(self.best_weights)
                self.model.save("Output\\Callback_All.h5")

    def on_train_end(self, logs=None):
        if self.stopped_epoch > 0:
            print("Epoch %05d: early stopping" % (self.stopped_epoch + 1))


def create_model():
    # Define the model
    model = Sequential([
        Dense(500, activation='relu', input_shape=(24,)),
        Dense(100, activation='relu'),
        Dense(50, activation='relu'),
        Dense(1, activation="sigmoid"),
    ])

    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=my_loss)
    csv_logger = CSVLogger('Output\\training.log')
    model.fit(X_train, y_train, epochs=200, batch_size=100,
              callbacks=[EarlyStoppingAtMinLoss(patience=2), csv_logger])
    return model


def impute_missing_values(column_name):
    imp_mean = SimpleImputer(missing_values=-1, strategy='most_frequent')
    df.loc[df[column_name].isnull(), column_name] = -1
    column_values = np.asarray(df[column_name]).reshape(-1, 1)
    df[column_name] = imp_mean.fit_transform(column_values)


def transform():
    return ColumnTransformer(
        [
            ("passthrough_1", "passthrough", ["AnalysisPeriod"]),
            ("passthrough_8", "passthrough", ["NumberOfDrivers"]),
            ("passthrough_14", "passthrough", ["VoluntaryExcess"]),
            ("passthrough_17", "passthrough", ["NumberOfPastClaims"]),
            ("passthrough_18", "passthrough", ["NumberOfPastConvictions"]),
            ("passthrough_24", "passthrough", ["ClaimLastYr"]),
            ("binned_2", KBinsDiscretizer(n_bins=4, encode='ordinal', strategy='quantile'), ["AgeMainDriver"]),
            ("binned_3", KBinsDiscretizer(n_bins=4, encode='ordinal', strategy='quantile'), ["AgeYoungestDriver"]),
            ("binned_4", KBinsDiscretizer(n_bins=2, encode='ordinal', strategy='quantile'),
             ["AgeYoungestAdditionalDriver"]),
            ("binned_9", KBinsDiscretizer(n_bins=2, encode='ordinal', strategy='quantile'), ["VehicleAge"]),
            ("binned_11", KBinsDiscretizer(n_bins=10, encode='ordinal', strategy='quantile'), ["VehicleValue"]),
            ("binned_13", KBinsDiscretizer(n_bins=4, encode='ordinal', strategy='quantile'), ["VehicleMileage"]),
            ("binned_15", KBinsDiscretizer(n_bins=4, encode='ordinal', strategy='quantile'), ["BonusMalusYears"]),
            ("binned_19", KBinsDiscretizer(n_bins=3, encode='ordinal', strategy='quantile'), ["PolicyTenure"]),
            (
                "onehot_categorical",
                OrdinalEncoder(),
                ["GenderMainDriver", "GenderYoungestDriver",  "MaritalMainDriver",
                 "Make", "Use", "PaymentMethod", "PaymentFrequency", "BonusMalusProtection",
                 "GenderYoungestAdditionalDriver", "VehFuel1"],
            ),
        ],
        remainder='drop'
    )


df = pd.read_csv("Output\\Input.csv")
impute_missing_values("AgeYoungestAdditionalDriver")
impute_missing_values("GenderYoungestAdditionalDriver")
X = df.iloc[:, :39]
y = df.iloc[:, 39:]

X = transform().fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=40)
actual_count = np.sum(y_test)
total_count = np.size(y_test)
actual_chance = float(actual_count / total_count)

y_pred_ = np.sum(create_model().predict(X_test))
print(y_pred_)
