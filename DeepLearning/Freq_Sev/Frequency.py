import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from imblearn.over_sampling import RandomOverSampler
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
from keras import Sequential
from keras.layers import Dense, Dropout
from keras.callbacks import EarlyStopping
from sklearn.metrics import plot_confusion_matrix
from sklearn.svm import SVC
from keras.metrics import FalseNegatives, FalsePositives, TrueNegatives, TruePositives, Precision, Recall


df = pd.read_csv("Output\\freq_data.csv")
print(df.shape)
print(df.describe())
print(df.info())
print(df["Claim"].unique())

# Feature target split
X = df.drop("Claim", axis=1)
y = df["Claim"]

print(X.shape)
print(y.shape)

# Label encoding on target column
le = LabelEncoder()
y = le.fit_transform(y)
# Split categorical and numerical data
df_num = X.select_dtypes(["int64", "float64"])
df_cat = X.select_dtypes("object")

# Standard Scaler:- A standard scaler converts a distribution, such that it has 0 mean and 1 standard deviation
for col in df_num:
    ss = StandardScaler()
    df_num[col] = ss.fit_transform(df_num[[col]])

# Categorical data plot
for col in df_cat:
    plt.figure()
    sns.countplot(data=df_cat, x=col)
    plt.xticks(rotation=90)
   # plt.show()


# encoding on categorical column
df_cat = pd.get_dummies(df_cat)
# Combine both categorical and numerical data for training
X = pd.concat([df_num, df_cat], axis=1)

# visualize the target variable
g = sns.countplot(df['Claim'])
# fix this NOW
# g.set_xticklabels([0, 1])
# plt.show()

# class count for 0 & 1
class_count_0, class_count_1 = df['Claim'].value_counts()

# Separate class
class_0 = df[df['Claim'] == 0]
class_1 = df[df['Claim'] == 1]

# print the shape of the class
print('class 0:', class_0.shape)
print('class 1:', class_1.shape)

# oversampling for class 1
class_1_over = class_1.sample(class_count_0, replace=True)

test_over = pd.concat([class_1_over, class_0], axis=0)

print("total class of 1 and 0:", test_over['Claim'].value_counts())

# plot the count after under-sampling
test_over['Claim'].value_counts().plot(kind='bar', title='Count (Claim)')

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

np.savetxt("Output\\X_train.csv", X_train, delimiter=",")
np.savetxt("Output\\y_train.csv", y_train, delimiter=",")
np.savetxt("Output\\X_test.csv", X_test, delimiter=",")
np.savetxt("Output\\y_test.csv", y_test, delimiter=",")

ros = RandomOverSampler(random_state=42)
# fit predictor and target variable
X_train_ros, y_train_ros = ros.fit_resample(X_train, y_train)
X_test_ros, y_test_ros = ros.fit_resample(X_test, y_test)

print('Original dataset shape', y_train.shape)
print('New dataset shape', y_train_ros.shape)

print("New feature shape", X_train_ros.shape)

X_test_ros.to_csv("Output\\Files\\X_test_ros.csv")
y_test_ros.to_csv("Output\\Files\\y_test_ros.csv")

'''
np.savetxt("Output\\X_train_ros.csv", X_train_ros, delimiter=",")
np.savetxt("Output\\y_train_ros.csv", y_train_ros, delimiter=",")
np.savetxt("Output\\y_test_ros.csv", y_test_ros, delimiter=",")
np.savetxt("Output\\X_test_ros.csv", X_test_ros, delimiter=",")
'''
model = Sequential()
# model.add(Dense(16, activation="relu", input_dim=154))
model.add(Dense(16, activation="relu", input_dim=48))
model.add(Dropout(0.5))
model.add(Dense(16, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(8, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(4, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(1, activation="sigmoid"))

metrics = [
    FalseNegatives(name="fn"),
    FalsePositives(name="fp"),
    TrueNegatives(name="tn"),
    TruePositives(name="tp"),
    Precision(name="precision"),
    Recall(name="recall"),
]

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=metrics)
early_stopping = EarlyStopping(monitor="loss", min_delta=0.01, patience=5)

model.fit(X_train_ros, y_train_ros, batch_size=2048, epochs=32)

y_pred = model.predict(X_test_ros)
np.savetxt("Output\\y_pred.csv", y_pred, delimiter=",")
y_pred = np.where(y_pred >= 0.5, 1, 0)
print(classification_report(y_test_ros, y_pred))

'''
clf = SVC(random_state=1)
clf.fit(X_train_ros, y_train_ros)
SVC(random_state=1)
plot_confusion_matrix(clf, X_test, y_test)
plt.show()
'''
