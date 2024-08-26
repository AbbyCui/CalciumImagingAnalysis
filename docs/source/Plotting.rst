Plotting
====================

Plot.py plots smoothed data for ROI in user-defined window of time. All stimuli will be plotted as shades of different colors on top of the graph, and a threshold (red line) will be present to indicate the calculated threshold. Similar to ProcessData.py, user can run the script from the terminal and it will plot all ROIs in the plane specified in the constant file. Alternatively, user can specify/pass commands in terminal to specity plane number, and the start and end of the plot (in frames), and the X-axis scale. The experiment number will still be given in constants.py. Input 1 as the start and "all" as the example for terminal input.

You can speed up the plotting by running 05Plot.py which just runs 5 planes in parallel. Make sure you specify the start stop and pixels per inch in the 05Plot.py file itself. If you do not have 5 planes you will need to adjust this script (('Plot.py', ['P0'],[start],[stop],[SecondsPerInch]), just increase or decrease the number of scripts_with_args.

A key variable to play with for different plots is:

SecondsPerInch=400

You can go as high as 800 for a compact graph but it'll be hard to read. ~300 the minimum for 15s VF spacing, but its still somewhat hard to read. For 10s spaced stimuli I would recommend less than 100, but you cannot plot the entire recording as the files will be too large. If you can error, that is why. Plot a subsection instead.

The y-axis is a static value (yaxismax=3) in order to keep each ROI in the same range when browsing traces.

For reference, 400 seconds per inch with a 1 point weight lines is the minimum resolution which is well resolved for VF counting. 0.5 to 0.75 weight was better (along with 200s/i) , but the non-zoomed imaged for quickly flipping through didn't render well in Adobe Bridge due to the aliasing of the massive resolution from 20000 pixels down to 1920. So maybe run it twice passing different sub sections through if you want higher x-axis resolution for some sections of especially long recordings, e.g. >4 hours (my test case is ~18000 seconds or 150,000 time points) `
python Plot.py "P0" 1 "all" 800

Sub population plotting
------------------
For visualization purposes, you can also only choose to plot selected ROI. This will require that you input a file named #expNumber_ROIsToInclude.csv (e.g. #40_ROIsToInclude.csv, in Data folder), which follows the same format as ROIsToRemove.csv. This file allows you to pull only the desired cells from each plane

.. image:: https://github.com/user-attachments/assets/cf1f7021-7704-4123-9710-09ef196cbf22

Inside the stimulus file, the 4th columm is the color of each stimuli. If nothing is entered, all stimuli will be defult to grey. If you ever have weird errors e.g. blanks values being imported copy the 4 columns and x rows into a new CSV and save it. I’ve had it happen once or twice that there must have been some extraneous blank cells included in the CSV when excel saved.

Valid colors are listed here for reference: https://matplotlib.org/stable/gallery/color/named_colors.html

.. image:: https://user-images.githubusercontent.com/81972652/193975593-45dabde4-c088-4e3e-8855-711fdf6d69c0.png
.. image:: https://user-images.githubusercontent.com/81972652/193975635-80655606-2f26-4955-bbfb-c3f84e9053fc.png

There is also a function to plot where each recording starts and stops. This is indicated by adding a CSV in the Data folder called Exp#_rec_length.csv. This CSV is just a single column which has the length of each recording. The ThorStackLengthFinder provides this information or you can do it manually. If the CSV is present, it will add a red line at the transitions between each recording. If you want to turn it off, just rename the CSV to something slightly else or set Rec_Splits=0 in Plot.py
