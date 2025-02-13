import pandas as pd
import duckdb as db


def prepare_tweedie_file():
    # q3 = """select vehicle_age_new, make_name_new, model_name_new,  transmission_type_new,  fuel_type_new, cubic_capacity_new,
    #         vehicle_details_segment_new, supplier_name_new, policy_type, registration_rto_code_new, seating_capacity_new,
    #          revised_plan_category_new, ncb_composite_new, revised_is_cng_fitted_new, owner_sr_new,
    #           is_travel_pb_customer,  lead_day_slot_new, t_booking_new, previous_insurer_type, previous_policy_type_new,
    #          sum(ultimate_paid_non_large) as PAID_AMT,sum(Claim_Count) as Claim_Count, sum(sum_insured_in_hundreds) as IDV,
    #          sum(Normalized_LIVES_EXPOSED) as LIVES_EXPOSED , sum(ultimate_paid_non_large) / sum(sum_insured_in_hundreds) as IDV_Loss_Cost
    #          from df
    #           group by   vehicle_age_new, make_name_new, model_name_new,  transmission_type_new,  fuel_type_new, cubic_capacity_new,
    #         vehicle_details_segment_new, supplier_name_new, policy_type, registration_rto_code_new, seating_capacity_new,
    #          revised_plan_category_new, ncb_composite_new, revised_is_cng_fitted_new,owner_sr_new,
    #           is_travel_pb_customer,  lead_day_slot_new, t_booking_new, previous_insurer_type, previous_policy_type_new
    #    """
    q3 = """select vehicle_age_new, make_name_new, model_name_new,  transmission_type_new,  fuel_type_new, cubic_capacity_new,
                vehicle_details_segment_new, supplier_name_new, policy_type, registration_rto_code_new, seating_capacity_new,
                 revised_plan_category_new, ncb_composite_new, revised_is_cng_fitted_new,owner_sr_new,
                  is_travel_pb_customer,  lead_day_slot_new, t_booking_new, previous_insurer_type, previous_policy_type_new,
                 sum(Pred_total) as PAID_AMT,sum(Claim_Count) as Claim_Count, sum(Normalized_LIVES_EXPOSED) as LIVES_EXPOSED
                 from df
                  group by   vehicle_age_new, make_name_new, model_name_new,  transmission_type_new,  fuel_type_new, cubic_capacity_new,
                vehicle_details_segment_new, supplier_name_new, policy_type, registration_rto_code_new, seating_capacity_new,
                 revised_plan_category_new, ncb_composite_new, revised_is_cng_fitted_new,owner_sr_new,
                  is_travel_pb_customer,  lead_day_slot_new, t_booking_new, previous_insurer_type, previous_policy_type_new
           """

    output = db.execute(q3).df()
    output.to_csv("Output\\4WheelerLossCostCombinedFile.csv")


def group_age(x):
    if x in [0, 1, 2, 6, 11]:
        return str(x) + "_years"
    elif x in [-1, 5, 37]:
        return "Five"
    elif x in [8, 9, 10]:
        return "Group 1"
    elif x in [-5, 7, 24]:
        return "Group 2"
    elif x in [3, 4]:
        return "Group 3"
    else:
        return "Above 12"


def group_cubic_capacity(x):
    if x in [1086, 1197, 1198, 1493, 1497]:
        return x
    elif x in [796, 814]:
        return "Group 1"
    elif x in [799, 998]:
        return "Group 2"
    elif x in [1199, 1396]:
        return "Group 4"
    elif x in [1498, 999]:
        return "Group 5"
    elif x in [1248, 1461, 2179]:
        return "Group 3"
    else:
        return "Others"


def group_composite_ncb(x):
    if x in ["50.0_50.0", "0.0_20.0", "0.0_0.0", "35.0_0.0"]:
        return x
    elif x in ["50.0_0.0", "45.0_50.0"]:
        return "Group 2"
    elif x in ["20.0_0.0", "25.0_0.0"]:
        return "Group 4"
    else:
        return "Group 3"


