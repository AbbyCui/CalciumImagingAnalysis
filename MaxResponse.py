'''
Calculate the max response of each ROI to each stimulus
INPUT: stimulus.csv and smoothed data in csv files, and badROIs (optional),
OUTPUT: csv with ROI names as horizontal headers. Contains max response of each ROI to each stimuli (only if an event occured)
    without an event during the stimulus window, the maxResponse would be 0. the lower half of the sheet contains "Res_" + stimulus 
    names as headers, and "0" indicating no response or "1" indicating a response
'''


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
Starts,Ends = Utility.extractEvent(debug, ROIdata, threshold, baselineStart,baselineEnd)
ROInum = ROIdata.shape[1]-1

#initialize maxResponse with the same number of rows as stimulus, 
# but the number of columns as number of ROI
maxResponse = np.zeros((stimNum,ROInum))
ROInames = ROIdata[0,...] #including [0,0]
StimulusNames = stimulus[...,0]
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

#duplicate maxResponse, then change all values >0 to 1 to indicate responder
responders = np.copy(maxResponse)
responders[responders > 0] = 1 

# add back the ROI names and stimulus names to maxResponse
if debug:
    print("shape of stimulusNames:",StimulusNames.shape, "shape of maxResponse:",maxResponse.shape)
maxResponse = np.hstack((StimulusNames[:, None],maxResponse)) #use [:,None] to change 1d array to 2d

if debug:
    print("shape of ROInames:",ROInames.shape,"shape of maxResponse:",maxResponse)
maxResponse = np.vstack((ROInames[None,:],maxResponse))

#make headers for responders for each stimulus (e.g. "Res_3nM GRP")
Res_StimulusNames = np.array(["Res_"]*len(StimulusNames))
Res_StimulusNames = np.core.defchararray.add(Res_StimulusNames, StimulusNames)
if debug:
    print("Res_StimulusNames =",Res_StimulusNames)
#add stim names 
responders = np.hstack((Res_StimulusNames[:, None],responders))
#put responders on the b0ottom of maxResponse
maxResponse = np.vstack((maxResponse,responders))


np.savetxt(pathToOutputData + splPrefix + "MaxResponse.csv", maxResponse, delimiter=',', comments='', fmt='%s')