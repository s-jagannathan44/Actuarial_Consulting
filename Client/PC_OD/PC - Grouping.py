import pandas as pd
import glob
# Sum Insured has been removed as we are normalising by sum insured
# Accident Year has been added
master_col_list = (
    "vehicle_age  registered_state_name registered_city_name make_name  model_name variant_name transmission_type  fuel_type   "
    "cubic_capacity  vehicle_details_segment supplier_name  opted_kms policy_type registration_rto_code seating_capacity "
    "is_cng_fitted type_of_cng_kit cc_range previous_ncb new_plan_category NCB  age_range idv_slot is_health_pb_customer "
    "is_claims_made_in_previous_policy is_two_wheeler_pb_customer  is_travel_pb_customer is_term_life_pb_customer lead_day_slot "
    "expiry_type is_ep is_coc   is_rsa  is_key_rep   is_inpc is_bi_fuel_kit_liability is_tp_pd_liability  t_booking  t_parent "    
    "previous_supplier_name is_bi_fuel_kit owner_sr previous_policy_type previous_insurer_type Accident_Year"
).split()

# Variables dropped due to co-relation
#  registered_state_name registered_city_name variant_name opted_kms is_cng_fitted type_of_cng_kit cc_range previous_ncb new_plan_category
#  NCB  age_range idv_slot is_claims_made_in_previous_policy is_bi_fuel_kit_liability is_tp_pd_liability is_bi_fuel_kit

model_col_list = (
    "vehicle_age  make_name  model_name  transmission_type  fuel_type  cubic_capacity  vehicle_details_segment  "
    "supplier_name policy_type registration_rto_code seating_capacity is_health_pb_customer revised_plan_category "
    "ncb_composite revised_is_cng_fitted is_two_wheeler_pb_customer  is_travel_pb_customer is_term_life_pb_customer "
    "lead_day_slot expiry_type is_ep is_coc   is_rsa  is_key_rep   is_inpc t_booking  t_parent previous_supplier_name "    
    "owner_sr previous_policy_type previous_insurer_type"
).split()

large_model_col_list = (
    "age_range  cc_range  make_name  fuel_type registered_state_name"
).split()


def find_ttl_separation(dataframe, columns):
    df2 = pd.pivot_table(dataframe, values="ultimate_paid_large_ttl sum_insured_in_hundreds  Normalized_LIVES_EXPOSED".split(),
                         columns=columns,
                         aggfunc="sum").T
    df2["IDV_LossCost"] = df2["ultimate_paid_large_ttl"] / df2["sum_insured_in_hundreds"]
    df2["LossCost"] = df2["ultimate_paid_large_ttl"] / df2["Normalized_LIVES_EXPOSED"]
    df2.sort_values(by='Normalized_LIVES_EXPOSED', ascending=False, inplace=True)
    df2.to_csv("Output\\Sep\\ttl_" + columns + ".csv")


def find_separation(dataframe, columns):
    df2 = pd.pivot_table(dataframe, values="ultimate_paid_non_large sum_insured_in_hundreds  Normalized_LIVES_EXPOSED".split(),
                         columns=columns,
                         aggfunc="sum").T
    df2["IDV_LossCost"] = df2["ultimate_paid_non_large"] / df2["sum_insured_in_hundreds"]
    df2["LossCost"] = df2["ultimate_paid_non_large"] / df2["Normalized_LIVES_EXPOSED"]
    df2.sort_values(by='Normalized_LIVES_EXPOSED', ascending=False, inplace=True)
    df2.to_csv("Output\\Sep\\" + columns + ".csv")


def group_opted_kms(x):
    if x in [0, 2500, 3000, 5000]:
        return "_Low Usage"
    elif x in [5500, 7000, 7500, 8500]:
        return "_Medium Usage"
    else:
        return "_null"


def correct_plan_name(x):
    if "PAYD" in x:
        return x
    else:
        return x.split("_", 1)[0]


def convert_null_to_na():
    df["NCB"] = df["NCB"].astype(str)
    df["previous_ncb"] = df["previous_ncb"].astype(str)
    df["cubic_capacity"] = df["cubic_capacity"].astype(str)
    df["seating_capacity"] = df["seating_capacity"].astype(str)
    df["transmission_type"] = df["transmission_type"].astype(str)
    df["t_booking"] = df["t_booking"].astype(str)
    df["t_parent"] = df["t_parent"].astype(str)
    df["vehicle_age"] = df["vehicle_age"].astype(str)
    df["vehicle_details_segment"] = df["vehicle_details_segment"].fillna("null")
    df["cubic_capacity"] = df["cubic_capacity"].fillna("null")
    df["NCB"] = df["NCB"].fillna("null")
    df["previous_ncb"] = df["previous_ncb"].fillna("null")
    df["make_name"] = df["make_name"].fillna("null")
    df["model_name"] = df["model_name"].fillna("null")
    df["variant_name"] = df["variant_name"].fillna("null")
    df["previous_supplier_name"] = df["previous_supplier_name"].fillna("null")
    df["registration_rto_code"] = df["registration_rto_code"].fillna("null")
    df["seating_capacity"] = df["seating_capacity"].fillna("null")
    df["transmission_type"] = df["transmission_type"].fillna("null")
    df["t_booking"] = df["t_booking"].fillna("null")
    df["t_parent"] = df["t_parent"].fillna("null")
    df["vehicle_age"] = df["vehicle_age"].fillna("null")
    df["type_of_cng_kit"] = df["type_of_cng_kit"].fillna("null")
    df["owner_sr"] = df["owner_sr"].fillna("-1")


df = pd.read_csv("CSV\\FixedMultiplier\\Combined_final_file.csv")
df.drop(["Unnamed: 0"], axis=1, inplace=True)
convert_null_to_na()

df["revised_is_cng_fitted"] = df["is_cng_fitted"].apply(lambda x: "Kit_Is" if x > 0 else "No_Kit")
df["revised_bi_fuel_kit"] = df["is_bi_fuel_kit_liability"].apply(lambda x: "Liability" if x > 0 else "Zero_Liability")
df["is_cng_fitted"] = df["is_cng_fitted"].fillna("null")
df["revised_is_cng_fitted"] = df["revised_is_cng_fitted"] + df["type_of_cng_kit"] + df["revised_bi_fuel_kit"]
df["ncb_composite"] = df["previous_ncb"] + "_" + df["NCB"]

df["opted_kms_New"] = df["opted_kms"].apply(lambda x: group_opted_kms(x) if x < 10000 else "_High Usage")
df["opted_kms_New"] = df["opted_kms_New"].fillna("null")
df["revised_plan_category"] = df["new_plan_category"] + df["opted_kms_New"]
df["revised_plan_category"] = df["revised_plan_category"].apply(lambda x: correct_plan_name(x))
df.drop(["is_claims_made_in_previous_policy", "type_of_cng_kit",  "NCB", "previous_ncb",
         "opted_kms",
         "is_tp_pd_liability", "is_bi_fuel_kit_liability", "is_cng_fitted", "new_plan_category", "opted_kms_New"],
        axis=1, inplace=True)


for var in large_model_col_list:
    find_ttl_separation(df, var)

path = "Output/Sep/*.csv"
files = glob.glob(path)
writer = pd.ExcelWriter('Output\\ttl_Clubbing(2).xlsx')
for file_name in files:
    frame = pd.read_csv(file_name)
    frame.to_excel(writer, sheet_name=file_name[11:-4])
writer.close()


