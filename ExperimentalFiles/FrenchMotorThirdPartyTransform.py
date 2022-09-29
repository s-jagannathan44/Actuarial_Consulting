from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder, MinMaxScaler
import pandas as pd


freq = pd.read_csv('Output\\FMTPL2freq.csv')
freq = freq.drop(['IDpol', 'VehBrand', 'Region'], axis=1)

categorical = list(freq.select_dtypes('object').columns)
numerical = list(freq.select_dtypes('int').columns)

print(freq.dtypes)
print(f"Categorical columns are: {categorical}")


columns = ["Area", "ClaimNb", "Exposure", "VehPower", "VehAge", "DrivAge", "BonusMalus",
           "VehGas", "Density"]

freq['VehGas'] = freq['VehGas'].apply(lambda x: 0.5 if x == "'Regular'" else -0.5)
area_pipe = Pipeline([
    ('encoder', OrdinalEncoder()),
    ('Scaler', MinMaxScaler())
])

preprocessor = ColumnTransformer(
    [("area", area_pipe, ["Area"])], remainder='passthrough')

ct = ColumnTransformer(
    [("Scaler", MinMaxScaler(), ["VehPower", "VehAge", "DrivAge", "BonusMalus", "Density"]), ],
    remainder='passthrough'
)
preprocessor.fit(freq)
area_transform = pd.DataFrame(preprocessor.transform(freq), columns=columns)
ct.fit(area_transform)

temp = ct.transform(area_transform)
full_columns = ["VehPower", "VehAge", "DrivAge", "BonusMalus", "Density", "Area", "ClaimNb", "Exposure",
                "VehGas"]
final_transform = pd.DataFrame(temp, columns=full_columns)
final_transform.to_csv("Output\\final.csv")
