import pandas as pd
import duckdb as db


def prepare_frequency_file():
    q3 = """select sum(EARNED_PREMIUM) as EARNED_PREMIUM,sum(PAID_AMT) as PAID_AMT,sum(Claim_Count) as Claim_Count, 
           sum(POLICIES_EXPOSED) as POLICIES_EXPOSED, sum(LIVES_EXPOSED) as LIVES_EXPOSED,
            Zone_Frequency,Mem_Gender_Frequency,Renewal_Count_Frequency,Financial_Year,
            Sum_Insured_Frequency, Mem_Age_Frequency, Channel_type_Frequency, Product_Name_Frequency,Revised_Individual_Floater_Frequency 
            from df            
            group by Zone_Frequency , Mem_Gender_Frequency , Sum_Insured_Frequency, Mem_Age_Frequency, Channel_type_Frequency, 
            Product_Name_Frequency,Financial_Year,Renewal_Count_Frequency,Revised_Individual_Floater_Frequency            
     """

    output = db.execute(q3).df()

    output.to_csv("CSV\\FrequencyFile.csv")


def group_renewal_count(x):
    if x in [0]:
        return "Group 1"
    elif x in [1]:
        return "Group 2"
    elif x in [2]:
        return "Group 3"
    elif x in [3, 4]:
        return "Group 4"
    elif x in [5, 6, 7, 8]:
        return "Group 5"


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
        return "FLOATER"


def group_channel_type(x):
    if x in ["Agents", "Bancassurance"]:
        return x
    elif x in ["Sales Direct"]:
        return "Direct"
    if x in ["Tele Marketer", "Web Aggregator"]:
        return x
    else:
        return "Other"


def group_product_name(x):
    if x in ["FHO", "COMP", "MCI"]:
        return x
    else:
        return "Other"


def group_si(x):
    if x in [100000, 2500000]:
        return x
    elif x in [150000, 200000]:
        return "Group 2"
    elif x in [300000, 400000]:
        return "Group 3"
    elif x in [500000, 750000]:
        return "Group 4"
    elif x in [1000000, 1500000]:
        return "Group 5"
    else:
        return "Other"


def group_age(x):
    if x in [45]:
        return x
    elif 10 <= x <= 13:
        return "Group 0"
    elif x in [8, 9, 14, 15]:
        return "Group 1"
    elif x in [7, 16, 17]:
        return "Group 2"
    elif x in [18, 19, 20, 21, 23]:
        return "Group 3"
    elif x in [6, 25, 24, 22]:
        return "Group 31"
    elif 26 <= x <= 34:
        return "Group 4"
    elif x in [5, 35]:
        return "Group 5"
    elif x in [36, 37]:
        return "Group 6"
    elif x in [38, 39]:
        return "Group 61"
    elif x in [4, 40, 41]:
        return "Group 7"
    elif x in [42, 43, 44]:
        return "Group 8"
    elif x in [3, 46, 47, 48]:
        return "Group 9"
    elif x in [2, 49, 50]:
        return "Group 91"
    elif x in [51, 52]:
        return "Group 10"
    elif x in [53, 54, 55]:
        return "Group 11"
    elif x in [1, 56, 57, 58]:
        return "Group 12"
    elif x in [59, 60]:
        return "Group 13"
    elif x in [62, 63, 64]:
        return "Group 15"
    elif x in [65, 66, 0]:
        return "Group 16"


zone_dict = {"DEL AO-II": "Zone 2", "MUMBAI": "Zone 3", "DEL AO-I": "Zone 3", "AHMEDABAD": "Zone 2",
             "KERALA-SOUTH": "Zone 1",
             "BANGALORE": "Zone 4", "CHANDIGARH": "Zone 4", "CHENNAI": "Zone 5", "DEHRADUN": "Zone 5",
             "PUNE": "Zone 3", "HYDERABAD": "Zone 5", "TIRUPATHI": "Zone 7", "KERALA-CENTRAL": "Zone 1",
             "LUCKNOW": "Zone 6",
             "LUDHIANA": "Zone 5", "INDORE": "Zone 4", "KERALA-NORTH": "Zone 2",
             "KOLKATA": "Zone 6", "COIMBATORE": "Zone 3", "JAIPUR": "Zone 6", "MADURAI": "Zone 4", "SALEM": "Zone 4",
             "TRICHY": "Zone 5",
             "PATNA": "Zone 7", "NAGPUR": "Zone 6", "WEB-SALES ONLINE": "Zone 6",
             "RANCHI": "Zone 7", "GUWAHATI": "Zone 8", "ODISHA": "Zone 8", "CORPORATE OFFICE": "Zone 5"}

FY_dict = {"FY18": 0, "FY19": 1, "FY20": 2, "FY21": 3, "FY22": 4, "FY23": 5}
# df = pd.read_csv("CSV\\SummaryExposed_Merged.csv")
# df["Revised_Individual_Floater_Frequency"] = df["Revised_Individual_Floater"].apply(lambda x: group_rif(x))
# df["Renewal_Count_Frequency"] = df["Renewal_Count"].apply(lambda x: "Above 8" if x > 8 else group_renewal_count(x))
# df["Mem_Age_Frequency"] = df["Mem_Age"].apply(lambda x: "Others" if x > 66 else group_age(x))
# df["Sum_Insured_Frequency"] = df["Sum_Insured"].apply(lambda x: group_si(x))
# df["Mem_Gender_Frequency"] = df["Mem_Gender"].apply(lambda x: group_gender(x))
# df["Channel_type_Frequency"] = df["Channel_type"].apply(lambda x: group_channel_type(x))
# df["Zone_Frequency"] = df["Zone"].apply(lambda x: zone_dict[x])
# df["Financial_Year"] = df["Financial_Year"].apply(lambda x: FY_dict[x])
# df["Product_Name_Frequency"] = df["Product_name"].apply(lambda x:group_product_name(x))
# # df.to_csv("Output\\clubbed_file.csv")
# prepare_frequency_file()
