import pandas as pd
import duckdb as db


def prepare_tweedie_file():
    q3 = """select make_name_new,model_name_new,transmission_type,fuel_type_new,previous_supplier_name_new,
             vehicle_details_segment_new,supplier_name_new,policy_type,registration_rto_code_new,seating_capacity_new,
             cc_range,revised_plan_category_new,NCB,age_range,idv_slot_new, revised_is_cng_fitted_new,
             is_health_pb_customer,is_claims_made_in_previous_policy,is_two_wheeler_pb_customer,is_travel_pb_customer, is_term_life_pb_customer,
             lead_day_slot_new,expiry_type_new,is_ep,is_coc,is_rsa,is_key_rep,is_inpc,is_bi_fuel_kit_liability,is_tp_pd_liability,                  
             sum(Ultimate_PAID) as PAID_AMT,sum(Claim_Count) as Claim_Count, 
             sum(Normalized_LIVES_EXPOSED) as LIVES_EXPOSED                
             from df            
              group by make_name_new,model_name_new,transmission_type,fuel_type_new,previous_supplier_name_new,
             vehicle_details_segment_new,supplier_name_new,policy_type,registration_rto_code_new,seating_capacity_new,
             cc_range,revised_plan_category_new,NCB,age_range,idv_slot_new, revised_is_cng_fitted_new,
             is_health_pb_customer,is_claims_made_in_previous_policy,is_two_wheeler_pb_customer,is_travel_pb_customer, is_term_life_pb_customer,
             lead_day_slot_new,expiry_type_new,is_ep,is_coc,is_rsa,is_key_rep,is_inpc,is_bi_fuel_kit_liability,is_tp_pd_liability            
       """
    output = db.execute(q3).df()
    output.to_csv("Output\\4WheelerFile.csv")


def group_rto(x):
    if x in ["DL4"]:
        return "Group 1"
    elif x in ["UK08", "HR03", "AP31", "AS06"]:
        return "Group 2"
    elif x in ["DL7", "DL6", "DL8", "DL3", "AS01"]:
        return "Group 3"
    if x in ["HR01", "DL2", "MH02", "DL1", "RJ14", "DL9", "WB06", "HR05", "MH04", "KA02"]:
        return "Group 4"
    elif x in ["UK06", "WB74", "KA05", "KA53", "MH01", "KA19", "MH03", "DL12", "MH46", "MH05", "KA03", "DL5", "CG07",
               "KA09", "KL01", "MH43", "WB02", "HR29", "UP15", "KA51", "KA04", "WB26", "UK07", "UP80", "MH31", "HR10"]:
        return "Group 5"
    elif x in ["MH12", "MH20", "RJ20", "GJ06", "HR06", "MH48", "JH05", "HR51", "PB08", "TN09", "PB65", "MH14", "JK02",
               "KL07", "UP14", "HR20", "KA01", "UP70", "TS09", "PB02"]:
        return "Group 6"
    if x in ["UP65", "GJ01", "RJ02", "DL10", "PB10", "CH01", "TN11", "TS07", "MH15", "MP04", "TN10", "TN22", "JH10",
             "HR26", "OD02", "UP16", "UK04", "DL14", "UP78", "GJ05", "GJ27"]:
        return "Group 7"
    elif x in ["TS08", "GJ03", "GJ18", "MH09", "RJ19", "HR12", "MH47", "MP20", "UP53", "MP09", "BR06", "JH01", "UP25",
               "TN07", "BR01"]:
        return "Group 8"
    elif x in ["RJ27", "GJ15", "HR36", "MH49", "UP32", "CG04"]:
        return "Group 9"
    if x in ["UP81", "TN14"]:
        return "Group 10"
    else:
        return "Others"


