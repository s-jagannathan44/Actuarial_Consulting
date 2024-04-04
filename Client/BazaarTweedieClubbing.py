import pandas as pd
import duckdb as db


def prepare_tweedie_file():
    q3 = """select  Zone_new, cc_New, Accident_Year_new, 
           Insurer_Fuel_new, plancategory_new, roundage_new, makename_new,
           sum(PAID_AMT) as PAID_AMT,sum(Claim_Count) as Claim_Count, 
           sum(LIVES_EXPOSED) as LIVES_EXPOSED                       
            from df            
            group by  Insurer_Fuel_new, plancategory_new, roundage_new, makename_new,  Accident_Year_new, 
                      Zone_new, cc_New           
     """

    output = db.execute(q3).df()

    output.to_csv("Bazaar\\Output\\4WheeleerFiles.csv")


def group_insurer_fuel(x):
    if x in ["National Pvt Car SATP_Petrol"]:
        return x
    if x in ["Chola Pvt Car Comp+SATP_Diesel", "Oriental Pvt Car Comp_Diesel"]:
        return "Group 1"
    if x in ["National Pvt Car SATP_Diesel", "Oriental Pvt Car Comp_Petrol", "SBI Pvt Car Comp+SATP_Petrol"]:
        return "Group 2"
    elif x in ["Bajaj Pvt Car SATP_Petrol", "Oriental Pvt Car SATP_Petrol", "Shriram Pvt Car Comp+ SATP_Diesel", "Shriram Pvt Car Comp+ SATP_Petrol"]:
        return "Group 3"
    elif x in ["Bajaj Pvt Car Comp_Petrol", "Chola Pvt Car Comp+SATP_Petrol", "SBI Pvt Car Comp+SATP_CNG"]:
        return "Group 4"
    elif x in ["FG Pvt Car Comp+SATP_Diesel", "National Pvt Car Comp_Diesel", "Universal Sompo Pvt Car Comp+SATP_Petrol"]:
        return "Group 6"
    elif x in ["FG Pvt Car Comp+SATP_Petrol", "National Pvt Car Comp_Petrol"]:
        return "Group 7"
    else:
        return "1Others"


def group_plancategory(x):
    if x in ["03. TP"]:
        return "TP"
    else:
        return "COMP"


def group_roumdage(x):
    if x in [3, 4]:
        return "G"+str(x)
    elif x in [9, 11]:
        return "Group 2"
    elif x in [7, 8, 19]:
        return "Group 4"
    elif x in [2, 5]:
        return "Group 5"
    elif x in [6, 10, 18]:
        return "Group 6"
    else:
        return "1Others"


def group_makename(x):
    if x in ["HONDA", "TATA"]:
        return "Group 3"
    elif x in ["HYUNDAI"]:
        return x
    elif x in ["MARUTI"]:
        return "1MARUTI"
    else:
        return "Others"



def group_zone(x):
    if x in ["North", "East"]:
        return "1North"
    else:
        return x


def group_cc(x):
    if x in ["Above 1500cc", "1000 to 1500cc"]:
        return "1Group 1"
    else:
        return x


def group_AY(x):
    if x in [2021]:
        return 1
    elif x in [2022]:
        return 2
    elif x in [2023]:
        return 3


def make_pivots(dataframe, columns):
    df2 = pd.pivot_table(dataframe, values="PAID_AMT  LIVES_EXPOSED".split(), columns=columns,
                         aggfunc="sum").T
    df2["Actual"] = df2["PAID_AMT"] / df2["LIVES_EXPOSED"]
    df2.to_csv("Bazaar\\Output\\Sep\\" + columns + ".csv")


def othering(dataframe):
    make_pivots(dataframe, "Insurer_Fuel_new")
    make_pivots(dataframe, "Zone_new")
    make_pivots(dataframe, "cc_new")
    make_pivots(dataframe, "plancategory_new")
    make_pivots(dataframe, "roundage_new")
    make_pivots(dataframe, "makename_new")
    make_pivots(dataframe, "Accident_Year_new")


def find_separation():
    df_ = pd.read_csv("Bazaar\\Output\\4WheeleerFiles.csv")
    othering(df_)


df = pd.read_csv("4Wheeler.csv")
df["roundage"] = df["roundage"].apply(pd.to_numeric, errors="coerce")
df = df[~ df["Insurer"].str.contains("Revised Pvt Car COMP S")]
df["PAID_AMT"].fillna(0, inplace=True)
df.dropna(subset=["Zone_1"], inplace=True)
df["Insurer_Fuel_new"] = df["Insurer_Fuel"].apply(lambda x: group_insurer_fuel(x))
df["Zone_new"] = df["Zone_1"].apply(lambda x: group_zone(x))
df["plancategory_new"] = df["newplancategory"].apply(lambda x: group_plancategory(x))
df["roundage_new"] = df["roundage"].apply(lambda x: group_roumdage(x))
df["cc_new"] = df["cubiccapacity_New"].apply(lambda x: group_cc(x))
df["makename_new"] = df["makename"].apply(lambda x: group_makename(x))
df["roundage_new"].fillna("Others", inplace=True)
df["Accident_Year_new"] = df["Accident_Year"].apply(lambda x: group_AY(x))
df.to_csv("Bazaar\\Output\\4WheelerTestFile.csv")
prepare_tweedie_file()
find_separation()
