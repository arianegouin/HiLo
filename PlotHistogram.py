from hilo import File, TiffImage
from matplotlib import pyplot as plt
import numpy

wantedFile = File()
print("... File '%s' uploaded from '%s'" % (wantedFile.name, wantedFile.directory))

image = TiffImage('%s/%s' % (wantedFile.directory, wantedFile.name))
array = image.returnArray()

meandev = numpy.mean(array)

plt.hist(array.ravel(), bins=10000)

plt.title('Distribution (mean=%s)' % meandev)
plt.xlabel('Standard deviations')

nameNoExtension = wantedFile.name.split('.')[0]
plt.savefig('%s/%s' % (wantedFile.directory, nameNoExtension))
# plt.show()
print('... Has saved figure %s to %s' % (nameNoExtension, wantedFile.directory))
