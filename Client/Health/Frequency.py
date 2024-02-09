import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.linear_model import TweedieRegressor


# ('ordinal_categorical', OrdinalEncoder(), ["Financial_Year"]),
def build_model():
    global df_train, df_test
    linear_model_preprocessor = ColumnTransformer(
        [
            (
                "onehot_categorical",
                OneHotEncoder(),
                "Renewal_Count_New".split()
            ),
        ],

        remainder='drop'
    )

    interaction = make_pipeline(
        OneHotEncoder(),
        PolynomialFeatures(degree=3, interaction_only=True, include_bias=False)
    )
    column_trans = ColumnTransformer(
        [('interaction', interaction, "Revised_Individual_Floater_New Mem_Gender_New Mem_Age_New".split())],
        remainder='drop')

    print(df_test.shape, df_train.shape)
    tweedie_glm = Pipeline(
        [
            ("interaction", column_trans),
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
                         aggfunc="sum").T
    df2["Actual"] = df2["PAID_AMT"] / df2["LIVES_EXPOSED"]
    df2["Predicted"] = df2["Pred_Cost"] / df2["LIVES_EXPOSED"]
    df2["Error"] = (df2["Actual"] - df2["Predicted"]) / df2["Actual"]
    df2['Error'] = df2['Error'].map('{:.2%}'.format)
    df2.to_csv("Output\\" + columns + ".csv")


def make_multi(dataframe, columns):
    df2 = pd.pivot_table(dataframe, values="PAID_AMT Pred_Cost LIVES_EXPOSED".split(), columns=columns,
                         aggfunc="sum").T
    df2["Actual"] = df2["PAID_AMT"] / df2["LIVES_EXPOSED"]
    df2["Predicted"] = df2["Pred_Cost"] / df2["LIVES_EXPOSED"]
    df2["Error"] = (df2["Actual"] - df2["Predicted"]) / df2["Actual"]
    df2['Error'] = df2['Error'].map('{:.2%}'.format)
    df2.to_csv("Output\\multi.csv")


def execute_model(tweedie_model, dataframe):
    # dataframe.to_csv("Output\\text.csv")
    y_pred = tweedie_model.predict(dataframe)
    dataframe["Pred"] = y_pred
    dataframe["Pred_Cost"] = dataframe["Pred"] * dataframe["LIVES_EXPOSED"]
    dataframe.to_csv("Output\\text_out.csv")
    # make_pivots(dataframe, "Revised_Individual_Floater_New")
    # make_pivots(dataframe, "Mem_Gender_New")
    # make_pivots(dataframe, "Mem_Age_New")
    make_multi(dataframe, "Revised_Individual_Floater_New Mem_Gender_New Mem_Age_New".split())


def othering(dataframe):
    make_pivots(dataframe, "Revised_Individual_Floater_New")
    make_pivots(dataframe, "Product_Name_New")
    make_pivots(dataframe, "Zone")
    make_pivots(dataframe, "Mem_Age_New")
    make_pivots(dataframe, "Mem_Gender_New")
    make_pivots(dataframe, "Renewal_Count_New")
    make_pivots(dataframe, "Channel_type_New")
    make_pivots(dataframe, "Sum_Insured_New")


# df = pd.read_csv("CSV\\SummaryExposed_Merged.csv", usecols="Mem_Age Mem_Gender LIVES_EXPOSED "
#                                                            "PAID_AMT Financial_Year Renewal_Count "
#                                                            "Revised_Individual_Floater".split())
# df2 = pd.pivot_table(df, values="PAID_AMT LIVES_EXPOSED".split(),
#                      columns="Mem_Age  Mem_Gender Revised_Individual_Floater Renewal_Count".split(),
#                      aggfunc="sum").T
#
# df2["Actual"] = df2["PAID_AMT"] / df2["LIVES_EXPOSED"]
# df2.to_csv("Output\\multi.csv")
# train, df = train_test_split(input_file, test_size=0.2, random_state=0)
# df.to_csv("Output\\OOS.csv")

df = pd.read_csv("CSV\\FrequencyModelFile.csv", usecols="Mem_Age_New Mem_Gender_New LIVES_EXPOSED "
                                                        "PAID_AMT Financial_Year  "
                                                        "Product_Name_New Revised_Individual_Floater_New".split())
for col in df.columns:
    if "Unnamed" in col:
        df.drop(col, axis=1, inplace=True)
df = df[df["LIVES_EXPOSED"] >= 1]
# df = df[(df['PAID_AMT'] != 0) & (df['PAID_AMT'] != -851)]
df = df[~ df["Product_Name_New"].isin("SURPLUS-FLOATER".split())]
df = df[df["Financial_Year"].isin("FY18 FY19 FY20 FY22 FY23".split())]
df["Loss_Cost"] = df["PAID_AMT"] / df["LIVES_EXPOSED"]
df["Loss_Cost"].fillna(0, inplace=True)
# df["Revised_Individual_Floater_New"].fillna("INDIVIDUAL", inplace=True)
df_train, df_test = train_test_split(df, test_size=0.2, random_state=0)
glm = build_model()
execute_model(glm, df_test)
