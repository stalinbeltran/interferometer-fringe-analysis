

import numpy as np
from sklearn.linear_model import LinearRegression
X = np.array([1,2,3])
print(X)
X = X.reshape(-1, 1)
print(X)

# y = 1 * x_0 + 2 * x_1 + 3
size = len(X)
y = np.zeros(size)
for i in range(size):
    y[i] = (X[i]*(-7.3) - 0.77)

print(y)    
y = y.reshape(-1, 1)
print(y)
reg = LinearRegression().fit(X, y)
print("reg.score(X, y):", reg.score(X, y))
print("reg.coef_:", reg.coef_)
print("reg.intercept_:", reg.intercept_)
print("reg.predict(np.array([[3, 5]])):", reg.predict(np.array([[3, 5]])))

#print("xxxxxxxxxx:", xxxxxxxxxx)