def group_rto(x):
    if x in ["WB06", "DL4"]:
        return "Group 1"
    elif x in ["AP31", "HR03", "HR01", "RJ14", "UK08"]:
        return "Group 2"
    elif x in ["AS01", "MH02", "DL7", "DL8", "DL3", "AS06", "WB74", "DL6", "KA19"]:
        return "Group 3"
    elif x in ["DL2", "DL1", "KA53", "DL9", "KL01", "MH04", "KA02", "KA04", "WB02", "KA05"]:
        return "Group 4"
    elif x in ["MH43", "KA09", "MH03", "MH31", "MH48", "PB65", "HR29", "KA03", "HR05", "WB26", "MH01", "TN09", "KL07",
               "UK06", "MH05", "PB08", "KA51", "MH46", "DL5"]:
        return "Group 5"
    elif x in ["UK07", "GJ06", "TN22", "UP80", "PB10", "JK02", "JH05", "MH12", "TN07", "PB02", "MH14", "CG07", "TN10",
               "HR51"]:
        return "Group 6"
    elif x in ["UP65", "HR20", "MH15", "UK04", "HR06", "HR10", "JH10", "CH01", "OD02", "KA01", "RJ20", "UP14", "UP70",
               "DL12", "UP78", "HR26", "TN11", "UP15", "BR06", "GJ01", "MH20", "MH09", "DL10", "MP20"]:
        return "Group 7"
    elif x in ["UP25", "RJ02", "JH01", "GJ05", "UP81", "HR12", "DL14", "GJ03", "MH47", "MP04", "UP53", "BR01", "TS07",
               "RJ27", "TS09", "HR36", "RJ19", "MH49", "UP16", "GJ15", "GJ18"]:
        return "Group 8"
    elif x in ["MP09", "TS08", "CG04", "GJ27", "UP32", "MP07", "TN14"]:
        return "Group 9"
    else:
        return "Others"


def group_model(x):
    if x in ["BEAT", "ALTO"]:
        return "Group 1"
    elif x in ["i 10 1.2 KAPPA", "i 10 1.1", "RITZ", "EON"]:
        return "Group 2"
    elif x in ["ALTO K10", "ALTO 800", "BRIO", "EECO"]:
        return "Group 3"
    elif x in ["FIGO", "BOLERO", "WAGON R", "SWIFT DZIRE KB"]:
        return "Group 4"
    elif x in ["SWIFT DZIRE", "ETIOS", "CELERIO"]:
        return "Group 5"
    elif x in ["SWIFT", "Kwid", "XCENT", "GRAND i10", "SCORPIO M HAWK"]:
        return "Group 6"
    elif x in ["POLO", "ERTIGA", "TIAGO", "IGNIS"]:
        return "Group 7"
    elif x in ["SANTRO", "JAZZ", "DUSTER", "i 20", "FLUIDIC VERNA", "VENTO", "AMAZE"]:
        return "Group 8"
    elif x in ["BALENO", "TIGOR", "NEW CITY", "DZIRE", "ECOSPORT", "CITY", "Vitara Brezza", "CIAZ"]:
        return "Group 9"
    elif x in ["WR-V", "NEXON"]:
        return "Group 10"
    elif x in ["CRETA", "ALTROZ", "Venue"]:
        return "Group 11"
    else:
        return "Others"


def group_previous_insurer(x):
    if x in ["Reliance Endorsement Collection", "National Endorsement Collection", "Acko General Insurance",
             "Magma HDI General Insurance",
             "National Insurance Company Ltd", "Navi General Insurance"]:
        return "Group 1"
    elif x in ["Bajaj Allianz General Insurance Company Ltd", "The New India Assurance Co. Ltd.",
               "Zurich Kotak General Insurance", "Zuno General Insurance"]:
        return "Group 3"
    elif x in ["AXA Assistance", "DIGIT General Insurance", "Universal Sompo General Insurance Company Ltd",
               "Iffco Tokio General Insurance Company Ltd",
               "Royal Sundaram Alliance Insurance Company Ltd", "Cholamandalam MS General Insurance Company Ltd",
               "Reliance General Insurance Company Ltd",
               "Raheja QBE General Insurance Company", "The Oriental Insurance Company Ltd"]:
        return "Group 4"
    elif x in ["United India Insurance Company Ltd", "HDFC Ergo General Insurance Company Ltd", "Bharti Axa",
               "Cross Roads India Assistance Pvt Ltd", "ICICI Lombard General Insurance Company Ltd"]:
        return "Group 5"
    elif x in ["Shriram General Insurance Company Ltd"]:
        return "Sriram"
    else:
        return "Others"


