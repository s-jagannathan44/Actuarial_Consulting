import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense

df = pd.read_csv("california_housing_train.csv")
dataset = df.values
# X is list of input features
X = dataset[:, 2:6]
# Y is label of what we want to predict
Y = dataset[:, 8]
Y = Y.reshape(-1, 1)
min_max_scaler = preprocessing.MinMaxScaler()
y_scaler = preprocessing.MinMaxScaler()
X_scale = min_max_scaler.fit_transform(X)
Y_scale = y_scaler.fit_transform(Y)
X_train, X_val_and_test, Y_train, Y_val_and_test = train_test_split(X_scale, Y_scale, test_size=0.3)
X_val, X_test, Y_val, Y_test = train_test_split(X_val_and_test, Y_val_and_test, test_size=0.5)
print(X_train.shape, X_val.shape, X_test.shape, Y_train.shape, Y_val.shape, Y_test.shape)

'''
https://machinelearningmastery.com/tensorflow-tutorial-deep-learning-with-tf-keras/

A model has a life cycle, and this very simple knowledge provides the backbone 
for both modeling a dataset and understanding the tf.keras API.
The five steps in the life cycle are as follows:

Define the model
Compile the model
Fit the model
Evaluate the model
Make predictions
'''

# Define the model
model = Sequential([
    Dense(32, activation='relu', input_shape=(4,)),
    Dense(32, activation='relu'),
    Dense(1),  # output layer with one node uses the default or linear activation function (no activation function).
])

# Compile the model
''' 
 https://www.tensorflow.org/api_docs/python/tf/keras/optimizers
 The three most common loss functions are:
‘binary_crossentropy‘ for binary classification
‘sparse_categorical_crossentropy‘ for multi-class classification
‘mse‘ (mean squared error) for regression
 https://www.tensorflow.org/api_docs/python/tf/keras/losses
 Metrics are defined as a list of strings for known metric functions 
 or a list of functions to call  to evaluate predictions.
 https://www.tensorflow.org/api_docs/python/tf/keras/metrics
'''

model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mean_squared_error'])

# Fit the Model

hist = model.fit(X_train, Y_train,
                 batch_size=32, epochs=100, verbose=2,
                 validation_data=(X_val, Y_val))
# Evaluate the model
# print accuracy as loss is stored in [0]
# print("history", hist)
print("evaluate", model.evaluate(X_test, Y_test, verbose=2))

# Make a prediction
y_pred = model.predict(X_test)
y_pred = y_scaler.inverse_transform(y_pred)
Y_test = y_scaler.inverse_transform(Y_test)
np.savetxt("output.csv", y_pred, delimiter=',')
np.savetxt("Y_test.csv", Y_test, delimiter=',')
np.savetxt("X_test.csv", X_test, delimiter=',')
