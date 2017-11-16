def bound_arm(value):
    maxvalue = 1.34
    minvalue = -0.33
    if(value>maxvalue):
        value = maxvalue
    elif(value<minvalue):
        value = minvalue
    return value
