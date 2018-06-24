from hilo import File, Folder, TiffImage
from matplotlib import pyplot as plt
import numpy

# wantedFile = File()
# print("... File '%s' uploaded from '%s'" % (wantedFile.name, wantedFile.directory))

wantedFolder = Folder()
print('... Uploading datafiles from %s' % wantedFolder.directory)

for i in wantedFolder.getFiles('tiff'):
    directory, name = i
    nameNoExtension = name.split( '.')[0]

    image = TiffImage('%s/%s' % (directory, name))
    array = image.returnArray()

    meandev = numpy.mean(array)

    # maximum = numpy.amax(array)
    # minimum = numpy.amin(array)

    plt.hist(array.ravel(), bins=200, label='%s' % nameNoExtension)

    plt.title('Distribution (mean=%s)' % meandev)
    plt.xlabel('Standard deviations')
    plt.ylabel('Number of pixels')
    plt.legend(loc=1, edgecolor='black')

    plt.savefig('%s/%s' % (directory, nameNoExtension))
    plt.show()
    print("... Has saved figure '%s' to '%s" % (nameNoExtension, directory))
