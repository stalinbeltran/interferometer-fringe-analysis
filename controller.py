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

print('before create Publisher')
pub = Publisher()
pub.init()
print('pub:')
print(pub)
pub.subscribe('photovalidated')
pub.publish("commandShutter", globals.HIDE)          #hide fixed retroreflector
state = globals.WAITING_MOBILE_MIRROR_PHOTO

mobileMirrorPhoto = None
fixedMirrorPhoto = None

while True:
    key = globals.getKey()
    if key: print(key)
    if key == 'q':
        print("salir")
        break
    
    message = pub.get_message()
    if message is None: continue
    photo = waitPhoto(message)
    if photo is None: continue
    match state:
        case globals.WAITING_MOBILE_MIRROR_PHOTO:
            mobileMirrorPhoto = photo
            pub.publish("commandShutter", globals.SHOW)          #hide fixed retroreflector
            state = globals.WAITING_FIXED_MIRROR_PHOTO
        case globals.WAITING_FIXED_MIRROR_PHOTO:
            fixedMirrorPhoto = photo
            data = {
                "mobileMirrorPhoto": pub.imageToString(mobileMirrorPhoto),
                "fixedMirrorPhoto": pub.imageToString(fixedMirrorPhoto),
            }
            dataString = json.dumps(data)
            #save data
            pub.publish("saveDataPair", dataString)
            pub.publish("commandShutter", globals.HIDE)          #hide fixed retroreflector
            state = globals.WAITING_MOBILE_MIRROR_PHOTO
            

    break                               #debugging
    
#cv2.destroyAllWindows()