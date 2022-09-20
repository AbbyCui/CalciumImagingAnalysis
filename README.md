# Calcium Imaging Analysis
These series of scripts takes raw data resulted from FIJI-multi-measure to basic figures, analysis of ISI, max response during each stimuli and responders to each stimuli

## Input data and Folder Structure
Please put all scripts in the same folder names "Analysis", and each experiment in their own folders, parallel to the "Analysis" folder.
![image](https://user-images.githubusercontent.com/109237711/191100514-77b4b353-91d8-4eec-b2c9-c74e510975e7.png)

Inside of each experiment folder, please have a folder called "Data" that contains all results from multi-measure and a .csv file containing the timestamp of each stimuli. Results should be in csv format, and names as **"experiemntNumber_PlaneNumber_Results.csv"**, and stimulus file should be named **"ExperimentNumber_Stimulus.csv"**, as shown below.
![image](https://user-images.githubusercontent.com/109237711/191100928-de310668-79e1-4a7d-89ab-f37a494d15c7.png)

Inside the stimulus file, columm 1 is the name of each stimuli. **Do no include comma!** comma in csv files indicate "next cell" and will not be interpreted as a part of the text. The second and the third columns are the start and end of each stimulus (in frames). Fourth column is optional, and can be used to indicate the color you want the stimulus to be during plotting. If nothing is entered, all stimuli will be defult to grey.
![image](https://user-images.githubusercontent.com/109237711/191102579-89f5260f-a990-45d3-bac9-836168db52ed.png)

## Establish Environment
Please make sure python is installed in computer and the IDE you're using, and install all packages in Requirement.txt by pasting the file in terminal. 

Open constants.py, and read through the document and modify as desired for each experiment. The first 8 variables are the most important to change for different experiments/needs. These variabels will be used for all scripts.

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

## Plot.py
plots smoothed data for ROI in user-defined window of time. All stimuli will be plotted as shades of different colors on top of the graph, and a threshold (red line) will be present to indicate threshold calculating based on the first 2000 (or user defined number of frames) frames.
Similar to ProcessData.py, user can just click "run" and the script will plot all (or user-defined ROIs) in a given plane that is defined in constants.py. Alternatively, user can input commands in terminal to specity plane number, and the start and end of the plot (in frames). The experiment number will still be given in constants.py. Input 1 as the start and "all" as the 

example for terminal input:
```
python Plot.py "P0" 1 "all"
```

## don't use the other scripts until my calculation for threshold is updated to be specific to each stimuli!  
