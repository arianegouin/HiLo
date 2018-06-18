
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

    def iterateThroughFolder(self, extension):
        for file in os.listdir(self.directory):
            filestring = os.fsdecode(file)
            if filestring.endswith(".%s" % extension):
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
            exposure = float(exposure.replace(',', '.'))
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
        print('option1')

        number = 0

        for file in Folder().iterateThroughFolder('csv'):
            number += 1

            # plt.figure(number // 1)

            CSV = CSVFile(file[0], file[1])
            noExtension, theExposure = CSV.getLabParams()
            xdata, data = CSV.getData()
            x = [i * theExposure for i in xdata]
            x = x[250:600]
            for ydata in data:
                y = [i/max(ydata) for i in ydata]
                y = y[250:600]
                stddev = statistics.stdev(y)
                y = [i + (len(data) - data.index(ydata) - 1) for i in y]

                plt.plot(x, y, label='%s (std dev = %s)' % (noExtension, stddev))

            plt.ylim(ymin=0)
            plt.xlabel('Time [s]')
            plt.ylabel('Intensity (normalised)')
            plt.legend()

        plt.show()

    elif option == 2:
        print('option2')

        number = 0
        f = 0
        ticks = []
        labels = []

        for file in Folder().iterateThroughFolder('csv'):
            f += 1

            CSV = CSVFile(file[0], file[1])
            noExtension, theExposure = CSV.getLabParams()
            xdata, data = CSV.getData()
            x = [i * theExposure for i in xdata]
            print('\n%s' %noExtension)

            xaxis = []
            deviations = []
            for ydata in data:
                # number += 1
                y = [i/max(ydata) for i in ydata]
                stddev = round(statistics.stdev(y), 2)
                print('Pixel %s: %s' % (data.index(ydata), stddev))

                xaxis.append(number)
                deviations.append(stddev)

            mean = numpy.mean(deviations)
            print('Mean = %s' % mean)

            number += 1
            x = [number]
            y = [mean]

            ticks.append(number)
            labels.append('%s' % noExtension)

            # plt.bar(xaxis, deviations, color='lightgrey', label='%s (mean = %s)' % (noExtension, mean))
            if (f % 2) == 0:
                plt.bar(x, y, color='red')
                number += 1
            else:
                plt.bar(x, y, color='blue')

        plt.ylim(ymin=0)
        plt.ylabel('Standard deviation (normalised)')
        plt.xticks(ticks, labels)
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()

    else:
        print('Option not recognised.')



# from PIL import Image
# import numpy
#
# class Tiff:
#     pass
#
#
# number = 0
# for directory, name in Folder().iterateThroughFolder('tiff'):
#     image = Image.open('%s' % os.path.join(directory, name))
#     # image.show()
#     print(number)
#     imageArray = numpy.array(image)
#     if number == 0:
#         print('yes')
#         imageStack = imageArray
#     else:
#         print('no')
#         numpy.stack((imageStack, imageArray), -1)
#     number += 1
#     print(imageStack.shape)

