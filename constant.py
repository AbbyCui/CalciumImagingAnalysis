"""
This python file include all constants. Change them here, and the changes will apply to all python file that you run afterwards
"""
from scipy import signal
import numpy as np

##################################### BELOW ARE THE MOST IMPORTANT VARIABLES TO MODIFY#####################
"""MetaData"""
parentFolder = "#541" #folder containing 3 children folder: Data (original data), OutputData(normalized, smoothed, etc. data),
fps = 12.9 #Frame per second for the experiment (used only in Plot.py)

"""Normalization settings"""
ThresholdsOnly=0 ##Set to 1 if you already have smoothed/normalized data and just need to re run thresholds
timewindow = 400 #This is the window for rolling ball normalization in seconds
#For a normal recording ~3-400 seconds is fine. For things that last a long time or have prolonged elevations in calcium (4880/GRP) 800 seconds or more seems to be necessary.
percentile=30 #percentile of window for normalization ##depending on how active your cells are, anything from the 5th to 30th percentile is usually fine. 
splitnorm=1 ##function to normalize individual recordings to help with changes in brightness between sessions 

"""Smoothing"""
window_size = 7 #window size for smoothing. Larger is more smooth. 15 window and 3rd order is ok for gcamp6s smoothing.
polynomial = 6 #polynomial order for smoothing. Smaller is more smooth 6th seems to be better for 8s with the fast kinetics.
# Choose something on the same scale as your events
# e.g. if a transient peak lasts around 30 frames, 15 is a good starting point.

"""Event Detection settings"""
varyingThreshold = False ##set to True to have each stimulation have it's own distinct threshold (not recommended)
threshold = 0.2 # signal above threshold are considered an event
pharmthreshold = 0.4 ##this is a secondary threshold which you can use to differentiate cutaneous vs pharmacological stimuli
SD=5 ##Threshold for SD 

MinimumDuration=0.25 #This is the duration (in seconds) for detecting transients, e.g. it needs to last at least this long to be detected
#for 6s 0.5 second is usually fine. For 8s, 0.25 seconds is ok, could be shorter, but gets noisy.
spikeduration=round(fps*MinimumDuration) #minimum width of event to be considered a response. 
#Note that this is the width, not the number of frames. e.g. there are 4 frames above threshold (e.g. frame 100 (start) through 103 (end)) but, the end-start=3 and this is what this is checking.
#Spike duration of 4 can work well for pharmacology, but should be reduced for natural stimulations. Also consider the frame rate in this, e.g. around a 350ms duration for natural stims seems reasonable (~4 frames at 8hz) but lower FPS means 4 frames at 4hz twice as long.

"""Analysis/Quantification Settings"""
MaxAll=True ##Output a third sheet which contains the max amp of all stims regardless of threshold (mostly for finding/validating thresholds)

DO_AUC=True##This uses the Events (starts/stops) to find events and then only calculates AUC of the detected events
AUC_norm=False ##whether to divide the total AUC by the duration of stim window (in minutes, so it's AUC/minute)
#of note, the AUC will be limited to the stimwindow, i.e. if the decay/calcium lasts longer than the window it will underestimate the AUC

Avg_c = 6 ##Amount of averaging to do (relates to Rename20xavg script and tempalte matching)
minPlane = 1 #1st plane which is present. Use literal nubmers, e.g. Plane0=0 and Plane 1=1
maxPlane = 4  #last plane which is present

"""__________________Other variables___________________"""
#set debug to True to show all debugging statements, and set to False to hide all (also saves time)
debug = False
debugCSV = False ##this is just outputting the various other CSVs for debugging or checking, e.g. Event Start and Stop Times, good/bad thresholds, etc

"""Plotting settings"""
#Size of graph created by Plot.py
SecondsPerInch=200 
##you can go as low as 800 for a compact graph but it'll be hard to read.
# ~300 the bare minimum for 15s VF spacing, but tight, ~50-100 would be better. C
# CICADA is totally readable at 800

#to be added to each file name
planeNumber= "P0"

#start of the stimulus (in frames, cannot be 0, must be >=1)
#input stimStart = "all" if want the entirety of the recording
stimStart = 1

#if want the entirety of the recording, input stimEnd = "all"
#if exceed max frame number, automatically take the 
# stimEnd = 2000*7.4
stimEnd = "all"

#start of baseline
baselineStart = 1

#end of baseline (used to measure noise)
baselineEnd = 2000

#ROIs of interest if say np.arrange (1,3), then will only include ROI 1 and 2
# ROIs = np.array([52,53])
ROIs = 'all'

######### for SpikePattern.py ###########
#user-defined index of stimulus to look at (based off of stimulus.csv). 
stimIndex = 1

##############################################################################################################

expNumber = parentFolder
#path to raw data

pathToRaw = "../"+parentFolder+"/Data/"+parentFolder+"_"+planeNumber+"_"
# directory = '../#2_Data/#2_P0_Results.csv'

pathToData = "../"+parentFolder+"/Data/"+parentFolder+"_"
# directory = ../#2_Data/#2_

pathToOutputData = "../"+parentFolder+"/"+"OutputData/"
# OutPath = '../#2_Output/'

pathToFigure = "../"+parentFolder+"/"+"Figure/"

#the prefix to add before all OutputData and Figures
prefix = expNumber + "_" + planeNumber+"_" 

#the prefix excluding frame number
splPrefix = expNumber + "_" + planeNumber+ "_"


#Design a digital low-pass filter at 4Hz to remove frequencies faster than 4Hz
sos = signal.butter(N = 10,Wn = 4, btype = 'lowpass', fs=8.2, output='sos') 

window = (round(timewindow*fps)) #This converts the seconds to frames

# sample spacing
T = 1.0 / fps # 8Hz
