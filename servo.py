"""
Enables a 10 kHz PWM output on FIO0, enables a high-speed counter on DIO18/CIO2,
waits 1 second and reads the counter. Jumper FIO0 to CIO2 and the read value
should return around 10000.

DIO extended features, PWM output and high-speed counter documented here:

https://labjack.com/support/datasheets/t7/digital-io/extended-features
https://labjack.com/support/datasheets/t7/digital-io/extended-features/pwm-out
https://labjack.com/support/datasheets/t7/digital-io/extended-features/high-speed-counter

"""

from labjack import ljm
import time

# Open first found LabJack.
handle = ljm.openS("ANY", "ANY", "ANY")
#handle = ljm.open(ljm.constants.dtANY, ljm.constants.ctANY, "ANY")

info = ljm.getHandleInfo(handle)
print("Opened a LabJack with Device type: %i, Connection type: %i,\n" \
    "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" % \
    (info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5]))

# How this PWM thing works:
# 1 sec is 1000000msec and we work in 50Hz
# >>> 1000000.0/50.0
# Each roll is 20000msec 
# 20000.0
# 10% duty cycle means 
# >>> 20000.0/10
# 2000.0 msec
# >>> 110000/1600000
# 0
# >>> 110000.0/1600000.0
# 0.06875
# >>> 110000.0/1600000.0*20000.0
# 1375.0 msec

def pwm(value):
	return int(value/20000.0*1600000.0)

servo_neutral = 1500
motor_neutral = 1040

# Configure Clock Registers:
ljm.eWriteName(handle, "DIO_EF_CLOCK0_ENABLE", 0) 	# Disable clock source
# Set Clock0's divisor and roll value to configure frequency: 80MHz/1/1600000 = 50Hz
ljm.eWriteName(handle, "DIO_EF_CLOCK0_DIVISOR", 1) 	# Configure Clock0's divisor
ljm.eWriteName(handle, "DIO_EF_CLOCK0_ROLL_VALUE", 1600000) # Configure Clock0's roll value for 50Hz
ljm.eWriteName(handle, "DIO_EF_CLOCK0_ENABLE", 1) 	# Enable the clock source

# Configure EF Channel Registers:
ljm.eWriteName(handle, "DIO0_EF_ENABLE", 0)  # Disable the EF system for initial configuration
ljm.eWriteName(handle, "DIO0_EF_INDEX", 0)   # Configure EF system for PWM
ljm.eWriteName(handle, "DIO0_EF_OPTIONS", 0) # Configure what clock source to use: Clock0
ljm.eWriteName(handle, "DIO0_EF_CONFIG_A", pwm(servo_neutral)) # Configure duty cycle to so that PWM is 1500ms
ljm.eWriteName(handle, "DIO0_EF_ENABLE", 1) # Enable the EF system, PWM wave is now being outputted

ljm.eWriteName(handle, "DIO2_EF_ENABLE", 0)  # Disable the EF system for initial configuration
ljm.eWriteName(handle, "DIO2_EF_INDEX", 0)   # Configure EF system for PWM
ljm.eWriteName(handle, "DIO2_EF_OPTIONS", 0) # Configure what clock source to use: Clock0
ljm.eWriteName(handle, "DIO2_EF_CONFIG_A", pwm(servo_neutral)) # Configure duty cycle to be: 50%
ljm.eWriteName(handle, "DIO2_EF_ENABLE", 1) # Enable the EF system, PWM wave is now being outputted

ljm.eWriteName(handle, "DIO3_EF_ENABLE", 0)
ljm.eWriteName(handle, "DIO3_EF_INDEX", 0)
ljm.eWriteName(handle, "DIO3_EF_OPTIONS", 0)
ljm.eWriteName(handle, "DIO3_EF_CONFIG_A", pwm(motor_neutral))
ljm.eWriteName(handle, "DIO3_EF_ENABLE", 1)

