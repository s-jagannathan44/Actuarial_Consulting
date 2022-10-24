from sklearn.compose import ColumnTransformer
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
import pandas as pd
from numpy import array
from sklearn.preprocessing import OrdinalEncoder

ordinal_columns = ["Sex", "AccidentArea", "Fault", "VehicleCategory", "PoliceReportFiled", "WitnessPresent",
                   "AgentType", "BasePolicy"]


def get_transformer():
    ordinal_tuple = ("ordinal", OrdinalEncoder(), ordinal_columns)
    transformer_ = ColumnTransformer(
        [("passthrough_n", "passthrough", ["Age", "Deductible"]),
         ordinal_tuple], remainder='drop')
    return transformer_


df_ = pd.read_csv("Output\\fraud_oracle.csv")
transformer = get_transformer()

X = df_.drop('FraudFound_P', axis=1)
y = df_["FraudFound_P"]

X = transformer.fit_transform(X)

print("Feature data dimension: ", X.shape)

select = SelectKBest(score_func=chi2, k=6)
z = select.fit_transform(X, y)
print("After selecting best 5 features:", z.shape)

filtered_columns = select.get_support()
features = array(["Age", "Deductible", "Sex", "AccidentArea", "Fault", "VehicleCategory", "PoliceReportFiled",
                  "WitnessPresent", "AgentType", "BasePolicy"])

print("Selected best 5:")
print(features[filtered_columns])
# print(z)
