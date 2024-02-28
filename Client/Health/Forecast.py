import joblib
import pandas as pd
# from sklearn.model_selection import train_test_split
#
# df = pd.read_csv("Output\\clubbed_file_AgeModified.csv")
# df_train, df_test = train_test_split(df, test_size=0.2, random_state=0)
# df_test.to_csv("Output\\TwentyPercentUnClubbed_AgeModified.csv")


def execute_model(tweedie_model, dataframe):
    y_pred = tweedie_model.predict(dataframe)
    dataframe["Pred"] = y_pred
    dataframe["Pred_Cost"] = dataframe["Pred"] * dataframe["LIVES_EXPOSED"]
    dataframe.to_csv("Output\\27Feb_AgeModified.csv")


FY_dict = {"FY18": 0, "FY19": 1, "FY20": 2, "FY22": 4, "FY23": 5}
df = pd.read_csv("Output\\TwentyPercentUnClubbed_AgeModified.csv")
for col in df.columns:
    if "Unnamed" in col:
        df.drop(col, axis=1, inplace=True)
df["Mem_Age_New"].fillna("Others", inplace=True)
df["Renewal_Count_New"].fillna("Above 8", inplace=True)
# df["Financial_Year"] = 6
df = df[df["Financial_Year"].isin([0, 1, 2, 4, 5])]
glm = joblib.load("Tweedie.sav")
execute_model(glm, df)
