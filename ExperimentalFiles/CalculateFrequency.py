import pandas as pd

col_list = ["AnalysisPeriod", "AgeMainDriver",
            'VehicleAge', 'BonusMalusYears',
            'PolicyTenure', "GenderMainDriver", "GenderYoungestDriver",
            "Use", "PaymentMethod", "BonusMalusProtection"]
full_list = col_list + ['Claim Count']
freq = pd.read_csv("Output\\Policies.csv")
freq = freq[full_list]
df_freq = freq[col_list]

df_freq = df_freq.iloc[df_freq.drop_duplicates().index]
df_freq = df_freq.reset_index(drop=True)
df_freq['GroupID'] = df_freq.index + 1
temp = df_freq.copy()

df_freq = pd.merge(freq, df_freq, how='left')
df_freq['GroupID'] = df_freq['GroupID'].fillna(method='ffill')
df_freq.set_index("GroupID", inplace=True, drop=True)
df_freq.to_csv("Output\\pivot.csv")

freq = pd.read_csv("Output\\pivot.csv")
freq = freq.groupby(col_list).sum()
freq.to_csv("Output\\pivot2.csv")