def group_lead_day(x):
    if x in ["daytime", "evening", "late_night", "night"]:
        return "Group 1"
    else:
        return "Early"


def group_previous_policy_type(x):
    if x in [0, 1]:
        return "Group 1"
    elif x in [2, 3]:
        return "Group 2"


def group_owner_sr(x):
    if x in [1, 2, 3]:
        return x
    else:
        return "Others"


def group_make(x):
    if x in ["MARUTI"]:
        return x
    elif x in ["MAHINDRA AND MAHINDRA", "HYUNDAI", "RENAULT"]:
        return "Group 1"
    elif x in ["TATA", "FORD", "HONDA", "VOLKSWAGEN"]:
        return "Group 2"
    else:
        return "Others"


def group_cng(x):
    if x in ["Kit_IsExternallyFittedLiability"]:
        return "Externally Fitted"
    elif x in ["Kit_IsCompanyFittedLiability"]:
        return "Company Fitted"
    else:
        return "No Kit"


def group_seating_capacity(x):
    if x in [5, 13]:
        return "5 seater"
    elif x in [7]:
        return "7 seater"
    else:
        return "Others"


def group_insurer(x):
    if x in ["Shriram General Insurance Company Ltd", "The New India Assurance Co. Ltd."]:
        return "Group 1"
    elif x in ["National Insurance Company Ltd", "Bajaj Allianz General Insurance Company Ltd"]:
        return "Group 2"
    elif x in ["Royal Sundaram Alliance Insurance Company Ltd", "Zuno General Insurance"]:
        return "Group 4"
    elif x in ["Liberty General Insurance Co. Ltd", "Future Generali"]:
        return "Group 5"
    elif x in ["Magma HDI General Insurance", "The Oriental Insurance Company Ltd",
               "United India Insurance Company Ltd"]:
        return x
    else:
        return "Group 3"


def group_fuel_type(x):
    if x in ["Petrol", "LPG"]:
        return "Group 1"
    elif x in ["CNG", "Electric"]:
        return "CNG+"
    else:
        return "Diesel"


def group_transmission_type(x):
    if x in [0]:
        return "Manual"
    else:
        return "Group 2"


def group_vehicle_segment(x):
    if x in ["COMPACT CARS", "MINI VEHICLES", "MULTI UTILITY VEHICLES"]:
        return 'Group 1'
    if x in ["SPORTS AND UTILITY VEHICLES", "MIDSIZE CARS"]:
        return x
    if x in ["null"]:
        return "BLANK"
    else:
        return "Others"


def group_plan(x):
    if x in ["01. Comp", "07. PAYD_High Usage", "04. SAOD"]:
        return "Group 1"
    elif x in ["10. PAYD + SAOD + ZD_High Usage", "13. PG + SAOD + ZD", "16. Long Term With ZD",
               "17. Long Term + ZD + PAYD_High Usage", "18. Long Term + PAYD_High Usage"]:
        return "Group 3"
    elif x in ["07. PAYD_Low Usage", "11. PG"]:
        return "Group 4"
    elif x in ["02. Comp With ZD", "08. PAYD + SAOD_Medium Usage", "10. PAYD + SAOD + ZD_Medium Usage",
               "17. Long Term + ZD + PAYD_Medium Usage"]:
        return "Group 5"
    elif x in ["05. SAOD + ZD", "15. Long Term", "17. Long Term + ZD + PAYD_Low Usage",
               "18. Long Term + PAYD_Medium Usage"]:
        return "Group 6"
    else:
        return "Group 2"


