import pandas as pd
import duckdb as db


def prepare_tweedie_file():
    q3 = """select vehicle_age_ttl, make_name_ttl, fuel_type_ttl, cubic_capacity_ttl, state_name_ttl,   
             sum(ultimate_paid_large_ttl) as PAID_AMT,sum(Claim_Count) as Claim_Count, sum(sum_insured_in_hundreds) as IDV, 
             sum(Normalized_LIVES_EXPOSED) as LIVES_EXPOSED , sum(ultimate_paid_large_ttl) / sum(sum_insured_in_hundreds) as IDV_Loss_Cost            
             from df            
              group by  vehicle_age_ttl, make_name_ttl, fuel_type_ttl, cubic_capacity_ttl, state_name_ttl
       """
    output = db.execute(q3).df()
    output.to_csv("Output\\4WheelerTTLFile.csv")


def group_age(x):
    if x in [0, 2, 5, 6, 8]:
        return "Group 1"
    elif x in [1, 3, 7]:
        return "Group 2"
    elif x in [4, 9, 12, 13, 16]:
        return "Group 3"
    else:
        return "Group 4"


def group_cubic_capacity(x):
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


def group_state(x):
    if x in ["Daman & Diu", "Haryana", "Madhya Pradesh", "Orissa", "Rajasthan", "Tamil Nadu"]:
        return "Group 1"
    elif x in ["Chandigarh", "Chattisgarh", "Delhi", "Goa", "Gujarat", "Himachal Pradesh", "Jammu and Kashmir",
               "Jharkhand", "Punjab", "Uttar Pradesh"]:
        return "Group 2"
    elif x in ["Andhra Pradesh", "Assam", "Bihar", "Kerala", "Maharashtra", "UTTARAKHAND"]:
        return "Group 4"
    else:
        return "Group 5"


def group_make(x):
    if x in ["MARUTI", "KIA", "HONDA"]:
        return "Maruti +"
    elif x in ["RENAULT", "FORD", "VOLKSWAGEN"]:
        return "Group 3"
    elif x in ["MAHINDRA AND MAHINDRA"]:
        return "M&M"
    else:
        return "Others"


def group_fuel_type(x):
    if x in ["Petrol", "Electric"]:
        return "Group 1"
    elif x in ["Diesel", "CNG", "LPG"]:
        return "CNG+"


def pre_clubbing_transformation():
    df.drop("Unnamed: 0", axis=1, inplace=True)
    df["round_age"] = df["vehicle_age"].round(0)


df = pd.read_csv("CSV\\FixedMultiplier\\Combined_final_file.csv")
df.rename(columns={"Claim count": "Claim_Count"}, inplace=True)
pre_clubbing_transformation()

# ----------------------------------------------- Clubbing
df["vehicle_age_ttl"] = df["round_age"].apply(lambda x: group_age(x))
df["make_name_ttl"] = df["make_name"].apply(lambda x: group_make(x))
df["state_name_ttl"] = df["registered_state_name"].apply(lambda x: group_state(x))
df["fuel_type_ttl"] = df["fuel_type"].apply(lambda x: group_fuel_type(x))
df["cubic_capacity_ttl"] = df["cubic_capacity"].apply(lambda x: group_cubic_capacity(x))
# -----------------------------------------------  Clubbing End

prepare_tweedie_file()
