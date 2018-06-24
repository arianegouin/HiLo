from hilo import Folder, TiffImage
import os
from matplotlib import pyplot as plt
import numpy


wantedFolder = Folder('Select folder with acquired data.')
print('... Uploading datafiles from %s' % wantedFolder.directory)
wantedFiles = wantedFolder.iterateThroughFolder('tiff')

newFigPath = '%s/IntensityAgainstTime' % Folder('Select folder where pyplot figure will be saved.').directory
# newFigPath = '%s/IntensityAgainstTime' % r"C:\Users\Ariane Gouin\Documents\ULaval\2018_Ete\cervo\P3_francois\fridayresults"
if not os.path.exists(newFigPath):
    os.makedirs(newFigPath)

exptime = input('Exposure time (ms): ')
exptimefloat = float(exptime) / 1000
illumtype = input('Illumination type (speckles / uniform): ')
newFigName = '%sms %s' % (exptime, illumtype)

print('... Processing images')

i = 0
x = []
y = []

for j in sorted(wantedFiles):
    directory, name = wantedFiles[j]
    i += 1
    x.append(i * exptimefloat)

    image = TiffImage('%s' % os.path.join(directory, name))

    array = image.turnIntoArray()

    integratedArea = array.sumAllPixels()
    # integratedArea = array.getMean()
    y.append(integratedArea)

mean = numpy.mean(y)
y = y / mean

plt.plot(x, y, marker='o', markerfacecolor='white', markersize=3, linestyle='-', linewidth=1, label='Exposure time = %sms \nIllumination type = %s' % (exptime, illumtype))

plt.tick_params(axis='both', direction='in')
plt.xlabel('Time [s]')
plt.ylabel("Sum of all pixels' intensity")
plt.legend()

plt.savefig('%s/%s' % (newFigPath, newFigName), bbox_inches='tight')
plt.show()
print('... Has saved figure to %s' % os.path.join(newFigPath, newFigName))
