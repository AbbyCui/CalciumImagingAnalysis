Inputs
=======================
This page documents the inputs in the Data Folder. 

Fluorescence Traces
-----------------------------------------------------------------------------------
The raw data is expected as a CSV and to work well should be named as: **"experimentNumber_PlaneNumber_Results.csv"**, as shown below. The names of the ROIs (i.e. the first row) cannot have # in it, e.g. Exp#455_P2_001 and should be left as Mean1, Mean2, etc as the outputs will be renamed later.

.. image:: https://github.com/AbbyCui/CalciumImagingAnalysis/assets/81972652/3bd42cb4-339e-49d4-8b92-307d17e40546

Stimulus File
-----------------------------------------------------------------------------------
The file which contains the timing of events/stimuli should be named similarly to the raw data, e.g. **"ExperimentNumber_Stimulus.csv"**,
Inside the stimulus file, columm 1 is the name of each stimuli. **Do no include commas or #!** comma in csv files indicate "next cell" and will not be interpreted as a part of the text. The second and the third columns are the start and end of each stimulus (in frames). Fourth column is optional, and can be used to indicate the color you want the stimulus to be during plotting. If nothing is entered, all stimuli will be defult to grey. If you ever have weird errors make sure your CSVs are correctly formatting by openeing them in a text editor like wordpad. This can be fixed by pasting just the 4 columns and x rows into a new CSV and save it. I've had it happen once or twice that there must have been some extraneous blank cells included in the CSV when excel saved.

.. image:: https://user-images.githubusercontent.com/109237711/191102579-89f5260f-a990-45d3-bac9-836168db52ed.png

Valid colors are listed here for reference:
https://matplotlib.org/stable/gallery/color/named_colors.html

.. image:: https://user-images.githubusercontent.com/81972652/193975593-45dabde4-c088-4e3e-8855-711fdf6d69c0.png

.. image:: https://user-images.githubusercontent.com/81972652/193975635-80655606-2f26-4955-bbfb-c3f84e9053fc.png

Threshold file
-----------------------------------------------------------------------------------
Finding the threshold of a given cell is done by examining the 30seconds prior to each stimulus and then taking the median value of all those stimuli. Because some stimuli may occur in the 30s prior you can mark which of the stimulations to include for the calculation of the Median threshold. This will only be necessary if you are using varyingThreshold = False, but I prefer a static threshold. 

You canm also mark any stimuli that require a higher threshold due to larger signals such as pharmacological stimuli (pharmthreshold). 

.. image:: https://github.com/AbbyCui/CalciumImagingAnalysis/assets/81972652/42b90823-8c9b-448f-89fc-47684dcd9d19

Split normalization
-------------------------------------
If you have artifacts that require a reset of the rolling ball normalization you will need to pass a CSV with the splits at which to reset the rolling ball normalization called **"ExperimentNumber_Stimulus.csv"**. This file should contain at minimum the 1st and last frame of the recording.

.. image:: https://github.com/user-attachments/assets/32614b02-f704-4443-80ba-4ba3a5aee915

BadROIs
--------------------------------------
After you inspect the figures, you may choose to exclude some bad/dead/unhappy cells for future analysis. In that case, create a BadROIs.csv (named as something like #468_BadROIs.csv) in Data folder. This csv file should include any ROIs that you do not want to include for responder analysis. The first row should be the plane number, and following rows should be ROIs to exclude for each plane. The order of plane or ROIs does not matter, and for planes where no ROI need to be excluded, you don't need to create a column for that plane.

.. image:: https://user-images.githubusercontent.com/109237711/196474386-454b9175-ed75-44d6-81a0-9896ef8a519f.png

Recording Length
--------------------------------------
There is also a function to plot where each recording starts and stops. This is indicated by adding a CSV in the Data folder called Exp#_rec_length.csv. This CSV is just a single column which has the length of each recording. The ThorStackLengthFinder provides this information or you can do it manually. If the CSV is present, it will add a red line at the transitions between each recording. If you want to turn it off, just rename the CSV to something slightly else or set Rec_Splits=0 in Plot.py

