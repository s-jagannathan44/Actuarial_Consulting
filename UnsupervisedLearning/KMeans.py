import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans as Km
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score


# -------------------- CODE STARTS HERE ---------------------------------------
sil_scores = []
calinksi_score = []
davies_score = []
df_ = pd.read_csv("Output\\FinalData.csv")

# Standardize the data
X_std = StandardScaler().fit_transform(df_)
# Run local implementation of k means
km = Km(n_clusters=8, max_iter=100, init='k-means++')

labels = km.fit_predict(X_std)
print(silhouette_score(X_std, labels))
print(davies_bouldin_score(X_std, labels))
centroids = km.cluster_centers_
df_["Cluster"] = km.labels_
df_.to_csv("Output\\clustered.csv")

# Plot the clustered data

# Run the Kmeans algorithm and get the index of data points clusters
sse = []
list_k = list(range(2, 10))

for k in list_k:
    km = Km(n_clusters=k)
    labels = km.fit_predict(X_std)
    sse.append(km.inertia_)
    sil_scores.append(silhouette_score(X_std, labels))
    calinksi_score.append(calinski_harabasz_score(X_std, labels))
    davies_score.append(davies_bouldin_score(X_std, labels))
# Plot sse against k
plt.figure(figsize=(6, 6))
plt.plot(list_k, sil_scores, '-o')
plt.xlabel(r'Number of clusters $k$')
plt.ylabel('Sum of squared distance')

plt.show()
