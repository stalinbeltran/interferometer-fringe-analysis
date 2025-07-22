
#import msvcrt
import sys, tty, termios
import select

#SERIAL_PORT_NAME = 'COM3'
SERIAL_PORT_NAME = '/dev/ttyUSB0'

#states
WAITING_MOBILE_MIRROR_PHOTO = 1
WAITING_FIXED_MIRROR_PHOTO = 2

#constants
HIDE = "hide"
SHOW = "show"


def getKey():
    return getKey_UNIX()

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
            return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return None
    
def shouldCloseThisApp():
    key = getKey()
    if key == 'q':
        print("salir")
        return True
    return False
    