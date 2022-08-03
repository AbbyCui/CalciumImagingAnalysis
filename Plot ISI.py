import matplotlib.pyplot as plt
import numpy as np

directory = "../#1_Output/EventNumber.csv"

eventNumber = np.loadtxt(directory,delimiter=',',dtype=str)  ##import the csv to a str using loadtxt