import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split, GridSearchCV
from Modules import Utilities as Ut

ordinal_list = ["NAME_CONTRACT_TYPE", "CODE_GENDER", "FLAG_OWN_CAR", "FLAG_OWN_REALTY", "NAME_INCOME_TYPE",
                "NAME_EDUCATION_TYPE", "OCCUPATION_TYPE", "NAME_FAMILY_STATUS", "NAME_HOUSING_TYPE",
                "REGION_RATING_CLIENT"]
scaler_list = ["AMT_INCOME_TOTAL", "AMT_CREDIT", "CNT_CHILDREN", "REGION_POPULATION_RELATIVE",
               "DAYS_BIRTH", "DAYS_EMPLOYED"]
to_bin_list = [['AMT_INCOME_TOTAL', 4, 'uniform'],
               ['AMT_CREDIT', 4, 'uniform']]


def data_analysis():
    df = pd.read_csv('Output\\application_data.csv')
    for c in df.columns:
        csv_file_name = "Output\\Columns\\" + c.replace("/", "_") + ".csv"
        insight = df[c].value_counts()
        insight.to_csv(csv_file_name)
    df.describe(percentiles=[0.25, 0.5, 0.75, 0.85, 0.9, 0.98, 1]).to_csv("Output\\Columns\\desc.csv")


def data_modification():
    df = pd.read_csv('Output\\Credit.csv')
    df = df.replace({'NAME_FAMILY_STATUS': {'Civil marriage': 'Single / not married'}})
    df = df.replace({'NAME_INCOME_TYPE': {'State servant': 'Pensioner'}})
    df = df.replace({'NAME_HOUSING_TYPE': {'Co-op apartment': 'House / apartment'}})
    df = df.replace({'OCCUPATION_TYPE': {'IT staff': 'Core staff', 'HR staff': 'Core staff',
                                         'Managers': 'Core staff',
                                         'High skill tech staff': 'Core staff'
                                         }})
    df = df.replace({'OCCUPATION_TYPE': {'Cooking staff': 'Laborers', 'Security staff': 'Laborers'}})
    df = df.replace({'OCCUPATION_TYPE': {'Waiters/barmen staff': 'Drivers'}})
    df = df.replace({'OCCUPATION_TYPE': {'Medicine staff': 'Private service staff',
                                         'Secretaries': 'Private service staff'}})
    df = df.replace({'OCCUPATION_TYPE': {'Cleaning staff': 'Sales staff', }})

    df["AMT_INCOME_TOTAL"] = df["AMT_INCOME_TOTAL"].clip(upper=420000)
    df["AMT_INCOME_TOTAL"] = df["AMT_INCOME_TOTAL"].clip(lower=55000)
    df["AMT_CREDIT"] = df["AMT_CREDIT"].clip(upper=2000000)
    df["AMT_CREDIT"] = df["AMT_CREDIT"].clip(lower=100000)
    df["AMT_ANNUITY"] = df["AMT_ANNUITY"].clip(lower=65000)
    df["AMT_ANNUITY"] = df["AMT_ANNUITY"].clip(upper=6500)
    df["CNT_CHILDREN"] = df["CNT_CHILDREN"].clip(upper=2)
    df["REGION_POPULATION_RELATIVE"] = df["REGION_POPULATION_RELATIVE"].clip(lower=.002)

    return df


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
    frame['Predicted'] = pred_val
    frame['Predicted'].replace({1: 0, -1: 1}, inplace=True)
    frame.to_csv("Output\\Output.csv")


def gridsearch(rgr):
    param_grid = \
        {
            'contamination': [0.05, 0.1, 0.075, 0.0807]
        }
    model = GridSearchCV(rgr, param_grid, cv=10, scoring="f1_macro", refit=True, verbose=3, n_jobs=-1)
    model.fit(X_train, y_train)
    print(model.best_params_)
    return model.best_estimator_


# -------------------- CODE STARTS HERE ---------------------------------------
df_ = data_modification()
df_ = Ut.impute_missing_values(df_, "OCCUPATION_TYPE")
# df_.to_csv("Output\\Df.csv")
X = df_.drop('TARGET', axis=1)
y = df_["TARGET"]
transformer = Ut.transform([], to_bin_list, ["CODE_GENDER", "NAME_EDUCATION_TYPE", "OCCUPATION_TYPE"])
X = transformer.fit_transform(X)

# frame_ = pd.DataFrame(X, columns=["Income", "Credit", "Gender", "Education", "Occupation"])
# frame_["Actual"] = y.to_list()
# frame_.to_csv("Output\\Input.csv")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=X[:, 2:4], random_state=25)

# define model
# IsolationForest(n_estimators=500, n_jobs=-1, contamination=0.1, random_state=7, max_samples=0.25)
estimator_ = IsolationForest(n_estimators=500, random_state=7, n_jobs=-1, max_samples="auto", contamination=0.0807,
                             max_features=1)
# estimator_ = gridsearch(estimator_)
estimator_.fit(X_train)
y_pred = estimator_.predict(X_test)
# estimator_ = XGBClassifier()
# estimator_.fit(X_train, y_train)
# y_pred = estimator_.predict_proba(X_test)
column_dict = get_columns()
write_output(X_test, y_test, y_pred)
