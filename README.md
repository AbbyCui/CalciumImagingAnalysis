# Calcium Imaging Analysis
These series of scripts takes raw data resulted from FIJI-multi-measure to basic figures, analysis of ISI, max response during each stimuli and responders to each stimuli

## Input data and Folder Structure
Put all scripts in the same folder named whatever you like, e.g. "PythonScripts"

![image](https://user-images.githubusercontent.com/81972652/193971557-d39188fd-2f6d-4e63-a4ad-920e689eeda2.png)

For EACH experiment, make a copy of the folder PythonScripts and place it within a folder (e.g. exp#462). 

![image](https://user-images.githubusercontent.com/81972652/193971950-23060e2c-ea8c-49cc-b026-a2eef60a6295.png)

Then create a folder called the same thing (Exp#462) and within it create a folder called "Data" that contains all results from multi-measure and a .csv file containing the timestamp of each stimuli. Results should be in csv format, and names as **"experiemntNumber_PlaneNumber_Results.csv"**, and stimulus file should be named **"ExperimentNumber_Stimulus.csv"**, as shown below. The names of the ROIs (i.e. the first row) cannot have # in it, e.g. Exp#455_P2_001 and should be left as Mean1, Mean2, etc as the outputs will be renamed later.

![image](https://user-images.githubusercontent.com/81972652/193972095-c63ea7de-ea6e-4dda-ae69-8981fde2ee41.png)

Inside the stimulus file, columm 1 is the name of each stimuli. **Do no include commas or #!** comma in csv files indicate "next cell" and will not be interpreted as a part of the text. The second and the third columns are the start and end of each stimulus (in frames). Fourth column is optional, and can be used to indicate the color you want the stimulus to be during plotting. If nothing is entered, all stimuli will be defult to grey.

![image](https://user-images.githubusercontent.com/109237711/191102579-89f5260f-a990-45d3-bac9-836168db52ed.png)

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


Normalization windows are dependent on sampling rate, but for 6-8hz these are a good starting point
![image](https://user-images.githubusercontent.com/81972652/193972855-70325468-0fe8-415e-bf33-fcb836f21cb8.png)

Baseline calcs will be changed later so retaining the first 2000 frames is good enough for now.

## ProcessData.py
This script needs to be run before any other are ran. 
This script imports raw data, normalize, smooth, then calculate the threshold for each ROI (0.5 or baselineMean+4*SD, whichever is bigger)

If click "run" for this script, the script will run for one data file (ie. 1 plane) designated in constants.py. Alternatively, user can input commands in terminal to specify experiment number of plane number. Because multiple lines can be input at once, inputing commands in terminal is recommended if you want to process multiple planes at once.

example for terminal input: 
```
python ProcessData.py "#5" "P0"
```

Running the script will output 3 data files in OutputData folder: 

![image](https://user-images.githubusercontent.com/109237711/191107721-b0e35ecc-655e-4ea9-ad7c-0ae2d2860685.png)

don't panic if the smoothed data seems 3 times larger in size than the original file! They have the exact same dimensions and number of cells, it's just that the numbers are stored differentl somehow, thus creating different sizes.

Currently, don't trust AllThresholds too much because it establishes threshold for the entire recording based on the first 2000 frames (or however huch you input in constants.py), which does not account for slow drifts during the experiments.

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
python Plot.py "P0" 1 "all"
```
