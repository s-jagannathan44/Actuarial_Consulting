import joblib
import pandas as pd


# from sklearn.model_selection import train_test_split


def multiplier(year):
    if year == "FY23":
        return 1.07
    elif year == "FY22":
        return 1.016
    else:
        return 1.0


def execute_model(tweedie_model, dataframe):
    y_pred = tweedie_model.predict(dataframe)
    dataframe["Pred"] = y_pred
    dataframe["Pred_Cost"] = dataframe["Pred"] * dataframe["LIVES_EXPOSED"]
    dataframe.to_csv("Output\\text_numeric.csv")


# df = df[~ df["Revised_Product_Name_New"].isin("SURPLUS-FLOATERFLOATER SURPLUS-FLOATERMED-PLT-046 "
#                                               "SURPLUS-INDINDIVIDUAL Corona Kavach PolicyFLOATER "
#                                               "Corona Kavach PolicyINDIVIDUAL"
#                                               " Star Hospital Cash Insurance PolicyFLOATER ".split())]
FY_dict = {"FY18": 0, "FY19": 1, "FY20": 2, "FY22": 4, "FY23": 5}
df = pd.read_csv("Output\\TwentyPercentUnClubbed.csv")
for col in df.columns:
    if "Unnamed" in col:
        df.drop(col, axis=1, inplace=True)
df["Mem_Age_New"].fillna("0.0", inplace=True)
df["Renewal_Count_New"].fillna("0.0", inplace=True)
df = df[df["Financial_Year"].isin("FY18 FY19 FY20 FY22 FY23".split())]
df["PAID_AMT"] = df["PAID_AMT"] * df["Financial_Year"].apply(lambda x: multiplier(x))
df["Financial_Year"] = df["Financial_Year"].apply(lambda x: FY_dict[x])
glm = joblib.load("Tweedie.sav")
execute_model(glm, df)
