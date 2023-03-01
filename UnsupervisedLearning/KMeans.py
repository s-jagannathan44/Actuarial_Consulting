import pandas as pd
import matplotlib.pyplot as plt
from kneed import KneeLocator
from sklearn.cluster import KMeans as Km
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score


def cluster_data():
    # Run local implementation of k means
    km = Km(n_clusters=n_clusters, max_iter=100, init='k-means++')
    labels = km.fit_predict(X_std)
    print(silhouette_score(X_std, labels))
    print(davies_bouldin_score(X_std, labels))
    df["Cluster"] = km.labels_
    df.to_csv("Output\\clustered.csv")


def elbow_method():
    list_k = list(range(2, 10))
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
    return KneeLocator(range(2, 10), sse, curve="convex", direction="decreasing").elbow


def process_data():
    df["TripEndDateTIme"] = pd.to_datetime(df['TripEndDateTIme'])
    df["TripStartDateTIme"] = pd.to_datetime(df['TripStartDateTIme'])
    df["Duration"] = df["TripEndDateTIme"] - df["TripStartDateTIme"]
    for index in range(len(df)):
        dayOfWeek.append(pd.Timestamp(df["TripStartDateTIme"].iloc[index]).dayofweek)
        duration.append(pd.Timedelta(df["Duration"].iloc[index]).total_seconds() / 3600)

    df["Distance"] = df["OdometerEnd"] - df["OdometerStart"]
    df["DayOfWeek"] = dayOfWeek
    df["TripDuration"] = duration
    df.drop(df.columns.difference(columns), axis=1, inplace=True)

    # Standardize the data
    return MinMaxScaler().fit_transform(df)


# -------------------- CODE STARTS HERE ---------------------------------------
sse = []
sil_scores = []
davies_score = []
dayOfWeek = []
duration = []
columns = ["id", "Trip_id", "AvgSpeed", "HarshBreaks", "InstancesAbove120KMPH", "InstancesAbove80KMPH", "MaxSpeed",
           "SuddenTurns", "RashAccelerations", "Distance", "TripDuration", "DayOfWeek"]
df = pd.read_csv("Output\\Weekend.csv")

# X_std = process_data()
X_std = MinMaxScaler().fit_transform(df)
# Determine number of clusters using silhouette_score and  davies_bouldin_score
# n_clusters = elbow_method()
# if n_clusters is None:
n_clusters = 5
cluster_data()
plt.show()
