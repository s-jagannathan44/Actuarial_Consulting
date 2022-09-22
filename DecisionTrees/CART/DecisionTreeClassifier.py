import pandas
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split

#  Part 1 read study and transform the file
df = pd.read_csv("Output\\Input_3.csv")

for c in df.columns:
    print(df[c].name, df[c].unique())
X = df.drop('Claim', axis=1)
columns = X.columns
y = df["Claim"]
transformer = ColumnTransformer(
    [
        (
            "onehot_categorical",
            OneHotEncoder(),
            ["MaritalMainDriver",  "DrivingRestriction"],
        ),
(
            "ordinal",
            OrdinalEncoder(),
            ["GenderMainDriver",  "VehFuel1"],
        ),
    ],
    remainder='drop'
)

X = transformer.fit_transform(X)

# Step2 Build a preliminary Classification tree

# default test size is test_size=0.25
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=40)

# we can add min_impurity_decrease, class_weight and max_depth parameters here
clf_dt = DecisionTreeClassifier(random_state=42)
clf_dt = clf_dt.fit(X_train, y_train)

# We will plot the tree here
plt.figure(figsize=(15, 7.5))
plot_tree(clf_dt, filled=True, rounded=True, class_names=["No Claim", "Claim"])
plt.show()

y_pred = clf_dt.predict_proba(X_test)

one_hot = transformer.named_transformers_['onehot_categorical'].inverse_transform(X_test[:, :9])
ordinal = transformer.named_transformers_['ordinal'].inverse_transform(X_test[:, 9:])
one_frame = pandas.DataFrame(one_hot, columns=["MaritalMainDriver",  "DrivingRestriction"])
ordinal_frame = pandas.DataFrame(ordinal, columns=["GenderMainDriver",  "VehFuel1"])

# axis 0 is vertical and axis 1 is horizontal
output = pd.concat([one_frame, ordinal_frame], axis=1)

frame = pandas.DataFrame(output.copy(), columns=columns)
frame["Claim"] = y_test.to_list()
frame['Predicted'] = y_pred[:, 1:]
frame.to_csv("Output\\Output.csv")
