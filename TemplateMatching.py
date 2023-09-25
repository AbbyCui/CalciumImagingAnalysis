import Utility_working as Utility #custom-made utility file, contains lengthy functions
from constant import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import sys
import os

#enter parameters
expNum = str(465)
planeRange = range(1,2)
dir = 'D:/DATA/Calcium Oscillation Data/Figures and source data/4880 CICADA response/'
output = 'filtered_noRes' #specify output file name
#load files with headers for ROIs to be extracted (e.g. exp456_P1_ROI002)
template = np.loadtxt("D:/DATA/Calcium Oscillation Data/Figures and source data/4880 CICADA response/ROInames_4880nonresponder.csv",delimiter=',',dtype=str)

#res=np.loadtxt("D:/DATA/Calcium Oscillation Data/Figures and source data/4880 CICADA response/ROInames_4880responder.csv",delimiter=',',dtype=str)
numROI = len(template)


# import raw data, normalized data, and smoothed data
for p in planeRange:
    filename = '#'+expNum+'_P'+str(p)
    splPATH = dir + filename
    avg = np.loadtxt(splPATH +"_20x avg_test.csv",delimiter=',',dtype=str)
    ROIsToRemove = np.zeros((1,1))
    f = Utility.extractData(debug, avg, ROIsToRemove = ROIsToRemove, stimStart = stimStart, stimEnd = stimEnd)
    print('the first 5 ROIs in f:',f[0,0:5])

    yf,xf = f.shape
    #if filteredRes has not been created, create it as a empty array
    try:
        filtered
    except:
        filtered = np.empty((yf-1,numROI))

    print('number of rows:',yf,'number of ROIs to be extracted',numROI)
    for i in range(1,xf):
        for k in range(numROI):
            if f[0,i]==template[k]:
                filtered[...,k] = f[1:,i]
                break
    
filtered = np.vstack((template[None,...],filtered))
filtered = np.hstack((f[...,0][...,None],filtered))
np.savetxt("D:/DATA/Calcium Oscillation Data/Figures and source data/4880 CICADA response/"+output+".csv",filtered, delimiter=',', comments='', fmt='%s')