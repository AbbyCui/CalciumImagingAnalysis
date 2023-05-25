import numpy as np
from scipy import signal
from numpy import trapz
from pandas import array, DataFrame, cut
import statistics
import constant as constant

def importDataFile (debug, directory):
    """
    Imports smoothed data from the google notebook.
    Input directory of the data file (relative path).
    Returns full dataset as array.
    """
    #create global variable to to be accessibel to all functions
    global Time
    global TotalROIs

    f = np.loadtxt(directory,delimiter=',',dtype=str)  ##import the csv to a str using loadtxt
    Time, ROIs=f.shape ##get the dimensions of array [1st, 2nd]
    ROIs=ROIs-1
    ROInames=f[0,...]
    data=f[1:,...]
    data=data.astype(float, copy=False)  ##after striping the names then convert to float
    Time, ROIs = data.shape ##get the dimensions of array [1st, 2nd]
    TotalROIs = ROIs-1 # 
    output = np.vstack((ROInames,data))

    ##Inspect the raw traces if desired
    if debug:
        print("----------importData function----------")
        print("data type:",data.dtype) ##for debugging
        print("data shape:",data.shape) ##for debugging
        print("# of ROIS:",TotalROIs)
        print("# of Time Points:",Time)
    return output, Time, TotalROIs

def getROIsToRemove(debug,AllROIsToRemove,plane):
    """
    get the ROIs to be removed from this plane
    Input: AllROisToRemove have the first row with plane names "P0" etc. Plane is a string (e.g. "P0"). 
    Output: 
    """
    if debug:
        print("----------getROIsToRemove----------")
        print("shape of AllROIsToRemove is:", AllROIsToRemove.shape)
    
    #define x = number of planes in AllROIsToRemove csv
    try: # if error out, AllROIsToRemove has 1 colomn 
        x = np.array(AllROIsToRemove).shape[1]
    except:
        x = 1

    if x == 1:
        ROIsToRemove = []
        for ROI in AllROIsToRemove[1:]:
            if ROI != "":
                ROIsToRemove.append(int(ROI))
        return ROIsToRemove

    # for each plane in AllROIsToRemove.csv
    for i in range(x):
        if debug:
            print("i=",i)
            print("this column has:",AllROIsToRemove[...,i])
        if str(AllROIsToRemove[0,i]) == str(plane):
            ROIsToRemove = []
            for ROI in AllROIsToRemove[1:,i]:
                if ROI != "":
                    ROIsToRemove.append(int(ROI))
            if debug:
                print("ROIsToRemove =:",ROIsToRemove)
                print("type is:",type(ROIsToRemove))
            return ROIsToRemove
        else:
            if debug:
                print("plane not found")

def extractData (debug, data, ROIs = "all", ROIsToRemove = [], stimStart = 0, stimEnd = "all"):
    """
    Extract desired ROIs and time from data array.
    Input the desired ROIs (can be multiple). If left empty, default to include all ROIs.
    and stimulus start and end time are optional (default to include the entire length of the recording).
    Output the truncated data set as an array that contains ROInames(first row) and frames(first column).
    """
    if debug:
        print("----------extractData function----------")
    #if user did not input stimEnd, then it is equal to the end of the recording (take the entire recording)
    y,x = data.shape
    if str(stimEnd) == "all":
        stimEnd = y-1
    ##ROIdata contains signals for the designated ROI(s)
    stimStart=int(stimStart)
    stimEnd=int(stimEnd)
    ROIsdata = data[stimStart:stimEnd,0] #timepoints
    ROInames = ["Frame",] #initiate new empty array
    #this for loop produces data with the wrong axis (one row for each ROI and one column for each time point)
    if str(ROIs) == "all":
        for ROI in range(1,x):
            if ROI not in ROIsToRemove:
                if debug:
                    print("ROI=",ROI)
                ROIdata = data[stimStart:stimEnd,ROI] #take the ROIth column in the data sheet
                ROIsdata = np.vstack((ROIsdata,ROIdata)) #stack on top
                ROIname = data[0,ROI]
                ROInames = np.append(ROInames,ROIname)
            else:
                if debug:
                    print("ROI in ROIsToRemove",ROI)
    else:
        for ROI in ROIs:
            if ROI not in ROIsToRemove:
                ROIdata = data[stimStart:stimEnd,ROI] #take the ROIth column in the data sheet
                ROIsdata = np.vstack((ROIsdata,ROIdata)) #stack on top
                ROIname = data[0,ROI]
                ROInames = np.append(ROInames,ROIname)
            else:
                if debug:
                    print("ROI in ROIsToRemove",ROI)

    output = ROIsdata.T #correct the axis of the data -> one colum for each ROI
    output = np.vstack((ROInames,output))

    ##see the first 10 elements in ROIdata
    if debug:
        print("first row of output:",output[0,0:9])
        print("first column of output:", output[0:9,0])
        print("second column of output:",output[...,1])
        print("data shape of output:",output.shape)

    return output 

