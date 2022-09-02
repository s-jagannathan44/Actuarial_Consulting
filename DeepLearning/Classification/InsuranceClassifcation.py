import math
from copy import deepcopy

from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, MinMaxScaler
from sklearn.model_selection import GroupShuffleSplit
import pandas as pd

# Step 1 read File
freq = pd.read_csv('Output\\FMTPL2freq.csv')
print(freq.describe())
print(freq.corr())

# Step 2 Add group id by clubbing rows which belong to the same policy as one group.
# This is done by finding all rows which have same values for below columns
# Area	VehPower	VehAge	Driver Age	BonusMalus	VehBrand	VehGas	Density	Region
# This is achieved by dropping all columns other than above , finding duplicate rows
# and then and assigning them the same group id
# Once the group Ids have been found the new dataframe is merged back into the old data frame using
# a left outer join and the missing group ids are filled in

df_freq = freq.iloc[freq.drop(['IDpol', 'Exposure', 'ClaimNb', 'Claim_YN'], axis=1).drop_duplicates().index]
df_freq = df_freq.reset_index(drop=True)
df_freq['GroupID'] = df_freq.index + 1
df_freq = pd.merge(freq, df_freq, how='left')
df_freq['GroupID'] = df_freq['GroupID'].fillna(method='ffill')
print(df_freq['GroupID'].max())

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
df_freq['VehGas'] = df_freq['VehGas'].apply(lambda x: 0.5 if x == "'Regular'" else -0.5)

# Step 4 Normalize the data.
# we use One hot  encoding for the feature components VehBrand and Region
# We use the MinMaxScaler for Area (after transforming {A,...,F} ↦ {1,...,6})
# VehPower , VehAge , DrivAge , BonusMalus, Density
# VehGas we transform to ±1/2 and the volume Exposure (0,1) we keep untransformed


# Step 5 create  a copy and split  using GroupShuffleSplit instead of train_test_split
df_freq_ml = deepcopy(df_freq)
splitter = GroupShuffleSplit(test_size=0.2, n_splits=2, random_state=999)
split = splitter.split(df_freq_ml, groups=df_freq_ml['GroupID'])
train_ind, test_ind = next(split)
train = df_freq_ml.iloc[train_ind]
test = df_freq_ml.iloc[test_ind]

# Step 6 Check if the proportion of train set to test set is indeed 80:20
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