def group_booking(x):
    if x in [0]:
        return "Zero"
    elif x in [1, 2]:
        return "Group 4"
    elif x in [-1, -3, -2, -50, -49]:
        return "Group 1"
    elif x in [15, -91, 16, 10, 5, 7, 3]:
        return "Group 2"
    elif x in [14, 4, 17, 6, 13, 12, 9, 8, 11]:
        return "Group 3"
    else:
        return "Others"


def group_parent(x):
    if x in [1]:
        return "One"
    elif x in [45, 57, 0, 58, 59, 60]:
        return "Group 1"
    elif x in [2, 3, 4, 5, 6, 7]:
        return "Group 2"
    else:
        return "Others"


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

def group_age_ttl(x):
    if x in [0, 2, 5, 6, 8]:
        return "Group 1"
    elif x in [1, 3, 7]:
        return "Group 2"
    elif x in [4, 9, 12, 13, 16]:
        return "Group 3"
    else:
        return "Group 4"


def group_cubic_capacity_ttl(x):
    if x in [1198]:
        return "Group 2"
    elif x in [1199, 1396]:
        return "Group 2"
    elif x in [796, 999, 1086, 1493]:
        return "Group 3"
    elif x in [814, 1461, 1498]:
        return "Group 4"
    else:
        return "Group 1"


def group_state_ttl(x):
    if x in ["Daman & Diu", "Haryana", "Madhya Pradesh", "Orissa", "Rajasthan", "Tamil Nadu"]:
        return "Group 1"
    elif x in ["Chandigarh", "Chattisgarh", "Delhi", "Goa", "Gujarat", "Himachal Pradesh", "Jammu and Kashmir",
               "Jharkhand", "Punjab", "Uttar Pradesh"]:
        return "Group 2"
    elif x in ["Andhra Pradesh", "Assam", "Bihar", "Kerala", "Maharashtra", "UTTARAKHAND"]:
        return "Group 4"
    else:
        return "Group 5"


def group_make_ttl(x):
    if x in ["MARUTI", "KIA", "HONDA"]:
        return "Maruti +"
    elif x in ["RENAULT", "FORD", "VOLKSWAGEN"]:
        return "Group 3"
    elif x in ["MAHINDRA AND MAHINDRA"]:
        return "M&M"
    else:
        return "Others"


def group_fuel_type_ttl(x):
    if x in ["Petrol", "Electric"]:
        return "Group 1"
    elif x in ["Diesel", "CNG", "LPG"]:
        return "CNG+"



def pre_clubbing_transformation():
    df.drop(["Unnamed: 0", "Unnamed: 0.1"], axis=1, inplace=True)
    df["round_owner"] = round(pd.to_numeric(df['owner_sr'], downcast='integer', errors='coerce'), 0)
    df["vehicle_details_segment"] = df["vehicle_details_segment"].fillna("null")
    df["previous_supplier_name"] = df["previous_supplier_name"].fillna("null")
# def pre_clubbing_transformation():
#     df.drop("Unnamed: 0", axis=1, inplace=True)
#     df["round_age"] = df["vehicle_age"].round(0)
#     df["round_owner"] = round(pd.to_numeric(df['owner_sr'], downcast='integer', errors='coerce'), 0)
#     df["NCB"] = df["NCB"].astype(str)
#     df["previous_ncb"] = df["previous_ncb"].astype(str)
#     df["vehicle_details_segment"] = df["vehicle_details_segment"].fillna("null")
#     df["previous_supplier_name"] = df["previous_supplier_name"].fillna("null")
#     df["type_of_cng_kit"] = df["type_of_cng_kit"].fillna("null")
#
#     df["revised_is_cng_fitted"] = df["is_cng_fitted"].apply(lambda x: "Kit_Is" if x > 0 else "No_Kit")
#     df["revised_bi_fuel_kit"] = df["is_bi_fuel_kit_liability"].apply(
#         lambda x: "Liability" if x > 0 else "Zero_Liability")
#     df["revised_is_cng_fitted"] = df["revised_is_cng_fitted"] + df["type_of_cng_kit"] + df["revised_bi_fuel_kit"]
#     df["ncb_composite"] = df["previous_ncb"] + "_" + df["NCB"]
#     df["opted_kms_New"] = df["opted_kms"].apply(lambda x: group_opted_kms(x) if x < 10000 else "_High Usage")
#     df["opted_kms_New"] = df["opted_kms_New"].fillna("null")
#     df["revised_plan_category"] = df["new_plan_category"] + df["opted_kms_New"]
#     df["revised_plan_category"] = df["revised_plan_category"].apply(lambda x: correct_plan_name(x))
#     df.drop(["is_claims_made_in_previous_policy", "type_of_cng_kit", "NCB", "previous_ncb",
#              "opted_kms",
#              "is_tp_pd_liability", "is_bi_fuel_kit_liability", "is_cng_fitted", "new_plan_category", "opted_kms_New"],
#             axis=1, inplace=True)


