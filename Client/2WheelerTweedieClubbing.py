import pandas as pd
import duckdb as db


def prepare_tweedie_file():
    q3 = """select  
           Accident_Year_new,Zone_new,cc_Make_new,Insurer_PlanType_new,body_type_new,Age_new, 
           sum(PAID_AMT) as PAID_AMT,sum(Count) as Claim_Count, 
           sum(LIVES_EXPOSED) as LIVES_EXPOSED                       
            from df            
            group by  Accident_Year_new,Zone_new,cc_Make_new,Insurer_PlanType_new,body_type_new,Age_new         
     """

    output = db.execute(q3).df()

    output.to_csv("Bazaar\\TW\\CSV\\Files\\Output\\2WheeleerNewFiles.csv")


def group_age(x):
    if x in [4, 10]:
        return "G" + str(x)
    elif x in [5, 3]:
        return "Group 1"
    elif x in [7, 13]:
        return "Group 3"
    elif x in [9, 6, 8]:
        return "1Group 4"
    elif x in [8, 11]:
        return "Group 5"
    elif x in [14, 12]:
        return "Group 6"
    elif x in [2, 16]:
        return "Group 6"
    else:
        return "Others"


def group_zone(x):
    if x in ["North", "South"]:
        return "1North"
    else:
        return x


def group_AY(x):
    if x in [2022]:
        return 1
    elif x in [2023]:
        return 2
    #  Forecast Years
    elif x in [2024]:
        return 3


def group_body_type(x):
    return x


def group_cc_make(x):
    if x in ["HONDA_75 to 150cc"]:
        return "1HONDA_75"
    elif x in ["HERO MOTOCORP_75 to 150cc", "YAMAHA_75 to 150cc"]:
        return "Group 2"
    elif x in ["ROYAL ENFIELD_150 to 350cc", "Bajaj_75 to 150cc"]:
        return "Group 3"
    elif x in ["HERO HONDA_75 to 150cc", "TVS_75 to 150cc"]:
        return "Group 4"
    else:
        return "Others"


def group_Insurer_PlanType(x):
    if x in ["Comp_CHOLA 2W COMP+SATP Booking", "Comp_Liberty Comp+SATP Bookings 2"]:
        return "Group 1"
    elif x in ["TP_Oriental SATP +COMP booking", "TP_Liberty Comp+SATP Bookings 2"]:
        return "Group 2"
    elif x in ["Comp_NIA Comp+SATP Bookings", "TP_NIA Comp+SATP Bookings"]:
        return "NIA"
    elif x in ["Comp_BAGIC 2W COMP+SATP Bookings", "TP_United 2W Comp+SATP Bookings"]:
        return x
    elif x in ["TP_BAGIC 2W COMP+SATP Bookings"]:
        return "1TP_Bajaj"
    elif x in ["Comp_Oriental SATP +COMP booking", "Comp_United 2W Comp+SATP Bookings"]:
        return "Group 5"
    else:
        return "Others"


def make_pivots(dataframe, columns):
    df2 = pd.pivot_table(dataframe, values="PAID_AMT  LIVES_EXPOSED".split(), columns=columns,
                         aggfunc="sum").T
    df2["Actual"] = df2["PAID_AMT"] / df2["LIVES_EXPOSED"]
    df2.to_csv("Bazaar\\TW\\CSV\\Files\\Output\\Sep\\" + columns + ".csv")


def othering(dataframe):
    make_pivots(dataframe, "Zone_new")
    make_pivots(dataframe, "body_type_new")
    make_pivots(dataframe, "cc_Make_new")
    make_pivots(dataframe, "Insurer_PlanType_new")
    make_pivots(dataframe, "Age_new")
    make_pivots(dataframe, "Accident_Year_new")


def find_separation():
    df_ = pd.read_csv("Bazaar\\TW\\CSV\\Files\\Output\\2WheeleerNewFiles.csv")
    othering(df_)


df = pd.read_csv("2Wheeler_Forecast.csv")
df["Age"] = df["Age"].apply(pd.to_numeric, errors="coerce")
df["PAID_AMT"].fillna(0, inplace=True)
df["Zone_new"] = df["Zone"].apply(lambda x: group_zone(x))
df["Age_new"] = df["Age"].apply(lambda x: group_age(x))
df["body_type_new"] = df["body_type"].apply(lambda x: group_body_type(x))
df["cc_Make_new"] = df["cc_Make"].apply(lambda x: group_cc_make(x))
df["Insurer_PlanType_new"] = df["Insurer_PlanType"].apply(lambda x: group_Insurer_PlanType(x))
df["Accident_Year_new"] = df["Accident_Year"].apply(lambda x: group_AY(x))
df.to_csv("Bazaar\\TW\\CSV\\Files\\Output\\2WheelerNewForecastFile.csv")

