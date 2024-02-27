import pandas as pd
import duckdb as db


def prepare_tweedie_file():
    q3 = """select sum(EARNED_PREMIUM) as EARNED_PREMIUM,sum(PAID_AMT) as PAID_AMT,sum(Claim_Count) as Claim_Count, 
           sum(POLICIES_EXPOSED) as POLICIES_EXPOSED, sum(LIVES_EXPOSED) as LIVES_EXPOSED,
            Zone_New,Mem_Gender_New,Renewal_Count_New,Financial_Year,
            Sum_Insured_New, Mem_Age_New, Channel_type_New, Revised_Product_Name_New 
            from df            
            group by Zone_New , Mem_Gender_New , Sum_Insured_New, Mem_Age_New, Channel_type_New, 
            Revised_Product_Name_New,Financial_Year,Renewal_Count_New            
     """

    output = db.execute(q3).df()

    output.to_csv("TweedieOutput\\TweedieModelFile.csv")


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
    # if x in ["FHOFLOATER", "COMPFLOATER", "Young Star Insurance PolicyFLOATER", "MCIINDIVIDUAL", "SCRCINDIVIDUAL",
    #          "COMPINDIVIDUAL", "Young Star Insurance PolicyINDIVIDUAL", "Arogya Sanjeevini PolicyFLOATER",
    #          "Star Health Assure Insurance PolicyFLOATER", "Arogya Sanjeevini PolicyINDIVIDUAL",
    #          "Star Health Assure Insurance PolicyINDIVIDUAL", "Star Micro Rural and Farmers CareFLOATER"]:
    #     return x
    if x in ["FHOFLOATER", "COMPFLOATER", "MCIINDIVIDUAL"]:
        return x
    elif x in ["SCRCINDIVIDUAL", "COMPINDIVIDUAL"]:
        return x
    elif x in ["Arogya Sanjeevini PolicyINDIVIDUAL", "Star Health Assure Insurance PolicyINDIVIDUAL"]:
        return "Other"
    elif x in ["Young Star Insurance PolicyFLOATER", "Arogya Sanjeevini PolicyFLOATER",
               "Star Health Assure Insurance PolicyFLOATER"]:
        return "Floater Group1"
    else:
        return "Other"


def group_si(x):
    if x in [2500000]:
        return x
    elif x in [500000, 300000, 100000, 10000000]:
        return "Group 1"
    elif x in [150000, 200000, 750000]:
        return "Group 2"
    elif x in [400000, 1000000, 1500000, 2000000]:
        return "Group 3"
    else:
        return "Other"


def group_age(x):
    if 7 <= x <= 12:
        return "Group 0"
    elif x in [6, 13]:
        return "Group 1"
    elif 30 <= x <= 32:
        return "Group 10"
    elif x in [34, 35]:
        return "Group 11"
    elif x in [0, 36]:
        return "Group 12"
    elif x in [37]:
        return "Group 13"
    elif x in [38, 39]:
        return "Group 14"
    elif x in [40, 41]:
        return "Group 15"
    elif x in [42, 43]:
        return "Group 16"
    elif x in [44, 45]:
        return "Group 17"
    elif x in [46]:
        return "Group 18"
    elif x in [47, 48]:
        return "Group 19"
    elif x in [49, 50]:
        return "Group 20"
    elif x in [52, 53]:
        return "Group 21"
    elif x in [53, 54]:
        return "Group 22"
    elif x in [55, 56]:
        return "Group 23"
    elif x in [57, 58]:
        return "Group 24"
    elif x in [59, 60, 68, 69, 70, 71, 72]:
        return "Group 25"
    elif x in [14]:
        return "Group 2"
    elif x in [5, 15]:
        return "Group 3"
    elif x in [4, 16, 17]:
        return "Group 4"
    elif x in [3, 18]:
        return "Group 5"
    elif x in [2, 19, 20]:
        return "Group 6"
    elif 21 <= x <= 25:
        return "Group 7"
    elif x in [1, 26, 27]:
        return "Group 8"
    elif 28 <= x <= 30:
        return "Group 9"
    elif 61 <= x <= 67:
        return "Others"
    elif 73 <= x <= 97:
        return "Others"
    elif x in [-1]:
        return "Others"


zone_dict = {"DEL AO-II": "DEL AO-II", "MUMBAI": "Zone 1", "DEL AO-I": "Zone 1", "AHMEDABAD": "Zone 2",
             "KERALA-SOUTH": "Zone 2",
             "BANGALORE": "Zone 3", "CHANDIGARH": "Zone 3", "CHENNAI": "Zone 3", "DEHRADUN": "Zone 4",
             "PUNE": "Zone 4", "HYDERABAD": "Zone 4", "TIRUPATHI": "Zone 4", "KERALA-CENTRAL": "Zone 4",
             "LUCKNOW": "Zone 5",
             "LUDHIANA": "Zone 5", "INDORE": "Zone 6", "KERALA-NORTH": "Zone 5",
             "KOLKATA": "Zone 8", "COIMBATORE": "Zone 6", "JAIPUR": "Zone 6", "MADURAI": "Zone 6", "SALEM": "Zone 6",
             "TRICHY": "Zone 7",
             "PATNA": "Zone 7", "NAGPUR": "Zone 7", "WEB-SALES ONLINE": "Zone 7",
             "RANCHI": "Zone 9", "GUWAHATI": "Zone 9", "ODISHA": "Zone 8", "CORPORATE OFFICE": "Zone 8"}

FY_dict = {"FY18": 0, "FY19": 1, "FY20": 2, "FY21": 3, "FY22": 4, "FY23": 5}

df = pd.read_csv("CSV\\SummaryExposed_Merged.csv")
df = df[~ df["ICD_category"].isin(["Certain conditions originating in the perinatal period",
                                   "Congenital malformations, deformations and chromosomal abnormalities", "Unspecified"
                                      , "Mental, Behavioral and Neurodevelopmental disorders"])]

df["Revised_Product_name"] = df["Product_name"] + df["Revised_Individual_Floater"].apply(lambda x: group_rif(x))
# df.to_csv("TweedieOutput\\WithoutUnspecified.csv")
df["Renewal_Count_New"] = df["Renewal_Count"].apply(lambda x: "Above 10" if x > 10 else group_renewal_count(x))
df["Mem_Age_New"] = df["Mem_Age"].apply(lambda x: group_age(x))
df["Sum_Insured_New"] = df["Sum_Insured"].apply(lambda x: group_si(x))
df["Mem_Gender_New"] = df["Mem_Gender"].apply(lambda x: group_gender(x))
df["Channel_type_New"] = df["Channel_type"].apply(lambda x: group_channel_type(x))
df["Revised_Product_Name_New"] = df["Revised_Product_name"].apply(lambda x: group_product_name(x))
df["Zone_New"] = df["Zone"].apply(lambda x: zone_dict[x])
df["Financial_Year"] = df["Financial_Year"].apply(lambda x: FY_dict[x])

df.to_csv("TweedieOutput\\clubbed_file.csv")
prepare_tweedie_file()
