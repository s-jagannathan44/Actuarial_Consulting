import pandas as pd
import duckdb as db


def prepare_tweedie_file():
    q3 = """select  
           Accident_Year_new,Zone_new,cc_New,Make_new,Insurer_new, body_type_new, 
           sum(PAID_AMT) as PAID_AMT,sum(Count) as Claim_Count, 
           sum(LIVES_EXPOSED) as LIVES_EXPOSED                       
            from df            
            group by  Accident_Year_new,Zone_new,cc_New,Make_new,Insurer_new, body_type_new         
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
    if x in ["North", "South", "East"]:
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


def group_cc(x):
    if x in ["75 to 150cc"]:
        return "075 to 150cc"
    elif x in ["150 to 350cc"]:
        return x
    else:
        return "Others"


def group_PlanType(x):
    if x in ["TP"]:
        return "1TP"
    else:
        return "COMP"


def group_make(x):
    if x in ["HONDA", "Bajaj"]:
        return "1HONDA"
    elif x in ["HERO MOTOCORP", "TVS", "HERO HONDA"]:
        return x
    else:
        return "Others"


def group_Insurer(x):
    if x in ["BAGIC 2W COMP+SATP Bookings", "United 2W Comp+SATP Bookings"]:
        return "1Group 3"
    elif x in ["ZUNO Comp+SATP Bookings 2", "SGI Comp+SATP Bookings 2", "Oriental SATP +COMP booking",
               "NIA Comp+SATP Bookings"]:
        return x
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
    make_pivots(dataframe, "Make_new")
    make_pivots(dataframe, "cc_new")
    make_pivots(dataframe, "Insurer_new")
    # make_pivots(dataframe, "PlanType_new")
    make_pivots(dataframe, "Accident_Year_new")


def find_separation():
    df_ = pd.read_csv("Bazaar\\TW\\CSV\\Files\\Output\\2WheeleerNewFiles.csv")
    othering(df_)


df = pd.read_csv("2Wheeler_New.csv")
df["Age"] = df["Age"].apply(pd.to_numeric, errors="coerce")
df["PAID_AMT"].fillna(0, inplace=True)
df["Zone_new"] = df["Zone"].apply(lambda x: group_zone(x))
# df["Age_new"] = df["Age"].apply(lambda x: group_age(x))
df["body_type_new"] = df["body_type"].apply(lambda x: group_body_type(x))
df["Make_new"] = df["Make"].apply(lambda x: group_make(x))
df["cc_new"] = df["ccnew"].apply(lambda x: group_cc(x))
df["Insurer_new"] = df["Insurer"].apply(lambda x: group_Insurer(x))
# df["PlanType_new"] = df["plan_category"].apply(lambda x: group_PlanType(x))
df["Accident_Year_new"] = df["Accident_Year"].apply(lambda x: group_AY(x))
prepare_tweedie_file()
df.to_csv("Bazaar\\TW\\CSV\\Files\\Output\\2WheelerNewFile.csv")
find_separation()
