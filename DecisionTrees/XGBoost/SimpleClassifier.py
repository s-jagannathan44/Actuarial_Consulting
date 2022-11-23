# Generate and plot a synthetic imbalanced classification dataset
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from xgboost import XGBClassifier
from Modules import Utilities as Ut

passthrough_list = ["Age", "Deductible"]
ordinal_list = ["Sex", "Fault", "VehicleCategory", "PoliceReportFiled", "WitnessPresent",
                "AgentType", "BasePolicy"]
to_bin_list = []


def get_columns():
    columns = {}
    for encoder in transformer.named_transformers_:
        if type(transformer.named_transformers_[encoder]) != str:
            item = [(encoder, transformer.named_transformers_[encoder].get_feature_names_out().size)]
            columns.update(item)
    return columns


def write_output(X_value, actual_val, pred_val):
    frame_list = []
    res = []
    length = 0
    index = 0
    for item in column_dict:
        encoder = transformer.named_transformers_[item]
        size = column_dict[item]
        length = length + size
        if length == size:
            col = encoder.inverse_transform(X_value[:, :length])
        else:
            col = encoder.inverse_transform(X_value[:, index:length])
        frame = pd.DataFrame(col, columns=encoder.get_feature_names_out())
        frame_list.append(frame)
        index = length

    for frame in frame_list:
        res.append(frame)

    # axis 0 is rows and axis 1 is columns
    frame = pd.concat(res, axis=1)
    frame["Actual"] = actual_val.to_list()
    frame['Proba'] = pred_val
    frame["Predicted"] = y_pred
    frame.to_csv("Output\\Output.csv")


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
transformer = Ut.transform(passthrough_list, to_bin_list, ordinal_list)

X = df_.drop('FraudFound_P', axis=1)
y = df_["FraudFound_P"]

X = transformer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=25)

# define model
estimator_ = XGBClassifier()
estimator_.fit(X_train, y_train)
# estimator_ = gridsearch(estimator_)
y_pred = estimator_.predict(X_test)

y_pred_proba = estimator_.predict_proba(X_test)
column_dict = get_columns()
write_output(X_test, y_test, y_pred_proba[:, 1:])
