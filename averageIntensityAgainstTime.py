
import csv
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os
import statistics
import numpy

# file = CSVFile(r"C:\Users\Ariane Gouin\Documents\ULaval\2018_Ete\cervo\P3_francois\20180612\results", '200ms during 1min speckles-SPC.csv')
# file.getData()


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
            listOfRows = []
            for row in reader:
                listOfRows.append(row)
            return listOfRows

    def getLabParams(self):
        name = self.name.split('.')[0]
        exposure, during, acquisition, what = name.split('-')[0].split(' ')
        exposure = exposure.replace('s', '')
        if exposure.find('m') != -1:
            exposure = float(exposure.replace('m', '')) / 1000
        else:
            exposure = float(exposure)
        return name, exposure

    def getData(self):

        listOfRows = self.read()
        nbOfPoints = len(listOfRows[0]) - 1

        time = []
        allData = []
        for i in range(nbOfPoints):
            allData.append([])

        nbOfRow = -1
        for row in listOfRows:
            try:
                float(row[0])
            except ValueError:
                pass
            else:
                time.append(float(row[0]))

                nbOfRow += 1
                for i in range(nbOfPoints):
                    allData[i].append(float(row[i + 1]))

        return time, allData






if __name__ == '__main__':

    option = float(input('1: graph, or 2: std dev --> ').strip())

    if option == 1:
        print('ootion1')

        # shift = -1
        shift = 0

        for file in Folder().iterateCSVThroughFolder():
            print('file')
            # shift += 1

            CSV = CSVFile(file[0], file[1])
            noExtension, theExposure = CSV.getLabParams()
            xdata, data = CSV.getData()
            x = [i * theExposure for i in xdata]
            for ydata in data:
                stddev = round(statistics.stdev(ydata), 2)
                y = [i/max(ydata) + shift + (len(data) - data.index(ydata) - 1) for i in ydata]

                plt.plot(x, y, label='%s (std dev = %s)' % (noExtension, stddev))

        # plt.ylim((0, shift + len(data) + 0.1))
        # plt.xlabel('Time [s]')
        # plt.ylabel('Intensity (normalised)')
        plt.legend()
        plt.show()

    elif option == 2:
        print('option2')

        yaxis = []
        alldeviations = []

        number = 0

        for file in Folder().iterateCSVThroughFolder():
            number += 2

            CSV = CSVFile(file[0], file[1])
            noExtension, theExposure = CSV.getLabParams()
            xdata, data = CSV.getData()
            x = [i * theExposure for i in xdata]
            print('\n%s' %noExtension)
            deviations = []
            for ydata in data:
                number += 1
                stddev = round(statistics.stdev(ydata), 2)
                print('Pixel %s: %s' % (data.index(ydata), stddev))
                deviations.append(stddev)

                yaxis.append()
            mean = numpy.mean(deviations)
            print('Mean = %s' % mean)
            alldeviations.append(mean)


    else:
        print('Option not recognised.')




