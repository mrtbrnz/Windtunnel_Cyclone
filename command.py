
import os
os.environ['HEBI_C_LIB'] = '/Users/murat/Work/Temporary_Work/DAQ_Py/Hebi_Py/lib/libhebi.dylib'

from hebi import *
from time import sleep

position_rad = 0.5

lookup = Lookup()
group = lookup.get_group_from_names(['X5-1'], ['X-00425'])

if not group:
  print('Group not found!')
  exit(1)

# Sets the command lifetime to 100 milliseconds
group.set_command_lifetime_ms(100)

# Nm/rad
spring_constant = -0.5
group_command = GroupCommand(group.size)

#info = GroupInfo(group.size)
#info.position_kp(group)

# Set Position PID Gains
# group_command.set_position_kp([0.3])
# group_command.set_position_ki([0.0])
# group_command.set_position_kd([0.0])
# group_command.set_effort_kp([0.5])
# group_command.set_effort_ki([0.0])
# group_command.set_effort_kd([1.0])

def feedback_handler(group_fbk):
  print("Position :", group_fbk.position)
  group_command.set_position([position_rad])
  # group_command.set_effort(spring_constant * group_fbk.position)
  group.send_command(group_command)


group.add_feedback_handler(feedback_handler)
# Control the robot at 100Hz for 30 seconds
group.set_feedback_frequency(100)
sleep(20)
position_rad = 0.6
sleep(10)
position_rad = 0.8
sleep(10)
group.clear_feedback_handlers()
