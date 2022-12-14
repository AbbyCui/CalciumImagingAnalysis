'''

'''

import Utility_working as Utility #custom-made utility file, contains lengthy functions
from constant import *
from gettext import install
import numpy as np
import matplotlib.pyplot as plt
import csv
import plotly.express as px
import matplotlib.pyplot as plt
import sys
import os

#TODO: add event/stimulus shading

# if want to customize some varibles, can enter them in terminal (see Unit Test.txt for example)
try:
    planeNumber = sys.argv[1]
    stimStart = int(sys.argv[2])
    stimEnd = int(sys.argv[3])

    splPrefix = expNumber + "_" + planeNumber + "_"
    prefix = expNumber + "_" + planeNumber+ " _frm" + str(stimStart) + "-"+ str(stimEnd)+ "_" 
    pathToRaw = "../"+parentFolder+"/Data/"+parentFolder+"_"+planeNumber+"_"
except:
    print("Starting Plot.py with variables in constant.py")

# if have a csv. file with ROIs to remove, it will be included in plotting
try:
    AllROIsToRemove = np.loadtxt(pathToData +"BadROIs.csv",delimiter=',',dtype=str)
except:
    AllROIsToRemove = np.zeros((3, 6))
    print("plotting all ROIs")





# if Figure folder do not exist, create one
if not os.path.exists(pathToFigure[:-1]):
    os.makedirs(pathToFigure[:-1])

# import raw data, normalized data, and smoothed data
splPATH = pathToOutputData + splPrefix
data, TotalTime, TotalROIs = Utility.importDataFile(debug, pathToRaw + "Results.csv") #import and format data
normalized = np.loadtxt(splPATH +"Normalized.csv",delimiter=',',dtype=str)
smoothed = np.loadtxt(splPATH +"Smoothed.csv",delimiter=',',dtype=str)
stimulus = np.loadtxt(pathToData +"Stimulus.csv",delimiter=',',dtype=str)
AllThresholds = np.loadtxt(pathToOutputData + prefix +"AllThresholds.csv",delimiter=',',dtype=str)

TotalTime = smoothed.shape[0]
TotalROIs = smoothed.shape[1]

if str(ROIs) == "all":
    # arrange(x,y) -> [x,y), so end has to be TotalROIs+1 to include the last ROI
    ROIs = np.arange(1,TotalROIs+1)
if str(stimEnd) == "all" or str(stimStart) == "all":
    stimStart = 1
    stimEnd = TotalTime
elif stimEnd > TotalTime:
    stimEnd = TotalTime

# remove unwanted ROIs, trim to only a time window of interest
ROIsToRemove=Utility.getROIsToRemove(debug, AllROIsToRemove, plane = planeNumber)

ROIdata = Utility.extractData(debug, data, ROIs, stimStart = stimStart, stimEnd = stimEnd) 
ROInormalized = Utility.extractData(debug, normalized, ROIs, stimStart = stimStart, stimEnd = stimEnd)
ROIsmoothed = Utility.extractData(debug, smoothed, ROIs, stimStart = stimStart, stimEnd = stimEnd)
ROIs = ROIsmoothed[0,1:]

# will generate 3 panels: raw data, normallized, and smoothed data from top to bottom
# range(x,y) -> [x,y), so end has to be len(ROI)+1 to include the last ROI
for i in range(1,len(ROIs)+1):
    ROI = str(ROIs[i-1])[4:]

    rawROIdata = ROIdata[1:,i].astype(float, copy=False)
    rawNormalized = ROInormalized[1:,i].astype(float,copy=False)
    rawSmoothed = ROIsmoothed[1:,i].astype(float,copy=False)
    try:
        thisThreshold = AllThresholds[i]
    except:
        thisThreshold = 0.5
    if debug:
        print("ROI =",ROI)
        print("i =",i)
        print("rawROIdata has shape:",rawROIdata.shape)

    fig = plt.figure()
   
    plt.subplot(3,1,1)
    plt.plot(range(stimStart,stimEnd,1),rawROIdata)
    plt.title('ROI'+ROI)

    plt.subplot(3,1,2)
    plt.plot(range(stimStart,stimEnd,1),rawNormalized)
    
    plt.subplot(3,1,3)
    plt.plot(range(stimStart,stimEnd,1),rawSmoothed)

    #draw a line at y = 0.5 for threshold
    plt.axhline(y=float(thisThreshold), color='r', linestyle='-')

    if debug:
        print("plotting with threshold =",thisThreshold)
    plt.axvspan(2300, 13100, alpha=0.3, color='blue')

    plt.savefig(pathToFigure+ expNumber+"_" + planeNumber + "_ROI" + ROI + "_Frm"+str(stimStart) + "-" + str(stimEnd) + ".png")
    plt.grid()
    plt.show()
    plt.close("all")