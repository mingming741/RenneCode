import seaborn; seaborn.set()
import scipy.io as sio
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB

train_data_raw = sio.loadmat('train.mat')
train_data_X = train_data_raw['Xtrain']
train_data_y = train_data_raw['ytrain'].ravel()
print("Number of features in the Training dataset is:",train_data_X.shape[1])
print("Number of features in the Training dataset is:",train_data_X.shape[0])

gnb = GaussianNB()
gnb.fit(train_data_X, train_data_y)
gnb_score = gnb.score(train_data_X, train_data_y)
print("GNB:",gnb_score)

mul = MultinomialNB()
mul.fit(train_data_X, train_data_y)
mul_score = mul.score(train_data_X, train_data_y)
print("MUL:",mul_score)

ber = BernoulliNB()
ber.fit(train_data_X, train_data_y)
ber_score = ber.score(train_data_X, train_data_y)
print("BER:",ber_score)
print("The accuracy of the classifier:", mul_score)

test_data_raw = sio.loadmat('test.mat')
test_data_X = test_data_raw['Xtest']
predicted_output = mul.predict(test_data_X)
thefile = open('prediction.txt', 'w')
for item in predicted_output:
  thefile.write("%s\n" % item)




