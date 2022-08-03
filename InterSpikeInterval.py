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
except:
    AllROIsToRemove = np.zeros((3, 6))
    print("plotting all ROIs")

data = np.loadtxt(pathToOutputData + splPrefix +"Smoothed.csv",delimiter=',',dtype=str)
ROIsToRemove=Utility.getROIsToRemove(debug, AllROIsToRemove, plane = planeNumber)
ROIdata = Utility.extractData(debug, data, ROIs, ROIsToRemove, stimStart = stimStart, stimEnd = stimEnd) 

Starts,Ends,spikesInOnes = Utility.extractEvent(debug, ROIdata, threshold, baselineStart,baselineEnd)
eventNumber = Utility.eventCounter(debug, Starts)
ISI = Utility.ISI(debug, ROIdata, Starts)
eventAmp = Utility.getEventAmp(debug, ROIdata, Starts, Ends)

# np.savetxt(pathToOutputData + prefix + "Starts.csv", Starts, delimiter=',', comments='', fmt='%s')
# np.savetxt(pathToOutputData + prefix + "Ends.csv", Ends, delimiter=',', comments='', fmt='%s')
np.savetxt(pathToOutputData + expNumber + "_" + planeNumber + "_" + "AllThresholds.csv", AllThresholds, delimiter=',', comments='', fmt='%s')
znp.savetxt(pathToOutputData + prefix + "EventNumber.csv", eventNumber, delimiter=',', comments='', fmt='%s')
np.savetxt(pathToOutputData + prefix + "ROINames.csv", ROIdata[0,...], delimiter=',', comments='', fmt='%s')
np.savetxt(pathToOutputData + prefix + "ISI.csv", ISI, delimiter=',', comments='', fmt='%s')
np.savetxt(pathToOutputData + prefix + "EventAmp.csv", eventAmp, delimiter=',', comments='', fmt='%s')