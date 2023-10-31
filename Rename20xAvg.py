import Utility_working as Utility #custom-made utility file, contains lengthy functions
from constant import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import sys
import os

#enter parameters
DataFolder = 'E:/#489 - Copy/#489/OutputData/'
exp = str(489)
planeRange = range(0,5) #range(1,5) iterates over plane 1,2,3,4
Avg_Amount = 5

####
ROIsToRemove = np.zeros((1,1))
for p in planeRange:
    #import and extract smoothed data
    filename = '#' + exp + '_P'+str(p)
    splPATH = DataFolder + filename
    smoothed = np.loadtxt(splPATH +"_Smoothed.csv",delimiter=',',dtype=str)
    f = Utility.extractData(debug, smoothed, ROIsToRemove = ROIsToRemove, stimStart = stimStart, stimEnd = stimEnd)

    #calculate 20x average
    y,x = f.shape
    avg = np.empty(((y-1)//Avg_Amount,x)) #an empty array to stored the 20x results

    for i in range((y-1)//Avg_Amount-1):
        thisf = np.array(f[1+i*Avg_Amount:i*Avg_Amount+Avg_Amount,...],dtype = float)
        # print(thisf)
        avg[i+1,...] = np.mean(thisf,axis = 0) #axis =0 -> average downwards across 20 rows
    out = avg.astype(str)

    #change ROI name to format such as exp465_P0_ROI002
    head=f[0,...]
    outhead = np.full_like(head,"12345678901234567", dtype="object")
    for i in range(len(head)):
        thishead = head[i]
        a = thishead.replace('Mean','')
        a = a.zfill(3)
        thisname = filename+"_ROI"+a
        outhead[i] = thisname
    out[0,...] = outhead
    print('changed header:',head[1],'to',outhead[1])
    AvgStr = str(Avg_Amount)
    np.savetxt(DataFolder + filename  +"_"+ AvgStr + "x avg.csv",out, delimiter=',', comments='', fmt='%s')
print('finished')
