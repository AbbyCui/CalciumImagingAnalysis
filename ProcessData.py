"""
import raw data, normalize, smooth, then calculate the threshold for each ROI (0.5 or baselineMean+4*SD, which ever is bigger)
"""
import Utility_working as Utility #custom-made utility file, contains lengthy functions
import numpy as np
import sys
import os
from constant import *

##if want to customize some varibles, can enter them in terminal (see Unit Test.txt for example)
try:
    #parentFolder = sys.argv[1]
    planeNumber = sys.argv[1]

    pathToRaw = "../"+parentFolder+"/Data/"+parentFolder+"_"+planeNumber+"_"
    pathToOutputData = "../"+parentFolder+"/"+"OutputData/"
    splPrefix = expNumber + "_" + planeNumber+ "_"
except:
    print("Starting ProcessData.py with constants in constant.py")

# if OutputData folder doesn't exist, create new one
if not os.path.exists(pathToOutputData[:-1]):
    os.makedirs(pathToOutputData[:-1])

# import raw data and stimulus file
data, TotalTime, TotalROIs = Utility.importDataFile(debug, pathToRaw + "Results.csv") #import and format data
stimulus = np.loadtxt(pathToData +"Stimulus.csv",delimiter=',',dtype=str,usecols = (0,1,2,3))

#normalize and smooth data
if(ThresholdsOnly==0):
    if(splitnorm==1):
        splits = np.loadtxt(pathToData +"Splits.csv",delimiter=',',dtype=int,usecols = (0))
        numsplits=(len(splits)-1)
        i=0
        rawdata = data[1:,1:] #only the data, excluding ROInames and frames 
        ###remember that these are now starting at 0 and the list of splits runs from the 1st frame not the 0th###
        rawdata = rawdata.astype(float, copy=False)    
        ROInames = data[0,1:]
        TotalROIs = len(ROInames)
        while i < numsplits:
            start=((splits[i]-1))
            end=((splits[i+1])-1)
            if i==((numsplits-1)): ##This is to include the last frame
                end=end+1
            if debug:
                print(start)
                print(end)

            splitdata=rawdata[start:end,0:]
            dff = Utility.normalizesplits(debug, splitdata, window = window, percentile = percentile, TotalROIs = TotalROIs)
            if i==0:
                splitDFF=dff
            else:
                splitDFF=np.vstack((splitDFF,dff))
            #SplitDFF=SplitDFF.astype(str, copy=True)
            #dff=dff.astype(str, copy=True)
            if debug:
                print(dff.shape)
                print(splitDFF.shape)
                print('splitDFF has shape of', splitDFF.shape)
                prefix = pathToOutputData + splPrefix
                np.savetxt(prefix + "splitdatanormalizedall.csv", splitDFF, delimiter=',', comments='', fmt='%s')
            i+=1
        normalized=splitDFF

        ##add back the ROI names and frames
        a = np.ones_like(data[1:,...])
        a[...,0]=data[1:,0] ##copy the X-axis into a column (frames)
        a[...,1:] = normalized ##copy the normalized array into the new array with the x axis
        normalized=a.astype(str, copy=True) ##convert array to string so that it can support text names
        titles = np.insert(ROInames,0,"Frame") 
        normalized[0,...] = titles #insert ROI names into the string np
       
        if debug:
            print("dffT has shape:", normalized.shape)
            print("ROI names after normalization:", normalized[...,0])
    else: 
        normalized = Utility.normalize(debug, data, window = window, percentile = percentile)
    smoothed = Utility.smooth(debug, normalized,window_size,polynomial)

# if already have smoothed data, and just want to re-run getAllTHreshods
if(ThresholdsOnly==1):
    print("Re-running Threshods, no normalization/smoothing")
    splPATH = pathToOutputData + splPrefix
    smoothed = np.loadtxt(splPATH +"Smoothed.csv",delimiter=',',dtype=str)

# get threshold for all ROIs and stimuli
allThresholds = Utility.getAllThresholds(debug, smoothed, stimulus, fps, threshold)

# prefix to save file to the correct directory
prefix = pathToOutputData + splPrefix

#save everything
#that save "Normalized.csv" and "Smoothed.csv" 
if(ThresholdsOnly==0):
    np.savetxt(prefix + "Normalized.csv", normalized, delimiter=',', comments='', fmt='%s')
    np.savetxt(prefix + "Smoothed.csv", smoothed, delimiter=',', comments='', fmt='%s')
np.savetxt(prefix + "AllThresholds.csv", allThresholds, delimiter=',', comments='', fmt='%s')
