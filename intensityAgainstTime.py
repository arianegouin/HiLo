from stddev import Folder, TiffImage, TiffArray
import os
from matplotlib import pyplot as plt


exptime = float(input('Exposure time (s): '))

i = 0
x = []
y = []
for directory, name in Folder().iterateThroughFolder('tiff'):
    print(directory, name)
    i += 1
    x.append(i * exptime)

    image = TiffImage('%s' % os.path.join(directory, name))

    array = image.turnIntoArray()

    integratedArea = array.sumAllPixels()
    y.append(integratedArea)

print(x)
print(y)

plt.plot(x, y, '-')
plt.show()
