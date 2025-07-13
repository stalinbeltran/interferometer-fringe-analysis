
import numpy as np
import cv2
import sys

img0 = cv2.imread("./videos/fringes_9/frames/fringes_9-400-.png", cv2.IMREAD_GRAYSCALE)
cv2.imshow('', img0)
cv2.waitKey()

img1 = cv2.imread("./videos/fringes_9/frames/fringes_9-369-.png", cv2.IMREAD_GRAYSCALE)
cv2.imshow('', img1)
cv2.waitKey()


img0_norm = img0/np.sqrt(np.sum(img0**2)) * 255
img1_norm = img1/np.sqrt(np.sum(img1**2)) * 255

cv2.imshow('', img0_norm)
cv2.waitKey()

cv2.imshow('', img1_norm)
cv2.waitKey()


cv2.destroyAllWindows()
sys.exit()