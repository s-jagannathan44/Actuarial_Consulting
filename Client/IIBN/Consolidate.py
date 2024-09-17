import pandas as pd
import glob
import duckdb as db


def merge_member_files():
    path = "C:\\Users\\jvpra\\Desktop\\IIB-Narayana\\Nararayana_member_data/*.dat"
    df = pd.DataFrame()
    files = glob.glob(path)
    for file_name in files:
        frame = pd.read_csv(file_name, encoding="UTF-16LE", delimiter="~~", engine="python")
        frame["file_name"] = file_name[-11:-3]
        df = pd.concat([df, frame], axis=0)
    # df.to_csv("Output\\base_member_file.csv")


def merge_policy_files():
    path = "C:\\Users\\jvpra\\Desktop\\IIB-Narayana\\Narayana_Policy_Dataset/*.dat"
    df = pd.DataFrame()
    files = glob.glob(path)
    for file_name in files:
        frame = pd.read_csv(file_name, delimiter="\t")
        frame["file_name"] = file_name[-11:-3]
        df = pd.concat([df, frame], axis=0)
    # df.to_csv("Output\\base_policy_file.csv")


# noinspection PyUnusedLocal
def merge_claim_files():
    path = "C:\\Users\\jvpra\\OneDrive\\Desktop\\Narayana\\IIB-Narayana\\Narayana Bespoke_Claims_Dataset/*.csv"
    df = pd.DataFrame()
    files = glob.glob(path)
    for file_name in files:
        frame = pd.read_csv(file_name)
        frame["file_name"] = file_name[-11:-3]
        frame["ICD_Code_New"] = frame["ICD_CODE"].str[:3]
        df = pd.concat([df, frame], axis=0)

    icd_master = pd.read_csv("C:\\SHAI\\Revised 11-12-23\\ICD_Ver10cm 2019 V1.csv")
    claim_master = db.sql("""select df.*, icd_master.ICD_category,ICD_Group,Description from df left join 
                               icd_master on icd_master.icd_code =  df.ICD_Code_New """).df()

    claim_master.to_csv("Output\\base_claim_file_v2.csv")


def group_member_product_type(x):
    if x in ["Indemnity_Policy", "Both_Indemnity_and_Benefit_Based", "Package_Policy"]:
        return x
    else:
        return "Others"


def group_claim_product_type(x):
    if x in ["Indemnity Policy", "Both Indemnity and Benefit Based",
             "Package Policy (covering more than one type of health above)"]:
        return x
    else:
        return "Others"


def map_pincode(x):
    try:
        return dict_df[x]
    except KeyError:
        print("Pincode mapping error")
        return ""


def map_year(x):
    try:
        if pd.isnull(x):
            return ""
        else:
            return x.strftime("%Y")
    except ValueError:
        print("Null date ")


def group_policy_term(x):
    if x in [0, 1, 2]:
        return x
    else:
        return "Above 2"


def group_Age(x):
    if 0 <= x <= 4:
        return "0 to 4"
    elif 5 <= x <= 9:
        return "5 to 9"
    elif 10 <= x <= 14:
        return "10 to 14"
    elif 15 <= x <= 19:
        return "15 to 19"
    if 20 <= x <= 24:
        return "20 to 24"
    elif 25 <= x <= 29:
        return "25 to 29"
    elif 30 <= x <= 34:
        return "30 to 34"
    elif 35 <= x <= 39:
        return "35 to 39"
    if 40 <= x <= 44:
        return "40 to 44"
    elif 45 <= x <= 49:
        return "45 to 49"
    elif 50 <= x <= 54:
        return "50 to 54"
    elif 55 <= x <= 59:
        return "55 to 59"
    if 60 <= x <= 64:
        return "60 to 64"
    elif 65 <= x <= 69:
        return "65 to 69"
    elif 70 <= x <= 79:
        return "70 to 79"
    elif 80 <= x <= 89:
        return "80 to 89"
    elif 90 <= x <= 99:
        return "90 to 99"
    else:
        return "Above 100"


def group_si(x):
    if x in [0, 500000, 1000000, 300000, 200000, 1500000, 2000000, 400000, 2500000, 100000, 600000, 800000, 700000,
             3000000, 5000000, 750000, 9000000, 1000, 1200000]:
        return x
    else:
        return "Other"


def group_files():
    m = pd.read_csv("Output\\base_member_file.csv")
    c = pd.read_csv("Output\\base_claim_file.csv")
    c["District_New"] = c["TXT_PIN_CODE_OF_HOSPITAL"].apply(lambda x: map_pincode(x))
    c["Product_Type_New"] = c["TXT_PRODUCT_TYPE"].apply(lambda x: group_claim_product_type(x))
    c["Policy_Term_New"] = c["Policy_Term"].apply(lambda x: group_policy_term(x))
    c["Age_New"] = c["Age"].apply(lambda x: group_Age(x))
    c["SI_New"] = c["Sum_Insured"].apply(lambda x: group_si(x))
    c['Date_of_Payment'] = pd.to_datetime(c['Date_of_Payment'], format="mixed", dayfirst=True)
    c["Year_OfPayment"] = c["Date_of_Payment"].apply(lambda x: map_year(x))

    m["District_New"] = m["Pincode"].apply(lambda x: map_pincode(x))
    m["Product_Type_New"] = m["txt_product_type"].apply(lambda x: group_member_product_type(x))
    m["Policy_Term_New"] = m["Policy_Term"].apply(lambda x: group_policy_term(x))
    m["Age_New"] = m["age"].apply(lambda x: group_Age(x))
    m["SI_New"] = m["NUM_SUM_INSURED"].apply(lambda x: group_si(x))

    # m["Key"] = m["Business_Type"] + "_" + m["Policy_Type_New"] + m["District_New"] + "_" + m["txt_product_type"] + \
    #            str(m["Policy_Term_New"]) + "_" + str(m["Age_New"]) + m["Gender"] + "_" + str(m["SI_New"])

    q3 = """select sum(Total_Amount_Claimed) as Claimed_Amount, sum(Number_of_Claims) as Claim_Count, sum(Total_Claim_Paid) as PAID_AMT,
                   Insurer_Type, Policy_Type, District_New,
                   Product_Type_New, Policy_Term_New, Age_New, TXT_GENDER, SI_New,file_name  
                from c
                group by  Insurer_Type, Policy_Type, District_New,
                   Product_Type_New, Policy_Term_New, Age_New, TXT_GENDER, SI_New,file_name 
         """

    claims_ = db.execute(q3).df()

    q4 = """select sum(NOM) as Member_Count, Business_Type, Policy_Type, District_New,
                   Product_Type_New, Policy_Term_New, Age_New, Gender, SI_New,file_name 
                from m
                group by Business_Type, Policy_Type, District_New,
                   Product_Type_New, Policy_Term_New, Age_New, Gender, SI_New,file_name 
         """

    members = db.execute(q4).df()

    members.to_csv("Output\\grouped_member.csv")
    claims_.to_csv("Output\\grouped_claim.csv")


# merge_policy_files()
# merge_member_files()
# merge_claim_files()

claims = pd.read_csv("Output\\base_claim_file_v2.csv")
claims["Age_New"] = claims["Age"].apply(lambda x: group_Age(x))
claims.to_csv("Output\\base_claim_file_v3_AgeBands.csv")

# pincode = pd.read_csv("Output\\pincodes.csv")
# dict_df = pincode.set_index('Pincode')['District'].to_dict()
dict_df = ""
