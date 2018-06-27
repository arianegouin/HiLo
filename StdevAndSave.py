from hilo import Folder, TiffImage, StackedArray
import os


wantedFolder = Folder('Select folder with acquired data.')
print('... Uploading datafiles from %s' % wantedFolder.directory)
wantedFiles = wantedFolder.iterateThroughFolder('tiff')

# newFolderPath = '%s/StandardDeviation' % Folder('Select folder where tiff image will be saved.').directory
newFolderPath = '%s/StandardDeviation' % r"C:\Users\Ariane Gouin\Documents\ULaval\2018_Ete\cervo\P3_francois\fridayresults"
if not os.path.exists(newFolderPath):
    os.makedirs(newFolderPath)

exptime = input('Exposure time (ms): ')
illumtype = input('Illumination type (speckles / uniform): ')

print('... Processing images')

arrays = []
for j in sorted(wantedFiles):
    directory, name = wantedFiles[j]

    image = TiffImage('%s/%s' % (directory, name))
    array = image.turnIntoArray()
    arrays.append(array.array)

    # print('... %s on %s' % (j, len(wantedFiles)))

print('... Stacking images')
zstack = StackedArray(arrays)
print('Shape of 3D image: ', zstack.shape)
print('Mean', zstack.getMean())

print('... Computing std deviations')
dev = zstack.relativeDeviationAlongZ()
print('Shape of 2D image of std dev: ', dev.shape)

name = '%sms %s.tiff' % (exptime, illumtype)
dev.saveImage('%s/%s' % (newFolderPath, name))
print("... Has saved tiff image of standard deviation for each pixel '%s' at %s" % (name, newFolderPath))
