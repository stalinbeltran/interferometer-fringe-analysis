
import numpy as np
import cv2
import sys

img0 = cv2.imread("./videos/fringes_9/frames/fringes_9-400-.png", cv2.IMREAD_GRAYSCALE)
# cv2.imshow('', img0)
# cv2.waitKey()

img1 = cv2.imread("./videos/fringes_9/frames/fringes_9-369-.png", cv2.IMREAD_GRAYSCALE)
# cv2.imshow('', img1)
# cv2.waitKey()


img0_norm = img0/np.sum(img0)
img1_norm = img1/np.sum(img1)

print("np.sum(img0): ", np.sum(img0))
print("np.sum(img1): ", np.sum(img1))
print(img0_norm)
print(img1_norm)

similaritiy = np.sum(np.sqrt(img0_norm*img0_norm))

print("similaritiy: ", similaritiy)


cv2.destroyAllWindows()