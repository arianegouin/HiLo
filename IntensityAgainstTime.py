from hilo import Folder, TiffImage
import os
from matplotlib import pyplot as plt


exptime = float(input('Exposure time (s): '))

# newFigPath = input('New figure path: ')
newFigPath = r"C:\Users\Ariane Gouin\Documents\ULaval\2018_Ete\cervo\P3_francois\results\IntensityAgainstTime"

newFigName = input('New figure name: ')

i = 0
x = []
y = []

wantedFolder = Folder()
print('... Uploading datafiles from %s' % wantedFolder.directory)
wantedFiles = wantedFolder.iterateThroughFolder('tiff')

print('... Processing images')
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

plt.savefig(os.path.join(newFigPath, newFigName))
print('... Has saved figure to %s' % os.path.join(newFigPath, newFigName))
