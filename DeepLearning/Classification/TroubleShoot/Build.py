import Modules.Utilities
import numpy as np
from keras.metrics import FalseNegatives, FalsePositives, TrueNegatives, TruePositives, Precision, Recall
from sklearn.model_selection import train_test_split

X, y = Modules.Utilities.fetch_data("Output\\Input.csv", 39)
# X = Utilities.impute_missing_values(X, "AgeYoungestAdditionalDriver")
# X = Utilities.impute_missing_values(X, "GenderYoungestAdditionalDriver")

passthrough_list = []
ordinal_list = ["GenderMainDriver", "MaritalMainDriver", "Make", "Use", "VehFuel1"]
to_bin_list = []

X = Modules.Utilities.transform(passthrough_list, to_bin_list, ordinal_list).fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=40)
print("Number of training samples:", X_train.shape[0])

"""
## Analyze class imbalance in the targets
"""

counts = np.bincount(y_train.iloc[:, 0])
print(
    "Number of positive samples in training data: {} ({:.2f}% of total)".format(
        counts[1], 100 * float(counts[1]) / len(y_train)
    )
)


metrics = [
    FalseNegatives(name="fn"),
    FalsePositives(name="fp"),
    TrueNegatives(name="tn"),
    TruePositives(name="tp"),
    Precision(name="precision"),
    Recall(name="recall"),
]
model = Modules.Utilities.create_classifier_model(X_train.shape[1], X_train, y_train, metrics)


'''
passthrough_list = ["AnalysisPeriod", "NumberOfDrivers", "VoluntaryExcess", "NumberOfPastClaims",
                    "NumberOfPastConvictions", "ClaimLastYr"]
ordinal_list = ["GenderMainDriver", "GenderYoungestDriver", "MaritalMainDriver",
                "Make", "Use", "PaymentMethod", "PaymentFrequency", "BonusMalusProtection",
                "GenderYoungestAdditionalDriver", "VehFuel1"]
to_bin_list = [['AgeMainDriver', 4, 'uniform'], ['AgeYoungestDriver', 4, 'uniform'],
               ['AgeYoungestAdditionalDriver', 2, 'uniform'], ['VehicleAge', 2, 'uniform'],
               ['VehicleValue', 10, 'uniform'], ['VehicleMileage', 4, 'uniform'],
               ['BonusMalusYears', 4, 'quantile'], ['PolicyTenure', 3, 'quantile']]
'''