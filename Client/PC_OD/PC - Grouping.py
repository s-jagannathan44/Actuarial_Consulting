import pandas as pd
import glob

col_list = (
    "vehicle_age  registration_rto_code  make_name  model_name transmission_type  fuel_type  "
    "cubic_capacity  vehicle_details_segment t_booking  t_parent   is_ep  "
    "is_coc   is_rsa  is_key_rep   is_inpc     lead_day_slot "
    "is_health_pb_customer  is_travel_pb_customer  is_two_wheeler_pb_customer  is_term_life_pb_customer  "
    " ncb_composite  policy_type age_range   previous_supplier_name supplier_name "
    " seating_capacity cc_range  expiry_type  "
    "revised_plan_category ncb_composite revised_is_cng_fitted").split()


def find_separation(dataframe, columns):
    df2 = pd.pivot_table(dataframe, values="Ultimate_PAID sum_insured  Normalized_LIVES_EXPOSED".split(), columns=columns,
                         aggfunc="sum").T
    df2["LC"] = df2["Ultimate_PAID"] / df2["Normalized_LIVES_EXPOSED"]
    df2["Ratio"] = df2["Ultimate_PAID"] / df2["sum_insured"]
    df2.to_csv("Output\\Sep\\" + columns + ".csv")


df = pd.read_csv("Output\\modelfile.csv")
df["sum_insured"] = df["sum_insured"]/1000

for var in col_list:
    find_separation(df, var)

path = "Output/Sep/*.csv"
files = glob.glob(path)
writer = pd.ExcelWriter('Output\\Clubbing.xlsx')
for file_name in files:
    frame = pd.read_csv(file_name)
    frame.to_excel(writer, sheet_name=file_name[11:-4])
writer.close()

#
#
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
