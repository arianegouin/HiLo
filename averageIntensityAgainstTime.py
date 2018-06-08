import csv
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os
import numpy


class Folder:

    def __init__(self):
        root = tk.Tk()
        root.withdraw()
        root.directory = filedialog.askdirectory(initialdir=os.getcwd(), title="Select folder with CSV files")
        self.directory = root.directory

    def iterateCSVThroughFolder(self):
        for file in os.listdir(self.directory):
            filestring = os.fsdecode(file)
            if filestring.endswith(".csv"):
                # yield os.path.join(self.directory, filestring)
                yield self.directory, filestring
            else:
                continue


class CSVFile:

    def __init__(self, directory, name):
        self.directory = directory
        self.name = name

    def read(self):
        with open(os.path.join(self.directory, self.name)) as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                yield row

    def getLabParams(self):
        name = self.name.split('.')[0]
        exposure, during, acquisition, what = name.split('-')[0].split(' ')
        exposure = float(exposure.replace('s', ''))
        return name, exposure

    def getData(self):
        number = []
        mean = []
        deviation = []
        for row in self.read():
            try:
                float(row[0])
            except ValueError:
                continue
            else:
                number.append(float(row[0]))
                mean.append(float(row[1]))
                deviation.append(float(row[2]))
        return number, mean, deviation


if __name__ == '__main__':
    for file in Folder().iterateCSVThroughFolder():
        CSV = CSVFile(file[0], file[1])
        noExtension, theExposure = CSV.getLabParams()
        xdata, ydata, deviationdata = CSV.getData()

        x = [i * theExposure for i in xdata]
        y = [i/max(ydata) for i in ydata]
        dev = round(numpy.mean([i/max(ydata) for i in deviationdata]), 2)

        plt.plot(x, y, label='%s (std dev = %s)' % (noExtension, dev))

    plt.xlabel('Time [s]')
    plt.ylabel('Intensity (normalised)')
    plt.legend()
    plt.show()
