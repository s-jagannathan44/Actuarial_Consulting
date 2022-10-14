import pandas as pd

col_list = ["VehicleValue", "GenderMainDriver", "MaritalMainDriver", "Make", "Use", "PaymentMethod", "PaymentFrequency"]
full_list = ["VehicleValue", "GenderMainDriver", "MaritalMainDriver", "Make", "Use", "PaymentMethod",
             "PaymentFrequency", "Exposure"]
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

df3 = df_freq.set_index(col_list).groupby(level=[0, 1, 2, 3, 4, 5, 6]).sum()


df3.to_csv("Output\\pivot.csv")
df3 = pd.read_csv("Output\\pivot.csv")
df_4 = pd.merge(temp, df3, how='left')
df_4['GroupID'] = df_4['GroupID'].fillna(method='ffill')
df_4.set_index("GroupID", inplace=True, drop=True)
df_4["Key"] = df_4["GenderMainDriver"] + df_4["MaritalMainDriver"] + df_4["Make"] + df_4["Use"] \
              + df_4["PaymentMethod"] + df_4["PaymentFrequency"] + df_4["VehicleValue"].astype(str)

# df_4.to_csv("Output\\pivot.csv")

freq = pd.read_csv("Output\\Policies.csv")
full_list = full_list + ["Actual"]
freq = freq[full_list]
freq["Key"] = freq["GenderMainDriver"] + freq["MaritalMainDriver"] + freq["Make"] + freq["Use"] \
              + freq["PaymentMethod"] + freq["PaymentFrequency"] + freq["VehicleValue"].astype(str)

# freq.to_csv("Output\\P.csv")

df = pd.merge(
    left=freq,
    right=df_4,
    on="Key",
    how='left'
)

df.to_csv("Output\\df.csv")
