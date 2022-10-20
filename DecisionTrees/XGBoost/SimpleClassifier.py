# Generate and plot a synthetic imbalanced classification dataset
from collections import Counter
import pandas as pd
from sklearn.compose import ColumnTransformer
from matplotlib import pyplot as plt
from numpy import mean, sort
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import precision_score, recall_score, \
    ConfusionMatrixDisplay, f1_score
from sklearn.model_selection import train_test_split, RepeatedStratifiedKFold, GridSearchCV
from sklearn.preprocessing import OrdinalEncoder
from xgboost import XGBClassifier

ordinal_columns = ["Sex", "Fault", "VehicleCategory", "PoliceReportFiled", "WitnessPresent",
                   "AgentType", "BasePolicy"]


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
        selection_model = XGBClassifier(scale_pos_weight=Counter(y_train)[0] / Counter(y_train)[1])
        selection_model.fit(select_X_train, y_train)
        # eval model
        select_X_test = selection.transform(X_test)
        y_pred_ = selection_model.predict(select_X_test)
        predictions = [round(value, ndigits=2) for value in y_pred_]
        f1_ = f1_score(y_test, predictions)
        print("Thresh=%.3f, n=%d, F1 score: %.2f" % (thresh, select_X_train.shape[1], f1_))


def get_transformer():
    ordinal_tuple = ("ordinal", OrdinalEncoder(), ordinal_columns)
    transformer_ = ColumnTransformer(
        [("passthrough_n", "passthrough", ["Age", "Deductible"]),
         ordinal_tuple], remainder='drop')
    return transformer_


def gridsearch(rgr):
    param_grid = \
        {

        }
    model = GridSearchCV(rgr, param_grid, cv=10, scoring="f1", refit=True, verbose=3, n_jobs=-1)
    model.fit(X_train, y_train)
    print(model.best_params_)
    return model.best_estimator_


ord_col_size = ohe_col_size = 0
df_ = pd.read_csv("Output\\fraud_oracle.csv")
transformer = get_transformer()

X = df_.drop('FraudFound_P', axis=1)
y = df_["FraudFound_P"]

X = transformer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=25)

# define model
estimator_ = XGBClassifier(objective='binary:logistic', seed=42, base_score=0.05,
                           max_depth=3, n_estimators=200, colsample_bytree=0.8,
                           reg_lambda=10, scale_pos_weight=10)
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
# define evaluation procedure
cv = RepeatedStratifiedKFold(n_splits=3, n_repeats=5, random_state=1)

# evaluate model
scores = 0  # cross_val_score(estimator_, X_test, y_test, scoring='f1', cv=cv, n_jobs=-1, verbose=True)
# summarize performance
print('Mean f1: %.5f' % mean(scores))
# plot_importance(model)
# select_features()
plt.show()
