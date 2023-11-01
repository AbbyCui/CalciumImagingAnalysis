import Utility_working as Utility #custom-made utility file, contains lengthy functions
from constant import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import sys
import os

#enter parameters
Avg_Amount = '5' ##this needs to be a string 
ParentDirectory = 'E:/#489 - Copy/#489/'
template_name = "#489_Non-Itch IN"
expNum = str(489)
planeRange = range(0,5) #range(1,5) iterates over plane 1,2,3,4


#assign directory based on our standard organization
dir = ParentDirectory + 'OutputData/' ##where your averaged/smoothed traces are
temp_dir = ParentDirectory + 'Data/' ##where your filter files are
output = template_name #specify output file name, or by default use the name of the template CSV
#load files with headers for ROIs to be extracted (e.g. exp456_P1_ROI002)

template = np.loadtxt(temp_dir + template_name + '.csv', delimiter=',',comments='%',dtype=str)


#template = np.loadtxt(ParentDirectory + template_name + ".csv",delimiter=',',dtype=str)

#res=np.loadtxt("D:/DATA/Calcium Oscillation Data/Figures and source data/4880 CICADA response/ROInames_4880responder.csv",delimiter=',',dtype=str)
numROI = len(template)


# import raw data, normalized data, and smoothed data
for p in planeRange:
    filename = '#'+expNum+'_P'+str(p)
    splPATH = dir + filename 
    avg = np.loadtxt(splPATH + "_" + str(Avg_Amount) + "x avg.csv",delimiter=',',comments='%',dtype=str)
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
np.savetxt(dir+output+".csv",filtered, delimiter=',', comments='', fmt='%s')
