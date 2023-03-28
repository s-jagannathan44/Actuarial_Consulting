import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import GammaRegressor
import joblib


def build_model():
    global df_train, df_test
    linear_model_preprocessor = ColumnTransformer(
        [
            ("binned_numeric", KBinsDiscretizer(n_bins=3, strategy='uniform'), ["V AGE NEW"]),
            (
                "onehot_categorical",
                OneHotEncoder(),
                ["LT_ANNUAL Flag", "UY New", "CC_Make", "Zone_State", "Body Type"]
            ),
        ],
        remainder='drop'
    )
    print(df_test.shape, df_train.shape)
    gamma_glm = Pipeline(
        [
            ("preprocessor", linear_model_preprocessor),
            ("regressor", GammaRegressor(alpha=1e-12, max_iter=300)),
        ]
    )
    gamma_glm.fit(
        df_train, df_train["Loss Cost"], regressor__sample_weight=df_train["Exposure"])
    # joblib.dump(gamma_glm, "Output\\GammaDeathModel.sav")
    return gamma_glm, linear_model_preprocessor


def get_columns():
    columns = {}
    for encoder in transformer.named_transformers_:
        if type(transformer.named_transformers_[encoder]) != str:
            item = [(encoder, transformer.named_transformers_[encoder].get_feature_names_out().size)]
            columns.update(item)
    return columns


def write_output(X_value):
    col_list = []
    for item in column_dict:
        encoder = transformer.named_transformers_[item]
        col_names = encoder.get_feature_names_out()
        for col_name in col_names:
            col_list.append(col_name)

    frame = pd.DataFrame(columns=col_list)
    np.savetxt("Output\\Injury_co_efficient", X_value, delimiter=",")
    frame.to_csv("Output\\Output.csv")


def execute_model(gamma_model, dataframe):
    y_pred = gamma_model.predict(dataframe)
    dataframe["Output"] = y_pred
    dataframe.to_csv("Output\\df_test.csv")


df = pd.read_csv("Output\\Injury_M_Clubbed.csv")
for col in df.columns:
    if "Unnamed" in col:
        df.drop(col, axis=1, inplace=True)
df_train = df
df_test = df

# glm, transformer = build_model()
# column_dict = get_columns()
# write_output(glm._final_estimator.coef_)
glm = joblib.load("GammaMultiplierInjuryModel.sav")
execute_model(glm, df_test)
