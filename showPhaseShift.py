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
if len(sys.argv) > 2:
    inputFolder = input_file
    input_file = None

def getFilePhase(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        segmentsJSON = json.load(f)

    processed = 0
    segments = segmentsJSON["segments"]
    allPhases = []
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
        
        samples = segment["samples"]
        periods = []
        firstSegmentTimestamp = None
        for sample in samples:
            deltaPhase = None
            if "hz" not in sample: continue
            hz = sample["hz"]
            if "deltaPhase" not in sample or sample["deltaPhase"] is None: continue
            deltaPhase = sample["deltaPhase"]
            if deltaPhase is None: continue
            if not firstSegmentTimestamp:
                firstSegmentTimestamp = sample["timestamp"]
                print("First timestamp: ", firstSegmentTimestamp)
                
            mobilePhase = sample["mobilePhase"]
            fixedPhase = sample["fixedPhase"]
            segmentMobilePhase.append(mobilePhase)
            segmentFixedPhase.append(fixedPhase)
            allPhases.append(deltaPhase)
            allTimestamps.append(float(sample["timestamp"]))
            processed+=1
            segmentHz.append(hz)
            segmentPhases.append(deltaPhase)
            segmentTimestamps.append(float(sample["timestamp"]))
            if processed % 200 == 0:
                
                if True:
                    plt.plot(segmentTimestamps, segmentFixedPhase, '.', label='Fixed Mirror')
                    plt.plot(segmentTimestamps, segmentMobilePhase, '.', label='Mobile Mirror')
                    plt.legend()
                    plt.show()
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
                    segmentHzModified = [x / 3 - 2 for x in segmentHz]
                    plt.plot(segmentTimestamps, segmentPhases, '.')
                    plt.plot(segmentTimestamps, segmentHzModified, '.')
                    plt.show()
                segmentHz = []
                segmentPhases = []
                segmentTimestamps = []
                segmentFixedPhase = []
                segmentMobilePhase = []
                firstSegmentTimestamp = None
        #if processed>500:break
    
        #histogram.showHistogram(segmentPhases, label= "Phases", show = False)
    #plt.show()

    #histogram.showHistogram(phases, "Phases")
    return allPhases, allHz, allTimestamps

if input_file:
    allPhases, allHz, allTimestamps = getFilePhase(input_file)
    exit()
    #print(allPhases)
    N = 100
    print("N: ", N)
    phaseShiftEvolution = np.convolve(allPhases, np.ones(N)/N, mode='valid')
    range1 = allTimestamps[:-N+1]
    print("len(range1): ", len(range1))
    #plt.plot(range1, phaseShiftEvolution, '.')
    inicio = 0 #allTimestamps.index(1759500426.971824)
    #final = allTimestamps.index(1759503780.421168)
    #final = inicio + 200
    final = len(allTimestamps)
    plt.plot(allTimestamps[inicio:final], allPhases[inicio:final], '.')
    # m, b = np.polyfit(allTimestamps, allPhases, 1)
    # print("m: ", m, "  -  b: ",b)
    plt.show()
    #histogram.showHistogram(phases, label = "12345678", histtype='bar', stacked= True)


