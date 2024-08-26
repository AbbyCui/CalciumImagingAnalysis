Plotting
====================

Plot.py plots smoothed data for ROI in user-defined window of time. All stimuli will be plotted as shades of different colors on top of the graph, and a threshold (red line) will be present to indicate threshold calculating based on the first 2000 (or user defined number of frames) frames. Similar to ProcessData.py, user can just click "run" and the script will plot all (or user-defined ROIs) in a given plane that is defined in constants.py. Alternatively, user can input commands in terminal to specity plane number, and the start and end of the plot (in frames). The experiment number will still be given in constants.py. Input 1 as the start and "all" as the example for terminal input:

CAW additions will need to be better annotated, but essentially all I've done is just add labels for the stims, more tick marks, and the ability to make the .PNGs it saves a constant ratio of seconds of recording/inch of graph so that the length of the graph for longer or shorter recordings are dynamically adjusted rather than stretched or squeezed as extremely short graphs are hard to read.

The key variable here is:

SecondsPerInch=400

You can go as high as 800 for a compact graph but it'll be hard to read. ~400 the minimum for 15s VF spacing, but its still somewhat hard to read. If you're specifically examining peaks and durations 200 seconds/inch would be better.

I also set the yaxismax=3 to a static number so that might need to be changed if you prefer something else.

Tick spacing is also now static as the default ticks were way too sparse. tickspacing=500 (this is in seconds) and the default minor ticks are 1/10 of the major ticks.

For my reference, 400 seconds per inch with a 1 point weight lines is the minimum resolution which is well resolved for VF counting. 0.5 to 0.75 weight was better (along with 200s/i) , but the non-zoomed imaged for quickly flipping through didn't render well in Adobe Bridge due to the aliasing of the massive resolution from 20000 pixels down to 1920. So maybe run it twice passing different sub sections through if you want higher x-axis resolutino for some sections of especially long recordings, e.g. >4 hours (my test case is ~18000 seconds or 150,000 time points) `
python Plot.py "P0" 1 "all" 800
` After you inspect the figures, you may choose to exclude some bad/dead/unhappy cells for future analysis. In that case, create a BadROIs.csv (named as something like #468_BadROIs.csv) in Data folder. This csv file should include any ROIs that you do not want to include for responder analysis. The first row should be the plane number, and following rows should be ROIs to exclude for each plane. The order of plane or ROIs does not matter, and for planes where no ROI need to be excluded, you don't need to create a column for that plane.

![image](https://user-images.githubusercontent.com/109237711/196474386-454b9175-ed75-44d6-81a0-9896ef8a519f.png)

If you choose to do that, the Data folder will now look like

![image](https://user-images.githubusercontent.com/109237711/196476310-63edfbbb-bca1-4104-9bfa-dcfe894223f0.png)

For visualization purposes, you can also only choose to plot selected ROI. This will require that you input a file named #expNumber_ROIsToInclude.csv (e.g. #40_ROIsToInclude.csv, in Data folder), which follows the same format as ROIsToRemove.csv. This file allows you to pull only the desired cells from each plane ![image](https://github.com/user-attachments/assets/cf1f7021-7704-4123-9710-09ef196cbf22)

Inside the stimulus file, the 4th columm is the color of each stimuli. If nothing is entered, all stimuli will be defult to grey. If you ever have weird errors e.g. blanks values being imported copy the 4 columns and x rows into a new CSV and save it. I’ve had it happen once or twice that there must have been some extraneous blank cells included in the CSV when excel saved.

Valid colors are listed here for reference: https://matplotlib.org/stable/gallery/color/named_colors.html

.. image:: https://user-images.githubusercontent.com/81972652/193975593-45dabde4-c088-4e3e-8855-711fdf6d69c0.png

![image](https://user-images.githubusercontent.com/81972652/193975635-80655606-2f26-4955-bbfb-c3f84e9053fc.png)
