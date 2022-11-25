import math
import numpy as np
from keras.optimizers import SGD
from tensorflow import keras
import Modules.Utilities as Ut
from sklearn.model_selection import GroupShuffleSplit
import pandas as pd
from keras.metrics import Poisson


def data_verification():
    # Step 6 Check if the proportion of train set to test set is indeed 80:20
    global train, test
    train = df_freq_ml.iloc[train_ind]
    test = df_freq_ml.iloc[test_ind]
    print("train %age ", len(train) / len(df_freq_ml))
    print("test %age ", len(test) / len(df_freq_ml))
    # Step 7 check if the average claims frequencies are similar between train set and test set.
    # They should be very similar, otherwise that means group shuffle has not been done appropriately.
    print("training Claim frequency", train['ClaimNb'].sum() / train['Exposure'].sum())
    print("test Claim frequency", test['ClaimNb'].sum() / test['Exposure'].sum())
    # Step 8 Check the sum of Exposure and count of ClaimNb in the train and test sets.
    print(train.groupby(by=['ClaimNb']).agg({'Exposure': ['sum'], 'ClaimNb': ['count']}))
    print('\n-------------------------\n')
    print(test.groupby(by=['ClaimNb']).agg({'Exposure': ['sum'], 'ClaimNb': ['count']}))


# Step 1 read File
df_freq = pd.read_csv('Output\\Grouped.csv')

'''
Step3 We will also simplify the data for our model. In particular, we will adjust the following columns:
VehAge: cap at 20 years
DrivAge: cap at 90 years old
BonusMalus: cap at 150, round to nearest integer
Density: apply log
Exposure: cap at 1 year
'''
df_freq['VehAge'] = df_freq['VehAge'].apply(lambda x: 20 if x > 20 else x)
df_freq['DrivAge'] = df_freq['DrivAge'].apply(lambda x: 90 if x > 90 else x)
df_freq['BonusMalus'] = df_freq['BonusMalus'].apply(lambda x: 150 if x > 150 else int(x))
df_freq['Density'] = df_freq['Density'].apply(lambda x: round(math.log(x), 2))
df_freq['Exposure'] = df_freq['Exposure'].apply(lambda x: 1. if x > 1 else x)
df_freq['Exposure'] = df_freq['Exposure'].apply(lambda x: 1. if x > 1 else x)
df_freq['ClaimNb'] = df_freq['ClaimNb'].apply(lambda x: 1. if x > 0 else x)
# Step 4 Normalize the data.
# we use One hot  encoding for the feature components VehBrand and Region
# We use the MinMaxScaler for Area (after transforming {A,...,F} ↦ {1,...,6})
# VehPower , VehAge , DrivAge , BonusMalus, Density
# VehGas we transform to ±1/2 and the volume Exposure 0-1 we keep untransformed

df_freq_ml = Ut.motor_third_party_transform(df_freq)
df_freq_ml["Target"] = df_freq_ml['ClaimNb']

# Step 5 create  a copy and split  using GroupShuffleSplit instead of train_test_split
# df_freq_ml = deepcopy(df_freq)
splitter = GroupShuffleSplit(test_size=0.2, n_splits=2, random_state=999)
split = splitter.split(df_freq_ml, groups=df_freq_ml['GroupID'])
train_ind, test_ind = next(split)
data_verification()

df_freq_ml = df_freq_ml.drop(['ClaimNb', 'Exposure', 'GroupID', 'Claim'], axis=1)
# df_freq_ml = df_freq_ml.drop(['BonusMalus', 'Density', 'Area'], axis=1)

train = df_freq_ml.iloc[train_ind]
test = df_freq_ml.iloc[test_ind]

# print(df_freq_ml.describe())
# df_freq_ml = df_freq_ml.drop(['ClaimNb', 'Exposure', 'GroupID', 'VehGas'], axis=1)
df_freq_ml.to_csv("Output\\normalised.csv")

X_train, y_train = Ut.fetch_xy(train, 7)
X_test, y_test = Ut.fetch_xy(test, 7)

metrics = [Poisson()]

model = Ut.create_model(X_train.shape[1], X_train, y_train, metrics)
my_model = keras.models.load_model("Output\\Checkpoint.h5")
my_model.compile(optimizer=SGD(learning_rate=0.01, momentum=0.1), loss="poisson", metrics=metrics)

Ut.load_predict(my_model, X_test)
np.savetxt("Output\\X_test.csv", X_test, delimiter=",")
np.savetxt("Output\\y_test.csv", y_test, delimiter=",")
