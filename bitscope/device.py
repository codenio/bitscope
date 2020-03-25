#!/usr/bin/env python

from bitlib import *
from bitscope.channel import Channel

class Device:

    name = ""
    id = ""
    mode = ""
    version = ""
    channels = []

    def __init__(self,device):
        self.id = device
        BL_Select(BL_SELECT_DEVICE,device)
        self.name = BL_Name()
        self.version = BL_Version(BL_VERSION_DEVICE)
        # Find number of channels in each device and create Channel object for each and append in devices.channels
        for channel in range(0,BL_Count(BL_COUNT_ANALOG)):
            self.channels.append(Channel(self.id, channel))
        for channel in range(0,BL_Count(BL_COUNT_LOGIC)):
            self.channels.append(Channel(self.id, channel))
    
    def select(self):
        # check if the required device is selected
        if self.id != BL_Select(BL_SELECT_DEVICE,BL_ASK):
            # select the corresponding device first
            BL_Select(BL_SELECT_DEVICE,self.id)
        # print "Selected Device : {}".format(self.id)
    
    def mode(self, mode):
        self.select()
        if mode in [BL_MODE_FAST, BL_MODE_DUAL, BL_MODE_MIXED, BL_MODE_LOGIC, BL_MODE_STREAM]:
            # select the mode
            BL_Mode(mode)
            self.mode = mode
            print "Device : {} set to Mode : {}".format(self.id,self.mode)    