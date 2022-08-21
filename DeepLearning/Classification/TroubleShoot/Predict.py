import numpy
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import KBinsDiscretizer, OrdinalEncoder
from tensorflow import keras


#def my_loss(y_true, y_pred):
#    return y_pred


df = pd.read_csv("Input.csv")
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
numpy.savetxt("what.csv", X, delimiter=",")
reconstructed_model = keras.models.load_model("frequency.h5")
reconstructed_model.compile(optimizer='adam',
                            loss='binary_crossentropy')
                            # , metrics=my_loss)
print(np.sum(reconstructed_model.predict(X)))
