import Utility_working as Utility #custom-made utility file, contains lengthy functions
from constant import *
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

#input: smoothed F/F0 for 5 planes; separate files with headers (ROI names) for each cluster
#output: smoothed F/F0 for each cell in each cluster

#enter parameters
try:
    template_name = sys.argv[1]
    print("using constants from terminal. Template Name is: ",template_name)
except:
    print("Starting TemplateMatching.py with variables in .py file")
    template_name = "#53-55_Ex_ligand_list 12 c"

#only change this if it's not assigned in the constant file
Avg_Amount = str(Avg_c) ##this needs to be a string 
planeRange = range(0,5) #range(1,5) iterates over plane 1,2,3,4

#assign directory based on our standard organization
expNum = str(parentFolder) ##Or you can enter it manually, it just needs to be a string

dir = pathToOutputData ##or you can just enter the file location manually, e.g. E:/#465/#465/OutputData/'  ##where your averaged/smoothed traces are
temp_dir = "../"+parentFolder+"/Data/" ##where your filter files are
output = template_name #specify output file name, or by default use the name of the template CSV
#load files with headers for ROIs to be extracted (e.g. exp456_P1_ROI002)
print(temp_dir + template_name + '.csv')
all_template = np.loadtxt(temp_dir + template_name + '.csv', delimiter=',',comments='%',dtype=str)
n_cluster=all_template.shape[0]-1

for i in range (n_cluster):
    template = all_template[i+1,1:]
    templateName = all_template[i+1,0]
    print(temp_dir,"template number=",i, "template name=",templateName)

    #template = np.loadtxt(ParentDirectory + template_name + ".csv",delimiter=',',dtype=str)

    #res=np.loadtxt("D:/DATA/Calcium Oscillation Data/Figures and source data/4880 CICADA response/ROInames_4880responder.csv",delimiter=',',dtype=str)
    numROI = len(template)


    # import raw data, normalized data, and smoothed data
    for p in planeRange:
        
        filename = expNum+'_P'+str(p)
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
