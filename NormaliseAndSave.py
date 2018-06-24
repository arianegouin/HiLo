from hilo import Folder, TiffImage, TiffArray, StackedArray
import os


wantedFolder = Folder()
print('... Uploading datafiles from %s' % wantedFolder.directory)
wantedFiles = wantedFolder.iterateThroughFolder('tiff')

newFolderPath = '%s/normalised' % wantedFolder.directory
if not os.path.exists(newFolderPath):
    os.makedirs(newFolderPath)

print('... Normalising each image')

arrays = []
for j in sorted(wantedFiles):
    directory, name = wantedFiles[j]

    image = TiffImage('%s/%s' % (directory, name))
    tiffarray = image.turnIntoArray()
    tiffarray.normalise()

    array = image.returnArray()
    arrays.append(array)

    image.close()

print('... Stacking images')
zstack = StackedArray(arrays)
print('Shape of 3D image: ', zstack.shape)

print('... Normalising Z-stack')
zstack.normalise()

i = -1
for j in sorted(wantedFiles):
    directory, name = wantedFiles[j]
    i += 1
    stack = TiffArray(zstack[i])
    stack.saveImage('%s/%s' % (newFolderPath, name))

print('... Has saved normalised datafiles to %s' % newFolderPath)
