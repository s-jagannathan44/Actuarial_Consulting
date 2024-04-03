import pandas as pd
import duckdb as db


def prepare_frequency_file():
    q3 = """select  State_new, cubiccapacity_New, 
           Insurer_new, plancategory_new, roundage_new, make_model_new, fuel_new,
           sum(Claim_Count) as Claim_Count, 
           sum(LIVES_EXPOSED) as LIVES_EXPOSED                       
            from df            
            group by  Insurer_new, plancategory_new, roundage_new, make_model_new, fuel_new,  
                      State_new, cubiccapacity_New           
     """

    output = db.execute(q3).df()

    output.to_csv("Bazaar\\Output\\4WheeleerFrequencies.csv")


def group_insurer(x):
    if x in ["Oriental Pvt Car Comp"]:
        return x
    if x in ["National Pvt Car Comp", "National Pvt Car SATP"]:
        return "1National"
    elif x in ["Shriram Pvt Car Comp+ SATP", "FG Pvt Car Comp+SATP"]:
        return "Group 1"
    elif x in ["Bajaj Pvt Car SATP", "Bajaj Pvt Car Comp"]:
        return "Bajaj"
    else:
        return "Others"


def group_plancategory(x):
    if x in ["03. TP"]:
        return "TP"
    else:
        return "COMP"


def group_roumdage(x):
    if x in [1]:
        return "1"
    elif x in [2, 4, 5, 8, 9, 10, 12, 14, 17]:
        return "0Group 4"
    elif x in [7, 11, 18, 19]:
        return "Group 3"
    elif x in [3, 15]:
        return "Group 5"
    elif x in [0, 6]:
        return "Group 2"
    else:
        return "Others"


def group_make_model_name(x):
    if x in ["MARUTI_RITZ", "MARUTI_SWIFT DZIRE"]:
        return x
    elif x in ["CHEVROLET_BEAT", "MARUTI_ALTO 800", "MARUTI_BALENO", "MARUTI_OMNI", "VOLKSWAGEN_POLO"]:
        return "Group 3"
    elif x in ["FORD_FIGO", "HYUNDAI_GRAND i10", "HYUNDAI_SANTRO XING"]:
        return "Group 4"
    elif x in ["HYUNDAI_i 10 1.1", "HYUNDAI_i 10 1.2 KAPPA", "MARUTI_ALTO K10", "MARUTI_CELERIO", "MARUTI_SWIFT", "MARUTI_WAGON R"]:
        return "Group 5"
    elif x in ["HONDA_AMAZE", "HYUNDAI_EON", "HYUNDAI_i 20", "HYUNDAI_SANTRO", "MARUTI_ALTO", "MARUTI_ERTIGA", "MARUTI_ESTILO 1.0  NEW", "MARUTI_ZEN"]:
        return "Group 6"
    elif x in ["CHEVROLET_SPARK", "HONDA_NEW CITY", "MARUTI_800", "MARUTI_SWIFT DZIRE KB", "RENAULT_Kwid"]:
        return "Group 7"
    else:
        return "1Others"


def group_fuel(x):
    if x in ["Diesel"]:
        return "Diesel"
    else:
        return "1Petrol"


def group_State(x):
    if x in ["Chattisgarh", "Delhi", "Maharashtra", "TELANGANA"]:
        return "1Group 1"
    elif x in ["Bihar", "Chandigarh", "Himachal Pradesh", "Jammu and Kashmir", "Jharkhand", "Punjab", "UTTARAKHAND"]:
        return "Group 2"
    elif x in ["Andhra Pradesh", "Gujarat", "Orissa", "Rajasthan", "Uttar Pradesh"]:
        return "Group 3"
    elif x in ["Haryana", "West Bengal"]:
        return "Group 4"
    elif x in ["Assam", "Karnataka"]:
        return "Group 5"
    else:
        return "Others"


def make_pivots(dataframe, columns):
    df2 = pd.pivot_table(dataframe, values="Claim_Count  LIVES_EXPOSED".split(), columns=columns,
                         aggfunc="sum").T
    df2["Actual"] = df2["Claim_Count"] / df2["LIVES_EXPOSED"]
    df2.to_csv("Bazaar\\Output\\Sep\\" + columns + ".csv")


def othering(dataframe):
    make_pivots(dataframe, "Insurer_new")
    make_pivots(dataframe, "State_new")
    make_pivots(dataframe, "fuel_new")
    make_pivots(dataframe, "plancategory_new")
    make_pivots(dataframe, "roundage_new")
    make_pivots(dataframe, "make_model_new")
    make_pivots(dataframe, "cubiccapacity_New")


def find_separation():
    df_ = pd.read_csv("Bazaar\\Output\\4WheeleerFrequencies.csv")
    othering(df_)


# df = pd.read_csv("4WheelerFrequency.csv")
df = pd.read_csv("Bazaar\\Output\\4WheelerTestFrequency.csv")
df["roundage"] = df["roundage"].apply(pd.to_numeric, errors="coerce")
df = df[~ df["Insurer"].str.contains("Revised Pvt Car COMP S")]
df.dropna(subset=["registration_state"], inplace=True)
df["Insurer_new"] = df["Insurer"].apply(lambda x: group_insurer(x))
df["State_new"] = df["registration_state"].apply(lambda x: group_State(x))
df["plancategory_new"] = df["newplancategory"].apply(lambda x: group_plancategory(x))
df["roundage_new"] = df["roundage"].apply(lambda x: group_roumdage(x))
df["make_model_new"] = df["Make_Model"].apply(lambda x: group_make_model_name(x))
df["fuel_new"] = df["fuel"].apply(lambda x: group_fuel(x))
df["roundage_new"].fillna("Others", inplace=True)
df.to_csv("Bazaar\\Output\\OutofTime.csv")
# prepare_frequency_file()
# find_separation()
