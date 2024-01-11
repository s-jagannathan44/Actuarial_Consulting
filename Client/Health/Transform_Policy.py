import pandas as pd


def rename_columns():
    dx = pd.read_csv("C:\\SHAI\\Revised 11-12-23\\FY22 Exposure Mapped_Final.csv",
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


def merge_policy():
    df11 = pd.read_csv("CSV\\Policy21.csv")
    df12 = pd.read_csv("CSV\\Policy22.csv")
    df13 = pd.read_csv("CSV\\Policy23.csv")
    df10 = pd.concat([df11, df12, df13], axis=0)
    for col in df10.columns:
        if "Unnamed" in col:
            df10.drop(col, axis=1, inplace=True)

    df10.to_csv("CSV\\Policy_Merged.csv")


def group_suminsured():
    df2 = pd.pivot_table(df, values="EARNED_PREMIUM", columns="Sum_Insured", aggfunc="sum")
    df2 = df2.transpose()
    df2 = df2.sort_values(by='EARNED_PREMIUM', axis=0, ascending=False)
    df2['cumpct'] = df2['EARNED_PREMIUM'].cumsum() / df2['EARNED_PREMIUM'].sum() * 100
    df2.reset_index(inplace=True)
    x = df2[df2['cumpct'] >= 90]["Sum_Insured"]
    df["Sum_Insured"].replace(x.tolist(), "Other", inplace=True)
    return df


def group_channel_type():
    df2 = pd.pivot_table(df, values="EARNED_PREMIUM", columns="Channel_type", aggfunc="sum")
    df2 = df2.transpose()
    df2 = df2.sort_values(by='EARNED_PREMIUM', axis=0, ascending=False)
    df2['cumpct'] = df2['EARNED_PREMIUM'].cumsum() / df2['EARNED_PREMIUM'].sum() * 100
    df2.reset_index(inplace=True)
    x = df2[df2['cumpct'] >= 99]["Channel_type"]
    df["Channel_type"].replace(x.tolist(), "Other", inplace=True)
    return df


def group_product_plan_floater():
    df["product_plan_floater"] = df["Product_name"] + df["Revised_Individual_Floater"] + df[
        "Revised_Individual_Floater"]
    df2 = pd.pivot_table(df, values="EARNED_PREMIUM", columns=["product_plan_floater"], aggfunc="sum")
    df2 = df2.transpose()
    df2 = df2.sort_values(by='EARNED_PREMIUM', axis=0, ascending=False)
    df2['cumpct'] = df2['EARNED_PREMIUM'].cumsum() / df2['EARNED_PREMIUM'].sum() * 100
    df2.reset_index(inplace=True)
    x = df2[df2['cumpct'] >= 90]["product_plan_floater"]

    df["product_plan_floater"].replace(x.tolist(), "Other", inplace=True)
    return df


df = rename_columns()

df["Financial_Year"] = "FY22"
df["Policy_number"] = df["Policy_number"].apply(lambda x: "FY22"+x)

# group_suminsured()
# group_channel_type()
# group_product_plan_floater()
df.to_csv("CSV\\Policy22.csv")
