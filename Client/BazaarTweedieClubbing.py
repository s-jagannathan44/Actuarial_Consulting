import pandas as pd
import duckdb as db


def prepare_tweedie_file():
    q3 = """select Insurer_new,  Zone_new, plancategory_new, roundage_new, cc_New, 
           makename_new, fuel_new, Accident_Year_new,              
           sum(PAID_AMT) as PAID_AMT,sum(Claim_Count) as Claim_Count, 
           sum(LIVES_EXPOSED) as LIVES_EXPOSED, sum(EP) as EARNED_PREMIUM               
            from df            
            group by  Insurer_new, plancategory_new, roundage_new, makename_new, fuel_new, Accident_Year_new, 
                      Zone_new, cc_New           
     """

    output = db.execute(q3).df()

    output.to_csv("Bazaar\\Output\\4WheelerFiles.csv")


def group_insurer(x):
    if x in ["National Pvt Car Comp", "National Pvt Car SATP", "Zuno_Pvt_Car_COMP_SATP"]:
        return "1Insurer_Group 1"
    elif x in ["NIA Pvt car comp satp bkgs apr 16 t"]:
        return "1Insurer_Group 1"
    elif x in ["FG Pvt Car Data Upda", "Oriental Pvt Car Comp"]:
        return "Insurer_Group 3"
    elif x in ["Bajaj Pvt Car Comp", "Liberty Pvt Car COMP+SA"]:
        return "Insurer_Group 2"
    elif x in ["Oriental Pvt Car SATP", "Universal Sompo Pvt Car Comp+SATP"]:
        return "Insurer_Group 4"
    elif x in ["RSA Pvt Car COMP+SATP", "United Comp SATP PVT"]:
        return "United RSA"
    elif x in ["Shriram Pvt Car Comp+ SATP", "Bajaj Pvt Car SATP"]:  # , "NIA Pvt car comp satp bkgs apr 16 t"]:
        return x
    else:
        return "Insurer_Others"


def group_plancategory(x):
    if x in ["03. TP"]:
        return "TP"
    else:
        return "COMP"


def group_roumdage(x):
    if x in [3, 5, 6, 12, 13]:
        return "1Age_Group 3"
    elif x in [4, 8, 9]:
        return "Age_Group 5"
    elif x in [1, 7, 10]:
        return "Age_Group 4"
    elif x in [2, 14]:
        return "1Age_Group 3"
    elif x in [0, 18, 19, -1]:
        return "Age_Group 1"
    elif x in [11]:
        return "Age_G11"
    else:
        return "Age_Others"


def group_makename(x):
    if x in ["FORD", "MARUTI", "TATA"]:
        return "1Make_Group 1"
    elif x in ["HYUNDAI", "HONDA", "SKODA"]:
        return "Make_Group 2"
    elif x in ["RENAULT", "VOLKSWAGEN"]:
        return "Make_Group 3"
    elif x in ["TOYOTA", "MAHINDRA AND MAHINDRA"]:
        return "1Make_Group 1"
    elif x in ["CHEVROLET"]:
        return "1Make_Group 1"
    else:
        return "1Make_Group 1"


def group_fuel(x):
    if x in ["Diesel"]:
        return "Diesel"
    else:
        return "1Petrol"


def group_zone(x):
    if x in ["North", "East", "West"]:
        return "NEW"
    else:
        return x


def group_cc(x):
    if x in ["Below 1000cc", "1000 to 1500cc"]:
        return "1000 to 1500cc"
    else:
        return x


def group_AY(x):
    if x in [2020]:
        return 1
    if x in [2019, 2021]:
        return 2
    if x in [2022]:
        return 3
    if x in [2023]:
        return 4
    if x in [2024]:
        return 5


def make_pivots(dataframe, columns):
    df2 = pd.pivot_table(dataframe, values="PAID_AMT  LIVES_EXPOSED".split(), columns=columns,
                         aggfunc="sum").T
    df2["Actual"] = df2["PAID_AMT"] / df2["LIVES_EXPOSED"]
    df2.to_csv("Bazaar\\Output\\Sep\\" + columns + ".csv")


def othering(dataframe):
    make_pivots(dataframe, "Insurer_new")
    make_pivots(dataframe, "Zone_new")
    make_pivots(dataframe, "cc_new")
    make_pivots(dataframe, "fuel_new")
    make_pivots(dataframe, "plancategory_new")
    make_pivots(dataframe, "roundage_new")
    make_pivots(dataframe, "makename_new")
    make_pivots(dataframe, "Accident_Year_new")


def find_separation():
    df_ = pd.read_csv("Bazaar\\Output\\4WheelerFiles.csv")
    othering(df_)


df = pd.read_csv("4Wheeler.csv")
df["roundage"] = df["roundage"].apply(pd.to_numeric, errors="coerce")
df = df[~ df["Insurer"].str.contains("Revised Pvt Car COMP S")]
df = df[df["Accident_Year"].isin([2021, 2022, 2023, 2024])]
df.dropna(subset=["Zone_1"], inplace=True)
df.dropna(subset=["cubiccapacity_New"], inplace=True)
df["Insurer_new"] = df["Insurer"].apply(lambda x: group_insurer(x))
df["Zone_new"] = df["Zone_1"].apply(lambda x: group_zone(x))
df["plancategory_new"] = df["newplancategory"].apply(lambda x: group_plancategory(x))
df["roundage_new"] = df["roundage"].apply(lambda x: group_roumdage(x))
df["cc_new"] = df["cubiccapacity_New"].apply(lambda x: group_cc(x))
df["makename_new"] = df["makename"].apply(lambda x: group_makename(x))
df["fuel_new"] = df["fuel"].apply(lambda x: group_fuel(x))
df["Accident_Year_new"] = df["Accident_Year"].apply(lambda x: group_AY(x))
df.to_csv("Bazaar\\Output\\4Wheeler2023&4File.csv")
# prepare_tweedie_file()
# find_separation()
