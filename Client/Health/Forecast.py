import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats


# from sklearn.model_selection import train_test_split
#
# df = pd.read_csv("Output\\clubbed_file_AgeModified.csv")
# df_train, df_test = train_test_split(df, test_size=0.2, random_state=0)
# df_test.to_csv("Output\\TwentyPercent_AgeModified.csv")

def scatter_plot(dataframe):
    plt.scatter(dataframe["Loss_Cost"], dataframe["Pred"])
    plt.xlabel('Actual Loss Cost')
    plt.ylabel('Predicted Loss Cost')
    plt.title('Actual vs Predicted Loss Cost')
    plt.show()


def residual_plot(dataframe, y_pred):
    # dataframe = dataframe[dataframe["Pred"] >= 1]
    # sns.residplot(data=dataframe, x="Pred", y="Loss_Cost")
    sns.residplot(x=y_pred, y=dataframe["Loss_Cost"])
    plt.xlabel("Pred")
    plt.title('Residual plot')
    plt.show()


def QQ_Plot(dataframe, y_pred):
    residuals = dataframe["Loss_Cost"] - y_pred.reshape(-1)
    plt.figure(figsize=(7, 7))
    stats.probplot(residuals, dist="norm", plot=plt)
    plt.title("Normal Q-Q Plot")
    plt.show()


def execute_model(tweedie_model, dataframe):
    y_pred = tweedie_model.predict(dataframe)
    dataframe["Pred"] = y_pred
    # residuals = dataframe["Loss_Cost"] - y_pred.reshape(-1)
    # model_norm_residuals_abs_sqrt = np.sqrt(np.abs(residuals))
    #
    # plt.figure(figsize=(7, 7))
    # sns.regplot(data=dataframe, x="Pred", y=model_norm_residuals_abs_sqrt)
    # plt.ylabel("Standarized residuals")
    # plt.xlabel("Fitted value")
    QQ_Plot(dataframe, y_pred)

    # dataframe["Pred_Cost"] = dataframe["Pred"] * dataframe["LIVES_EXPOSED"]
    # dataframe.to_csv("Output\\24_ExposureModified")


FY_dict = {"FY18": 0, "FY19": 1, "FY20": 2, "FY22": 4, "FY23": 5}
df = pd.read_csv("Output\\TwentyPercent_AgeModified.csv")
for col in df.columns:
    if "Unnamed" in col:
        df.drop(col, axis=1, inplace=True)
df["Mem_Age_New"].fillna("Others", inplace=True)
df["Renewal_Count_New"].fillna("Above 9", inplace=True)
df = df[df["LIVES_EXPOSED"] >= 1]
df["Loss_Cost"] = df["PAID_AMT"] / df["LIVES_EXPOSED"]
# df["Financial_Year"] = 6
glm = joblib.load("Tweedie.sav")
execute_model(glm, df)

# df = pd.read_csv("Output\\27Feb_AgeModified.csv")
# df = df[df["LIVES_EXPOSED"] >= 1]
# df = df[df["PAID_AMT"] > 0]
# df["Loss_Cost"] = df["PAID_AMT"] / df["LIVES_EXPOSED"]
# scatter_plot(df)
# residual_plot(df)
# plt.show()

# Divides into deciles
# df = df.sort_values("Pred", ascending=True)
# # df['cum_exposure'] = 100*(df["LIVES_EXPOSED"].cumsum() / df["LIVES_EXPOSED"].sum())
# # df['cum_loss'] = 100*(df["Loss_Cost"].cumsum() / df["Loss_Cost"].sum())
#
# df["decile"] = pd.qcut(df["Pred"], q=10, labels=list(range(10, 0, -1)))
# df['decile'].value_counts().plot(kind='line')
# plt.show()
#
# # Plots the deciles
# sns.countplot(x="decile", data=df, order=range(1, 11), palette='Blues_r')
# # plt.show()
