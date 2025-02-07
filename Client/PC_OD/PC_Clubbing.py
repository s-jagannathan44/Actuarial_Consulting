import pandas as pd
import duckdb as db


def prepare_tweedie_file():
    q3 = """select vehicle_age_new, make_name_new, model_name_new,  transmission_type_new,  fuel_type_new, cubic_capacity_new,   
            vehicle_details_segment_new, supplier_name_new, policy_type, registration_rto_code_new, seating_capacity_new,
             revised_plan_category_new, ncb_composite_new, revised_is_cng_fitted_new,
              is_travel_pb_customer,  lead_day_slot_new, t_booking_new, previous_insurer_type, previous_policy_type_new,                   
             sum(ultimate_paid_non_large) as PAID_AMT,sum(Claim_Count) as Claim_Count, sum(sum_insured_in_hundreds) as IDV, 
             sum(Normalized_LIVES_EXPOSED) as LIVES_EXPOSED , sum(ultimate_paid_non_large) / sum(sum_insured_in_hundreds) as IDV_Loss_Cost            
             from df            
              group by   vehicle_age_new, make_name_new, model_name_new,  transmission_type_new,  fuel_type_new, cubic_capacity_new,   
            vehicle_details_segment_new, supplier_name_new, policy_type, registration_rto_code_new, seating_capacity_new,
             revised_plan_category_new, ncb_composite_new, revised_is_cng_fitted_new,
              is_travel_pb_customer,  lead_day_slot_new, t_booking_new, previous_insurer_type, previous_policy_type_new
       """
    output = db.execute(q3).df()
    output.to_csv("Output\\4WheelerFile.csv")


def group_age(x):
    if x in [7, 8, 9, 10, 11]:
        return "7 to 11"
    elif x in [4, 6]:
        return str(x) + "_years"
    elif x in [0, 2, 5]:
        return "Group 1"
    elif x in [1, 3]:
        return "Group 2"
    else:
        return "Above 12"


def group_cubic_capacity(x):
    if x in [796, 1461]:
        return "Group 1"
    elif x in [814, 998, 1086, 1198, 1493, 1497]:
        return "Group 2"
    elif x in [1197, 1199, 1248, 1498]:
        return "Group 3"
    elif x in [799, 999, 1396]:
        return "Group 4"
    else:
        return "Others"


def group_composite_ncb(x):
    if x in ["50.0_50.0", "45.0_50.0"]:
        return x
    elif x in ["35.0_45.0", "25.0_35.0", "20.0_25.0", "50.0_0.0"]:
        return "Group 3"
    elif x in ["0.0_20.0", "45.0_0.0"]:
        return "Group 4"
    else:
        return "Group 0"


def group_rto(x):
    if x in ["DL4"]:
        return "Group 1"
    elif x in ["TS09", "KA53", "HR03", "AS01", "TS07", "KA03", "DL1", "DL7", "KA05", "Dl12", "DL8", "KA09"]:
        return "Group 2"
    elif x in ["KA01", "MH01", "DL6", "DL3", "CH01", "KA19", "KA04", "Dl10", "DL9", "AP31", "MH02", 'KA51', "TS08",
               "HR05", "UK08", "MH47", "UP80", "MH03"]:
        return "Group 3"
    elif x in ["RJ14", "DL2", "HR06", "UP16", "DL14", "HR10", "MH46", "TN09", "KA02", "DL5", "HR51", "HR26", "WB06",
               "KL01", "PB65", "KL07", "MH04", "OD02", "UP14", "MH12", "HR01", "PB02", "HR29", "MH14", "MH05", "MH48",
               "GJ06", "UP65", "WB74", "MH43", "UK07", "PB08"]:
        return "Group 4"
    elif x in ["CG07", "UP15", "MH20", "GJ01", "HR12", "UK06", "AP39", "MH31", "MH15", "TN07", "MP04", "GJ18", "JH01",
               "UP70", "JH10", "BR06", "WB02", "JH05", "TN11", "HR20", "TN10"]:
        return "Group 5"
    elif x in ["JK02", "RJ02", "MP20", "MP09", "UK04", "RJ20", "UP25", "PB10", "GJ03", "WB26", "UP78", "UP53", "MH09",
               "TN14", "RJ19", "GJ05", "HR36"]:
        return "Group 6"
    elif x in ["TN22", "MH49", "GJ27", "UP32", "GJ15", "BR01", "RJ27", "CG04", "RJ45"]:
        return "Group 7"
    else:
        return "Others"


