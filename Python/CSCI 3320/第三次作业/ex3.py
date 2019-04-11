from __future__ import print_function
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt

from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn import metrics

def create_data():
    centers = [[3,5], [5,1], [8,2], [6,8], [9,7]]
    X, y = make_blobs(n_samples=1000,centers=centers,cluster_std=0.5,random_state=3320)
    # =======================================
    return [X, y]

def my_clustering(X, y, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(X)
    plt.figure(1)
    plt.xlabel("dim1")
    plt.ylabel("dim2")
    plt.scatter(X[:,0], X[:,1], c= kmeans.labels_)
    plt.title("Kmean Result")
    plt.show()
    print("Center is:\n", kmeans.cluster_centers_);
    AdjustRandIndex = metrics.cluster.adjusted_rand_score(y,kmeans.labels_)
    MutualInformationBaseScore = metrics.adjusted_mutual_info_score(y,kmeans.labels_)
    vMeasureScore = metrics.cluster.v_measure_score(y, kmeans.labels_)
    SilhouetteCoef = metrics.silhouette_score(X, kmeans.labels_, metric='euclidean')
    return [AdjustRandIndex,MutualInformationBaseScore,vMeasureScore,SilhouetteCoef]

def main():
    X, y = create_data()
    range_n_clusters = [2, 3, 4, 5, 6]
    ari_score = [None] * len(range_n_clusters)
    mri_score = [None] * len(range_n_clusters)
    v_measure_score = [None] * len(range_n_clusters)
    silhouette_avg = [None] * len(range_n_clusters)

    for n_clusters in range_n_clusters:
        i = n_clusters - range_n_clusters[0]
        print("Number of clusters is: ", n_clusters)
        [ari_score[i], mri_score[i], v_measure_score[i], silhouette_avg[i]] = my_clustering(X, y, n_clusters)
        print('The ARI score is: ', ari_score[i])
        print('The MRI score is: ', mri_score[i])
        print('The v-measure score is: ', v_measure_score[i])
        print('The average silhouette score is: ', silhouette_avg[i])

    plt.figure(3)
    plt.title("score information")
    plt.subplot(221)
    plt.xlabel("number of cluster")
    plt.ylabel("Adjust Rand Index")
    plt.plot(range_n_clusters, ari_score, c= "black")
    plt.subplot(222)
    plt.xlabel("number of cluster")
    plt.ylabel("Mutual Information Base Score")
    plt.plot(range_n_clusters, mri_score, c= "black")
    plt.subplot(223)
    plt.xlabel("number of cluster")
    plt.ylabel("v Measure Score")
    plt.plot(range_n_clusters, v_measure_score, c= "black")
    plt.subplot(224)
    plt.xlabel("number of cluster")
    plt.ylabel("Silhouette Coef")
    plt.plot(range_n_clusters, silhouette_avg, c= "black")
    plt.show()

if __name__ == '__main__':
    main()

