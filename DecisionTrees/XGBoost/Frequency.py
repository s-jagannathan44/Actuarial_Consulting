import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from numpy import sort
from sklearn.feature_selection import SelectFromModel
# from sklearn.metrics import get_scorer_names
from sklearn.model_selection import train_test_split, GridSearchCV
from xgboost import XGBRegressor
import Modules.Utilities as Ut

# Make and Payment_frequency to go under One hot encoding
passthrough_list = ["AnalysisPeriod", "NumberOfDrivers", "VoluntaryExcess",
                    "NumberOfPastConvictions"]
ordinal_list = ["GenderMainDriver", "GenderYoungestDriver", "MaritalMainDriver",
                "Use", "PaymentMethod",
                "GenderYoungestAdditionalDriver"]
to_bin_list = [['AgeMainDriver', 4, 'uniform'], ['AgeYoungestDriver', 4, 'uniform'],
               ['AgeYoungestAdditionalDriver', 2, 'uniform'], ['VehicleAge', 2, 'uniform'],
               ['VehicleValue', 10, 'uniform'], ['VehicleMileage', 4, 'uniform'],
               ['BonusMalusYears', 4, 'quantile'], ['PolicyTenure', 3, 'quantile']]


def data_analysis():
    for c in df.columns:
        csv_file_name = "Output\\Columns\\" + c.replace("/", "_") + ".csv"
        insight = df[c].value_counts()
        insight.to_csv(csv_file_name)
    df.describe(percentiles=[0.25, 0.5, 0.75, 0.85, 0.9, 0.98, 1]).to_csv("Output\\Columns\\desc.csv")


def select_features():
    thresholds = sort(rgr.feature_importances_)
    for thresh in thresholds:
        # select features using threshold
        selection = SelectFromModel(rgr, threshold=thresh, prefit=True)
        select_X_train = selection.transform(X_train)
        # train model
        selection_model = XGBRegressor(objective='count:poisson', seed=42, n_estimators=300, max_depth=7,
                                       learning_rate=0.1, colsample_bytree=0.6)
        selection_model.fit(select_X_train, y_train)
        # eval model
        select_X_test = selection.transform(X_test)
        predictions = selection_model.predict(select_X_test)
        print("Thresh=%.3f, n=%d, Accuracy: " % (thresh, select_X_train.shape[1]))
        predict_output(y_test, predictions)


def get_columns():
    columns = {}
    for encoder in transformer.named_transformers_:
        if type(transformer.named_transformers_[encoder]) != str:
            item = [(encoder, transformer.named_transformers_[encoder].get_feature_names_out().size)]
            columns.update(item)
    return columns


def write_output(X_val, actual_val, pred_val):
    frame_list = []
    res = []
    length = 0
    index = 0
    for item in column_dict:
        encoder = transformer.named_transformers_[item]
        size = column_dict[item]
        length = length + size
        if length == size:
            col = encoder.inverse_transform(X_val[:, :length])
        else:
            col = encoder.inverse_transform(X_val[:, index:length])
        frame = pd.DataFrame(col, columns=encoder.get_feature_names_out())
        frame_list.append(frame)
        index = length

    for frame in frame_list:
        res.append(frame)

    # axis 0 is rows and axis 1 is columns
    frame = pd.concat(res, axis=1)
    frame["Actual"] = actual_val.to_list()
    frame['Predicted'] = pred_val
    # frame["Exposure"] = test_exposure
    frame.to_csv("Output\\Output.csv")


def predict_output(actual_val, pred_val):
    actual = np.sum(actual_val)
    predicted = np.sum(pred_val)
    error = 1 - (predicted / actual)
    print("error", float(error) * 100)
    print("predicted", float(predicted))


def gridsearch(estimator):
    param_grid = \
        {

        }
    model = GridSearchCV(estimator, param_grid, cv=10, scoring="neg_mean_poisson_deviance", refit=True,
                         verbose=3, n_jobs=-1)
    model.fit(X_train, y_train)
    print(model.best_params_)
    return model.best_estimator_


# -------------------- CODE STARTS HERE ---------------------------------------
# print(get_scorer_names())
df = pd.read_csv("Output\\pivot2.csv")
X = df.drop('Claim Count', axis=1)
y = df["Claim Count"]

transformer = Ut.transform(passthrough_list, to_bin_list, ordinal_list)
X = transformer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=40)
rgr = XGBRegressor(objective='count:poisson', seed=42, n_estimators=300, max_depth=7, learning_rate=0.1,
                   colsample_bytree=0.6)
# rgr = gridsearch(rgr)
rgr.fit(X_train, y_train)
y_pred = rgr.predict(X_test)
column_dict = get_columns()
write_output(X_test, y_test, y_pred)

(pd.Series(rgr.feature_importances_, index=["AnalysisPeriod", "NumberOfDrivers", "VoluntaryExcess",
                                            "NumberOfPastConvictions",
                                            "AgeMainDriver", 'AgeYoungestDriver', 'AgeYoungestAdditionalDriver',
                                            'VehicleAge', 'VehicleValue', 'VehicleMileage', 'BonusMalusYears',
                                            'PolicyTenure', "GenderMainDriver", "GenderYoungestDriver",
                                            "MaritalMainDriver", "Use", "PaymentMethod",
                                            "GenderYoungestAdditionalDriver"])
 .nlargest(18)
 .plot(kind='barh'))
select_features()
plt.show()