def group_model(x):
    if x in ["NANO", "OMNI", "SPARK"]:
        return "Group 1"
    elif x in ["A STAR", "BEAT", "ESTILO 1.0  NEW", "SANTRO XING"]:
        return "Group 2"
    elif x in ["ALTO", "Sx4"]:
        return "Group 3"
    if x in ["i 10 1.1", "INDICA VISTA", "RITZ"]:
        return "Group 4"
    elif x in ["ALTO 800", "ALTO K10", "BRIO", "EON", "i 10 1.2 KAPPA"]:
        return "Group 5"
    elif x in ["BOLERO", "EECO"]:
        return "Group 6"
    if x in ["GO", "KUV100", "Redi-GO", "SWIFT DZIRE KB", "WAGON R", "ZEST"]:
        return "Group 7"
    elif x in ["FIGO", "S-Presso", "SWIFT DZIRE", "SWIFT DZIRE (2017)", "TUV300"]:
        return "Group 8"
    elif x in ["CELERIO"]:
        return "Group 9"
    if x in ["ETIOS", "LIVA", "GRAND i10", "INNOVA	Kwid", "SWIFT"    "XCENT", "XUV500"]:
        return "Group 10"
    elif x in ["DUSTER", "ETIOS", "IGNIS", "SCORPIO M", "HAWK"]:
        return "Group 11"
    elif x in ["ERTIGA", "FLUIDIC VERNA", "i 20", "JAZZ", "POLO", "SANTRO"]:
        return "Group 12"
    if x in ["AMAZE", "TIAGO", "VENTO"]:
        return "Group 13"
    elif x in ["BALENO", "CITY", "DZIRE", "ECOSPORT", "Figo Aspire", "NEW CITY"]:
        return "Group 14"
    elif x in ["CIAZ", "Grand i10 Nios", "i20 (2018)", "Punch", "TIGOR", "Vitara Brezza"]:
        return "Group 15"
    if x in ["AMAZE(2018)", "CRETA(2018)", "FREESTYLE", "NEXON", "RAPID", "S CROSS", "Triber", "WR-V"]:
        return "Group 16"
    elif x in ["CRETA", "Venue"]:
        return "Group 17"
    elif x in ["AURA", "Magnite", "SELTOS", "Sonet", "XUV300"]:
        return "Group 18"
    elif x in ["ALTROZ", "VERNA"]:
        return "Group 19"
    else:
        return "Others"


def group_previous_insurer(x):
    if x in ["National Insurance Company Ltd", "Acko General Insurance", "Bajaj Allianz General Insurance Company Ltd",
             "Navi General Insurance", "The New India Assurance Co. Ltd.", "Zurich Kotak General Insurance",
             "Magma HDI General Insurance"]:
        return "Group 1"
    elif x in ["DIGIT General Insurance", "Reliance General Insurance Company Ltd",
               "Iffco Tokio General Insurance Company Ltd", "Zuno General Insurance",
               "Cholamandalam MS General Insurance Company Ltd", "The Oriental Insurance Company Ltd",
               "Royal Sundaram Alliance Insurance Company Ltd", "SBI General Insurance Company Ltd",
               "Raheja QBE General Insurance Company"]:
        return "Group 2"
    elif x in ["Future Generali", "Universal Sompo General Insurance Company Ltd",
               "HDFC Ergo General Insurance Company Ltd", "Tata AIG General Insurance Company ltd.",
               "ICICI Lombard General Insurance Company Ltd", "Bharti Axa"]:
        return "Group 3"
    if x in ["United India Insurance Company Ltd", "Liberty General Insurance Co. Ltd"]:
        return "Group 4"
    else:
        return "Others"


def group_lead_day(x):
    if x in ["daytime", "evening"]:
        return "Day"
    else:
        return "Night"


def group_expiry_type(x):
    if x in ["Active", "BreakIn"]:
        return "Group 1"


def group_make(x):
    if x in ["MARUTI", "MAHINDRA AND MAHINDRA", "TOYOTA"]:
        return x
    elif x in ["FORD", "HONDA", "TATA"]:
        return "Group 1"
    elif x in ["RENAULT", "HYUNDAI"]:
        return "1Group 2"
    else:
        return "Others"


def group_cng(x):
    if x in ["Kit_Is_CompanyFitted", "Kit_Is_ExternallyFitted"]:
        return x
    else:
        return "No Kit"


def group_seating_capacity(x):
    if x in [5, 7, 8]:
        return x
    else:
        return "Others"


