import pandas as pd
import duckdb as db


def prepare_tweedie_file():
    q3 = """select  Zone_new, Accident_Year_new,
           plancategory_new, Age_new, CC_new, makename_new, body_type,
           sum(PAID_AMT) as PAID_AMT,sum(Claim_Count) as Claim_Count, 
           sum(LIVES_EXPOSED) as LIVES_EXPOSED                       
            from df            
            group by  plancategory_new, Age_new, Accident_Year_new, makename_new,
                      Zone_new, CC_new, body_type           
     """

    output = db.execute(q3).df()

    output.to_csv("Bazaar\\Output\\2WheeleerFiles.csv")


def group_plancategory(x):
    if x in ["TP"]:
        return "1TP"
    else:
        return "COMP"


def group_age(x):
    if x in [4]:
        return "G4"
    elif x in [3, 10]:
        return "Group 2"
    elif x in [2, 7, 9]:
        return "1Group 3"
    elif x in [1, 5, 17]:
        return "Group 4"
    elif x in [8, 12]:
        return "Group 5"
    elif x in [6, 13]:
        return "Group 6"
    elif x in [11, 15]:
        return "G11Plus"
    else:
        return "1Group 3"


def group_zone(x):
    if x in ["North", "blanks"]:
        return "1North"

    else:
        return x


# def group_cc_make(x):
#     if x in ["BAJAJ_75 to 150cc"]:
#         return "Bajaj 75"
#     elif x in ["HONDA_75 to 150cc"]:
#         return "HOMDA"
#     elif x in ["HERO HONDA_75 to 150cc", "HERO MOTOCORP_75 to 150cc"]:
#         return "Group 1"
#     else:
#         return "Others"


def group_AY(x):
    if x in [2020]:
        return 1
    elif x in [2021]:
        return 2
    elif x in [2022]:
        return 3


def group_cc(x):
    if x in ["Below 75cc", "Above 350cc"]:
        return "Others"
    elif x in ["75 to 150cc"]:
        return "075 to 150cc"
    else:
        return x


def group_makename(x):
    if x in ["HONDA", "BAJAJ", "TVS"]:
        return x
    elif x in ["HERO HONDA", "HERO MOTOCORP"]:
        return "1Group 1"
    else:
        return "Others"


def make_pivots(dataframe, columns):
    df2 = pd.pivot_table(dataframe, values="PAID_AMT  LIVES_EXPOSED".split(), columns=columns,
                         aggfunc="sum").T
    df2["Actual"] = df2["PAID_AMT"] / df2["LIVES_EXPOSED"]
    df2.to_csv("Bazaar\\Output\\Sep\\" + columns + ".csv")


def othering(dataframe):
    make_pivots(dataframe, "Zone_new")
    make_pivots(dataframe, "CC_new")
    make_pivots(dataframe, "makename_new")
    make_pivots(dataframe, "body_type")
    make_pivots(dataframe, "plancategory_new")
    make_pivots(dataframe, "Age_new")
    make_pivots(dataframe, "Accident_Year_new")


def find_separation():
    df_ = pd.read_csv("Bazaar\\Output\\2WheeleerFiles.csv")
    othering(df_)


df = pd.read_csv("2Wheeler.csv")
df["Age"] = df["Age"].apply(pd.to_numeric, errors="coerce")
df["PAID_AMT"].fillna(0, inplace=True)
df["Zone_new"] = df["Zone"].apply(lambda x: group_zone(x))
df["plancategory_new"] = df["plan_category"].apply(lambda x: group_plancategory(x))
df["Age_new"] = df["Age"].apply(lambda x: group_age(x))
df["CC_new"] = df["ccnew"].apply(lambda x: group_cc(x))
df["makename_new"] = df["makename"].apply(lambda x: group_makename(x))
df["Accident_Year_new"] = df["Accident_Year"].apply(lambda x: group_AY(x))
df.to_csv("Bazaar\\Output\\2WheelerTestFile.csv")
prepare_tweedie_file()
find_separation()
