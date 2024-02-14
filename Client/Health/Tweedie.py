import pandas as pd
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split, GridSearchCV
from xgboost import XGBRegressor

passthrough_list = ["LIVES_EXPOSED"]
ordinal_list = ["Mem_Age_New", "Mem_Gender_New", "Revised_Product_Name_New", "Financial_Year", "Renewal_Count_New",
                "Zone_New", "Sum_Insured_New"]


def return_best_model(estimator):
    # get the mean baseline because this is a regression problem
    # with regression, the baseline can be as simple as the mean.
    mean_baseline = y_test.mean()
    y_pred_base = [mean_baseline] * len(y_test)

    mae_base = mean_absolute_error(y_test, y_pred_base)
    print(f'Mean Baseline: {mean_baseline:.1f} ')
    print(f'Baseline mean absolute error: {mae_base}')
    # print(f'r2 score: {r2_base}')
    # defining parameter range
    param_grid = {
        'n_estimators': [1000, 3000],
        'colsample_bytree': [0.6, 0.7, 0.8, 0.9, 1]
    }
    param_dict = {'eval_set': [(X_val, y_val)], 'verbose': True, 'sample_weight': X_train["LIVES_EXPOSED"]}
    xgb_reg = GridSearchCV(estimator, param_grid, error_score="raise",
                           cv=10, refit=True, verbose=3, n_jobs=-1)
    xgb_reg.fit(X_train, y_train, **param_dict)
    # print best parameter after tuning
    print(xgb_reg.best_params_, xgb_reg.best_score_)
    return xgb_reg.best_estimator_


def multiplier(year):
    if year == "FY23":
        return 1.07
    elif year == "FY22":
        return 1.016
    else:
        return 1.0


def make_multi(dataframe, columns):
    df2 = pd.pivot_table(dataframe, values="PAID_AMT Pred_Cost LIVES_EXPOSED".split(), columns=columns,
                         aggfunc="sum").T
    df2["Actual"] = df2["PAID_AMT"] / df2["LIVES_EXPOSED"]
    df2["Predicted"] = df2["Pred_Cost"] / df2["LIVES_EXPOSED"]
    df2["Error"] = (df2["Actual"] - df2["Predicted"]) / df2["Actual"]
    df2['%ageError'] = df2['Error'].map('{:.2%}'.format)
    df2["Error"] = df2["Error"].abs()
    below_ten = df2[df2["Error"] <= 0.1]["LIVES_EXPOSED"].sum()
    total = df2["LIVES_EXPOSED"].sum()
    print('{:.2%}'.format(below_ten / total))
    df2.to_csv("Output\\multi.csv")


def execute_model(tweedie_model, test_set, dataframe):
    y_pred = tweedie_model.predict(test_set)
    dataframe["Pred"] = y_pred
    dataframe["Pred_Cost"] = dataframe["Pred"] * dataframe["LIVES_EXPOSED"]
    dataframe.to_csv("Output\\text_out.csv")
    make_multi(dataframe, "Mem_Age_New Mem_Gender_New Revised_Product_Name_New Renewal_Count_New  Financial_Year "
                          "Zone_New Sum_Insured_New".split())


# -------------------- CODE STARTS HERE ---------------------------------------
df = pd.read_csv("FrequencyModelFile.csv", usecols="Mem_Age_New Mem_Gender_New LIVES_EXPOSED "
                                                   "PAID_AMT Financial_Year Renewal_Count_New Zone_New "
                                                   "Revised_Product_Name_New Sum_Insured_New "
                 .split())

for col in df.columns:
    if "Unnamed" in col:
        df.drop(col, axis=1, inplace=True)

df = df[df["LIVES_EXPOSED"] >= 1]
df = df[~ df["Revised_Product_Name_New"].isin("SURPLUS-FLOATERFLOATER SURPLUS-FLOATERMED-PLT-046 "
                                              "SURPLUS-INDINDIVIDUAL Corona Kavach PolicyFLOATER "
                                              "Corona Kavach PolicyINDIVIDUAL"
                                              " Star Hospital Cash Insurance PolicyFLOATER ".split())]
df = df[df["Financial_Year"].isin("FY18 FY19 FY20 FY22 FY23".split())]
df["PAID_AMT"] = df["PAID_AMT"] * df["Financial_Year"].apply(lambda x: multiplier(x))
df["Loss_Cost"] = df["PAID_AMT"] / df["LIVES_EXPOSED"]
df["Loss_Cost"].fillna(0, inplace=True)
df["Mem_Age_New"].fillna("0.0", inplace=True)
for col in ordinal_list:
    df[col] = df[col].astype('category')

df_train, df_test_val, y_train, y_test_val = train_test_split(df, df["Loss_Cost"], test_size=0.30, random_state=40)
df_test, df_val, y_test, y_val = train_test_split(df_test_val, y_test_val, test_size=0.33, random_state=40)
X_train = df_train.drop(["PAID_AMT", "Loss_Cost"], axis=1)
X_test = df_test.drop(["PAID_AMT", "Loss_Cost"], axis=1)
X_val = df_val.drop(["PAID_AMT", "Loss_Cost"], axis=1)
# df.head(1).to_csv("test.csv")
# rgr = XGBRegressor(objective='reg:tweedie', seed=42, eval_metric='tweedie-nloglik@1.2', n_estimators=100,
#                    max_depth=3, learning_rate=0.1, colsample_bytree=0.6, tweedie_variance_power=1.9)

rgr = XGBRegressor(objective='reg:tweedie', seed=42, eval_metric='tweedie-nloglik@1.7',
                   tweedie_variance_power=1.7, enable_categorical=True, max_cat_to_onehot=1)

params_dict = {'sample_weight': X_train["LIVES_EXPOSED"], 'verbose': True}
# rgr.fit(X_train, y_train, **params_dict)
rgr = return_best_model(rgr)
rgr.save_model('Output\\model.json')
execute_model(rgr, X_test, df_test)

# rgr = XGBRegressor()
# rgr.load_model('Output\\model.json')
# X_test = pd.read_csv("test.csv")
# for col in ordinal_list:
#     X_test[col] = X_test[col].astype('category')
