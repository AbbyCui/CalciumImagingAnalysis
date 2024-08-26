Setup
================================
# Calcium Imaging Analysis
These series of scripts takes raw data resulted from FIJI-multi-measure to basic figures, analysis of ISI, max response during each stimuli and responders to each stimuli

Input data and Folder Structure
------------------------------------
Put all scripts in the same folder named whatever you like, e.g. "PythonScripts"

.. image:: https://user-images.githubusercontent.com/81972652/193971557-d39188fd-2f6d-4e63-a4ad-920e689eeda2.png

For EACH experiment, make a copy of the folder PythonScripts and place it within a folder (e.g. exp#462). 

.. image:: https://user-images.githubusercontent.com/81972652/193971950-23060e2c-ea8c-49cc-b026-a2eef60a6295.png

Then create a folder called the same thing (Exp#462) and within it create a folder called "Data" that contains all the raw inputs and metadata. 

We will go over more about inputs after setting up python.

Establish Environment
-----------------------------------------------
Please make sure python is installed in computer and the IDE you're using, and install all packages in Requirement.txt by pasting the file in terminal. 

E.g. download Visual Studio Code and make sure python is installed and then do File>open folder and find your exp# folder to load in the scripts.

Open constants.py, and read through the document and modify as desired for each experiment. The first 8 variables are the most important to change for different experiments/needs. These variabels will be used for all scripts.
The following are the most important things to adjust
Parent folder variable needs to be changed to whatever you named it earlier, e.g. #462

.. image:: https://user-images.githubusercontent.com/81972652/193972821-cced4f47-93ea-4f2b-8e4b-2951b8ccc33d.png

Sampling rate 
e.g. if your sampling rate is 8.46hz, then set the FPS to 8.46 and value of T should be: T = 1.0 / 8.46

.. image:: https://user-images.githubusercontent.com/81972652/193972751-314c8871-defc-4387-86ee-5be8a991a92d.png

This is the time window for rolling normalizatoin. If you have very large and long lasting responses I recommend a longer window like 800 seconds, but that will permit some drift on a faster time scale. 2-400 seconds is generally ok, but for things like GRP without TTX 400 is better. Basically the rule of thumb is that the window should be much larger than any event, e.g. if you have a response which lasts 30s you need at least 60 seconds of window as a bare minimum. Complex ongoing activity greatly benefits from a larger window.

.. image:: https://github.com/AbbyCui/CalciumImagingAnalysis/assets/81972652/0984c137-8c70-48f5-bc4b-9aa88f431b22
