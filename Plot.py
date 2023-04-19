'''
Plots user specified exp number, plane, ROI, time frame (in sec), with each stimuli shaded with user specified colors (at the 3rd column of the Stimulus.csv)
Make sure stimulus names don't include ","
'''
import Utility_working as Utility #custom-made utility file, contains lengthy functions
from constant import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import sys
import os

# if want to customize some varibles, can enter them in terminal (see Unit Test.txt for example)
try:
    planeNumber = sys.argv[1]
    stimStart = sys.argv[2]
    stimEnd = sys.argv[3]
    print(planeNumber,stimStart,stimEnd)
    splPrefix = expNumber + "_" + planeNumber + "_"
    prefix = expNumber + "_" + planeNumber+ " _frm" + str(stimStart) + "-"+ str(stimEnd)+ "_" 
    pathToRaw = "../"+parentFolder+"/Data/"+parentFolder+"_"+planeNumber+"_"
    print("using constants from terminal input: INPUT: ",pathToOutputData + splPrefix +"Smoothed.csv","OUTPUT:",pathToFigure + expNumber+"_" + planeNumber)
except:
    print("Starting Plot.py with variables in constant.py")

# if have a csv. file with ROIs to remove, it will be included in plotting
try:
    AllROIsToRemove = np.loadtxt(pathToData +"BadROIs.csv",delimiter=',',dtype=str)
    print("found badROIs")
    ROIsToRemove=Utility.getROIsToRemove(debug, AllROIsToRemove, plane = planeNumber)
    print("ROIsToRemove=",ROIsToRemove)
    
except:
    ROIsToRemove = np.zeros((1,1))
    print("plotting all ROIs")

# if Figure folder do not exist, create one
if not os.path.exists(pathToFigure[:-1]):
    os.makedirs(pathToFigure[:-1])

# import raw data, normalized data, and smoothed data
splPATH = pathToOutputData + splPrefix
smoothed = np.loadtxt(splPATH +"Smoothed.csv",delimiter=',',dtype=str)
smoothed = Utility.extractData(debug, smoothed, ROIsToRemove = ROIsToRemove, stimStart = stimStart, stimEnd = stimEnd)
stimulus = np.loadtxt(pathToData +"Stimulus.csv",delimiter=',',dtype=str,usecols = (0,1,2,3))
AllThresholds = np.loadtxt(pathToOutputData + splPrefix +"AllThresholds.csv",delimiter=',',dtype=str)

TotalTime = smoothed.shape[0]-1
TotalROIs = smoothed.shape[1]-1
print("plotting experiment ",expNumber, "plane ",planeNumber,"with ",TotalROIs,"ROIs", "from frame",stimStart,'to',stimEnd)

if str(ROIs) == "all":
    # arrange(x,y) -> [x,y), so end has to be TotalROIs+1 to include the last ROI
    ROIs = np.arange(1,TotalROIs+1)
if str(stimEnd) == "all" or str(stimStart) == "all":
    stimStart = 1
    stimEnd = TotalTime
elif int(stimEnd) > TotalTime:
    stimEnd = TotalTime

stimStart = int(stimStart)
stimEnd = int(stimEnd)

# extract only the wanted ROIs and crop recording to desired time frames
ROIsmoothed = Utility.extractData(debug, smoothed, ROIs, stimStart = stimStart, stimEnd = stimEnd)
ROIs = ROIsmoothed[0,1:] #AC_exp17_P0_Mean1


# range(x,y) -> [x,y), so end has to be len(ROI)+1 to include the last ROI
rawTime = ROIsmoothed[1:,0]
for i in range(1,len(ROIs)+1):
    ROI = str(ROIs[i-1])
    rawSmoothed = ROIsmoothed[1:,i].astype(float,copy=False)

    fig = plt.figure() 
    ax = fig.add_subplot()
    leftxaxis=((round(stimStart/fps/10))*10)
    leftxaxis=int(leftxaxis)
    rightxaxis=(round(((stimEnd)/fps/10)*10))
    rightxaxis=int(rightxaxis)
    xaxisrange=(rightxaxis-leftxaxis)##this is the duration in seconds of the total recording
    SecondsPerInch=int(SecondsPerInch)
    xaxisrange=int(xaxisrange)
    figsize=(xaxisrange/SecondsPerInch)
    figsize=int(figsize)
    if(figsize<1):
        figsize=1
        print("X-axis too small, increase range or the seconds/inch")
    fig.set_size_inches(figsize, 5)
    plt.title(ROI, loc='center', y=.9)
    #plt.title(expNumber + " "+planeNumber +" ROI=" + ROI, loc='center', y=.9)
    plt.xlabel("Time (sec)")
    plt.plot(np.arange(stimStart, stimEnd, step = 1)/fps,rawSmoothed,linewidth=1)
    #plt.plot(rawTime/fps,rawSmoothed,linewidth=1)
    plt.tight_layout()
    plt.axis()
    yaxismax=3
    plt.ylim(-.2, yaxismax)
    plt.xlim(leftxaxis, rightxaxis)
    left, right = plt.xlim() 
    plt.subplots_adjust(left=None, bottom=None, right=None, top=.7, wspace=None, hspace=None)
    tickspacing=500 #this is in seconds
    Ticks=1
    if(Ticks==1):
        xmarks=[i for i in range(leftxaxis,rightxaxis,tickspacing)]
        plt.xticks(xmarks)
        #minor tick spacing
        minortickspacing=.1 #this is in fractions of major
        tickspacing=tickspacing*minortickspacing
        tickspacing=int(tickspacing)
        xmarks=[i for i in range(leftxaxis,rightxaxis,tickspacing)]
        plt.xticks(xmarks,minor=True)
    
    #mark each stimulus with shadings and draw threshold for them with red line
    for j in range(1,stimulus.shape[0]+1):
        stimName = stimulus[j-1,0]
        thisThreshold = float(AllThresholds[j,i])
        start = int(float(stimulus[j-1,1]))/fps
        end = int(float(stimulus[j-1,2]))/fps
        percentStart = (start-left)/(right-left)
        percentEnd = (end-left)/(right-left)

        #try to find color in Stimulus.csv
        #if fail (not provided), default to grey
        try:
            color = stimulus[j-1,3]
        except:
            color = "grey"
            if debug:
                print("no color provided in Stimulus.csv. Color defaulted to grey")
        if debug:
            print("for stimulus:",stimName ,", stimStart =",start,percentStart,"stimEnd =",end,percentEnd,"color is",color,"threshold is",thisThreshold)
        # if the window plotted include only a part of a stimuli window, still draw the shadings
        if start >= stimStart/fps and end <= stimEnd/fps:
            plt.axvspan(start, end, alpha=0.3, color=color) 
            plt.axhline (y = thisThreshold, xmin =percentStart, xmax =percentEnd, color='red', linewidth = 1 )
            plt.text(start, (yaxismax), stimName, rotation=-45, fontsize=12, wrap=False, ha='right')

    plt.savefig(pathToFigure + ROI + "_"+str(stimStart) + "-" + str(stimEnd) + ".png")
    plt.grid()
    # plt.show()
    plt.close("all")
