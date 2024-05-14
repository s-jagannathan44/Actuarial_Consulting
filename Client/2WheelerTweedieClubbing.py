import pandas as pd
import duckdb as db


def prepare_tweedie_file():
    q3 = """select  
           plan_category,CC_new, Make_type_new, Accident_Year_new, Insurer_new, Zone_new,
           sum(PAID_AMT) as PAID_AMT,sum(Count) as Claim_Count, 
           sum(LIVES_EXPOSED) as LIVES_EXPOSED                       
            from df            
            group by  plan_category,CC_new, Make_type_new ,Accident_Year_new, Insurer_new,Zone_new         
     """

    output = db.execute(q3).df()

    output.to_csv("Bazaar\\TW\\CSV\\Files\\Output\\2WheeleerNewFiles.csv")


def group_age(x):
    if x in [10, 11]:
        return "G" + str(x)
    elif x in [5, 6]:
        return "1Group 3"
    elif x in [3, 4]:
        return "Group 1"
    elif x in [2, 8]:
        return "1Group 3"  # return "Group 5"
    elif x in [9, 13, 16]:
        return "Group 2"
    elif x in [7, 18]:
        return "1Group 3"  # return "Group 4"
    elif x in [12, 14]:
        return "Group 6"
    else:
        return "1Group 3"  # return "Others"


def group_zone(x):
    if x in ["North", "East"]:
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


def group_cc(x):
    if x in ["Below 75cc", "Above 350cc"]:
        return "Others"
    elif x in ["75 to 150cc"]:
        return "075 to 150cc"
    else:
        return x


def group_make_type(x):
    if x in ["HERO HONDA_Bike", "HERO MOTOCORP_Bike", "HONDA_Scooter", "TVS_Bike"]:
        return x
    elif x in ["YAMAHA_Bike", "BAJAJ_Bike", "HONDA_Bike"]:
        return "Bajaj+"
    elif x in ["ROYAL ENFIELD_Bike"]:
        return "Bajaj+"    # return "Royal Honda"
    else:
        return "Bajaj+"  # "Others"


def group_Insurer(x):
    if x in ["Bajaj 2w comp satp", "NIA 2W Comp SATP", "SGI 2W Bookings"]:
        return "Bajaj+"
    else:
        return x


def make_pivots(dataframe, columns):
    df2 = pd.pivot_table(dataframe, values="PAID_AMT  LIVES_EXPOSED".split(), columns=columns,
                         aggfunc="sum").T
    df2["Actual"] = df2["PAID_AMT"] / df2["LIVES_EXPOSED"]
    df2.to_csv("Bazaar\\TW\\CSV\\Files\\Output\\Sep\\" + columns + ".csv")


def othering(dataframe):
    make_pivots(dataframe, "Zone_new")
    make_pivots(dataframe, "CC_new")
    # make_pivots(dataframe, "makename_new")
    make_pivots(dataframe, "Make_type_new")
    make_pivots(dataframe, "plan_category")
    # make_pivots(dataframe, "Age_new")
    make_pivots(dataframe, "Accident_Year_new")
    make_pivots(dataframe, "Insurer_new")


def find_separation():
    df_ = pd.read_csv("Bazaar\\TW\\CSV\\Files\\Output\\2WheeleerNewFiles.csv")
    othering(df_)


df = pd.read_csv("2Wheeler_New.csv")
df.dropna(subset=["Zone"], inplace=True)
# df.dropna(subset=["ccnew"], inplace=True)
# df.dropna(subset=["Age"], inplace=True)
# df = df[df["Accident_Year"].isin([2023, 2024])]
df["Age"] = df["Age"].apply(pd.to_numeric, errors="coerce")
df["PAID_AMT"].fillna(0, inplace=True)
df["Zone_new"] = df["Zone"].apply(lambda x: group_zone(x))
df["Age_new"] = df["Age"].apply(lambda x: group_age(x))
df["CC_new"] = df["ccnew"].apply(lambda x: group_cc(x))
df["Make_type_new"] = df["Make_type"].apply(lambda x: group_make_type(x))
df["Insurer_new"] = df["Insurer"].apply(lambda x: group_Insurer(x))
df["Accident_Year_new"] = df["Accident_Year"].apply(lambda x: group_AY(x))
prepare_tweedie_file()
df.to_csv("Bazaar\\TW\\CSV\\Files\\Output\\2WheelerNewFile.csv")
find_separation()
