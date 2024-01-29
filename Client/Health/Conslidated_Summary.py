import pandas as pd
import glob
import duckdb as db


def create_file():
    claim = pd.read_csv("CSV\\Claims_for_severity.csv")
    q1 = """select claim.*, Zone,Renewal_Count,
            Sum_Insured, Product_Name,Plan_type,  
            Channel_type, Revised_Individual_Floater from claim inner join policy on claim.Policy_number = policy.policy_number and 
            claim.Financial_Year = policy.Financial_Year  where claim.Mem_ID !='' """
    policy_claim = db.execute(q1).df()
    q2 = """select policy_claim.*,  member.Mem_Age, Mem_Gender from policy_claim join member on 
policy_claim.Policy_number = member.policy_number and 
            policy_claim.Mem_Id = member.Mem_Id  and policy_claim.Financial_Year = member.Financial_Year   """
    member_claim = db.execute(q2).df()
    member_claim.to_csv("CSV\\PolicyMemberClaim.csv")


def summaries():
    q3 = """select sum(Normalized_Earned_Premium) as EARNED_PREMIUM,sum(Aggregate) as PAID_AMT,sum(claim_count) as Claim_Count, 
           sum(Normalized_POLICIES_EXPOSED) as POLICIES_EXPOSED, sum(Normalized_LIVES_EXPOSED) as LIVES_EXPOSED,
            sum(members_per_policy) as MEMBER_COUNT, 
            icd_category,Zone,Mem_Gender,Renewal_Count,norm_policy.Financial_Year,
            norm_policy.Sum_Insured, member_claim.Mem_Age, Product_name,  
            Channel_type, Revised_Individual_Floater 
            from norm_policy
            inner join member_claim on
            norm_policy.Policy_number = member_claim.Policy_number  
            where member_claim.Mem_ID !=''
            group by norm_policy.Zone , member_claim.Mem_Gender , norm_policy.Sum_Insured, member_claim.Mem_Age, 
            Product_name,Channel_type, Revised_Individual_Floater,icd_category,norm_policy.Financial_Year,Renewal_Count            
     """

    output = db.execute(q3).df()
    output.to_csv("CSV\\SummaryExposed_Merged.csv")


def rename_columns(file_name):
    dx = pd.read_csv(file_name,
                     usecols=['Policy number', 'Policy Start Date', 'Policy End Date', 'Product Name', 'Plan type',
                              'Policy Period', 'Office Name', 'Zone', 'Channel type',
                              'Ported Customer',
                              'Previous Company Name', 'Inception Date', 'Renewal Count', 'NOP_RCD', 'NOR_RCD',
                              'GWP_RCD',
                              'EARNED_PREMIUM', 'POLICIES_EXPOSED', 'LIVES_EXPOSED', 'Revised Individual/Floater',
                              'POLICY_VERSION_CODE', 'Sum Insured'])
    dx.rename(columns={'Policy number': "Policy_number", 'Policy Start Date': "Policy_Start_Date",
                       'Policy End Date': 'Policy_End-Date',
                       'Product Name': 'Product_name', 'Plan type': 'Plan_type', 'Policy Period': 'Policy_Period',
                       'Office Name': 'Office_Name',
                       'Channel type': 'Channel_type',
                       'Ported Customer': 'Ported_Customer',
                       'Previous Company Name': 'Previous_Company_Name', 'Inception Date': 'Inception_Date',
                       'Renewal Count': 'Renewal_Count',
                       'Revised Individual/Floater': 'Revised_Individual_Floater', 'Sum Insured': 'Sum_Insured'},
              inplace=True)
    return dx


def merge_policies():
    path = "C:\\SHAI\\Revised 11-12-23\\Data\\*.csv"
    concatenated_policies = pd.DataFrame()
    files = glob.glob(path)
    for file_name in files:
        financial_year = file_name[30:34]
        frame = rename_columns(file_name)
        frame["Financial_Year"] = financial_year
        frame["Policy_number"] = frame["Policy_number"].apply(lambda x: financial_year + x)
        concatenated_policies = pd.concat([concatenated_policies, frame], axis=0)
        print(financial_year)
    concatenated_policies.to_csv("CSV\\Policy_Merged.csv")


