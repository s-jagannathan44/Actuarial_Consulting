import pandas as pd
import duckdb as db


def prepare_tweedie_file():
    q3 = """select  Zone_new, Accident_Year_new,
           plancategory_new, Age_new, CC_Make_new, body_type,
           sum(PAID_AMT) as PAID_AMT,sum(Claim_Count) as Claim_Count, 
           sum(LIVES_EXPOSED) as LIVES_EXPOSED                       
            from df            
            group by  plancategory_new, Age_new,  Accident_Year_new,
                      Zone_new, CC_Make_new, body_type           
     """

    output = db.execute(q3).df()

    output.to_csv("Bazaar\\Output\\2WheeleerFiles.csv")


def group_plancategory(x):
    if x in ["TP"]:
        return "1TP"
    else:
        return "COMP"


def group_age(x):
    if x in [4, 11]:
        return "G" + str(x)
    elif x in [5, 7, 9]:
        return "1Group 1"
    elif x in [6, 8]:
        return "Group 2"
    elif x in [3, 10]:
        return "Group 3"
    else:
        return "Others"


# def group_makename(x):
#     if x in ["HONDA", "YAMAHA"]:
#         return "1Group 1"
#     elif x in ["BAJAJ", "TVS", "HERO HONDA", "HERO MOTOCORP"]:
#         return x
#     else:
#         return "Others"


def group_zone(x):
    if x in ["North"]:
        return "1North"
    else:
        return x


def group_cc_make(x):
    if x in ["BAJAJ_75 to 150cc", "HONDA_75 to 150cc"]:
        return "1Group 1"
    elif x in ["HERO MOTOCORP_75 to 150cc", "TVS_75 to 150cc"]:
        return "Group 2"
    elif x in ["HERO HONDA_75 to 150cc"]:
        return x
    else:
        return "Others"


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
    make_pivots(dataframe, "Zone_new")
    make_pivots(dataframe, "CC_Make_new")
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
df["CC_Make_new"] = df["CC_Make"].apply(lambda x: group_cc_make(x))
# df["makename_new"] = df["makename"].apply(lambda x: group_makename(x))
df["Accident_Year_new"] = df["Accident_Year"].apply(lambda x: group_AY(x))
df.to_csv("Bazaar\\Output\\2WheelerTestFile.csv")
prepare_tweedie_file()
find_separation()
