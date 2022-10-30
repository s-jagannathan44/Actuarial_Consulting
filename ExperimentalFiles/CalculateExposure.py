import pandas as pd
import Modules.Utilities as Ut

col_list = ["AnalysisPeriod", "NumberOfDrivers", "VoluntaryExcess",
            "NumberOfPastClaims", "NumberOfPastConvictions", "ClaimLastYr", "AgeMainDriver",
            'AgeYoungestDriver', 'AgeYoungestAdditionalDriver', 'VehicleAge', 'VehicleValue', 'VehicleMileage', 'BonusMalusYears',
            'PolicyTenure', "GenderMainDriver", "GenderYoungestDriver",
            "MaritalMainDriver", "Use", "PaymentMethod", 'GenderYoungestAdditionalDriver', "BonusMalusProtection",
            "VehFuel1"]
full_list = col_list + ['Exposure']
freq = pd.read_csv("Output\\Policies.csv")
freq = Ut.impute_missing_values(freq, "AgeYoungestAdditionalDriver")
freq = Ut.impute_missing_values(freq, "GenderYoungestAdditionalDriver")
freq = freq[full_list]
df_freq = freq[col_list]

df_freq = df_freq.iloc[df_freq.drop_duplicates().index]
df_freq = df_freq.reset_index(drop=True)
df_freq['GroupID'] = df_freq.index + 1
temp = df_freq.copy()

df_freq = pd.merge(freq, df_freq, how='left')
df_freq['GroupID'] = df_freq['GroupID'].fillna(method='ffill')
df_freq.set_index("GroupID", inplace=True, drop=True)
df_freq = df_freq.groupby(col_list).sum()

df_freq.to_csv("Output\\pivot2.csv")
df_4 = pd.read_csv("Output\\pivot2.csv")
df_4["Key"] = " "
for col in col_list:
    df_4["Key"] = df_4["Key"] + df_4[col].astype(str)

freq = pd.read_csv("Output\\Policies.csv")
freq = Ut.impute_missing_values(freq, "AgeYoungestAdditionalDriver")
freq = Ut.impute_missing_values(freq, "GenderYoungestAdditionalDriver")

temp_list = col_list + ["Actual"]
freq = freq[temp_list]
freq["Key"] = " "
for col in col_list:
    freq["Key"] = freq["Key"] + freq[col].astype(str)

freq.to_csv("Output\\freq.csv")
df_4.to_csv("Output\\df_4.csv")

df = pd.merge(df_4, freq,  on='Key')


df.to_csv("Output\\df.csv")
