import pandas as pd
import matplotlib.pyplot as plt
from kneed import KneeLocator
from sklearn.cluster import KMeans as Km
# from sklearn.metrics import silhouette_score
from sklearn.preprocessing import MinMaxScaler
import joblib
import seaborn as sns
# from sklearn.model_selection import train_test_split


def plot3d(x, y_clusters):
    fig = plt.figure(figsize=(15, 15))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x[y_clusters == 0, 0], x[y_clusters == 0, 2], x[y_clusters == 0, 1], s=40, color='blue',
               label="cluster 0")
    ax.scatter(x[y_clusters == 1, 0], x[y_clusters == 1, 2], x[y_clusters == 1, 1], s=40, color='orange',
               label="cluster 1")
    ax.scatter(x[y_clusters == 2, 0], x[y_clusters == 2, 2], x[y_clusters == 2, 1], s=40, color='green',
                label="cluster 2")
    ax.scatter(x[y_clusters == 3, 0], x[y_clusters == 3, 2], x[y_clusters == 3, 1], s=40, color='#D12B60',
                label="cluster 3")

    ax.set_xlabel('NRA by Distance')
    ax.set_ylabel('NHB by distance')
    ax.set_zlabel('A120 by distance')
    ax.legend()
    plt.show()


def plot(X, y):
    plt.figure(figsize=(16, 6))
    colors = ["#FFFF00", "#FF0000", "#599988", "#E08181", "#000000"]
    ax = sns.scatterplot(data=df, x=X, y=y, hue='Cluster',
                         s=200, palette=colors, legend=True)
    plt.legend(loc='lower right', title='Cluster')
    ax.set_title("Clustered Points", fontsize='xx-large', y=1.05)


def cluster_data():
    # km = Km(n_clusters=n_clusters, max_iter=100, init='k-means++')
    # km.fit(X_std)
    # joblib.dump(km, "Output\\Cluster.sav")

    km = joblib.load("Output\\ModelFiles\\NRANHB1204Clusters.sav")
    labels = km.predict(X_std)
    print("Predict complete")
    # print(silhouette_score(X_std, labels))
    df["Cluster"] = labels  # km.labels_
    df.to_csv("Output\\Clustered\\clustered.csv")

    # plot("NRA by Distance", "NHB by Distance")
    # plot("NRA by Distance", "A 120")
    # plot("NHB by Distance", "A 120")
    # plt.show()
    plot3d(X_std, labels)


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


# -------------------- CODE STARTS HERE ---------------------------------------
sse = []
# df = pd.read_csv("Output\\Clustered\\Out of Sample\\RandomSampling\\InputFile_Test.csv")
df = pd.read_csv("Output\\InputFile.csv")
X_std = MinMaxScaler().fit_transform(df)
# n_clusters = elbow_method()
# print(n_clusters)
# n_clusters = 4
cluster_data()

# X_train, X_test, y_train, y_test = train_test_split(df, df, test_size=0.5, random_state=25)
# X_train.to_csv("Output\\Clustered\\Out of Sample\\RandomSampling\\InputFile_Fit.csv")
# X_test.to_csv("Output\\Clustered\\Out of Sample\\RandomSampling\\InputFile_Test.csv")
