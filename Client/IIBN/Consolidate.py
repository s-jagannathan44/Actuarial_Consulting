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


def merge_claim_files():
    path = "C:\\Users\\jvpra\\Desktop\\IIB-Narayana\\Narayana Bespoke_Claims_Dataset/*.csv"
    df = pd.DataFrame()
    files = glob.glob(path)
    for file_name in files:
        frame = pd.read_csv(file_name)
        frame["file_name"] = file_name[-11:-3]
        df = pd.concat([df, frame], axis=0)
    # df.to_csv("Output\\base_claim_file.csv")


# # merge_policy_files()
# merge_member_files()
# # merge_claim_files()
# p = pd.read_csv("Output\\base_claim_file.csv")
# c = pd.read_csv("Output\\base_policy_file.csv")
def group_member_policy_type(x):
    if x in ["Others"]:
        return "Any Other Cover Type"
    else:
        return x


def group_claim_product_type(x):
    if x in ["Any Other Product Type"]:
        return "Any_Other_Product_type"
    elif x in ["Benefit Based Policy"]:
        return "Benefit_Based_Policy"
    elif x in ["Both Indemnity and Benefit Based"]:
        return "Both_Indemnity_and_Benefit_Based"
    elif x in ["Critical Illness Policy"]:
        return "Critical_Illness_Policy"
    elif x in ["High Deductible"]:
        return "High_Deductible"
    elif x in ["Hybrid Policy (covering other than health also)"]:
        return "Any_Other_Product_type"
    elif x in ["Indemnity Policy"]:
        return "Indemnity_Policy"
    elif x in ["Loan care product"]:
        return "Loan_care_product"
    elif x in ["Micro insurance Policy"]:
        return "Micro_insurance_Policy"
    elif x in ["Out Patient Policy"]:
        return "Out_Patient_Policy"
    elif x in ["Package Policy (covering more than one type of health above)"]:
        return "Package_Policy"
    elif x in ["Specific Disease Cover (For Ex. Cancer, HIV, Diabetes etc.)"]:
        return "Specific_Disease_Cover"
    else:
        return x


def group_claim_gender(x):
    if x in [1]:
        return "Male"
    elif x in [2]:
        return "Female"
    else:
        return "Others"


def map_pincode(x):
    try:
        return dict_df[x]
    except KeyError:
        print("Pincode mapping error")
        return ""


def group_policy_term(x):
    if x in [0, 1]:
        return x
    else:
        return "Above 1"


def group_Age(x):
    if x in [0, 1]:
        return x
    elif 2 < x < 20:
        return "2 to 20"
    elif 21 < x < 40:
        return "21 to 40"
    elif 41 < x < 60:
        return "41 to 60"
    elif 61 < x < 80:
        return "61 to 80"
    else:
        return "Above 80"


def group_SI(x):
    if 0 < x <= 25000:
        return "O to 25"
    elif 25000 < x <= 300000:
        return "25 to 3 lacs"
    elif 300000 < x <= 400000:
        return "3 lacs to 4 lacs"
    elif 400000 < x <= 500000:
        return "4 lacs to 5 lacs"
    elif 500000 < x <= 500000:
        return "5 lacs to 6 lacs"
    elif 600000 < x <= 800000:
        return "6 lacs to 8 lacs"
    elif 800000 < x <= 1000000:
        return "8 lacs to 10 lacs"
    elif 1000000 < x <= 2000000:
        return "10 lacs to 20 lacs"
    else:
        return "Above 20 lacs"


pincode = pd.read_csv("Output\\pincodes.csv")
dict_df = pincode.set_index('Pincode')['District'].to_dict()
m = pd.read_csv("Output\\base_member_file.csv")
c = pd.read_csv("Output\\base_claim_file.csv")
c["District_New"] = c["TXT_PIN_CODE_OF_HOSPITAL"].apply(lambda x: map_pincode(x))
c["Gender_New"] = c["TXT_GENDER"].apply(lambda x: group_claim_gender(x))
c["Product_Type_New"] = c["TXT_PRODUCT_TYPE"].apply(lambda x: group_claim_product_type(x))
c["SI_New"] = c["Sum_Insured"].apply(lambda x: group_SI(x))
c["Policy_Term_New"] = c["Policy_Term"].apply(lambda x: group_policy_term(x))
c["Age_New"] = c["Age"].apply(lambda x: group_Age(x))
c["Key"] = c["Insurer_Type"] + "_" + c["Policy_Type"] + c["District_New"] + "_" + c["Product_Type_New"] + \
           str(c["Policy_Term_New"]) + "_" + str(c["Age_New"]) + c["Gender_New"] + "_" + str(c["SI_New"])

m["SI_New"] = m["NUM_SUM_INSURED"].apply(lambda x: map_pincode(x))
m["Policy_Term_New"] = m["Policy_Term"].apply(lambda x: group_policy_term(x))
m["Age_New"] = m["age"].apply(lambda x: group_Age(x))
m["District_New"] = m["Pincode"].apply(lambda x: map_pincode(x))
m["SI_New"] = m["NUM_SUM_INSURED"].apply((lambda x: group_SI(x)))
m["Policy_Type_New"] = m['Policy_Type'].apply(lambda x: group_member_policy_type(x))
m["Key"] = m["Business_Type"] + "_" + m["Policy_Type_New"] + m["District_New"] + "_" + m["txt_product_type"] + \
           str(m["Policy_Term_New"]) + "_" + str(m["Age_New"]) + m["Gender"] + "_" + str(m["SI_New"])

q3 = """select sum(Total_Amount_Claimed), sum(Number_of_Claims), Key, Insurer_Type, Policy_Type, District_New,
               Product_Type_New, Policy_Term_New, Age_New, Gender_New, SI_New 
            from c
            group by Key, Insurer_Type, Policy_Type, District_New,
               Product_Type_New, Policy_Term_New, Age_New, Gender_New, SI_New 
     """

claims = db.execute(q3).df()

q4 = """select sum(NOM), Key, Business_Type, Policy_Type, District_New,
               txt_product_type, Policy_Term_New, Age_New, Gender, SI_New 
            from m
            group by Key, Business_Type, Policy_Type, District_New,
               txt_product_type, Policy_Term_New, Age_New, Gender, SI_New 
     """

members = db.execute(q4).df()

members.to_csv("Output\\grouped_member.csv")
claims.to_csv("Output\\grouped_claim.csv")
