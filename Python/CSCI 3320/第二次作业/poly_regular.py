import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model

X_train = [[5.3], [7.2], [10.5], [14.7], [18], [20]]
y_train = [[7.5], [9.1], [13.2], [17.5], [19.3], [19.5]]

X_test = [[6], [8], [11], [22]]
y_test = [[8.3], [12.5], [15.4], [19.6]]

poly = PolynomialFeatures(degree=5)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)
#print(X_train_poly.shape)

model = linear_model.LinearRegression()
model.fit(X_train, y_train)
print("Coefficient: " ,model.intercept_, model.coef_)
print("Linear Regression (order 1) score is :", model.score(X_test,y_test))

#2.3.1 Linear Regression of data
model = linear_model.LinearRegression()
model.fit(X_train_poly, y_train)
print("Coefficient: " ,model.intercept_, model.coef_)
print("Linear Regression (order 5) score is :", model.score(X_test_poly,y_test))

xx = np.linspace(0, 26, 100)
xx_poly = poly.transform(xx.reshape(xx.shape[0], 1))
yy_poly = model.predict(xx_poly)

plt.xlabel("X")
plt.ylabel("Y")
plt.plot(xx, yy_poly, color = "blue")
plt.plot(X_test,y_test, color = "black")
plt.title("Linear Regression (order 5) result")
plt.show()

#2.3.2 Ridge Regression
ridge_model = Ridge(alpha=20, normalize=False)
ridge_model.fit(X_train_poly, y_train)
print("Coefficient: " ,ridge_model.intercept_, ridge_model.coef_)
print("Ridge Regression (order 5) score is :", ridge_model.score(X_test_poly,y_test))

yy_ridge = ridge_model.predict(xx_poly)

plt.xlabel("X")
plt.ylabel("Y")
plt.plot(xx, yy_ridge, color = "blue")
plt.plot(X_test,y_test, color = "black")
plt.title("Linear Regression (order 5) result")
plt.show()
