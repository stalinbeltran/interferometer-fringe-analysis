import cv2
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import sys

archivoProcesar = sys.argv[1]
print('file:',archivoProcesar)
img = cv2.imread(archivoProcesar, cv2.IMREAD_GRAYSCALE)

fig = plt.figure(tight_layout=True)
gs = gridspec.GridSpec(1, 2)
ax1 = fig.add_subplot(gs[0, 0])
ax1.imshow(img, cmap='gray')
plt.show()

cv2.imshow("Image", img)

cv2.waitKey(0)
cv2.destroyAllWindows()


