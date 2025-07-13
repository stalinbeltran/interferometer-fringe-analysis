import numpy as np
fd = open('./images/9281-raw10toraw8-test.raw', 'rb')
rows = 800
cols = 1280
f = np.fromfile(fd, dtype=np.uint8,count=rows*cols)
im = f.reshape((rows, cols)) #notice row, column format
fd.close()
#This makes a numpy array that can be directly manipulated by OpenCV

import cv2
cv2.imshow('', im)
cv2.waitKey()
cv2.destroyAllWindows()