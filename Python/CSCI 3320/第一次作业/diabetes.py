import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
import seaborn; seaborn.set()

# Load the diabetes dataset
diabetes = datasets.load_diabetes()
# which feature
i_feature = 0
score = []
loss = []
# Get the feature name
feature_names = ['Age', 'Sex', 'Body mass index', 'Average blood pressure', 'S1',
                 'S2', 'S3', 'S4', 'S5', 'S6']
diabetes_X = diabetes.data[:, np.newaxis, 1]
print("Number of features in the Diabetes dataset is:",diabetes.data.shape[1])
print("Number of features in the Diabetes dataset is:",diabetes.data.shape[0])

#print(diabetes.data)
print(diabetes_X)

for i_feature in range (0, len(feature_names)):
    diabetes_X = diabetes.data[:, np.newaxis, i_feature]
    diabetes_X_train = diabetes_X[:-20]
    diabetes_X_test = diabetes_X[-20:]
    diabetes_y_train = diabetes.target[:-20]
    diabetes_y_test = diabetes.target[-20:]
    model = linear_model.LinearRegression()
    model.fit(diabetes_X_train, diabetes_y_train)
    model_score = model.score(diabetes_X_test, diabetes_y_test)
    score.append((i_feature, model_score))
    model_loss = ((model.predict(diabetes_X_test) - diabetes_y_test) ** 2).mean()
    loss.append(model_loss)

score = sorted(score, key=lambda tup: tup[1], reverse=True)
for i in range (0, len(score)):
    print("Order list of feature name is:", feature_names[score[i][0]])
    print("Order list of model scores is:", score[i][1])

print("Value of the loss function for the best fitted model is:",min(loss))

diabetes_X = diabetes.data[:, np.newaxis, score[0][0]]
diabetes_X_train = diabetes_X[:-20]
diabetes_X_test = diabetes_X[-20:]
diabetes_y_train = diabetes.target[:-20]
diabetes_y_test = diabetes.target[-20:]
model = linear_model.LinearRegression()
#print(diabetes_X_train.shape)
#print(diabetes_y_train.shape)
model.fit(diabetes_X_train, diabetes_y_train)

plt.xlabel(feature_names[score[0][0]])
plt.ylabel('Disease progression')
plt.scatter(diabetes_X_test, diabetes_y_test, color = "blue")
plt.plot(diabetes_X_test,model.predict(diabetes_X_test), color = "black")
plt.show()