def group_insurer(x):
    if x in ["National Insurance Company Ltd", "Shriram General Insurance Company Ltd"]:
        return "Group 1"
    elif x in ["Iffco Tokio General Insurance Company Ltd", "Royal Sundaram Alliance Insurance Company Ltd"]:
        return "Group 2"
    elif x in ["The New India Assurance Co. Ltd.", "SBI General Insurance Company Ltd"]:
        return "1Group 3"
    if x in ["Raheja QBE General Insurance Company", "Liberty General Insurance Co. Ltd"]:
        return "Group 4"
    elif x in ["Zuno General Insurance", "The Oriental Insurance Company Ltd", "Future Generali"]:
        return "Group 5"
    elif x in ["Bajaj Allianz General Insurance Company Ltd", "Magma HDI General Insurance"]:
        return "Group 6"
    elif x in ["United India Insurance Company Ltd"]:
        return x
    else:
        return "Group 7"


def group_fuel_type(x):
    if x in ["Petrol"]:
        return "1 Petrol"
    elif x in ["Diesel"]:
        return x
    else:
        return "CNG+"


def group_vehicle_segment(x):
    if x in ["COMPACT CARS", "MIDSIZE CARS", "SPORTS AND UTILITY VEHICLES"]:
        return x
    if x in ["MULTI UTILITY VEHICLES", "null"]:
        return "Group 1"
    else:
        return "Others"


def group_idv_slot(x):
    if x in ["100000-125000", "125000-150000", "150000-175000", "175000-200000", "200000-225000", "225000-250000",
             "Others"]:
        return x
    elif x in ["0-80000", "80000-100000"]:
        return "Group 1"
    elif x in ["275000-300000", "300000-325000"]:
        return "Group 2"
    elif x in ["325000-350000", "350000-375000"]:
        return "Group 3"
    elif x in ["375000-400000", "400000-425000"]:
        return "Group 4"
    elif x in ["425000-450000", "450000-475000"]:
        return "Group 5"
    elif x in ["475000-500000", "500000-550000"]:
        return "Group 6"
    elif x in ["550000-600000", "600000-650000", "650000-700000", "700000-750000"]:
        return "Group 7"
    else:
        return "Above 7.5 lacs"


def group_opted_kms(x):
    if x in [0, 2500, 3000, 5000]:
        return "_Low Usage"
    elif x in [5500, 7000, 7500, 8500]:
        return "_Medium Usage"
    else:
        return "_null"


def group_plan(x):
    if x in ["02. Comp With ZD", "05. SAOD + ZD", "07. PAYD_High usage"]:
        return x
    elif x in ["01. Comp", "08. PAYD + SAOD_Low Usage"]:
        return "01. Group 1"
    elif x in ["09. PAYD + ZD_Low Usage", "06. SAOD + PG"]:
        return "Group 3"
    elif x in ["04. SAOD", "09. PAYD + ZD_Medium Usage", "10. PAYD + SAOD + ZD_Medium Usage",
               "08. PAYD + SAOD_Medium Usage",
               "10. PAYD + SAOD + ZD_Low Usage", "08. PAYD + SAOD_High usage"]:
        return "Group 4"
    elif x in ["09. PAYD + ZD_High usage", "12. PG + ZD", "15. Long Term", "10. PAYD + SAOD + ZD_High usage",
               "13. PG + SAOD + ZD"]:
        return "Group 5"
    else:
        return "Others"


def correct_plan_name(x):
    if "PAYD" in x:
        return x
    else:
        return x.split("_", 1)[0]


df = pd.read_csv("CSV\\Ultimate_fixed.csv")

