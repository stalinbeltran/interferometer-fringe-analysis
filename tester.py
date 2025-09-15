
import globals
from publisher import Publisher
import cv2 as cv2


image_path = "images/fringes_10092025_4pm-10-.png"
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE )
cv2.imshow('aaa', img)
pub = Publisher()
pub.init()
pub.publishImage(globals.FOTO_TAKEN, img)
cv2.waitKey()
	

cv2.destroyAllWindows()