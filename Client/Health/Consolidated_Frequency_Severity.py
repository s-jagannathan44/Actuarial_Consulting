import joblib
import pandas as pd
from sklearn.model_selection import train_test_split

from Client.Health import Clubbing as FrequencyClubbing
from Client.Health import Claims_Clubbing as SeverityClubbing


def group_frequency():
    df["Revised_Individual_Floater_Frequency"] = df["Revised_Individual_Floater"].apply(
        lambda x: FrequencyClubbing.group_rif(x))
    df["Renewal_Count_Frequency"] = df["Renewal_Count"].apply(
        lambda x: "Above 8" if x > 8 else FrequencyClubbing.group_renewal_count(x))
    df["Mem_Age_Frequency"] = df["Mem_Age"].apply(lambda x: "Others" if x > 66 else FrequencyClubbing.group_age(x))
    df["Sum_Insured_Frequency"] = df["Sum_Insured"].apply(lambda x: FrequencyClubbing.group_si(x))
    df["Mem_Gender_Frequency"] = df["Mem_Gender"].apply(lambda x: FrequencyClubbing.group_gender(x))
    df["Channel_type_Frequency"] = df["Channel_type"].apply(lambda x: FrequencyClubbing.group_channel_type(x))
    df["Zone_Frequency"] = df["Zone"].apply(lambda x: FrequencyClubbing.zone_dict[x])
    df["Financial_Year"] = df["Financial_Year"].apply(lambda x: FrequencyClubbing.FY_dict[x])
    df["Product_Name_Frequency"] = df["Product_name"].apply(lambda x: FrequencyClubbing.group_product_name(x))


def group_severity():
    df["Renewal_Count_New"] = df["Renewal_Count"].apply(
        lambda x: "Other" if x > 8 else SeverityClubbing.group_renewal_count(x))
    df["Mem_Age_New"] = df["Mem_Age"].apply(lambda x: SeverityClubbing.group_age(x))
    df["Sum_Insured_New"] = df["Sum_Insured"].apply(lambda x: SeverityClubbing.group_si(x))
    df["Mem_Gender_New"] = df["Mem_Gender"].apply(lambda x: SeverityClubbing.group_gender(x))
    df["Revised_Individual_Floater_New"] = df["Revised_Individual_Floater"].apply(
        lambda x: SeverityClubbing.group_rif(x))
    df["Channel_type_New"] = df["Channel_type"].apply(lambda x: SeverityClubbing.group_channel_type(x))
    df["Product_Name_New"] = df["Product_name"].apply(lambda x: SeverityClubbing.group_product_name(x))
    df["Zone_New"] = df["Zone"].apply(lambda x: SeverityClubbing.zone_dict[x])
    # df["Financial_Year"] = df["Financial_Year"].apply(lambda x: SeverityClubbing.FY_dict[x])


def club_frequency_severity():
    global df
    df = pd.read_csv("CSV\\SummaryExposed_Merged.csv")
    for col_ in df.columns:
        if "Unnamed" in col_:
            df.drop(col_, axis=1, inplace=True)
    df = df[df["Financial_Year"].isin("FY23".split())]
    group_frequency()
    group_severity()
    df_train, df_test = train_test_split(df, test_size=0.5, random_state=0)
    df_test.to_csv("SeverityOutput\\Twenty_Percent.csv")


def execute_model(tweedie_model, dataframe):
    y_pred = tweedie_model.predict(dataframe)
    dataframe["Pred"] = y_pred
    dataframe["Pred_Count"] = dataframe["Pred"] * dataframe["LIVES_EXPOSED"]
    dataframe.to_csv("SeverityOutput\\FrequencyOutput.csv")


def execute_severity_model(gamma_model, dataframe):
    y_pred = gamma_model.predict(dataframe)
    dataframe["Pred_Sev"] = y_pred
    dataframe["Pred_Amount"] = dataframe["Pred_Sev"] * dataframe["Claim_Count"]
    dataframe.to_csv("SeverityOutput\\CombinedOutput.csv")


# club_frequency_severity()
df = pd.read_csv("SeverityOutput\\Twenty_Percent.csv")
for col in df.columns:
    if "Unnamed" in col:
        df.drop(col, axis=1, inplace=True)
df["Mem_Age_Frequency"].fillna("0.0", inplace=True)
df["Renewal_Count_Frequency"].fillna("Group 1", inplace=True)
glm = joblib.load("Frequency.sav")
execute_model(glm, df)

df = pd.read_csv("SeverityOutput\\FrequencyOutput.csv")
df.rename(columns={"PAID_AMT": "Aggregate"}, inplace=True)

for col in df.columns:
    if "Unnamed" in col:
        df.drop(col, axis=1, inplace=True)
glm = joblib.load("Severity.sav")
df["Mem_Age_New"].fillna("Group 11", inplace=True)
df["Renewal_Count_New"].fillna("0.0", inplace=True)
execute_severity_model(glm, df)

# df.rename(columns={'Mem_Age_Severity': "Mem_Age_New", 'Mem_Gender_Severity': "Mem_Gender_New",
#                    'Product_Name_Severity': 'Product_Name_New', "PAID_AMT": "Aggregate",
#                    'Renewal_Count_Severity': 'Renewal_Count_New', 'Zone_Severity': 'Zone_New',
#                    'Sum_Insured_Severity': 'Sum_Insured_New',
#                    'Revised_Individual_Floater_Severity': 'Revised_Individual_Floater_New',
#                    },
#           inplace=True)
