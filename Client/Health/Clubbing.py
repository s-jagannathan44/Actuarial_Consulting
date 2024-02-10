import pandas as pd
import duckdb as db


# Clubbed Other with Individual in RIF
# Clubbed Other with Male in Gender


def prepare_frequency_file():
    q3 = """select sum(EARNED_PREMIUM) as EARNED_PREMIUM,sum(PAID_AMT) as PAID_AMT,sum(Claim_Count) as Claim_Count, 
           sum(POLICIES_EXPOSED) as POLICIES_EXPOSED, sum(LIVES_EXPOSED) as LIVES_EXPOSED,
            Zone_New,Mem_Gender_New,Renewal_Count_New,Financial_Year,
            Sum_Insured_New, Mem_Age_New, Channel_type_New, Revised_Product_Name_New 
            from df            
            group by Zone_New , Mem_Gender_New , Sum_Insured_New, Mem_Age_New, Channel_type_New, 
            Revised_Product_Name_New,Financial_Year,Renewal_Count_New            
     """

    output = db.execute(q3).df()

    output.to_csv("CSV\\FrequencyModelFile.csv")


def group_renewal_count(x):
    if x in [0, 1]:
        return x
    elif x in [2, 3]:
        return "Group 1"
    elif x in [4, 5, 6, 7, 8]:
        return "Group 2"
    elif x in [9, 10]:
        return "Group 3"


def group_gender(x):
    if x in ["MALE", "M"]:
        return "MALE"
    if x in ["FEMALE", "F"]:
        return "FEMALE"
    else:
        return "MALE"


def group_rif(x):
    if x in ["FLOATER", "INDIVIDUAL"]:
        return x
    else:
        return "INDIVIDUAL"


def group_channel_type(x):
    if x in ["Agents"]:
        return x
    elif x in ["Office Direct", "Sales Direct"]:
        return "Direct"
    else:
        return "Other"


def group_product_name(x):
    if x in ["FHOFLOATER", "COMPFLOATER", "Young Star Insurance PolicyFLOATER", "MCIINDIVIDUAL", "SCRCINDIVIDUAL",
             "COMPINDIVIDUAL", "Young Star Insurance PolicyINDIVIDUAL", "Arogya Sanjeevini PolicyFLOATER",
             "Star Health Assure Insurance PolicyFLOATER", "Arogya Sanjeevini PolicyINDIVIDUAL",
             "Star Health Assure Insurance PolicyINDIVIDUAL", "Star Micro Rural and Farmers CareFLOATER"]:
        return x
    else:
        return "Other"


def group_si(x):
    if x in [150000, 400000, 500000]:
        return x
    elif x in [100000, 300000]:
        return "Group 2"
    elif x in [200000, 750000]:
        return "Group 4"
    elif x in [1000000, 1500000, 2000000, 2500000, 5000000, 10000000]:
        return "Group 3"
    else:
        return "Other"


def group_age(x):
    if x in [0, 1, 2, 3, 4, 15]:
        return x
    elif 5 <= x <= 6:
        return "Group 18"
    elif 7 <= x <= 12:
        return "Group 17"
    elif 13 <= x <= 14:
        return "Group 19"
    elif 16 <= x <= 17:
        return "Group 21"
    elif 18 <= x <= 19:
        return "Group 20"
    elif 20 <= x <= 25:
        return "Group 16"
    elif 26 <= x <= 30:
        return "Group 15"
    elif 31 <= x <= 35:
        return "Group 13"
    elif 36 <= x <= 37:
        return "Group 12"
    elif 38 <= x <= 39:
        return "Group 11"
    elif 40 <= x <= 41:
        return "Group 10"
    elif 42 <= x <= 43:
        return "Group 9"
    elif 44 <= x <= 45:
        return "Group 8"
    elif 46 <= x <= 48:
        return "Group 7"
    elif 49 <= x <= 50:
        return "Group 6"
    elif 51 <= x <= 53:
        return "Group 5"
    elif 54 <= x <= 56:
        return "Group 4"
    elif 57 <= x <= 59 or 68 <= x <= 72:
        return "Group 3"
    elif 60 <= x <= 67 or 73 <= x <= 75:
        return "Group 2"


zone_dict = {"DEL AO-II": "DEL AO-II", "MUMBAI": "Zone 1", "DEL AO-I": "Zone 1", "AHMEDABAD": "AHMEDABAD",
             "KERALA-SOUTH": "KERALA-SOUTH",
             "BANGALORE": "Zone 2", "CHANDIGARH": "Zone 2", "CHENNAI": "Zone 3", "DEHRADUN": "Zone 3",
             "PUNE": "Zone 4", "HYDERABAD": "Zone 4", "TIRUPATHI": "Zone 4", "KERALA-CENTRAL": "Zone 5",
             "LUCKNOW": "Zone 5",
             "LUDHIANA": "Zone 5", "INDORE": "Zone 7", "KERALA-NORTH": "Zone 7",
             "KOLKATA": "Zone 8", "COIMBATORE": "Zone 8", "JAIPUR": "Zone 8", "MADURAI": "Zone 9", "SALEM": "Zone 9",
             "TRICHY": "Zone 9",
             "PATNA": "Zone 10", "NAGPUR": "Zone 10", "WEB-SALES ONLINE": "Zone 10",
             "RANCHI": "Others", "GUWAHATI": "Others", "ODISHA": "Others", "CORPORATE OFFICE": "Others"}

df = pd.read_csv("CSV\\SummaryExposed_Merged.csv")
df["Revised_Product_name"] = df["Product_name"] + df["Revised_Individual_Floater"]
df["Renewal_Count_New"] = df["Renewal_Count"].apply(lambda x: "Above 10" if x > 10 else group_renewal_count(x))
df["Mem_Age_New"] = df["Mem_Age"].apply(lambda x: "Group 1" if x > 75 else group_age(x))
df["Sum_Insured_New"] = df["Sum_Insured"].apply(lambda x: group_si(x))
df["Mem_Gender_New"] = df["Mem_Gender"].apply(lambda x: group_gender(x))
df["Channel_type_New"] = df["Channel_type"].apply(lambda x: group_channel_type(x))
df["Revised_Product_Name_New"] = df["Revised_Product_name"].apply(lambda x: group_product_name(x))
df["Zone_New"] = df["Zone"].apply(lambda x: zone_dict[x])

prepare_frequency_file()
