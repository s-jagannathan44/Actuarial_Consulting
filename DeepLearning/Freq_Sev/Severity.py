import numpy as np
from keras.optimizers import SGD
from sklearn.metrics import mean_absolute_error
from tensorflow import keras

import Modules.Utilities as Ut
from sklearn.model_selection import train_test_split
import pandas as pd
from keras.metrics import MeanAbsoluteError


def data_verification():
    # Step 6 Check if the proportion of train set to test set is indeed 80:20
    global X_train, X_test
    print("train %age ", len(X_train) / len(X))
    print("test %age ", len(X_test) / len(X))
    # Step 7 check if the average claims amounts are similar between train set and test set.
    # They should be very similar, otherwise that means group shuffle has not been done appropriately.
    print("training Claim average", y_train.mean())
    print("test Claim average", y_test.mean())


# Step 1 read File
sev = pd.read_csv('Output\\Policies.csv')

sev = sev[sev["Claim"] > 0]
X = sev.drop("Claim", axis=1)
y = sev["Claim"]

passthrough_list = ["AnalysisPeriod", "NumberOfDrivers", "VoluntaryExcess", "NumberOfPastClaims",
                    "NumberOfPastConvictions", "ClaimLastYr"]
ordinal_list = ["GenderMainDriver", "GenderYoungestDriver", "MaritalMainDriver",
                "Make", "Use", "PaymentMethod", "PaymentFrequency", "BonusMalusProtection",
                "GenderYoungestAdditionalDriver", "VehFuel1"]
to_bin_list = [['AgeMainDriver', 4, 'uniform'], ['AgeYoungestDriver', 4, 'uniform'],
               ['AgeYoungestAdditionalDriver', 2, 'uniform'], ['VehicleAge', 2, 'uniform'],
               ['VehicleValue', 10, 'uniform'], ['VehicleMileage', 4, 'uniform'],
               ['BonusMalusYears', 4, 'quantile'], ['PolicyTenure', 3, 'quantile']]

X = Ut.impute_missing_values(X, "AgeYoungestAdditionalDriver")
X = Ut.impute_missing_values(X, "GenderYoungestAdditionalDriver")

X = Ut.transform(passthrough_list, to_bin_list, ordinal_list).fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=40)

data_verification()


metrics = [
    MeanAbsoluteError(name="mean_absolute_error")]

Ut.create_severity_model(X_train.shape[1], X_train, y_train, metrics)
my_model = keras.models.load_model("Output\\Severity.h5")
my_model.compile(optimizer=SGD(learning_rate=0.01, momentum=0.1), loss="mean_absolute_error", metrics=metrics)


y_pred = my_model.predict(X)
np.savetxt("Output\\y_pred.csv", y_pred, delimiter=",")
actual = np.sum(y)
predicted = np.sum(y_pred)

error = 1 - (predicted / actual)
print("error", float(error) * 100)
print("MAE", mean_absolute_error(y, y_pred))

