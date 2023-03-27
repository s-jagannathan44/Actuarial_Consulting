# This file contains Utility functions which perform the following functions
# combine_make combines makes with different spellings into one .

import pandas as pd
from matplotlib import pyplot as plt


def combine_make(filename):
    df = pd.read_csv(filename)
    Major_manufacturer = ["HERO", "BAJAJ", "HOND", "TVS", "YAMAHA", "ROYALENFIELD", "SUZUKI"]
    list_makes = df["Vehicle Make"].unique()
    OtherMakes = []

    # Below loop takes all makes not in list of major manufacturers and labels them Other
    for Make in list_makes:
        if Major_manufacturer.count(Make) == 0:
            OtherMakes.append(Make)

    for Make in Major_manufacturer:
        df.loc[df['Vehicle Make'].str.startswith(Make, na=False), 'Vehicle Make'] = Make

    for Make in OtherMakes:
        df.loc[df['Vehicle Make'].str.startswith(Make, na=False), 'Vehicle Make'] = "OTHER"
    return df


def combine_state(filename):
    df = pd.read_csv(filename, encoding='windows-1252')
    Major_States = ["Tamil Nadu", "Madhya Pradesh", "Kerala", "Karnataka", "Rajasthan", "Odisha", "West Bengal",
                    "Maharashtra", "Chattisgarh", "Telangana", "Uttar Pradesh", "Gujarat", "Andhra Pradesh",
                    "Bihar", "Haryana", "Delhi"]
    list_states = df["Registration States"].unique()
    OtherStates = []

    for State in list_states:
        if Major_States.count(State) == 0:
            OtherStates.append(State)
    for State in OtherStates:
        for index in range(len(df)):
            if index < len(df):
                if df["Registration States"].iloc[index] == State:
                    df["Registration States"].iloc[index] = df["Zone"].iloc[index]
    return df


def plot_histograms(df):
    # plotting the histogram over the whole range
    plt.hist(df["Loss Cost"], bins=200, range=(0, 10000))
    plt.xlabel('Loss Cost')
    plt.ylabel('Frequency')
    plt.title('Frequency of Loss Cost')
    plt.show()


# combine_make("D:\\2 Wheeler Magma\\Review\\Injury\\Injury_InputFile.csv")\
#     .to_csv("D:\\2 Wheeler Magma\\Review\\Injury\\Injury_Make.csv")
# combine_state("D:\\2 Wheeler Magma\\Review\\Injury\\Injury_Make.csv")\
#      .to_csv("D:\\2 Wheeler Magma\\Review\\Injury\\Injury_State.csv")
#
plot_histograms(pd.read_csv("Output\\Injury_M_NonZero.csv"))

# combine_make("D:\\2 Wheeler Magma\\Review\\Death\\Death_Input.csv")\
#     .to_csv("D:\\2 Wheeler Magma\\Review\\Death\\Death_Make.csv")
# combine_state("D:\\2 Wheeler Magma\\Review\\Death\\Death_FullFile.csv")\
#      .to_csv("D:\\2 Wheeler Magma\\Review\\Death\\Death_State.csv")
