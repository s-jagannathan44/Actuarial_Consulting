import pandas as pd

# Step 1 read file and set index
df = pd.read_csv("Output\\Data.csv")
df.set_index("Sl. No", inplace=True, drop=True)

# Step 2 set filter condition and write to file
cond_ = (df["CLAIM_COUNT"] > 0) & (df["Register 1"] == "Settled") & (df['TOTAL_OURSHARE'] > 0) & \
         df['TOTAL_OURSHARE'].notnull() & df['Make'].notnull()
df = df.loc[cond_]
df.drop(df[(df["RTO State - RTO State"] == "(None)") & (df["RTO State - RTO State"].isnull())].index, inplace=True)
df.to_csv("Output\\Commercial.csv")


# Step 3 write column wise analysis to files
col_list = ["FY", "TP Pool / Non TP Pool", "Segment 1", "Make", "RTO State - RTO State", "Loss Type", "Product Type 1",
            "TOTAL_OURSHARE"]
for c in col_list:
    csv_file_name = "Output\\V1\\" + c.replace("/", "_") + ".csv"
    insight = df[c].value_counts()
    insight.to_csv(csv_file_name)
df.describe(percentiles=[0.25, 0.5, 0.75, 0.85, 0.9, 0.98, 1]).to_csv("Output\\V1\\V1_desc.csv")

# & (df["Loss Type"] == "Injury") \
#        & (df["FY"].isin(["2018-19", "2019-20", "2020-21"])) & (df["Product Type 1"] == "Commercial Veh")
