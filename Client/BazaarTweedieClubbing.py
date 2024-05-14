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
    if x in ["Chola Pvt Car Comp+SATP", "Oriental Pvt Car SATP", "Bajaj Pvt Car SATP", "Oriental Pvt Car Comp"]:
        return "1Insurer_Group 5"
    elif x in ["National Pvt Car Comp", "Liberty Pvt Car COMP+SA"]:
        return "Insurer_Group 2"
    elif x in ["FG Pvt Car Data Upda", "Universal Sompo Pvt Car Comp+SATP"]:
        return "Insurer_Group 3"
    elif x in ["Liberty Pvt Car COMP+SA", "National Pvt Car Comp"]:
        return "Insurer_Group 2"
    elif x in ["Shriram Pvt Car Comp+ SATP", "Bajaj Pvt Car Comp"]:
        return "Insurer_Group 4"
    elif x in ["RSA Pvt Car COMP+SATP", "United Comp SATP PVT", "KGI SATP+COMP Pvt Car", "Zuno_Pvt_Car_COMP_SATP"]:
        return "Insurer_Group 6"
    elif x in ["National Pvt Car SATP", "NIA Pvt car comp satp bkgs apr 16 t" , "SBI Pvt Car Comp+SATP"]:
        return x


def group_plancategory(x):
    if x in ["03. TP"]:
        return "TP"
    if x in ["02. Comp With ZD"]:
        return x
    else:
        return "02. COMP"


def group_roumdage(x):
    if x in [2, 5, 7, 8, 13]:
        return "1Age_Group 3"
    elif x in [9, 11]:
        return "Age_Group 5"
    elif x in [3, 12, 19]:
        return "Age_Group 4"
    elif x in [6, 10, 18]:
        return "Age_Group 2"
    elif x in [0, 14, 16, 17]:
        return "Age_Group 1"
    elif x in [4]:
        return "Age_G4"
    else:
        return "Age_Others"


def group_makename(x):
    if x in ["CHEVROLET", "MARUTI"]:
        return "1Make_Group 1"
    elif x in ["HYUNDAI", "RENAULT"]:
        return "Make_Group 2"
    elif x in ["TATA", "HONDA"]:
        return "Make_Group 4"
    elif x in ["TOYOTA", "MAHINDRA AND MAHINDRA"]:
        return "Make_Group 3"
    elif x in ["FORD"]:
        return x
    else:
        return "Make_Others"


def group_fuel(x):
    if x in ["Diesel"]:
        return "Diesel"
    elif x in ["Petrol"]:
        return "1Petrol"
    else:
        return "CNG+"


def group_zone(x):
    # if x in ["North",  "West"]:
    #     return "1NW"
    # else:
    return x


def group_cc(x):
    # if x in ["Below 1000cc", "1000 to 1500cc"]:
    #     return "1000 to 1500cc"
    # else:
    return x


def group_AY(x):
    return x


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
df = df[df["Accident_Year"].isin([2024])]
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
df.to_csv("Bazaar\\Output\\4WheelerPPT2024File.csv")
# prepare_tweedie_file()
# find_separation()
