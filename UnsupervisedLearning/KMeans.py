import pandas as pd
from kneed import KneeLocator
from sklearn.cluster import KMeans as Km
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline


def elbow_method(X_std):
    list_k = list(range(2, 10))
    for k in list_k:
        km = Km(n_clusters=k)
        km.fit(X_std)
        sse.append(km.inertia_)
    # Plot sse against k
    return KneeLocator(range(2, 10), sse, curve="convex", direction="decreasing").elbow


# -------------------- CODE STARTS HERE ---------------------------------------
sse = []
sil_scores = []
davies_score = []
n_clusters = 5
df_ = pd.read_csv("Output\\FinalData.csv")
# Create Pipelines
preprocessor = Pipeline([("scaler", MinMaxScaler()), ("pca", PCA(n_components=4, random_state=42)), ])
clusterer = Pipeline([(
    "kmeans",
    Km(n_clusters=n_clusters, init="k-means++", n_init=50, max_iter=500, random_state=42, ),
)])
pipe = Pipeline([("preprocessor", preprocessor), ("clusterer", clusterer)])

pipe.fit(df_)
preprocessed_data = pipe["preprocessor"].transform(df_)
n_clusters = elbow_method(preprocessed_data)
print(n_clusters)
predicted_labels = pipe["clusterer"]["kmeans"].labels_
print(silhouette_score(preprocessed_data, predicted_labels))
