from geopy.distance import geodesic
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans as Km
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def tz_from_utc_ms_ts(utc_ms_ts):
    # convert from time stamp to datetime
    utc_datetime = dt.datetime.utcfromtimestamp(utc_ms_ts / 1000.)

    # set the timezone to UTC, and then convert to desired timezone
    return utc_datetime


def read_transform():
    df = pd.read_csv("Output\\telematics.csv")
    df = df[df["Creation_Time"] != ""]
    df["Creation_Time"] = df["Time Message Container Created"].apply(lambda x: tz_from_utc_ms_ts(x))
    df["Receipt_Time"] = df["Time Received"].apply(lambda x: tz_from_utc_ms_ts(x))
    distances = [-1]
    interval = [-1]
    for index in range(len(df)):
        if index < len(df) - 1:
            origin = (df["Latitude"].iloc[index], df["Longitude"].iloc[index])
            destin = (df["Latitude"].iloc[index + 1], df["Longitude"].iloc[index + 1])
            time_interval = df["Time Message Container Created"].iloc[index + 1] - \
                            df["Time Message Container Created"].iloc[index]
            interval.append(time_interval / 1000)
            distances.append(geodesic(origin, destin).meters)
    df["Distance"] = distances
    df["Interval"] = interval
    df.to_csv("Output\\interim.csv")


# -------------------- CODE STARTS HERE ---------------------------------------

df_ = pd.read_csv("Output\\HighwayTraffic.csv")
# df_ = df_[df_["deviceID"] != 14]
# train, test = train_test_split(df_, test_size=0.5, random_state=42)
# train.to_csv("train.csv")
# train.to_csv("test.csv")

# Standardize the data
X_std = StandardScaler().fit_transform(df_.drop(["timeStamp", "Interval"], axis=1))
# Run local implementation of kmeans
km = Km(n_clusters=4, max_iter=100)
km.fit(X_std)
centroids = km.cluster_centers_
df_["Cluster"] = km.labels_
df_.to_csv("Output\\clustered.csv")

# Plot the clustered data

# Run the Kmeans algorithm and get the index of data points clusters
sse = []
list_k = list(range(1, 10))

for k in list_k:
    km = Km(n_clusters=k)
    km.fit(X_std)
    sse.append(km.inertia_)

# Plot sse against k
plt.figure(figsize=(6, 6))
plt.plot(list_k, sse, '-o')
plt.xlabel(r'Number of clusters $k$')
plt.ylabel('Sum of squared distance')

plt.show()
