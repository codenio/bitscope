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
print "Name = {}, Version = {}, ID = {}, Count = {}".format(scope.name,scope.version,scope.id,scope.count)

# select the channel A, using the individual selection options available
scope.select.device(0)
scope.select.mode(BL_MODE_FAST)
scope.select.channel(1)

# get the probe object
probeA = scope.select.probes

# configure the probe object
probeA.source()
probeA.rate()
probeA.size()
probeA.pre_capture()
probeA.post_capture()

# enable the selected probe
probeA.enable()

# trace and get data from probe A
BL_Trace(0.01,BL_SYNCHRONOUS)
Data = BL_Acquire()

# plot the received data from channel A
plt.plot(x,np.array(Data))

# select the channel B, using the individual probe selection option directly
probeB = scope.select.probe(0,BL_MODE_FAST,2)

# configure the probe
probeB.configure()

# enable the probe B
probeB.enable()

BL_Trace(0.01,BL_SYNCHRONOUS)
Data = BL_Acquire()

# create a new window
plt.figure()

# plot the received data from channel B
plt.plot(x,np.array(Data))

# show the plots
plt.show()