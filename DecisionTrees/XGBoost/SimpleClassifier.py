# Generate and plot a synthetic imbalanced classification dataset
import pandas as pd
from matplotlib import pyplot as plt
from numpy import mean, sort
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import precision_score, recall_score, \
    ConfusionMatrixDisplay, f1_score
from sklearn.model_selection import train_test_split, RepeatedStratifiedKFold, GridSearchCV
from Modules import Utilities as Ut
from xgboost import XGBClassifier

# Make and Payment_frequency to go under One hot encoding
passthrough_list = ["AnalysisPeriod", "NumberOfDrivers", "VoluntaryExcess",
                    "NumberOfPastConvictions"]
ordinal_list = ["GenderMainDriver", "MaritalMainDriver",
                "Use", "PaymentMethod", "BonusMalusProtection",
                "GenderYoungestAdditionalDriver", "VehFuel1"]
to_bin_list = [['AgeMainDriver', 4, 'uniform'], ['AgeYoungestDriver', 4, 'uniform'],
               ['AgeYoungestAdditionalDriver', 2, 'uniform'], ['VehicleAge', 2, 'uniform'],
               ['VehicleValue', 10, 'uniform'], ['VehicleMileage', 4, 'uniform'],
               ['BonusMalusYears', 4, 'quantile'], ['PolicyTenure', 3, 'quantile']]


def data_analysis(df=None):
    for c in df.columns:
        csv_file_name = "Output\\Columns\\" + c.replace("/", "_") + ".csv"
        insight = df[c].value_counts()
        insight.to_csv(csv_file_name)
    df.describe(percentiles=[0.25, 0.5, 0.75, 0.85, 0.9, 0.98, 1]).to_csv("Output\\Columns\\desc.csv")


def select_features():
    threshold = sort(estimator_.feature_importances_)
    for thresh in threshold:
        # select features using threshold
        selection = SelectFromModel(estimator_, threshold=thresh, prefit=True)
        select_X_train = selection.transform(X_train)
        # train model
        selection_model = XGBClassifier(objective='binary:logistic', seed=42, base_score=0.05,
                                        learning_rate=0.01, max_depth=7, n_estimators=500, colsample_bytree=0.7,
                                        gamma=3, reg_alpha=10, reg_lambda=0.5, scale_pos_weight=35)
        selection_model.fit(select_X_train, y_train)
        # eval model
        select_X_test = selection.transform(X_test)
        y_pred_ = selection_model.predict(select_X_test)
        predictions = [round(value, ndigits=3) for value in y_pred_]
        f1_ = f1_score(y_test, predictions)
        print("Thresh=%.3f, n=%d, F1 score: %.3f" % (thresh, select_X_train.shape[1], f1_))


def gridsearch(rgr):
    param_grid = \
        {
            'learning_rate': [0.01, 0.05, 0.3, 0.5]
        }
    model = GridSearchCV(rgr, param_grid, cv=10, scoring="f1", refit=True, verbose=3, n_jobs=-1)
    model.fit(X_train, y_train)
    print(model.best_params_)
    return model.best_estimator_


# -------------------- CODE STARTS HERE ---------------------------------------
ord_col_size = ohe_col_size = 0
df_ = pd.read_csv("Output\\Policies.csv")
df_ = df_[df_["Use"] != "Business Use - Class 1"]
df_ = df_[df_["PaymentMethod"] != "Other"]

X = df_.drop('Claim Count', axis=1)
y = df_["Claim Count"]
X = Ut.impute_missing_values(X, "AgeYoungestAdditionalDriver")
X = Ut.impute_missing_values(X, "GenderYoungestAdditionalDriver")
transformer = Ut.transform(passthrough_list, to_bin_list, ordinal_list)
X = transformer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=25)

# define model
estimator_ = XGBClassifier(objective='binary:logistic', seed=42, base_score=0.05,
                           learning_rate=0.01, max_depth=7, n_estimators=500, colsample_bytree=0.7,
                           gamma=3, reg_alpha=10, reg_lambda=10, scale_pos_weight=35)
estimator_.fit(X_train, y_train)
# estimator_ = gridsearch(estimator_)
y_pred = estimator_.predict(X_test)

f1 = round(f1_score(y_test, y_pred), ndigits=3)
precision = round(precision_score(y_test, y_pred), ndigits=3)
recall = round(recall_score(y_test, y_pred), ndigits=3)

print("Model F1 : ", f1)
print('Precision on testing set:', precision)
print('Recall on testing set:', recall)

# plotting the confusion-matrix
ConfusionMatrixDisplay.from_predictions(y_test, y_pred)
plt.show()
# define evaluation procedure
cv = RepeatedStratifiedKFold(n_splits=3, n_repeats=5, random_state=1)

# evaluate model
scores = 0  # cross_val_score(estimator_, X_test, y_test, scoring='f1', cv=cv, n_jobs=-1, verbose=True)
# summarize performance
print('Mean f1: %.5f' % mean(scores))
# plot_importance(estimator_)

(pd.Series(estimator_.feature_importances_, index=[
    "AnalysisPeriod", "NumberOfDrivers", "VoluntaryExcess",
    "NumberOfPastConvictions",
    "AgeMainDriver", 'AgeYoungestDriver', 'AgeYoungestAdditionalDriver',
    'VehicleAge', 'VehicleValue', 'VehicleMileage', 'BonusMalusYears',
    'PolicyTenure', "GenderMainDriver",
    "MaritalMainDriver", "Use", "PaymentMethod", "BonusMalusProtection",
    "GenderYoungestAdditionalDriver", "VehFuel1"])
 .nlargest(19)
 .plot(kind='barh'))
select_features()
plt.show()
