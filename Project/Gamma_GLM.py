import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import GammaRegressor
import joblib
# import numpy as np


def build_model():
    linear_model_preprocessor = ColumnTransformer(
        [
            ("binned_numeric", KBinsDiscretizer(n_bins=3, strategy='uniform'), ["V AGE NEW"]),
            (
                "onehot_categorical",
                OneHotEncoder(),
                ["LT_ANNUAL Flag", "UY New", "Body Type", "CC_desc", "Vehicle Make", "Zone_State"]
            ),
        ],
        remainder='drop'
    )
    print(df_test.shape, df_train.shape)
    gamma_glm = Pipeline(
        [
            ("preprocessor", linear_model_preprocessor),
            # ("regressor", TweedieRegressor(power=1.9, alpha=1e-12, max_iter=300)),
            ("regressor", GammaRegressor(alpha=1e-12, max_iter=300)),
        ]
    )
    gamma_glm.fit(
        df_train, df["Loss Cost"], regressor__sample_weight=df["Exposure"])
    #    joblib.dump(gamma_glm, "Output\\GammaDeathModel.sav")
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

    frame = pd.DataFrame(X_value, columns=col_list)
    frame.to_csv("Output\\Output.csv")


def execute_model(gamma_model, dataframe):
    y_pred = gamma_model.predict(dataframe)
    dataframe["Output"] = y_pred
    dataframe.to_csv("Output\\df_test.csv")


df = pd.read_csv("Output\\Death_M_Clubbed.csv")

for col_ in df.columns:
    if "Unnamed" in col_:
        df.drop(col_, axis=1, inplace=True)
df_train = df
df_test = df

glm, transformer = build_model()
column_dict = get_columns()
# X = transformer.fit_transform(df_train).toarray()
# write_output(X)
# np.savetxt("Output\\co_efficient.csv", glm._final_estimator.coef_, delimiter=",")

glm_ = joblib.load("Output\\GammaMultiplierDeathModel.sav")
execute_model(glm_, df_test)
