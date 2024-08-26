Data Processing
====================
DFF normalization, smoothing, event detection, and amplitude extraction

Proccess Data
-----------------------------------------------------------------------------------
This script needs to be run before any other are ran. 
This script imports raw data, normalize, smooth, then calculate the threshold for each ROI, the actual threshold of response can vary depending on your experiment. For cutaneous stimuli an amplitude of 0.2 and baselineMean+7xSD works fairly well, but then for pharmacologic stimuli a threshold o 0.3 seems to be more reasonable.

If click "run" for this script, the script will run for one data file (ie. 1 plane) designated in constants.py. Alternatively, user can input commands in terminal to specify experiment number of plane number. Because multiple lines can be input at once, inputing commands in terminal is recommended if you want to process multiple planes at once.

example for terminal input: 

``python ProcessData.py "#5" "P0"``

Running the script will output 3 data files in OutputData folder: 

.. image:: https://user-images.githubusercontent.com/109237711/191107721-b0e35ecc-655e-4ea9-ad7c-0ae2d2860685.png


Max Response
-----------------------------------------------------------------------------------
Summarizes the max amplitude of each cell's response to each stimuli. If the cell doesn't reach threshold for the entire duration of the stimulus, amplitude will be 0.
Also will summarize which cell is a responder to each stimuli where 1 indicate responder, and 0 indicate non-responder (never reached threshold in this stimulus window).

MaxResponse can take BadROIs.csv as and optional input. MaxResponse.py will automatically try to retrieve BadRoIs file regardless of input, and failure to find this file will not affect the rest of the program.

You can run this script from termina by inputting:

``python MaxResponse.py "P0"``
 
The first half of the output csv file will be like this, where each cell indicates the max amplitude for responders, and is 0 for non-responders

.. image:: https://user-images.githubusercontent.com/109237711/196473537-904b7e97-6420-48a4-9404-bf4f7b5d1328.png

The second half of the output will be like this, where each cell is 1 or 0 to indicate responder vs non-responder

.. image:: https://user-images.githubusercontent.com/109237711/196473883-5bb39907-19ef-4007-aecb-aeb3a0786451.png

## StitchFiles.py
This script simply combines the same type of output data (e.g. maxResponse) for different planes into one single file. This script will arrange all files in the OutputData folder that ends with e.g. "MaxResponse", order them by their names (i.e. P0, P1, P2...), and combine the second file to the right side of the first file, then add the third file to the right side of the merged file etc. The first column (often header for stimuli name) will only appear once, and the first row containing ROI number will be changed so that each ROI will be associated with their individual planes (e.g. P0_Mean129,P1_Mean1).

You should only run this from the terminal with the following command

``python StitchFiles.py "#462" "MaxResponse"``

Optional Improvements
-----------------------------------------------------------------------------------
instead of running each script serially in the terminal you can run the 05 line of scripts which just runs each one in parallel. These assume 5 planes, but just add or remove tuples as necessary. This imroves the speed of processing by ~5x

.. image:: https://github.com/user-attachments/assets/a1781faa-00c1-4cb8-a452-ec54eeafefe1

The 05Plot.py has the relevant variables for specifying the range and SPI at the top of the file. 

It should be possible to stack these to run the whole pipeline at once, e.g. pasting this into the terminal
Python 05ProcessData.py
Python 05Plot.py
Python 05MaxResponse.py