def normalize(debug, data, window, percentile):
    """
    Normalizes data
    input data set (array) with ROInames (first row) and frames (first column), window, and percentile of normalization
    returns array of normalized data
    """
    if debug:
        print("----------normalize function----------")
        print("data input to normalize has shape:",data.shape)
        print("data input to normalize has the first row as:",data[...,0])
    rawdata = data[1:,1:] #only the data, excluding ROInames and frames
    rawdata = rawdata.astype(float, copy=False)
    ROInames = data[0,1:]
    if debug:
        print("ROInames =",ROInames)
        
    TotalROIs = len(ROInames)
    
    #initialize fb, fbtemp and index f
    fb=np.ones_like(rawdata)
    fbtemp=np.ones_like(rawdata[...,0])
    f = 0
    while f<(TotalROIs):
        #print out ROI number for every 10 ROIs
        if debug and f%10 == 0:
            print("normalizing ROI",f)
        halfwindow=int(window/2)
        i=halfwindow
        raw = rawdata[...,f]
        while i<(len(raw)-window):
            aslice=raw[(i-(halfwindow)):(i+(halfwindow))]

            fbtemp[i]=(np.percentile(aslice, percentile)) ##arrayname, percentile between 0-100
            if i==(len(raw)-window-1):
                temp=(np.percentile(aslice, percentile)) ##arrayname, percentile between 0-100
                ii=1
                while ii<(window+1):
                    fbtemp[i+ii]=temp
                    ii+=1
                iii=0
                while iii<(halfwindow):
                    aslice=raw[1:window]
                    temp=(np.percentile(aslice, percentile))
                    fbtemp[iii]=temp
                    iii+=1
            i+=1
        fb[...,f]=fbtemp
        f+=1
    if debug:
        print("data has shape:",rawdata.shape)
        print("fb has shape:",fb.shape)

    fb=fb.astype(float, copy=False)
    rawdata=rawdata.astype(float, copy=False)
    df=np.subtract(rawdata,fb)
    dff=np.divide(df,fb)

    dffT=dff
    if debug:
        print("dff has shape:",dff.shape)
        print("dffT has shape:", dffT.shape)
    # dffT[...,0]=rawdata[...,0] ##adding back the X-axis
    a = np.ones_like(data[1:,...])
    a[...,0]=data[1:,0] ##adding back the X-axis (frames)
    a[...,1:] = dffT
    dffT=a.astype(str, copy=True) 
    titles = np.insert(ROInames,0,"Frame")
    dffT[0,...] = titles
    #dffT=np.insert(dffT, 0, titles, axis=0) ##inserting the titles ("frame" and ROInames)
    if debug:
        print ("the shape of the normalized data is:", dffT.shape)
        print("ROI names after normalization:", dffT[...,0])
    return dffT

def smooth(debug, data,window_size, polynomial):
    """
    smoothes each ROI data in a data array
    input normalized data as array, window size and polynomial for smoothing
    output smoothed data as array
    """
    smoothed=np.ones_like(data)
    smoothed[...,0] = data[...,0] ##adding  the first column - frame number
    smoothed[0,...] = data[0,...] #adding back the first row - ROIs 
    num_rows, num_cols = data.shape

    if debug:
        print("----------smooth function----------")
        print("data input to smooth function has shape:", data.shape)
        print("data type:", data.dtype)
        print("data frames:", data[...,0])
        print("data ROIs:", data[0,1:])

    #loop through columns to smooth each ROI data
    i=1
    while i< num_cols: #loop for each ROI (except for the first column of frames)
        smoothed[1:,i] = signal.savgol_filter(data[1:,i],window_size, polynomial) # window size 51, polynomial order 3
        i+=1

    return smoothed

def lowPassFilter(debug,data,sos):
    """
    Apply a low pass filter to each row of the np.array
    input np array with headers, and a low pass filter
    outputs np.array with headers with filtered data
    """
    if debug:
        print("----------lowPassFilter function----------")
    filtered = np.ones_like(data)
    filtered[...,0] = data[...,0] ##adding  the first column - frame number
    filtered[0,...] = data[0,...] #adding back the first row - ROIs 
    Time, ROIs=data.shape

    for i in range(1,ROIs):
        if debug:
            print("current i:",i)
        rawsmoothed = data[1:,i].astype(float, copy=False)
        filtered[1:,i] = signal.sosfilt(sos, rawsmoothed)

    if debug:
        print("data input to smooth function has shape:", filtered.shape)
        print("data type:", filtered.dtype)
        print("data frames:", filtered[...,0])
        print("data ROIs:", filtered[0,1:])
    return filtered

