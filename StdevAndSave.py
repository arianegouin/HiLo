from hilo import Folder, TiffImage, StackedArray
import os
from matplotlib import pyplot as plt


wantedFolder = Folder()
wantedFiles = wantedFolder.iterateThroughFolder('tiff')
print('... Datafiles are uploading from %s' % wantedFolder.directory)

arrays = []
for j in sorted(wantedFiles):

    print(j)

    directory, name = wantedFiles[j]

    image = TiffImage('%s' % os.path.join(directory, name))

    array = image.returnArray()

    arrays.append(array)

print('... Stacking images')
zstack = StackedArray(arrays)
print('3D image shape: ', zstack.shape)

print('... Computing std deviations')
# dev = zstack.deviationAlongZ()
dev = zstack.arnaud()
print('2D image of std dev: ', dev.shape)

# plt.figure()
# plt.hist(dev.ravel(), bins=100)
# plt.show()

newFolderPath = '%s/stddev' % r"C:\Users\Ariane Gouin\Documents\ULaval\2018_Ete\cervo\P3_francois\results"
if not os.path.exists(newFolderPath):
    os.makedirs(newFolderPath)

name = '%s.tiff' % input('Input tiff file name: ')

dev.saveImage('%s.tiff' % os.path.join(newFolderPath, 'std.tiff'))

print('Tiff image of standard deviation for each pixel saved at %s.tiff' % os.path.join(newFolderPath, name))
