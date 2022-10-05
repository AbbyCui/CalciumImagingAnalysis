"""
calculate AUC (above threshold) for a given stimulus for all ROIs. Also generate a distribution of events for each stimuli (AUC-time), 
and calculate kurtosis, skewness and the median from the distribution
INPUT: smoothed data, stimulus.csv
OUTPUT: a dataframe with 5 rows (header AUC, kurtosis, skewness and median) and each ROI in each column.
"""
import Utility_working as Utility #custom-made utility file, contains lengthy functions
import numpy as np
from constant import *
import sys

try:
    parentFolder = sys.argv[1]
    planeNumber = sys.argv[2]
    stimIndex = int(sys.argv[3])

    pathToOutputData = "../"+parentFolder+"/"+"OutputData/"
    splPrefix = expNumber + "_" + planeNumber+ "_"
except:
    print("Starting ProcessData.py with constants in constant.py")

#import files
data = np.loadtxt(pathToOutputData + splPrefix +"Smoothed.csv",delimiter=',',dtype=str)
AllThresholds = np.loadtxt(pathToOutputData + splPrefix +"AllThresholds.csv",delimiter=',',dtype=str)
stimulus = np.loadtxt(pathToData +"Stimulus.csv",delimiter=',',dtype=str)

#extract the name of the stimulus
stimName = stimulus[stimIndex,0]

#extract the start and end (frame) fo the stimulus
start = int(float(stimulus[stimIndex,1]))
end = int(float(stimulus[stimIndex,2]))

#extract only the desired ROIs (extract only frames during the desired stimulus window)
ROIstimdata = Utility.extractData(debug, data, stimStart = start, stimEnd = end) 
Starts,Ends = Utility.extractEvent(debug, ROIstimdata, AllThresholds)

#print some info about input/output
print("Summarizing spike pattern for",pathToOutputData + splPrefix +"Smoothed.csv")
print("Stimulus name is",stimName)
print("saving file to",pathToOutputData + splPrefix + stimName + " SpikePattern.csv")

#find the AUC, SD and median of spike time
SpikePattern = Utility.getSpikePattern(debug, ROIstimdata, AllThresholds,Starts,binSize = fps*60)

np.savetxt(pathToOutputData + splPrefix + stimName + " SpikePattern.csv", SpikePattern, delimiter=',', comments='', fmt='%s')