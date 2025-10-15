#python3 showPhaseShift.py D:\Stalin\FotosFranjasProyecto\friday19092025\results\40hzSegmentSamplesPhaseShift.json  

import os
import sys
import json
import cv2
import numpy as np
import histogram
import phaseProcessing
import matplotlib.pyplot as plt

input_file = (sys.argv[1])
sampleSize = int(sys.argv[2])


def showSignalConvolution(segmentTimestamps, segmentFixedPhase, segmentMobilePhase, segmentMobilePhase_soft, segmentFixedPhase_soft, segmentHz, title):
    N = 80
    kernel = np.ones(N) / N
    convolutionFixed = np.convolve(segmentFixedPhase, kernel, mode='valid')
    convolutionMobile = np.convolve(segmentMobilePhase, kernel, mode='valid')
    size = len(convolutionFixed)
    diffConv = []
    for i in range(0, size):
        diffConv.append((convolutionMobile[i] - convolutionFixed[i])*3)
    avg = sum(diffConv)/size
    
    for i in range(0, size):
        diffConv[i] = (diffConv[i]-1*avg)
        
    convLen = len(convolutionFixed)
    segmentHzModified = [x / 2 - 2.5 for x in segmentHz]
    plt.plot(segmentTimestamps, segmentFixedPhase, '-', label='Fixed')
    plt.plot(segmentTimestamps, segmentMobilePhase, '-', label='Mobile')
    plt.plot(segmentTimestamps, segmentHzModified, '.', label='Speed (Hz)')
    plt.title(title)
    plt.legend()
    plt.show()


def getFilePhase(input_file):
    global sampleSize
    with open(input_file, 'r', encoding='utf-8') as f:
        segmentsJSON = json.load(f)

    processed = 0
    segments = segmentsJSON["segments"]
    allHz = []
    allTimestamps = []
    segmentCounter = 0
    for segment in segments:
        segmentCounter+=1
        if segmentCounter < 1: continue
        segmentPhases = []
        segmentHz = []
        segmentTimestamps = []
        segmentFixedPhase = []
        segmentMobilePhase = []
        segmentFixedPhase_soft = []
        segmentMobilePhase_soft = []
        
        samples = segment["samples"]
        firstSegmentTimestamp = None
        for sample in samples:
            if "hz" not in sample: continue
            hz = sample["hz"]
            if not firstSegmentTimestamp:
                firstSegmentTimestamp = sample["timestamp"]
                print("First timestamp: ", firstSegmentTimestamp)
                
            mobilePhase = sample["mobilePhase"]
            fixedPhase = sample["fixedPhase"]
            segmentMobilePhase.append(mobilePhase)
            segmentFixedPhase.append(fixedPhase)
            allTimestamps.append(float(sample["timestamp"]))
            processed+=1
            segmentHz.append(hz)
            segmentTimestamps.append(float(sample["timestamp"]))
            
            if processed % sampleSize == 0:
                segmentHzModified = [x / 2 - 2.5 for x in segmentHz]
                if False:
                    for i in range(2, 60):
                        N = i
                        kernel = np.ones(N) / N
                        convolutionFixedPhase = np.convolve(segmentFixedPhase, kernel, mode='valid')
                        convolutionMobilePhase = np.convolve(segmentMobilePhase, kernel, mode='valid')
                        convoDifference = []
                        for index in range(0, len(convolutionFixedPhase)):
                            convoDifference.append(convolutionFixedPhase[index] - convolutionMobilePhase[index])
                        size = len(convoDifference)
                        average = sum(convoDifference)/size
                        print("N: ", N, "       average: ", average)
                            
                if True:
                    showSignalConvolution(segmentTimestamps, segmentFixedPhase, segmentMobilePhase, segmentMobilePhase_soft, segmentFixedPhase_soft,  segmentHz, title = input_file)
                if False:
                    m, b = np.polyfit(segmentHz, segmentPhases, 1)
                    print("m: ", m, "    b: ",b)
                if False:
                    plt.plot(segmentHz, segmentPhases, '.')
                    plt.show()
                if False:
                    plt.plot(segmentTimestamps, segmentPhases, '-')
                    plt.show()
                if False:
                    plt.plot(segmentTimestamps, segmentPhases, '.')
                    plt.plot(segmentTimestamps, segmentHzModified, '.')
                    plt.show()
                segmentHz = []
                segmentPhases = []
                segmentTimestamps = []
                segmentFixedPhase = []
                segmentMobilePhase = []
                segmentFixedPhase_soft = []
                segmentMobilePhase_soft = []
                firstSegmentTimestamp = None
        if processed % sampleSize > 0 and len(segmentTimestamps) > 0:
            if True:
                print("segment remaining")
                showSignalConvolution(segmentTimestamps, segmentFixedPhase, segmentMobilePhase, segmentMobilePhase_soft, segmentFixedPhase_soft,  segmentHz, title = input_file)

    return allHz, allTimestamps


N = 40
kernel = np.ones(N) / N
#print(kernel)
#exit()


if input_file:
    allHz, allTimestamps = getFilePhase(input_file)
    exit()