from hilo import Folder, TiffImage
from matplotlib import pyplot as plt


def getIlluminationType(string):
    if 'speckles' in string:
        return True
    elif 'uniform' in string:
        return False
    else:
        return None


def getExposureTime(string):
    return float(''.join(i for i in string if i.isdigit()))


wantedFolder = Folder()
print('... Uploading datafiles from %s' % wantedFolder.directory)
wantedFiles = wantedFolder.iterateThroughFolder('tiff')

print('... Processing images')

xSpeckles = []
ySpeckles = []

xUniform = []
yUniform = []

for j in sorted(wantedFiles):
    directory, name = wantedFiles[j]

    image = TiffImage('%s/%s' % (directory, name))
    array = image.turnIntoArray()
    mean = array.getMean()

    illtype = getIlluminationType(name)
    exptime = getExposureTime(name)

    print(name)

    if illtype is True:
        xSpeckles.append(exptime)
        ySpeckles.append(mean)
    elif illtype is False:
        xUniform.append(exptime)
        yUniform.append(mean)
    else:
        continue

print(len(xSpeckles), len(ySpeckles))
# print(xSpeckles, ySpeckles)
print(len(xUniform), len(yUniform))
# print(xUniform, yUniform)


plt.plot(xSpeckles, ySpeckles, 'o', color='red', label='Speckles')
plt.plot(xUniform, yUniform, 'o', color='blue', label='Uniform')

plt.xlabel('Time [ms]')
plt.ylabel('Std dev (mean)')
plt.legend()
# plt.show()


plt.savefig('%s/%s' % (wantedFolder.directory, '#ALL'))

