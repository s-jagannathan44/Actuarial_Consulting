# This file contains the code for clustering Commercial Vehicle - Taxi Data

# Import statements used to include code from other libraries
import pandas as pd
import matplotlib.pyplot as plt
from kneed import KneeLocator
from sklearn.cluster import KMeans as Km
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import MinMaxScaler
import joblib
import seaborn as sns


# This method is for plotting the clusters in a 3-dimensional scatter plot
def plot3d(x, y_clusters):
    fig = plt.figure(figsize=(15, 15))
    ax = fig.add_subplot(111, projection='3d')

    # There is one line for each cluster to be plotted. As we have 6 clusters we have 6 lines.
    # In case fewer clusters are used the necessary changes can be made
    ax.scatter(x[y_clusters == 0, 0], x[y_clusters == 0, 2], x[y_clusters == 0, 1], s=40, color='red',
               label="cluster 0")
    ax.scatter(x[y_clusters == 1, 0], x[y_clusters == 1, 2], x[y_clusters == 1, 1], s=40, color='blue',
               label="cluster 1")
    ax.scatter(x[y_clusters == 2, 0], x[y_clusters == 2, 2], x[y_clusters == 2, 1], s=40, color='green',
               label="cluster 2")
    ax.scatter(x[y_clusters == 3, 0], x[y_clusters == 3, 2], x[y_clusters == 3, 1], s=40, color='black',
               label="cluster 3")

    ax.scatter(x[y_clusters == 4, 0], x[y_clusters == 4, 2], x[y_clusters == 4, 1], s=40, color='yellow',
               label="cluster 4")
    ax.scatter(x[y_clusters == 5, 0], x[y_clusters == 5, 2], x[y_clusters == 5, 1], s=40, color='orange',
               label="cluster 5")

    # These are the 3 columns in the input file which are clustered
    ax.set_xlabel('NRA by Distance')
    ax.set_ylabel('NHB by distance')
    ax.set_zlabel('A120 by distance')
    ax.legend()
    plt.show()


# This method is for plotting the clusters in a 2-dimensional scatter plot
def plot(X, y):
    plt.figure(figsize=(16, 6))

    # The number of  colors should be equal to the number of  clusters and should be specified in RGB format.
    colors = ["#FFFF00", "#FF0000", "#599988", "#E08181", "#F00000", "#ABCDEF"]
    ax = sns.scatterplot(data=df, x=X, y=y, hue='Cluster',
                         s=200, palette=colors, legend=True)
    plt.legend(loc='lower right', title='Cluster')
    ax.set_title("Clustered Points", fontsize='xx-large', y=1.05)


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
    ModelFileName = "Output\\Cluster.sav"

    # Below code loads the model from file, calculates the silhouette_score after generating the clusters
    # and finally plots them in 2 and 3 dimensions
    km = joblib.load(ModelFileName)
    labels = km.predict(X_std)
    print("Predict complete")
    print(silhouette_score(X_std, labels))
    df["Cluster"] = labels  # km.labels_
    df.to_csv("Output\\Clustered\\clustered.csv")
    plot("NRA by Distance", "NHB by Distance")
    plot("NRA by Distance", "A 120")
    plot("NHB by Distance", "A 120")
    plt.show()
    plot3d(X_std, labels)


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
df = pd.read_csv("CommercialVehicle\\InputFile.csv")
# this line is used for Scaling  the input before clustering
X_std = MinMaxScaler().fit_transform(df)
# This line sets the number of clusters to be used by K Means
n_clusters = 6
fit_data()
cluster_data()