df = pd.read_csv("Output\\ModelGammaInputCombined.csv")
# df = pd.read_csv("Output\\ModelGammaInput.csv")
# df = pd.read_csv("CSV\\FixedMultiplier\\Combined_final_file.csv")
# df.rename(columns={"Claim count": "Claim_Count"}, inplace=True)
df["Pred_total"] = df["Pred_Cost_NL"] + df["Pred_Cost_ttl"]
# df["Pred_total"] = df["Pred_Cost_NL"]
pre_clubbing_transformation()

# ----------------------------------------------- Clubbing
df["vehicle_age_new"] = df["round_age"].apply(lambda x: group_age(x))
df["make_name_new"] = df["make_name"].apply(lambda x: group_make(x))
df["model_name_new"] = df["model_name"].apply(lambda x: group_model(x))
df["transmission_type_new"] = df["transmission_type"].apply(lambda x: group_transmission_type(x))
df["fuel_type_new"] = df["fuel_type"].apply(lambda x: group_fuel_type(x))
df["cubic_capacity_new"] = df["cubic_capacity"].apply(lambda x: group_cubic_capacity(x))
df["vehicle_details_segment_new"] = df["vehicle_details_segment"].apply(lambda x: group_vehicle_segment(x))
df["supplier_name_new"] = df["supplier_name"].apply(lambda x: group_insurer(x))
df["registration_rto_code_new"] = df["registration_rto_code"].apply(lambda x: group_rto(x))
df["seating_capacity_new"] = df["seating_capacity"].apply(lambda x: group_seating_capacity(x))
df["revised_plan_category_new"] = df["revised_plan_category"].apply(lambda x: group_plan(x))
df["ncb_composite_new"] = df["ncb_composite"].apply(lambda x: group_composite_ncb(x))
df["revised_is_cng_fitted_new"] = df["revised_is_cng_fitted"].apply(lambda x: group_cng(x))
df["lead_day_slot_new"] = df["lead_day_slot"].apply(lambda x: group_lead_day(x))
df["t_booking_new"] = df["t_booking"].apply(lambda x: group_booking(x))
df["t_parent_new"] = df["t_parent"].apply(lambda x: group_parent(x))
df["previous_supplier_name_new"] = df["previous_supplier_name"].apply(lambda x: group_previous_insurer(x))
df["owner_sr_new"] = df["round_owner"].apply(lambda x: group_owner_sr(x))
df["previous_policy_type_new"] = df["previous_policy_type"].apply(lambda x: group_previous_policy_type(x))
df = df[~ df["vehicle_age_new"].str.contains("-0.0_years", na=False)]
# -----------------------------------------------  Clubbing End

df["vehicle_age_ttl"] = df["round_age"].apply(lambda x: group_age_ttl(x))
df["make_name_ttl"] = df["make_name"].apply(lambda x: group_make_ttl(x))
df["state_name_ttl"] = df["registered_state_name"].apply(lambda x: group_state_ttl(x))
df["fuel_type_ttl"] = df["fuel_type"].apply(lambda x: group_fuel_type_ttl(x))
df["cubic_capacity_ttl"] = df["cubic_capacity"].apply(lambda x: group_cubic_capacity_ttl(x))

# df.to_csv("Output\\4WheelerLossCostCombinedFile.csv")

# df.to_csv("Output\\4WheelerUnClubbedLossCostFile.csv")
prepare_tweedie_file()
