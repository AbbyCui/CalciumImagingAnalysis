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

    print("Starting InterspikeInterval with variables from terminal input: planeNumber:",planeNumber)

    splPrefix = expNumber + "_" + planeNumber + "_"
    prefix = expNumber + "_" + planeNumber+ " _frm" + str(stimStart) + "-"+ str(stimEnd)+ "_" 
except:
    print("Starting InterSpikeInterval with variables in constant.py")

# if have a csv. file with ROIs to remove, it will be included in plotting
try:
    AllROIsToRemove = np.loadtxt(pathToData +"BadROIs.csv",delimiter=',',dtype=str)
    ROIsToRemove=Utility.getROIsToRemove(debug, AllROIsToRemove, plane = planeNumber)
except:
    ROIsToRemove = np.zeros((1,1))
    print("plotting all ROIs")

#import smoothed data and stimulus files
data = np.loadtxt(pathToOutputData + splPrefix +"Smoothed.csv",delimiter=',',dtype=str)
stimulus = np.loadtxt(pathToData +"Stimulus.csv",delimiter=',',dtype=str)
stimNum = stimulus.shape[0]
#extract only the desired ROIs (extract all frames)

ROIdata = Utility.extractData(debug, data, ROIs, ROIsToRemove, stimStart = 1, stimEnd = "all") 
Starts,Ends,spikesInOnes = Utility.extractEvent(debug, ROIdata, threshold, baselineStart,baselineEnd)
ROInum = ROIdata.shape[1]-1

#initialize maxResponse with the same number of rows as stimulus, 
# but the number of columns as number of ROI
maxResponse = np.zeros((stimNum,ROInum))
ROInames = np.array(ROIdata[0,...]) #including [0,0]
StimulusNames = np.array(stimulus[...,0])
if debug:
    print("maxResponse initially:",maxResponse)
    print("ROinames =",ROInames,"StimulusNames =",StimulusNames)

# for each stimulus (each row), get maxResponse of each ROI
for i in range(0,stimulus.shape[0]):
    stimName = stimulus[i,0]
    stimStart = int(float(stimulus[i,1]))
    stimEnd = int(float(stimulus[i,2]))
    stimNum = stimulus.shape[0]
    if debug:
        print("for stimulus:",stimName ,", stimStart =",stimStart,"stimEnd =",stimEnd)
    thisMaxResponse = Utility.getMaxResponse(debug, ROIdata, stimStart, stimEnd, Starts, Ends)
    maxResponse[i,...] = thisMaxResponse.astype(str)
    if debug:
        print("shape of thisMaxResponse is",thisMaxResponse.shape)
        print("thisMaxResponse:",thisMaxResponse.astype(str))

# add back the ROI names and stimulus names
if debug:
    print("shape of stimulusNames:",StimulusNames.shape, "shape of maxResponse:",maxResponse.shape)
maxResponse = np.hstack((StimulusNames[:, None],maxResponse)) #use [:,None] to change 1d array to 2d
if debug:
    print("shape of ROInames:",ROInames.shape,"shape of maxResponse:",maxResponse)
maxResponse = np.vstack((ROInames[None,:],maxResponse))  

np.savetxt(pathToOutputData + splPrefix + "MaxResponse.csv", maxResponse, delimiter=',', comments='', fmt='%s')