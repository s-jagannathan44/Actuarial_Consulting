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
    elif x in ["National Pvt Car Comp", "Zuno_Pvt_Car_COMP_SATP", "Liberty Pvt Car COMP+SA"]:
        return "Group 1"

    else:
        return "1Others"


def group_plancategory(x):
    if x in ["03. TP"]:
        return "TP"
    else:
        return "COMP"


def group_roumdage(x):
    if x in [4, 13]:
        return "Group 3"
    elif x in [3, 5, 6, 8, 7, 10, 12]:
        return "Group 1"
    elif x in [9, 11]:
        return "Group 2"
    else:
        return "Others"


def group_makename(x):
    if x in ["HYUNDAI", "TATA", "CHEVROLET", "VOLKSWAGEN"]:
        return "Group 1"
    elif x in ["TOYOTA", "MAHINDRA AND MAHINDRA"]:
        return "Group 2"
    elif x in ["MARUTI", "HONDA"]:
        return "1Group 3"
    else:
        return "Others"


def group_fuel(x):
    if x in ["Petrol"]:
        return "1Petrol"
    else:
        return "Diesel"


def group_zone(x):
    if x in ["North"]:
        return "1North"
    else:
        return x


def make_pivots(dataframe, columns):
    df2 = pd.pivot_table(dataframe, values="PAID_AMT  LIVES_EXPOSED".split(), columns=columns,
                         aggfunc="sum").T
    df2["Actual"] = df2["PAID_AMT"] / df2["LIVES_EXPOSED"]
    df2.to_csv("Bazaar\\Output\\Sep\\" + columns + ".csv")


def othering(dataframe):
    make_pivots(dataframe, "Insurer_new")
    make_pivots(dataframe, "Zone_1")
    make_pivots(dataframe, "cubiccapacity_New")
    make_pivots(dataframe, "fuel_new")
    make_pivots(dataframe, "plancategory_new")
    make_pivots(dataframe, "roundage_new")
    make_pivots(dataframe, "makename_new")


def find_separation():
    df_ = pd.read_csv("Bazaar\\Output\\4WheeleerFile.csv")
    othering(df_)


df = pd.read_csv("4Wheeler.csv")

df["roundage"] = df["roundage"].apply(pd.to_numeric, errors="coerce")
df = df[~ df["Insurer"].str.contains("Revised Pvt Car COMP S")]
df["Claim_Amount"].fillna(0, inplace=True)
df.dropna(subset=["Zone_1"], inplace=True)
df = df[df["Claim_Amount"] < 10000000]
df["Insurer_new"] = df["Insurer"].apply(lambda x: group_insurer(x))
df["Zone_1"] = df["Zone_1"].apply(lambda x: group_zone(x))
df["plancategory_new"] = df["newplancategory"].apply(lambda x: group_plancategory(x))
df["roundage_new"] = df["roundage"].apply(lambda x: group_roumdage(x))
df["makename_new"] = df["makename"].apply(lambda x: group_makename(x))
df["fuel_new"] = df["fuel"].apply(lambda x: group_fuel(x))
df["roundage_new"].fillna("Others", inplace=True)
df.to_csv("Bazaar\\Output\\4WheelerTestFile.csv")
prepare_tweedie_file()
find_separation()
