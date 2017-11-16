
from labjack import ljm
import numpy as np

def pwm_val(value):
    return int(value/20000.0*1600000.0)
    

def bound_arm(value):
    maxvalue = 1.34
    minvalue = -0.33
    if(value>maxvalue):
        value = maxvalue
    elif(value<minvalue):
        value = minvalue
    return value

def bound(value, maxv):
    if(value>maxv):
        value = maxv
    elif(value< -maxv):
        value = -maxv
    return value


def update_control_inputs(handle, vector):
  ljm.eWriteName(handle, "DIO0_EF_CONFIG_A", pwm_val(vector[0]))
  ljm.eWriteName(handle, "DIO2_EF_CONFIG_A", pwm_val(vector[1]))
  ljm.eWriteName(handle, "DIO3_EF_CONFIG_A", pwm_val(vector[2]))
  ljm.eWriteName(handle, "DIO4_EF_CONFIG_A", pwm_val(vector[3]))

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


B40 = np.array([[0.1476432979106903, 0.14606346189975739, -0.11490651965141296, 0.1375323235988617, 0.09234895557165146, -0.29624149203300476]])
B17 = np.array([[-0.08521055430173874, 0.22347553074359894, -0.10100627690553665, 0.45128822326660156, 0.1454315185546875, 0.5179573893547058]])

def signal_to_force(signal):
	A = np.array([[0.0,0.0,0.0,0.0,0.0,0.0]])
	A[0][0] = signal[0]
	A[0][1] = signal[1]
	A[0][2] = signal[2]
	A[0][3] = signal[3]
	A[0][4] = signal[4]
	A[0][5] = signal[5]
	AB = A-B40
	force = C40.dot(AB.T)
	return force

def get_hebi_from_aircraft_angle(angle):
    return ((angle - 30)*0.0186+0.503)


