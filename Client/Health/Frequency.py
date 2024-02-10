import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.linear_model import TweedieRegressor


def build_model():
    global df_train, df_test

    interaction = make_pipeline(
        OneHotEncoder(),
        PolynomialFeatures(degree=3, interaction_only=True, include_bias=False)
    )
    # interactive_2 = make_pipeline(OneHotEncoder(),
    #                               PolynomialFeatures(degree=2, interaction_only=True, include_bias=False))
    non_interactive = make_pipeline(OneHotEncoder())

    column_trans = ColumnTransformer(
        [
            ('interaction', interaction,
             "Revised_Product_Name_New Mem_Gender_New Mem_Age_New Renewal_Count_New".split()),
            # ('interactive_2', interactive_2, "Mem_Age_New Renewal_Count_New".split()),
            # ('non_interactive', non_interactive, "Zone_New Channel_type_New Sum_Insured_New".split()),
        ],
    )

    print(df_test.shape, df_train.shape)
    tweedie_glm = Pipeline(
        [
            ("transform", column_trans),
            ("regressor", TweedieRegressor(power=1.9, alpha=1e-12, max_iter=1000)),
        ]
    )
    tweedie_glm.fit(
        df_model, df_train["Loss_Cost"], regressor__sample_weight=df_train["LIVES_EXPOSED"]
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
    # make_pivots(dataframe, "Sum_Insured_New")
    make_multi(dataframe, "Revised_Product_Name_New Mem_Gender_New Mem_Age_New Renewal_Count_New"
                          .split())


def othering(dataframe):
    make_pivots(dataframe, "Revised_Individual_Floater_New")
    # make_pivots(dataframe, "Product_Name_New")
    make_pivots(dataframe, "Zone_New")
    make_pivots(dataframe, "Mem_Age_New")
    make_pivots(dataframe, "Mem_Gender_New")
    # make_pivots(dataframe, "Renewal_Count_New")
    # make_pivots(dataframe, "Channel_type_New")
    # make_pivots(dataframe, "Sum_Insured_New")


def find_separation():
    df_ = pd.read_csv("CSV\\FrequencyModelFile.csv", usecols="LIVES_EXPOSED "
                                                             "PAID_AMT "
                                                             "Revised_Product_Name_New".split())
    df2 = pd.pivot_table(df_, values="PAID_AMT LIVES_EXPOSED".split(),
                         columns="Revised_Product_Name_New".split(),
                         aggfunc="sum").T
    df2["Actual"] = df2["PAID_AMT"] / df2["LIVES_EXPOSED"]
    df2.to_csv("Output\\multi.csv")


df = pd.read_csv("CSV\\FrequencyModelFile.csv", usecols="Mem_Age_New Mem_Gender_New LIVES_EXPOSED "
                                                        "PAID_AMT Financial_Year Renewal_Count_New Zone_New "
                                                        "Revised_Product_Name_New Channel_type_New Sum_Insured_New "
                 .split())
for col in df.columns:
    if "Unnamed" in col:
        df.drop(col, axis=1, inplace=True)
df = df[df["LIVES_EXPOSED"] >= 1]
# df = df[(df['PAID_AMT'] != 0) & (df['PAID_AMT'] != -851)]
df = df[~ df["Revised_Product_Name_New"].isin("SURPLUS-FLOATERFLOATER SURPLUS-FLOATERMED-PLT-046 "
                                              "SURPLUS-INDINDIVIDUAL Corona Kavach PolicyFLOATER "
                                              "Corona Kavach PolicyINDIVIDUAL"
                                              " Star Hospital Cash Insurance PolicyFLOATER ".split())]
df = df[df["Financial_Year"].isin("FY18 FY19 FY20 FY22 FY23".split())]
df["Loss_Cost"] = df["PAID_AMT"] / df["LIVES_EXPOSED"]
df["Loss_Cost"].fillna(0, inplace=True)
df["Pred_Cost"] = df["Loss_Cost"]
df_train, df_test = train_test_split(df, test_size=0.2, random_state=0)
df_model = df_train[['Mem_Age_New', "Mem_Gender_New", "Revised_Product_Name_New", "Renewal_Count_New"
                     ]]
glm = build_model()
execute_model(glm, df_test)
