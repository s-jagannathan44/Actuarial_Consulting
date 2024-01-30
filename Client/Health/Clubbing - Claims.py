import pandas as pd
import duckdb as db


def prepare_claim_file():
    q3 = """select count(claim_num) as claim_count,sum(Aggregate) as Aggregate,
            Zone,Mem_Gender_New,Renewal_Count_New,Financial_Year,
            Sum_Insured_New, Mem_Age_New, Product_Name_New,  
            Channel_type_New, Revised_Individual_Floater_New 
            from df            
            group by Zone , Mem_Gender_New , Sum_Insured_New, Mem_Age_New, Product_name_New,Channel_type_New, 
            Revised_Individual_Floater_New,Financial_Year,Renewal_Count_New            
     """

    output = db.execute(q3).df()
    output.to_csv("CSV\\ClaimsModelFile.csv")


def group_renewal_count(x):
    if x in [0, 1]:
        return "0 & 1"
    if x in [2, 3]:
        return "2 & 3"
    elif x in [4, 5, 6, 7]:
        return "4 to 7"
    elif x in [8, 9, 10, 11, 12]:
        return x


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
             "SURPLUS-FLOATER", "SURPLUS-IND", "HEALTH GAIN", "Star Womens care Insurance Policy",
             "Arogya Sanjeevini Policy"]:
        return x
    else:
        return "Other"


def group_si(x):
    if x in [500000, 1000000, 300000, 400000, 1500000, 200000, 750000, 2500000, 2000000, 10000000, 5000000]:
        return x
    else:
        return "Other"


def group_age(x):
    if x in [78, 77, 76, 75, 74, 73, 72, 71, 70, 69]:
        return "69 to 78"
    elif x in [72, 71, 70, 69]:
        return "69 to 72"
    elif x in [61, 60, 59, 58, 57]:
        return "57 to 61"
    elif x in [31, 32, 33]:
        return "31 to 33"
    elif x in [30, 29, 28, 27]:
        return "27 to 30"
    elif x in [18, 19, 20, 21, 22, 23, 24]:
        return "18 to 24"
    else:
        return x


df = pd.read_csv("CSV\\PolicyMemberClaim.csv")

df["Renewal_Count_New"] = df["Renewal_Count"].apply(lambda x: "Other" if x >= 13 else group_renewal_count(x))
df["Mem_Age_New"] = df["Mem_Age"].apply(lambda x: "Other" if x >= 79 else group_age(x))
df["Sum_Insured_New"] = df["Sum_Insured"].apply(lambda x: group_si(x))
df["Mem_Gender_New"] = df["Mem_Gender"].apply(lambda x: group_gender(x))
df["Revised_Individual_Floater_New"] = df["Revised_Individual_Floater"].apply(lambda x: group_rif(x))
df["Channel_type_New"] = df["Channel_type"].apply(lambda x: group_channel_type(x))
df["Product_Name_New"] = df["policy_product_name"].apply(lambda x: group_product_name(x))
prepare_claim_file()
