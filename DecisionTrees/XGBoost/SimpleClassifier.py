# Generate and plot a synthetic imbalanced classification dataset
from collections import Counter
from imblearn.over_sampling import ADASYN
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from matplotlib import pyplot as plt
from numpy import mean, sort
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import precision_recall_curve, precision_score, recall_score, \
    ConfusionMatrixDisplay, f1_score
from sklearn.model_selection import train_test_split, RepeatedStratifiedKFold, cross_val_score
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder
from xgboost import XGBClassifier, plot_importance

ordinal_columns = ["GenderMainDriver", "PaymentMethod"]
ohe_columns = ["MaritalMainDriver", "Make", "Use", "PaymentFrequency"]


def get_columns():
    global ord_col_size, ohe_col_size
    encoder = transformer.named_transformers_['onehot_categorical']
    columns = encoder.get_feature_names_out()
    ohe_col_size = columns.size
    encoder = transformer.named_transformers_['ordinal']
    ord_columns = encoder.get_feature_names_out()
    columns = np.append(columns, ord_columns)
    columns = np.append(columns, "VehicleValue")
    ord_col_size = ord_columns.size
    return columns


def data_analysis(df=None):
    for c in df.columns:
        csv_file_name = "Output\\Columns\\" + c.replace("/", "_") + ".csv"
        insight = df[c].value_counts()
        insight.to_csv(csv_file_name)
    df.describe(percentiles=[0.25, 0.5, 0.75, 0.85, 0.9, 0.98, 1]).to_csv("Output\\Columns\\desc.csv")


def select_features():
    threshold = sort(model.feature_importances_)
    for thresh in threshold:
        # select features using threshold
        selection = SelectFromModel(model, threshold=thresh, prefit=True)
        select_X_train = selection.transform(X_train)
        # train model
        selection_model = XGBClassifier(scale_pos_weight=Counter(y_train)[0] / Counter(y_train)[1])
        selection_model.fit(select_X_train, y_train)
        # eval model
        select_X_test = selection.transform(X_test)
        y_pred_ = selection_model.predict(select_X_test)
        predictions = [round(value, ndigits=2) for value in y_pred_]
        f1_ = f1_score(y_test, predictions)
        print("Thresh=%.3f, n=%d, F1 score: %.2f" % (thresh, select_X_train.shape[1], f1_))


def write_output():
    ordinal_array = X_test[:, 1:ord_col_size+1].toarray()
    passthrough = pd.DataFrame(X_test[:, :1].toarray(), columns=["VehicleValue"])
    one_hot = transformer.named_transformers_['onehot_categorical'].inverse_transform(X_test[:, ord_col_size+1:])
    ordinal = transformer.named_transformers_['ordinal'].inverse_transform(ordinal_array)
    one_frame = pd.DataFrame(one_hot, columns=ohe_columns)
    ordinal_frame = pd.DataFrame(ordinal, columns=ordinal_columns)

    # axis 0 is vertical and axis 1 is horizontal
    frame = pd.concat([passthrough, ordinal_frame], axis=1)
    frame = pd.concat([frame, one_frame], axis=1)
    frame["Actual"] = y_test.to_list()
    frame['Predicted'] = y_pred
    frame.to_csv("Output\\Output.csv")


def get_transformer():
    ordinal_tuple = ("ordinal", OrdinalEncoder(), ordinal_columns)
    ohe_tuple = ("onehot_categorical", OneHotEncoder(), ohe_columns)
    transformer_ = ColumnTransformer(
        [("passthrough_n", "passthrough", ["VehicleValue"]),
         ordinal_tuple, ohe_tuple], remainder='drop')
    return transformer_


ord_col_size = ohe_col_size = 0
df_ = pd.read_csv("Output\\WeightedPolicy.csv")
transformer = get_transformer()

X = df_.drop('Actual', axis=1)
y = df_["Actual"]

X = transformer.fit_transform(X)
sm = ADASYN(sampling_strategy="all")
# X, y = sm.fit_resample(X, y)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=25)
X_train, y_train = sm.fit_resample(X_train, y_train)

# define model
model = XGBClassifier(scale_pos_weight=Counter(y_train)[0] / Counter(y_train)[1])
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

precision, recall, thresholds = precision_recall_curve(y_test, y_pred)
plt.plot(recall, precision, linestyle='--')
plt.xlabel('Recall')
plt.ylabel('Precision')

# calculate precision-recall AUC

f1 = f1_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)

print("Model F1 : ", f1)
print('Precision on testing set:', precision)
print('Recall on testing set:', recall)

# plotting the confusion-matrix
ConfusionMatrixDisplay.from_predictions(y_test, y_pred)
# define evaluation procedure
cv = RepeatedStratifiedKFold(n_splits=3, n_repeats=5, random_state=1)

# evaluate model
scores = 0  # cross_val_score(model, X_test, y_test, scoring='f1', cv=cv, n_jobs=-1, verbose=True)
# summarize performance
print('Mean f1: %.5f' % mean(scores))
# plot_importance(model)
# select_features()
plt.show()
get_columns()
write_output()
