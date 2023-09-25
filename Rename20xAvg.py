import Utility_working as Utility #custom-made utility file, contains lengthy functions
from constant import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import sys
import os

#enter parameters
exp = str(465)
planeRange = range(1,5) #range(1,5) iterates over plane 1,2,3,4

####
ROIsToRemove = np.zeros((1,1))
for p in planeRange:
    #import and extract smoothed data
    filename = exp+'_P'+str(p)
    splPATH = 'D:/DATA/Calcium Oscillation Data/Figures and source data/4880 CICADA response/smoothed/#' + filename
    smoothed = np.loadtxt(splPATH +"_Smoothed.csv",delimiter=',',dtype=str)
    f = Utility.extractData(debug, smoothed, ROIsToRemove = ROIsToRemove, stimStart = stimStart, stimEnd = stimEnd)

    #calculate 20x average
    y,x = f.shape
    avg = np.empty(((y-1)//20,x)) #an empty array to stored the 20x results

    for i in range((y-1)//20-1):
        thisf = np.array(f[1+i*20:i*20+20,...],dtype = float)
        # print(thisf)
        avg[i+1,...] = np.mean(thisf,axis = 0) #axis =0 -> average downwards across 20 rows
    out = avg.astype(str)

    #change ROI name to format such as exp465_P0_ROI002
    head=f[0,...]
    outhead = np.empty_like(head)
    for i in range(len(head)):
        thishead = head[i]
        a = thishead.replace('Mean','')
        a = a.zfill(3)
        a = 'exp'+filename+"_ROI"+a
        outhead[i] = a
    out[0,...] = outhead
    np.savetxt("D:/DATA/Calcium Oscillation Data/Figures and source data/4880 CICADA response/#"+filename+"_20x avg_test.csv",out, delimiter=',', comments='', fmt='%s')
print('finished')

