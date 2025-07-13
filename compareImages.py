
import cv2
import sys

img = cv2.imread("./videos/fringes_9/frames/fringes_9-400-.png", cv2.IMREAD_GRAYSCALE)
cv2.imshow('', img)
cv2.waitKey()
cv2.destroyAllWindows()
sys.exit()

import numpy as np

picture1 = np.random.rand(100,100)
picture2 = np.random.rand(100,100)
picture1_norm = picture1/np.sqrt(np.sum(picture1**2))
picture2_norm = picture2/np.sqrt(np.sum(picture2**2))