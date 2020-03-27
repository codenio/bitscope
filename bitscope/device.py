#!/usr/bin/env python

from bitlib import *
from bitscope.channel import Channel

class Device:
    """Device class to select and configure devices that are open."""
    name = None
    id = None
    mode = None
    version = None
    channels = None

    def __init__(self,device):
        """Initialise the Device Object.

        :type device: int
        :param device: device id to be initialised
        """
        self.id = device
        BL_Select(BL_SELECT_DEVICE,device)
        self.name = BL_Name()
        self.version = BL_Version(BL_VERSION_DEVICE)
        # Find number of channels in each device and create Channel object for each and append in devices.channels
        self.channels = []
        for channel in range(0,BL_Count(BL_COUNT_ANALOG)):
            self.channels.append(Channel(self.id, channel))
        for channel in range(0,BL_Count(BL_COUNT_LOGIC)):
            self.channels.append(Channel(self.id, channel))
    
    def select(self):
        """Request the selection of a current device.

        :return: current selection is returned.
        """
        # check if the required device is selected
        if self.id != BL_Select(BL_SELECT_DEVICE,BL_ASK):
            # select the corresponding device first
            return BL_Select(BL_SELECT_DEVICE,self.id)
        # print "Selected Device : {}".format(self.id)
    
    def mode(self, mode):
        """Assign mode to the selected device and return the mode if
        successful.

        :type mode: int
        :param mode: Assign mode (BL_MODE_FAST=>SCOPE, BL_MODE_DUAL=>CHOP, BL_MODE_MIXED=>MIXED, BL_MODE_LOGIC=>LOGIC, BL_MODE_STREAM=>STREAM) to the selected device
        :return: return the mode if successful
        """
        self.select()
        if mode in [BL_MODE_FAST, BL_MODE_DUAL, BL_MODE_MIXED, BL_MODE_LOGIC, BL_MODE_STREAM]:
            # select the mode
            BL_Mode(mode)
            self.mode = mode
            print "Device : {} set to Mode : {}".format(self.id,self.mode)