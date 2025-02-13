import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import GammaRegressor
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


def build_model(columns):
    column_trans = ColumnTransformer(
        [
            ('OHE', OneHotEncoder(),
             columns),
        ],
    )
    tweedie_glm = Pipeline(
        [
            ("transform", column_trans),
            ("regressor", GammaRegressor(alpha=0.01, max_iter=300)),
        ]
    )
    tweedie_glm.fit(
        df_model, df_train["Targeted_Loss_Cost"])
    joblib.dump(tweedie_glm, "Output\\GammaLossCost.sav")
    return tweedie_glm, column_trans


df = pd.read_csv("Output\\4WheelerLossCostCombinedFile.csv")
df = df[df["LIVES_EXPOSED"] > 0.15]
df = df[df["PAID_AMT"] > 0]

df["Targeted_Loss_Cost"] = df["PAID_AMT"] / df["LIVES_EXPOSED"]

df_train, df_test = train_test_split(df, test_size=0.2, random_state=0)

variable_lost = (
    "vehicle_age_new make_name_new model_name_new  transmission_type_new  fuel_type_new cubic_capacity_new  "
    "vehicle_details_segment_new supplier_name_new policy_type registration_rto_code_new seating_capacity_new  "
    "revised_plan_category_new ncb_composite_new revised_is_cng_fitted_new   is_travel_pb_customer "
    " lead_day_slot_new  "
    "t_booking_new  "
    "previous_insurer_type  previous_policy_type_new ").split()

df_model = df_train[variable_lost]
model, transformer = build_model(variable_lost)
write_output(model._final_estimator.coef_, get_columns())
y_pred = model.predict(df_test)
df_test["Pred"] = y_pred
df_test["Pred_Cost"] = df_test["Pred"] * df_test["LIVES_EXPOSED"]
percent = (df_test["Pred_Cost"].sum() / df_test["PAID_AMT"].sum()) - 1
print("{:.2%}".format(percent))
print(df["LIVES_EXPOSED"].sum())


def make_pivots(dataframe, columns):
    df2 = pd.pivot_table(dataframe, values="PAID_AMT  Pred_Cost LIVES_EXPOSED".split(), columns=columns,
                         aggfunc="sum").T
    df2["Actual"] = df2["PAID_AMT"] / df2["LIVES_EXPOSED"]
    df2["Predicted"] = df2["PAID_AMT"] / df2["LIVES_EXPOSED"]
    df2["Error"] = (df2["Predicted"] - df2["Actual"]) / df2["Actual"]
    df2["AbsError"] = df2["Error"].abs()
    df2['%ageError'] = df2['Error'].map('{:.2%}'.format)
    df2.sort_values(by='LIVES_EXPOSED', ascending=False, inplace=True)
    df2.to_csv("Output\\Errors\\" + columns + ".csv")


for var in variable_lost:
    make_pivots(df_test, var)
