import pandas as pd
from scikeras.wrappers import KerasClassifier
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split, GridSearchCV
from keras.models import Sequential
from keras.layers import Dense
from sklearn.metrics import make_scorer
from sklearn.preprocessing import KBinsDiscretizer, OrdinalEncoder


def my_custom_loss_func(y_true, y_pred):
    actual = y_true.sum()
    predicted = y_pred.sum()
    diff = predicted - actual
    return float(diff / actual) * 100


score = make_scorer(my_custom_loss_func, greater_is_better=False)


def create_model():
    # Define the model
    model = Sequential([
        Dense(500, activation='relu', input_shape=(7,)),
        Dense(100, activation='relu'),
        Dense(50, activation='relu'),
        Dense(1, activation="sigmoid"),
    ])

    model.compile(optimizer='adam',
                  loss='binary_crossentropy')
    return model


df = pd.read_csv("Base_File.csv")
X = df.iloc[:, :39]
y = df.iloc[:, 39:]

transformer = ColumnTransformer(
    [
        ("binned_numeric", KBinsDiscretizer(n_bins=10, encode='ordinal', strategy='quantile'), ["VehicleValue"]),
        (
            "onehot_categorical",
            OrdinalEncoder(),
            ["GenderMainDriver", "MaritalMainDriver", "Make", "Use", "PaymentMethod", "PaymentFrequency"],
        ),
    ],
    remainder='drop'
)
X = transformer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=40)
estimator = KerasClassifier(model=create_model, verbose=0)

# defining parameter range
param_grid = {
    'epochs': [60, 120, 150, 200],
    'batch_size': [200, 100],
}
# print(X_train[0:1].values)
# print(y_train[0:1].values)
var = 1
if var:
    grid = GridSearchCV(estimator, param_grid, refit=True, scoring=score,  verbose=3, n_jobs=-1)

    # fitting the model for grid search
    grid.fit(X_train, y_train)

    # print best parameter after tuning
    print(grid.best_params_)
    grid_predictions = grid.predict(X_test)

    print(grid_predictions.sum())

# print(insurance_model.evaluate(X_test, y_test, verbose=2))
# y_pred = insurance_model.predict(X_test)
# print(sum(y_pred))
'''
A = df["Freq_Act"].values
print(A[7:18])
print(y[7:18])
'''
