'''
Stitches up multiple files with the same number of rows, and different columns. Would arrange the files based on file names, then stitch them to the right of each other.
The column names would also be changed to include information (plane number) of the original file.
Can be used for any csv files in OutputData folder, such as SpikePattern, and MaxResponse
'''

import Utility_working as Utility #custom-made utility file, contains lengthy functions
import numpy as np
import sys
import os
from constant import *

correct = 'y'
parentFolder = sys.argv[1]
FileName = sys.argv[2]
#if not the right arguments passed, ask for user input
try:
    parentFolder = sys.argv[1]
    FileName = sys.argv[2]
    path = "../"+parentFolder+"/"+"OutputData/"
    foundFiles = [f for f in os.listdir(path) if f.endswith(FileName+'.csv')]
except:
    correct = 'n'

# get user input of the parent folder and file name
while correct == 'n' or correct =='N':
    parentFolder = input("Input parent folder (e.g.'#468'): ")
    FileName = input("Input file name here (e.g. 'SpikePattern'): ")
    path = "../"+parentFolder+"/"+"OutputData/"
    foundFiles = [f for f in os.listdir(path) if f.endswith(FileName+'.csv')]
    print(foundFiles)
    correct = input("Are these the file you want to merge? (y, n or q(quit)")
    if correct == "q" or correct == "Q" or correct == "quit":
        break 

counter = 0

if correct == 'y' or correct == "Y":
    for f in foundFiles:
        counter += 1
        planeNum = f.split("_")[1]
        #import file, and change column names to PlaneNumber_Mean+ROInumber (e.g. P2_Mean1)
        file = np.loadtxt(str(path+f),delimiter=',',dtype=str)
        for i in range(len(file[0,1:])):
            ROIname=file[0,i+1]
            ROInumber=ROIname.replace("Mean","")
            ROInumber=int(ROInumber)
            ROInumber = f'{ROInumber:03d}'
            file[0,i+1] = parentFolder + "_" + planeNum+"_"+"ROI"+ROInumber
        #first file
        if counter == 1:
            output = file
        else:
            output = np.hstack((output,file[...,1:]))
    output=np.transpose(output)
    np.savetxt(pathToOutputData + parentFolder + FileName + "_Stitched.csv", output, delimiter=',', comments='', fmt='%s')
