import pandas as pd
import glob


# ----------------- Combine multiple CSV files into one Excel sheet-------------------------
path = "Output/Recon/final/*.csv"
files = glob.glob(path)
writer = pd.ExcelWriter('Output\\recon.xlsx')
for file_name in files:
    frame = pd.read_csv(file_name)
    frame.drop(["Unnamed: 0"], axis=1, inplace=True)
    frame.to_excel(writer, sheet_name=file_name[19:-4])
writer.close()


col_list = (
    "vehicle_age  registered_state_name  registered_city_name    registration_rto_code  make_name  model_name  variant_name  transmission_type  fuel_type  "
    "cubic_capacity  vehicle_details_segment  sum_insured  is_bi_fuel_kit  t_booking_x  t_parent_x    is_pg  is_paid_x  is_zd  is_ep  "
    "is_lpb  is_coc  is_pa  is_rsa  is_daily_ac  is_key_rep  is_ncb_pr  is_windshield  is_inpc  is_electrical_accessories  is_non_electrical_accessories  "
    "is_bi_fuel_kit  is_bi_fuel_kit_liability  is_pa_for_unnamed_passenger  is_compulsory_pa_cover_for_owner_driver  is_legal_liability_to_paid_driver  "
    "is_tp_pd_liability  is_voluntary_discount  previous_policy_type  previous_ncb_x  is_claims_made_in_previous_policy   is_zd  lead_day_slot  "
    "is_health_pb_customer  is_travel_pb_customer  is_two_wheeler_pb_customer  is_term_life_pb_customer  owner_sr  is_investment_pb_customer  "
    " ncb_x  policy_type   opted_kms   "
    "  is_cng_fitted  type_of_cng_kit  seating_capacity  previous_supplier_name  cc_range  new_plan_category  expiry_type  "
    "age_range  idv_slot  previous_supplier_name supplier_name").split()

col_list_new = (
    "vehicle_age  registered_state_name  registered_city_name    registration_rto_code  make_name  model_name  variant_name  transmission_type  fuel_type  "
    "cubic_capacity  vehicle_details_segment  sum_insured  is_bi_fuel_kit  t_booking_x  t_parent_x  t_booking_y  t_parent_y   is_pg  is_paid_x is_paid_y is_zd  is_ep  "
    "is_lpb  is_coc  is_pa  is_rsa  is_daily_ac  is_key_rep  is_ncb_pr  is_windshield  is_inpc  is_electrical_accessories  is_non_electrical_accessories  "
    "is_bi_fuel_kit  is_bi_fuel_kit_liability  is_pa_for_unnamed_passenger  is_compulsory_pa_cover_for_owner_driver  is_legal_liability_to_paid_driver  "
    "is_tp_pd_liability  is_voluntary_discount  previous_policy_type  previous_ncb_x previous_ncb_y  is_claims_made_in_previous_policy   is_zd  lead_day_slot  "
    "is_health_pb_customer  is_travel_pb_customer  is_two_wheeler_pb_customer  is_term_life_pb_customer  owner_sr  is_investment_pb_customer  "
    " ncb_x ncb_y   policy_type   opted_kms   "
    "  is_cng_fitted  type_of_cng_kit  seating_capacity  previous_supplier_name  cc_range  new_plan_category  expiry_type  "
    "age_range  idv_slot  previous_supplier_name supplier_name").split()


def find_old_separation(dataframe, columns):
    df2 = pd.pivot_table(dataframe, values="Ultimate_PAID  Normalized_LIVES_EXPOSED".split(), columns=columns,
                         aggfunc="sum").T
    df2["LC_Old"] = df2["Ultimate_PAID"] / df2["Normalized_LIVES_EXPOSED"]
    df2.to_csv("Output\\Recon\\old_" + columns + ".csv")


def find_new_separation(dataframe, columns):
    df2 = pd.pivot_table(dataframe, values="Ultimate_PAID  Normalized_LIVES_EXPOSED".split(), columns=columns,
                         aggfunc="sum").T
    df2["LC_new"] = df2["Ultimate_PAID"] / df2["Normalized_LIVES_EXPOSED"]
    df2.to_csv("Output\\Recon\\new_" + columns + ".csv")

    # old = pd.read_csv("CSV\\Ultimate.csv")
    # old.rename(columns={"t_booking": "t_booking_x"}, inplace=True)
    # old.rename(columns={"t_parent": "t_parent_x"}, inplace=True)
    # old.rename(columns={"is_paid": "is_paid_x"}, inplace=True)
    # old.rename(columns={"ncb": "ncb_x"}, inplace=True)
    # old.rename(columns={"previous_ncb": "previous_ncb_x"}, inplace=True)
    #
    # new = pd.read_csv("CSV\\Ultimate_fixed.csv")
    #
    # for var in col_list:
    #     find_old_separation(old, var)
    #
    #
    # for var in col_list_new:
    #     find_new_separation(new, var)
    #
    #
    # new = pd.read_csv("Output\\Recon\\new_make_name.csv")
    # old = pd.read_csv("Output\\Recon\\old_make_name.csv")
    # new.drop(["Ultimate_PAID"], axis=1, inplace=True)
    # old.drop(["Ultimate_PAID"], axis=1, inplace=True)
    # old.rename(columns={"Normalized_LIVES_EXPOSED": "Exposure_Old"}, inplace=True)
    # new.rename(columns={"Normalized_LIVES_EXPOSED": "Exposure_new"}, inplace=True)
    #
    # df_final = old.merge(new, on=["make_name"], how="left")
    # df_final["Diff"] = df_final["Exposure_new"] - df_final["Exposure_Old"]
    # df_final.to_csv("Output\\Recon\\make_name.csv")

    # for column in col_list:
    #     new = pd.read_csv("Output\\Recon\\new_" + column + ".csv")
    #     old = pd.read_csv("Output\\Recon\\old_" + column + ".csv")
    #     new.drop(["Ultimate_PAID"], axis=1, inplace=True)
    #     old.drop(["Ultimate_PAID"], axis=1, inplace=True)
    #     old.rename(columns={"Normalized_LIVES_EXPOSED": "Exposure_Old"}, inplace=True)
    #     new.rename(columns={"Normalized_LIVES_EXPOSED": "Exposure_new"}, inplace=True)
    #
    #     df_final = old.merge(new, on=[column], how="left")
    #     df_final["Diff"] = df_final["Exposure_new"] - df_final["Exposure_Old"]
    #     df_final.to_csv("Output\\Recon\\final\\" + column + ".csv")
