#python3 ./controller.py
import globals
import time
import numpy as np
from publisher import Publisher
import cv2 as cv2

def waitPhoto(message):
    value = message['data']
    if value == 'qc': exit()
    if isinstance(value, int) or len(value) < 200: return None
    imageBase64 = value
    photo = pub.getImage(imageBase64, 640, 480)
    return photo

pub = Publisher()
pub.init()
pub.subscribe(globals.FOTO_TAKEN)
pub.publish("commandShutter", globals.HIDE)          #hide fixed retroreflector
state = globals.WAITING_MOBILE_MIRROR_PHOTO

mobileMirrorPhoto = None
fixedMirrorPhoto = None

while True:
    key = globals.getKey()
    if globals.shouldCloseThisApp(key): break
    
    message = pub.get_message()
    if message is None: continue
    photo = message['data']
    if photo is None: continue
    match state:
        case globals.WAITING_MOBILE_MIRROR_PHOTO:
            mobileMirrorPhoto = photo
            pub.publish("commandShutter", globals.SHOW)          #hide fixed retroreflector
            state = globals.WAITING_FIXED_MIRROR_PHOTO
        case globals.WAITING_FIXED_MIRROR_PHOTO:
            fixedMirrorPhoto = photo
            data = {
                "mobileMirrorPhoto": mobileMirrorPhoto,
                "fixedMirrorPhoto": fixedMirrorPhoto,
            }
            dataString = json.dumps(data)
            #save data
            pub.publish("saveDataPair", dataString)
            pub.publish("commandShutter", globals.HIDE)          #hide fixed retroreflector
            state = globals.WAITING_MOBILE_MIRROR_PHOTO
            

    break                               #debugging
    
#cv2.destroyAllWindows()
