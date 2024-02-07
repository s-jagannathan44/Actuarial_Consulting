import joblib
import pandas as pd
from sklearn.metrics import d2_tweedie_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import TweedieRegressor
from sklearn.metrics import log_loss


# ('ordinal_categorical', OrdinalEncoder(), ["Financial_Year"]),
def build_model():
    global df_train, df_test
    linear_model_preprocessor = ColumnTransformer(
        [
            (
                "onehot_categorical",
                OneHotEncoder(),
                "Revised_Individual_Floater_New".split()
            ),
        ],
        remainder='drop'
        # remainder ='passthrough'
    )
    print(df_test.shape, df_train.shape)
    tweedie_glm = Pipeline(
        [
            ("preprocessor", linear_model_preprocessor),
            ("regressor", TweedieRegressor(power=1.9, alpha=1e-12, max_iter=300)),
        ]
    )
    tweedie_glm.fit(
        df_train, df_train["Loss_Cost"], regressor__sample_weight=df_train["LIVES_EXPOSED"]
    )
    joblib.dump(tweedie_glm, "Tweedie.sav")
    return tweedie_glm


def make_pivots(dataframe, columns):
    df2 = pd.pivot_table(dataframe, values="PAID_AMT Pred_Cost LIVES_EXPOSED".split(), columns=columns,
                         aggfunc="sum")
    df2 = df2.transpose()
    df2["Actual"] = df2["PAID_AMT"] / df2["LIVES_EXPOSED"]
    df2["Predicted"] = df2["Pred_Cost"] / df2["LIVES_EXPOSED"]
    df2["Error"] = (df2["Actual"] - df2["Predicted"]) / df2["Actual"]
    df2.to_csv("Output\\" + columns + ".csv")


def make_multi(dataframe, columns):
    df2 = pd.pivot_table(dataframe, values="PAID_AMT Pred_Cost LIVES_EXPOSED".split(), columns=columns,
                         aggfunc="sum")
    df2 = df2.transpose()
    df2["Actual"] = df2["PAID_AMT"] / df2["LIVES_EXPOSED"]
    df2["Predicted"] = df2["Pred_Cost"] / df2["LIVES_EXPOSED"]
    df2["Error"] = (df2["Actual"] - df2["Predicted"]) / df2["Actual"]
    df2.to_csv("Output\\multi.csv")


def execute_model(tweedie_model, dataframe):
    # dataframe.to_csv("Output\\text.csv")
    y_pred = tweedie_model.predict(dataframe)
    dataframe["Pred"] = y_pred
    dataframe["Pred_Cost"] = dataframe["Pred"] * dataframe["LIVES_EXPOSED"]
    dataframe.to_csv("Output\\text_out.csv")
    # print(d2_tweedie_score(dataframe["Loss_Cost"], y_pred, power=1.9, sample_weight=dataframe["LIVES_EXPOSED"]))
    print(log_loss(dataframe["Loss_Cost"], y_pred, sample_weight=dataframe["LIVES_EXPOSED"]))
    make_pivots(dataframe, "Revised_Individual_Floater_New")
    # make_pivots(dataframe, "Product_Name_New")
    # make_pivots(dataframe, "Zone")
    # make_multi(dataframe, "Zone Product_Name_New Revised_Individual_Floater_New".split())


def othering(dataframe):
    make_pivots(dataframe, "Revised_Individual_Floater_New")
    make_pivots(dataframe, "Product_Name_New")
    make_pivots(dataframe, "Zone")
    make_pivots(dataframe, "Mem_Age_New")
    make_pivots(dataframe, "Mem_Gender_New")
    make_pivots(dataframe, "Renewal_Count_New")
    make_pivots(dataframe, "Channel_type_New")
    make_pivots(dataframe, "Sum_Insured_New")


df = pd.read_csv("CSV\\FrequencyModelFile.csv")

# train, df = train_test_split(input_file, test_size=0.2, random_state=0)
# df.to_csv("Output\\OOS.csv")
for col in df.columns:
    if "Unnamed" in col:
        df.drop(col, axis=1, inplace=True)
df = df[df["LIVES_EXPOSED"] >= 1]
df = df[(df['PAID_AMT'] != 0) & (df['PAID_AMT'] != -851)]
df = df[~ df["Product_Name_New"].isin("SURPLUS-FLOATER".split())]
df = df[df["Financial_Year"].isin("FY18 FY19 FY20 FY22 FY23".split())]
df["Loss_Cost"] = df["PAID_AMT"] / df["LIVES_EXPOSED"]
df["Loss_Cost"].fillna(0, inplace=True)
df_train, df_test = train_test_split(df, test_size=0.2, random_state=0)
glm = build_model()
execute_model(glm, df_test)
