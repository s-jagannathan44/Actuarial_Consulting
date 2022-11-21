from collections import Counter
import pandas as pd
from numpy import mean
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold
from xgboost import XGBClassifier

# generate dataset
X, y = make_classification(n_samples=100000, n_features=2, n_redundant=1, n_informative=1, n_clusters_per_class=1,
                           weights=[0.95], flip_y=0, random_state=7)
frame = pd.DataFrame(X)
frame["Response"] = y
frame.to_csv("Output\\frame.csv")
# count examples in each class
counter = Counter(y)
# estimate scale_pos_weight value
estimate = counter[0] / counter[1]
# print('Estimate: %.3f' % estimate)


# define model
model = XGBClassifier(scale_pos_weight=estimate)
# define evaluation procedure
cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
# evaluate model
scores = cross_val_score(model, X, y, scoring='f1', cv=cv, n_jobs=-1)
# summarize performance
print('f1: %.5f' % mean(scores))
