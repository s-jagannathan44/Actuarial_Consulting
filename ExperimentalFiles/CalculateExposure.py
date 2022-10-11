import pandas as pd

freq = pd.read_csv("Output\\Policies.csv")
df_freq = freq.drop(['Actual', 'Exposure'], axis=1)
df_freq = df_freq.iloc[df_freq.drop_duplicates().index]
df_freq = df_freq.reset_index(drop=True)
df_freq['GroupID'] = df_freq.index + 1
temp = df_freq.copy()


df_freq = pd.merge(freq, df_freq, how='left')
df_freq['GroupID'] = df_freq['GroupID'].fillna(method='ffill')
df_freq.set_index("GroupID", inplace=True, drop=True)


df3 = df_freq.set_index(['GenderMainDriver', 'MaritalMainDriver', 'DrivingRestriction', "Make", 'VehFuel1'])\
    .groupby(level=[0, 1, 2, 3, 4]).sum()

df3["Average_Sev"] = df3["Actual"] / df3["Exposure"]
df3["Actual"] = df3["Average_Sev"]
df3 = df3.drop(['Average_Sev'], axis=1)

df3.to_csv("Output\\pivot.csv")
df3 = pd.read_csv("Output\\pivot.csv")
df_4 = pd.merge(temp, df3, how='left')
df_4['GroupID'] = df_4['GroupID'].fillna(method='ffill')

df5 = df_4.merge(df_freq["Exposure"], on='GroupID', how="left")
df_freq = df_freq.reset_index(drop=True)
df5["Actual"] = df_freq["Actual"]
df5["Exposure"] = df5["Exposure_x"]
df5 = df5.drop(['Exposure_x', 'Exposure_y'], axis=1)

df5.set_index("GroupID", inplace=True, drop=True)
df5.to_csv("Output\\df5.csv")
