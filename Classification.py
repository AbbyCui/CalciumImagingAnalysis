import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
from scipy.stats import norm,skewnorm
import Utility_working as Utility #custom-made utility file, contains lengthy functions
from constant import *
from lmfit.models import SkewedGaussianModel

######### USER INPUT REQUIRED
grp = 26340-fps*900 #when GRP starts (frames); #14->26340; #1 -> 40700
##########

def getISIstat(debug,st,amp):
    flag = False # calculate median and std if flag = true
    isi = st.diff() # diff between every 2 consequtive elements in st
    isi = isi.to_numpy()
    amp = amp.to_numpy()
    X = [i for i in isi if i > 0] #remove 0
    y = [i for i in amp if i > 0] #remove 0
    st = [i for i in st if i > 0]

    # X contains arrays inside of a list
    # the for-loop here flattens the arrays
    x = []
    for sublist in X:
        for num in sublist:
            x.append(num)
    
    # if the cell has >3 consequtive spikes -> flag = true
    if len(x)<=1: # 1 or 2 spikes after GRP application (1 isi)
        flag = False
        if debug:
            print(x)
            print("less than 3 spikes")
        
    else:
        #need to change x1 to pandas dataframe to perform conditional slicing
        x1 = pd.DataFrame(x[1:]) #remove the first ISI
        
        #exclude ISI that is 2 std away from median
        median = np.median(x1)
        std = np.std(x1)

        x1[x1>median+2*std] = 0 #make ISI 2std away from median = 0
        x1[x1<median-2*std]=0
        x2 = x1.to_numpy()
        if debug:
            print('isi,median,std before exclusion',x1,median,std)

        #data format wrangling
        x1 = []
        for sublist in x2:
            for num in sublist:
                x1.append(num)

        #must still have more than 3 spikes (>=2isi) after excluding isi that's more than 2std away from median
        tmp = [i for i in x1 if i!=0]
        if debug:
            print('isi after exclusion',tmp,'length =',len(tmp))
        if len(tmp)>=2:
            # must have at least 2 consequtive ISI
            for i in range(0,len(x1)-1):
                if min(x1[i:i+2])>0:
                    flag = True
                    if min(x1)==0: #if x1 contains 0
                        first0 = x1.index(0)# index function returns the index of the first occurance of 0
                        if i<first0: # the conseuitive ISIs are before the first occurance of 0
                            x1=x1[0:first0]
                            y=y[0:first0+1]
                            print("new x1=",x1)
                        else:
                            x1=x1[first0+1:]
                            y=y[first0+1:]
                            print("first spike excluded, newx1=",x1)
                    break   


            # delete the other side of zero

    # calculate median and std for isi and std for amp (of all spikes)
    if flag:    
        #calculate median and std for remaining isi
        x2 = [i for i in x1 if i!=0] #exclude isi that are 2std away from median
        
        median = np.median(x2)
        std = np.std(x2)
        ampstd = np.std(y)

    else:
        median = -1
        std = -1
        ampstd = -1

    if debug:
        print('output',median,std,ampstd)
        plotISIstats(x2,median,std)

    return median,std,ampstd

def plotISIstats(x,median,std):
    plt.hist(x,bins = 20)  # density=False would make counts
    plt.axvline(x = median, color = 'b', label = 'median')
    plt.axvline(x = median+2*std, color = 'r',label = '2std above median')
    plt.axvline(x = median-2*std, color = 'r')
    plt.ylabel('Count')
    plt.xlabel('ISI')
    plt.show()

##if want to customize some varibles, can enter them in terminal (see Unit Test.txt for example)
try:
    planeNumber = sys.argv[1]
    print("Starting Classification with variables from terminal input: planeNumber:",planeNumber)

    splPrefix = expNumber + "_" + planeNumber + "_"
    prefix = expNumber + "_" + planeNumber+ "_" 
except:
    print("Starting MaxResponse with variables in constant.py")


##### Main ######
eventAmp = np.loadtxt(pathToOutputData + prefix + "EventAmp.csv", delimiter=',', dtype = float)
ROInames = np.loadtxt(pathToOutputData + prefix + "ROInames.csv", delimiter=',', dtype=str)
Starts = np.loadtxt(pathToOutputData + prefix + "starts.csv", delimiter=',', dtype=float)
#only count after GRP application
Starts[Starts<grp] = 0
Starts[Starts>grp+fps*900] = 0 #only take 15min post GRP app

ISIstats = [["ROI","median","std","ampstd"]]
xs = Starts.shape[1] #number of ROIs
for i in range(1,xs):
    st = pd.DataFrame(Starts[:,i])
    # print(ROInames[i],ISIstats)
    # np.sign(st) = 0 for cells where st = 0, and 1s for cells where st >0
    # multiplication of the two matrices performs confolution where the cell in evenAmp = 0 if that corresponding cell in st =0
    amp = np.sign(st)*pd.DataFrame(eventAmp[:,i]) 
    median,std,ampstd = getISIstat(False,st,amp)
    data = [prefix+"ROI"+ROInames[i][4:],median,std,ampstd]
    ISIstats.append(data)

np.savetxt(pathToOutputData + prefix + "baseline_ISIstats.csv", ISIstats, delimiter=',', comments='', fmt='%s')

############
# ISIstats = np.loadtxt(pathToOutputData + prefix + "ISIstats.csv", delimiter=',', dtype=str)
# print(ISIstats[:,0])
# plt.plot(ISIstats[:,0],ISIstats[:,1],marker = 'o')
# plt.show()
