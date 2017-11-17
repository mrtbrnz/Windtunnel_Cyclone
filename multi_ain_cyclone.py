"""
Reading multiple analog inputs (AIN) from a LabJack.

"""

from labjack import ljm
import time
import sys
import os
import platform
from ivy.std_api import *
import numpy as np

def pwm(value):
    return int(value/20000.0*1600000.0)

servo_neutral = 1500
motor_neutral = 1040

C17 = np.array([
		[-0.00913,  -0.08197,   0.00814,  -3.33902,  -0.06631,   3.24349 ],
		[ 0.15977,   4.06983,  -0.04982,  -1.98943,   0.02155,  -1.81224 ],
		[ 3.75783,   0.01159,   3.81047,  -0.05917,   3.73985,   0.01544 ],
		[ 0.59718,  24.80018,  20.62192, -12.26305, -21.14349, -11.18867 ],
		[-23.74593, 0.36636,   12.62541,  20.26775,  12.67510, -19.73277 ],
		[ 0.31759,  15.10976,   0.20531,  14.88887,   0.04100,  14.32650 ] ])
C40 = np.array([
		[ 0.10573,  -0.04946,  -0.03339,   6.31374,  -0.04072,  -6.35659 ],
		[ 0.24983,  -7.21789,   0.12016,   3.62807,  -0.08762,   3.70953 ],
		[10.12504,   0.21548,  10.10169,   0.36926,  10.57529,   0.28278 ],
		[-0.00249,  -0.03763,   0.14501,   0.02394,  -0.15264,   0.01486 ],
		[-0.17046,  -0.00215,   0.08486,  -0.03049,   0.08772,   0.03596 ],
		[ 0.00226,  -0.08472,  -0.00019,  -0.08519,   0.00105,  -0.08698 ] ])

if os.getenv('IVY_BUS') is not None:
    IVY_BUS = os.getenv('IVY_BUS')
elif platform.system() == 'Darwin':
    IVY_BUS = "127.0.0.1:2010"
else:
    IVY_BUS = ""

IVY_BUS = "127.0.0.1:2010"

IvyInit("LABJACK", "LABJACK READY")
IvyStart(IVY_BUS)
time.sleep(1)

# Open first found LabJack
handle = ljm.open(ljm.constants.dtANY, ljm.constants.ctANY, "ANY")
#handle = ljm.openS("ANY", "ANY", "ANY")

info = ljm.getHandleInfo(handle)
print("Opened a LabJack with Device type: %i, Connection type: %i,\n" \
    "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" % \
    (info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5]))

# Setup and call eWriteNames to configure AINs on the LabJack.
settling_us_all = 100 # 10^-6 sec
numFrames = 27
names = ["AIN0_NEGATIVE_CH", "AIN0_RANGE", "AIN0_RESOLUTION_INDEX", "AIN0_SETTLING_US",
         "AIN2_NEGATIVE_CH", "AIN2_RANGE", "AIN2_RESOLUTION_INDEX", "AIN2_SETTLING_US",
         "AIN4_NEGATIVE_CH", "AIN4_RANGE", "AIN4_RESOLUTION_INDEX", "AIN4_SETTLING_US",
         "AIN6_NEGATIVE_CH", "AIN6_RANGE", "AIN6_RESOLUTION_INDEX", "AIN6_SETTLING_US",
         "AIN8_NEGATIVE_CH", "AIN8_RANGE", "AIN8_RESOLUTION_INDEX", "AIN8_SETTLING_US",
         "AIN10_NEGATIVE_CH", "AIN10_RANGE", "AIN10_RESOLUTION_INDEX", "AIN10_SETTLING_US",
         "AIN12_RANGE", "AIN12_RESOLUTION_INDEX", "AIN12_SETTLING_US"]

aValues = [  1, 10, 1, settling_us_all,
             3, 10, 1, settling_us_all,
             5, 10, 1, settling_us_all,
             7, 10, 1, settling_us_all,
             9, 10, 1, settling_us_all,
             11, 10, 1,settling_us_all,
                 10, 1,settling_us_all]

ljm.eWriteNames(handle, numFrames, names, aValues)

print("\nSet configuration:")
for i in range(numFrames):
    print("    %s : %f" % (names[i], aValues[i]))

# Setup and call eReadNames to read AINs from the LabJack.
numFrames = 7
names = ["AIN0", "AIN2", "AIN4", "AIN6", "AIN8", "AIN10", "AIN12"]

s = ""
if len(sys.argv) > 1:
    #An argument was passed. The first argument specfies how many times to loop.
    try:
        loopAmount = int(sys.argv[1])
    except:
        raise Exception("Invalid first argument \"%s\". This specifies how many " \
                        "times to loop and needs to be a number." % str(sys.argv[1]))
else:
    #An argument was not passed. Loop an infinite amount of times.
    loopAmount = float("inf")
    s = " Press Ctrl+C to stop."

print("\nStarting %s read loops.%s" % (str(loopAmount), s))
delay = 0.1 #delay between readings (in sec)
duration = 15.0 # Seconds
i = 0
A = np.array([[0.0,0.0,0.0,0.0,0.0,0.0]])
B40 = np.array([[0.1476432979106903, 0.14606346189975739, -0.11490651965141296, 0.1375323235988617, 0.09234895557165146, -0.29624149203300476]])
B17 = np.array([[-0.08521055430173874, 0.22347553074359894, -0.10100627690553665, 0.45128822326660156, 0.1454315185546875, 0.5179573893547058]])

loopAmount = int(duration/delay)

while i < loopAmount:
    try:
        results = ljm.eReadNames(handle, numFrames, names)
        #print("\n %i, Time:%f, AIN0 : %f V, AIN1 : %f V" % (i, time.time(), results[0], results[1]))
        # Function for this
        A[0][0] = results[0]
        A[0][1] = results[1]
        A[0][2] = results[2]
        A[0][3] = results[3]
        A[0][4] = results[4]
        A[0][5] = results[5]
        AB = A-B40
        R = C40.dot(AB.T)
        
        print("%f  %f  %f  %f  %f  %f  %f  %f" % (time.time(), R[0], R[1], R[2], R[3], R[4], R[5], results[6]) )
        # IvySendMsg("LABJACK %f  %f  %f  %f  %f  %f  %f  %f " % (time.time(), R[0], R[1], R[2], R[3], R[4], R[5], results[6]) )
        # Raw values
        #IvySendMsg("LABJACK %f  %f  %f  %f  %f  %f  %f  %f " % (time.time(), results[0], results[1], results[2], results[3], results[4], results[5], results[6]) )
        #print(i, time.time(), results[0], results[1],  results[2], results[3], results[4], results[5])
        time.sleep(delay)
        i = i + 1
    except KeyboardInterrupt:
        break
    except Exception:
        import sys
        print(sys.exc_info()[1])
        break

# Close handle
ljm.close(handle)
IvyStop()