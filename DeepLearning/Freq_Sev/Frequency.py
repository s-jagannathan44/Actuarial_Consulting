import pandas as pd
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.optimizers import SGD
from sklearn.model_selection import train_test_split
from Modules import Utilities as Ut
from keras.models import Sequential
from keras.layers import Dense


# Make and Payment_frequency to go under One hot encoding
passthrough_list = ["AnalysisPeriod"]
ordinal_list = ["GenderMainDriver", "GenderYoungestDriver",
                "Use", "PaymentMethod", "BonusMalusProtection"]
to_bin_list = [['AgeMainDriver', 4, 'uniform'],
               ['VehicleAge', 2, 'uniform'],
               ['BonusMalusYears', 4, 'quantile'], ['PolicyTenure', 3, 'quantile']]


def get_columns():
    columns = {}
    for encoder in transformer.named_transformers_:
        if type(transformer.named_transformers_[encoder]) != str:
            item = [(encoder, transformer.named_transformers_[encoder].get_feature_names_out().size)]
            columns.update(item)
    return columns


def write_output(X_value, actual_val, pred_val):
    frame_list = []
    res = []
    length = 0
    index = 0
    for item in column_dict:
        encoder = transformer.named_transformers_[item]
        size = column_dict[item]
        length = length + size
        if length == size:
            col = encoder.inverse_transform(X_value[:, :length])
        else:
            col = encoder.inverse_transform(X_value[:, index:length])
        frame = pd.DataFrame(col, columns=encoder.get_feature_names_out())
        frame_list.append(frame)
        index = length

    for frame in frame_list:
        res.append(frame)

    # axis 0 is rows and axis 1 is columns
    frame = pd.concat(res, axis=1)
    frame["Actual"] = actual_val.to_list()
    frame['Predicted_Proba'] = pred_val
    frame.to_csv("Output\\Output.csv")


def data_analysis(df=None):
    for c in df.columns:
        csv_file_name = "Output\\Columns\\" + c.replace("/", "_") + ".csv"
        insight = df[c].value_counts()
        insight.to_csv(csv_file_name)
    df.describe(percentiles=[0.25, 0.5, 0.75, 0.85, 0.9, 0.98, 1]).to_csv("Output\\Columns\\desc.csv")


# -------------------- CODE STARTS HERE ---------------------------------------
ord_col_size = ohe_col_size = 0
df_ = pd.read_csv("Output\\Policies.csv")
df_ = df_[df_["Use"] != "Business Use - Class 1"]
df_ = df_[df_["PaymentMethod"] != "Other"]

X = df_.drop('Claim Count', axis=1)
y = df_["Claim Count"]
transformer = Ut.transform(passthrough_list, to_bin_list, ordinal_list)
X = transformer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=25)

# define model
estimator_ = Sequential([
        Dense(5, activation='relu', input_shape=(X_train.shape[1],)),
        Dense(10, activation='relu'),
        Dense(5, activation='relu'),
        Dense(1, activation="sigmoid"),
    ])
checkpoint = ModelCheckpoint(filepath="Output\\Checkpoint.h5", monitor="poisson", verbose=1,
                             save_best_only=True, mode="min")
early_stopping = EarlyStopping(monitor="poisson", min_delta=0.00001, patience=5)
estimator_.compile(optimizer=SGD(learning_rate=0.01, momentum=0.1), loss="poisson", metrics="poisson")
estimator_.fit(X, y, epochs=1000, batch_size=1000, callbacks=[checkpoint, early_stopping])

# estimator_ = gridsearch(estimator_)
y_pred = estimator_.predict(X_test)
column_dict = get_columns()
write_output(X_test, y_test, y_pred)