def merge_members():
    path = "C:\\SHAI\\Revised 11-12-23\\Data\\*.csv"
    concatenated_members = pd.DataFrame()
    files = glob.glob(path)
    for file_name in files:
        financial_year = file_name[30:34]
        frame = pd.read_csv(file_name, usecols=['Member ID 1', 'Member ID 2', 'Member ID 3', 'Member ID 4',
                                                'Member ID 5',
                                                'Member ID 6', 'Member Age 1', 'Member Age 2', 'Member Age 3',
                                                'Member Age 4', 'Member Age 5', 'Member Age 6', 'Member Gender 1',
                                                'Member Gender 2', 'Member Gender 3', 'Member Gender 4',
                                                'Member Gender 5', 'Member Gender 6', 'Policy number'])

        transformed_member = transform_member(frame)
        print("append complete")
        transformed_member.rename(columns={"Policy number": "Policy_number"}, inplace=True)
        final_member = db.sql("select * from transformed_member where Mem_ID is not null").df()
        final_member["Financial_Year"] = financial_year
        final_member["Policy_number"] = final_member["Policy_number"].apply(lambda x: financial_year + x)
        final_member["Mem_ID"] = final_member["Mem_ID"].apply(lambda x: financial_year + x)
        print(financial_year)
        concatenated_members = pd.concat([concatenated_members, final_member], axis=0)

    concatenated_members.to_csv("CSV\\Member_Merged.csv")


def transform_member(member):
    member1 = pd.DataFrame(columns=["Policy_number", "Mem_ID", "Mem_Age", "Mem_Gender"])
    member2 = pd.DataFrame(columns=["Policy_number", "Mem_ID", "Mem_Age", "Mem_Gender"])
    member3 = pd.DataFrame(columns=["Policy_number", "Mem_ID", "Mem_Age", "Mem_Gender"])
    member4 = pd.DataFrame(columns=["Policy_number", "Mem_ID", "Mem_Age", "Mem_Gender"])
    member5 = pd.DataFrame(columns=["Policy_number", "Mem_ID", "Mem_Age", "Mem_Gender"])
    member6 = pd.DataFrame(columns=["Policy_number", "Mem_ID", "Mem_Age", "Mem_Gender"])
    member1[["Policy_number", "Mem_ID", "Mem_Age", "Mem_Gender"]] = member[
        ["Policy number", "Member ID 1", "Member Age 1", "Member Gender 1"]]
    member2[["Policy_number", "Mem_ID", "Mem_Age", "Mem_Gender"]] = member[
        ["Policy number", "Member ID 2", "Member Age 2", "Member Gender 2"]]
    member3[["Policy_number", "Mem_ID", "Mem_Age", "Mem_Gender"]] = member[
        ["Policy number", "Member ID 3", "Member Age 3", "Member Gender 3"]]
    member4[["Policy_number", "Mem_ID", "Mem_Age", "Mem_Gender"]] = member[
        ["Policy number", "Member ID 4", "Member Age 4", "Member Gender 4"]]
    member5[["Policy_number", "Mem_ID", "Mem_Age", "Mem_Gender"]] = member[
        ["Policy number", "Member ID 5", "Member Age 5", "Member Gender 5"]]
    member6[["Policy_number", "Mem_ID", "Mem_Age", "Mem_Gender"]] = member[
        ["Policy number", "Member ID 6", "Member Age 6", "Member Gender 6"]]
    members_as_vertical = pd.concat([member1, member2, member3, member4, member5, member6], axis=0)
    return members_as_vertical


