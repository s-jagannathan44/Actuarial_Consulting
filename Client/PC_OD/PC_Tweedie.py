import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import TweedieRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


# ("make_name_new model_name_new transmission_type fuel_type_new previous_supplier_name_new  cc_range "
#  "vehicle_details_segment_new supplier_name_new policy_type registration_rto_code_new seating_capacity_new "
#  "revised_plan_category_new ncb age_range idv_slot_new  revised_is_cng_fitted_new  is_health_pb_customer "
#  "is_claims_made_in_previous_policy is_two_wheeler_pb_customer is_travel_pb_customer    "
#  "lead_day_slot_new expiry_type_new is_ep is_coc is_rsa is_key_rep is_inpc is_bi_fuel_kit_liability "
#  "is_term_life_pb_customer is_tp_pd_liability").split()

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
            ("regressor", TweedieRegressor(alpha=1.0, power=1.9)),
        ]
    )
    tweedie_glm.fit(
        df_model, df_train["Loss_Cost"], regressor__sample_weight=df_train["LIVES_EXPOSED"]
    )
    joblib.dump(tweedie_glm, "Output\\Tweedie.sav")
    return tweedie_glm  # , column_trans


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
    df2.to_csv("Output\\" + columns + ".csv")


df = pd.read_csv("Output\\4WheelerFile.csv")
df = df[df["LIVES_EXPOSED"] > 0]
df["Loss_Cost"] = df["PAID_AMT"] / df["LIVES_EXPOSED"]
df["Loss_Cost"].fillna(0, inplace=True)
df_train, df_test = train_test_split(df, test_size=0.2, random_state=0)
variable_lost = "make_name_new  fuel_type_new  cc_range supplier_name_new  revised_plan_category_new".split()
df_model = df_train[variable_lost]
model = build_model(variable_lost)

# --------------EXECUTE MODEL-----------------------------
y_pred = model.predict(df_test)
df_test["Pred"] = y_pred
df_test["Pred_Cost"] = df_test["Pred"] * df_test["LIVES_EXPOSED"]
df_test.to_csv("Output\\Tweedie_4wheelerOutput.csv")
make_pivots(df_test, "make_name_new")
make_pivots(df_test, "fuel_type_new")
make_pivots(df_test, "cc_range")
make_pivots(df_test, "supplier_name_new")
make_pivots(df_test, "revised_plan_category_new")



