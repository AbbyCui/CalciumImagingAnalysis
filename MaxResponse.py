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
    print("Starting MaxResponse with variables from terminal input: planeNumber:",planeNumber)

    splPrefix = expNumber + "_" + planeNumber + "_"
    prefix = expNumber + "_" + planeNumber+ " _frm" + str(stimStart) + "-"+ str(stimEnd)+ "_" 
except:
    print("Starting MaxResponse with variables in constant.py")

# if have a csv. file with ROIs to remove, it will be included in plotting
try:
    AllROIsToRemove = np.loadtxt(pathToData +"BadROIs.csv",delimiter=',',dtype=str)
    print("found badROIs")
    ROIsToRemove=Utility.getROIsToRemove(debug, AllROIsToRemove, plane = planeNumber)
    print("ROIsToRemove=",ROIsToRemove)
    
except:
    ROIsToRemove = np.zeros((1,1))
    print("calculating max response for all ROIs")
    
#import smoothed data and stimulus files
data = np.loadtxt(pathToOutputData + splPrefix +"Smoothed.csv",delimiter=',',dtype=str)
print("data has dimension:",data.shape)

stimulus = np.loadtxt(pathToData +"Stimulus.csv",delimiter=',',dtype=str)
AllThresholds = np.loadtxt(pathToOutputData + splPrefix +"AllThresholds.csv",delimiter=',',dtype=str)
y,x = AllThresholds.shape
GoodThresholds = AllThresholds[0:,0] #create new threshold array in which to place the thresholds post ROI removal
ROInames = ["Frame",] #initiate new empty array
if debug:
    print("AllThresholds Shape",AllThresholds.shape)
    print("y,x",y,x)

for ROI in range(1,x): #skip the 0th row because it's the names 
    if ROI not in ROIsToRemove:
        if debug:
            print("ROI",ROI)
            print("Allthresholds",AllThresholds[0:,ROI])
        thisgoodthreshold = AllThresholds[0:,ROI] #take the ROIth column in the data sheet
        if debug:
            print(thisgoodthreshold.shape)
        GoodThresholds = np.vstack((GoodThresholds,thisgoodthreshold)) #stack on top
        ROIname = data[0,ROI]
        ROInames = np.append(ROInames,ROIname)
        if debug:
            print("ROIname",ROIname)
    else:
        if debug:
            print("ROI in ROIsToRemove",ROI)
AllThresholds = GoodThresholds.T #correct the axis of the data -> one colum for each ROI
if debugCSV:
    np.savetxt(pathToOutputData + splPrefix + "Goodthresholds.csv", AllThresholds, delimiter=',', comments='', fmt='%s')

stimNum = stimulus.shape[0]

#extract only the desired ROIs (extract all frames)
ROIdata = Utility.extractData(debug, data, ROIs, ROIsToRemove, stimStart = 1, stimEnd = "all") 
Starts,Ends = Utility.extractEventGreedy(debug, ROIdata, stimulus, AllThresholds) ##Options include either extractEventGreedy or extractEvent is more conservative in delineating events. 
EventAmp = Utility.getEventAmp(debug,ROIdata,Starts,Ends)
ROInum = ROIdata.shape[1]-1
if debugCSV:
    np.savetxt(pathToOutputData + splPrefix + "starts.csv", Starts, delimiter=',', comments='', fmt='%s')
    np.savetxt(pathToOutputData + splPrefix + "ends.csv", Ends, delimiter=',', comments='', fmt='%s')
    np.savetxt(pathToOutputData + splPrefix + "EventAmp.csv", EventAmp, delimiter=',', comments='', fmt='%s')
    np.savetxt(pathToOutputData + splPrefix + "ROInames.csv", ROInames, delimiter=',', comments='', fmt='%s')

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
    #get data from all ROI
    thisMaxResponse = Utility.getMaxResponse(debug, ROIdata, stimStart, stimEnd, Starts, Ends)
    maxResponse[i,...] = thisMaxResponse.astype(str)
    if debug:
        print("shape of thisMaxResponse is",thisMaxResponse.shape)
        print("thisMaxResponse:",thisMaxResponse.astype(str))

#initialize MaxResponseAll with the same number of rows as stimulus, 
# but the number of columns as number of ROI
if(MaxAll==True):
    MaxResponseAll = np.zeros((stimNum,ROInum))
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
        #get data from all ROI
        thisMaxResponse = Utility.getMaxResponseAll(debug, ROIdata, stimStart, stimEnd, Starts, Ends)##DO THE THING AND ASSIGN THE number to a variable
        MaxResponseAll[i,...] = thisMaxResponse.astype(str) ##append the number to the appropriate column
        if debug:
            print("shape of thisMaxResponse is",thisMaxResponse.shape)
            print("thisMaxResponse:",thisMaxResponse.astype(str))


