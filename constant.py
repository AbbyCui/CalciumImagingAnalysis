"""
This python file include all constants. Change them here, and the changes will apply to all python file that you run afterwards
"""
from scipy import signal
import numpy as np

##################################### BELOW ARE THE MOST IMPORTANT VARIABLES TO MODIFY#####################

#set debug to True to show all debugging statements, and set to False to hide all (also saves time)
debug = False
#set varyingThreshold to have different threshold for each stimuli for each ROI (e.g. 3 ROI x 5 stimuli = 15 different thresholdds)
varyingThreshold = True ##set to True to skip median determination of thresholds
# signal above threshold are considered an event
threshold = 0.3
##Threshold for SD 
SD=5
##Output a third sheet which contains the max amp of all stims regardless of threshold (mostly for finding/validating thresholds)
MaxAll=True
##Set to 1 if you already have smoothed/normalized data and just need to re run thresholds
ThresholdsOnly=1

##Simple AUC calculations. This is just a simple sum of the thresholded frames within a stim window
DO_AUC=True
AUC_threshold=0.3
AUC_norm=True ##whether to divide the total AUC by the duration of stim window (in minutes, so it's AUC/minute)


#folder containing 3 children folder: Data (original data), OutputData(normalized, smoothed, etc. data),
parentFolder = "#462"

#Frame per second for the experiment (used only in Plot.py)
fps = 8.4
# sample spacing
T = 1.0 / fps # 8Hz

#window for normalization
#For a normal recording ~3-400 seconds is fine. For things that last a long time or have prolonged elevations in calcium (4880/GRP) 800 seconds or more seems to be necessary.
timewindow = 800 #This is in seconds
window = (round(timewindow*fps)) #This is in seconds
#percentile of window for normalization
percentile=30 ##depending on how active your cells are, anything from the 5th to 30th percentile is usually fine. 

#window size for smoothing
# this is the window in which the polynomial fits. Larger numbers are more smooth, 
# but can decrease the height of transient peaks. Choose something on the same scale as your events, 
# e.g. if a transient peak lasts around 30 frames, 15 is a good starting point.
window_size = 9
#polynomial order for smoothing
#this is the order of polynomial used for smoothing. 
# Bigger numbers fit the curve more closely (i.e. less smooth, but more accurate)
polynomial = 3

#Size of graph created by Plot.py
SecondsPerInch=50 
##you can go as low as 800 for a compact graph but it'll be hard to read.
# ~300 the bare minimum for 15s VF spacing, but tight, ~50-100 would be better. C
# CICADA is totally readable at 800

#minimum number of frames which meet threshold to be considered a response
#Spike duration of 4 can work well for pharmacology, but should be reduce for natural stimulations. Also consider the frame rate in this. Around a 350ms duration for natural stims seems reasonable (~3 frames at 8hz)
spikeduration=3



#__________________Other variables___________________#

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
stimIndex = 19

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
