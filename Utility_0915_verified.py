import numpy as np
from scipy import signal
from pandas import array, DataFrame
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
    y,x = AllROIsToRemove.shape
    for i in range(x):
        if debug:
            print("i=",i)
            print("this column has:",AllROIsToRemove[...,i])
        if AllROIsToRemove[0,i] == plane:
            ROIsToRemove = []
            for ROI in AllROIsToRemove[1:,i]:
                if ROI != "":
                    np.append(ROIsToRemove,int(ROI))
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
            if debug:
                print("ROIS=",ROI)
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

    data = extractData(debug, data, ROIs = constant.ROIs, stimStart = baselineStart, stimEnd = baselineEnd)
    y,x = data.shape
    baselineSD = np.zeros((x-1,1), dtype=float, order='C')
    for i in range(1,x):
        if debug:
            print("i=",i)
        signal = data[1:,i].astype(float, copy=False)
        #starts at index 0
        baselineSD [i-1,0] = statistics.stdev(signal)
        if debug:
            print("i=",i)
            print("baselineSD  =",baselineSD[i-1,0])

    return baselineSD

def getBaselineMean(debug,data,baselineStart = 1,baselineEnd = 240):
    '''
    Gets the mean of baseline (often the first recording in the experiment)
    input: smoothed data, the start and the end of baseline recording (in frames)
    output: a single column nd.array with no headers
    '''
    if debug:
        print("----------getBaselineMean----------")

    data = extractData(debug, data, ROIs = constant.ROIs, stimStart = baselineStart, stimEnd = baselineEnd)
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

def getAllThresholds(debug,data,threshold = 0.5 ,baselineStart = 1, baselineEnd = 240):
    '''
    Get the threshold for each ROI
    Threshold is 0.5 or mean + 4*SD, whichever is larger
    input: smoothed data, the manually determined threshold, the start and the end of baseline recording (in frames)
    output: a single column nd.array with no headers
    '''
    if debug:
        print("----------getAllThresholds function----------")
    y,x = data.shape #has header
    baselineMean = getBaselineMean(debug, data, baselineStart = baselineStart, baselineEnd = baselineEnd)
    baselineSD = getBaselineSD(debug, data,baselineStart = baselineStart, baselineEnd = baselineEnd)
    #intialize AllThresholds
    AllThresholds = np.zeros((x-1,1), dtype=float)

    for i in range(1,x):
        thisBaselineSD = baselineSD[i-1]
        thisBaselineMean = baselineMean[i-1]
        if debug:
            print("i=",i)
            print("mean =",thisBaselineMean)
            print("SD =",thisBaselineSD)
            print("mean + 4 SD=",thisBaselineMean + 4*thisBaselineSD)
        if threshold > thisBaselineMean + 4*thisBaselineSD:
            thisThreshold =threshold
            AllThresholds[i-1,0]=thisThreshold
        else:
            thisThreshold = thisBaselineMean + 4*thisBaselineSD
            AllThresholds[i-1,0]=thisThreshold

        if debug:
            print("This threshold is:",thisThreshold)
    return AllThresholds

def extractEvent(debug,data,threshold,baselineStart,baselineEnd):
    """
    extract the start and end of each event, as well as a dataframe with 1s representing frames above threshold and 0s representing frames below threshold
    Input np.array of all ROIs with headers, threshold
    Outputs Starts and Ends as np.array with the same dimensions as data, but with zeros as headers, and frame number of start and end of each event for each ROI
    also output spikesInOnes with the same dimensions and headers as data, but each value are mutated to 1 if the value is above threshold, or 0 if below
    """
    if debug:
        print("----------eventCounter function----------")

    #get threshold for all ROIs
    AllThresholds = getAllThresholds(debug, data,threshold,baselineStart, baselineEnd)
    # spikeInOnes have the same dimensions and headers as data, but filled with zeros (below threshold) or ones (above threshold)
    spikesInOnes = np.zeros_like(data)
    spikesInOnes[...,0] = data[...,0] ##adding  the first column - frame number
    spikesInOnes[0,...] = data[0,...] #adding back the first row - ROIs 
    ys,xs = data.shape
    # startsAndEnds have the same dimensions and headers as data, but filled with tuples of (start,end) frame numbers for each event
    Starts = np.zeros_like(data,dtype = float)
    Ends = np.zeros_like(data,dtype = float)
    if debug:
        print("ys =",ys)
        print("xs =",xs)
        print("initialized spikesInOnes with the second row:",spikesInOnes[1,...])

    for x in range(1,xs): #for each ROI
        event = 0 #initialize event number as 0
        thisThreshold = AllThresholds[x-1]
        if debug:
            print("x =",x)
            print("this threshold =",thisThreshold)
        for y in range(1,ys):
            thisData = float(data[y,x]) #extract raw data and change to float
            if thisData>thisThreshold:
                spikesInOnes[y,x] = 1
                # if the prior frame is 0 (smaller than threshold)
                try:
                    if int(spikesInOnes[y-1,x]) == 0:
                        start = y
                        if debug:
                            print("start =",start)
                # if the prior frame doesn't exist, then this is the first row/frame
                except:
                    if debug:
                        print("reached the first or the last row")
                # if this value is smaller than threshold
                try:
                    if float(data[y+1,x]) < thisThreshold: 
                        end = y
                        #if spike lasted for more than 4 frames, count as an event
                        if end-start >= 4:
                        #after a spike ends, add start and finish to startsAndEnds as a tuple
                            event += 1
                            Starts[event,x] = start
                            Ends[event,x] = end
                            if debug:
                                print("event =",event)
                                print("end =",end)
                            #then reset start and end
                            start = 0
                            end = 0
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
    dataStart = data[1,0]
    #initialize eventAmp
    eventAmp = np.zeros_like(data,dtype = float)
    # for each ROI
    for i in range(1,x+1):
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
            if start >= int(float(stimStart)) and end <= int(float(stimEnd)):
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
