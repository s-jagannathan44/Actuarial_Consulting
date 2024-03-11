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
    if x in ["Bajaj Pvt Car Comp"]:
        return x
    elif x in ["National Pvt Car SATP", "National Pvt Car Comp", "RSA Pvt Car COMP+SATP"]:
        return "National RSA"
    elif x in ["Zuno_Pvt_Car_COMP_SATP", "Universal Sompo Pvt Car Comp+SATP", "Liberty Pvt Car COMP+SA"]:
        return "Group 3"
    elif x in ["FG Pvt Car Comp+SATP", "Shriram Pvt Car Comp+ SATP"]:
        return "Group 5"
    elif x in ["Bajaj Pvt Car SATP", "Oriental Pvt Car Comp"]:
        return "Group 4"
    else:
        return "Group 1"


def group_plancategory(x):
    if x in ["TP"]:
        return "TP"
    else:
        return "COMP"


def group_roumdage(x):
    if x in [16, 18]:
        return "Group 1"
    elif x in [2, 5, 6, 12, 14]:
        return "Group 2"
    elif x in [3, 7, 10, 13]:
        return "Group 3"
    elif x in [0, 1, 8]:
        return "Group 4"
    elif x in [4, 9, 11, 20]:
        return "Group 5"
    else:
        return "Others"


def group_makename(x):
    if x in ["TOYOTA", 'FIAT', "DATSUN", "Jeep"]:
        return "Group 2"
    elif x in ["FORD", "RENAULT", "MITSUBISHI", "SKODA"]:
        return "Group 1"
    elif x in ["AUDI", "MAHINDRA AND MAHINDRA"]:
        return "Group 3"
    elif x in ["HONDA", "CHEVROLET"]:
        return "HONDA"
    elif x in ["MARUTI", "TATA"]:
        return "MARUTI"
    elif x in ["HYUNDAI"]:
        return x
    else:
        return "Other"


def group_fuel(x):
    if x in ["Petrol", "Diesel"]:
        return x
    else:
        return "Diesel"


df = pd.read_csv("4Wheeler.csv")
df = df[~ df["Insurer"].str.contains("Revised Pvt Car COMP S")]
df["Claim_Amount"].fillna(0, inplace=True)
df["roundage"].fillna("Group 1", inplace=True)
df.dropna(subset=["Zone_1"], inplace=True)
df = df[df["Claim_Amount"] < 10000000]
df["Insurer_new"] = df["Insurer"].apply(lambda x: group_insurer(x))
df["plancategory_new"] = df["newplancategory"].apply(lambda x: group_plancategory(x))
df["roundage_new"] = df["roundage"].apply(lambda x: group_roumdage(x))
df["makename_new"] = df["makename"].apply(lambda x: group_makename(x))
df["fuel_new"] = df["fuel"].apply(lambda x: group_fuel(x))

prepare_tweedie_file()
