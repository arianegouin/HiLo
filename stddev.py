from PIL import Image
import numpy
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os


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


class TiffImage:

    def __init__(self, path):
        self.image = Image.open('%s' % path)

    def show(self):
        self.image.show()

    def returnArray(self):
        return numpy.array(self.image, dtype='float64')

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


class StackArray:

    def __init__(self, stack1, *args):
        self.stack = numpy.stack((stack1, *args), axis=0)

        self.shape = self.stack.shape

    def stddev(self):
        return numpy.std(self.stack, axis=0)


# image0 = TiffImage('0.tiff')
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
# image0 = TiffImage('0.tiff')
# array0 = image0.returnArray()
# # print(array0.ravel().shape)
# plt.hist(array0.ravel(), bins=100)
# # plt.show()
#
# image1 = TiffImage('1.tiff')
# array1 = image1.returnArray()
#
# image2 = TiffImage('2.tiff')
# array2 = image2.returnArray()
#
# stack = StackArray(array0, array1, array2)
# std = stack.stddev()
