import Utility_working as Utility #custom-made utility file, contains lengthy functions
import numpy as np
import sys
import os
from constant import *

try:
    AllROIsToRemove = np.loadtxt(pathToData +"BadROIs.csv",delimiter=',',dtype=str)
    print("found badROIs")
    ROIsToRemove=Utility.getROIsToRemove(debug, AllROIsToRemove, plane = planeNumber)
    print("ROIsToRemove=",ROIsToRemove)
    
except:
    ROIsToRemove = np.zeros((1,1))
    print("plotting all ROIs")

data, TotalTime, TotalROIs = Utility.importDataFile(debug, pathToRaw + "Results.csv") #import and format data
extracted = Utility.extractData(debug, data, ROIs = np.array([22,24,26,31,55,57,88]), ROIsToRemove = ROIsToRemove, stimStart = stimStart, stimEnd = stimEnd)



np.savetxt(prefix + "ExtractedGRPR.csv", extracted, delimiter=',', comments='', fmt='%s')
print("saved to"+ prefix + "ExtractedGRPR.csv")