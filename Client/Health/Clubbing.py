import pandas as pd
import duckdb as db


def prepare_frequency_file():
    q3 = """select sum(EARNED_PREMIUM) as EARNED_PREMIUM,sum(PAID_AMT) as PAID_AMT,sum(Claim_Count) as Claim_Count, 
           sum(POLICIES_EXPOSED) as POLICIES_EXPOSED, sum(LIVES_EXPOSED) as LIVES_EXPOSED,
            Zone,Mem_Gender_New,Renewal_Count_New,Financial_Year,
            Sum_Insured_New, Mem_Age_New, Product_Name_New,  
            Channel_type_New, Revised_Individual_Floater_New 
            from df            
            group by Zone , Mem_Gender_New , Sum_Insured_New, Mem_Age_New, Product_name_New,Channel_type_New, 
            Revised_Individual_Floater_New,Financial_Year,Renewal_Count_New            
     """

    output = db.execute(q3).df()

    output.to_csv("CSV\\FrequencyModelFile.csv")


def group_renewal_count(x):
    if x in [0, 1, 2, 3, 7]:
        return x
    elif x in [4, 5, 6]:
        return "4to6"
    elif x in [8, 9]:
        return "8to9"


def group_gender(x):
    if x in ["MALE", "M"]:
        return "MALE"
    if x in ["FEMALE", "F"]:
        return "FEMALE"
    else:
        return "Other"


def group_rif(x):
    if x in ["FLOATER", "INDIVIDUAL"]:
        return x
    else:
        return "Other"


def group_channel_type(x):
    if x in ["Agents", "Broker", "Office Direct", "Sales Direct", "Tele Marketer", "Bancassurance"]:
        return x
    else:
        return "Other"


def group_product_name(x):
    if x in ["FHO", "COMP", "MCI", "SCRC", "Young Star Insurance Policy", "Star Health Assure Insurance Policy",
             "SURPLUS-FLOATER",  "Arogya Sanjeevini Policy"]:
        return x
    else:
        return "Other"


def group_si(x):
    if x in [500000, 1000000, 300000, 400000, 1500000, 2500000]:
        return x
    elif x in [100000, 200000, 7500000, 2000000]:
        return "1_2_20_7.5"

    else:
        return "Other"


def group_age(x):
    if x in [62, 64, 65, 67]:
        return "46"
    elif x in [33, 34, 45]:
        return "33to35"
    elif x in [28, 29, 30]:
        return "28to30"
    elif x in [26, 27]:
        return "26to27"
    elif x in [20, 21, 22, 23, 24]:
        return "20to24"
    elif x in [16, 17]:
        return "16to17"
    elif x in [13, 14]:
        return "13to14"
    elif x in [8, 9, 10, 11, 12]:
        return "8to12"
    elif x in [1, 2, 3]:
        return "1to3"
    else:
        return x


df = pd.read_csv("CSV\\SummaryExposed_Merged.csv")

df["Renewal_Count_New"] = df["Renewal_Count"].apply(lambda x: "Other" if x >= 10 else group_renewal_count(x))
df["Mem_Age_New"] = df["Mem_Age"].apply(lambda x: "Other" if x >= 71 else group_age(x))
df["Sum_Insured_New"] = df["Sum_Insured"].apply(lambda x: group_si(x))
df["Mem_Gender_New"] = df["Mem_Gender"].apply(lambda x: group_gender(x))
df["Revised_Individual_Floater_New"] = df["Revised_Individual_Floater"].apply(lambda x: group_rif(x))
df["Channel_type_New"] = df["Channel_type"].apply(lambda x: group_channel_type(x))
df["Product_Name_New"] = df["Product_name"].apply(lambda x: group_product_name(x))
df.to_csv("freq.csv")

df = pd.read_csv("freq.csv")
prepare_frequency_file()
