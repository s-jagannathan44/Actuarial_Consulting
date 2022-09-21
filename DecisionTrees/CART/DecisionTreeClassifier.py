import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import plot_confusion_matrix

#  Part 1 read study and transform the file
df = pd.read_csv("Output\\Input_3.csv")
# print(df.describe(percentiles=[0.25, 0.5, 0.75, 0.966, 0.968]))
# print(df.corr())
print(df.dtypes)
for c in df.columns:
    print(df[c].name, df[c].unique())
X = df.drop('Claim', axis=1)
y = df["Claim"]
X_encoded = pd.get_dummies(X, columns=['MaritalMainDriver', 'DrivingRestriction'])
X_encoded['VehFuel1'] = X_encoded['VehFuel1'].apply(lambda x: 0.5 if x == 'D' else -0.5)
X_encoded['GenderMainDriver'] = X_encoded['GenderMainDriver'].apply(lambda x: 0 if x == 'Male' else 1)
X_encoded.to_csv("Output\\X_encoded.csv")

# Step2 Build a preliminary Classification tree

# default test size is test_size=0.25
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, random_state=40)

clf_dt = DecisionTreeClassifier(random_state=42)
clf_dt = clf_dt.fit(X_train, y_train)

# We will plot the tree here
plt.figure(figsize=(15, 7.5))
plot_tree(clf_dt, filled=True, rounded=True, class_names=["No Claim", "Claim"], feature_names=X_encoded.columns)
plot_confusion_matrix(clf_dt, X_test, y_test, display_labels=["Does not Have Claim", "Has Claim"])
plt.show()
path = clf_dt.cost_complexity_pruning_path(X_train, y_train)  # determine values for alpha
ccp_alphas = path.ccp_alphas  # extract different values of alpha
ccp_alphas = ccp_alphas[:-1]  # exclude maximum value for alpha

clf_dts = []  # create an array to put decision trees into

# now create one decision tree per value of alpha and store it in the array
# ccp = cost complexity pruning
for ccp_alpha in ccp_alphas:
    clf_dt = DecisionTreeClassifier(random_state=0, ccp_alpha=ccp_alpha)
    clf_dt.fit(X_train, y_train)
    clf_dts.append(clf_dt)

train_scores = [clf_dt.score(X_train, y_train) for clf_dt in clf_dts]
test_scores = [clf_dt.score(X_test, y_test) for clf_dt in clf_dts]

fig, ax = plt.subplots()
ax.set_xlabel("alpha")
ax.set_ylabel("accuracy")
ax.set_title("Accuracy vs alpha for training and test sets")
ax.plot(ccp_alphas, train_scores, marker='o', label='train', drawstyle="steps-post")
ax.plot(ccp_alphas, test_scores, marker='*', label='test', drawstyle="steps-post")
ax.legend()
plt.show()

clf_dt = DecisionTreeClassifier(random_state=42, ccp_alpha=0)
scores = cross_val_score(clf_dt, X_train, y_train, cv=10)
df = pd.DataFrame(data={'tree': range(10), 'accuracy': scores})
df.plot(x='tree', y='accuracy', marker='o', linestyle='--')
plt.show()

# create an array to store the results of each fold during cross validation
alpha_loop_values = []

for ccp_alpha in ccp_alphas:
    clf_dt = DecisionTreeClassifier(random_state=0, ccp_alpha=ccp_alpha)
    scores = cross_val_score(clf_dt, X_train, y_train, cv=10)
    alpha_loop_values.append([ccp_alpha, np.mean(scores), np.std(scores)])

# now we can draw a graph of the means and standard deviations of the scores for each candidate value of alpha
alpha_results = pd.DataFrame(alpha_loop_values, columns=['alpha', "mean_accuracy", 'std'])
alpha_results.plot(x='alpha', y='mean_accuracy', yerr='std', marker='o', linestyle='--')
plt.show()

# ideal_alpha  = alpha_results[(alpha_results['alpha']>0.014) & (alpha_results['alpha']<0.015)]
