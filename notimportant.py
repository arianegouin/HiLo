from hilo import *


foo_array = [38,26,14,55,31,0,15,8,0,0,0,18,40,27,3,19,0,49,29,21,5,38,29,17,16]
foo = numpy.array(foo_array)
# Compute the median of the non-zero elements
m = 1111111
# Assign the median to the zero elements
foo[foo == 0] = m

if 38 in foo:
    print('yes')

print(foo)

