import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans as Km
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score


def cluster_data():
    # Run local implementation of k means
    km = Km(n_clusters=8, max_iter=100, init='k-means++')
    labels = km.fit_predict(X_std)
    print(silhouette_score(X_std, labels))
    print(davies_bouldin_score(X_std, labels))
    df_["Cluster"] = km.labels_
    df_.to_csv("Output\\clustered.csv")


def score_clusters():
    list_k = list(range(2, 10))
    for k in list_k:
        km = Km(n_clusters=k)
        labels = km.fit_predict(X_std)
        sil_scores.append(silhouette_score(X_std, labels))
    # Plot sse against k
    plt.figure(figsize=(6, 6))
    plt.plot(list_k, sil_scores, '-o')
    plt.xlabel(r'Number of clusters $k$')
    plt.ylabel('Score')


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


# -------------------- CODE STARTS HERE ---------------------------------------
sse = []
sil_scores = []
davies_score = []
df_ = pd.read_csv("Output\\FinalData.csv")
# Standardize the data
X_std = StandardScaler().fit_transform(df_)
# Determine number of clusters using silhouette_score and  davies_bouldin_score
score_clusters()
elbow_method()
cluster_data()
plt.show()