def getBaselineSD(debug,data,baselineStart = 1,baselineEnd = 240):
    """
    Gets the standard deviation of baseline (often the first recording in the experiment)
    input: smoothed data, the start and the end of baseline recording (in frames)
    output: a single column nd.array with no headers
    """
    if debug:
        print("----------getBaselineSD----------")

    data = extractData(debug, data, ROIs = "all", stimStart = baselineStart, stimEnd = baselineEnd)
    y,x = data.shape
    baselineSD = np.zeros((x-1,1), dtype=float, order='C')
    for i in range(1,x):
        if debug:
            print("i=",i)
        signal = data[1:,i].astype(float, copy=False)
        #starts at index 0
        baselineSD [i-1,0] = statistics.stdev(signal)

    return baselineSD

def getBaselineMean(debug,data,baselineStart = 1,baselineEnd = 240):
    '''
    Gets the mean of baseline (often the first recording in the experiment)
    input: smoothed data, the start and the end of baseline recording (in frames)
    output: a single column nd.array with no headers
    '''
    if debug:
        print("----------getBaselineMean----------")
        print("baseline start=",baselineStart, "end =",baselineEnd)

    data = extractData(debug, data, ROIs = "all", stimStart = baselineStart, stimEnd = baselineEnd)
    y,x = data.shape
    baselineMean = np.zeros((x-1,1), dtype=float, order='C')
    for i in range(1,x):
        signal = data[1:,i].astype(float, copy=False)
        baselineMean [i-1,0] = statistics.mean(signal)
        if debug:
            print("i=",i)
            print("extracted frome data:",data[0,i])
            print("baselineMean  =",baselineMean[i-1,0])

    return baselineMean

def getStimThresholds(debug,data,baselineStart,baselineEnd,threshold):
    '''
    get the threshold for each ROI for a given stimulus window
    input: smoothed data, the threshold, the start and end of baseline recording (in frames)
    output: a single row of nd.array with no headers
    '''
    if debug:
        print("----------getStimThresholds  function----------")

    y,x = data.shape #has header
    baselineMean = getBaselineMean(debug, data, baselineStart = baselineStart, baselineEnd = baselineEnd)
    baselineSD = getBaselineSD(debug, data,baselineStart = baselineStart, baselineEnd = baselineEnd)
    #intialize AllThresholds
    StimThresholds = np.zeros((1,x-1), dtype=float)
    if debug:
        print("initialized StimThresholds with dimension:",StimThresholds.shape)

    for i in range(1,x):
        thisBaselineSD = baselineSD[i-1]
        thisBaselineMean = baselineMean[i-1]
        if threshold > thisBaselineMean + constant.SD*thisBaselineSD:
            thisThreshold =threshold
            StimThresholds[0,i-1]=thisThreshold
        else:
            thisThreshold = thisBaselineMean + constant.SD*thisBaselineSD
            StimThresholds[0,i-1]=thisThreshold
        if debug:
            print("This threshold is:",thisThreshold)
    return StimThresholds

