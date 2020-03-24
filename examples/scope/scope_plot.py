#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
from bitscope import *

#Setup general parameters for the capture
MY_RATE = 1000000 # default sample rate in Hz we'll use for capture.
MY_SIZE = 12288 # number of samples we'll capture - 12288 is the maximum size

#Vector storing time-data for x-axis
x = np.arange(MY_SIZE)/float(MY_RATE)

# initialise and open the bitscope micro
scope = Scope()

# print some details about the device
print "Name = {}, Version = {}, ID = {}, Count = {}".format(scope.devices[0].name,scope.devices[0].version,scope.devices[0].id,len(scope.devices))


# select device
# scope.devices[0].select()

# setting mode to device 0 will by default selects the device
scope.devices[0].mode(BL_MODE_FAST)

for channel in scope.devices[0].channels:
    channel.configure(BL_SOURCE_BNC,BL_ZERO,BL_ZERO,BL_COUPLING_RF)
    channel.enable()

# select the device 0, channel 0
# scope.devices[0].channels[0].select()

# configuring a channel will by default selects the device and channel
# scope.devices[0].channels[0].configure(BL_SOURCE_BNC,BL_ZERO,BL_ZERO,BL_COUPLING_DC)

# enabling a channel will by default selects the device and channel
# scope.devices[0].channels[0].enable()

# configure tracer
# scope.tracer.configure.rate()
# scope.tracer.configure.time()

# trace for a particular device once
# BL_Trace(0.01,BL_SYNCHRONOUS)
scope.trace(0.01,BL_SYNCHRONOUS)

# select the required device and channel to obtain the data
# scope.devices[0].channels[0].select()
# print "Read data from channel : {}".format(BL_Select(BL_SELECT_CHANNEL,BL_ASK))
# Data = BL_Acquire()

# scope.trace(0.01,BL_SYNCHRONOUS)

# acurie data from the required device and channel
Data = scope.devices[0].channels[0].acquire()

# plot the received data from channel 0
plt.plot(x,np.array(Data))

# create a new window
plt.figure()

# acurie data from the required device and channel
Data = scope.devices[0].channels[1].acquire()

# plot the received data from channel B
plt.plot(x,np.array(Data))

# show the plots
plt.show()