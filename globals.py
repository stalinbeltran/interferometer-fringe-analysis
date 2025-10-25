
import os
OS = my_variable_value = os.getenv('OS_INTERFEROMETER_FRINGE_ANALYSIS')

BLACK_IMAGE_LEVEL = 30
EQUALIZED_IMAGE_WIDTH = 50


CAMERA_SENSOR_MODE = 0# 0 o 2


#photo taken size
if CAMERA_SENSOR_MODE == 0:
    WIDTH = 640
    HEIGHT = 400
    
if CAMERA_SENSOR_MODE == 2:
    WIDTH = 1280
    HEIGHT = 800
    
    

'''

WIDTH = 640
HEIGHT = 400

WIDTH = 1280
HEIGHT = 800
'''

#photo resized size
RESIZED_WIDTH = WIDTH
RESIZED_HEIGHT = HEIGHT



#STATUS
BLACK_IMAGE = 0
FIRST_FIXED_MIRROR = 1
MOBILE_MIRROR = 2
SECOND_FIXED_MIRROR = 3
WAIT_BLACK_IMAGE = 4



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
    if mean > BLACK_IMAGE_LEVEL:
        return False
    return True


def filterFFT(signal, cutoff = 25):
    fourier_transform = np.fft.fft(signal)
    fourier_transform[cutoff:-cutoff] = 0       #low pass filter
    reconstructed_signalComplex = np.fft.ifft(fourier_transform) #Inverse Fourier Transform
    reconstructed_signal = []
    for p in reconstructed_signalComplex:
        reconstructed_signal.append(p.real)
    return reconstructed_signal
    

def pointsAverage(lastPoints):
    average = sum(lastPoints) / len(lastPoints)
    return average
    
    
def getAroundPoints(sampleIndex, N_lastPoints, samples, phaseKey):
    if sampleIndex > N_lastPoints:
        beginning = sampleIndex-N_lastPoints
    else:
        beginning = 0
    end = beginning + N_lastPoints
    aroundPoints = [ x[phaseKey] for x in samples[beginning:end] ]
    return aroundPoints
    
def getAroundPoints2(sampleIndex, N_lastPoints, samples):
    if sampleIndex > N_lastPoints:
        beginning = sampleIndex-N_lastPoints
    else:
        beginning = 0
    end = beginning + N_lastPoints
    aroundPoints = [ x for x in samples[beginning:end] ]
    return aroundPoints
    
    
def getFileName(filepath):
    parts = filepath.split("\\")
    size = len(parts)
    path = ""
    for i in range(0, size-1):
        path += parts[i]
    filename = parts[-1]
    return path, filename
    

def softenSignal(data, N_points):
    kernel = np.ones(N_points) / N_points           #averaging kernel
    convolution = np.convolve(data, kernel, mode='same')
    return convolution.tolist()
    

def getData(fixedPhase, mobilePhase, hz, timestamp, deltaPhase):
    return {
        "fixedPhase" : fixedPhase,
        "mobilePhase" : mobilePhase,
        "deltaPhase" : deltaPhase,
        "hz" : hz,
        "timestamp" : timestamp
    }


def applyFunctionToArray(array, func, funcParams):
    if funcParams:
        size = len(array)
        for i in range(size):
            array[i] = func(array[i], funcParams)
    else:
        size = len(array)
        for i in range(size):
            array[i] = func(array[i])

def getPromptOptionalParameter(n, funcs = None):
    if len(sys.argv) <= n: return None
    params = (sys.argv[n])
    if params is None or funcs is None:
        return params
    if not isinstance(funcs, list):
        params = funcs(params)
        return
    #deal with array of functions
    for f in funcs:
        func = f["func"]
        funcParams = None
        if "funcParams" in f:
            funcParams = f["funcParams"]
        if func:
            if not isinstance(params, list):
                if funcParams:
                    params = func(params, funcParams)
                else:
                    params = func(params)
                continue
            applyFunctionToArray(params, func, funcParams)
    return params
    
def split(s, params):
    return s.split(params[0])


def getMaximumPeriod():
    global WIDTH
    maximumPeriod = WIDTH/4                 #do not take photos with less than 4 fringes
    return maximumPeriod
    
    
    