def group_model(x):
    if x in ["BOLERO", "XUV500", "SCORPIO M HAWK"]:
        return "Group 1"
    elif x in ["SANTRO XING", "BEAT", "EECO"]:
        return "Group 2"
    elif x in ["RITZ", "BRIO", "ALTO", "i 10 1.1", "DUSTER"]:
        return "Group 3"
    elif x in ["i 10 1.2 KAPPA", "SELTOS", "ALTO 800", "CRETA", "ALTO K10"]:
        return "Group 4"
    elif x in ["ERTIGA", "WAGON R", "SWIFT DZIRE KB", "EON", "ECOSPORT", "NEXON", "CITY", "IGNIS", "SWIFT DZIRE"]:
        return "Group 5"
    elif x in ["FLUIDIC VERNA", "JAZZ", "Venue", "XCENT", "FIGO", "GRAND i10"]:
        return "Group 6"
    elif x in ["Vitara Brezza", "WR-V", "SWIFT", "CELERIO", "ETIOS", "NEW CITY", "SANTRO", "AMAZE", "i 20", "TIGOR",
               "TIAGO"]:
        return "Group 7"
    elif x in ["POLO", "CIAZ", "DZIRE", "BALENO", "Kwid", "Figo Aspire", "ALTROZ"]:
        return "Group 8"
    else:
        return "Others"


def group_previous_insurer(x):
    if x in ["National Insurance Company Ltd", "Bajaj Allianz General Insurance Company Ltd",
             "DIGIT General Insurance", "The New India Assurance Co. Ltd.", "Zurich Kotak General Insurance",
             ]:
        return "Group 1"
    elif x in ["null", "Reliance General Insurance Company Ltd", "Acko General Insurance", "Magma HDI General Insurance"
                                                                                           "Cholamandalam MS General Insurance Company Ltd",
               "The Oriental Insurance Company Ltd", "Liberty General Insurance Co. Ltd"
                                                     "HDFC Ergo General Insurance Company Ltd",
               "Tata AIG General Insurance Company ltd."
               ]:
        return "Group 2"
    elif x in ["Royal Sundaram Alliance Insurance Company Ltd"
               "Raheja QBE General Insurance Company", "L&T", "Navi General Insurance",
               "ICICI Lombard General Insurance Company Ltd", "United India Insurance Company Ltd"]:
        return "Group 3"
    elif x in ["Future Generali", "Universal Sompo General Insurance Company Ltd", "SBI General Insurance Company Ltd",
               "Bharti Axa", "Iffco Tokio General Insurance Company Ltd"]:
        return "Group 4"
    elif x in ["Zuno General Insurance"]:
        return "ZUNO"
    else:
        return "Others"


def group_lead_day(x):
    if x in ["daytime", "evening", "early", "night"]:
        return "Group 1"
    else:
        return "Late Night"


def group_previous_policy_type(x):
    if x in [0]:
        return "None"
    elif x in [1]:
        return "Comp"
    elif x in [2]:
        return "TP  Cover"
    else:
        return "Addon Cover"


def group_owner_sr(x):
    if x in [0, 1]:
        return "New"
    elif x in [-1, 2, 3]:
        return "Group 1"
    else:
        return "Others"


def group_make(x):
    if x in ["MARUTI", "HYUNDAI", "TATA", "FORD"]:
        return "Group 1"
    elif x in ["RENAULT", "HONDA", "VOLKSWAGEN"]:
        return "Group 2"
    elif x in ["MAHINDRA AND MAHINDRA", "CHEVROLET"]:
        return "Group 3"
    elif x in ["TOYOTA", "KIA"]:
        return "Group 4"
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
    if x in [5]:
        return "5 seater"
    elif x in [7, 6]:
        return "7/6 seater"
    elif x in [8, 4]:
        return "8/4 seater"
    else:
        return "Others"


def group_insurer(x):
    if x in ["National Insurance Company Ltd", "The New India Assurance Co. Ltd."]:
        return "Group 1"
    elif x in ["Zurich Kotak General Insurance", "Shriram General Insurance Company Ltd",
               "Magma HDI General Insurance"]:
        return "Group 2"
    elif x in ["The Oriental Insurance Company Ltd", "Liberty General Insurance Co. Ltd"]:
        return "Group 3"
    elif x in ["United India Insurance Company Ltd", "Royal Sundaram Alliance Insurance Company Ltd",
               "Future Generali"]:
        return "Group 4"
    elif x in ["Bajaj Allianz General Insurance Company Ltd", "Zuno General Insurance",
               "Reliance General Insurance Company Ltd", "Cholamandalam MS General Insurance Company Ltd"]:
        return x