#initialize AUC with the same number of rows as stimulus, 
# but the number of columns as number of ROI
if(DO_AUC==True):
    TotalAUC = np.zeros((stimNum,ROInum))
    Events = np.zeros((stimNum,ROInum))
    EventAmp = np.zeros((stimNum,ROInum))
    EventWidth = np.zeros((stimNum,ROInum))
    ROInames = ROIdata[0,...] #including [0,0]
    StimulusNames = stimulus[...,0]
    # for each stimulus (each row), get maxResponse of each ROI
    for i in range(0,stimulus.shape[0]):
        stimName = stimulus[i,0]
        stimStart = int(float(stimulus[i,1]))
        stimEnd = int(float(stimulus[i,2]))
        stimNum = stimulus.shape[0]
        if debug:
            print("for stimulus:",stimName ,", stimStart =",stimStart,"stimEnd =",stimEnd)
        #get data from all ROI
        AUCTotal,NumEvents,AvgAmplitude,AvgEventWidth = Utility.getAUC(debug, ROIdata, stimStart, stimEnd, Starts, Ends)##DO THE THING AND ASSIGN THE number to a variable
        TotalAUC[i,...] = AUCTotal.astype(str) ##append the number to the appropriate column
        Events[i,...] = NumEvents.astype(str) ##append the number to the appropriate column
        EventAmp[i,...] = AvgAmplitude.astype(str) ##append the number to the appropriate column
        EventWidth[i,...] = AvgEventWidth.astype(str) ##append the number to the appropriate column


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

# add back the ROI names and stimulus names to maxResponseAll
Amp_StimulusNames = np.array(["Amp_"]*len(MaxResponseAll))
Amp_StimulusNames = np.core.defchararray.add(Amp_StimulusNames, StimulusNames)
MaxResponseAll = np.hstack((Amp_StimulusNames[:, None],MaxResponseAll))

# add back the stimulus names to AUC
TotalAUC_StimulusNames = np.array(["AUC_"]*len(StimulusNames))
TotalAUC_StimulusNames = np.core.defchararray.add(TotalAUC_StimulusNames, StimulusNames)
TotalAUC = np.hstack((TotalAUC_StimulusNames[:, None],TotalAUC))

Events_StimulusNames = np.array(["Events_"]*len(StimulusNames))
Events_StimulusNames = np.core.defchararray.add(Events_StimulusNames, StimulusNames)
Events = np.hstack((Events_StimulusNames[:, None],Events))

EventAmp_StimulusNames = np.array(["AvgEventAmp_"]*len(StimulusNames))
EventAmp_StimulusNames = np.core.defchararray.add(EventAmp_StimulusNames, StimulusNames)
EventAmp = np.hstack((EventAmp_StimulusNames[:, None],EventAmp))

EventWidth_StimulusNames = np.array(["AvgEventWidth_"]*len(StimulusNames))
EventWidth_StimulusNames = np.core.defchararray.add(EventWidth_StimulusNames, StimulusNames)
EventWidth = np.hstack((EventWidth_StimulusNames[:, None],EventWidth))

#make headers for responders for each stimulus (e.g. "Res_3nM GRP")
Res_StimulusNames = np.array(["Binary_"]*len(StimulusNames))
Res_StimulusNames = np.core.defchararray.add(Res_StimulusNames, StimulusNames)
if debug:
    print("Res_StimulusNames =",Res_StimulusNames)
#add stim names 
responders = np.hstack((Res_StimulusNames[:, None],responders))

if(MaxAll==True):
    #stack all the arrays
    if(DO_AUC==True):
        maxResponse = np.vstack((maxResponse,responders,MaxResponseAll,TotalAUC,Events,EventAmp,EventWidth))
    else: maxResponse = np.vstack((maxResponse,responders,MaxResponseAll))
else:
    #put responders on the bottom of maxResponse
    if(DO_AUC==True):
        maxResponse = np.vstack((maxResponse,responders,MaxResponseAll,TotalAUC,Events,EventAmp,EventWidth))
    else:maxResponse = np.vstack((maxResponse,responders))

#save maxResponse
np.savetxt(pathToOutputData + splPrefix + "_MaxResponse.csv", maxResponse, delimiter=',', comments='', fmt='%s')
