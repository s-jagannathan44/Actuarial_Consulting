import pandas as pd
from matplotlib import pyplot as plt


# Code to Plot Histogram
def plot_histograms(df_):
    # plotting the histogram over the whole range
    plt.hist(df_["Claim_Count"], bins=200, range=(0, 200))
    plt.xlabel('Claim Count')
    plt.ylabel('Frequency')
    plt.title('Frequency of Claim')
    plt.show()


# code to create pivot table and find rows which makes up 90% of premium amount
df = pd.read_csv("Sheet1.csv")
df2 = pd.pivot_table(df, values="Premium", columns="SI", aggfunc="sum")
df2 = df2.transpose()
df2 = df2.sort_values(by='Premium', axis=0, ascending=False)
df2['cumpct'] = df2['Premium'].cumsum() / df2['Premium'].sum() * 100
df2.reset_index(inplace=True)
x = df2[df2['cumpct'] >= 90]["SI"]
df.replace(x.tolist(), "Other", inplace=True)
print(df)
# end of code

# query to find top 20% of rows
q2 = """select df.*
from (select df.*,
             row_number() over (order by Premium desc) as seqnum,
             count(*) over () as cnt
      from df
     ) df
where seqnum <= 0.2 * cnt"""
