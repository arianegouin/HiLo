from hilo import Folder, TiffImage
import os

wantedFolder = Folder()
wantedFiles = wantedFolder.iterateThroughFolder('tiff')
print('... Uploading datafiles from %s' % wantedFolder.directory)

newFolderPath = '%s/normalised' % wantedFolder.directory
if not os.path.exists(newFolderPath):
    os.makedirs(newFolderPath)

for j in sorted(wantedFiles):
    directory, name = wantedFiles[j]

    image = TiffImage('%s/%s' % (directory, name))

    array = image.turnIntoArray()

    array.normalise()

    array.saveImage('%s/%s' % (newFolderPath, name))

print('... Has saved normalised datafiles to %s' % newFolderPath)

