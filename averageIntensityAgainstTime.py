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
                print(row)
                # yield row

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
        # number = []
        # mean = []
        for row in self.read():
            print(row)
        #     nbOfColumns = len(row)
        #     nbOfPoints = round(nbOfColumns/3)
        #
        #     try:
        #         float(row[0])
        #     except ValueError:
        #         continue
        #     else:
        #         number.append(float(row[0]))
        #         mean.append(float(row[1]))
        # return number, mean, deviation


# if __name__ == '__main__':
#
#     inter = float(input("1:A-B-A-B \n2:A-A-B-B \n3:A-B-C-D \n4:A-A-A-A \nChoose an option --> ").strip())
#
#     numberOfFile = 0
#
#     for file in Folder().iterateCSVThroughFolder():
#         numberOfFile += 1
#
#         if inter == 3:
#             if (numberOfFile % 4) == 1:
#                 shift = 3
#             elif (numberOfFile % 4) == 2:
#                 shift = 2
#             elif (numberOfFile % 4) == 3:
#                 shift = 1
#             elif (numberOfFile % 4) == 0:
#                 shift = 0
#             else:
#                 continue
#
#         elif inter == 2:
#             if (numberOfFile % 2) == 1:
#                 shift = 1
#             elif (numberOfFile % 2) == 0:
#                 shift = 0
#             else:
#                 continue
#
#         elif inter == 1:
#             if numberOfFile in (1, 2):
#                 shift = 0
#             elif numberOfFile in (4, 3):
#                 shift = 1
#             else:
#                 continue
#
#         elif inter == 4:
#             shift = 0
#
#         else:
#             print("The input was not recognised.")
#             continue
#
#         CSV = CSVFile(file[0], file[1])
#         noExtension, theExposure = CSV.getLabParams()
#         xdata, ydata, deviationdata = CSV.getData()
#
#         x = [i * theExposure for i in xdata]
#         y = [i/max(ydata) + shift for i in ydata]
#         dev = round(numpy.mean([i/max(ydata) for i in deviationdata]), 2)
#
#         plt.plot(x, y, label='%s (std dev = %s)' % (noExtension, dev))
#
#     if inter in (1, 2):
#         plt.ylim((0, 2.1))
#     elif inter == 2:
#         plt.ylim((0, 4.1))
#     elif inter == 4:
#         plt.ylim((0, 1.1))
#     else:
#         pass
#
#     plt.xlabel('Time [s]')
#     plt.ylabel('Intensity (normalised)')
#     plt.legend()
#     plt.show()


file = CSVFile(r"C:\Users\Ariane Gouin\Documents\ULaval\2018_Ete\cervo\P3_francois\20180612\0results", '200ms during 1min speckles-SPC.csv')
file.read()

