from hilo import Folder, TiffImage
import os
from matplotlib import pyplot as plt


wantedFolder = Folder()
print('... Uploading datafiles from %s' % wantedFolder.directory)
wantedFiles = wantedFolder.iterateThroughFolder('tiff')

exptime = float(input('Exposure time (s): '))

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
    y.append(integratedArea)


plt.xlabel('Time [s]')
plt.ylabel('Sum of all pixels intensity')
plt.plot(x, y, '-')

# newFigPath = input('New figure path: ')
newFigPath = r"C:\Users\Ariane Gouin\Documents\ULaval\2018_Ete\cervo\P3_francois\results\IntensityAgainstTime"
newFigName = input('New figure name: ')
plt.savefig(os.path.join(newFigPath, newFigName))
print('... Has saved figure to %s' % os.path.join(newFigPath, newFigName))
