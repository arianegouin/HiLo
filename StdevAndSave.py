from hilo import Folder, TiffImage, StackedArray
import os


wantedFolder = Folder()

print('... Uploading datafiles from %s' % wantedFolder.directory)
wantedFiles = wantedFolder.iterateThroughFolder('tiff')

print('... Processing images')

arrays = []
for j in sorted(wantedFiles):
    directory, name = wantedFiles[j]

    image = TiffImage('%s/%s' % (directory, name))
    array = image.returnArray()
    arrays.append(array)

    # print('... %s on %s' % (j, len(wantedFiles)))

print('... Stacking images')
zstack = StackedArray(arrays)
print('Shape of 3D image: ', zstack.shape)

print('... Computing std deviations')
dev = zstack.deviationAlongZ()
print('Shape of 2D image of std dev: ', dev.shape)

# newFolderPath = input('New figure path: ')
newFolderPath = '%s/StandardDeviation' % r"C:\Users\Ariane Gouin\Documents\ULaval\2018_Ete\cervo\P3_francois\results"
if not os.path.exists(newFolderPath):
    os.makedirs(newFolderPath)

name = '%s.tiff' % input('Tiff file of standard deviations should be named: ')
dev.saveImage('%s/%s' % (newFolderPath, name))
print('Tiff image of standard deviation for each pixel saved at %s/%s' % (newFolderPath, name))
