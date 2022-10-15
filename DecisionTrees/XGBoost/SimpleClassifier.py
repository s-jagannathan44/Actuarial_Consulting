# Generate and plot a synthetic imbalanced classification dataset
from collections import Counter

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from matplotlib import pyplot, pyplot as plt
from numpy import where
from sklearn.metrics import precision_recall_curve, accuracy_score, precision_score, recall_score, \
     ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder
from xgboost import XGBClassifier

ordinal_columns = ["GenderMainDriver"]
ohe_columns = ["MaritalMainDriver", "Make", "Use", "PaymentMethod", "PaymentFrequency"]


def make_plot_classification():
    # summarize class distribution
    counter = Counter(y)
    print(counter)
    # scatter plot of examples by class label
    for label, _ in counter.items():
        row_ix = where(y == label)[0]
        pyplot.scatter(X[row_ix, 0], X[row_ix, 1], label=str(label))
    pyplot.legend()
    pyplot.show()


def get_transformer():
    ordinal_tuple = ("ordinal", OrdinalEncoder(), ordinal_columns)
    transformer_ = ColumnTransformer(
        [("passthrough_numeric", "passthrough", ["Exposure"]), ordinal_tuple,
         ("onehot_categorical", OneHotEncoder(sparse=False), ohe_columns)],
        remainder='drop')
    return transformer_


# define dataset Mean ROC AUC: 0.53475
# X, y = make_classification(n_samples=100000, n_features=7, n_redundant=0,
#                           n_clusters_per_class=2, weights=[0.99], flip_y=0, random_state=7)

df = pd.read_csv("Output\\creditcard.csv")

transformer = get_transformer()

X = df.drop('Class', axis=1)
y = df["Class"]
# X = transformer.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=25)
# define model
model = XGBClassifier(scale_pos_weight=Counter(y_train)[0]/Counter(y_train)[1])
model.fit(X_train, y_train)
predictions = model.predict(X_test)
np.savetxt("Output\\output.csv", predictions, delimiter=",")
np.savetxt("Output\\y_test.csv", y_test, delimiter=",")
precision, recall, thresholds = precision_recall_curve(y_test, predictions)
plt.plot(recall, precision, linestyle='--')
plt.xlabel('Recall')
plt.ylabel('Precision')

# calculate precision-recall AUC

accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions)
recall = recall_score(y_test, predictions)

print("Model Accuracy : ", accuracy)
print('Precision on testing set:', precision)
print('Recall on testing set:', recall)

# plotting the confusion-matrix
ConfusionMatrixDisplay.from_predictions(y_test, predictions)
plt.show()
# define evaluation procedure
# cv = RepeatedStratifiedKFold(n_splits=3, n_repeats=1, random_state=1)

# evaluate model
# scores = cross_val_score(model, X, y, scoring='roc_auc', cv=cv, n_jobs=-1, verbose=True)
# summarize performance
# print('Mean ROC AUC: %.5f' % mean(scores))
