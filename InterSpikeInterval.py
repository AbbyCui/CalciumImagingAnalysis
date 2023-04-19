"""
import libraries
"""
from pandas import array
import Utility_working as Utility #custom-made utility file, contains lengthy functions
from gettext import install
import numpy as np
import matplotlib.pyplot as plt
import csv
import plotly.express as px
from scipy import signal
import sys
import matplotlib.pyplot as plt
from constant import *

##if want to customize some varibles, can enter them in terminal (see Unit Test.txt for example)
try:
    planeNumber = sys.argv[1]
    stimStart = int(sys.argv[2])
    stimEnd = int(sys.argv[3])

    print("Starting InterspikeInterval with variables from terminal input: planeNumber:",planeNumber,"stimStart:",stimStart,"stimEnd:",stimEnd)

    splPrefix = expNumber + "_" + planeNumber + "_"
    prefix = expNumber + "_" + planeNumber+ " _frm" + str(stimStart) + "-"+ str(stimEnd)+ "_" 
except:
    print("Starting InterSpikeInterval with variables in constant.py")

# if have a csv. file with ROIs to remove, it will be included in plotting
try:
    AllROIsToRemove = np.loadtxt(pathToData +"BadROIs.csv",delimiter=',',dtype=str)
    ROIsToRemove=Utility.getROIsToRemove(debug, AllROIsToRemove, plane = planeNumber)
except:
    ROIsToRemove = []
    print("plotting all ROIs")

#import smoothed data
data = np.loadtxt(pathToOutputData + splPrefix +"Smoothed.csv",delimiter=',',dtype=str)
AllThresholds = np.loadtxt(pathToOutputData + prefix +"AllThresholds.csv",delimiter=',',dtype=str)
stimulus = np.loadtxt(pathToData +"Stimulus.csv",delimiter=',',dtype=str,usecols = (0,1,2,3))
ROIdata = Utility.extractData(debug, data, ROIs, ROIsToRemove, stimStart = stimStart, stimEnd = stimEnd) 

Starts,Ends,frAboveThreshold,MidSpike = Utility.extractEvent(debug, ROIdata, stimulus,AllThresholds)
eventNumber = Utility.eventCounter(debug, Starts)
ISI = Utility.ISI(debug, ROIdata, Starts)
#eventAmp = Utility.getEventAmp(debug, ROIdata, Starts, Ends)

Starts= Starts.astype('object').astype('str')
Ends = Ends.astype('object').astype('str')
frAboveThreshold = frAboveThreshold.astype('object').astype('str')

Starts[0,1:]= ROIdata[0,1:]
Ends[0,1:] = ROIdata[0,1:]
frAboveThreshold[0,1:] = ROIdata[0,1:]


np.savetxt(pathToOutputData + prefix + "Starts.csv", Starts, delimiter=',', comments='', fmt='%s')
np.savetxt(pathToOutputData + prefix + "Ends.csv", Ends, delimiter=',', comments='', fmt='%s')
np.savetxt(pathToOutputData + expNumber + "_" + planeNumber + "_" + "AllThresholds.csv", AllThresholds, delimiter=',', comments='', fmt='%s')
np.savetxt(pathToOutputData + prefix + "EventNumber.csv", eventNumber, delimiter=',', comments='', fmt='%s')
np.savetxt(pathToOutputData + prefix + "ROINames.csv", ROIdata[0,...], delimiter=',', comments='', fmt='%s')
np.savetxt(pathToOutputData + prefix + "ISI.csv", ISI, delimiter=',', comments='', fmt='%s')
np.savetxt(pathToOutputData + prefix + "Frames_above_Threshold.csv", frAboveThreshold, delimiter=',', comments='', fmt='%s')
np.savetxt(pathToOutputData + prefix + "Spike_Median.csv", MidSpike, delimiter=',', comments='', fmt='%s')
#np.savetxt(pathToOutputData + prefix + "EventAmp.csv", eventAmp, delimiter=',', comments='', fmt='%s')