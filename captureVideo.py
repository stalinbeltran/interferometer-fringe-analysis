#python3 captureVideo.py 0

import globals
import numpy as np
import cv2 as cv2
from publisher import Publisher
import time
import redis
from picamera2 import Picamera2
from gpiozero import Button, DigitalInputDevice
from signal import pause
import threading
import queue
import sys

saveImagesOnly = int(sys.argv[1]) == 1

exit1 = False
delayComparison = 0.2
photoMobile = None
photoFixed = None
imageQueue = queue.Queue()

def visibleComparison(imageQueue):
    global exit1, delayComparison, photoMobile, photoFixed, cv2
    if saveImagesOnly: return       #no comparison if save only
    
    while not exit1:
        if photoMobile is not None and photoFixed is not None:
            break
        time.sleep(delayComparison)
 
    while not exit1:
        imageQueue.put('union')
        imageQueue.put(photoMobile)
        time.sleep(delayComparison)
        imageQueue.put('union')
        imageQueue.put(photoFixed)
        time.sleep(delayComparison)


def capture(imageQueue):
    global photoFixed, photoMobile, exit1
    pub = Publisher()
    pub.init()

    picam2 = Picamera2()
    WIDTH = globals.WIDTH
    HEIGHT = globals.HEIGHT
    RESIZED_WIDTH = globals.RESIZED_WIDTH
    RESIZED_HEIGHT = globals.RESIZED_HEIGHT

    config = picam2.create_video_configuration(
        raw = picam2.sensor_modes[globals.CAMERA_SENSOR_MODE],
        buffer_count=12,
    )
    picam2.configure(config)
    #print(picam2.camera_configuration())
    #print("picam2.sensor_modes:")
    #print(picam2.sensor_modes)
    picam2.start()
    picam2.set_controls({'ExposureTime':40})

    NTESTS = 50
    tiemposCaptura = np.zeros(NTESTS)
    tiemposProceso = np.zeros(NTESTS)
    pos = 0
    tfinal = time.time()
    
    status = globals.MOBILE_MIRROR
    while not exit1:
        tinicial = time.time()
        tiemposProceso[pos] = tinicial - tfinal
        photo = picam2.capture_array('raw')                 
        tfinal = time.time()
        tiemposCaptura[pos] = tfinal-tinicial
        # pos+=1
        # if pos==NTESTS: break
                                                            #photo have 16 bits when actually 8 bits where sent by the camera
        photo = globals.toY8array(photo, WIDTH, HEIGHT)     #so we fix that    
        pub.publishImage(globals.FOTO_TAKEN, photo)         #publish original, to be used by other processes
        timestamp = f"{tfinal:.6f}"
        pub.publish(globals.FOTO_TAKEN, timestamp)             #publish timestamp
        
        

        if saveImagesOnly: continue         #prioritize image publishing
        
        if status == globals.MOBILE_MIRROR:
            status = globals.FIRST_FIXED_MIRROR
        else:
            status = globals.MOBILE_MIRROR

        if status == globals.MOBILE_MIRROR:
            imageQueue.put('mobile mirror')
            imageQueue.put(photo)
            photoMobile = photo
        if status == globals.FIRST_FIXED_MIRROR:
            imageQueue.put('fixed mirror')
            imageQueue.put(photo)
            photoFixed = photo

    # print("tiemposCaptura:")
    # print(tiemposCaptura)
    # print("tiemposProceso:")
    # print(tiemposProceso)
    
    
    picam2.stop()
        

p1 = threading.Thread(target=visibleComparison, args = (imageQueue,))
p2 = threading.Thread(target=capture, args = (imageQueue,))
p1.daemon = True
#p2.daemon = True
p1.start()
p2.start()

        
        
while True:
    key = globals.getKey()
    if globals.shouldCloseThisApp(key):
        exit1 = True
        break
    while not imageQueue.empty():
        title = imageQueue.get()
        image = imageQueue.get()
        cv2.imshow(title, image)
        cv2.waitKey(1)
    time.sleep(0.01)


cv2.destroyAllWindows()

# When everything done, release the capture

p1.join()
p2.join()
