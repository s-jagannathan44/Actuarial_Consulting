import pandas as pd
import duckdb as db


def prepare_tweedie_file():
    q3 = """select  Zone_1, cubiccapacity_New,
           Insurer_new, plancategory_new, roundage_new, makename_new, fuel_new,
           sum(Ep) as EARNED_PREMIUM,sum(Claim_Amount) as PAID_AMT,sum(Claim_Count) as Claim_Count, 
           sum(Exposure) as LIVES_EXPOSED                       
            from df            
            group by  Insurer_new, plancategory_new, roundage_new, makename_new, fuel_new, 
                      Zone_1, cubiccapacity_New           
     """

    output = db.execute(q3).df()

    output.to_csv("Bazaar\\Output\\4WheeleerFile.csv")


def group_insurer(x):
    if x in ["National Pvt Car SATP", "Bajaj Pvt Car Comp"]:
        return x
    elif x in ["Bajaj Pvt Car SATP", "Oriental Pvt Car Comp"]:
        return "Oriental Bajaj"
    else:
        return "Others"


def group_plancategory(x):
    if x in ["03. TP"]:
        return "TP"
    else:
        return "COMP"


def group_roumdage(x):
    if x in [4, 13]:
        return "Group 3"
    elif x in [3, 6, 8, 7, 10, 12]:
        return "Group 1"
    elif x in [5, 9, 11]:
        return "Group 2"
    else:
        return "Others"


def group_makename(x):
    if x in ["HYUNDAI", "TOYOTA", "CHEVROLET", "VOLKSWAGEN"]:
        return "Group 1"
    elif x in ["TOYOTA", "MAHINDRA AND MAHINDRA"]:
        return "Group 2"
    elif x in ["MARUTI", "HONDA"]:
        return "Group 3"
    else:
        return "Others"


def group_fuel(x):
    if x in ["Petrol", "Diesel"]:
        return x
    else:
        return "Diesel"


df = pd.read_csv("4Wheeler.csv")

df["roundage"] = df["roundage"].apply(pd.to_numeric, errors="coerce")
df = df[~ df["Insurer"].str.contains("Revised Pvt Car COMP S")]
df["Claim_Amount"].fillna(0, inplace=True)
df.dropna(subset=["Zone_1"], inplace=True)
df = df[df["Claim_Amount"] < 10000000]
df["Insurer_new"] = df["Insurer"].apply(lambda x: group_insurer(x))
df["plancategory_new"] = df["newplancategory"].apply(lambda x: group_plancategory(x))
df["roundage_new"] = df["roundage"].apply(lambda x: group_roumdage(x))
df["makename_new"] = df["makename"].apply(lambda x: group_makename(x))
df["fuel_new"] = df["fuel"].apply(lambda x: group_fuel(x))
df["roundage_new"].fillna("Others", inplace=True)
prepare_tweedie_file()
