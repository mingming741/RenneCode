import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn import linear_model, datasets
from sklearn.cross_validation import train_test_split

n_samples = 10000
centers = [(-1, -1), (1, 1)]
X, y = make_blobs(n_samples=n_samples, n_features=2, cluster_std=1.8,
                  centers=centers, shuffle=False, random_state=42)
y[:n_samples // 2] = 0
y[n_samples // 2:] = 1
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
log_reg = linear_model.LogisticRegression()
#print(X, X.shape)
#print(y, y.shape)
log_reg.fit(X_train, y_train)
#for x in range(0, log_reg.predict(X_train).shape[0]):
#    if (log_reg.predict(X_train)[x] != 0) and (log_reg.predict(X_train)[x] != 1):
#        print("Oh")

print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)
label = log_reg.predict(X_test)
error = y_test -  label
total = 0
for x in range(0, error.shape[0]):
    total = total + error[x] * error[x]

print("Number of wrong prediction is :", total)
plt.xlabel("X")
plt.ylabel("Y")
plt.scatter(X_test[:,0], X_test[:,1] ,c = label)
plt.title("Classification with Logistic Regression")
plt.show()