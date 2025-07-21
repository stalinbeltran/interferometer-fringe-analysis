#python3 ./controller.py
import constants
import time
import numpy as np
from publisher import Publisher
import cv2 as cv2
import msvcrt

def getKey():
    if msvcrt.kbhit():  # Check if a keypress is available
        return msvcrt.getch().decode() # Read the character
    return None
    
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
pub.publish("commandShutter", constants.HIDE)          #hide fixed retroreflector
state = constants.WAITING_MOBILE_MIRROR_PHOTO

mobileMirrorPhoto = None
fixedMirrorPhoto = None

while True:
    key = getKey()
    if key: print(key)
    if key == 'q':
        print("salir")
        break
    
    message = pub.get_message()
    if message is None: continue
    photo = waitPhoto(message)
    if photo is None: continue
    match state:
        case constants.WAITING_MOBILE_MIRROR_PHOTO:
            mobileMirrorPhoto = photo
            pub.publish("commandShutter", constants.SHOW)          #hide fixed retroreflector
            state = constants.WAITING_FIXED_MIRROR_PHOTO
        case constants.WAITING_FIXED_MIRROR_PHOTO:
            fixedMirrorPhoto = photo
            data = {
                "mobileMirrorPhoto": pub.imageToString(mobileMirrorPhoto),
                "fixedMirrorPhoto": pub.imageToString(fixedMirrorPhoto),
            }
            dataString = json.dumps(data)
            #save data
            pub.publish("saveDataPair", dataString)
            pub.publish("commandShutter", constants.HIDE)          #hide fixed retroreflector
            state = constants.WAITING_MOBILE_MIRROR_PHOTO
            

    break                               #debugging
    
#cv2.destroyAllWindows()