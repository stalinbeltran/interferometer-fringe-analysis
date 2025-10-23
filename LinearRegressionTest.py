

import numpy as np
from sklearn.linear_model import LinearRegression
X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
# y = 1 * x_0 + 2 * x_1 + 3
y = np.dot(X, np.array([3.5, 9.04])) - 1.5
reg = LinearRegression().fit(X, y)
print("reg.score(X, y):", reg.score(X, y))
print("reg.coef_:", reg.coef_)
print("reg.intercept_:", reg.intercept_)
print("reg.predict(np.array([[3, 5]])):", reg.predict(np.array([[3, 5]])))

#print("xxxxxxxxxx:", xxxxxxxxxx)



