import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import TweedieRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


def get_columns():
    columns = {}
    for encoder in transformer.named_transformers_:
        if transformer.named_transformers_[encoder] != 'passthrough':
            item = [(encoder, transformer.named_transformers_[encoder].get_feature_names_out().size)]
            columns.update(item)
    return columns


def write_output(x_value, column_dict):
    col_list = []
    # col_list.insert(0, "AY")
    for item in column_dict:
        encoder = transformer.named_transformers_[item]
        col_names = encoder.get_feature_names_out()
        for col_name in col_names:
            col_list.append(col_name)
    frame = pd.DataFrame(x_value.reshape(1, -1), columns=col_list).T
    frame.to_csv("Output\\new_efficient.csv")


def build_model(power, iter_, columns):
    column_trans = ColumnTransformer(
        [
            ('OHE', OneHotEncoder(),
             columns),
        ],
    )
    tweedie_glm = Pipeline(
        [
            ("transform", column_trans),
            ("regressor", TweedieRegressor(power=power, alpha=0.01, max_iter=iter_)),
        ]
    )
    tweedie_glm.fit(
        df_model, df_train["IDV_Loss_Cost"], regressor__sample_weight=df_train["IDV"]
    )
    joblib.dump(tweedie_glm, "Output\\Tweedie_ttl.sav")
    return tweedie_glm, column_trans


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
    df2.to_csv("Output\\multi.csv")


def make_pivots(dataframe, columns):
    df2 = pd.pivot_table(dataframe, values="PAID_AMT  Pred_Cost LIVES_EXPOSED".split(), columns=columns,
                         aggfunc="sum").T
    df2["Actual"] = df2["PAID_AMT"] / df2["LIVES_EXPOSED"]
    df2["Predicted"] = df2["Pred_Cost"] / df2["LIVES_EXPOSED"]
    df2["Error"] = (df2["Predicted"] - df2["Actual"]) / df2["Actual"]
    df2["AbsError"] = df2["Error"].abs()
    df2['%ageError'] = df2['Error'].map('{:.2%}'.format)
    df2.sort_values(by='LIVES_EXPOSED', ascending=False, inplace=True)
    df2.to_csv("Output\\Errors\\" + columns + ".csv")


def find_separation(dataframe, columns):
    df2 = pd.pivot_table(dataframe, values="PAID_AMT  LIVES_EXPOSED".split(), columns=columns,
                         aggfunc="sum").T
    df2["Actual"] = df2["PAID_AMT"] / df2["LIVES_EXPOSED"]
    df2.to_csv("Output\\Sep\\" + columns + ".csv")


df = pd.read_csv("Output\\4WheelerTTLFile.csv")
df["IDV_Loss_Cost"] = df["IDV_Loss_Cost"]
df["IDV_Loss_Cost"].fillna(0, inplace=True)

# df = df[df["LIVES_EXPOSED"] > 0]
# df["Loss_Cost"] = df["PAID_AMT"] / df["LIVES_EXPOSED"]
# df["Loss_Cost"].fillna(0, inplace=True)

df_train, df_test = df, df  # train_test_split(df, test_size=0.2, random_state=0)
# find_separation(df_train, "revised_plan_category_new")

variable_lost = (
    "vehicle_age_ttl make_name_ttl state_name_ttl fuel_type_ttl cubic_capacity_ttl  ").split()

df_model = df_train[variable_lost]

powers = [1.05]
iterations = [3000]
for p_ in powers:
    for i in iterations:
        print(p_, i)
        model, transformer = build_model(p_, i, variable_lost)
        # column_dict = get_columns()
        # write_output(model._final_estimator.coef_, column_dict)
        y_pred = model.predict(df_test)
        df_test["Pred"] = y_pred
        df_test["Pred_Cost"] = df_test["Pred"] * df_test["IDV"]
        # df_test["Pred_Cost"] = df_test["Pred"] * df_test["LIVES_EXPOSED"]
        percent = (df_test["Pred_Cost"].sum() / df_test["PAID_AMT"].sum()) - 1
        print("{:.2%}".format(percent))

# model = build_model(variable_lost)
#
# # --------------EXECUTE MODEL-----------------------------
# y_pred = model.predict(df_test)
# df_test["Pred"] = y_pred
# df_test["Pred_Cost"] = df_test["Pred"] * df_test["IDV"]
# df_test.to_csv("Output\\Tweedie_4wheelerOutput.csv")
# percent = (df_test["Pred_Cost"].sum() / df_test["PAID_AMT"].sum()) - 1
# print("{:.2%}".format(percent))
for var in variable_lost:
    make_pivots(df_test, var)
