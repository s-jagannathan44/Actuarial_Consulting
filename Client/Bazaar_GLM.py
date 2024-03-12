# import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.linear_model import TweedieRegressor


def build_model(power, iter_):
    global df_train, df_test

    interaction = make_pipeline(
        OneHotEncoder(drop=["National RSA", "East", "1000 to 1500cc", "COMP", "Group 2", "MARUTI", "Petrol"]),
    )

    column_trans = ColumnTransformer(
        [
            ('interaction', interaction,
             "Insurer_new Zone_1 cubiccapacity_New plancategory_new roundage_new makename_new fuel_new"
             .split()),
        ],
    )

    print(df_test.shape, df_train.shape)
    tweedie_glm = Pipeline(
        [
            ("transform", column_trans),
            ("regressor", TweedieRegressor(power=power, alpha=1e-12, max_iter=iter_)),
        ]
    )
    tweedie_glm.fit(
        df_model, df_train["Loss_Cost"], regressor__sample_weight=df_train["LIVES_EXPOSED"]
    )
    # joblib.dump(tweedie_glm, "Tweedie.sav")
    return tweedie_glm, column_trans


def make_pivots(dataframe, columns):
    df2 = pd.pivot_table(dataframe, values="PAID_AMT  LIVES_EXPOSED".split(), columns=columns,
                         aggfunc="sum").T
    df2["Actual"] = df2["PAID_AMT"] / df2["LIVES_EXPOSED"]
    df2.to_csv("Bazaar\\Output\\Sep\\" + columns + ".csv")


def make_multi(dataframe, columns):
    df2 = pd.pivot_table(dataframe, values="PAID_AMT Pred_Cost LIVES_EXPOSED".split(), columns=columns,
                         aggfunc="sum").T
    df2["Actual"] = df2["PAID_AMT"] / df2["LIVES_EXPOSED"]
    df2["Predicted"] = df2["Pred_Cost"] / df2["LIVES_EXPOSED"]
    df2["Error"] = (df2["Actual"] - df2["Predicted"]) / df2["Actual"]
    df2['%ageError'] = df2['Error'].map('{:.2%}'.format)
    df2["Error"] = df2["Error"].abs()
    below_ten = df2[df2["Error"] <= 0.1]["LIVES_EXPOSED"].sum()
    total = df2["LIVES_EXPOSED"].sum()
    print('{:.2%}'.format(below_ten / total))
    df2.to_csv("Bazaar\\Output\\text_out.csv")
    # 1 feature and constant
    p = 1 + 1
    aic_value = aic(df2["Actual"], df_test, df2["Predicted"], p)
    print(round(aic_value, 2))


def execute_model(tweedie_model, dataframe):
    y_pred = tweedie_model.predict(dataframe)
    dataframe["Pred"] = y_pred
    dataframe["Pred_Cost"] = dataframe["Pred"] * dataframe["LIVES_EXPOSED"]
    # column_dict = get_columns()
    #  write_output(tweedie_model._final_estimator.coef_, column_dict)
    make_multi(dataframe, "Insurer_new Zone_1 cubiccapacity_New plancategory_new roundage_new makename_new fuel_new"
               .split())


def get_columns():
    columns = {}
    for encoder in transformer.named_transformers_:
        if transformer.named_transformers_[encoder] != 'passthrough':
            item = [(encoder, transformer.named_transformers_[encoder].get_feature_names_out().size)]
            columns.update(item)
    return columns


def write_output(x_value, column_dict):
    col_list = []
    col_list.insert(0, "FY")
    for item in column_dict:
        encoder = transformer.named_transformers_[item]
        col_names = encoder.get_feature_names_out()
        for col_name in col_names:
            col_list.append(col_name)
    frame = pd.DataFrame(x_value.reshape(1, -1), columns=col_list).T
    frame.to_csv("Bazaar\\Output\\new_efficients.csv")


def llf_(y, x, pr):
    # return maximized log likelihood
    nobs = float(x.shape[0])
    nobs2 = nobs / 2.0
    nobs = float(nobs)
    resid = y - pr
    ssr = np.sum(resid ** 2)
    llf = -nobs2 * np.log(2 * np.pi) - nobs2 * np.log(ssr / nobs) - nobs2
    return llf


def aic(y, X_, pr, p):
    # return aic metric
    llf = llf_(y, X_, pr)
    return -2 * llf + 2 * p


df = pd.read_csv("Bazaar\\Output\\4WheeleerFile.csv")
for col in df.columns:
    if "Unnamed" in col:
        df.drop(col, axis=1, inplace=True)

df["Loss_Cost"] = df["PAID_AMT"] / df["LIVES_EXPOSED"]

df_train, df_test = train_test_split(df, test_size=0.2, random_state=0)
df_model = df_train["Insurer_new Zone_1 cubiccapacity_New plancategory_new roundage_new makename_new fuel_new".split()]

powers = [1.5]
iterations = [5000]
for p_ in powers:
    for i in iterations:
        print(p_, i)
        glm, transformer = build_model(p_, i)
        execute_model(glm, df_test)


def othering(dataframe):
    make_pivots(dataframe, "Insurer_new")
    make_pivots(dataframe, "Zone_1")
    make_pivots(dataframe, "cubiccapacity_New")
    make_pivots(dataframe, "fuel_new")
    make_pivots(dataframe, "plancategory_new")
    make_pivots(dataframe, "roundage_new")
    make_pivots(dataframe, "makename_new")


def find_separation():
    df_ = pd.read_csv("Bazaar\\Output\\4WheeleerFile.csv")
    othering(df_)
