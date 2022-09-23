import numpy
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


def plot_feature_importance():
    importance = dt.feature_importances_
    print(importance)
    encoder = transformer.named_transformers_['onehot_categorical']
    columns = encoder.get_feature_names_out()
    encoder = transformer.named_transformers_['ordinal']
    ord_columns = encoder.get_feature_names_out()
    columns = numpy.append(columns, ord_columns)
    combo = pd.Series(importance, columns)
    figure(figsize=(16, 4))
    combo.sort_values().plot.barh(color='red')
    plt.title('Visualization of decision tree model feature importance')
    plt.show()


def write_output():
    one_hot = transformer.named_transformers_['onehot_categorical'].inverse_transform(X_test[:, :4])
    ordinal = transformer.named_transformers_['ordinal'].inverse_transform(X_test[:, 4:])
    one_frame = pd.DataFrame(one_hot, columns=["MaritalMainDriver"])
    ordinal_frame = pd.DataFrame(ordinal, columns=["GenderMainDriver"])

    # axis 0 is vertical and axis 1 is horizontal
    output = pd.concat([one_frame, ordinal_frame], axis=1)

    frame = pd.DataFrame(output.copy(), columns=df.columns)
    frame["Claim"] = y_test.to_list()
    frame['Predicted'] = y_pred_dt
    frame.to_csv("Output\\Output.csv")


#  Part 1 read study and transform the file
df = pd.read_csv("Output\\Sev_1.csv")

for c in df.columns:
    print(df[c].name, df[c].unique())
X = df.drop('Claim', axis=1)

y = df["Claim"]
print(X["GenderMainDriver"].value_counts())

transformer = ColumnTransformer(
    [("onehot_categorical", OneHotEncoder(), ["MaritalMainDriver"],),
     ("ordinal", OrdinalEncoder(), ["GenderMainDriver"],),
     ],
    remainder='drop'
)

X = transformer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=40)

dt = DecisionTreeRegressor(random_state=42)
dt.fit(X_train, y_train)
y_pred_dt = dt.predict(X_test)
print('r2 score', dt.score(X_test, y_test))
print('predicted mean', y_pred_dt.mean())

# get the mean baseline because this is a regression problem
# with regression, the baseline can be as simple as the mean.

mean_baseline = y_test.mean()

y_pred_base = [mean_baseline] * len(y_test)
mae_base = mean_absolute_error(y_test, y_pred_base)
mae_model = mean_absolute_error(y_test, y_pred_dt)
r2_base = r2_score(y_test, y_pred_base)

print(f'Mean Baseline: {mean_baseline:.1f} ')
print(f'Baseline mean absolute error: {mae_base}')
print(f'Model mean absolute error: {mae_model}')
print(f'r2 score: {r2_base}')

"""
Why R2 of 0?

From SKLEARN

"A constant model that always predicts the expected value of y, 
disregarding the input features, would get a R^2 score of 0.0."

"""
# plot_feature_importance()
write_output()
# Try out Permutation Importance
