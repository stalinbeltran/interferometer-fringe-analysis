import math
import numpy as np

def getProcessedPhase(phase, amplitude):
    factor = abs(math.trunc(phase/(2*np.pi)))
    if phase <= -2*np.pi: phase += (factor)*2*np.pi         #avoid lower than -2pi
    elif phase >= 2*np.pi: phase -= factor*2*np.pi     #avoid greater than 2pi
    if amplitude < 0:                               #fix negative amplitude (every comparison is amplitude positive
        phase -= np.pi
        amplitude *=-1                              #now amplitude is positive
    
    # if phase > np.pi: phase -=2*np.pi
    # if phase < -np.pi: phase +=2*np.pi
    return phase, amplitude
    
def getPositivePhaseDegrees(phase):
    if phase < 0: return phase+360
    return phase