def getAllThresholds(debug,data,stim,fps,threshold):
    '''
    Get the threshold for each ROI
    Threshold is 0.5 or mean + 4*SD, whichever is larger
    input: smoothed data, stimulus file, the manually determined threshold, the start and the end of baseline recording (in frames)
    output: a data frame with x = ROI and y = stimulus (with headers)
    '''
    if debug:
        print("----------getAllThresholds function----------")

    y,x = data.shape #has header
    ys,xs = stim.shape
    AllThresholds = np.empty((ys+1,x),dtype = object)
    AllThresholds[0,...] = data[0,...]
    AllThresholds[1:,0] = stim[...,0]
    if debug:
        print("Allthresholds cols",AllThresholds[...,0])
        print("dimension of stim =",stim.shape)
    #for each stimuli
    for i in range(0,ys):
        stimName = stim[i,0]
        stimStart = int(float(stim[i,1]))
        baselineEnd = stimStart-1
        baselineStart = int(stimStart-1-10*fps)
        StimThresholds = getStimThresholds(debug,data,baselineStart,baselineEnd,threshold)
        AllThresholds[i+1,1:] = StimThresholds
        if debug:
            print("stimName",stimName)

    if constant.varyingThreshold==False:
        if constant.debugCSV:
            np.savetxt(constant.pathToOutputData + "IndividualThresholds (no plane number).csv", AllThresholds, delimiter=',', comments='', fmt='%s') ##saving the non-median'd thresholds for reference
        ThresholdFilt = np.loadtxt(constant.pathToData +"Threshold.csv",delimiter=',',dtype=str) ##import the file for which thresholds to use
        temp=ThresholdFilt[0:,1] #take all the values from the 2nd column which contains which stims to include for median
        RowsToIncludeForMedian = [i for i, row in enumerate(temp) if '1' in row] ##report which rows (from 0 to end) have a 1, e.g. which to include
        if debug:
            print(RowsToIncludeForMedian)
        FilteredThresholds = AllThresholds[0,0:] #create new threshold array in which to place the thresholds post ROI removal
        if debug:
            print("ThresholdFilt Shape",ThresholdFilt.shape)
            print("y,x",y,x)

        for MStim in range(1,(ys+1)): #skip the 0th row because it's the names 
            if MStim in RowsToIncludeForMedian:
                if debug:
                    print("Stimulus Number:",MStim)
                    print("Stimulus Name",ThresholdFilt[MStim,0])
                thisgoodthreshold = AllThresholds[MStim,0:] #take the ROIth column in the data sheet
                if debug:
                    print("shape of this goodthreshold",thisgoodthreshold.shape)
                FilteredThresholds = np.vstack((FilteredThresholds,thisgoodthreshold)) #stack on top
                if debug:
                    print("filtered thresholds shape",FilteredThresholds.shape)
        if constant.debugCSV:
            np.savetxt(constant.pathToOutputData + "FilteredThresholds(no plane number).csv", FilteredThresholds, delimiter=',', comments='', fmt='%s') ##saving the non-median'd thresholds for reference
        for i in range (1,x):
            ROIthreshold = np.median(FilteredThresholds[1:,i])
            AllThresholds[1:,i] = ROIthreshold
            if debug:
                print("varying threshold = False")
        ##part 2 which involves setting the Pharmacology to a minimum of 0.3 (or whatever is set)
        temp=ThresholdFilt[0:,2] #take all the values from the 2nd column which contains which stims to include for median
        RowsToIncludeForPharm = [i for i, row in enumerate(temp) if '1' in row] ##report which rows (from 0 to end) have a 1, e.g. which to include
        if debug:
            print(RowsToIncludeForPharm)
        for MStim in range(1,(ys+1)): ##skip the 0th row because it's the names 
            if MStim in RowsToIncludeForPharm:
                for i in range(1,x):
                    thisThreshold = AllThresholds[MStim,i]
                    if thisThreshold<0.3:
                        AllThresholds[MStim,i]=constant.pharmthreshold
                if debug:
                    print("shape of temp",temp.shape)
        if debug:
            print(RowsToIncludeForPharm)
    return AllThresholds
    
