#python3 showPhaseShift.py D:\Stalin\FotosFranjasProyecto\friday19092025\results\40hzSegmentSamplesPhaseShift.json  

import os
import sys
import json
import cv2
import numpy as np
import histogram
import phaseProcessing

input_file = (sys.argv[1])
if len(sys.argv) > 2:
    inputFolder = input_file
    input_file = None

def getFilePhase(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        segmentsJSON = json.load(f)

    processed = 0
    segments = segmentsJSON["segments"]
    phases = []
    phasesArray = []
    for segment in segments:
        segmentPhases = []
        samples = segment["samples"]
        periods = []
        for sample in samples:
            deltaPhase = None
            deltaPhasePixels = None
            if "deltaPhase" not in sample or sample["deltaPhase"] is None: continue
            deltaPhase = sample["deltaPhase"]
            if deltaPhase is None: continue
            amplitude = 1           #only sign is used in getProcessedPhase(), so a positive value is enough
            deltaPhase, amplitude = phaseProcessing.getProcessedPhase(deltaPhase*2*np.pi, amplitude)
            deltaPhase = deltaPhase/(2*np.pi)
            phases.append(deltaPhase)
            processed+=1
            if processed >= 6000:
                processed = 0
                phasesArray.append(phases)
                phases = []
            segmentPhases.append(deltaPhase)
            # except Exception as e:
                # print(e)

        phasesArray.append(phases)
    #histogram.showHistogram(segmentPhases, "Phases", show = False)
    #histogram.showHistogram(phases, "Phases")
    return phasesArray

if input_file:
    phases = getFilePhase(input_file)
    histogram.showHistogram(phases, label = "Phases", histtype='step')
else:
    phases = []
    filenames = []
    for filename in os.listdir(inputFolder):
        absolutePath = os.path.join(inputFolder, filename)
        phases.append(getFilePhase(absolutePath))
        filenames.append(filename)
    histogram.showHistogram(phases, label = filenames, histtype='step')


