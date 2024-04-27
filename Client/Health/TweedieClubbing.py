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

    output.to_csv("CSV\\TweedieModelFile_AgeModified.csv")


def group_renewal_count(x):
    if x in [0, 1]:
        return x
    elif x in [2, 3]:
        return "Group 1"
    elif x in [4, 5, 6, 7]:
        return "Group 2"
    elif x in [8, 9]:
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
    if x in ["FHOFLOATER", "MCIINDIVIDUAL"]:
        return x
    elif x in ["COMPFLOATER", "Young Star Insurance PolicyIndividual", "FHO ACC CAREFLOATER",
               "Star Womens care Insurance PolicyINDIVIDUAL", "Star Health Assure Insurance PolicyINDIVIDUAL"]:
        return "FHOFLOATER"
    elif x in ["Star Cancer Care Group INDIVIDUAL"]:
        return "MCIINDIVIDUAL"
    elif x in ["SCRCINDIVIDUAL", "COMPINDIVIDUAL"]:
        return "Individual Group 1"
    elif x in ["Young Star Insurance PolicyFLOATER", "Arogya Sanjeevini PolicyFLOATER",
               "Star Health Assure Insurance PolicyFLOATER", "Star Womens care Insurance PolicyFLOATER",
               "MCI ACC CAREINDIVIDUAL", "FHO ACC CARE INDIVIDUAL"]:
        return "Floater Group1"
    elif x in ["Star Micro Rural and Farmers CareFLOATER", "True Value Health InsuranceFLOATER",
               "FIRST OPTIMAINDIVIDUAL", "POS Family Health OptimaFLOATER",
               "Star Micro Rural and Farmers CareINDIVIDUAL", "MCI FAMILYFLOATER", "MCI POS INDVINDIVIDUAL",
               "Star Special CareINDIVIDUAL"]:
        return "Floater Group5"
    elif x in ["DIABETESINDIVIDUAL", "CARDIACINDIVIDUAL",
               "DIABETESFLOATER", "",
               "Star Care Micro Insurance PolicyFLOATER", "Star Cardiac Care Insurance Policy - PlatinumINDIVIDUAL"
               ]:
        return "Floater Group6"
    elif x in ["DIABETESINDIVIDUAL", "CARDIACINDIVIDUAL",
               "DIABETESFLOATER", "",
               "Star Care Micro Insurance PolicyFLOATER", "Star Cardiac Care Insurance Policy - PlatinumINDIVIDUAL"
               ]:
        return "Floater Group6"
    elif x in ["Star Delite Insurance PolicyINDIVIDUAL", "Star Care Micro Insurance PolicyINDIVIDUAL",
               "Star First ComprehensiveINDIVIDUAL", "Star Critical Illness Multipay Insurance PolicyINDIVIDUAL",
               "Star Outpatientcare Insurance PolicyFLOATER", "Micro Insurance IndividualINDIVIDUAL",
               "Star Outpatientcare Insurance PolicyFLOATER"
               ]:
        return "Floater Group4"

    else:
        return "Other"


def group_si(x):
    if x in [400000, 1000000]:
        return "Group 2"
    elif x in [100000, 300000, 500000]:
        return "Group 1"
    elif x in [150000, 200000, 750000, 1500000, 2000000]:
        return "Group 3"
    elif x in [2500000, 10000000]:
        return "Group 3"
    else:
        return "Other"


def group_age(x):
    if x in [0, 55]:
        return x
    elif 1 <= x <= 2:
        return "Group 1"
    elif x in [3]:
        return "Group 5"
    elif x in [4]:
        return "Group 4"
    elif x in [5, 14]:
        return "Group 2"
    elif 6 <= x <= 13:
        return "Group 3"
    elif 15 <= x <= 17:
        return "Group 4"
    elif 18 <= x <= 19:
        return "Group 5"
    elif 20 <= x <= 26:
        return "Group 6"
    elif 27 <= x <= 33:
        return "Group 7"
    elif 34 <= x <= 37:
        return "Group 8"
    elif 38 <= x <= 41:
        return "Group 9"
    elif 42 <= x <= 45:
        return "Group 10"
    elif 46 <= x <= 50:
        return "Group 11"
    elif 51 <= x <= 54:
        return "Group 12"
    elif 56 <= x <= 59:
        return "Group 13"
    elif x in [60]:
        return "Others"
    elif 61 <= x <= 66:
        return "Group 14"


