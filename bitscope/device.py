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
        self.channels = [ Channel(self.id, channel) for channel in range(0,BL_Count(BL_SELECT_CHANNEL))]
    
    def select(self):
        # check if the required device is selected
        if self.id != BL_Select(BL_SELECT_DEVICE,BL_ASK):
            # select the corresponding device first
            BL_Select(BL_SELECT_DEVICE,self.id)
        # print "Selected Device : {}".format(self.id)
    
    def mode(self, mode):
        self.select()
        # select the mode
        BL_Mode(mode)
        self.mode = mode
        print "Device : {} set to Mode : {}".format(self.id,self.mode)    