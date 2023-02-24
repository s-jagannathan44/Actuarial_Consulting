import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

def print_details():
    print("The number of rows and columns are " + str(df.shape))
    print(df.info())
    # How many years does the data cover?
    print("The number of unique years are " + str(df.AnalysisPeriod.nunique()) + '\n')
    # What are the possible values for 'Age'?
    print("The possible values for 'Gender' are " + str(df.GenderMainDriver.unique()) + '\n')
    # How many states are there?
    print("The possible values for 'MaritalStatus' are  " + str(df.MaritalMainDriver.nunique()) + '\n')
    # How many insurance providers are there?
    print("The possible values for 'Age' are " + str(df.VehicleAge.nunique()) + '\n')
    print("The average value for the Claim  is " + str(df.Claim.mean()))
    print("The max value for the Claim  for a policy  is " + str(df.Claim.max()))
    print("The min value for Claim  is " + str(df.Claim.min()))


def plot_histograms():
    # plotting the histogram over the whole range
    plt.hist(df.Claim, bins=20)
    plt.xlabel('Claim')
    plt.ylabel('Frequency')
    plt.title('Frequency of Claim')
    plt.show()
    # plotting the histogram from 800000 to 1000000
    plt.hist(df.Claim, bins=20, range=(3000, 18000))
    plt.xlabel('Individual Rate')
    plt.ylabel('Frequency')
    plt.title('Frequency of Claim ')
    plt.show()
    plt.hist(df.Claim, bins=50, range=(51, 3000))
    plt.xlabel('Individual Rate')
    plt.ylabel('Frequency')
    plt.title('Frequency of Claim ')


def summary(data, x):
    x_min = data[x].min()
    x_max = data[x].max()
    Q1 = data[x].quantile(0.25)
    Q2 = data[x].quantile(0.50)
    Q3 = data[x].quantile(0.75)
    print(f'5 Point Summary of {x.capitalize()} Attribute:\n'
          f'{x.capitalize()}(min) : {x_min}\n'
          f'Q1                    : {Q1}\n'
          f'Q2(Median)            : {Q2}\n'
          f'Q3                    : {Q3}\n'
          f'{x.capitalize()}(max) : {x_max}')

    fig = plt.figure(figsize=(16, 10))
    plt.subplots_adjust(hspace=0.6)
    sns.set_palette('pastel')

    plt.subplot(221)
    ax1 = sns.histplot(data[x], color='r')
    plt.title(f'{x.capitalize()} Density Distribution')

    plt.subplot(222)
    ax2 = sns.violinplot(x=data[x], palette='Accent', split=True)
    plt.title(f'{x.capitalize()} Violinplot')

    plt.subplot(223)
    ax2 = sns.boxplot(x=data[x], palette='cool', width=0.7, linewidth=0.6)
    plt.title(f'{x.capitalize()} Boxplot')

    plt.subplot(224)
    ax3 = sns.kdeplot(data[x], cumulative=True)
    plt.title(f'{x.capitalize()} Cumulative Density Distribution')

    plt.show()


def data_analysis():
    for c in df.columns:
        csv_file_name = "Output\\Columns\\" + c.replace("/", "_") + ".csv"
        insight = df[c].value_counts()
        insight.to_csv(csv_file_name)
    df.describe(percentiles=[0.25, 0.5, 0.75, 0.85, 0.9, 0.98, 1]).to_csv("Output\\Columns\\desc.csv")


df = pd.read_csv("Output\\Policies.csv")
for col in df.columns:
    if "Unnamed" in col:
        df.drop(col, axis=1, inplace=True)

df.set_index("PolicyReference", inplace=True, drop=True)


summary(df, 'VehicleAge')
# data_analysis()
# print_details()
# plot_histograms()

# rotate the axis and set a bigger fig size to ease reading
df.boxplot(column='Claim', by='GenderMainDriver', rot=90, fontsize=9, figsize=(10, 10))
df.boxplot(column='Claim', by='VehicleAge', rot=90, fontsize=9, figsize=(10, 10))
groupbyAge = df.groupby('VehicleAge').agg({"Claim": ['nunique']})
groupbyAge = groupbyAge.reset_index()
groupbyAge.columns = groupbyAge.columns.droplevel(0)
groupbyAge.rename(columns={'': 'VehicleAge'}, inplace=True)
# groupbyAge.T.to_csv("plot.csv")

plt.show()

# aggregate the data to find the number of insurance companies by state
# groupbyVehicleAge = df.groupby('StateCode').agg({'IssuerId':{'companies_count':'nunique'}})
# groupbystate=groupbystate.reset_index()
# groupbystate.columns=groupbystate.columns.droplevel(0)
# groupbystate.rename(columns = {'':'StateCode'},inplace = True)
# plt.bar(groupbystate.StateCode,groupbystate.companies_count)
# plt.title('No. of insurance issuers in each state')
# plt.xlabel('State Code')
# plt.ylabel('No.of insurance issuers')
# plt.xticks(rotation=90,fontsize=7)
# plt.show()