def extractEvent(debug,data,stim,AllThresholds):
    """
    extract the start and end of each event, as well as a dataframe with 1s representing frames above threshold and 0s representing frames below threshold
    Input np.array of all ROIs with headers, threshold
    Outputs Starts and Ends as np.array with the same dimensions as data, but with zeros as headers, and frame number of start and end of each event for each ROI
    also output spikesInOnes with the same dimensions and headers as data, but each value are mutated to 1 if the value is above threshold, or 0 if below
    """
    if debug:
        print("----------eventCounter function----------")

    # spikeInOnes have the same dimensions and headers as data, but filled with zeros (below threshold) or ones (above threshold)
   
    doublesmoothed=np.zeros_like(data,dtype = float)
    num_rows, num_cols = data.shape

    if debug:
        print("----------smooth function----------")
        print("data input to smooth function has shape:", data.shape)
        print("data type:", data.dtype)
        print("data frames:", data[...,0])
        print("data ROIs:", data[0,1:])

    #loop through columns to smooth each ROI data
    i=1
    while i< num_cols: #loop for each ROI (except for the first column of frames)
        doublesmoothed[1:,i] = signal.savgol_filter(data[1:,i],41, 2) # this is fairly aggresive smoothing for 8hz intended to smooth out any noise to use with the stops only
        i+=1
    
    if constant.debugCSV:
        np.savetxt(constant.pathToOutputData + "DoubleSmoothedForSpikeEnds (lacks plane number).csv", doublesmoothed, delimiter=',', comments='', fmt='%s')
   
    spikesInOnes = np.zeros_like(data)
    spikesInOnes[...,0] = data[...,0] ##adding  the first column - frame number
    spikesInOnes[0,...] = data[0,...] #adding back the first row - ROIs 
    ys,xs = data.shape
    stimNum = stim.shape[0]-1
    # startsAndEnds have the same dimensions and headers as data, but filled with tuples of (start,end) frame numbers for each event
    Starts = np.zeros_like(data,dtype = float)
    Ends = np.zeros_like(data,dtype = float)
    if debug:
        print("ys =",ys)
        print("xs =",xs)
        print("initialized spikesInOnes with the second row:",spikesInOnes[1,...])
    
    for x in range(1,xs): #for each ROI
        lastend=0
        event = 0 #initialize event number as 0
        s = 0 # initialize stimlus index as 1 *this was abby's code. I think it needs to be 0 because the stim array has no title so this is skipping the 1st stim row
        for y in range(1,ys): #for each frame in this ROI
            lastend=np.max(Ends[:,x])
            if y<=(lastend+1):##this needs to be plus one, because the y+1 was set as zero based on the smoothed data. Edge cases require this.
                if debug:
                    print("Skipping this frame: value of y",y," Value of Ends",lastend)
            else: 
                thisData = float(data[y,x]) #extract raw data and change to float
                #determine threshold based on which stimuli this current frame is in
                for i in range(s,stimNum):
                    if y >= float(stim[i,1]) and y <= float(stim[i,2]):
                        s = i
                        break
                st=s+1 #this needs to be +1 relative to the stim array as it contains the title row
                thisThreshold = float(AllThresholds[st,x])
                if debug:
                    print("ith stim is",s,"time",y,"x",x,"thisthresh",thisThreshold)
                # find events
                if thisData>thisThreshold:
                    spikesInOnes[y,x] = 1
                    # if the prior frame is 0 (smaller than threshold)
                    try:
                        if int(spikesInOnes[y-1,x]) == 0:
                            start = y
                            maxvalue=thisData
                            if debug:
                                print("Start is assigned at Current frame",y,"prior frame is a 0",maxvalue,"at ROI/column",x)
                        else:
                            if thisData>maxvalue:
                                maxvalue=thisData
                                if debug:
                                    print("maxvalue is being overwritten as",maxvalue)
                    except:
                        print("reached the first or the last row, this has something to do with stims being active at the first frame. Otherwise it might be supressing a silent error.")
                        print("ith stim is",s,"time",y,"x",x,"thisthresh",thisThreshold)
                        print("Start is assigned at Current frame",y,"prior frame is a 0",maxvalue,"at ROI/column",x)
                    # if the prior frame doesn't exist, then this is the first row/frame
                    # if this value is smaller than threshold
                    try:
                        if float(data[y+1,x]) < thisThreshold: ##if the next frame is expected to be a 0
                            end = y
                            #if spike lasted for more than 4 [ or the variable spikeduration] (variable name) frames, count as an event
                            if end-start >= constant.spikeduration:
                            #after a spike ends, add start and finish to startsAndEnds as a tuple
                                varThreshold=max(thisThreshold*.6,.15)
                                if float(doublesmoothed[y+1,x]) < varThreshold:
                                    event += 1
                                    Starts[event,x] = start
                                    Ends[event,x] = end
                                    spikesInOnes[y+1,x] = 0
                                    #then reset start and end
                                    #print("for frame=",y,"in column(ROI)",x,"final maxvalue for x5 or mean6",maxvalue)
                                    start = 0
                                    end = 0
                                    maxvalue=0
                                else:
                                    while float(doublesmoothed[y+1,x]) > varThreshold:
                                        spikesInOnes[y+1,x] = 1
                                        end=y
                                        y=y+1
                                    else:
                                        event += 1
                                        Starts[event,x] = start
                                        Ends[event,x] = end
                                        #then reset start and end
                                        #print("for frame=",y,"in column(ROI)",x,"final maxvalue for x5 or mean6",maxvalue)
                                        spikesInOnes[y,x] = 0
                                        spikesInOnes[y+1,x] = 0
                                        start = 0
                                        end = 0
                                        maxvalue=0
                    except:
                        if debug:
                            print("reached the first or the last row")
                else: 
                    spikesInOnes[y,x] = 0
    if debug:
        print("Starts has shape:",Starts.shape)
        print("Ends has shape:",Ends.shape)
    return Starts, Ends
   
def eventCounter (debug, Starts):
    """
    input dataframe with headers (zeros) with the frame number of the start of each event
    output dataframe with single column, listing the number of events for all ROIs
    """
    if debug:
        print("----------eventCounter function----------")
    y , x = Starts.shape
    eventNumber = np.zeros((x-1,1), dtype=int, order='C')
    #count the number of starts for each ROI to get the number of events
    for i in range(1,x):
        eventNumber[i-1,0] = int(np.count_nonzero(Starts[...,i]))
        if debug:
            print("i=",i)
            print("event number =",eventNumber[i-1,0])
    return eventNumber

