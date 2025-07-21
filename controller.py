#python3 ./controller.py
import controller
import time
import numpy as np
from publisher import Publisher
import cv2 as cv2
import curses

#states
WAITING_MOBILEMIRROR_PHOTO = 1
WAITING_FIXEDMIRROR_PHOTO = 2
HIDE = "hide"
SHOW = "show"

stdscr = curses.initscr()
stdscr.nodelay(True)
#curses.noecho()  # Don't echo keypresses to the screen
curses.cbreak()  # React to keys instantly, without waiting for Enter
#stdscr.keypad(True) # Enable special keys like arrow keys

# stdscr.addstr("Press any key (or 'q' to quit): ")
# stdscr.refresh()


def waitPhoto(message):
    try:
        value = message['data']
    except:
        return None
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

mobileMirrorPhoto = None
fixedMirrorPhoto = None

while True:
    key = stdscr.getch()
    if key == ord('q'):
        print("salir")
        break
    else:
        print('.')
    message = pub.get_message()
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