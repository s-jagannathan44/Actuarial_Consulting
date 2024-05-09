import pandas as pd
import duckdb as db


def prepare_tweedie_file():
    q3 = """select  
           plan_category,Age_new, Accident_Year_new, CC_new, Make_type_new,Zone_new,
           sum(PAID_AMT) as PAID_AMT,sum(Count) as Claim_Count, 
           sum(LIVES_EXPOSED) as LIVES_EXPOSED                       
            from df            
            group by  plan_category,Age_new, Accident_Year_new, CC_new, Make_type_new, Zone_new          
     """

    output = db.execute(q3).df()

    output.to_csv("Bazaar\\TW\\CSV\\Files\\Output\\2WheeleerFiles.csv")


def group_age(x):
    if x in [11]:
        return "G" + str(x)
    elif x in [2, 8, 12 ,13]:
        return "1Group 2"
    elif x in [4, 6]:
        return "Group 1"
    elif x in [5, 7]:
        return "Group 4"
    elif x in [3, 10]:
        return "Group 3"
    elif x in [1, 9, 14, 15]:
        return "Group 5"
    else:
        return "Others"


def group_zone(x):
    if x in ["North"]:
         return "1North"
    else:
        return x


def group_AY(x):
    if x in [2020]:
        return 1
    elif x in [2021]:
        return 2
    elif x in [2022]:
        return 3
    #  Forecast Years
    elif x in [2023]:
        return 4
    elif x in [2024]:
        return 5


def group_cc(x):
    if x in ["Below 75cc", "Above 350cc"]:
        return "Others"
    elif x in ["75 to 150cc"]:
        return "075 to 150cc"
    else:
        return x


def group_make_type(x):
    if x in ["TVS_Bike", "MAHINDRA_Bike"]:
        return "TVS+"
    elif x in ["HERO HONDA_Bike", "HERO MOTOCORP_Bike", "BAJAJ_Bike", "ROYAL ENFIELD_Bike"]:
        return "1HERO HONDA"
    elif x in ["YAMAHA_Bike", "SUZUKI_Bike", "HONDA_Bike", "HONDA_Scooter"]:   # "BAJAJ_Bike", "ROYAL ENFIELD_Bike",
        return x
    else:
        return "Others"


def group_Insurer(x):
    if x in ["Bajaj 2w comp satp ", "SGI 2W Bookings"]:
        return "Bajaj"
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
    make_pivots(dataframe, "Age_new")
    # make_pivots(dataframe, "Accident_Year_new")
    make_pivots(dataframe, "Insurer_new")


def find_separation():
    df_ = pd.read_csv("Bazaar\\TW\\CSV\\Files\\Output\\2WheeleerFiles.csv")
    othering(df_)


df = pd.read_csv("2Wheeler_Forecast.csv")
# df.dropna(subset=["body_type"], inplace=True)
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
# prepare_tweedie_file()
df.to_csv("Bazaar\\TW\\CSV\\Files\\Output\\2WheelerForecastFile.csv")
# find_separation()
