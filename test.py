import numpy as np
import Utility_working as Utility #custom-made utility file, contains lengthy functions
from constant import *

frAboveThreshold = np.loadtxt(pathToOutputData + prefix + "Frames_above_Threshold.csv", delimiter=',',dtype=str)
SpikeMid = np.loadtxt(pathToOutputData + prefix + "Spike_Median.csv", delimiter=',', dtype=str)
Starts = np.loadtxt(pathToOutputData + prefix + "Starts.csv", delimiter=',',dtype=str )[1:,1:]

Starts = Starts.astype('float')



std = np.std(Starts,axis = 1)
print(std)