import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import KBinsDiscretizer, OrdinalEncoder
from tensorflow import keras


def my_loss(y_true, y_pred):
    actual = float(y_true)
    predicted = float(y_pred)
    loss = actual - predicted
    return loss


var = 1
if var:
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

# numpy.savetxt("what.csv", X, delimiter=",")
reconstructed_model = keras.models.load_model("frequency.h5", custom_objects={"my_loss": my_loss})
reconstructed_model.compile(optimizer='adam',
                            loss='binary_crossentropy')
print(np.sum(reconstructed_model.predict(X)))
