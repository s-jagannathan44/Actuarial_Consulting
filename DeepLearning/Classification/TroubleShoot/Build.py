import sys


from sklearn.model_selection import train_test_split
from tensorflow import keras

sys.path.append("C:\\Actuarial Consulting\\Modules")
import Utilities


metrics = [
    keras.metrics.FalseNegatives(name="fn"),
    keras.metrics.FalsePositives(name="fp"),
    keras.metrics.TrueNegatives(name="tn"),
    keras.metrics.TruePositives(name="tp"),
    keras.metrics.Precision(name="precision"),
    keras.metrics.Recall(name="recall"),
]
passthrough_list = ["AnalysisPeriod", "NumberOfDrivers", "VoluntaryExcess", "NumberOfPastClaims",
                    "NumberOfPastConvictions", "ClaimLastYr"]
ordinal_list = ["GenderMainDriver", "GenderYoungestDriver", "MaritalMainDriver",
                "Make", "Use", "PaymentMethod", "PaymentFrequency", "BonusMalusProtection",
                "GenderYoungestAdditionalDriver", "VehFuel1"]
to_bin_list = [['AgeMainDriver', 4, 'uniform'], ['AgeYoungestDriver', 4, 'uniform'],
               ['AgeYoungestAdditionalDriver', 2, 'uniform'], ['VehicleAge', 2, 'uniform'],
               ['VehicleValue', 10, 'uniform'], ['VehicleMileage', 4, 'uniform'],
               ['BonusMalusYears', 4, 'quantile'], ['PolicyTenure', 3, 'quantile']]


X, y = Utilities.fetch_data("Output\\Input.csv", 39)
X = Utilities.impute_missing_values(X, "AgeYoungestAdditionalDriver")
X = Utilities.impute_missing_values(X, "GenderYoungestAdditionalDriver")

X = Utilities.transform(passthrough_list, to_bin_list, ordinal_list).fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=40)
print(X_train.shape, y_test.shape)

# model = Utilities.create_classifier_model(24, X_train, y_train, metrics)

# Utilities.load_predict("Output\\Checkpoint.h5", X)

