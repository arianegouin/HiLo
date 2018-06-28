from hilo import *
from matplotlib import pyplot as plt

# wantedFolder = Folder(r"C:\Users\Ariane Gouin\Documents\ULaval\2018_Ete\cervo\P3_francois\friday\1300ms speckles gain1\Jun 22, 2018 10-17-54 AM\normalised")
# wantedFiles = wantedFolder.iterateThroughFolder('tiff')
# print(wantedFiles[1])
#
#
# arrays = []
# for i in sorted(wantedFiles[1]):
#     image = TiffImage('%s/%s' % (wantedFiles[0], wantedFiles[1][i]))
#     array = image.turnIntoArray()
#     arrays.append(array.array)
# #
# print('stacking')
# zstack = StackedArray(arrays)
#
# print('...')
# dev = zstack.getRelativeDeviationAlongZ()
#
# print(dev.shape)

a = TiffArray(numpy.array([[0, 1, 1], [0, 1, 10]]))
a.normalise()
a.show()
b = TiffArray(numpy.array([[1, 1, 1], [0, 1, 4]]))
b.normalise()
b.show()
print('\n')

c = StackedArray([a.array, b.array])
print(c.getMean())
print('stack')
c.show()

print('\n')
e = c.getDeviationAlongZ()
print(e)
f = c.getMeanAlongZ()
print(f)

print('\n')
d = c.getRelativeDeviationAlongZ()
d.show()
