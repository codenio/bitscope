#!/usr/bin/env python

from bitlib import *
from bitscope.device import Device
from bitscope.channel import Channel
from bitscope.trace import Trace

# from bitscope.select import Select
# from bitscope.probe import Probe

class Scope:
    """
    scope class to open bitscope modules connected to pc
    """
    devices = []
    tracer = ""
    
    def __init__(self, name, count=1):
        # open 1 unit by default 
        count = BL_Open(name,count)
        # Finds number of Devices, create Device object for each and append in scope.devices
        self.devices = [ Device(device) for device in range(0,BL_Count(BL_COUNT_DEVICE))] 
        # number of corresponding channels
        # instanciate Object from Sub Classess 
        self.tracer = Trace()
        print "Bitscope Micro Units Opened : {}".format(len(self.devices))

    def initialise(self):
        BL_Initialize()

    def open(self):
        BL_Open()
    
    def trace(self, time_out, sync):
        self.tracer.trace(time_out, sync)

    def halt(self):
        BL_Halt()
    
    def version(self, type=BL_VERSION_LIBRARY): 
        if type in [BL_VERSION_DEVICE, BL_VERSION_LIBRARY, BL_VERSION_BINDING]:
            return BL_Version(type)
        else:
            print "Invaild Version Type Specified"

    def close(self):
        BL_Close()

    # def configure(self, range, offset, coupling)
    def __del__(self):
        print "Closing {} Bitscope Micro Units".format(len(self.devices))
        BL_Close()