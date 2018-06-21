from PIL import Image
import numpy
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os
import statistics
import itertools


class Folder:

    def __init__(self):
        # root = tk.Tk()
        # root.withdraw()
        # root.directory = filedialog.askdirectory(initialdir=os.getcwd(), title="Select folder with CSV files")
        # self.directory = root.directory
        self.directory = r"C:\Users\Ariane Gouin\Documents\ULaval\2018_Ete\cervo\P3_francois\20180620\40ms gain10 speckles\Jun 20, 2018 04-34-45 AM\normalised"

    def iterateThroughFolder(self, extension):
        wantedFiles = {}
        for file in sorted(os.listdir(self.directory)):
            filestring = os.fsdecode(file)
            if filestring.endswith(".%s" % extension):
                number = float(filestring.split('.')[0])
                # yield os.path.join(self.directory, filestring)
                wantedFiles[number] = [self.directory, filestring]
            else:
                continue
        return wantedFiles


class File:
    def __init__(self):
        root = tk.Tk()
        root.withdraw()
        root.PathAndFilename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Tiff file",
                                                          filetypes=(("TIFF files", "*.tiff"), ("all files", "*.*")))
        self.directory = os.path.split(root.PathAndFilename)[0]
        self.name = os.path.basename(root.PathAndFilename)


class TiffImage:

    def __init__(self, path):
        self.image = Image.open(r"%s" % path, mode='r')

    def show(self):
        self.image.show()

    def returnArray(self):
        # return numpy.array(self.image, dtype='float32')
        a = numpy.asarray(self.image)
        # print(a.dtype)
        return a

    def turnIntoArray(self):
        array = self.returnArray()
        return TiffArray(array)


class TiffArray:

    def __init__(self, array):
        self.array = array

        self.shape = self.array.shape

    def show(self):
        print(self.array)

    def sumAllPixels(self):
        return self.array.sum()

    def normalise(self):
        self.array = self.array / self.sumAllPixels()

    def saveImage(self, name):
        return Image.fromarray(self.array).save('%s' % name)


class StackedArray:

    def __init__(self, stacks, *args):
        self.stack = numpy.stack(stacks, axis=0)

        self.shape = self.stack.shape

    def deviationAlongZ(self):
        # return numpy.std(self.stack, axis=0)
        stacks = self.shape[0]
        lines = self.shape[1]
        columns = self.shape[2]

        alldev = numpy.zeros((lines, columns))
        for j in range(lines):
            for k in range(columns):
                f = []
                for i in range(stacks):
                    f.append(self.stack[:, j, k])
                    # print(i, j, k)
                dev = statistics.stdev(f)
                # print(i, j, k, 'stddev')
                alldev[j, k] = dev
                # print(i, j, k, 'alldev')
            # print('%s' % (j/range(lines)))
        return alldev

    def arnaud(self):
        stacks = self.shape[0]
        lines = self.shape[1]
        columns = self.shape[2]

        alldev = numpy.zeros((lines, columns))
        for y, x in itertools.product(range(lines), range(columns)):
            f = self.stack[:, y, x]
            dev = numpy.std(f)
            alldev[y, x] = dev
        return TiffArray(alldev)


# a = numpy.array([ [ [1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4] ], [ [11, 11, 11], [22, 22, 22], [33, 33, 33], [44, 44, 44] ] ])
# print(a)
# print('\n')
#
# b = a[0, 0]
# print(b)
#
# stack = a.shape[0]
# lines = a.shape[1]
# columns = a.shape[2]
# print(stack, lines, columns)
#
# stacked = numpy.zeros((lines, columns))


# array0 = image0.turnIntoArray()
# array0.normalise()
# array0.saveImage('your_file.tiff')
#
# yourfile = TiffImage('your_file.tiff')
# yourfile = yourfile.returnArray()
#
# stack = StackArray(yourfile, yourfile, yourfile)
# std = stack.stddev()
#
#
#
# image0 = TiffImage(r"C:\Users\Ariane Gouin\Documents\ULaval\2018_Ete\cervo\P3_francois\20180620\40ms gain10 speckles\Jun 20, 2018 04-34-45 AM\normalised\0.tiff")
# array0 = image0.turnIntoArray()
# array0.show()
# # print(array0.ravel().shape)
# plt.hist(array0.ravel(), bins=100)
# plt.show()
#
# image1 = TiffImage('1.tiff')
# array1 = image1.returnArray()
#
# image2 = TiffImage('2.tiff')
# array2 = image2.returnArray()
#
# stack = StackArray(array0, array1, array2)
# std = stack.stddev()