def ISI (debug,data,Starts):
    """
    input dataframe with ROIs of interest with smoothed signal
    also input Starts and Ends with zeros as headers, and filled with frame number of the start and end of each event
    output a datafram with zeros as headers, filled with the number of frames between each two consequtive events
    """
    if debug:
        print("----------ISI function----------")
    # convert Starts to pandas dataframe in order to use diff funciton in pandas package
    Starts = DataFrame(Starts)
    # because Starts has zeros as headers, ISI[1,...] = Starts[1,...]
    # because the rest of the dataframe is filled with zeros, the value below the last start time of each ROI is also zero
    # so each column would end with a negative value
    ISI = Starts.diff(axis=0)
    ISI = ISI[ISI>=0] # remove negative values
    ISI = ISI.fillna(0) #fill na. with zeros
    return ISI

def getEventAmp(debug,data,Starts,Ends):
    """
    get the amplitude of events
    input original data frame with headers, and the starts and ends data frame with headers as zeros
    output a dataframe with the amplitude of each event
    """
    if debug:
        print("----------getEventAmp function----------")
    #get dimension of data
    y,x = data.shape
    #get the starting frame of data
    dataStart = int(float(data[1,0]))
    #initialize eventAmp
    eventAmp = np.zeros_like(data,dtype = float)
    # for each ROI
    for i in range(1,x):
        #if the last frame is above threshold, there will be more values in "starts" than "ends" for this ROI
        numStart = np.count_nonzero(Starts[...,i])
        numEnd = np.count_nonzero(Ends[...,i])
        if numStart > numEnd:
            #if more starts than ends, add a value to ends = the last frame of the recording
            Ends[numEnd+1,i] = data[y-1,0]
        elif numEnd>numStart:
            Starts[1,i] = 1
        #for each event
        for j in range (1,numStart+1):
            start = int(Starts[j,i]) + dataStart
            end = int(Ends[j,i]) + dataStart
            if debug:
                print("the event occured at frame",start + constant.stimStart,"to",end + constant.stimStart)
                print("the signal is:",data[start:end+1,i])

            maxSignal = max(data[start:end+1,i])
            if debug:
                print("max sig=",maxSignal)
            eventAmp[j,i] = maxSignal
    
    return eventAmp
    
def getMaxResponse (debug,data,stimStart,stimEnd,Starts,Ends):
    '''
    Get the max response of each ROIs for ONE stimulus with defined start and end
    Input: smoothed data, int for the start and the end of the stimulus,
        and Starts and Ends dataframe with the starting and ending frames for each event
    Output: maxResposne dataframe with 1 row, and the same number of columns the number of ROIs (no header)
    '''
    if debug:
        print("----------getMaxResponse function----------")
    #get dimension of data
    y,x = data.shape
    #get the starting frame of data
    dataStart = int(float(data[1,0]))
    #initialize maxResponse with 2 rows, and the same number of columns as data
    maxResponse = np.zeros((1,x-1))
    # for each ROI
    for i in range(1,x):
        #if the last frame is above threshold, there will be more values in "starts" than "ends" for this ROI
        numStart = np.count_nonzero(Starts[...,i])
        numEnd = np.count_nonzero(Ends[...,i])
        curr_maxResponse = 0.0
        # fill up starts and ends to give them the same lengths
        if numStart > numEnd:
            #if more starts than ends, add a value to ends = the last frame of the recording
            Ends[numEnd+1,i] = data[y-1,0]
        elif numEnd>numStart:
            Starts[1,i] = 1
        # for each event in Starts/Ends
        for j in range (1,numStart+1):
            start = int(Starts[j,i]) + dataStart
            end = int(Ends[j,i]) + dataStart
            # if this event occured during the stimulation window
            if (start >= int(float(stimStart)) and start<= int(float(stimEnd))):
                if debug:
                    print("current start and end:",start,end)
                maxSignal = max(data[start:end+1,i])
                if float(maxSignal) > float(curr_maxResponse):
                    curr_maxResponse = maxSignal
                if debug:
                    print("max sig=",maxSignal)
                    print("curr_maxResponse =",curr_maxResponse)
        
        maxResponse[0,i-1] = curr_maxResponse
    
    return maxResponse