ljm.eWriteName(handle, "DIO4_EF_ENABLE", 0)
ljm.eWriteName(handle, "DIO4_EF_INDEX", 0)
ljm.eWriteName(handle, "DIO4_EF_OPTIONS", 0)
ljm.eWriteName(handle, "DIO4_EF_CONFIG_A", pwm(motor_neutral))
ljm.eWriteName(handle, "DIO4_EF_ENABLE", 1)

#Process to reconfigure PWM frequency of active EF Channel:
# Set Clock0's divisor and roll value to configure frequency: 80MHz/1/1600000 = 50Hz
#ljm.eWriteName(handle, "DIO_EF_CLOCK0_DIVISOR", 1) 	# Re-configure Clock0's divisor
#ljm.eWriteName(handle, "DIO_EF_CLOCK0_ROLL_VALUE", 1600000) 	# Re-configure Clock0's roll value

# Process to reconfigure PWM Duty Cycle of active EF Channel:
time.sleep(5)

ljm.eWriteName(handle, "DIO0_EF_CONFIG_A", pwm(1400)) 
ljm.eWriteName(handle, "DIO2_EF_CONFIG_A", pwm(1400))
ljm.eWriteName(handle, "DIO3_EF_CONFIG_A", pwm(1200))
ljm.eWriteName(handle, "DIO4_EF_CONFIG_A", pwm(1200))
print("Values changed")

time.sleep(10)
# # Configure the PWM output and counter.
# aNames = ["DIO_EF_CLOCK0_DIVISOR", "DIO_EF_CLOCK0_ROLL_VALUE",
#           "DIO_EF_CLOCK0_ENABLE", "DIO0_EF_INDEX",
#           "DIO0_EF_CONFIG_A", "DIO0_EF_ENABLE",
#           "DIO18_EF_INDEX", "DIO18_EF_ENABLE"]
# aValues = [1, 8000,
#            1, 0,
#            2000, 1,
#            7, 1]
# numFrames = len(aNames)
# results = ljm.eWriteNames(handle, numFrames, aNames, aValues)

# Wait 1 second.
#time.sleep(3.0)

# Read from the counter.
# value = ljm.eReadName(handle, "DIO18_EF_READ_A")

# ljm.eWriteName(handle, "DIO0_EF_CONFIG_A", 110000)
# ljm.eWriteName(handle, "DIO2_EF_CONFIG_A", 110000)
# time.sleep(2.0)
# ljm.eWriteName(handle, "DIO0_EF_CONFIG_A", 120000)
# ljm.eWriteName(handle, "DIO2_EF_CONFIG_A", 120000)
# time.sleep(2.0)
# ljm.eWriteName(handle, "DIO0_EF_CONFIG_A", 130000)
# time.sleep(2.0)
# ljm.eWriteName(handle, "DIO0_EF_CONFIG_A", 140000)

# print("\nCounter = %f" % (value))
# t = 0.0
# while (t<3.0):
# 	ljm.eWriteName(handle, "DIO0_EF_CONFIG_A", 110000)
# 	t += 0.1
# 	time.sleep(0.1)

# print("Second value")

# t = 0.0
# while (t<3.0):
# 	ljm.eWriteName(handle, "DIO0_EF_CONFIG_A", 120000)
# 	t += 0.1
# 	time.sleep(0.1)

# # time.sleep(3.0)

# ljm.eWriteName(handle, "DIO0_EF_CONFIG_A", 0)

print("Last value")

# time.sleep(3.0)


# filename = "log_file.txt"
# # Open log file
# log_file = open(filename, "w")

# log_file.write('%s \n' % larg[0])

# # Close the log file
# log_file.close()



# Turn off PWM output and counter
aNames = ["DIO_EF_CLOCK0_ENABLE", "DIO0_EF_ENABLE"]
aValues = [0, 0]
numFrames = len(aNames)
results = ljm.eWriteNames(handle, numFrames, aNames, aValues)

# Close handle
ljm.close(handle)
