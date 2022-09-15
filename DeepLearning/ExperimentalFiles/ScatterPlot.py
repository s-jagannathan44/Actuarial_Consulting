import matplotlib.pyplot as plt
import pandas as pd

freq = pd.read_csv("Output\\X_test.csv")
df_freq = freq.iloc[freq.drop_duplicates().index]
df_freq = df_freq.reset_index(drop=True)
df_freq['GroupID'] = df_freq.index + 1
df_freq = pd.merge(freq, df_freq, how='left')
df_freq['GroupID'] = df_freq['GroupID'].fillna(method='ffill')
df_freq.set_index("GroupID", inplace=True, drop=True)
df_group = df_freq.groupby(by=['GroupID'], as_index=False)

# print(df_group.agg("sum"))
# print(df_group.first())
# GroupBy multiple columns using pivot function
# df2 = df_freq.groupby(['Gender', 'MaritalMainDriver', 'DrivingRestriction', 'VehFuel1'], as_index=False).\
#    sum().pivot('Gender', 'MaritalMainDriver', 'DrivingRestriction', 'VehFuel1').fillna(0)
df3 = df_freq.set_index(['Gender', 'MaritalMainDriver', 'DrivingRestriction', "Make", 'VehFuel1'])\
    .groupby(level=[0, 1, 2, 3, 4]).sum()

df3.to_csv("Output\\pivot.csv")
x = df3["Actual"]
y = df3["Predicted"]
plt.scatter(x, y)
plt.show()


# df_freq.to_csv("Output\\X_drop.csv")
# df_group.to_csv("Output\\X_group.csv")
