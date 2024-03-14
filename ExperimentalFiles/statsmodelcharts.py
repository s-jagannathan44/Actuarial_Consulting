import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import joblib
# from statsmodels.graphics.regressionplots import plot_ceres_residuals

df = pd.read_csv("WheelerTestFile.csv")
df["Loss_Cost"] = df["PAID_AMT"] / df["LIVES_EXPOSED"]
result2 = joblib.load("C:\\Users\\jvpra\\Python\\Client\\Bazaar\\Output\\4Wheeleer.sav")

# fig = sm.graphics.plot_fit(result2, result2.params.index[1], vlines=False)
# # fig = sm.graphics.plot_regress_exog(result2, result2.params.index[1])
# plot_ceres_residuals(result2, result2.params.index[1])
# sm.qqplot(result2, line="45")
# fig.tight_layout(pad=1.0)
# plt.show()


data = sm.datasets.statecrime.load_pandas().data
murder = data['murder']
X = data[['poverty', 'hs_grad']]
X["constant"] = 1
y = murder
model = sm.OLS(y, X)
results = model.fit()
data["MP"]= results.predict(X)
# data.to_csv("C:\\Users\\jvpra\\Python\\Client\\Bazaar\\Output\\Sep\\data.csv")
fig = sm.graphics.plot_regress_exog(results, 0)
plt.show()
