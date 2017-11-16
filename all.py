"""
DAQ code for HEBI and LABJACK

"""
import os
os.environ['HEBI_C_LIB'] = '/Users/murat/Work/Temporary_Work/DAQ_Py/Hebi_Py/lib/libhebi.dylib'

from hebi import *
from time import sleep

from labjack import ljm
import time
import sys
import utility_functions as uf
import numpy as np
import datetime


servo_neutral = 1500
motor_neutral = 1040


# Open first found LabJack
handle = ljm.open(ljm.constants.dtANY, ljm.constants.ctANY, "ANY")
#handle = ljm.openS("ANY", "ANY", "ANY")

info = ljm.getHandleInfo(handle)
print("Opened a LabJack with Device type: %i, Connection type: %i,\n" \
    "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" % \
    (info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5]))



# Open the HEBI
lookup = Lookup()
group = lookup.get_group_from_names(['X5-1'], ['X-00425'])

if not group:
  print('Group not found!')
  exit(1)


# Init position
position_rad = 0.451
# global actual_position

actual_position = 0.5

def update_position(value):
  global actual_position
  actual_position = value


# Sets the command lifetime to 100 milliseconds
group.set_command_lifetime_ms(100)

# Nm/rad
#spring_constant = -0.5
group_command = GroupCommand(group.size)

# HEBI feedback Handler
def feedback_handler(group_fbk):
  # Uncomment to print out the actual position
  #print("Position :", group_fbk.position)
  update_position(group_fbk.position)
  group_command.set_position([position_rad])
  # group_command.set_effort(spring_constant * group_fbk.position)
  group.send_command(group_command)


# Labjack
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

############ Configure for Servo ################
# Configure Clock Registers:
ljm.eWriteName(handle, "DIO_EF_CLOCK0_ENABLE", 0)   # Disable clock source
# Set Clock0's divisor and roll value to configure frequency: 80MHz/1/1600000 = 50Hz
ljm.eWriteName(handle, "DIO_EF_CLOCK0_DIVISOR", 1)  # Configure Clock0's divisor
ljm.eWriteName(handle, "DIO_EF_CLOCK0_ROLL_VALUE", 1600000) # Configure Clock0's roll value for 50Hz
ljm.eWriteName(handle, "DIO_EF_CLOCK0_ENABLE", 1)   # Enable the clock source

# Configure EF Channel Registers:
ljm.eWriteName(handle, "DIO0_EF_ENABLE", 0)  # Disable the EF system for initial configuration
ljm.eWriteName(handle, "DIO0_EF_INDEX", 0)   # Configure EF system for PWM
ljm.eWriteName(handle, "DIO0_EF_OPTIONS", 0) # Configure what clock source to use: Clock0
ljm.eWriteName(handle, "DIO0_EF_CONFIG_A", uf.pwm_val(servo_neutral)) # Configure duty cycle to so that PWM is 1500ms
ljm.eWriteName(handle, "DIO0_EF_ENABLE", 1) # Enable the EF system, PWM wave is now being outputted

ljm.eWriteName(handle, "DIO2_EF_ENABLE", 0)  # Disable the EF system for initial configuration
ljm.eWriteName(handle, "DIO2_EF_INDEX", 0)   # Configure EF system for PWM
ljm.eWriteName(handle, "DIO2_EF_OPTIONS", 0) # Configure what clock source to use: Clock0
ljm.eWriteName(handle, "DIO2_EF_CONFIG_A", uf.pwm_val(servo_neutral)) # Configure duty cycle to be: 50%
ljm.eWriteName(handle, "DIO2_EF_ENABLE", 1) # Enable the EF system, PWM wave is now being outputted

ljm.eWriteName(handle, "DIO3_EF_ENABLE", 0)
ljm.eWriteName(handle, "DIO3_EF_INDEX", 0)
ljm.eWriteName(handle, "DIO3_EF_OPTIONS", 0)
ljm.eWriteName(handle, "DIO3_EF_CONFIG_A", uf.pwm_val(motor_neutral))
ljm.eWriteName(handle, "DIO3_EF_ENABLE", 1)

ljm.eWriteName(handle, "DIO4_EF_ENABLE", 0)
ljm.eWriteName(handle, "DIO4_EF_INDEX", 0)
ljm.eWriteName(handle, "DIO4_EF_OPTIONS", 0)
ljm.eWriteName(handle, "DIO4_EF_CONFIG_A", uf.pwm_val(motor_neutral))
ljm.eWriteName(handle, "DIO4_EF_ENABLE", 1)
#################################################
time.sleep(2)
print("\nStarting %s read loops.%s" % (str(loopAmount), s))
delay = 0.007 #delay between readings (in sec)
duration = 5.0 # Seconds


group.add_feedback_handler(feedback_handler)
# Control the robot at 100Hz for 30 seconds
group.set_feedback_frequency(100)



pwm = (1400,1400,1500,1500)
print("Servo Values changed")

# Start a file
datenow = datetime.datetime.now()
filename = datenow.strftime("%d_%m_%y__%H_%M")

log_file = open(filename, "w")


def go_to_position(desired_position):
  error = desired_position - actual_position
  while abs(error) > 0.05:
    new_position = actual_position + uf.bound(error, 0.05)
    position_rad = uf.bound_arm(new_position)
    error = desired_position - actual_position

go_to_position(0.6)


uf.update_control_inputs(handle, pwm)

loopAmount = int(duration/delay)

def do_measurement(number):
  i = 0
  while i < number:
    try:
        results = ljm.eReadNames(handle, numFrames, names)
        #R = uf.signal_to_force(results)
        R = results
        # uf.update_control_inputs(handle, pwm)
        #print("%f  %f  %f  %f  %f  %f  %f  %f  %f  %f  %f  %f  %f " % (time.time(), R[0], R[1], R[2], R[3], R[4], R[5], results[6], pwm[0], pwm[1], pwm[2], pwm[3], actual_position) )
        log_file.write("%f  %f  %f  %f  %f  %f  %f  %f  %f  %f  %f  %f  %f \n" % (time.time(), R[0], R[1], R[2], R[3], R[4], R[5], results[6], pwm[0], pwm[1], pwm[2], pwm[3], actual_position))

        time.sleep(delay)
        i = i + 1
    except KeyboardInterrupt:
        break
    except Exception:
        import sys
        print(sys.exc_info()[1])
        break


do_measurement(loopAmount)

# while i < loopAmount:
#     try:
#         results = ljm.eReadNames(handle, numFrames, names)
#         #R = uf.signal_to_force(results)
#         R = results
#         # uf.update_control_inputs(handle, pwm)
#         #print("%f  %f  %f  %f  %f  %f  %f  %f  %f  %f  %f  %f  %f " % (time.time(), R[0], R[1], R[2], R[3], R[4], R[5], results[6], pwm[0], pwm[1], pwm[2], pwm[3], actual_position) )
#         log_file.write("%f  %f  %f  %f  %f  %f  %f  %f  %f  %f  %f  %f  %f \n" % (time.time(), R[0], R[1], R[2], R[3], R[4], R[5], results[6], pwm[0], pwm[1], pwm[2], pwm[3], actual_position))

#         time.sleep(delay)
#         i = i + 1
#     except KeyboardInterrupt:
#         break
#     except Exception:
#         import sys
#         print(sys.exc_info()[1])
#         break

pwm = (1400,1400,1040,1040)

uf.update_control_inputs(handle, pwm)




log_file.close()

# Clear HEBI handler
group.clear_feedback_handlers()

# Close handle
ljm.close(handle)
# IvyStop()
