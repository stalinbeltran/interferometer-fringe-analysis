
import msvcrt

#states
WAITING_MOBILE_MIRROR_PHOTO = 1
WAITING_FIXED_MIRROR_PHOTO = 2

#constants
HIDE = "hide"
SHOW = "show"


def getKey():
    if msvcrt.kbhit():  # Check if a keypress is available
        return msvcrt.getch().decode() # Read the character
    return None