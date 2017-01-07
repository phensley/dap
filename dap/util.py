
import sys
from math import log


UNITS = zip(['bytes', 'kB', 'MB', 'GB', 'TB', 'PB'], [0, 0, 1, 2, 2, 2])


def info(m):
    sys.stderr.write(m + '\n')
    sys.stderr.flush()


def sizeof(num):
    if num > 1:
        exponent = min(int(log(num, 1024)), len(UNITS) - 1)
        quotient = float(num) / 1024**exponent
        unit, num_decimals = UNITS[exponent]
        format_string = '{:.%sf} {}' % (num_decimals)
        return format_string.format(quotient, unit)
    if num == 0:
        return '0 bytes'
    if num == 1:
        return '1 byte'

