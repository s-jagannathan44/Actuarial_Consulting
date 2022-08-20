import pandas as pd

df = pd.read_csv("cal_housing.csv")
target_column = ['Indicator']
categorical_columns = ['Make', 'GenderMainOwner']

predictors = list(set(list(df.columns)) - set(target_column) - set(categorical_columns))
df[predictors] = df[predictors] / df[predictors].max()

# begin
Make = df.Make.unique()
MakeValues = {}
counter = 0
for m in Make:
    item = [(m, counter)]
    MakeValues.update(item)
    counter = counter + 1

Gender = df.GenderMainOwner.unique()
GenderValues = {}
counter = 0
for g in Gender:
    item = [(g, counter)]
    GenderValues.update(item)
    counter = counter + 1

df.Make = df.Make.map(MakeValues)
df.GenderMainOwner = df.GenderMainOwner.map(GenderValues)

print(df.head(5))

invertGender = {v: k for k, v in GenderValues.items()}
invertMake = {v: k for k, v in MakeValues.items()}

df.Make = df.Make.map(invertMake)
df.GenderMainOwner = df.GenderMainOwner.map(invertGender)
print(df.head(5))
# end

# print(df.head(7))

