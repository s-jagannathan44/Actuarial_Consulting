import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.cluster import KMeans as Km
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score
from keras import Model, Input
from keras.layers import Dense


def cluster_data():
    # Run local implementation of k means
    km = Km(n_clusters=7, max_iter=100, init='k-means++', random_state=42)
    labels = km.fit_predict(X_std)
    print(silhouette_score(X_std, labels))
    print(davies_bouldin_score(X_std, labels))
    df_["Cluster"] = km.labels_
    df_.to_csv("Output\\clustered.csv")


def score_clusters():
    list_k = list(range(2, 10))
    for k in list_k:
        km = Km(n_clusters=7, max_iter=100, init='k-means++', random_state=42)
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


def run_autoencoder(X):
    input_layer = Input(shape=(7,))
    intermediate = Dense(50, activation='relu')(input_layer)
    intermediate = Dense(500, activation='relu', kernel_initializer='glorot_uniform')(intermediate)
    intermediate = Dense(500, activation='relu', kernel_initializer='glorot_uniform')(intermediate)
    intermediate = Dense(2000, activation='relu', kernel_initializer='glorot_uniform')(intermediate)
    encoded = Dense(10, activation='relu', kernel_initializer='glorot_uniform')(intermediate)
    intermediate = Dense(2000, activation='relu', kernel_initializer='glorot_uniform')(encoded)
    intermediate = Dense(500, activation='relu', kernel_initializer='glorot_uniform')(intermediate)
    decoded = Dense(7, kernel_initializer='glorot_uniform')(intermediate)
    # This is a functional, not sequential neural network
    encoder = Model(input_layer, encoded)
    autoencoder = Model(input_layer, decoded)
    autoencoder.compile(optimizer='adam', loss="mae", metrics="mae")
    autoencoder.fit(X, X, epochs=500, batch_size=1000)
    np.savetxt("Output\\encoder.csv", X, delimiter=',')
    return encoder.predict(X)


# -------------------- CODE STARTS HERE ---------------------------------------
tf.random.set_seed(5)
os.environ['PYTHONHASHSEED'] = str(33)
np.random.seed(33)


session_conf = tf.compat.v1.ConfigProto(
    intra_op_parallelism_threads=1,
    inter_op_parallelism_threads=1
)
sess = tf.compat.v1.Session(
    graph=tf.compat.v1.get_default_graph(),
    config=session_conf
)
tf.compat.v1.keras.backend.set_session(sess)
sse = []
sil_scores = []
davies_score = []
df_ = pd.read_csv("Output\\encoder.csv")
# df_ = pd.read_csv("Output\\FinalData.csv")
# Standardize the data
X_std = StandardScaler().fit_transform(df_)
# X_std = run_autoencoder(X_std)
# Determine number of clusters using silhouette_score and  davies_bouldin_score
# score_clusters()
# elbow_method()
cluster_data()
# plt.show()
