from hilo import Folder, TiffImage, StackArray
import os
from matplotlib import pyplot as plt


wantedFolder = Folder()
wantedFiles = wantedFolder.iterateThroughFolder('tiff')
print('... Datafiles are uploading from %s' % wantedFolder.directory)

arrays = []
for j in sorted(wantedFiles):
    directory, name = wantedFiles[j]

    image = TiffImage('%s' % os.path.join(directory, name))

    array = image.returnArray()

    arrays.append(array)

stack = StackArray(arrays)
print(stack.shape)

dev = stack.stddev()
print(dev.shape)

plt.figure()
plt.hist(dev.ravel(), bins=100)
plt.show()
