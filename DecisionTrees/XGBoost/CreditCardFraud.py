import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from Modules import Utilities as Ut

ordinal_list = ["NAME_CONTRACT_TYPE", "CODE_GENDER", "FLAG_OWN_CAR", "FLAG_OWN_REALTY", "NAME_INCOME_TYPE",
                "NAME_EDUCATION_TYPE", "NAME_FAMILY_STATUS", "NAME_HOUSING_TYPE", "OCCUPATION_TYPE"]


def data_analysis():
    df = pd.read_csv('Output\\application_data.csv')
    for c in df.columns:
        csv_file_name = "Output\\Columns\\" + c.replace("/", "_") + ".csv"
        insight = df[c].value_counts()
        insight.to_csv(csv_file_name)
    df.describe(percentiles=[0.25, 0.5, 0.75, 0.85, 0.9, 0.98, 1]).to_csv("Output\\Columns\\desc.csv")


def data_modification():
    df = pd.read_csv('Output\\Credit.csv')
    df = df.replace({'NAME_FAMILY_STATUS': {'Widow': 'Married', 'Seperated': 'Married'}})
    df.loc[df['NAME_HOUSING_TYPE'] != 'House / apartment', 'NAME_HOUSING_TYPE'] = 'Others'
    df = df.replace({'OCCUPATION_TYPE': {'IT staff': 'High skill tech staff', 'HR staff': 'High skill tech staff',
                                         'Realty agents': 'High skill tech staff',
                                         'Secretaries': 'High skill tech staff',
                                         'Medicine staff': 'High skill tech staff',
                                         'Private service staff': 'High skill tech staff',
                                         }})
    df = df.replace({'OCCUPATION_TYPE': {'Waiters/barmen staff': 'Drivers', 'Cooking staff': 'Drivers',
                                         'Cleaning staff': 'Drivers', 'Security staff': 'Drivers',
                                         }})
    df = df.replace({'OCCUPATION_TYPE': {'Low-skill Laborers': ''}})
    df.to_csv("Output\\credit_input.csv")


def data_level2_modification():
    df = pd.read_csv('Output\\credit_input.csv')
    df = df.replace({'NAME_FAMILY_STATUS': {'Civil marriage': 'Single / not married'}})
    df = df.replace({'NAME_INCOME_TYPE': {'State servant': 'Pensioner'}})
    df = df.replace({'OCCUPATION_TYPE': {'Managers': 'Core staff', 'High skill tech staff': 'Core staff'}})
    df = df.replace({'OCCUPATION_TYPE': {'Drivers': 'Laborers'}})
    df.to_csv("Output\\credit_data.csv")


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
    frame.to_csv("Output\\Output.csv")


df_ = pd.read_csv('Output\\credit_data.csv')
df_["AMT_INCOME_TOTAL"] = df_["AMT_INCOME_TOTAL"].clip(upper=420000)
df_["AMT_INCOME_TOTAL"] = df_["AMT_INCOME_TOTAL"].clip(lower=55000)
df_["AMT_CREDIT"] = df_["AMT_CREDIT"].clip(upper=2000000)
df_["AMT_CREDIT"] = df_["AMT_CREDIT"].clip(lower=100000)
df_["AMT_ANNUITY"] = df_["AMT_ANNUITY"].clip(lower=65000)
df_["AMT_ANNUITY"] = df_["AMT_ANNUITY"].clip(upper=6500)

X = df_.drop('TARGET', axis=1)
y = df_["TARGET"]
transformer = Ut.transform(["AMT_INCOME_TOTAL", "AMT_CREDIT", "AMT_ANNUITY"], [], ordinal_list)
X = transformer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=25)

# define model
estimator_ = XGBClassifier()
estimator_.fit(X_train, y_train)
# estimator_ = gridsearch(estimator_)
y_pred = estimator_.predict_proba(X_test)
column_dict = get_columns()
write_output(X_test, y_test, y_pred[:, 1:])
