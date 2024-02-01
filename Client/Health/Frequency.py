import pandas as pd
from sklearn.model_selection import train_test_split
from statsmodels.genmod.families import Tweedie
import statsmodels.formula.api as smf

df = pd.read_csv("Policies.csv")
df["Loss_Cost"] = df["Claim"]
# df["LIVES_EXPOSED"] = df["LIVES_EXPOSED"].clip(lower=1)
# df["ccl"] = df["PAID_AMT"] / df["LIVES_EXPOSED"]
train, test = train_test_split(df, test_size=0.33, random_state=25)

# result = smf.glm(formula="ccl ~ Mem_Age_New + Mem_Gender_New + Renewal_Count_New",
#                  data=train, family=Tweedie(var_power=1.0)).fit()

result = smf.glm(formula="Loss_Cost ~ GenderMainDriver + MaritalMainDriver + Make + Use + PaymentMethod "
                         "+ PaymentFrequency + VehicleValue",
                 data=train, family=Tweedie(var_power=1.9), var_weights=train["Exposure"]).fit()


print("-----------Summary-----------")
print(result.summary2())

print("-----------predict-----------")
y_pred = result.predict(test)
test["Pred"] = y_pred
test.to_csv("text_out.csv")