def merge_claim():
    is_os = False
    path = "C:\\SHAI\\Revised 11-12-23\\Data\\Claims\\*.csv"
    concatenated_claims = pd.DataFrame()
    files = glob.glob(path)
    for file_name in files:
        frame = pd.read_csv(file_name)
        if file_name == "C:\\SHAI\\Revised 11-12-23\\Data\\Claims\\FY23_OS_Final.csv":
            frame.rename(columns={'PROVISION_AMT': 'PAID_AMT'}, inplace=True)
            is_os = True
        frame["file_name"] = file_name
        print(file_name)
        frame = remove_group(frame, is_os)
        concatenated_claims = pd.concat([concatenated_claims, frame], axis=0)

    claims = concatenated_claims
    claims.rename(columns={'POLICY_NUM': "Policy_number", "MEMBER_ID_CARD_NUM": "Mem_ID"}, inplace=True)
    consolidated_claim = group_by_claim_number(claims)
    icd_master = pd.read_csv("C:\\SHAI\\Revised 11-12-23\\ICD_Ver10cm 2019 V1.csv")
    claim_master = db.sql("""select consolidated_claim.*, icd_master.ICD_category from consolidated_claim left join 
                            icd_master on icd_master.icd_code =  consolidated_claim.icd_code 
                            where consolidated_claim.icd_code NOT like 'B99%' """).df()

    q1 = """ select Policy_number, Mem_ID, icd_category, Financial_Year, count(claim_num) as claim_count,sum(Aggregate) as Aggregate
            from claim_master group by Policy_number, Mem_ID, icd_category,Financial_Year"""
    claim_count = db.execute(q1).df()

    claim_count.to_csv("CSV\\Claims_Merged.csv")
    claim_master.to_csv("CSV\\Claims_for_severity.csv")


def group_by_claim_number(claims):
    q1 = """SELECT claims.*,filter.Aggregate
    FROM claims
    JOIN
        (SELECT CLAIM_NUM, sum(PAID_AMT) as Aggregate
        FROM claims
        GROUP BY CLAIM_NUM
        ) filter
        ON claims.CLAIM_NUM = filter.CLAIM_NUM """
    consolidated_claim = db.execute(q1).df()
    consolidated_claim.drop_duplicates(subset="CLAIM_NUM", inplace=True)
    return consolidated_claim


def set_financial_year(year_p):
    return "FY" + str(year_p.to_period('Q-MAR').qyear)[2:]


def remove_group(claims, is_os):
    claims['ADMISSION_DT'] = pd.to_datetime(claims['ADMISSION_DT'], format="mixed", dayfirst=True)
    claims['DISCHARGE_DT'] = pd.to_datetime(claims['DISCHARGE_DT'], format="mixed", dayfirst=True, errors="coerce")
    claims["Financial_Year"] = claims["ADMISSION_DT"].apply(lambda x: "FY" if pd.isnull(x) else set_financial_year(x))
    if not is_os:
        claims = db.query("""select * from claims where PROD_TYPE != 'Group'""").df()
    claims.rename(columns={'POLICY_NUM': "Policy_number", "MEMBER_ID_CARD_NUM": "Mem_ID"}, inplace=True)
    claims["Policy_number"] = claims["Financial_Year"] + claims["Policy_number"]
    claims["Mem_ID"] = claims["Financial_Year"] + claims["Mem_ID"]
    claims["Days_Hospitalised"] = claims['DISCHARGE_DT'] - claims['ADMISSION_DT']
    return claims


# merge_policies()
# print("policies have been merged")
# merge_members()
# print("members  have been merged")
# merge_claim()
# print("claims  have been merged")

claim = pd.read_csv("CSV\\Claims_Merged.csv")
policy_file = pd.read_csv("CSV\\Policy_Merged.csv")
member = pd.read_csv("CSV\\Member_Merged.csv")
print("files have been loaded")
member_per_policy_count = db.sql(
    """ select Policy_number, count(Mem_ID) as members_per_policy  from member group by Policy_number """).df()
policy = policy_file.merge(member_per_policy_count, on="Policy_number")
member_claim = member.merge(claim, on=["Policy_number", "Mem_ID", "Financial_Year"], how="left")
member_count = db.sql(
    """ select Policy_number, count(Mem_ID) as count  from member_claim group by Policy_number """).df()

q2 = """select policy.Policy_number, EARNED_PREMIUM/count  as Normalized_Earned_Premium,
        POLICIES_EXPOSED/count as Normalized_POLICIES_EXPOSED , LIVES_EXPOSED/count as Normalized_LIVES_EXPOSED,
        from policy join member_count
        on policy.Policy_number =member_count.Policy_number"""
nep = db.execute(q2).df()
norm_policy = policy.merge(nep, on="Policy_number")
print("entering summaries")
summaries()
print("Creating Severity FIle ")
create_file()
