from hilo import Folder, TiffImage
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit


def getIlluminationType(string):
    if 'bla' in string:
        return True
        pass
    elif 'speckles' in string:
        return True
    elif 'uniform' in string:
        return False
    else:
        return None


def getExposureTime(string):
    return int(''.join(i for i in string if i.isdigit()))


wantedFolder = Folder('Select folder where tiff images of standard deviations are.')
print('... Uploading datafiles from %s' % wantedFolder.directory)
wantedFiles = wantedFolder.iterateThroughFolder('tiff')

print('... Processing images')

xSpeckles = []
ySpeckles = []

xUniform = []
yUniform = []

newFigName = '#ALL'

for j in sorted(wantedFiles):
    directory, name = wantedFiles[j]

    image = TiffImage('%s/%s' % (directory, name))
    array = image.turnIntoArray()
    mean = array.getMean()

    illtype = getIlluminationType(name)
    exptime = getExposureTime(name)

    print(name)

    # if exptime == 40:
    #     newFigName = '#ALLexcept40ms'
    #     continue

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


def function(x, a, b):
    return a / (x - b)**0.5

popt, pcov = curve_fit(function, xSpeckles, ySpeckles)
xxSpeckles = [i for i in range(min(xSpeckles), max(xSpeckles), 1)]
print(xxSpeckles)
yySpeckles = [function(x, *popt) for x in xxSpeckles]
print(yySpeckles)
plt.plot(xxSpeckles, yySpeckles, 'r:', linewidth=1, label='fit: a=%.1f, b=%.1f' % tuple(popt))

popt, pcov = curve_fit(function, xUniform, yUniform)
xxUniform = [i for i in range(min(xUniform), max(xUniform), 1)]
yyUniform = [function(x, *popt) for x in xxUniform]
plt.plot(xxUniform, yyUniform, 'b:', linewidth=1, label='fit: a=%.1f, b=%.1f' % tuple(popt))


plt.plot(xSpeckles, ySpeckles, 'o', markersize=10, markerfacecolor='red', markeredgecolor='white', label='Speckles')
plt.plot(xUniform, yUniform, 'o', markersize=5, markerfacecolor='blue', markeredgecolor='white', label='Uniform')


plt.tick_params(axis='both', direction='in')
plt.xlabel('Exposure time [ms]')
plt.ylabel('Std dev (mean)')
plt.tight_layout()
plt.legend(loc=0, edgecolor='black', title='fit: $y = a / \sqrt{(x - b)}$')



plt.savefig('%s/%s' % (wantedFolder.directory, newFigName), bbox_inches='tight')
plt.show()
print("... Has saved figure '%s' to '%s" % (newFigName, wantedFolder.directory))

