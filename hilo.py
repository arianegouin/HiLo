from PIL import Image
import numpy
import tkinter as tk
from tkinter import filedialog
import os


class Folder:

    def __init__(self, directory):
        self.directory = directory

    def chooseDirectory(self, message):
        root = tk.Tk()
        root.withdraw()
        root.directory = filedialog.askdirectory(
            initialdir=os.getcwd(), title="%s" % message)
        self.directory = root.directory

    def iterateThroughFolder(self, extension):
        wantedFiles = {}
        for element in sorted(os.listdir(self.directory)):
            string = os.fsdecode(element)
            if string.endswith(".%s" % extension):
                key = string.split('.')[0]
                try:
                    key = int(key)
                except ValueError:
                    pass
                wantedFiles[key] = string
            else:
                continue
        return self.directory, wantedFiles

    def hasFolder(self):
        for element in os.listdir(self.directory):
            if not '.' in element:
                # print(element, 'is a folder')
                return True
                pass

    def getFolders(self):
        folders = []
        for element in os.listdir(self.directory):
            if '.' in element:
                # print('extension', element)
                continue
            folders.append(element)
        return folders

    def hasFile(self, extension):
        for element in os.listdir(self.directory):
            if '.%s' % extension in element:
                # print(element, 'is a file')
                return True
                pass

    def getFiles(self, extension):
        files = []
        for element in os.listdir(self.directory):
            string = os.fsdecode(element)
            if string.endswith(".%s" % extension):
                files.append((self.directory, element))
        return files


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
        a = numpy.asarray(self.image, dtype='float32')
        return a

    def turnIntoArray(self):
        array = numpy.asarray(self.image, dtype='float32')
        return TiffArray(array)

    def close(self):
        self.image.close()


class TiffArray:

    def __init__(self, array):
        self.array = array

        self.shape = self.array.shape
        self.dtype = self.array.dtype

    def show(self):
        print(self.array)

    def sumAllPixels(self):
        return self.array.sum()

    def getMax(self):
        return max(map(max, self.array))

    def getMean(self):
        return numpy.mean(self.array)

    # def normalise(self):
    #     self.array = self.array / self.sumAllPixels()
    def normalise(self):
        self.array = self.array / self.getMean()

    def saveImage(self, name):
        return Image.fromarray(self.array).save('%s' % name)


class StackedArray:

    def __init__(self, tiffarrays, *args):
        self.stack = numpy.stack(tiffarrays, axis=0)

        self.shape = self.stack.shape
        self.dtype = self.stack.dtype

    def __getitem__(self, key):
        return self.stack[int(key)]

    def show(self):
        print(self.stack)

    def getDeviationAlongZ(self):
        return numpy.std(self.stack, axis=0)

    def getMax(self):
        return max([max(map(max, i)) for i in self.stack])

    def getMean(self):
        return numpy.mean(self.stack)

    def getMeanAlongZ(self):
        return numpy.mean(self.stack, axis=0)

    def relativeDeviationAlongZ(self):
        self.getMeanAlongZ()[self.getMeanAlongZ() == 0] = 999999
        if 999999 in self.getMeanAlongZ():
            print('0 were changed.')
        return TiffArray(self.getDeviationAlongZ() / self.getMeanAlongZ())

    def normalise(self):
        self.stack = self.stack / self.getMean()

#
# a = numpy.array([ [ [1, 1, 1111], [2, 2, 2], [3, 3, 3], [4, 4, 4] ], [ [111, 11, 11], [22, 2000, 2222], [33, 33, 33], [44, 44, 44] ] ])
# print(a)
# print(a/10)
# print(numpy.mean(a))

# print(b.meanAlongZ().show())
# b = numpy.array([[1, 1, 1], [2, 2, 2]])
# c = numpy.array([[1, 11, 0], [2, 22, 222]])

# for i in b:
# d = [max(map(max, i)) for i in b]
# print(max(d))
# print(max(map(max, b)))
#
# b = numpy.mean(a)
# print(b)
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
# yourfile = TiffImage(r"C:\Users\Ariane Gouin\Documents\ULaval\2018_Ete\cervo\P3_francois\results\Mean\40ms uniform.tiff")
# yourfile = yourfile.returnArray()
# print(yourfile.shape)
# a = 0
# for i in yourfile:
#     a += 1
# print(a)
# secondfile = TiffImage(r"C:\Users\Ariane Gouin\Documents\ULaval\2018_Ete\cervo\P3_francois\20180620\40ms gain10 uniform\Jun 20, 2018 04-50-10 AM\1.tiff")
# secondfile = secondfile.returnArray()
# print(secondfile)
# stack = StackedArray([yourfile, secondfile])
# mean = stack.meanAlongZ()
# print(mean.show())
# print(max([max(yourfile[i]) for i in range(len(yourfile))]))
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


