import cv2
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from skimage import exposure
import sys

archivoProcesar = sys.argv[1]
print('file:',archivoProcesar)
img = cv2.imread(archivoProcesar, cv2.IMREAD_GRAYSCALE)
print(img)

img2 = exposure.rescale_intensity(img)
print(img2)
cv2.imshow("Image", img2)

cv2.waitKey(0)
cv2.destroyAllWindows()


