# Import statements used to include code from other libraries
import pandas as pd
import matplotlib.pyplot as plt
from kneed import KneeLocator
from sklearn.cluster import KMeans as Km
# from sklearn.metrics import silhouette_score
from sklearn.preprocessing import MinMaxScaler
import joblib


# This method is used for fitting the clusters and should not be called
# once the model has been finalised and saved
def fit_data():
    OutputFileName = "Output\\Cluster.sav"
    km = Km(n_clusters=n_clusters, max_iter=100, init='k-means++')
    km.fit(X_std)
    # This line saves the fitted model to file.
    # Once model is finalised this file will be used to cluster the data
    joblib.dump(km, OutputFileName)


# This method is used for generating the clusters from the saved file
def cluster_data():
    ModelFileName = "KMeansModelFiles\\NRANHB1204Clusters.sav"

    # Below code loads the model from file, calculates the silhouette_score after generating the clusters
    # and finally plots them in 2 and 3 dimensions
    km = joblib.load(ModelFileName)
    labels = km.predict(X_std)
    print("Predict complete")
    # print(silhouette_score(X_std, labels))
    df["Cluster"] = labels  # km.labels_
    df.to_csv("Output\\Clustered\\clustered.csv")


# This method is used for calculating the initial number of clusters using the elbow method
def elbow_method():
    sse = []
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
    # sometimes the elbow is hard to identify visually so this library returns us the number of clusters
    return KneeLocator(range(2, 12), sse, curve="convex", direction="decreasing").elbow


# -------------------- MAIN CODE STARTS HERE ---------------------------------------
# This is the input file from which the clusters are to be generated
df = pd.read_csv("Output\\InputFile - Test.csv")
# this line is used for Scaling  the input before clustering
X_std = MinMaxScaler().fit_transform(df)
# This line sets the number of clusters to be used by K Means
n_clusters = 4
cluster_data()
