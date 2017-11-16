
from labjack import ljm

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



def update_control_inputs(handle, vector):
  ljm.eWriteName(handle, "DIO0_EF_CONFIG_A", pwm_val(vector[0]))
  ljm.eWriteName(handle, "DIO2_EF_CONFIG_A", pwm_val(vector[1]))
  ljm.eWriteName(handle, "DIO3_EF_CONFIG_A", pwm_val(vector[2]))
  ljm.eWriteName(handle, "DIO4_EF_CONFIG_A", pwm_val(vector[3]))