def prepare_forecast_file():
    df_24 = pd.read_csv("CSV\\SummaryExposed_24_v2.csv")
    df_24["Revised_Product_name"] = (
            df_24["Product_name"] + df_24["Revised_Individual_Floater"].apply(lambda x: group_rif(x)))
    df_24["Financial_Year"] = 6
    df_24 = df_24[~ df_24["Product_name"].isin("SURPLUS-FLOATER SURPLUS-IND".split())]
    df_24 = df_24[~ df_24["Product_name"].str.contains("Corona")]
    df_24 = df_24[~ df_24["Product_name"].str.contains("Cash")]
    df_24["Renewal_Count_New"] = df_24["Renewal_Count"].apply(lambda x: "Above 9" if x > 9 else group_renewal_count(x))
    df_24["Mem_Age_New"] = df_24["Mem_Age"].apply(lambda x: "Others" if x > 66 else group_age(x))
    df_24["Sum_Insured_New"] = df_24["Sum_Insured"].apply(lambda x: group_si(x))
    df_24["Mem_Gender_New"] = df_24["Mem_Gender"].apply(lambda x: group_gender(x))
    df_24["Channel_type_New"] = df_24["Channel_type"].apply(lambda x: group_channel_type(x))
    df_24["Revised_Product_Name_New"] = df_24["Revised_Product_name"].apply(lambda x: group_product_name(x))
    df_24["Zone_New"] = df_24["Zone"].apply(lambda x: zone_dict[x])

    df_24.to_csv("Output\\24_File.csv")


zone_dict = {"DEL AO-II": "DEL AO-II", "MUMBAI": "Zone 1", "DEL AO-I": "Zone 1", "AHMEDABAD": "AHMEDABAD",
             "KERALA-SOUTH": "Zone 2",
             "BANGALORE": "Zone 2", "CHANDIGARH": "Zone 2", "CHENNAI": "Zone 3", "DEHRADUN": "Zone 3",
             "PUNE": "Zone 4", "HYDERABAD": "Zone 3", "TIRUPATHI": "Zone 3", "KERALA-CENTRAL": "Zone 5",
             "LUCKNOW": "Zone 5",
             "LUDHIANA": "Zone 5", "INDORE": "Zone 5", "KERALA-NORTH": "Zone 5",
             "KOLKATA": "Zone 8", "COIMBATORE": "Zone 8", "JAIPUR": "Zone 8", "MADURAI": "Zone 8", "SALEM": "Zone 8",
             "TRICHY": "Zone 8",
             "PATNA": "Zone 8", "NAGPUR": "Zone 8", "WEB-SALES ONLINE": "Zone 8",
             "RANCHI": "Others", "GUWAHATI": "Others", "ODISHA": "Others", "CORPORATE OFFICE": "Others"}

FY_dict = {"FY18": 0, "FY19": 1, "FY20": 2, "FY21": 3, "FY22": 4, "FY23": 5, "Test": 6}
# df = pd.read_csv("CSV\\SummaryExposed_Merged.csv")
# df["Revised_Product_name"] = df["Product_name"] + df["Revised_Individual_Floater"].apply(lambda x: group_rif(x))
# df["Financial_Year"] = df["Financial_Year"].apply(lambda x: FY_dict[x])
# df = df[~ df["Product_name"].isin("SURPLUS-FLOATER SURPLUS-IND"
#                                   .split())]
# df = df[ ~ df["Product_name"].str.contains("Corona")]
# df = df[ ~ df["Product_name"].str.contains("Cash")]
# df = df[df["Financial_Year"].isin([0, 1, 2, 4, 5])]
# df.to_csv("Output\\SummaryFile.csv")
df = pd.read_csv("Output\\SummaryFile.csv")
df["Renewal_Count_New"] = df["Renewal_Count"].apply(lambda x: "Above 9" if x > 9 else group_renewal_count(x))
df["Mem_Age_New"] = df["Mem_Age"].apply(lambda x: "Others" if x > 66 else group_age(x))
df["Sum_Insured_New"] = df["Sum_Insured"].apply(lambda x: group_si(x))
df["Mem_Gender_New"] = df["Mem_Gender"].apply(lambda x: group_gender(x))
df["Channel_type_New"] = df["Channel_type"].apply(lambda x: group_channel_type(x))
df["Revised_Product_Name_New"] = df["Revised_Product_name"].apply(lambda x: group_product_name(x))
df["Zone_New"] = df["Zone"].apply(lambda x: zone_dict[x])

df.to_csv("Output\\clubbed_file_AgeModified.csv")
prepare_tweedie_file()

