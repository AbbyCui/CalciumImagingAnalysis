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

GreedyEvent Detection
----------------------------------------------------------------------
``GreedyEventDetection``

Here we will go through the broad strokes of how GreedyEventDetection works. I will reference the code sparsley, but this is mostly to explain the logic behind the code rather than the code's workings.

Our example cell with the DFF and stims/thresholds indicated

.. image:: https://github.com/user-attachments/assets/02ba816e-7d6d-4244-b09d-db7b60b65bd8


As explained above, our thresholds are set as a function of trace noise (SD) so here is when the first frame above threshold (i.e. trace noise) is detected:

.. image::  https://github.com/user-attachments/assets/0dad6d62-d500-449d-9ef9-1ce14827f6cc


Once it reaches the spike duration (i.e. a certain number of frames/seconds above threshold) we decide it's a real event and not noise

``if EventDuration > constant.spikeduration:``

.. image::  https://github.com/user-attachments/assets/4a64c712-0939-4988-b7b5-412f3f9ea33d

So, it assigns the 1st frame above threshold as the start time of the event. 

It is worth nothing that because the start time of the event is when it is above threshold there is some error in the timing of the events.
e.g. if the threshold is 20% DFF but the event is slow to rise you may have a few frames of lag relative to the actual start of electrical activity. 
This is especially true with Gcamp6s as it has a very slow rise time relative to Gcamp8.

Now we also start checking for whether the supra threshold DFF is also increasing which is a sign of a discrete event rather than a random drunkard's walk towards a positive that may be more likely z-drift, noise, or background. This requirement is that of the past 4 frames of suprathreshold frames they all need to have a positive derivative. This could be dropped to 3/4 frames (maybe for Gcamp8) but the derivative is additionally smoothed in order to track the general upward trend rather than an absolute t2-t1 type of requirement.
If you need to change the smoothing it is located here. These values still preserve most of the temporal kinetics. This is smoothing the already once smoothed data (i.e. it take the smoothed input and smoothes it again)
``DerivativeInput[1:,i] = signal.savgol_filter(data[1:,i],13, 2)`` 

If the smoothing in the derivative still shows a negative trend, in 1 of the 4 frames, it would shift the window forward by 1 frame and then check the 4/4 positive again. 
``if PositiveSlope < 4: if the 4 frame are not all increasing, otherwise it's a false start.``
Once all 4 frames are positive it writes the 1st frame of the 4 values which was positive as the start.
This works fairly well because Gcamp6s is slow to rise and with 8hz sampling we regularly get 6-10 frames of positively trending activity. This will need to be adjusted depending on the indicator and sensor. 

Once we have 4 frames above threshold and also 4 frames that are also positive we get our 'realstart' time.

.. image::  https://github.com/user-attachments/assets/01afd90f-9749-4052-831d-6b9877193e71

``if PositiveSlope==4: realstart=y-3``

Now that we've assigned a start, we're now looking for 3 consecutively negative frames to assign the stop of the the event. Again, this will be smeared due to the slow kinetics of Gcamp6s, but without deconvolution this is a safely conservative estimate.

``if ConsecutiveNegativeFrames > 2: end = y``


In the above example, this cell has it's end point here, where the 3rd frame is negative. This will once again be FPS dependent. These are ~8hz recordings on gcamp6s.

.. image::  https://github.com/user-attachments/assets/c9dbb22d-49f8-47c0-be70-8269a0e76d5f


This loop now resets that it's found an 'end' and we start looking for suprathreshold frames 

``Starts[event,x] = realstart
Ends[event,x] = end``

Since we immediately find 4 frames above threshold, it goes into the 'check positive slope' loop, but fails bcause the prior 4 frames are also not sloped positive.

.. image::  https://github.com/user-attachments/assets/53ff6dde-ba9d-4406-a00d-bc7ffa30baf2


We now roll our window forward 1 frame at a time checking if all frames in that window are positive until we find 4 frames that are positive, and now we have our 2nd event.

.. image::  https://github.com/user-attachments/assets/5917a5a1-ba14-437f-a302-8b66b99f56d9


Repeat for the end to find 3 negative frames

.. image::  https://github.com/user-attachments/assets/b7af3e4d-4c54-4aeb-8cab-1c063de42be1

Binary Response/Stim windows
-------------------------
To decide whether a cell responded to a particular stimuli we check the list of starts and stops that we just created.

Using our example from above we detected 2 sets of starts and stops as shown here

.. image::  https://github.com/user-attachments/assets/bed4e006-a816-4580-9442-ed151877973f

We go through our stimlist (which is a list of frame times as a start and stop, e.g. the event occured between frames 100 and 120) and find that a start was assigned during the window of Stim1 so we call it a responder, and find the peak response during the window. Similarly, we check during Stim2 for any starts and again, we find that there was a start which occured, so it's a responder. 

It's important to note that if a Start is detected before the stim window it WILL NOT consider it a responder even if the amplitude is high during the window. This is why it is very important to have your stimulation times very accurately estimated because if you're stim times are a few frames off if could miss the 'start'. You can also fudge this by just adding 2-3 frames to each side of your stim window if you don't have frame-precise timing. Of note, if you have a long stimulation (e.g. something without a discrete start and stop window that lasts for minutes) any start in the window will trigger a response. If there are multiple starts and stops, the max response will be the max of any pair of starts and stops which have their starts within the stim window.


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
