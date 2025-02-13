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


# drop=["7 to 11", "Group 1", "Group 7", "Manual", "Group 1", "Group 3", "COMPACT CARS", "Group 1",
#                       "New", "Others", "5 seater",
#                       "01. Comp", "Group 3", "No Kit", 0, "Group 1", "Group 2", "pvt", "Comp"]
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
        df_model, df_train["Loss_Cost"], regressor__sample_weight=df_train["LIVES_EXPOSED"]
    )
    # joblib.dump(tweedie_glm, "Output\\Tweedie.sav")
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
    df2 = pd.pivot_table(dataframe, values="PAID_AMT IDV LIVES_EXPOSED".split(), columns=columns,
                         aggfunc="sum").T
    df2["Actual"] = df2["PAID_AMT"] / df2["IDV"]
    df2.sort_values(by='LIVES_EXPOSED', ascending=False, inplace=True)
    df2.to_csv("Output\\Sep\\" + columns + ".csv")


df = pd.read_csv("Output\\4WheelerGammaFile.csv")
# df["IDV_Loss_Cost"] = df["IDV_Loss_Cost"]
# df["IDV_Loss_Cost"].fillna(0, inplace=True)
df = df[df["LIVES_EXPOSED"] > 0]
df["Loss_Cost"] = df["PAID_AMT"] / df["LIVES_EXPOSED"]
df["Loss_Cost"].fillna(0, inplace=True)

df_train, df_test = train_test_split(df, test_size=0.2, random_state=0)


# drop=["7 to 11", "Group 1", "Group 7", "Manual", "Group 1", "Group 3", "COMPACT CARS", "Group 1",
#                       "New", "Others", "5 seater",
#                       "01. Comp", "Group 3", "No Kit", 0, "Group 1", "Group 2", "pvt", "Comp"]
variable_lost = (
    "vehicle_age_new make_name_new model_name_new  transmission_type_new  fuel_type_new cubic_capacity_new  "
    "vehicle_details_segment_new supplier_name_new policy_type registration_rto_code_new seating_capacity_new  "
    "revised_plan_category_new ncb_composite_new revised_is_cng_fitted_new   is_travel_pb_customer "
    " lead_day_slot_new  "
    "t_booking_new  "
    "previous_insurer_type  previous_policy_type_new ").split()
# find_separation(df, "vehicle_age_new")
# for var in variable_lost:
#     find_separation(df_train, var)

df_model = df_train[variable_lost]

powers = [1.05]
iterations = [300]
for p_ in powers:
    for i in iterations:
        print(p_, i)
        model, transformer = build_model(p_, i, variable_lost)
        column_dict = get_columns()
        write_output(model._final_estimator.coef_, column_dict)
        y_pred = model.predict(df_test)
        df_test["Pred"] = y_pred
        # df_test["Pred_Cost"] = df_test["Pred"] * df_test["IDV"]
        df_test["Pred_Cost"] = df_test["Pred"] * df_test["LIVES_EXPOSED"]
        percent = (df_test["Pred_Cost"].sum() / df_test["PAID_AMT"].sum()) - 1
        print("{:.2%}".format(percent))

for var in variable_lost:
    make_pivots(df_test, var)
#  make_pivots(df_test, "Accident_Year")
