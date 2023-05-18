import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import MinMaxScaler

ActualOutlierCount = 18935
df = pd.read_csv('Output\\InputFile-PrivateCar.csv')
X_std = MinMaxScaler().fit_transform(df)
estimator_ = IsolationForest(n_estimators=500, random_state=7, n_jobs=-1, max_samples="auto", contamination=0.09,
                             max_features=3)
estimator_.fit(X_std)
y_pred = estimator_.predict(X_std)
df["Output"] = y_pred
df["score"] = df["NRA by Distance"]*0.4 + df["NHB by Distance"]*0.4 + df["A 120"]*.2
Outliers = df[df["Output"] == -1]

totalCount = len(Outliers.index)
#  print(Outliers[(Outliers["NRA by Distance"] == 0) & (Outliers["NHB by Distance"] == 0)].count())

countOfZero = len(Outliers[Outliers["score"] == 0].index)
countOfOutliers = len(Outliers[Outliers["score"] > 0.36].index)

recall = countOfOutliers / ActualOutlierCount
precision = countOfOutliers / totalCount
print(countOfZero)
print(round(recall, ndigits=2), round(precision, ndigits=2))
# df.to_csv("Output\\Output.csv")
