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
scope = Scope("",1)

# print some details about the device
print "Name = {}, Version = {}, ID = {}, Count = {}".format(scope.devices[0].name,scope.devices[0].version,scope.devices[0].id,scope.device_count)

# setting mode to device 0 will by default selects the device
scope.devices[0].mode(MODE.FAST)

for channel in scope.devices[0].channels:
    channel.configure(
        source=SOURCE.BNC,
        offset=ZERO,
        range=scope.device_count,
        coupling=COUPLING.RF
    )
    channel.enable()

# trace for a particular device once
scope.tracer.trace(0.01,TRACE.SYNCHRONOUS)

# acurie data from the required device and channel
Data = scope.devices[0].channels[0].acquire()

# plot the received data from channel A
plt.plot(x,np.array(Data),label="Channel A")

# acurie data from the required device and channel
Data = scope.devices[0].channels[1].acquire()

# plot the received data from channel B
plt.plot(x,np.array(Data),label="Channel B")

plt.xlabel("Time in Sec")
plt.ylabel("Voltage")

plt.legend()

# show the plots
plt.show()