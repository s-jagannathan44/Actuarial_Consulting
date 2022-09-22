import pandas
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split

#  Part 1 read study and transform the file
df = pd.read_csv("Output\\Input_3.csv")

for c in df.columns:
    print(df[c].name, df[c].unique())
X = df.drop('Claim', axis=1)
y = df["Claim"]
X['GenderMainDriver'] = X['GenderMainDriver'].apply(lambda x: 0 if x == 'Male' else 1)
X['VehFuel1'] = X['VehFuel1'].apply(lambda x: 0.5 if x == 'D' else -0.5)
X = pd.get_dummies(X, columns=['MaritalMainDriver', 'DrivingRestriction'])



# Step2 Build a preliminary Classification tree

# default test size is test_size=0.25
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=40)

frame = pandas.DataFrame(X_test.copy(), columns=X.columns)
frame["Claim"] = y_test


# we can add min_impurity_decrease, class_weight and max_depth parameters here
clf_dt = DecisionTreeClassifier(random_state=42)
clf_dt = clf_dt.fit(X_train, y_train)

# We will plot the tree here
plt.figure(figsize=(15, 7.5))
plot_tree(clf_dt, filled=True, rounded=True, class_names=["No Claim", "Claim"], feature_names=X.columns)
plt.show()

threshold = 0.033
# y_pred = (clf_dt.predict_proba(X_test)[:, 1] >= threshold).astype(bool)  # set threshold as 0.3
y_pred = clf_dt.predict_proba(X_test)
Output_frame = frame.copy()
Output_frame['Predicted'] = y_pred[:, 1:]
Output_frame.to_csv("Output\\Output.csv")
