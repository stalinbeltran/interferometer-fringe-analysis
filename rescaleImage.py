#D:\Stalin\Desarrollo\interferometer-fringe-analysis>python rescaleImage.py ./images/alineacion666.png

import cv2
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from skimage import exposure
import sys
import os

archivoProcesar = sys.argv[1]
print('file:',archivoProcesar)
img = cv2.imread(archivoProcesar, cv2.IMREAD_GRAYSCALE)
print('img: ', img)

img2 = exposure.rescale_intensity(img)
print('img2: ', img2)
filename, file_extension = os.path.splitext(archivoProcesar)
cv2.imwrite(filename + "_rescaled" + file_extension, img2)
cv2.imshow("Image", img2)

cv2.waitKey(0)
cv2.destroyAllWindows()


