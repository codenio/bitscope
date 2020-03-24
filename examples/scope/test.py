#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
# from bitlib import *
from bitscope import *

# initialisation of scope collects all the device data and stores them in
# scope.devices list 
scope = Scope()

# collect the list of devices
devices = scope.devices

# select mode for device 0
devices[0].mode(BL_MODE_FAST)

# select configure 1 form device 0
devices[0].channels[1].configure(BL_ZERO,BL_ZERO,BL_COUPLING_AC,True)

BL_Trace(0.01,BL_SYNCHRONOUS)
Data = BL_Acquire()
print Data

# devices[0].channels[2].configure(BL_ZERO,BL_ZERO,BL_COUPLING_AC,True)

# batch configuration
# for device in devices:
#     device.mode(BL_MODE_FAST)
#     for channel in device.channels:
#         channel.configure(Offset,Range,Coupling,enable)
#     device.trace.Time(sec)

# device.trace(0.01,BL_SYNC)


# # select mode for device 1
# devices[1].mode(BL_MODE_FAST)

# # select configure 1 form device 1
# devices[1].channel[1].configure(1,Offset,Range,Coupling,enable)
# devices[1].channel[2].configure(2,Offset,Range,Coupling,enable)

# configure trace settings either use Rate & Size or Use Time 
# devices[0].trace.Rate(rate,size)
# or 
# devices[0].trace.Time(sec)

# devices[0].trigger.configure(ALevel : Double; AEdge : Integer,Intro,Delay)

# trace
# devices[0].trace()

# acquire
# dataA = devices[0].channel[1].acquire()
# dataB = devices[0].channel[2].acquire()

# devices[1].trace()
# dataC = devices[1].channel[1].acquire()
# dataD = devices[2].channel[2].acquire()

# print dataA
# print dataB

# BL_Open()
# print BL_Count(BL_COUNT_DEVICE)
# devices = [ device for device in range(0,BL_Count(BL_COUNT_DEVICE))]
# print devices
# BL_Close()