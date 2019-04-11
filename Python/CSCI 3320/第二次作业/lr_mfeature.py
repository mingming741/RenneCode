import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.preprocessing import StandardScaler
import seaborn
seaborn.set()

#2.1.(1&2): Read Data & clean NaN
df = pd.read_csv('imports-85.data',
            header=None,
            names=['symboling', 'normalized-losses','make','fuel-type','aspiration',' num-of-doors','body-style', \
                   'drive-wheels', 'engine-location', 'wheel-base','length', 'width', 'height', 'curb-weight', \
                   'engine-type', 'num-of-cylinders', 'engine-size', 'fuel-system', 'bore', 'stroke', 'compression-ratio', \
                   'horsepower', 'peak-rpm', 'city-mpg', 'highway-mpg', 'price'],
                na_values=('?'))
df = df.dropna(axis = 0, how = 'any')
feature = list(df)
data = df.values
print("Number of features in the Training dataset is:",len(feature))
print("Number of instance in the Training dataset is:",len(data))

#2.2: Standardization
target_feature = data[:,[21,16,22,25]]
scaler = StandardScaler()
data_scaled = scaler.fit_transform(target_feature) #select 4 feature
X_data_scaled = data_scaled[:,[0,1,2]]
Y_data_scaled = data_scaled[:,3]
ones = [1 for x in range(X_data_scaled.shape[0]) ]
#print(ones)
X_data_scaled_prime = np.insert(X_data_scaled, 0, ones, axis=1)
#print(X_data_scaled)
theta = np.linalg.inv(np.dot(X_data_scaled_prime.transpose(),X_data_scaled_prime)) # (XT * X) ^ -1
theta = np.dot(np.dot(theta, X_data_scaled_prime.transpose()), Y_data_scaled) #  (XT * X) ^ -1 * XT * y
print("Parameter theta calculated by normal equation: ", theta)

clf = linear_model.SGDRegressor(max_iter = 10000)
clf.fit(X_data_scaled, Y_data_scaled)
print("Parameter theta calculated by SDG :", clf.intercept_, clf.coef_);

