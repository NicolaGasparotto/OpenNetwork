from math import log10

f = open('../sources/constants.txt', 'r')
CONSTANTS = {}
for line in f:
    k, v = line.strip().split('=')
    CONSTANTS[k.strip()] = float(v.strip())
f.close()


def from_dB_to_linear(number):
    return 10 ** (number / 10)
