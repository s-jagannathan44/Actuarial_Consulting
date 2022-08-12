import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from tensorflow import keras
from sklearn import preprocessing

df = pd.read_csv("cal_housing.csv")
# ------------------ begin ----------------------------------
target_column = ['Indicator']
categorical_columns = ['Make', 'GenderMainOwner']

predictors = list(set(list(df.columns)) - set(target_column) - set(categorical_columns))
numerical_predictors = list()
for column in predictors:
    numerical_predictors.append(column)

min_max_scaler = preprocessing.MinMaxScaler()

df[predictors] = X_scale = min_max_scaler.fit_transform(df[predictors])

for column in categorical_columns:
    predictors.append(column)
# ------------------ end ----------------------------------

# ------------------ begin ----------------------------------
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
# ------------------ end ----------------------------------


X = df[predictors].values
y = df[target_column].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=40)
# ------------------ begin ----------------------------------
train_targets = np.array(y_test)
counts = np.bincount(train_targets[:, 0])
print(
    "Number of houses above median in test data: {} ({:.2f}% of total)".format(
        counts[1], 100 * float(counts[1]) / len(train_targets)
    )
)
# ------------------ end ----------------------------------


# Define the model
model = Sequential([
    Dense(500, activation='relu', input_shape=(len(predictors),)),
    Dense(100, activation='relu'),
    Dense(50, activation='relu'),
    Dense(1, activation="sigmoid"),
])

# Compile the model


metrics = [
    keras.metrics.FalseNegatives(name="fn"),
    keras.metrics.FalsePositives(name="fp"),
    keras.metrics.TrueNegatives(name="tn"),
    keras.metrics.TruePositives(name="tp"),
]

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=metrics)

model.fit(X_train, y_train, epochs=30, verbose=0)
y_pred = model.predict(X_test)
model.evaluate(X_test, y_test, verbose=2)

# ------------------begin--------------------------------

numeric_column_count = X_test.shape[1] - 2

my_numerical_input = X_test[:, 0:numeric_column_count]

my_numerical_input = min_max_scaler.inverse_transform(my_numerical_input)

numerical_df = pd.DataFrame(my_numerical_input, columns=numerical_predictors)


invertGender = {v: k for k, v in GenderValues.items()}
invertMake = {v: k for k, v in MakeValues.items()}
my_input = X_test[:, numeric_column_count:numeric_column_count+2]

Make = my_input[:, 0]
Gender = my_input[:, 1]

df = pd.DataFrame({"Make": Make, "Gender": Gender})
df.Make = df.Make.map(invertMake)
df.Gender = df.Gender.map(invertGender)
df.to_csv("test1.csv")
numerical_df.to_csv("output.csv")
np.savetxt("y_test.csv", y_test, delimiter=",")
np.savetxt("y_pred.csv", y_pred, delimiter=",")
# ------------------end--------------------------------------
'''
scores2 = model.evaluate(X_test, y_test, verbose=2)
np.savetxt("X_test.csv", X_test, delimiter=",")
np.savetxt("y_test.csv", y_test, delimiter=",")
'''