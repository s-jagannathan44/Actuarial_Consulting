import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from tensorflow import keras

df = pd.read_csv("cal_housing.csv")
target_column = ['Indicator']
predictors = list(set(list(df.columns)) - set(target_column))
df[predictors] = df[predictors] / df[predictors].max()

X = df[predictors].values
y = df[target_column].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=40)


# Define the model
model = Sequential([
    Dense(500, activation='relu', input_shape=(len(predictors),)),
    Dense(100, activation='relu'),
    Dense(50, activation='relu'),
    Dense(1, activation="sigmoid"),
])

# Compile the model


metrics = [
    keras.metrics.FalseNegatives(name="fn"),
    keras.metrics.FalsePositives(name="fp"),
    keras.metrics.TrueNegatives(name="tn"),
    keras.metrics.TruePositives(name="tp"),
]

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=metrics)

model.fit(X_train, y_train, epochs=30, verbose=0)
model.save("california")
reconstructed_model = keras.models.load_model("california")


scores2 = reconstructed_model.evaluate(X, y, verbose=2)
'''
pred_test = reconstructed_model.predict(X)
# print('Accuracy on test data: {}% \n Error on test data: {}'.format(scores2[1], 1 - scores2[1]))
np.savetxt("output.csv", pred_test, delimiter=",")
np.savetxt("y.csv", y, delimiter=",")
'''