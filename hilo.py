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
        self.update()

    def update(self):
        self.shape = self.array.shape
        self.dtype = self.array.dtype

    def ravel(self):
        self.array = self.array.ravel()
        self.update()

    def show(self):
        print(self.array)

    def sumAllPixels(self):
        return self.array.sum()

    def getMax(self):
        return max(map(max, self.array))

    def getMin(self):
        return min(map(min, self.array))

    def getMean(self):
        return numpy.mean(self.array)

    def normalise(self):
        self.array = self.array / self.getMean()
        self.update()

    def saveImage(self, name):
        return Image.fromarray(self.array).save('%s' % name)


class StackedArray:

    def __init__(self, tiffarrays, *args):
        self.stack = numpy.stack(tiffarrays, axis=0)

    def update(self):
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

    def getMaxAlongZ(self):
        return numpy.amax(self.stack, axis=0)

    def getMin(self):
        return min([min(map(min, i)) for i in self.stack])

    def getMean(self):
        return numpy.mean(self.stack)

    def getMeanAlongZ(self):
        return numpy.mean(self.stack, axis=0)

    def getRelativeDeviationAlongZ(self):
        a = self.getDeviationAlongZ()
        # b = self.getMeanAlongZ()
        b = self.getMaxAlongZ()
        condition = (b !=0)
        c = numpy.divide(a, b, out=numpy.zeros_like(a), where=condition)
        return TiffArray(c)

    def normalise(self):
        self.stack = self.stack / self.getMean()
        self.update()
