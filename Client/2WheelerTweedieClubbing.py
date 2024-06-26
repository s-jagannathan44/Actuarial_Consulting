import pandas as pd
import duckdb as db


def prepare_tweedie_file():
    q3 = """select  
           Accident_Year_new , cc_New, body_type_new,Zone_new,Make_new,Insurer_new,
           sum(PAID_AMT) as PAID_AMT,sum(Count) as Claim_Count, sum(EP) as EP, 
           sum(LIVES_EXPOSED) as LIVES_EXPOSED                       
            from df            
            group by  Accident_Year_new , cc_New, body_type_new,Zone_new,Make_new,Insurer_new 
     """

    output = db.execute(q3).df()

    output.to_csv("Bazaar\\TW\\CSV\\Files\\Output\\2WheelerFinalFile.csv")


def group_zone(x):
    if x in ["South", 'East']:
        return "1SouthEast"
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


def group_InsurerType(x):
    if x in ["Public "]:
        return "1Public"
    else:
        return x


def group_make(x):
    if x in ["HONDA","HERO MOTOCORP", "Bajaj"]:
        return "1HONDA"
    elif x in ["HERO HONDA", "TVS"]:
        return x
    else:
        return "Others"


def group_Insurer(x):
    if x in ["National 2W Comp+SATP Bookings", "NIA Comp+SATP Bookings", "BAGIC 2W COMP+SATP Bookings",
             "Oriental SATP +COMP booking"]:
        return x
    elif x in ["United 2W Comp+SATP Bookings", "Liberty Comp+SATP Bookings 2"]:
        return "Group 2"
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
  #  make_pivots(dataframe, "InsurerType_new")
    make_pivots(dataframe, "Accident_Year_new")


def find_separation():
    df_ = pd.read_csv("Bazaar\\TW\\CSV\\Files\\Output\\2WheelerFinalFile.csv")
    othering(df_)


df = pd.read_csv("2Wheeler_New.csv")
df["Age"] = df["Age"].apply(pd.to_numeric, errors="coerce")
df["PAID_AMT"].fillna(0, inplace=True)
df["Zone_new"] = df["Zone"].apply(lambda x: group_zone(x))
df["cc_new"] = df["ccnew"].apply(lambda x: group_cc(x))
df["body_type_new"] = df["body_type"].apply(lambda x: group_body_type(x))
df["Make_new"] = df["Make"].apply(lambda x: group_make(x))
df["InsurerType_new"] = df["InsurerType"].apply(lambda x: group_InsurerType(x))
df["Insurer_new"] = df["Insurer"].apply(lambda x: group_Insurer(x))
df["Accident_Year_new"] = df["Accident_Year"].apply(lambda x: group_AY(x))
# prepare_tweedie_file()
df.to_csv("Bazaar\\TW\\CSV\\Files\\Output\\2WheelerForecast.csv")
# find_separation()
