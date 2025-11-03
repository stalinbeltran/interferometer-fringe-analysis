#showSections.py


import os
import sys
import json
import cv2
import numpy as np
import globals
from collections import deque
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

input_file = (sys.argv[1])
output_file = (sys.argv[2])


with open(input_file, 'r', encoding='utf-8') as f:
    dataJSON = json.load(f)


for section in dataJSON:
    data = section["data"]
    sectionSize = section["size"]
    ydata = data[dataType]["deltaPhase"]

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



with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(newData, f, ensure_ascii=False, indent=4)
