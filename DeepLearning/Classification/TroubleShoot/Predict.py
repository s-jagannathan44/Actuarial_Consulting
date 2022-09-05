from keras.metrics import Poisson
from keras.optimizers import SGD
from sklearn.model_selection import train_test_split
import numpy as np
from tensorflow import keras
import Modules.Utilities as Ut

X, y = Ut.fetch_data("Output\\normalised.csv", 6)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=40)
metrics = [Poisson(name="mean_absolute_percentage_error")]
'''
model = Ut.create_model(X.shape[1], X_train, y_train, metrics)

np.savetxt("Output\\X_train.csv", X_train, delimiter=",")
np.savetxt("Output\\y_train.csv", y_train, delimiter=",")
np.savetxt("Output\\X_test.csv", X_test, delimiter=",")
np.savetxt("Output\\y_test.csv", y_test, delimiter=",")
actual = np.sum(y_test)
'''
''''''
#X, y = Ut.fetch_data("Output\\X_test.csv", 7)
actual = np.sum(y)
my_model = keras.models.load_model("ModelFiles\\Policies.h5")
my_model.compile(optimizer=SGD(learning_rate=0.01, momentum=0.1), loss="poisson", metrics=metrics)
predicted = np.sum(Ut.load_predict(my_model, X))

error = 1 - (predicted / actual)
print("error", float(error) * 100)

# freq = pd.read_csv('Output\\Y_test.csv')
# print(freq.describe())

'''
X, y = Ut.fetch_data("FMTPL2.csv", 7)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=40)
metrics = [Poisson(name="poisson")]
model = Ut.create_model(X.shape[1], X_train, y_train, metrics)
'''

'''
np.savetxt("Output\\X_train.csv", X_train, delimiter=",")
np.savetxt("Output\\y_train.csv", y_train, delimiter=",")
np.savetxt("Output\\X_test.csv", X_test, delimiter=",")
np.savetxt("Output\\y_test.csv", y_test, delimiter=",")

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, MinMaxScaler
import pandas as pd
import numpy as np

freq = pd.read_csv('Output\\FMTPL2freq.csv')
freq = freq.drop('IDpol', axis=1)
categorical = list(freq.select_dtypes('object').columns)
numerical = list(freq.select_dtypes('int').columns)
print(freq.dtypes)
print(f"Categorical columns are: {categorical}")
categorical = ["VehBrand", "Region"]
residual = ["VehGas", "Area", "Exposure", ]

columns = ["Area", "ClaimNb", "Exposure", "VehPower", "VehAge", "DrivAge", "BonusMalus", "VehBrand",
           "VehGas", "Density", "Region"]

freq['VehGas'] = freq['VehGas'].apply(lambda x: 0.5 if x == "'Regular'" else -0.5)
area_pipe = Pipeline([
    ('encoder', OrdinalEncoder()),
    ('Scaler', MinMaxScaler())
])

preprocessor = ColumnTransformer(
    [("area", area_pipe, ["Area"])], remainder='passthrough')

ct = ColumnTransformer(
    # [("onehot_categorical", OneHotEncoder(), ["VehBrand", "Region"]),
    [("Scaler", MinMaxScaler(), ["VehPower", "VehAge", "DrivAge", "BonusMalus", "Density"]), ],
    remainder='passthrough'
)
preprocessor.fit(freq)
area_transform = pd.DataFrame(preprocessor.transform(freq), columns=columns)
ct.fit(area_transform)


cat_columns = ct.named_transformers_['onehot_categorical'].get_feature_names_out(categorical)
print(f"One hot  columns are: {cat_columns}")
columns = np.append(numerical, residual)
columns = np.append(columns, cat_columns)

temp = ct.transform(area_transform)
full_columns = ["VehPower", "VehAge", "DrivAge", "BonusMalus", "Density", "Area", "ClaimNb", "Exposure",
                "VehBrand", "VehGas", "Region"]
final_transform = pd.DataFrame(temp, columns=full_columns)
final_transform.to_csv("Output\\final.csv")
'''