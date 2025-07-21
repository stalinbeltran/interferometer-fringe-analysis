#python3 ./controller.py
import controller
import time
import numpy as np
from publisher import Publisher
import cv2 as cv2

#states
WAITING_MOBILEMIRROR_PHOTO = 1
WAITING_FIXEDMIRROR_PHOTO = 2
HIDE = "hide".encode('ascii', 'ignore').decode('ascii')
SHOW = "show".encode('ascii', 'ignore').decode('ascii')

def waitPhoto(message):
    value = message['data']
    if value == 'qc': exit()
    if isinstance(value, int) or len(value) < 200: return None
    imageBase64 = value
    photo = pub.getImage(imageBase64, 640, 480)
    return photo




pub = Publisher()
pub.init()
print(pub)
pub.subscribe('photovalidated')
pub.publish("commandShutter", HIDE)          #hide fixed retroreflector
state = WAITING_MOBILEMIRROR_PHOTO
exit()

mobileMirrorPhoto = None
fixedMirrorPhoto = None
for message in pub.listen():
    photo = waitPhoto(message)
    if photo is None: continue
    match state:
        case controller.WAITING_MOBILEMIRROR_PHOTO:
            mobileMirrorPhoto = photo
            pub.publish("commandShutter", SHOW)          #hide fixed retroreflector
            state = WAITING_FIXEDMIRROR_PHOTO
        case controller.WAITING_FIXEDMIRROR_PHOTO:
            fixedMirrorPhoto = photo
            data = {
                "mobileMirrorPhoto": pub.imageToString(mobileMirrorPhoto),
                "fixedMirrorPhoto": pub.imageToString(fixedMirrorPhoto),
            }
            dataString = json.dumps(data)
            #save data
            pub.publish("saveDataPair", dataString)
            pub.publish("commandShutter", HIDE)          #hide fixed retroreflector
            state = WAITING_MOBILEMIRROR_PHOTO
            

    break                               #debugging
    
cv2.destroyAllWindows()