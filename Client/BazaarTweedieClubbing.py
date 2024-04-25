import pandas as pd
import duckdb as db


def prepare_tweedie_file():
    q3 = """select  Zone_new, cc_New, 
           Insurer_new, makename_new,
           sum(PAID_AMT) as PAID_AMT,sum(Claim_Count) as Claim_Count, 
           sum(LIVES_EXPOSED) as LIVES_EXPOSED               
            from df            
            group by  Insurer_new, makename_new, 
                      Zone_new, cc_New           
     """

    output = db.execute(q3).df()

    output.to_csv("Bazaar\\Output\\4WheelerLargeFiles.csv")


def group_insurer(x):
    if x in ["Oriental Pvt Car Comp", "NIA Pvt car comp satp bkgs apr 16 t"]:
        return "1Insurer_Group1"
    elif x in ["FG Pvt Car Data Upda", "KGI SATP+COMP Pvt Car", "Oriental Pvt Car SATP", "Shriram Pvt Car Comp+ SATP"]:
        return "Insurer_Group5"
    elif x in ["Bajaj Pvt Car SATP", "National Pvt Car SATP", "United Comp SATP PVT"]:
        return "Insurer_Group3"
    elif x in ["Bajaj Pvt Car Comp", "Liberty Pvt Car COMP+SA", "SBI Pvt Car Comp+SATP"]:
        return "Insurer_Group2"
    else:
        return "Insurer_Others"


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
    if x in ["MARUTI"]:
        return "1MARUTI"
    elif x in ["FORD", "CHEVROLET", "HONDA", "SKODA"]:
        return "Make_Group6"
    elif x in ["HYUNDAI", "TATA"]:
        return x
    elif x in ["MAHINDRA AND MAHINDRA", "VOLKSWAGEN"]:
        return "Make_Group4"
    else:
        return "Make_Others"


def group_fuel(x):
    if x in ["Diesel"]:
        return "Diesel"
    else:
        return "1Petrol"


def group_zone(x):
    if x in ["North", "South"]:
        return "1North"
    else:
        return "EastWest"


def group_cc(x):
    if x in ["Below 1000cc", "1000 to 1500cc"]:
        return "1000 to 1500cc"
    else:
        return x


def group_AY(x):
    if x in [2019, 2021, 2022]:
        return 3
    if x in [2020]:
        return 2
    if x in [2023]:
        return 4
    if x in [2018]:
        return 1


def make_pivots(dataframe, columns):
    df2 = pd.pivot_table(dataframe, values="PAID_AMT  LIVES_EXPOSED".split(), columns=columns,
                         aggfunc="sum").T
    df2["Actual"] = df2["PAID_AMT"] / df2["LIVES_EXPOSED"]
    df2.to_csv("Bazaar\\Output\\Sep\\" + columns + ".csv")


def othering(dataframe):
    make_pivots(dataframe, "Insurer_new")
    make_pivots(dataframe, "Zone_new")
    make_pivots(dataframe, "cc_new")
    make_pivots(dataframe, "makename_new")
    make_pivots(dataframe, "Accident_Year_new")


def find_separation():
    df_ = pd.read_csv("Bazaar\\Output\\4WheelerFiles.csv")
    othering(df_)


df = pd.read_csv("4Wheeler - Large Loss.csv")
df["roundage"] = df["roundage"].apply(pd.to_numeric, errors="coerce")
df["PAID_AMT"] = df["PAID_AMT"].fillna(0)
df = df[~ df["Insurer"].str.contains("Revised Pvt Car COMP S")]
df = df[df["Accident_Year"].isin([2018, 2019, 2020, 2021, 2022, 2023])]
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
df.to_csv("Bazaar\\Output\\4WheelerLargeLossFile.csv")
prepare_tweedie_file()
# find_separation()