df["IDV_Ratio"] = df["incurred"] / df["sum_insured"]
# df = df[~ df["cause_of_loss"].str.contains("Theft of entire vehicle", na=False)]
# df = df[~ df["cause_of_loss"].str.contains("Theft", na=False)]
# df = df[~ df["cause_of_loss"].str.contains("Theft of Entire Vehicle", na=False)]
# df = df[~ df["cause_of_loss"].str.contains("THEFT-VEHICLE", na=False)]
# df = df[~ df["cause_of_loss"].str.contains("Theft - Vehicle", na=False)]
# df = df[~ df["cause_of_loss"].str.contains("Theft of Vehicle", na=False)]
# df = df[~ df["cause_of_loss"].str.contains("Total Loss", na=False)]
# df["is_non_large"] = df["IDV_Ratio"].apply(lambda x: "N" if x > 0.399 else "Y")
df = df[df["cause_of_loss"].isin(["Theft of entire vehicle", "Theft", "Theft of Entire Vehicle", "THEFT-VEHICLE", "Theft - Vehicle", "Theft of Vehicle", "Total Loss"])]
# df = df[~ df["IDV_Ratio"] > 0.3999]
# df = df[df["IDV_Ratio"] < 0.47]
# df = df[df["is_non_large"] == 'N']

df["NCB"] = df["NCB"].astype(str)
df["previous_ncb"] = df["previous_ncb"].astype(str)
# df["opted_kms"] = df["opted_kms"].astype(str)
df.rename(columns={"Claim count": "Claim_Count"}, inplace=True)

df["vehicle_details_segment"] = df["vehicle_details_segment"].fillna("null")
df["revised_is_cng_fitted"] = df["is_cng_fitted"].apply(lambda x: "Kit_Is" if x > 0 else "No_Kit")
df["revised_bi_fuel_kit"] = df["is_bi_fuel_kit_liability"].apply(lambda x: "Liability" if x > 0 else "Zero_Liability")
df["is_cng_fitted"] = df["is_cng_fitted"].fillna("null")
df["type_of_cng_kit"] = df["type_of_cng_kit"].fillna("null")
df["revised_is_cng_fitted"] = df["revised_is_cng_fitted"] + df["type_of_cng_kit"] + df["revised_bi_fuel_kit"]
df["ncb_composite"] = df["previous_ncb"] + "_" + df["NCB"]

df["opted_kms_New"] = df["opted_kms"].apply(lambda x: group_opted_kms(x) if x < 10000 else "_High Usage")
df["revised_plan_category"] = df["new_plan_category"] + df["opted_kms_New"]
df["revised_plan_category"] = df["revised_plan_category"].apply(lambda x: correct_plan_name(x))
df.drop(["is_claims_made_in_previous_policy", "type_of_cng_kit", "Unnamed: 0", "Unnamed: 0.1", "NCB", "previous_ncb",
         "opted_kms",
         "is_tp_pd_liability", "is_bi_fuel_kit_liability", "is_cng_fitted", "new_plan_category", "opted_kms_New"],
        axis=1, inplace=True)

df.to_csv("Output\\theft_total_loss_model_file.csv")
#
# df["revised_plan_category_new"] = df["revised_plan_category"].apply(lambda x: group_plan(x))
# df["revised_is_cng_fitted_new"] = df["revised_is_cng_fitted"].apply(lambda x: group_cng(x))
#
# df["lead_day_slot_new"] = df["lead_day_slot"].apply(lambda x: group_lead_day(x))
# df["expiry_type_new"] = df["expiry_type"].apply(lambda x: group_expiry_type(x))
# df["registration_rto_code_new"] = df["registration_rto_code"].apply(lambda x: group_rto(x))
# df["model_name_new"] = df["model_name"].apply(lambda x: group_model(x))
# df["make_name_new"] = df["make_name"].apply(lambda x: group_make(x))
# df["seating_capacity_new"] = df["seating_capacity"].apply(lambda x: group_seating_capacity(x))
# df["supplier_name_new"] = df["supplier_name"].apply(lambda x: group_insurer(x))
# df["fuel_type_new"] = df["fuel_type"].apply(lambda x: group_fuel_type(x))
# df["vehicle_details_segment_new"] = df["vehicle_details_segment"].apply(lambda x: group_vehicle_segment(x))
# df["idv_slot_new"] = df["idv_slot"].apply(lambda x: group_idv_slot(x))
# df["previous_supplier_name_new"] = df["previous_supplier_name"].apply(lambda x: group_previous_insurer(x))
# prepare_tweedie_file()
