import pandas as pd
import joblib


def execute_model(tweedie_model, dataframe):
    y_pred = tweedie_model.predict(dataframe)
    dataframe["Pred"] = y_pred
    dataframe["Pred_Cost"] = dataframe["Pred"] * dataframe["sum_insured_in_hundreds"]
    dataframe.to_csv("Output\\ModelOutput.csv")


def make_pivots(dataframe, column):
    df2 = pd.pivot_table(dataframe,
                         values="ultimate_paid_non_large  Pred_Cost sum_insured_in_hundreds Normalized_LIVES_EXPOSED".split(),
                         columns=column,
                         aggfunc="sum").T
    df2["Actual"] = df2["ultimate_paid_non_large"] / df2["sum_insured_in_hundreds"]
    df2["Predicted"] = df2["Pred_Cost"] / df2["sum_insured_in_hundreds"]
    df2["Error"] = (df2["Predicted"] - df2["Actual"]) / df2["Actual"]
    df2["AbsError"] = df2["Error"].abs()
    df2['%ageError'] = df2['Error'].map('{:.2%}'.format)
    df2.sort_values(by='Normalized_LIVES_EXPOSED', ascending=False, inplace=True)
    df2.to_csv("Output\\Errors\\" + column + ".csv")


def make_multi(dataframe, columns):
    df2 = pd.pivot_table(dataframe,
                         values="ultimate_paid_non_large  Pred_Cost sum_insured_in_hundreds Normalized_LIVES_EXPOSED".split(),
                         columns=columns,
                         aggfunc="sum").T
    df2["Actual"] = df2["ultimate_paid_non_large"] / df2["sum_insured_in_hundreds"]
    df2["Predicted"] = df2["Pred_Cost"] / df2["sum_insured_in_hundreds"]
    df2["Error"] = (df2["Predicted"] - df2["Actual"]) / df2["Actual"]
    df2["AbsError"] = df2["Error"].abs()
    df2['%ageError'] = df2['Error'].map('{:.2%}'.format)
    df2.sort_values(by='Normalized_LIVES_EXPOSED', ascending=False, inplace=True)
    df2.to_csv("Output\\Errors\\" + "multi" + ".csv")


def CombineModels():
    df_ = pd.read_csv("Output\\4WheelerLossCostCombinedFile.csv")
    # df = pd.read_csv("Output\\4WheelerUnClubbedLossCostFile.csv")
    # df_train, df_test = train_test_split(df, test_size=0.2, random_state=0)
    df_train, df_test = df_, df_
    model = joblib.load("Output\\TweedieLossCost.sav")
    model_ttl = joblib.load("Output\\Tweedie_ttl.sav")
    y_pred = model.predict(df_test)
    df_test["Pred_NL"] = y_pred
    df_test["Pred_Cost_NL"] = df_test["Pred_NL"] * df_test["Normalized_LIVES_EXPOSED"]
    y_pred = model_ttl.predict(df_test)
    df_test["Pred_ttl"] = y_pred
    df_test["Pred_Cost_ttl"] = df_test["Pred_ttl"] * df_test["sum_insured_in_hundreds"]
    df_test.to_csv("Output\\ModelGammaInputCombined.csv")


df = pd.read_csv("Output\\ModelGammaInputCombined.csv")
df["Pred_total"] = df["Pred_Cost_NL"] + df["Pred_Cost_ttl"]

model_g = joblib.load("Output\\GammaLossCost.sav")
y_pred_ = model_g.predict(df)
df["Pred_Gamma"] = y_pred_
df["Pred_Cost_Gamma"] = df["Pred_Gamma"] * df["Normalized_LIVES_EXPOSED"]

model_t = joblib.load("Output\\TweedieSingleModelLossCost.sav")
y_pred_ = model_t.predict(df)
df["Pred_Tweedie"] = y_pred_
df["Pred_Cost_Tweedie"] = df["Pred_Tweedie"] * df["Normalized_LIVES_EXPOSED"]

df.to_csv("Output\\FinalOutput.csv")
print(df["Pred_Cost_Gamma"].sum()/10000000)
print(df["Pred_total"].sum()/10000000)
print(df["Pred_Cost_Tweedie"].sum()/10000000)
print(df["Ultimate_PAID"].sum()/10000000)
