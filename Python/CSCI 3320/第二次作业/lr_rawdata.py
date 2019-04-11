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

cut = int(len(data) * 0.2)
data_train = data[cut:]
data_test = data[:cut]

#2.1.3: Standardization for 2 feature, engine size & price
target_feature_train = data_train[:,[21,25]]
target_feature_test = data_test[:,[21,25]]
X_scaler = StandardScaler()
X_train_scaled = X_scaler.fit_transform(target_feature_train) #select 2 feature
X_test_scaled = X_scaler.transform(target_feature_test)

#2.1.4: Treat horsepower as feature & price as label:
model = linear_model.LinearRegression()
X_train_horsepower = np.reshape(X_train_scaled[:,0], (-1, 1))
X_test_horsepower = np.reshape(X_test_scaled[:,0], (-1, 1))
Y_train_price = np.reshape(X_train_scaled[:,1], (-1, 1))
Y_test_price = np.reshape(X_test_scaled[:,1], (-1, 1))
#print(X_train_horsepower.shape, Y_train_price.shape, X_test_horsepower.shape, Y_test_price.shape)
model.fit(X_train_horsepower, Y_train_price)

#Try to plot horsepower and price
plt.xlabel(feature[21])
plt.ylabel(feature[25])
plt.scatter(X_test_horsepower, Y_test_price, color = "blue")
plt.plot(X_test_horsepower,model.predict(X_test_horsepower), color = "black")
plt.title("Linear Regression on clean and standardized data")
plt.show()

