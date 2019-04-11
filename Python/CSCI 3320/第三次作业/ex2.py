import os.path
import numpy as np
import matplotlib.pyplot as plt
from scipy import misc
from sklearn.decomposition import PCA

def load_data(digits = [0], num = 200):
    totalsize = 0
    for digit in digits:
        totalsize += min([len(next(os.walk('train%d' % digit))[2]), num])
    print('We will load %d images' % totalsize)
    X = np.zeros((totalsize, 784), dtype = np.uint8)   #784=28*28
    for index in range(0, len(digits)):
        digit = digits[index]
        print('\nReading images of digit %d' % digit)
        for i in range(num):
            pth = os.path.join('train%d' % digit,'%05d.pgm' % i)
            image = misc.imread(pth).reshape((1, 784))
            X[i + index * num, :] = image
        print('\n')
    return X

def plot_mean_image(X, digits = [0]):
    ''' example on presenting vector as an image
    '''
    plt.close('all')
    meanrow = X.mean(0)
    # present the row vector as an image
    plt.imshow(np.reshape(meanrow,(28,28)))
    plt.title('Mean image of digit ' + str(digits))
    plt.gray(), plt.xticks(()), plt.yticks(()), plt.show()

def main():
    digits = [0, 1, 2]
    X = load_data(digits, 500)
    #print("Shape of x is:", X.shape[0], "x", X.shape[1])
    model = PCA(n_components=X.shape[1])
    model.fit(X)
    D = model.explained_variance_
    V = model.components_
    plot_mean_image(V[:9], digits)

    pov = [0];
    flag = 0
    pov_denominator = np.sum(model.explained_variance_)
    pov_numerator = 0
    for i in range(0,len(D)):
        pov_numerator = pov_numerator + D[i]
        if (pov_numerator / pov_denominator) > 0.9 and flag == 0:
            flag = 1
            print("Pov > 0.9, we need", i, "feature")
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
