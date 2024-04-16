import pandas as pd
import duckdb as db


def prepare_tweedie_file():
    q3 = """select  Zone_new, cc_New, Accident_Year_new, 
           Insurer_new, plancategory_new, roundage_new, makename_new, fuel_new,
           sum(PAID_AMT) as PAID_AMT,sum(Claim_Count) as Claim_Count, 
           sum(LIVES_EXPOSED) as LIVES_EXPOSED               
            from df            
            group by  Insurer_new, plancategory_new, roundage_new, makename_new, fuel_new, Accident_Year_new, 
                      Zone_new, cc_New           
     """

    output = db.execute(q3).df()

    output.to_csv("Bazaar\\Output\\4WheelerFiles.csv")


def group_insurer(x):
    if x in ["Bajaj Pvt Car Comp", "Bajaj Pvt Car SATP", "Oriental Pvt Car Comp",
               "NIA Pvt car comp satp bkgs apr 16 t"]:
        return "1 Group1"
    elif x in ["Liberty Pvt Car COMP+SA", "Oriental Pvt Car SATP", "SBI Pvt Car Comp+SATP"]:
        return "Group 2"
    elif x in ["Chola Pvt Car Comp+SATP", "Shriram Pvt Car Comp+ SATP"]:
        return "Group 4"
    elif x in ["FG Pvt Car Data Upda", "National Pvt Car SATP"]:
        return x
    else:
        return "Others"


def group_plancategory(x):
    if x in ["03. TP"]:
        return "TP"
    else:
        return "COMP"


def group_roumdage(x):
    if x in [4, 8, 9, 2, 12]:
        return "1Group 1"
    elif x in [7, 11, 14]:
        return "Group 3"
    elif x in [5, 10]:
        return "Group 4"
    elif x in [3, 1]:
        return "Group 2"
    else:
        return "Others"


def group_makename(x):
    if x in ["RENAULT", "MARUTI", "TATA"]:
        return "1Group 1"
    elif x in ["HYUNDAI", "HONDA", "CHEVROLET", "TOYOTA"]:
        return "Group 2"
    elif x in ["FORD", "MAHINDRA AND MAHINDRA"]:
        return "Group 3"
    else:
        return "Others"


def group_fuel(x):
    if x in ["Diesel"]:
        return "Diesel"
    else:
        return "1Petrol"


def group_zone(x):
    if x in ["North", "East"]:
        return "1North"
    else:
        return x


def group_cc(x):
    if x in ["Below 1000cc", "1000 to 1500cc"]:
        return "1000 to 1500cc"
    else:
        return x


def group_AY(x):
    if x in [2019, 2020, 2021]:
        return 1
    if x in [2022]:
        return 2


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


df = pd.read_csv("4Wheeler - Large Loss.csv")
df["roundage"] = df["roundage"].apply(pd.to_numeric, errors="coerce")
# df["PAID_AMT"].fillna(0, inplace=True)
df = df[~ df["Insurer"].str.contains("Revised Pvt Car COMP S")]
df = df[df["Accident_Year"].isin([2019, 2020, 2021, 2022])]
df.dropna(subset=["Zone_1"], inplace=True)
df["Insurer_new"] = df["Insurer"].apply(lambda x: group_insurer(x))
df["Zone_new"] = df["Zone_1"].apply(lambda x: group_zone(x))
df["plancategory_new"] = df["newplancategory"].apply(lambda x: group_plancategory(x))
df["roundage_new"] = df["roundage"].apply(lambda x: group_roumdage(x))
df["cc_new"] = df["cubiccapacity_New"].apply(lambda x: group_cc(x))
df["makename_new"] = df["makename"].apply(lambda x: group_makename(x))
df["fuel_new"] = df["fuel"].apply(lambda x: group_fuel(x))
# df["roundage_new"].fillna("Others", inplace=True)
df["Accident_Year_new"] = df["Accident_Year"].apply(lambda x: group_AY(x))
df.to_csv("Bazaar\\Output\\4WheelerTestFile.csv")
prepare_tweedie_file()
find_separation()
