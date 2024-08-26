**Main**
===

# Calcium Imaging Analysis
These series of scripts takes raw data resulted from FIJI-multi-measure to basic figures, analysis of ISI, max response during each stimuli and responders to each stimuli

## Input data and Folder Structure
Put all scripts in the same folder named whatever you like, e.g. "PythonScripts"

![image](https://user-images.githubusercontent.com/81972652/193971557-d39188fd-2f6d-4e63-a4ad-920e689eeda2.png)

For EACH experiment, make a copy of the folder PythonScripts and place it within a folder (e.g. exp#462). 

![image](https://user-images.githubusercontent.com/81972652/193971950-23060e2c-ea8c-49cc-b026-a2eef60a6295.png)

Then create a folder called the same thing (Exp#462) and within it create a folder called "Data" that contains all results from multi-measure and a .csv file containing the timestamp of each stimuli. Results should be in csv format, and names as **"experimentNumber_PlaneNumber_Results.csv"**, and stimulus file should be named **"ExperimentNumber_Stimulus.csv"**, as shown below. The names of the ROIs (i.e. the first row) cannot have # in it, e.g. Exp#455_P2_001 and should be left as Mean1, Mean2, etc as the outputs will be renamed later.

![image](https://github.com/AbbyCui/CalciumImagingAnalysis/assets/81972652/3bd42cb4-339e-49d4-8b92-307d17e40546)

Inside the stimulus file, columm 1 is the name of each stimuli. **Do no include commas or #!** comma in csv files indicate "next cell" and will not be interpreted as a part of the text. The second and the third columns are the start and end of each stimulus (in frames). Fourth column is optional, and can be used to indicate the color you want the stimulus to be during plotting. If nothing is entered, all stimuli will be defult to grey. If you ever have weird errors e.g. blanks values being imported copy the 4 columns and x rows into a new CSV and save it. I've had it happen once or twice that there must have been some extraneous blank cells included in the CSV when excel saved.

![image](https://user-images.githubusercontent.com/109237711/191102579-89f5260f-a990-45d3-bac9-836168db52ed.png)

Inside the Threshold file you can mark which of the stimulations to include for the calculation of the Median threshold as well as mark which thresholds to set to the pharmthreshold. This will only be necessary if you are using varyingThreshold = False, i.e. if you want to specify which thresholds to include make sure the CSV exists.

![image](https://github.com/AbbyCui/CalciumImagingAnalysis/assets/81972652/42b90823-8c9b-448f-89fc-47684dcd9d19)


Valid colors are listed here for reference:
https://matplotlib.org/stable/gallery/color/named_colors.html

![image](https://user-images.githubusercontent.com/81972652/193975593-45dabde4-c088-4e3e-8855-711fdf6d69c0.png)

![image](https://user-images.githubusercontent.com/81972652/193975635-80655606-2f26-4955-bbfb-c3f84e9053fc.png)


## Establish Environment
Please make sure python is installed in computer and the IDE you're using, and install all packages in Requirement.txt by pasting the file in terminal. 

E.g. download Visual Studio Code and make sure python is installed and then do File>open folder and find your exp# folder to load in the scripts.

Open constants.py, and read through the document and modify as desired for each experiment. The first 8 variables are the most important to change for different experiments/needs. These variabels will be used for all scripts.
The following are the most important things to adjust
Parent folder variable needs to be changed to whatever you named it earlier, e.g. #462

![image](https://user-images.githubusercontent.com/81972652/193972821-cced4f47-93ea-4f2b-8e4b-2951b8ccc33d.png)

Sampling rate 
e.g. if your sampling rate is 8.46hz, then set the FPS to 8.46 and value of T should be: T = 1.0 / 8.46

![image](https://user-images.githubusercontent.com/81972652/193972751-314c8871-defc-4387-86ee-5be8a991a92d.png)

This is the time window for rolling normalizatoin. If you have very large and long lasting responses I recommend a longer window like 800 seconds, but that will permit some drift on a faster time scale. 2-400 seconds is generally ok, but for things like GRP without TTX 400 is better. Basically the rule of thumb is that the window should be much larger than any event, e.g. if you have a response which lasts 30s you need at least 60 seconds of window as a bare minimum. Complex ongoing activity greatly benefits from a larger window.

![image](https://github.com/AbbyCui/CalciumImagingAnalysis/assets/81972652/0984c137-8c70-48f5-bc4b-9aa88f431b22)



**Proccess Data**
-----------------------------------------------------------------------------------
This script needs to be run before any other are ran. 
This script imports raw data, normalize, smooth, then calculate the threshold for each ROI, the actual threshold of response can vary depending on your experiment. For cutaneous stimuli an amplitude of 0.2 and baselineMean+7xSD works fairly well, but then for pharmacologic stimuli a threshold o 0.3 seems to be more reasonable.

If click "run" for this script, the script will run for one data file (ie. 1 plane) designated in constants.py. Alternatively, user can input commands in terminal to specify experiment number of plane number. Because multiple lines can be input at once, inputing commands in terminal is recommended if you want to process multiple planes at once.

example for terminal input: 
```
python ProcessData.py "#5" "P0"
```

Running the script will output 3 data files in OutputData folder: 

![image](https://user-images.githubusercontent.com/109237711/191107721-b0e35ecc-655e-4ea9-ad7c-0ae2d2860685.png)

don't panic if the smoothed data seems 3 times larger in size than the original file! They have the exact same dimensions and number of cells, it's just that the numbers are stored differentl somehow, thus creating different sizes.

For thresholds, if you want each stimulus to have a distinct threshold, you're finished. But I prefer to have them the same for all stimuli so I go through the CSV and take the median value of the thresholds and copy them to all stimuli.

Once your variables are changed in the constant.py file, save it and open the Unit Test.txt doc in VScode (or whatever). Open a new terminal and CD to  E:\#462\PythonScripts>  (or however you've named it) and then run either one or all of the planes as described. 
python ProcessData.py "#462" "P0"

## Plot.py
plots smoothed data for ROI in user-defined window of time. All stimuli will be plotted as shades of different colors on top of the graph, and a threshold (red line) will be present to indicate threshold calculating based on the first 2000 (or user defined number of frames) frames.
Similar to ProcessData.py, user can just click "run" and the script will plot all (or user-defined ROIs) in a given plane that is defined in constants.py. Alternatively, user can input commands in terminal to specity plane number, and the start and end of the plot (in frames). The experiment number will still be given in constants.py. Input 1 as the start and "all" as the example for terminal input:

CAW additions will need to be better annotated, but essentially all I've done is just add labels for the stims, more tick marks, and the ability to make the .PNGs it saves a constant ratio of seconds of recording/inch of graph so that the length of the graph for longer or shorter recordings are dynamically adjusted rather than stretched or squeezed as extremely short graphs are hard to read.

The key variable here is:

SecondsPerInch=400

You can go as high as 800 for a compact graph but it'll be hard to read. ~400 the minimum for 15s VF spacing, but its still somewhat hard to read. If you're specifically examining peaks and durations 200 seconds/inch would be better.

I also set the yaxismax=3 to a static number so that might need to be changed if you prefer something else.

Tick spacing is also now static as the default ticks were way too sparse. tickspacing=500 (this is in seconds) and the default minor ticks are 1/10 of the major ticks.

For my reference, 400 seconds per inch with a 1 point weight lines is the minimum resolution which is well resolved for VF counting. 0.5 to 0.75 weight was better (along with 200s/i) , but the non-zoomed imaged for quickly flipping through didn't render well in Adobe Bridge due to the aliasing of the massive resolution from 20000 pixels down to 1920. So maybe run it twice passing different sub sections through if you want higher x-axis resolutino for some sections of especially long recordings, e.g. >4 hours (my test case is ~18000 seconds or 150,000 time points)
```
python Plot.py "P0" 1 "all" 800
```
After you inspect the figures, you may choose to exclude some bad/dead/unhappy cells for future analysis. In that case, create a BadROIs.csv (named as something like #468_BadROIs.csv) in Data folder. This csv file should include any ROIs that you do not want to include for responder analysis. The first row should be the plane number, and following rows should be ROIs to exclude for each plane. The order of plane or ROIs does not matter, and for planes where no ROI need to be excluded, you don't need to create a column for that plane. 

![image](https://user-images.githubusercontent.com/109237711/196474386-454b9175-ed75-44d6-81a0-9896ef8a519f.png)

If you choose to do that, the Data folder will now look like 

![image](https://user-images.githubusercontent.com/109237711/196476310-63edfbbb-bca1-4104-9bfa-dcfe894223f0.png)

For visualization purposes, you can also only choose to plot selected ROI. This will require that you input a file named #expNumber_ROIsToInclude.csv (e.g. #40_ROIsToInclude.csv, in Data folder), which follows the same format as ROIsToRemove.csv. This file allows you to pull only the desired cells from each plane
![image](https://github.com/user-attachments/assets/cf1f7021-7704-4123-9710-09ef196cbf22)



*Max Response**
-----------------------------------------------------------------------------------
Summarizes the max amplitude of each cell's response to each stimuli. If the cell doesn't reach threshold for the entire duration of the stimulus, amplitude will be 0.
Also will summarize which cell is a responder to each stimuli where 1 indicate responder, and 0 indicate non-responder (never reached threshold in this stimulus window).

MaxResponse can take BadROIs.csv as and optional input. MaxResponse.py will automatically try to retrieve BadRoIs file regardless of input, and failure to find this file will not affect the rest of the program.

You can run this script from termina by inputting:
```
python MaxResponse.py "P0"
```
 
The first half of the output csv file will be like this, where each cell indicates the max amplitude for responders, and is 0 for non-responders

![image](https://user-images.githubusercontent.com/109237711/196473537-904b7e97-6420-48a4-9404-bf4f7b5d1328.png)

The second half of the output will be like this, where each cell is 1 or 0 to indicate responder vs non-responder
![image](https://user-images.githubusercontent.com/109237711/196473883-5bb39907-19ef-4007-aecb-aeb3a0786451.png)

## StitchFiles.py
This script simply combines the same type of output data (e.g. maxResponse) for different planes into one single file. This script will arrange all files in the OutputData folder that ends with e.g. "MaxResponse", order them by their names (i.e. P0, P1, P2...), and combine the second file to the right side of the first file, then add the third file to the right side of the merged file etc. The first column (often header for stimuli name) will only appear once, and the first row containing ROI number will be changed so that each ROI will be associated with their individual planes (e.g. P0_Mean129,P1_Mean1).

You should only run this from the terminal with the following command

```
python StitchFiles.py "#462" "MaxResponse"
```

## Rename20xAvg.py and TemplateMatching.py
Rename20xAvg.py performs 20x average (or whatever averaging you'd like) on input csv and rename the ROI names from 'Mean34' to 'exp465_P0_034'. This script produces one output csv file for each plane.

By default the script will grab the relevant information from the constant file as it will assume you're operating within the folder where it resides so input the number of planes and amount of averaging into the constant file.
![image](https://github.com/AbbyCui/CalciumImagingAnalysis/assets/81972652/8d4b41f5-5e4c-416b-a90d-f0714c409a63)


TemplateMatching.py takes in a csv file with only the header (first row containing ROI names for the desired ROIs) as template. This file can contain ROIs from different planes.

![image](https://github.com/AbbyCui/CalciumImagingAnalysis/assets/109237711/192f6641-776d-45bf-965c-396d9dba1ef5)

this script also takes in the smoothed (or 20x averaged smoothed).csv for all of the planes that contain the desired ROIs

![image](https://github.com/AbbyCui/CalciumImagingAnalysis/assets/109237711/797e6cc2-6501-47a6-bcd9-697f451f3c1c)

then will output a csv containing the smoothed/20x smoothed data points for each selected ROIs. This will output one csv file for each template file.

![image](https://github.com/AbbyCui/CalciumImagingAnalysis/assets/109237711/edccc02f-044d-44fd-b42a-764337e679cf)

By default it will assume the location of the template that it uses for matching (i.e. the cells you want to pull out) is within the Data folder. It will then (by default) save those traces back to the output folder.
![image](https://github.com/AbbyCui/CalciumImagingAnalysis/assets/81972652/7d88f2eb-2fe9-47d1-b5ac-5f63e41bf9e8)

You will need to specify the name of the file and it will name the output file the same name.
![image](https://github.com/AbbyCui/CalciumImagingAnalysis/assets/81972652/9a1e027c-1ca7-44b5-b47f-3b04118e6a1a)

## Peri-Stimulus.py
On a plane-by-plane basis: This script extract ROIs of interest at the time window of interest, extracts the data within the peri-stimulus window (output one file ending with "Peri-stim"), and calculate mean, median, 95% range for each frame (output another file ending with "avg Peri-stim"), 
Then, the script stitches the "avg Peri-stim.cvs" from all planes together, and calculate mean, median, 95% range for cells from all planes.

**Input files** : 
1. Smoothed.csv (in OutputData folder)
2. Stimulus.csv (in Data folder)
3. #expNumber_ROIsToInclude.csv (e.g. #40_ROIsToInclude.csv, in Data folder), which follows the same format as ROIsToRemove.csv. This file allows you to pull only the desired cells from each plane
![image](https://github.com/user-attachments/assets/cf1f7021-7704-4123-9710-09ef196cbf22)

**Input info**

Terminal Input: Enter the experiment Number (e.g. #40) in constant.py, and in terminal, the only required input is the number of total planes you have (P0-P4 = 5 planes in total). This will pull data from P0-P4.
(e.g. python Peri-Stimulus.py 5)

stim_index = [46] #index 1 means the 2nd stimulus (yes we love python); input list to merge multiple stim (e.g. [1,2,3])

interval = 20*fps #20*fps would mean 20sec pre and post the start of the stim

grace = 1.5*fps #exclude some time before and after stim start/end (this is useful when you're not so cofident about start/stop time stamps)

postfix = "test" #something meaningful to include in file names

**Output**
For each plane, the script will output 2 files
1. full Peri-stim *postfix of your choosing* (e.g.#40_P0_full Peri-stim test)

   this file simply crops out the time window before and after stimulus
   ![image](https://github.com/user-attachments/assets/e82e04de-2925-4348-bc80-7dc29b0d090d)

3. avg Peri-stim *postfix of your choosing* (e.g.#40_P0_avg Peri-stim test)

   this file calculates the mean, median, upper and lower limit of the 95% range of each frame within the timewindow.
![image](https://github.com/user-attachments/assets/c1bda973-f880-4c93-96bd-f3915c09aa7c)

For all planes combined, the script will output 2 files
1. stitching "full Peri-stim" file from all planes together -> e.g #40_full Peri-stim test_Stitched
2. allPlanes_avg Peri-stim (e.g. #40_allPlanes_avg Peri-stim test)

   This file computes mean, median, upper and lower limit of the 95% range of each frame within the timewindow for all selected cells from all planes.


**Improvements**
-----------------------------------------------------------------------------------
instead of running each script serially in the terminal you can run the 05 line of scripts which just runs each one in parallel. These assume 5 planes, but just add or remove tuples as necessary. This imroves the speed of processing by ~5x

![image](https://github.com/user-attachments/assets/a1781faa-00c1-4cb8-a452-ec54eeafefe1)

The 05Plot.py has the relevant variables for specifying the range and SPI at the top of the file. 

It should be possible to stack these to run the whole pipeline at once, e.g. pasting this into the terminal
Python 05ProcessData.py
Python 05Plot.py
Python 05MaxResponse.py
