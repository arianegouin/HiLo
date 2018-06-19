from stddev import Folder, TiffImage
import os

wantedFolder = Folder()
wantedFiles = wantedFolder.iterateThroughFolder('tiff')
print('... Datafiles are uploading from %s' % wantedFolder.directory)

newFolderPath = '%s/normalised' % wantedFolder.directory
if not os.path.exists(newFolderPath):
    os.makedirs(newFolderPath)

for j in sorted(wantedFiles):
    directory, name = wantedFiles[j]

    image = TiffImage('%s' % os.path.join(directory, name))

    array = image.turnIntoArray()

    array.normalise()

    array.saveImage('%s' % os.path.join(newFolderPath, name))

print('... Normalised datafiles are saved to %s' % newFolderPath)

