import numpy as np
from sklearn.linear_model import RANSACRegressor, LinearRegression
from sklearn.metrics import mean_squared_error

# Example data
x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)
y = np.array([0.1, 1.1, 2.0, 2.9, 4.1, 5.0, 6.2, 7.1, 8.2, 20.0, 80.5])  # last point is an outlier

# Reshape for sklearn
X = x.reshape(-1, 1)

# Create a Linear Regression model
model = LinearRegression()

# Train the model
model.fit(X, y)

# Make predictions
#predictions = model.predict(X_test)

# Access coefficients and intercept
print(f"Coefficient: {model.coef_[0]}")
print(f"Intercept: {model.intercept_}")




print("--------------- Ransac ")
lr = LinearRegression()
# --- Robust fit (ignores outliers automatically) ---
ransac = RANSACRegressor()
ransac.fit(X, y)

coefficients = ransac.estimator_.coef_
intercept = ransac.estimator_.intercept_

print(f"Coefficients: {coefficients}")
print(f"Intercept: {intercept}")

y_pred = ransac.predict(X)

# Residuals (inliers only)
inlier_mask = ransac.inlier_mask_
print("inlier_mask: ", inlier_mask)
residuals = y[inlier_mask] - y_pred[inlier_mask]

# --- Dispersion measures ---
# 1. Root Mean Square Error (classical)
rmse = np.sqrt(mean_squared_error(y[inlier_mask], y_pred[inlier_mask]))

# 2. Median Absolute Deviation (robust)
mad = 1.4826 * np.median(np.abs(residuals - np.median(residuals)))

print(f"RMSE (inliers): {rmse:.4f}")
print(f"Robust MAD dispersion: {mad:.4f}")
print(f"Inliers detected: {np.sum(inlier_mask)}/{len(y)}")

y_inliers = y[inlier_mask]
print("max: ", max(y_inliers))
print("min: ", min(y_inliers))