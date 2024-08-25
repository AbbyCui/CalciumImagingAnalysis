'''
Plots user specified exp number, plane, ROI, time frame (in sec), with each stimuli shaded with user specified colors (at the 3rd column of the Stimulus.csv)
Make sure stimulus names don't include ","
Can exclude ROIs with ROIstoRemove.csv; or include only selected ROIs using ROIstoInclude.csv
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

try:
    SecondsPerInch = sys.argv[4]
    print("using SecondsPerInch from Terminal",SecondsPerInch)
except:
    print("using SecondsPerInch from Constant File", SecondsPerInch)

# if have a csv. file with ROIs to remove, it will be included in plotting
try:
    AllROIsToRemove = np.loadtxt(pathToData +"BadROIs.csv",delimiter=',',dtype=str)
    print("found badROIs")
    ROIsToRemove=Utility.getROIsToRemove(debug, AllROIsToRemove, plane = planeNumber)
    print("ROIsToRemove=",ROIsToRemove)
    
except:
    ROIsToRemove = np.zeros((1,1))
    print("found no ROIs to remove")

# if have a csv file with ROIs to include, the script will only plot those ROIs
try:
    AllROIsToInclude = np.loadtxt(pathToData +"ROIsToInclude.csv",delimiter=',',dtype=str)
    print("found ROIsToInclude. Only plotting ROIsToInclude")
    ROIsToInclude=Utility.getROIsToRemove(debug, AllROIsToInclude, plane = planeNumber)
    print("for plane",planeNumber,", ROIsToInclude=",ROIsToInclude)

except:
    ROIsToInclude = "all"
    print("found no list of ROIs to specifically include -> including all ROIs")

# if Figure folder do not exist, create one
if not os.path.exists(pathToFigure[:-1]):
    os.makedirs(pathToFigure[:-1])

# import raw data, normalized data, and smoothed data
splPATH = pathToOutputData + splPrefix
smoothed = np.loadtxt(splPATH +"Smoothed.csv",delimiter=',',dtype=str)
smoothed = Utility.extractData(debug, smoothed, ROIsToRemove = ROIsToRemove, stimStart = stimStart, stimEnd = stimEnd, ROIs=ROIsToInclude)
stimulus = np.loadtxt(pathToData +"Stimulus.csv",delimiter=',',dtype=str,usecols = (0,1,2,3))

AllThresholds = np.loadtxt(pathToOutputData + splPrefix +"AllThresholds.csv",delimiter=',',dtype=str)
y,x = AllThresholds.shape
GoodThresholds = AllThresholds[0:,0] #create new threshold array in which to place the thresholds post ROI removal
ROInames = ["Frame",] #initiate new empty array

Rec_Splits=0
if os.path.isfile(pathToData +"rec_length.csv"):
    rec_length = np.loadtxt(pathToData +"rec_length.csv",delimiter=',',dtype=int)
    print("found a recording length file, plotting rec splits")
    Rec_Splits=1

SecondsPerInch = int(SecondsPerInch)
if(SecondsPerInch>200):
    tickspacing=500
else:
    if(SecondsPerInch>100):
        tickspacing=100
    else:
        if(SecondsPerInch)>50:
            tickspacing=50
        else:
            if SecondsPerInch>25:
                tickspacing=25
            else:
                tickspacing=10

    #tickspacing=500 #this is in seconds;at 400 SPI, 500 is a good number. If you want to set it manually. Otherwise it'll be scaled ~ to SPI

if debug:
    print("AllThresholds Shape",AllThresholds.shape)
    print("y,x",y,x)

for ROI in range(1,x): #skip the 0th row because it's the names 
    if (ROI not in ROIsToRemove and ROIsToInclude == "all") or (ROIsToInclude != "all" and ROI in ROIsToInclude and ROI not in ROIsToRemove):
        if debug:
            print("ROI",ROI)
            print("Allthresholds",AllThresholds[0:,ROI])
        thisgoodthreshold = AllThresholds[0:,ROI] #take the ROIth column in the data sheet
        if debug:
            print(thisgoodthreshold.shape)
        GoodThresholds = np.vstack((GoodThresholds,thisgoodthreshold)) #stack on top
        if debug:
            print("ROIname",ROInames)
    else:
        if debug:
            print("ROI in ROIsToRemove",ROI)
AllThresholds = GoodThresholds.T #correct the axis of the data -> one colum for each ROI

TotalTime = smoothed.shape[0]-1
TotalROIs = smoothed.shape[1]-1
print("plotting experiment ",expNumber, "plane ",planeNumber,"with a toatl number of ",TotalROIs,"ROIs")

if str(ROIs) == "all":
    # arrange(x,y) -> [x,y), so end has to be TotalROIs+1 to include the last ROI
    ROIs = np.arange(1,TotalROIs+1)
if str(stimEnd) == "all" or str(stimStart) == "all":
    stimStart = 0 ##This was changed by CAW to 0 on 2-17-23 as when it was 1 there was a 1 number mismatch when graphing
    stimEnd = TotalTime
    if debug:
        print("stimEnd==all")

stimStart = int(stimStart)
stimEnd = int(stimEnd)

# extract only the wanted ROIs and crop recording to desired time frames
if debug:
        print("stimStart=",stimStart,"stimEnd=",stimEnd)
        print("plotting experiment ",expNumber, "plane ",planeNumber,"with",ROIsmoothed.shape[1]-1,"ROIs")
ROIsmoothed = smoothed ##This used to be an ExtraData and was changed by CAW 2-17-23
ROIs = ROIsmoothed[0,1:]

# range(x,y) -> [x,y), so end has to be len(ROI)+1 to include the last ROI
for i in range(1,len(ROIs)+1):
    ROI = str(ROIs[i-1])[4:]
    ROInumber = int(ROI)
    ROInumber = f'{ROInumber:03d}'
    rawSmoothed = ROIsmoothed[1:,i].astype(float,copy=False)

    fig = plt.figure() 
    ax = fig.add_subplot()
    leftxaxis=((round(((stimStart)/fps)/10))*10)
    leftxaxis=int(leftxaxis)
    rightxaxis=(round(((stimEnd)/fps/10)*10))
    rightxaxis=int(rightxaxis)
    xaxisrange=(rightxaxis-leftxaxis)##this is the duration in seconds of the total recording
    xaxisrange=int(xaxisrange)
    figsize=(xaxisrange/SecondsPerInch)
    figsize=int(figsize)
    if(figsize<1):
        figsize=1
        print("X-axis too small, increase range or the seconds/inch")
    fig.set_size_inches(figsize, 7)
    plt.title(expNumber + "_"+planeNumber +"_ROI" + ROInumber, loc='center', y=.9)
    plt.xlabel("Time (sec)")
    plt.plot(np.arange(stimStart, stimEnd, step = 1)/fps,rawSmoothed,linewidth=1)
    plt.tight_layout()
    plt.axis()
    yaxismax=3
    plt.ylim(-.2, yaxismax)
    plt.xlim(leftxaxis, rightxaxis)
    left, right = plt.xlim() 
    plt.subplots_adjust(left=None, bottom=None, right=None, top=.7, wspace=None, hspace=None)

    Ticks=1
    if(Ticks==1):
        xmarks=[i for i in range(leftxaxis,rightxaxis,tickspacing)]
        plt.xticks(xmarks)
        #minor tick spacing
        minortickspacing=.1 #this is in fractions of major
        minortickspacingplot=tickspacing*minortickspacing
        minortickspacingplot=int(minortickspacingplot)
        xmarks=[i for i in range(leftxaxis,rightxaxis,minortickspacingplot)]
        plt.xticks(xmarks,minor=True)
    
    #mark each stimulus with shadings and draw threshold for them with red line
    for j in range(1,stimulus.shape[0]):
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
            # print(" ")
        # if the window plotted include only a part of a stimuli window, still draw the shadings
        if start >= stimStart/fps and end <= stimEnd/fps:
            plt.axvspan(start, end, alpha=0.3, color=color) 
            plt.axhline (y = thisThreshold, xmin =percentStart, xmax =percentEnd, color='red', linewidth = 1 )
            plt.text(start, (yaxismax), stimName, rotation=-45, fontsize=12, wrap=False, ha='right')
    
    # add a red vertical line to mark the start of each recording
    # this could be helpful in identifying z-drifts associated with the z-adjustments that we do between each recordings
    # rec_length inidcates the length (in frames) of each recording
    #rec_length = np.repeat(2500, 22)
    if Rec_Splits==1:
        #rec_length = [700,0,1750,3000,1500,2000,3000,0,2000,2000,2000,2000,1300,2000,2000,2000,540,2000,1610,2000,1270,0,2000,3000,2000,3000,900,2000,2000,2000,2000,2000,2000,2000,2000,2000,2000,2000,2000,2000,3000,3000] if you want to manually place your tick marks
        pos=0
        for rec in range(len(rec_length)):
            pos += rec_length[rec]
            plt.vlines(pos/fps,0,3,colors="red",linewidth = 1)

    plt.savefig(pathToFigure + expNumber+"_" + planeNumber + "_ROI" + ROInumber + "-"+str(stimStart) + "-" + str(stimEnd) + ".png", dpi=300)
    plt.grid()
    # plt.show()
    plt.close("all")
