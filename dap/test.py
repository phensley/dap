import time
import sys

for i in range(100):
    time.sleep(.01)
#    sys.stdout.write("\r%d%%" % i)
    amtDone = i / 100.0
    sys.stdout.write("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(amtDone * 50), amtDone * 100))
    sys.stdout.flush()

