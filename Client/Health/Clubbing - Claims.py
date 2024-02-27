import pandas as pd
import duckdb as db


def prepare_claim_file():
    q3 = """select count(claim_num) as claim_count,sum(Aggregate) as Aggregate,
            Zone_New,Mem_Gender_New,Renewal_Count_New,Financial_Year,
            Sum_Insured_New, Mem_Age_New, Product_Name_New,  
            Channel_type_New, Revised_Individual_Floater_New 
            from df            
            group by Zone_New , Mem_Gender_New , Sum_Insured_New, Mem_Age_New, Product_name_New,Channel_type_New, 
            Revised_Individual_Floater_New,Financial_Year,Renewal_Count_New            
     """

    output = db.execute(q3).df()
    output.to_csv("CSV\\ClaimsFile.csv")


def group_renewal_count(x):
    if x in [0, 1]:
        return x
    if x in [2, 3]:
        return "2 & 3"
    elif x in [4, 5]:
        return "4 &5"
    elif x in [6, 7, 8]:
        return "6 to 8"


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
        return "FLOATER"


def group_channel_type(x):
    if x in ["Agents", "Sales Direct"]:
        return "Group 1"
    elif x in ["Bancassurance", "Corporate Agents", "Pos Agents", "IMF", "NBFC-Bancassurance"]:
        return "Group 2"
    elif x in ["Tele Marketer", "Web Aggregator", "Broker"]:
        return "Group 3"
    else:
        return "Office Direct"


def group_product_name(x):
    if x in ["FHO", "COMP", "MCI"]:
        return x
    elif x in ["SCRC", "Young Star Insurance Policy", "Arogya Sanjeevini Policy"]:
        return "Group 1"
    else:
        return "Other"


def group_si(x):
    if x in [100000, 150000, 200000, 300000, 400000, 500000, 750000, 1000000, 2500000]:
        return x
    elif x in [1500000, 2000000, 10000000]:
        return "Group 1"
    else:
        return "Other"


def group_age(x):
    if x in [42, 43, 44, 45, 46, 66]:
        return "Group 1"
    elif x in [47, 48, 64, 65]:
        return "Group 3"
    elif x in [40, 41, 67]:
        return "Group 5"
    elif x in [49, 50, 51, 52, 53, 63]:
        return "Group 6"
    elif x in [38, 39]:
        return "Group 7"
    elif x in [17, 23, 24, 25, 34, 35, 36, 37]:
        return "Group 8"
    elif 54 <= x <= 62:
        return "Group 9"
    elif 69 <= x <= 88:
        return "Group 10"
    elif x in [14, 15, 16, 26, 27, 28, 30, 31, 32, 33, 90]:
        return "Group 10"
    elif x in [0, 1]:
        return "Group 11"
    elif x in [29]:
        return x
    elif x in [2, 3]:
        return "Group 13"
    elif x in [18, 19, 20, 21, 22, 68]:
        return "Group 14"
    elif x in [4, 5]:
        return "Group 15"
    elif x in [6, 7, 8]:
        return "Group 16"
    elif x in [9, 10, 11]:
        return "Group 17"
    elif x in [12, 13]:
        return "Group 18"


zone_dict = {"DEL AO-II": "Zone 3", "MUMBAI": "Zone 1", "DEL AO-I": "Zone 3", "AHMEDABAD": "Zone 8",
             "KERALA-SOUTH": "Zone 6",
             "BANGALORE": "Zone 3", "CHANDIGARH": "Zone 5", "CHENNAI": "Zone 1", "DEHRADUN": "Zone 6",
             "PUNE": "PUNE", "HYDERABAD": "Zone 4", "TIRUPATHI": "Zone 4", "KERALA-CENTRAL": "Zone 5",
             "LUCKNOW": "Zone 7",
             "LUDHIANA": "LUDHIANA", "INDORE": "Zone 8", "KERALA-NORTH": "Zone 5",
             "KOLKATA": "Zone 3", "COIMBATORE": "Zone 8", "JAIPUR": "JAIPUR", "MADURAI": "Zone 7", "SALEM": "Zone 7",
             "TRICHY": "TRICHY",
             "PATNA": "Zone 11", "NAGPUR": "Zone 11", "WEB-SALES ONLINE": "Zone 3",
             "RANCHI": "Zone 11", "GUWAHATI": "Zone 4", "ODISHA": "Zone 1", "CORPORATE OFFICE": "Zone 5"}

FY_dict = {"FY18": 0, "FY19": 1, "FY20": 2, "FY21": 3, "FY22": 4, "FY23": 5}

df = pd.read_csv("CSV\\PolicyMemberClaim.csv")

df["Renewal_Count_New"] = df["Renewal_Count"].apply(lambda x: "Other" if x > 8 else group_renewal_count(x))
df["Mem_Age_New"] = df["Mem_Age"].apply(lambda x: group_age(x))
df["Sum_Insured_New"] = df["Sum_Insured"].apply(lambda x: group_si(x))
df["Mem_Gender_New"] = df["Mem_Gender"].apply(lambda x: group_gender(x))
df["Revised_Individual_Floater_New"] = df["Revised_Individual_Floater"].apply(lambda x: group_rif(x))
df["Channel_type_New"] = df["Channel_type"].apply(lambda x: group_channel_type(x))
df["Product_Name_New"] = df["policy_product_name"].apply(lambda x: group_product_name(x))
df["Zone_New"] = df["Zone"].apply(lambda x: zone_dict[x])
df["Financial_Year"] = df["Financial_Year"].apply(lambda x: FY_dict[x])
prepare_claim_file()
