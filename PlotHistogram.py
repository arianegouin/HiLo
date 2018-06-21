from hilo import File, TiffImage
from matplotlib import pyplot as plt

wantedFile = File()

image = TiffImage('%s/%s' % (wantedFile.directory, wantedFile.name))
array = image.returnArray()

plt.hist(array.ravel(), bins=100)

plt.title('Distribution of standard deviations')
plt.xlabel('Standard deviations')

nameNoExtension = wantedFile.name.split('.')[0]
plt.savefig('%s/%s' % (wantedFile.directory, nameNoExtension))
print('... Has saved figure to %s/%s' % (wantedFile.directory, nameNoExtension))
