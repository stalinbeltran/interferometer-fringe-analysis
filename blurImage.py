 #img = blurImage(img)

import numpy as np
import cv2

def blurImage(img, dim = 25):
    product = dim*dim
    kernel = np.ones((dim,dim),np.float32)/product
    imgBlurred = cv2.filter2D(img,-1,kernel)
    return imgBlurred