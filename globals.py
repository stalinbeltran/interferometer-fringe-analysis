
import os
OS = my_variable_value = os.getenv('OS_INTERFEROMETER_FRINGE_ANALYSIS')

BLACK_IMAGE_LEVEL = 10



import threading
import queue
import sys

input_queue = queue.Queue()

def read_stdin_thread(q):
    while True:
        line = sys.stdin.readline().strip()
        q.put(line)

# Start the reading thread
reader_thread = threading.Thread(target=read_stdin_thread, args=(input_queue,), daemon=True)
reader_thread.start()

def getKey():
    user_input = None
    try:
        # Try to get input from the queue without blocking
        user_input = input_queue.get_nowait()
        return user_input
        #if user_input:
        #    print(f"Processed: {user_input}")
    except queue.Empty:
        # No input available, perform other tasks
        pass
    return user_input

    
    
    
import numpy as np

#SERIAL_PORT_NAME = 'COM3'
SERIAL_PORT_NAME = '/dev/ttyUSB0'

#states
WAITING_MOBILE_MIRROR_PHOTO = 1
WAITING_FIXED_MIRROR_PHOTO = 2

#redis subscriptions
FOTO_TAKEN_RESIZED = 'phototakenresized'
FOTO_TAKEN = 'phototaken'


#constants
HIDE = "hide"
SHOW = "show"

#photo taken size
WIDTH = 640
HEIGHT = 400


#photo resized size
RESIZED_WIDTH = WIDTH
RESIZED_HEIGHT = HEIGHT


    
def isPressedKey(key):
    keyReaded = getKey()
    if keyReaded == key:
        return True
    return False
    
    
    
def shouldCloseThisApp(key):
    return key == 'q'
    
def shouldPauseThisApp(key):
    return key == 'p'

    
def toY8array(Y16array, width, height):
    Y16array = Y16array.reshape((width*height, 2))
    Y8array = np.ascontiguousarray(Y16array[:, 1])                     #avoid unnecesary zeroes, halve the size
    Y8array = Y8array.reshape((height, width))
    return Y8array
    

def isBlackImage(img):
    mean = np.mean(img)
    if mean > globals.BLACK_IMAGE_LEVEL:
        print(mean)
        return False
    return True
