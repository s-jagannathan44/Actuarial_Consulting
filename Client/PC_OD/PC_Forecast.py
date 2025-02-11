import pandas as pd
import joblib
from sklearn.model_selection import train_test_split


def execute_model(tweedie_model, dataframe):
    y_pred = tweedie_model.predict(dataframe)
    dataframe["Pred"] = y_pred
    dataframe["Pred_Cost"] = dataframe["Pred"] * dataframe["sum_insured_in_hundreds"]
    dataframe.to_csv("Output\\ModelOutput.csv")


def make_pivots(dataframe, column):
    df2 = pd.pivot_table(dataframe, values="ultimate_paid_non_large  Pred_Cost sum_insured_in_hundreds Normalized_LIVES_EXPOSED".split(), columns=column,
                         aggfunc="sum").T
    df2["Actual"] = df2["ultimate_paid_non_large"] / df2["sum_insured_in_hundreds"]
    df2["Predicted"] = df2["Pred_Cost"] / df2["sum_insured_in_hundreds"]
    df2["Error"] = (df2["Predicted"] - df2["Actual"]) / df2["Actual"]
    df2["AbsError"] = df2["Error"].abs()
    df2['%ageError'] = df2['Error'].map('{:.2%}'.format)
    df2.sort_values(by='Normalized_LIVES_EXPOSED', ascending=False, inplace=True)
    df2.to_csv("Output\\Errors\\" + column + ".csv")


def make_multi(dataframe, columns):
    df2 = pd.pivot_table(dataframe, values="ultimate_paid_non_large  Pred_Cost sum_insured_in_hundreds Normalized_LIVES_EXPOSED".split(), columns=columns,
                         aggfunc="sum").T
    df2["Actual"] = df2["ultimate_paid_non_large"] / df2["sum_insured_in_hundreds"]
    df2["Predicted"] = df2["Pred_Cost"] / df2["sum_insured_in_hundreds"]
    df2["Error"] = (df2["Predicted"] - df2["Actual"]) / df2["Actual"]
    df2["AbsError"] = df2["Error"].abs()
    df2['%ageError'] = df2['Error'].map('{:.2%}'.format)
    df2.sort_values(by='Normalized_LIVES_EXPOSED', ascending=False, inplace=True)
    df2.to_csv("Output\\Errors\\" + "multi" + ".csv")


df = pd.read_csv("Output\\4WheelerCombinedFile.csv")
df_train, df_test = train_test_split(df, test_size=0.2, random_state=0)
model = joblib.load("Output\\Tweedie.sav")
model_ttl = joblib.load("Output\\Tweedie_ttl.sav")
y_pred = model.predict(df_test)
df_test["Pred_NL"] = y_pred
df_test["Pred_Cost_NL"] = df_test["Pred_NL"] * df_test["sum_insured_in_hundreds"]

y_pred = model_ttl.predict(df_test)
df_test["Pred_ttl"] = y_pred
df_test["Pred_Cost_ttl"] = df_test["Pred_ttl"] * df_test["sum_insured_in_hundreds"]
df_test.to_csv("Output\\ModelOutput.csv")

# df = pd.read_csv("Output\\ModelOutput.csv")
# make_multi(df, "make_name new_plan_category cc_range seating_capacity previous_insurer_type".split())
#
# master_col_list = (
#     "vehicle_age  registered_state_name registered_city_name make_name  model_name variant_name transmission_type  fuel_type   "
#     "cubic_capacity  vehicle_details_segment supplier_name  opted_kms policy_type registration_rto_code seating_capacity "
#     "is_cng_fitted type_of_cng_kit cc_range previous_ncb new_plan_category NCB  age_range idv_slot is_health_pb_customer "
#     "is_claims_made_in_previous_policy is_two_wheeler_pb_customer  is_travel_pb_customer is_term_life_pb_customer lead_day_slot "
#     "expiry_type is_ep is_coc   is_rsa  is_key_rep   is_inpc is_bi_fuel_kit_liability is_tp_pd_liability  t_booking  t_parent "
#     "previous_supplier_name is_bi_fuel_kit owner_sr previous_policy_type previous_insurer_type Accident_Year"
# ).split()
#
# for var in master_col_list:
#     make_pivots(df, var)