def getSpikePattern (debug,data,AllThresholds,Starts,binSize):
    '''
    input data frame trimmed to the desired window, all ROI's threshold during this stimuli, and a dataframe of start of all events within the stimulus window
    output the AUC of that portion of data above the threshold (the area under the entire curve, not normalized by time), the SD and median of the start time of events
    '''
    if debug:
        print("----------getAUC function----------")

    y,x = data.shape
    remainder = (y-1) % round(binSize)
    data = data[:-remainder,...]
    y,x = data.shape
    ROInames = data [0,1:]
    if debug:
        print("the shape of data input: y=",y,"x=",x)
    
    #loop through all ROIs
    SpikePattern = np.empty((4,x),dtype = object)
    for ROI in range(1,x):
        ROIthreshold = float(AllThresholds[1,ROI])
        ROIdata = data[1:,ROI]
        ROIstart = np.array(Starts[1:,ROI])
        if max(ROIstart) != 0:
            ROIstart = ROIstart[ROIstart != 0]

        ROIdata = [float(item)-ROIthreshold for item in ROIdata] #change to float and subtract threshold
        ROIdata = [0 if i < 0 else i for i in ROIdata] #make all negative values = 0 (below threshold = zero)

        #AUCs
        #for all elements in ROIdata that is bigger than the threshold, subtract the threshold from them, then take the sum
        SpikePattern[1,ROI] = sum(ROIdata) #AUC

        #timing of starts
        SpikePattern[2,ROI] = np.std(ROIstart) #how spread out the peaks are
        SpikePattern[3,ROI] = np.median(ROIstart) #where does most peaks happen

        #average into 1min bins
        ROIdata = np.array(ROIdata)
        avgROI = np.average(ROIdata.reshape(-1, round(binSize)), axis=1)

    #add in headers
        rowNames = np.array(["AUC","sd of spike time","median of spike time"]) #list
        SpikePattern[1:,0] = rowNames
        SpikePattern[0,1:] = ROInames
    return SpikePattern

def getMaxResponseAll (debug,data,stimStart,stimEnd,Starts,Ends):
    '''
    Get the max response of each ROIs for ONE stimulus with defined start and end
    Input: smoothed data, int for the start and the end of the stimulus,
        and Starts and Ends dataframe with the starting and ending frames for each event
    Output: maxResposne dataframe with 1 row, and the same number of columns the number of ROIs (no header)
    '''
    if debug:
        print("----------getMaxResponse function----------")
    #get dimension of data
    y,x = data.shape
    #initialize maxResponse with 2 rows, and the same number of columns as data
    MaxResponseAll = np.zeros((1,x-1))
    # for each ROI
    c=1
    while c<(x):
        yrange=y-1
        temp = data[1:y,c]
        if(debug==1):
            print(temp[0])
            print(temp.shape)
            print(type(temp))
        stimwindow=temp[stimStart:stimEnd]
        stimwindow=stimwindow.astype(float)  
        tempmax=np.max(stimwindow)
        if(debug==1):
            print(tempmax)
            print(tempmax.shape)
            print(type(tempmax))
        MaxResponseAll[0,(c-1)]=tempmax
        c+=1
    return MaxResponseAll

def getAUCv0 (debug,data,stimStart,stimEnd,Starts,Ends):
    '''
    Get the AUC  of each ROIs for ONE stimulus with defined start and end
    Input: smoothed data, int for the start and the end of the stimulus,
        and Starts and Ends dataframe with the starting and ending frames for each event
    Output: AUC dataframe with 1 row, and the same number of columns the number of ROIs (no header)
    '''
    if debug:
        print("----------getAUC function----------")
    #get dimension of data
    y,x = data.shape
    #initialize maxResponse with 2 rows, and the same number of columns as data
    AUC = np.zeros((1,x-1))
    # for each ROI

    c=1
    arrayx=np.zeros(y)
    while c<(x):
        yrange=y-1
        temp = data[1:y,c]
        if(debug==1):
            print(temp[0])
            print(temp.shape)
            print(type(temp))
        stimwindow=temp[stimStart:stimEnd]
        stimwindow=stimwindow.astype(float)
        duration=(((len(stimwindow))/constant.fps)/60)
        AUCtemp=0
        for frames in stimwindow:
            if (frames>constant.AUC_threshold):
                AUCtemp=AUCtemp+frames
        if(constant.AUC_norm==True):
            AUC[0,(c-1)]=(AUCtemp/duration)
        else: AUC[0,(c-1)]=AUCtemp
        c+=1
    return AUC

