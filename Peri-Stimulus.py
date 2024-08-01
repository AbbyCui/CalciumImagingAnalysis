import Utility_working as Utility #custom-made utility file, contains lengthy functions
from constant import *
import numpy as np
import sys
import os
import math
import subprocess


##  This script extracts the data withint peri-stimulus window (output one file ending with "Peri-stim"), 
## and calculate mean, median, 95% range for each frame (output another file ending with "avg Peri-stim")
## Input: Smoothed data, stim file, ROIsToInclude.
if debug:
    print("--------------Peri-Stimulus.py---------------")

## User input
stim_index = [46] #index 1 means the 2nd stimulus (yes we love python); input list to merge multiple stim (e.g. [1,2,3])
interval = 20*fps #10*fps would mean 10sec pre and post the start of the stim
grace = 1.5*fps #exclude some time before and after stim start/end (this is useful when you're not so cofident about start/stop time stamps)
postfix = "test" #something meaningful to include in file names

## Note to self
# 
# # [6,7,8,9,10,11,12] for pre 4880
# [6,7,10,12] 100g
# [8,11] 100g x2
# [9] 60g

# [36,37,38,44,45,46] for post 4880
# [38,44,45] 100g
# [36] 60g
# [37] 60g x2
# [46] 100gx2

for plane in range(0,int(float(sys.argv[1]))):
    # if want to customize some varibles, can enter them in terminal (see Unit Test.txt for example)

    planeNumber = "P"+str(plane)
    splPrefix = expNumber + "_" + planeNumber + "_"
    pathToRaw = "../"+parentFolder+"/Data/"+parentFolder+"_"+planeNumber+"_"
    print("running",planeNumber,": INPUT: ",pathToOutputData + splPrefix +"Smoothed.csv","OUTPUT:",pathToOutputData + expNumber+"_" + planeNumber)

    # if have a csv. file with ROIs to remove, it will be included in plotting
    try:
        AllROIsToRemove = np.loadtxt(pathToData +"BadROIs.csv",delimiter=',',dtype=str)
        print("found badROIs")
        ROIsToRemove=Utility.getROIsToRemove(debug, AllROIsToRemove, plane = planeNumber)
        print("ROIsToRemove=",ROIsToRemove)
    except:
        ROIsToRemove = np.zeros((1,1))
        print("No Bad ROIs")

    #if have a csv file with ROIs to include, only those ROIs will be analyzed. Otherwise, will include all ROIs in this plane
    try:
        AllROIsToInclude = np.loadtxt(pathToData +"ROIsToInclude.csv",delimiter=',',dtype=str)
        print("found ROIsToInclude")
        ROIsToInclude=Utility.getROIsToRemove(debug, AllROIsToInclude, plane = planeNumber)
        print("for plane",planeNumber,", ROIsToInclude=",ROIsToInclude)

    except:
        ROIsToInclude = "all"
        print("including all ROIs")

    # if Figure folder does not exist, create one
    if not os.path.exists(pathToFigure[:-1]):
        os.makedirs(pathToFigure[:-1])

    #import data
    splPATH = pathToOutputData + splPrefix
    smoothed = np.loadtxt(splPATH +"Smoothed.csv",delimiter=',',dtype=str)
    smoothed = Utility.extractData(debug, smoothed, ROIsToRemove = ROIsToRemove, stimStart = 1, stimEnd = "all",ROIs=ROIsToInclude)
    stimulus = np.loadtxt(pathToData +"Stimulus.csv",delimiter=',',dtype=str,usecols = (0,1,2,3))
    starts = stimulus[...,1]
    ends = stimulus [...,2]
    stimName = stimulus[...,0]
    durations = [float(xi) - float(yi) for xi, yi in zip(ends, starts)]
    max_dur = max(durations)

    # Extract data
    for i in range(len(stim_index)): #for each stimulus start time

        # extract the start and end for this specific stimulus
        this_start = math.ceil(float(starts[stim_index[i]]))-grace
        this_end = math.ceil(float(ends[stim_index[i]]))+grace
        duration=this_end-this_start
        this_name= stimName[stim_index[i]]

        # cropp out the time before and after stimulus (tihs includes header)
        croppedData = Utility.extractData(debug,smoothed,stimStart=this_start-interval,stimEnd=this_start + interval + duration)
        y,x=croppedData.shape
        
        # assemble header
        # stim start,end,name
        name = [str(ele) for ele in [this_name] for i in range(x-1)] #repeat this_start for each ROI
        name = np.insert(name,0,"stim name")

        start_head = [str(ele) for ele in [this_start] for i in range(x-1)] #repeat this_start for each ROI
        start_head = np.insert(start_head,0,"start fr")

        end_head = [str(ele) for ele in [this_end] for i in range(x-1)] #repeat this_start for each ROI
        end_head = np.insert(end_head,0,"end fr")

        # mean pre vs post stim
        pre=Utility.getBaselineMean(debug,croppedData,baselineStart = 1,baselineEnd = interval-grace)
        pre=np.transpose(pre)
        pre=pre.astype(str)
        pre = np.insert(pre,0,"pre_mean")

        post = Utility.getBaselineMean(debug,croppedData,baselineStart = interval+duration+grace,baselineEnd=duration + 2*interval)
        post=np.transpose(post)
        post=post.astype(str)
        post = np.insert(post,0,"post_mean")

        if debug:
            print("averaged frame 1-",interval-grace, "as pre, and ",interval+duration+grace, "-",duration + 2*interval,"as post")
            print("for stimulus:",stimName[stim_index[i]])

        #put them all together
        if i==0:
            out = np.vstack((croppedData[0,:],name,start_head,end_head,pre,post,croppedData[1:,:]))
            stripped = croppedData
        else:
            temp=np.vstack((croppedData[1,:],name,start_head,end_head,pre,post,croppedData[:,1:]))
            out=np.hstack((out,temp[...,1:]))
            stripped = np.hstack((stripped,croppedData[...,1:]))
        

    np.savetxt(splPATH +"full Peri-stim "+postfix+".csv",out, delimiter=',', comments='', fmt='%s')

    #### calculate median,mean and 95 percentile (2.5%-97.5%) for stripped dataset
    y,x=stripped.shape
    summary_stripped = [postfix+"_mean_"+planeNumber,postfix+"_median_"+planeNumber,"lower 95 range","upper 95 range"]
    for i in range(1,y):
        data=stripped[i,1:] # remove the first column b/c it'll be the frame number
        data=data.astype(float)    
        
        if debug and i%1000 == 1:
            # print out every 10000 frames
            print("reaching i=",i,"out of",y) 
            print("max signal in this frame:", np.max(data))

        #calculate upper and lower limit of 95 percentile (2.5%-97.5%)
        l = np.percentile(data, 2.5)
        u = np.percentile(data, 97.5)
        mean = np.mean(data)
        median = np.median(data)
        summary_stripped=np.vstack((summary_stripped,[mean,median,l,u]))

    np.savetxt(splPATH +"_avg Peri-stim "+postfix+".csv",summary_stripped, delimiter=',', comments='', fmt='%s')
    print("wrote to file",splPATH +"_avg Peri-stim "+postfix+".csv")

