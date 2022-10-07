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
    parentFolder = sys.argv[1]
    planeNumber = sys.argv[2]

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
normalized = Utility.normalize(debug, data, window = window, percentile = percentile)
smoothed = Utility.smooth(debug, normalized,window_size,polynomial)

# if already have smoothed data, and just want to re-run getAllTHreshods, un-comment out the following 2 lines
splPATH = pathToOutputData + splPrefix
smoothed = np.loadtxt(splPATH +"Smoothed.csv",delimiter=',',dtype=str)

# get threshold for all ROIs and stimuli
allThresholds = Utility.getAllThresholds(debug, smoothed, stimulus, fps, threshold)

# prefix to save file to the correct directory
prefix = pathToOutputData + splPrefix

#save everything
#if already have smoothed data, and just want to re-run getAllthresholds, comment out the 2 lines
#that save "Normalized.csv" and "Smoothed.csv" 
# np.savetxt(prefix + "Normalized.csv", normalized, delimiter=',', comments='', fmt='%s')
# np.savetxt(prefix + "Smoothed.csv", smoothed, delimiter=',', comments='', fmt='%s')
# np.savetxt(prefix + "AllThresholds.csv", allThresholds, delimiter=',', comments='', fmt='%s')