def group_fuel_type(x):
    if x in ["Petrol", "Diesel", "Electric"]:
        return "Group 1"
    elif x in ["CNG", "LPG"]:
        return "CNG+"


def group_transmission_type(x):
    if x in [0]:
        return "Manual"
    else:
        return "Group 2"


def group_vehicle_segment(x):
    if x in ["COMPACT CARS", "MIDSIZE CARS"]:
        return x
    if x in ["SPORTS AND UTILITY VEHICLES"]:
        return "SUV"
    if x in ["null"]:
        return "BLANK"
    else:
        return "Others"


def group_plan(x):
    if x in ["02. Comp With ZD", "05. SAOD + ZD"]:
        return x
    elif x in ["01. Comp", "09. PAYD + ZD_Low Usage"]:
        return "01. Comp"
    elif x in ["07. PAYD_Medium Usage", "06. SAOD + PG", "11. PG"]:
        return "Group 1"
    elif x in ["10. PAYD + SAOD + ZD_Low Usage", "15. Long Term", "08. PAYD + SAOD_High Usage", "04. SAOD"]:
        return "Group 2"
    elif x in ["07. PAYD_High Usage", "09. PAYD + ZD_Medium Usage", "12. PG + ZD", "13. PG + SAOD + ZD"]:
        return "Group 4"
    elif x in ["09. PAYD + ZD_High Usage", "16. Long Term With ZD", "10. PAYD + SAOD + ZD_High Usage"]:
        return "Group 5"
    else:
        return "Others"


def group_booking(x):
    if x in [0, 1, 2]:
        return "0 to 2"
    if x in [30, 16, -50]:
        return "Group 1"
    if x in [15, -91, 7, 10, 9, -3, -1, 14, 12, -49, 11, 3, 6, 13, 17, 4,
             5, -2, 8]:
        return "Group 2"
    else:
        return "Others"


def group_parent(x):
    if x in [0]:
        return "Zero"
    if x in [3, 6, 59, 60, 7, 4, 58, 57, 5, 1, 2]:
        return "Group 1"
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


def pre_clubbing_transformation():
    df.drop("Unnamed: 0", axis=1, inplace=True)
    df["round_age"] = df["vehicle_age"].round(0)
    df["NCB"] = df["NCB"].astype(str)
    df["previous_ncb"] = df["previous_ncb"].astype(str)
    df["vehicle_details_segment"] = df["vehicle_details_segment"].fillna("null")
    df["previous_supplier_name"] = df["previous_supplier_name"].fillna("null")
    df["type_of_cng_kit"] = df["type_of_cng_kit"].fillna("null")

    df["revised_is_cng_fitted"] = df["is_cng_fitted"].apply(lambda x: "Kit_Is" if x > 0 else "No_Kit")
    df["revised_bi_fuel_kit"] = df["is_bi_fuel_kit_liability"].apply(
        lambda x: "Liability" if x > 0 else "Zero_Liability")
    df["revised_is_cng_fitted"] = df["revised_is_cng_fitted"] + df["type_of_cng_kit"] + df["revised_bi_fuel_kit"]
    df["ncb_composite"] = df["previous_ncb"] + "_" + df["NCB"]
    df["opted_kms_New"] = df["opted_kms"].apply(lambda x: group_opted_kms(x) if x < 10000 else "_High Usage")
    df["opted_kms_New"] = df["opted_kms_New"].fillna("null")
    df["revised_plan_category"] = df["new_plan_category"] + df["opted_kms_New"]
    df["revised_plan_category"] = df["revised_plan_category"].apply(lambda x: correct_plan_name(x))
    df.drop(["is_claims_made_in_previous_policy", "type_of_cng_kit", "NCB", "previous_ncb",
             "opted_kms",
             "is_tp_pd_liability", "is_bi_fuel_kit_liability", "is_cng_fitted", "new_plan_category", "opted_kms_New"],
            axis=1, inplace=True)


df = pd.read_csv("CSV\\FixedMultiplier\\Combined_final_file.csv")
df.rename(columns={"Claim count": "Claim_Count"}, inplace=True)
pre_clubbing_transformation()

# ----------------------------------------------- Clubbing
df["vehicle_age_new"] = df["vehicle_age"].apply(lambda x: group_age(x))
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
df["owner_sr_new"] = df["owner_sr"].apply(lambda x: group_owner_sr(x))
df["previous_policy_type_new"] = df["previous_policy_type"].apply(lambda x: group_previous_policy_type(x))
# -----------------------------------------------  Clubbing End
prepare_tweedie_file()
