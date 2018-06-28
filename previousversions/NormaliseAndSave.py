from hilo import Folder, TiffImage, TiffArray, StackedArray
import os


wantedFolder = Folder('Select folder with acquired data.')
print('... Uploading datafiles from %s' % wantedFolder.directory)
wantedFiles = wantedFolder.iterateThroughFolder('tiff')

newFolderPath = '%s/normalised' % wantedFolder.directory
if not os.path.exists(newFolderPath):
    os.makedirs(newFolderPath)

print('... Normalising each image')

for j in sorted(wantedFiles):
    directory, name = wantedFiles[j]

    image = TiffImage('%s/%s' % (directory, name))
    array = image.turnIntoArray()

    # print(array.dtype, array.getMean())

    array.normalise()

    array.saveImage('%s/%s' % (newFolderPath, name))

    image.close()

print('... Has saved normalised datafiles to %s' % newFolderPath)
