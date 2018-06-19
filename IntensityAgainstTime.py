from stddev import Folder, TiffImage
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
wantedFiles = wantedFolder.iterateThroughFolder('tiff')
print('... Datafiles are uploading from %s' % wantedFolder.directory)

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
print('... Figure has been saved to %s' % os.path.join(newFigPath, newFigName))
