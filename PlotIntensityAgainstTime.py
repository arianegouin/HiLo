from hilo import Folder, TiffImage
import os
from matplotlib import pyplot as plt
import numpy


wantedFolder = Folder()
print('... Uploading datafiles from %s' % wantedFolder.directory)
wantedFiles = wantedFolder.iterateThroughFolder('tiff')

exptime = float(input('Exposure time (ms): ')) / 1000

print('... Processing images')

i = 0
x = []
y = []

for j in sorted(wantedFiles):
    directory, name = wantedFiles[j]
    i += 1
    x.append(i * exptime)

    image = TiffImage('%s' % os.path.join(directory, name))

    array = image.turnIntoArray()

    integratedArea = array.sumAllPixels()
    # integratedArea = array.getMean()
    y.append(integratedArea)

mean = numpy.mean(y)
y = y / mean

plt.plot(x, y, marker='o', colorfacemarker='black', markersize=5, linestyle='-', linecolor='blue', label='%s ms' % (exptime*1000))

plt.tick_params(axis='both', direction='in')
plt.xlabel('Time [s]')
plt.ylabel("Sum of all pixels' intensity")
plt.legend()

newFigPath = '%s/IntensityAgainstTime' % r"C:\Users\Ariane Gouin\Documents\ULaval\2018_Ete\cervo\P3_francois\fridayresults"
if not os.path.exists(newFigPath):
    os.makedirs(newFigPath)

newFigName = input('New figure name: ')
plt.savefig(os.path.join(newFigPath, newFigName), bbox_inches='tight')
print('... Has saved figure to %s' % os.path.join(newFigPath, newFigName))
