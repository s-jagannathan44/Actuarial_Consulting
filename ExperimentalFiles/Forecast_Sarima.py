import pandas as pd
import statsmodels.api as sm


def group_age(x):
    if x == 'FY18':
        return "01-01-2018"
    elif x == 'FY19':
        return "01-01-2019"
    elif x == 'FY20':
        return "01-01-2020"
    elif x == 'FY21':
        return "01-01-2021"
    elif x == 'FY22':
        return "01-01-2022"
    elif x == 'FY23':
        return "01-01-2023"


df = pd.read_csv("forecast.csv", usecols=['Financial_Year', 'Frequency'])
df["Financial_Year"] = df["Financial_Year"].apply(lambda x: group_age(x))
df["Financial_Year"] = pd.to_datetime(df["Financial_Year"], format="mixed", dayfirst=True)
# linear_model_preprocessor = ColumnTransformer(

df.set_index('Financial_Year', inplace=True)
mod = sm.tsa.statespace.SARIMAX(df,
                                order=(1, 1, 1),
                                seasonal_order=(1, 1, 1, 12),
                                enforce_stationarity=False,
                                enforce_invertibility=False)

results = mod.fit()

pred = results.get_prediction(start=pd.to_datetime('01-01-2023'), dynamic=False)

# Get forecast 500 steps ahead in future
pred_uc = results.get_forecast(steps=3)
print(pred_uc.predicted_mean)