########### Finish running each individual planes##########

# Run Stitch Files to combine data from all planes
subprocess.run(["python", "StitchFiles.py", "#40", "full Peri-stim "+postfix])

# Load the stitched file and calculate mean, median, 95% range
stitched = np.loadtxt(pathToOutputData + parentFolder + "_"+"full Peri-stim "+postfix + "_Stitched.csv",delimiter=',',dtype=str,ndmin=2)
stitched = Utility.extractData(debug, stitched)
# calculate median, mean, 95% 
print("opening",pathToOutputData + parentFolder + "_"+"full Peri-stim "+postfix + "_Stitched.csv"," with shape=",stitched.shape)

y,x=stitched.shape
summary_stitched = [postfix+"_mean_"+planeNumber,postfix+"_median_"+planeNumber,"lower 95range","upper 95range"]
# i starts at 6 b/c the first 6 columns are mean of pre, post stim, stim name etc.
for i in range(6,x):
    # remove the first column b/c it'll be the frame number
    # not sure why i had to remove the second column as well, but hey, it works
    data=stitched[2:,i] 
    data=data.astype(float)    
    if debug and i%1000 == 1:
        # print out every 10000 frames
        print("reaching i=",i,"out of",y) 
        print("max signal in this frame:", np.max(data))

    #calculate upper and lower limit of 95 percentile (2.5%-97.5%)
    l = np.percentile(data, 2.5)
    u = np.percentile(data, 97.5)
    mean = np.mean(data)
    median = np.median(data)
    summary_stitched=np.vstack((summary_stitched,[mean,median,l,u]))

np.savetxt(pathToOutputData+expNumber +"_allPlanes_avg Peri-stim "+postfix+".csv",summary_stitched, delimiter=',', comments='', fmt='%s')
print("wrote to file",splPATH +"full avg Peri-stim "+postfix+".csv")