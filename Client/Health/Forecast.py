import joblib
import pandas as pd
from sklearn.model_selection import train_test_split


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
    dataframe.to_csv("Output\\test_output.csv")


# input_file = pd.read_csv("Output\\clubbed_file.csv")
#
# df_train, df = train_test_split(input_file, test_size=0.2, random_state=0)
df = pd.read_csv("Output\\TwentyPercentUnClubbed.csv")
df["Mem_Age_New"].fillna("0.0", inplace=True)
df["Renewal_Count_New"].fillna("0.0", inplace=True)

df["PAID_AMT"] = df["PAID_AMT"] * df["Financial_Year"].apply(lambda x: multiplier(x))
df = df[df["Financial_Year"].isin("FY18 FY19 FY20 FY22 FY23".split())]
# df = df[~ df["Revised_Product_Name_New"].isin("SURPLUS-FLOATERFLOATER SURPLUS-FLOATERMED-PLT-046 "
#                                               "SURPLUS-INDINDIVIDUAL Corona Kavach PolicyFLOATER "
#                                               "Corona Kavach PolicyINDIVIDUAL"
#                                               " Star Hospital Cash Insurance PolicyFLOATER ".split())]
glm = joblib.load("Tweedie.sav")
execute_model(glm, df)

