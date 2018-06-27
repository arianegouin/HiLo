from hilo import *
from matplotlib import pyplot as plt
from matplotlib import rcParams


class hilo:

    def __init__(self):
        # self.mainFolder = Folder(os.getcwd())
        # self.mainFolder.chooseDirectory('Select the main folder.')
        # self.mainFolder = Folder(r"C:\Users\Ariane Gouin\Documents\doc")
        self.mainFolder = Folder(r"C:\Users\Ariane Gouin\Documents\ULaval\2018_Ete\cervo\P3_francois\friday")

        print('The main folder is: ', self.mainFolder.directory)

        self.raw = self.GetDataPaths()

    @staticmethod
    def getIlluminationType(string):
        if 'speckles' in string:
            return 'speckles'
        elif 'uniform' in string:
            return 'uniform'
        else:
            return None

    @staticmethod
    def getExposureTime(string):
        return int(string.split('ms')[0])

    def GetDataPaths(self):
        subFolders = [Folder('%s/%s' % (self.mainFolder.directory, e)) for e in self.mainFolder.getFolders()]

        wantedData = {}
        for subFolder in subFolders:
            exptime = hilo.getExposureTime(os.path.basename(subFolder.directory))
            illumtype = hilo.getIlluminationType(os.path.basename(subFolder.directory))

            wantedFolder = subFolder
            if subFolder.hasFile('tiff') is True:
                pass
            elif subFolder.hasFolder() is True:
                wantedFolder = Folder('%s/%s' % (subFolder.directory, subFolder.getFolders()[0]))

            wantedFiles = wantedFolder.iterateThroughFolder('tiff')
            wantedData[exptime, illumtype] = wantedFiles

        return wantedData

    def GetDataAsArrays(self, dataset):
        datasetPath = self.raw[dataset][0]
        for j in sorted(self.raw[dataset][1]):
            image = TiffImage(self.raw[dataset][0] + '/%s' % self.raw[dataset][1][j])
            array = image.turnIntoArray()
            image.close()
            yield j, array

    @staticmethod
    def createFolder(path):
        if not os.path.exists(path):
            os.makedirs(path)

    def PlotIntensityAgainstTime(self):

        newFolderPath = '%s/%sResults/IntensityAgainstTime' % (os.path.dirname(self.mainFolder.directory), os.path.basename(self.mainFolder.directory))
        hilo.createFolder(newFolderPath)

        for dataset in self.raw:
            exptime = dataset[0]
            illumtype = dataset[1]

            x = []
            y = []
            for j, array in self.GetDataAsArrays(dataset):
                x.append(j * exptime / 1000)
                mean = array.getMean()
                y.append(mean)
            mean = numpy.mean(y)
            y = y / mean

            plt.plot(x, y, marker='o', markerfacecolor='white', markersize=3, linestyle='-', linewidth=1,
                     label='Exposure time = %sms \nIllumination type = %s' % (exptime, illumtype))
            rcParams.update({'font.size': 18})
            plt.xlabel('Time [s]')
            plt.ylabel("Mean of pixels intensity (normalised)")
            plt.tick_params(axis='both', direction='in')
            plt.legend()

            name = '%sms %s' % (exptime, illumtype)
            plt.savefig('%s/%s' % (newFolderPath, name), bbox_inches='tight')
            plt.show()

        print('... Has saved figures at %s' % newFolderPath)

    def NormaliseAndSave(self):
        for dataset in self.raw:

            newFolderPath = '%s/normalised' % self.raw[dataset][0]
            hilo.createFolder(newFolderPath)

            for j, array in self.GetDataAsArrays(dataset):
                array.normalise()
                array.saveImage('%s/%s.tiff' % (newFolderPath, j))
                yield j, array

            yield 'dataset', dataset

        print('... Has saved normalised datafiles at .../normalised')

    def GetStddevAndSave(self):

        newFolderPath = '%s/%sResults/Stddev' % (os.path.dirname(self.mainFolder.directory), os.path.basename(self.mainFolder.directory))
        hilo.createFolder(newFolderPath)

        arrays = []
        for i in self.NormaliseAndSave():

            if i[0] == 'dataset':
                newdataset = True
            else:
                newdataset = False

            if newdataset is False:
                arrays.append(i[1].array)
            else:
                print(i[1])
                zstack = StackedArray(arrays)
                arrays = []

                dev = zstack.relativeDeviationAlongZ()
                # print('Shape of 2D image of std dev: ', dev.shape)

                exptime = i[1][0]
                illumtype = i[1][1]
                name = '%sms %s.tiff' % (exptime, illumtype)
                dev.saveImage('%s/%s' % (newFolderPath, name))

        print("... Has saved tiff images of relative standard deviation at %s" % newFolderPath)

    def PlotHistogram(self):

        newFolderPath = '%s/%sResults/Stddev' % (
        os.path.dirname(self.mainFolder.directory), os.path.basename(self.mainFolder.directory))
        if not os.path.exists(newFolderPath):
            os.makedirs(newFolderPath)

        rcParams.update({'font.size': 18})
        plt.xlabel('Standard deviations')
        plt.ylabel('Number of pixels')

        allStdev = self.GetStddevAndSave()
        for dataset in allStdev:
            exptime = dataset[0]
            illumtype = dataset[1]

            array = allStdev[dataset].array
            meandev = numpy.mean(array)
            plt.hist(array.ravel(), bins=200,
                     label='Exposure time = %s \nIllumination type = %s' % (exptime, illumtype))
            plt.title('Distribution (mean=%s)' % meandev)
            plt.legend(loc=1, edgecolor='black')

            name = '%sms %s' % (exptime, illumtype)
            plt.savefig('%s/%s' % (newFolderPath, name), bbox_inches='tight')
            plt.show()
        print("... Has saved histograms to '%s" % newFolderPath)


a = hilo()
# b = a.GetDataPaths()
# for i in b:
#     d = a.GetDataAsArrays(i)
# d = a.PlotIntensityAgainstTime()
e = a.NormaliseAndSave()
# for i in e:
#     print(i)
# f = a.GetStddevAndSave()
# g = a.PlotHistogram()

