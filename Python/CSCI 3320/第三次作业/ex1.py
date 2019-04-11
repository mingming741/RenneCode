import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def create_data(x1, x2, x3):
    x4 = -4.0 * x1
    x5 = 10 * x1 + 10
    x6 = -1 * x2 / 2
    x7 = np.multiply(x2, x2)
    x8 = -1 * x3 / 10
    x9 = 2.0 * x3 + 2.0
    X = np.hstack((x1, x2, x3, x4, x5, x6, x7, x8, x9))
    return X

def pca(X):
    featureMean = X.mean(axis = 0)
    X_Append = featureMean[np.newaxis, :]
    for i in range (0, X.shape[0] - 1):
        X_Append = np.append(X_Append, featureMean[np.newaxis, :], axis = 0)
    X_Normal = np.subtract(X, X_Append)
    X_Cov = np.cov(np.transpose(X_Normal))
    D, V = np.linalg.eigh(X_Cov)
    idx = D.argsort()[::-1]
    D = D[idx]
    V = V[:, idx]
    return [V, D]
    # here V is the matrix containing all the eigenvectors, D is the column vector containing all the corresponding eigenvalues.

def main():
    N = 1000
    shape = (N, 1)
    x1 = np.random.normal(0, 1, shape) # samples from normal distribution
    x2 = np.random.exponential(10.0, shape) # samples from exponential distribution
    x3 = np.random.uniform(-100, 100, shape) # uniformly sampled data points
    X = create_data(x1, x2, x3)

    model = PCA(n_components=9)
    model.fit(X)
    print("Packet eigenvalue:", model.explained_variance_)#, "\nPacket eigenvector:", model.components_)
    V, D = pca(X)
    print("My eigenvalue is", D)
    D_sorted = sorted(D,reverse=True)

    plt.figure(1)
    x_axis = [i for i in range(1,len(D) + 1)]
    plt.xlabel("Order of eigenvalue")
    plt.ylabel("Value of eigenvalue")
    plt.plot(x_axis, D_sorted, color="blue")
    plt.title("Eigenvalue order and value")

    pov = [0];
    pov_denominator = np.sum(D_sorted)
    pov_numerator = 0
    for i in range(0,9):
        pov_numerator = pov_numerator + D_sorted[i]
        pov.append(pov_numerator / pov_denominator)

    plt.figure(2)
    x_axis = [i for i in range(0, len(D) + 1)]
    plt.xlabel("Number of eigenvalue")
    plt.ylabel("POV")
    plt.plot(x_axis, pov, color="blue")
    plt.title("POV")
    plt.show()

if __name__ == '__main__':
    main()