def getAUC (debug,data,stimStart,stimEnd,Starts,Ends):
    '''
    Get the AUC  of each ROIs for ONE stimulus with defined start and end
    Input: smoothed data, int for the start and the end of the stimulus,
        and Starts and Ends dataframe with the starting and ending frames for each event
    Output: AUC dataframe with 1 row, and the same number of columns the number of ROIs (no header)
    '''
    if debug:
        print("----------getAUC function----------")
    #get dimension of data
    y,x = data.shape
    stimwindow=(stimEnd-stimStart)
    duration=(((stimwindow/constant.fps)/60)) ##this is in minutes
    #get the starting frame of data
    dataStart = int(float(data[1,0]))
    #initialize AUCTotal with 2 rows, and the same number of columns as data
    AUCTotal = np.zeros((1,x-1))
    AvgAmplitude = np.zeros((1,x-1))
    AvgEventWidth = np.zeros((1,x-1))
    NumEvents = np.zeros((1,x-1))

    # for each ROI
    for i in range(1,x):
        #if the last frame is above threshold, there will be more values in "starts" than "ends" for this ROI
        numStart = np.count_nonzero(Starts[...,i])
        numEnd = np.count_nonzero(Ends[...,i])

        curr_NumEvents = 0
        curr_AUC = 0.0
        curr_AvgAmplitude = 0.0
        curr_EventWidth = 0.0

        # fill up starts and ends to give them the same lengths
        if numStart > numEnd:
            #if more starts than ends, add a value to ends = the last frame of the recording
            Ends[numEnd+1,i] = data[y-1,0]
        elif numEnd>numStart:
            Starts[1,i] = 1
        # for each event in Starts/Ends
        for j in range (1,numStart+1):
            start = int(Starts[j,i]) + dataStart
            end = int(Ends[j,i]) + dataStart
            # if this event occured during the stimulation window
            ############Part1: checks for a start within the stim window and extracts the appropriate frames (i.e. those that occur during the window) into the array tdata
            if (start >= int(float(stimStart)) and start<= int(float(stimEnd))): ## this changed from the typical as I only ever want to count each spike once (e.g. for back to back windows) so only the start is considered
                if ((end-start)>(1500)): ## This makes sure that there aren't any weirdly long events (~>2 minutes long) that suggest a manual check of the data is necessary
                    print("ROI",data[0,i],"has an event between frames",start,"and",end,"which lasts for more than 1500 frames, consider checking raw data")
                if debug:
                    print("current start and end:",start,end)
                curr_NumEvents = curr_NumEvents+1
                if (end >= int(float(stimEnd))):
                    ##if the end of the event outlasts the stimwindow, only extract the stim window for analysis
                    tdata=data[start:stimEnd+1,i]
                    tdata = tdata.astype(float)
                else:
                    tdata=data[start:end+1,i]
                    tdata = tdata.astype(float)
                ##once the data is extracted, we evaluated the event and add it to the running total
                area=trapz(tdata,dx=constant.T) ##this uses the trapezoid rule which is more accurate than a simple sum
                curr_AUC = curr_AUC + area
                curr_AvgAmplitude = curr_AvgAmplitude + max(tdata)
                curr_EventWidth = curr_EventWidth + (len(tdata))
            ###########Part2: if there is no start that occurs within the window, it now checks for an end which occurs within the stimwindow
            else:
                if (end >= int(float(stimStart)) and end <= int(float(stimEnd))):
                    tdata=data[stimStart:end+1,i]
                    tdata = tdata.astype(float)
                    curr_NumEvents = curr_NumEvents+1
                    ##evalute the extracted data
                    area=trapz(tdata,dx=constant.T) ##this uses the trapezoid rule which is more accurate than a simple sum
                    curr_AUC = curr_AUC + area
                    curr_AvgAmplitude = curr_AvgAmplitude + max(tdata)
                    curr_EventWidth = curr_EventWidth + (len(tdata))
                else:
                    if (start <= int(float(stimStart)) and end>= int(float(stimEnd))):
                        print("start/stop pair lasts longer than the duration of the stim window for ROI",data[0,i],"at frames",start,"and",end)
                        tdata=data[stimStart:stimEnd+1,i]
                        tdata = tdata.astype(float)
                        curr_NumEvents = curr_NumEvents+1
                        ##evalute the extracted data
                        area=trapz(tdata,dx=constant.T) ##this uses the trapezoid rule which is more accurate than a simple sum
                        curr_AUC = curr_AUC + area
                        curr_AvgAmplitude = curr_AvgAmplitude + max(tdata)
                        curr_EventWidth = curr_EventWidth + (len(tdata))
            if debug:
                print("curr_AvgAmplitude=",curr_AvgAmplitude)
                print("curr_AUC =",curr_AUC)
                

        if(constant.AUC_norm==True):
            curr_AUC = ((curr_AUC)/duration) ##this give AUC per minute
        else: curr_AUC = (curr_AUC)
        if curr_NumEvents==0:
            curr_AvgAmplitude=0
        else: curr_AvgAmplitude = curr_AvgAmplitude/curr_NumEvents
        if curr_NumEvents==0:
            curr_EventWidth=0
        else:curr_EventWidth = ((curr_EventWidth/curr_NumEvents)*constant.T)

        AUCTotal[0,i-1] = curr_AUC
        NumEvents[0,i-1] = curr_NumEvents
        AvgAmplitude[0,i-1] = curr_AvgAmplitude
        AvgEventWidth[0,i-1] = curr_EventWidth

    return AUCTotal,NumEvents,AvgAmplitude,AvgEventWidth
