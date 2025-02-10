import pandas as pd
# import joblib


def set_financial_year(year_p):
    try:
        year = year_p.to_period('Q-MAR').qyear
        quarter = year_p.to_period('Q-MAR').quarter
        retval = str(year) + "_Q" + str(quarter)
        print(retval)
        return retval
        # return year_p.to_period('Q-MAR').quarter
    except AttributeError:
        print("error occurred in set_financial_year")
        return ""


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

#
# df = pd.read_csv("Output\\4WheelerUn_clubbedFile.csv")
# model = joblib.load("Output\\Tweedie.sav")
# execute_model(model, df)


# df = pd.read_csv("Output\\ModelOutput.csv")
# make_multi(df, "make_name new_plan_category cc_range seating_capacity previous_insurer_type".split())

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

df = pd.read_csv("CSV\\policy_claims_analysis.csv")
df = df[~ df["supplier_name"].str.contains("Iffco Tokio General Insurance Company Ltd", na=False)]
df = df[~ df["supplier_name"].str.contains("Raheja QBE General Insurance Company", na=False)]
df = df[~ df["supplier_name"].str.contains("SBI General Insurance Company Ltd", na=False)]
df['Loss Date'] = pd.to_datetime(df['Loss Date'], format="mixed", dayfirst=True)
df['registration_rto_code'] = df['registration_rto_code'].str.replace('DL01', 'DL1')
df['registration_rto_code'] = df['registration_rto_code'].str.replace('RJ01', 'RJ1')
df["Accident_Quarter"] = df["Loss Date"].apply(lambda x: set_financial_year(x))


df = df[df["Accident_Quarter"].isin(["2022_Q4"])]
df.to_csv("Output\\OutOfTimeQ42022.csv")
