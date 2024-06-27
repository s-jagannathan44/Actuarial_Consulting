import pandas as pd
import duckdb as db


def prepare_tweedie_file():
    q3 = """select  
           cc_large, body_type_large,Zone_large,Make_large,Insurer_large,
           sum(PAID_AMT) as PAID_AMT,sum(Count) as Claim_Count, sum(EP) as EP, 
           sum(LIVES_EXPOSED) as LIVES_EXPOSED                       
            from df            
            group by cc_large, body_type_large,Zone_large,Make_large,Insurer_large 
     """

    output = db.execute(q3).df()

    output.to_csv("Bazaar\\TW\\CSV\\Files\\Output\\2WheelerNewLargeFiles.csv")


def group_zone(x):
    if x in ["North", "South", "West"]:
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


def group_plan(x):
    return x


def group_make(x):
    if x in ["HERO HONDA", "HONDA"]:
        return "1HONDA"
    elif x in ["YAMAHA", "Bajaj"]:
        return "Group 2"
    elif x in ["HERO MOTOCORP", "TVS"]:
        return x
    else:
        return "Others"


def group_Insurer(x):
    if x in ["BAGIC 2W COMP+SATP Bookings", "National 2W Comp+SATP Bookings"]:
        return "1Group 1"
    elif x in ["Oriental SATP +COMP booking", "FG 2W Comp+SATP Booking", "United 2W Comp+SATP Bookings"]:
        return "Group 2"
    elif x in ["NIA Comp+SATP Bookings"]:
        return x
    else:
        return "Others"


def make_pivots(dataframe, columns):
    df2 = pd.pivot_table(dataframe, values="PAID_AMT  LIVES_EXPOSED".split(), columns=columns,
                         aggfunc="sum").T
    df2["Actual"] = df2["PAID_AMT"] / df2["LIVES_EXPOSED"]
    df2.to_csv("Bazaar\\TW\\CSV\\Files\\Output\\Sep\\" + columns + ".csv")


def othering(dataframe):
    make_pivots(dataframe, "Zone_large")
    make_pivots(dataframe, "body_type_large")
    make_pivots(dataframe, "Make_large")
    make_pivots(dataframe, "cc_large")
    make_pivots(dataframe, "Insurer_large")
    # make_pivots(dataframe, "PlanType_large")
    # make_pivots(dataframe, "Accident_Year_large")


def find_separation():
    df_ = pd.read_csv("Bazaar\\TW\\CSV\\Files\\Output\\2WheelerNewLargeFiles.csv")
    othering(df_)


df = pd.read_csv("Bazaar\\TW\\CSV\\Files\\Output\\2WheelerFull.csv")
df["Age"] = df["Age"].apply(pd.to_numeric, errors="coerce")
df["PAID_AMT"].fillna(0, inplace=True)
df["Zone_large"] = df["Zone"].apply(lambda x: group_zone(x))
df["cc_large"] = df["ccnew"].apply(lambda x: group_cc(x))
df["body_type_large"] = df["body_type"].apply(lambda x: group_body_type(x))
df["Make_large"] = df["Make"].apply(lambda x: group_make(x))
# df["PlanType_new"] = df["plan_category"].apply(lambda x: group_plan(x))
df["Insurer_large"] = df["Insurer"].apply(lambda x: group_Insurer(x))
# df["Accident_Year_new"] = df["Accident_Year"].apply(lambda x: group_AY(x))
# prepare_tweedie_file()
df.to_csv("Bazaar\\TW\\CSV\\Files\\Output\\2WheelerFullFile.csv")
# find_separation()
