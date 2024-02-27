import joblib
import pandas as pd


def execute_model(tweedie_model, dataframe):
    y_pred = tweedie_model.predict(dataframe)
    dataframe["Pred"] = y_pred
    dataframe["Pred_Cost"] = dataframe["Pred"] * dataframe["LIVES_EXPOSED"]
    dataframe.to_csv("Output\\forecast_24.csv")


FY_dict = {"FY18": 0, "FY19": 1, "FY20": 2, "FY22": 4, "FY23": 5}
df = pd.read_csv("Output\\clubbed_file_24.csv")
for col in df.columns:
    if "Unnamed" in col:
        df.drop(col, axis=1, inplace=True)
df["Mem_Age_New"].fillna("0.0", inplace=True)
df["Renewal_Count_New"].fillna("0.0", inplace=True)
df["Financial_Year"] = 6
# df = df[df["Financial_Year"].isin("FY18 FY19 FY20 FY22 FY23".split())]
# df["Financial_Year"] = df["Financial_Year"].apply(lambda x: FY_dict[x])
glm = joblib.load("Tweedie.sav")
execute_model(glm, df)
