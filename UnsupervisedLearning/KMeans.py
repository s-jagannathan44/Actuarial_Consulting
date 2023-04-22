import pandas as pd
import matplotlib.pyplot as plt
from kneed import KneeLocator
from sklearn.cluster import KMeans as Km
# from sklearn.metrics import silhouette_score
from sklearn.preprocessing import MinMaxScaler
import joblib
import seaborn as sns


def plot(X, y):
    plt.figure(figsize=(16, 6))
    colors = ["#FFFF00", "#FF0000", "#599988", "#E08181"]
    ax = sns.scatterplot(data=df, x=X, y=y, hue='Cluster',
                         s=200, palette=colors, legend=True)
    plt.legend(loc='lower right', title='Cluster')
    ax.set_title("Clustered Points", fontsize='xx-large', y=1.05)


def cluster_data():
    km = joblib.load("Output\\ModelFiles\\NRANHB1204Clusters.sav")
    labels = km.predict(X_std)
    print("Predict complete")
    # print(silhouette_score(X_std, labels))
    df["Cluster"] = labels  # km.labels_
    df.to_csv("Output\\Clustered\\clustered.csv")

    plot("NRA by Distance", "NHB by Distance")
    plt.show()


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
df = pd.read_csv("Output\\InputFile_March.csv")
X_std = MinMaxScaler().fit_transform(df)

cluster_data()
