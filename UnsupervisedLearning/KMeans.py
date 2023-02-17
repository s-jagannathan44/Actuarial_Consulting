import pandas as pd
import matplotlib.pyplot as plt
from kneed import KneeLocator
from sklearn.cluster import KMeans as Km
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline


def score_PCA():
    for n in range(1, 8):
        # This set the number of components for pca,
        # but leaves other steps unchanged
        pipe["preprocessor"]["pca"].n_components = n
        pipe.fit(df_)

        silhouette_coef = silhouette_score(
            pipe["preprocessor"].transform(df_),
            pipe["clusterer"]["kmeans"].labels_,
        )
        # Add metrics to their lists
        sil_scores.append(silhouette_coef)
    plt.style.use("fivethirtyeight")
    plt.figure(figsize=(6, 6))
    plt.plot(
        range(1, 8),
        sil_scores,
        c="#008fd5",
        label="Silhouette Coefficient",
    )
    plt.xlabel("n_components")
    plt.legend()
    plt.title("Clustering Performance as a Function of n_components")
    plt.tight_layout()
    plt.show()


def elbow_method(X_std):
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


# -------------------- CODE STARTS HERE ---------------------------------------
sse = []
sil_scores = []
davies_score = []
df_ = pd.read_csv("Output\\FinalData.csv")
n_clusters = elbow_method(MinMaxScaler().fit_transform(df_))
# Create Pipelines
preprocessor = Pipeline([("scaler", MinMaxScaler()), ("pca", PCA(n_components=1, random_state=42)), ])
clusterer = Pipeline([(
    "kmeans",
    Km(n_clusters=n_clusters, init="k-means++", n_init=50, max_iter=500, random_state=42, ),
)])
pipe = Pipeline([("preprocessor", preprocessor), ("clusterer", clusterer)])
score_PCA()
pipe.fit(df_)
preprocessed_data = pipe["preprocessor"].transform(df_)
print(n_clusters)
predicted_labels = pipe["clusterer"]["kmeans"].labels_
df_["Cluster"] = predicted_labels
df_.to_csv("Output\\clustered.csv")
print(silhouette_score(preprocessed_data, predicted_labels))
