Analysis Tools
===============
No unifying theme here other than these are common useful tools to visualize, process, or analyze calcium traces

Data Slicing and downsampling for graphing
-----------------------------------------
Rename20xAvg.py and TemplateMatching.py
Rename20xAvg.py performs 20x average (or whatever averaging you'd like) on input csv and rename the ROI names from 'Mean34' to 'exp465_P0_034'. This script produces one output csv file for each plane.

By default the script will grab the relevant information from the constant file as it will assume you're operating within the folder where it resides so input the number of planes and amount of averaging into the constant file.

  .. image:: https://github.com/AbbyCui/CalciumImagingAnalysis/assets/81972652/8d4b41f5-5e4c-416b-a90d-f0714c409a63


TemplateMatching.py takes in a csv file with only the header (first row containing ROI names for the desired ROIs) as template. This file can contain ROIs from different planes.

.. image:: https://github.com/AbbyCui/CalciumImagingAnalysis/assets/109237711/192f6641-776d-45bf-965c-396d9dba1ef5

this script also takes in the smoothed (or 20x averaged smoothed).csv for all of the planes that contain the desired ROIs

.. image:: https://github.com/AbbyCui/CalciumImagingAnalysis/assets/109237711/797e6cc2-6501-47a6-bcd9-697f451f3c1c

then will output a csv containing the smoothed/20x smoothed data points for each selected ROIs. This will output one csv file for each template file.

.. image:: https://github.com/AbbyCui/CalciumImagingAnalysis/assets/109237711/edccc02f-044d-44fd-b42a-764337e679cf

By default it will assume the location of the template that it uses for matching (i.e. the cells you want to pull out) is within the Data folder. It will then (by default) save those traces back to the output folder.

  .. image:: https://github.com/AbbyCui/CalciumImagingAnalysis/assets/81972652/7d88f2eb-2fe9-47d1-b5ac-5f63e41bf9e8

You will need to specify the name of the file and it will name the output file the same name.

  .. image:: https://github.com/AbbyCui/CalciumImagingAnalysis/assets/81972652/9a1e027c-1ca7-44b5-b47f-3b04118e6a1a

Peristimulus time histogram
--------------------------------------------------------------
On a plane-by-plane basis: This script extract ROIs of interest at the time window of interest, extracts the data within the peri-stimulus window (output one file ending with "Peri-stim"), and calculate mean, median, 95% range for each frame (output another file ending with "avg Peri-stim"), 
Then, the script stitches the "avg Peri-stim.cvs" from all planes together, and calculate mean, median, 95% range for cells from all planes.

**Input files** : 
1. Smoothed.csv (in OutputData folder)
2. Stimulus.csv (in Data folder)
3. #expNumber_ROIsToInclude.csv (e.g. #40_ROIsToInclude.csv, in Data folder), which follows the same format as ROIsToRemove.csv. This file allows you to pull only the desired cells from each plane

  .. image:: https://github.com/user-attachments/assets/cf1f7021-7704-4123-9710-09ef196cbf22

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
  
.. image:: https://github.com/user-attachments/assets/e82e04de-2925-4348-bc80-7dc29b0d090d

3. avg Peri-stim *postfix of your choosing* (e.g.#40_P0_avg Peri-stim test)

   this file calculates the mean, median, upper and lower limit of the 95% range of each frame within the timewindow.

.. image:: https://github.com/user-attachments/assets/c1bda973-f880-4c93-96bd-f3915c09aa7c

For all planes combined, the script will output 2 files
1. stitching "full Peri-stim" file from all planes together -> e.g #40_full Peri-stim test_Stitched
2. allPlanes_avg Peri-stim (e.g. #40_allPlanes_avg Peri-stim test)

   This file computes mean, median, upper and lower limit of the 95% range of each frame within the timewindow for all selected cells from all planes.
