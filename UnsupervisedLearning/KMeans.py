import pandas as pd
import matplotlib.pyplot as plt
from kneed import KneeLocator
from sklearn.cluster import KMeans as Km
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import MinMaxScaler
import joblib
import numpy as np
# import seaborn as sns


def cluster_data():
    # Run local implementation of k means
    km = Km(n_clusters=n_clusters, max_iter=100, init='k-means++')
    km.fit(X_std)
    joblib.dump(km, "Output\\Cluster.sav")
    # km = joblib.load("Output\\Cluster.sav")
    labels = km.predict(X_std)
    print("Predict complete")
    print(silhouette_score(X_std, labels))
    df["Cluster"] = labels  # km.labels_
    df.to_csv("Output\\clustered.csv")

    # plt.figure(fig size=(16, 6))
    # colors = ["#A181E0", "#E08181", "#599988", "#FF0000"]
    # ax = sns.scatter plot(data=df, x="A80", y="NRA by Distance", hue='Cluster',
    #                      s=200, palette=colors, legend=True)
    #
    # plt.legend(loc='lower right', title='Cluster')
    # ax.set_title("Clustered Points", font size='xx-large', y=1.05)
    # plt.show()


def elbow_method():
    list_k = list(range(2, 12))
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
    return KneeLocator(range(2, 12), sse, curve="convex", direction="decreasing").elbow


def silhouette_method():
    list_k = list(range(2, 10))

    for k in list_k:
        print(k)
        km = Km(n_clusters=k)
        labels = km.fit_predict(X_std)
        sil_scores.append(silhouette_score(X_std, labels))
    # Plot sil  against k
    plt.figure(figsize=(6, 6))
    plt.plot(list_k, sil_scores, '-o')
    plt.xlabel(r'Number of clusters $k$')
    plt.ylabel('Silhouette Score')

    plt.show()


def explained_variance():
    pca = PCA().fit(X_std)
    plt.rcParams["figure.figsize"] = (12, 6)

    fig, ax = plt.subplots()
    xi = np.arange(1, 4, step=1)
    y = np.cumsum(pca.explained_variance_ratio_)

    plt.ylim(0.0, 1.1)
    plt.plot(xi, y, marker='o', linestyle='--', color='b')

    plt.xlabel('Number of Components')
    plt.xticks(np.arange(1, 4, step=1))  # change from 0-based array index to 1-based human-readable label
    plt.ylabel('Cumulative variance (%)')
    plt.title('The number of components needed to explain variance')

    plt.axhline(y=0.85, color='r', linestyle='-')
    plt.text(0.5, 0.95, '85% cut-off threshold', color='red', fontsize=16)

    ax.grid(axis='x')
    plt.show()


# -------------------- CODE STARTS HERE ---------------------------------------
sse = []
sil_scores = []
df = pd.read_csv("Output\\InputFile -All.csv")
X_std = MinMaxScaler().fit_transform(df)

# explained_variance()
# Determine number of clusters using silhouette_score

# silhouette_method()

# n_clusters = elbow_method()
# print(n_clusters)
# if n_clusters is None:
n_clusters = 4
cluster_data()
