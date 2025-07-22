
import os
OS = my_variable_value = os.getenv('OS_INTERFEROMETER_FRINGE_ANALYSIS')

if OS == "WINDOWS":
    import msvcrt
    
    def getKey():
        return getKey_WINDOWS()

if OS == "LINUX":
    import sys, tty, termios
    import select
    
    def getKey():
        return getKey_UNIX()
    
    
    
import numpy as np

#SERIAL_PORT_NAME = 'COM3'
SERIAL_PORT_NAME = '/dev/ttyUSB0'

BLACK_IMAGE_LEVEL = 10

#states
WAITING_MOBILE_MIRROR_PHOTO = 1
WAITING_FIXED_MIRROR_PHOTO = 2

#constants
HIDE = "hide"
SHOW = "show"

#photo taken size
WIDTH = 1280
HEIGHT = 800


#photo resized size
RESIZED_WIDTH = 320
RESIZED_HEIGHT = 200


def getKey_WINDOWS():
    if msvcrt.kbhit():  # Check if a keypress is available
        return msvcrt.getch().decode() # Read the character
    return None
    
def getKey_UNIX():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)  # Set terminal to cbreak mode (non-canonical)
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            print('getKey_UNIX 1')
            return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return None
    
def isPressedKey(key):
    keyReaded = getKey()
    if keyReaded: print(keyReaded)
    if keyReaded == key:
        return True
    return False
    
    
    
def shouldCloseThisApp():
    return isPressedKey('q')
    
def shouldPauseThisApp():
    print('should pause check')
    return isPressedKey('p')
    
def toY8array(Y16array, width, height):
    Y16array = Y16array.reshape((width*height, 2))
    Y8array = np.ascontiguousarray(Y16array[:, 1])                     #avoid unnecesary zeroes, halve the size
    Y8array = Y8array.reshape((height, width))
    return Y8array
    