import pandas
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import plot_confusion_matrix


def over_sample(dataframe):
    # class count for 0 & 1
    class_count_0, class_count_1 = dataframe['Claim'].value_counts()
    class_0 = dataframe[dataframe['Claim'] == 0]
    class_1 = dataframe[dataframe['Claim'] == 1]
    # oversampling for class 1
    class_1_over = class_1.sample(class_count_0, replace=True)
    test_over = pd.concat([class_1_over, class_0], axis=0)
    print("total class of 1 and 0:", test_over['Claim'].value_counts())
    return test_over


#  Part 1 read study and transform the file
df = pd.read_csv("Output\\Input_3.csv")
df = over_sample(df)

print(df.dtypes)
for c in df.columns:
    print(df[c].name, df[c].unique())
X = df.drop('Claim', axis=1)
y = df["Claim"]
X['GenderMainDriver'] = X['GenderMainDriver'].apply(lambda x: 0 if x == 'Male' else 1)
X['VehFuel1'] = X['VehFuel1'].apply(lambda x: 0.5 if x == 'D' else -0.5)
# X = pd.get_dummies(X, columns=['MaritalMainDriver', 'DrivingRestriction'])
# X.to_csv("Output\\X_encoded.csv")


# Step2 Build a preliminary Classification tree

# default test size is test_size=0.25
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=40)

frame = pandas.DataFrame(X_train, columns=["GenderMainDriver", "VehFuel1"])
frame["Claim"] = y_train
frame.to_csv("Output\\train.csv")

frame = pandas.DataFrame(X_test, columns=["GenderMainDriver", 'VehFuel1'])
frame["Claim"] = y_test
frame.to_csv("Output\\test.csv")


# clf_dt = DecisionTreeClassifier(random_state=42, min_impurity_decrease=0.01, class_weight={0: 1, 1: 10})
# clf_dt = DecisionTreeClassifier(random_state=42,  min_impurity_decrease=0.001, max_depth=3)
clf_dt = DecisionTreeClassifier(random_state=42)
clf_dt = clf_dt.fit(X_train, y_train)

# We will plot the tree here
plt.figure(figsize=(15, 7.5))
plot_tree(clf_dt, filled=True, rounded=True, class_names=["No Claim", "Claim"], feature_names=X.columns)
plot_confusion_matrix(clf_dt, X_test, y_test, display_labels=["Does not Have Claim", "Has Claim"])
plt.show()
print(clf_dt.score(X_test, y_test))
