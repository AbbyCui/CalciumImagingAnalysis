"""
import raw data, normalize, smooth, then calculate the threshold for each ROI (0.5 or baselineMean+4*SD, which ever is bigger)
"""

#TODO add moving threshold feature (refer to google collab)

from cmath import log
from pandas import array
import Utility_working as Utility #custom-made utility file, contains lengthy functions
from gettext import install
import numpy as np
import matplotlib.pyplot as plt
import csv
import plotly.express as px
from scipy.fft import fft, fftfreq
from scipy import signal
import sys
import os
import matplotlib.pyplot as plt
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

# import raw data
data, TotalTime, TotalROIs = Utility.importDataFile(debug, pathToRaw + "Results.csv") #import and format data

#normalize and smooth data
normalized = Utility.normalize(debug, data, window = window, percentile = polynomial)
smoothed = Utility.smooth(debug, normalized,window_size,polynomial)
allThresholds = Utility.getAllThresholds(debug, smoothed, threshold, baselineStart = baselineStart, baselineEnd=baselineEnd)

# prefix to save file to the correct directory
prefix = pathToOutputData + splPrefix

np.savetxt(prefix + "Normalized.csv", normalized, delimiter=',', comments='', fmt='%s')
np.savetxt(prefix + "Smoothed.csv", smoothed, delimiter=',', comments='', fmt='%s')
np.savetxt(prefix + "AllThresholds.csv", allThresholds, delimiter=',', comments='', fmt='%s')
