from hilo import *
from matplotlib import pyplot as plt
from matplotlib import rcParams
rcParams['font.size'] = 18
from scipy.optimize import curve_fit


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

    @staticmethod
    def createFolder(path):
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def setPlotParams(xlabel, ylabel, legendtitle=None):
        plt.tick_params(axis='both', direction='in')
        plt.legend(loc=0, edgecolor='black', fancybox=False, title=legendtitle)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

    @staticmethod
    def saveFigure(newFolderPath, exptime=None,illumtype=None, othername=None, show=False):
        if othername is not None:
            name = othername
        else:
            name = '%sms %s' % (exptime, illumtype)
        hilo.createFolder(newFolderPath)
        plt.savefig('%s/%s' % (newFolderPath, name), bbox_inches='tight')
        if show is True:
            plt.show()


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

    def GetDataAsArrays(self, dataset, normalised=False):
        datasetPath = self.raw[dataset][0]
        if normalised is True:
            datasetPath += '/normalised'
        for j in sorted(self.raw[dataset][1]):
            path = datasetPath + '/%s' % self.raw[dataset][1][j]
            image = TiffImage(path)
            array = image.turnIntoArray()
            image.close()
            yield j, array


    def ReturnMax(self, dataset):
        maxx = []
        for j, array in self.GetDataAsArrays(dataset):
            maxx.append(array.getMax())
        return maxx, numpy.amax(maxx)

    def ReturnTimes(self, dataset):
        exptime = dataset[0]

        x = []
        for j, array in self.GetDataAsArrays(dataset):
            x.append(j * exptime / 1000)

        return x

    def ReturnMeans(self, dataset):
        y = []
        for j, array in self.GetDataAsArrays(dataset):
            y.append(array.getMean())

        return y, numpy.mean(y)

    def PlotIntensityAgainstTime(self):

        print('... Plotting IntensityAgainstTime')

        newFolderPath = '%s/%sResults/IntensityAgainstTime' % (os.path.dirname(self.mainFolder.directory), os.path.basename(self.mainFolder.directory))

        for dataset in self.raw:
            exptime, illumtype = dataset

            x = self.ReturnTimes(dataset)
            y, m = self.ReturnMeans(dataset)
            y = y / numpy.mean(y)

            maxx, maxxi = self.ReturnMax(dataset)
            print('max of max', maxxi)

            plt.figure()
            plt.plot(x, y, linestyle='-', linewidth=1,
                     label='Exposure time = %sms \nIllumination = %s' % (exptime, illumtype))
            hilo.setPlotParams(xlabel='Time [s]', ylabel='Intensity (normalised mean)')

            hilo.saveFigure(newFolderPath=newFolderPath, exptime=exptime, illumtype=illumtype, show=True)

            print('... ... Has plot', dataset)

        print('... Has saved figures at %s' % newFolderPath)


    def NormaliseAndSave(self):

        for dataset in self.raw:

            print('... ... Has normalised', dataset)

            newFolderPath = '%s/normalised' % self.raw[dataset][0]
            hilo.createFolder(newFolderPath)

            for j, array in self.GetDataAsArrays(dataset):
                array.normalise()
                array.saveImage('%s/%s.tiff' % (newFolderPath, j))
                yield dataset, j, array
            # yield 'dataset', dataset

        print('... Has saved normalised datafiles at .../normalised')

    def FindNormalisedData(self):
        for dataset in self.raw:
            for j, array in self.GetDataAsArrays(dataset, normalised=True):
                yield dataset, j, array

    def GetStdevAndSave(self):

        normalise =  input('Normalise raw data first (y) or go find normalised data (n): ')
        where = self.NormaliseAndSave()
        if normalise == 'n':
            where = self.FindNormalisedData()

        newFolderPath = '%s/%sResults/Stddev' % (os.path.dirname(self.mainFolder.directory), os.path.basename(self.mainFolder.directory))
        hilo.createFolder(newFolderPath)

        nbOfImages = float(input('Number of images per dataset: '))
        arrays = []
        for dataset, j, tiffarray in where:
            exptime, illumtype = dataset

            arrays.append(tiffarray.array)
            print(dataset, len(arrays))

            if len(arrays) == nbOfImages:
                zstack = StackedArray(arrays)
                # print('z stack mean', zstack.getMean())
                print('... ... Has stacked', dataset)
                arrays = []

                dev = zstack.getRelativeDeviationAlongZ()
                # print('std dev max, min', dev.getMax(), dev.getMin())

                dev.saveImage('%s/%sms %s.tiff' % (newFolderPath, exptime, illumtype))
                print('... ... Has saved std dev of', dataset)

                yield dataset, dev

        print("... Has saved tiff images of relative standard deviation at %s" % newFolderPath)


    @staticmethod
    def plotHistogram(dataset, dev, newFolderPath):

        exptime, illumtype = dataset

        meandev = dev.getMean()
        dev.ravel()

        plt.figure()
        plt.hist(dev.array, bins=100,
                 label='Exposure time = %sms \nIllumination = %s' % (exptime, illumtype))
        hilo.setPlotParams(xlabel='Std dev', ylabel='Number of pixels')
        plt.title('Distribution (mean=%s)' % meandev)

        hilo.saveFigure(newFolderPath=newFolderPath, exptime=exptime, illumtype=illumtype, show=True)

        print('... ... Has saved histogram for', dataset)

    def FindStdevData(self):
        folderPath = '%s/%sResults/Stddev' % (os.path.dirname(self.mainFolder.directory), os.path.basename(self.mainFolder.directory))
        for dataset in self.raw:
            exptime, illumtype = dataset
            filePath = '%s/%sms %s.tiff' % (folderPath, exptime, illumtype)
            image = TiffImage(filePath)
            array = image.turnIntoArray()
            image.close()
            yield dataset, array

    def PlotDistributionOfStdev(self):
        newFolderPath = '%s/%sResults/Stddev' % (os.path.dirname(self.mainFolder.directory), os.path.basename(self.mainFolder.directory))

        normalise = input('Compute standard deviations (y) or go find computed standard deviations (n): ')
        where = self.GetStdevAndSave()
        if normalise == 'n':
            where = self.FindStdevData()

        for dataset, dev in where:
            hilo.plotHistogram(dataset, dev, newFolderPath)
        print("... Has saved histograms to '%s'" % newFolderPath)


    @staticmethod
    def getCurvefit(x, y):
        def function(x, a, b):
            return a / (x - b) ** 0.5

        popt, pcov = curve_fit(function, x, y)
        xx = [i for i in range(min(x), max(x), 1)]
        yy = [function(x, *popt) for x in xx]

        return xx, yy, popt

    def PlotStddevAgainstExpTime(self):

        newFolderPath = '%s/%sResults/Stddev' % (os.path.dirname(self.mainFolder.directory), os.path.basename(self.mainFolder.directory))

        normalise = input('Compute standard deviations (y) or go find computed standard deviations (n): ')
        histogram = input('Plot and save histograms (y / n): ')
        curvefit = input('Display curve fit (y / n): ')

        xSpeckles = []
        ySpeckles = []

        xUniform = []
        yUniform = []

        where = self.GetStdevAndSave()
        if normalise == 'n':
            where = self.FindStdevData()

        for dataset, dev in where:

            if histogram == 'y':
                hilo.plotHistogram(dataset, dev, newFolderPath)

            exptime, illumtype = dataset
            if exptime == 40:
                newFigName = '#ALLexcept40ms'
                continue

            if illumtype is 'speckles':
                xSpeckles.append(int(exptime))
                ySpeckles.append(dev.getMean())
            elif illumtype is 'uniform':
                xUniform.append(int(exptime))
                yUniform.append(dev.getMean())

        if curvefit == 'y':
            xxSpeckles, yySpeckles, popt = hilo.getCurvefit(xSpeckles, ySpeckles)
            plt.plot(xxSpeckles, yySpeckles, 'r:', linewidth=1, label='fit: a=%.1f, b=%.1f' % tuple(popt))
            xxUniform, yyUniform, popt = hilo.getCurvefit(xUniform, yUniform)
            plt.plot(xxUniform, yyUniform, 'b:', linewidth=1, label='fit: a=%.1f, b=%.1f' % tuple(popt))

        plt.plot(xSpeckles, ySpeckles, 'o', markersize=10, markerfacecolor='red', markeredgecolor='white',
                 label='Speckles')
        plt.plot(xUniform, yUniform, 'o', markersize=5, markerfacecolor='blue', markeredgecolor='white',
                 label='Uniform')
        hilo.setPlotParams(xlabel='Exposure time [ms]', ylabel='Std dev (mean)', legendtitle='fit: $y = a / \sqrt{(x - b)}$')

        hilo.saveFigure(newFolderPath=newFolderPath, othername='#ALL', show=True)
        print("... Has saved figure to '%s" % newFolderPath)


a = hilo()
# b = a.GetDataPaths()
# for i in b:
#     d = a.GetDataAsArrays(i)
# d = a.PlotIntensityAgainstTime()
# e = a.NormaliseAndSave()
# for i in e:
#     pass
# f = a.GetNormalisedData()
# f = a.GetStdevAndSave()
# for i in f:
#     pass
# g = a.PlotDistributionOfStdev()
h = a.PlotStddevAgainstExpTime()

