from __future__ import print_function

import os
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from scipy import misc
from struct import unpack

from sklearn import metrics
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

def plot_mean_image(X, log):
    meanrow = X.mean(0)
    # present the row vector as an image
    plt.figure(figsize=(3,3))
    plt.imshow(np.reshape(meanrow,(28,28)), cmap=plt.cm.binary)
    plt.title('Mean image of ' + log)
    plt.show()

def get_labeled_data(imagefile, labelfile):
    """
    Read input-vector (image) and target class (label, 0-9) and return it as list of tuples.
    Adapted from: https://martin-thoma.com/classify-mnist-with-pybrain/
    """
    # Open the images with gzip in read binary mode
    images = open(imagefile, 'rb')
    labels = open(labelfile, 'rb')

    # Read the binary data
    # We have to get big endian unsigned int. So we need '>I'

    # Get metadata for images
    images.read(4)  # skip the magic_number
    number_of_images = images.read(4)
    number_of_images = unpack('>I', number_of_images)[0]
    rows = images.read(4)
    rows = unpack('>I', rows)[0]
    cols = images.read(4)
    cols = unpack('>I', cols)[0]

    # Get metadata for labels
    labels.read(4)  # skip the magic_number
    N = labels.read(4)
    N = unpack('>I', N)[0]

    if number_of_images != N:
        raise Exception('number of labels did not match the number of images')

    # Get the data
    X = np.zeros((N, rows * cols), dtype=np.uint8)  # Initialize numpy array
    y = np.zeros(N, dtype=np.uint8)  # Initialize numpy array
    for i in range(N):
        for id in range(rows * cols):
            tmp_pixel = images.read(1)  # Just a single byte
            tmp_pixel = unpack('>B', tmp_pixel)[0]
            X[i][id] = tmp_pixel
        tmp_label = labels.read(1)
        y[i] = unpack('>B', tmp_label)[0]
    return (X, y)


def my_clustering(X, y, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(X)
    print("Center is:\n", kmeans.cluster_centers_);
    AdjustRandIndex = metrics.cluster.adjusted_rand_score(y,kmeans.labels_)
    MutualInformationBaseScore = metrics.adjusted_mutual_info_score(y,kmeans.labels_)
    vMeasureScore = metrics.cluster.v_measure_score(y, kmeans.labels_)
    SilhouetteCoef = metrics.silhouette_score(X, kmeans.labels_, metric='euclidean')
    return [AdjustRandIndex,MutualInformationBaseScore,vMeasureScore,SilhouetteCoef]

def main():
    # Load the dataset
    fname_img = 't10k-images.idx3-ubyte'
    fname_lbl = 't10k-labels.idx1-ubyte'
    [X, y]=get_labeled_data(fname_img, fname_lbl)
    print("Number of sample instance is:", X.shape[0])
    print("Number of feature is:", X.shape[1])
    # Plot the mean image
    #plot_mean_image(X, 'all images')

    model = PCA(n_components = X.shape[1])
    model.fit(X)
    D = model.explained_variance_
    pov = [0];
    flag = 0
    pov_denominator = np.sum(model.explained_variance_)
    pov_numerator = 0
    for i in range(0,len(D)):
        pov_numerator = pov_numerator + D[i]
        if (pov_numerator / pov_denominator) > 0.95 and flag == 0:
            flag = 1
            print("Pov > 0.95, we need", i, "feature")
            numOfPreserve = i
        pov.append(pov_numerator / pov_denominator)

    pca = PCA(n_components = numOfPreserve)
    pca.fit(X)
    X = pca.transform(X) #reduce dimision of X to be numOfPreserve feature
    #print(X.shape[0],X.shape[1])

    # Clustering
    range_n_clusters = [8, 9, 10, 11, 12]
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
