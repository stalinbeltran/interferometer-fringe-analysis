#python3 captureVideo.py 0

import globals
import numpy as np
import cv2 as cv2
from publisher import Publisher
import time
import redis
from picamera2 import Picamera2
from libcamera import Transform
from gpiozero import Button, DigitalInputDevice
from signal import pause
import threading
import queue
import sys


NTESTS = 0
ExposureTime = 40000 #40 #original fringes capture
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


def capture(imageQueue, cameraNumber):
    global photoFixed, photoMobile, exit1, NTESTS
    pub = Publisher()
    pub.init()

    picam2 = Picamera2(cameraNumber)
    WIDTH = globals.WIDTH
    HEIGHT = globals.HEIGHT
    RESIZED_WIDTH = globals.RESIZED_WIDTH
    RESIZED_HEIGHT = globals.RESIZED_HEIGHT

    flip = True
    if cameraNumber > 0:
        flip = False
        
    config = picam2.create_video_configuration(
        raw = picam2.sensor_modes[globals.CAMERA_SENSOR_MODE],
        buffer_count=12,
        transform = Transform(hflip = flip),
    )
    picam2.configure(config)
    #Camera information:
    #print(picam2.camera_configuration())
    #print("picam2.sensor_modes:")
    #print(picam2.sensor_modes)
    picam2.start()
    picam2.set_controls({'ExposureTime':ExposureTime})

    tiemposCaptura = np.zeros(NTESTS)
    tiemposProceso = np.zeros(NTESTS)
    pos = 0
    tfinal = time.time()
    
    cameraNumber
    if cameraNumber == 0:
        status = globals.MOBILE_MIRROR
    else:
        status = globals.FIRST_FIXED_MIRROR
    while not exit1:
        
        tinicial = time.time()
        tiempoProceso = tinicial - tfinal
        photo = picam2.capture_array('raw')                 
        tfinal = time.time()
        if NTESTS > 0:
            tiemposProceso[pos] = tiempoProceso
            tiemposCaptura[pos] = tfinal-tinicial
            pos+=1
            if pos==NTESTS: break
                                                            #photo have 16 bits when actually 8 bits where sent by the camera
        photo = globals.toY8array(photo, WIDTH, HEIGHT)     #so we fix that    
        pub.publishImage(globals.FOTO_TAKEN, photo)         #publish original, to be used by other processes
        timestamp = f"{tfinal:.6f}"
        pub.publish(globals.FOTO_TAKEN, timestamp)             #publish timestamp
        
        

        if saveImagesOnly: continue         #prioritize image publishing

        if status == globals.MOBILE_MIRROR:
            imageQueue.put('mobile mirror')
            imageQueue.put(photo)
            photoMobile = photo
        if status == globals.FIRST_FIXED_MIRROR:
            imageQueue.put('fixed mirror')
            imageQueue.put(photo)
            photoFixed = photo

    if NTESTS > 0:
        print("tiemposCaptura:")
        print(tiemposCaptura)
        print("tiemposProceso:")
        print(tiemposProceso)
    
    
    picam2.stop()
        

p1 = threading.Thread(target=visibleComparison, args = (imageQueue,))
p2 = threading.Thread(target=capture, args = (imageQueue, 0))       #capture camera 0
p3 = threading.Thread(target=capture, args = (imageQueue, 1))       #capture camera 1
p1.daemon = True

p1.start()
p2.start()
p3.start()

        
        
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
p3.join()
